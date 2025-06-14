from copy import deepcopy
from typing import Dict, List, Set, Tuple
from src.model.lr0_item import LR0Item
from src.model.grammar import Grammar
import tempfile


def extend_grammar(grammar: Grammar) -> Grammar:
    """
    Retorna uma nova gramática estendida com:
    1. Um novo símbolo inicial (adicionando "'" ao símbolo original)
    2. Uma nova produção S' → S (onde S é o símbolo inicial original)
    3. Mantém todas as produções originais
    """
    original_start = grammar.get_start_symbol()
    extended_start = f"{original_start}'"
    
    # Cria as produções da gramática estendida
    extended_productions = deepcopy(grammar.get_productions())
    extended_productions[extended_start] = [[original_start]]  # S' → S
    
    # Constrói o conteúdo do arquivo (garantindo que S' aparece primeiro)
    grammar_lines = [f"{extended_start} ::= {original_start}"]  # S' → S primeiro
    
    for head, bodies in extended_productions.items():
        if head == extended_start:
            continue  # Já adicionamos S' → S primeiro
        body_strs = [' '.join(body) for body in bodies]
        grammar_lines.append(f"{head} ::= {' | '.join(body_strs)}")
    
    # Cria e carrega a gramática estendida
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
        temp_file.write('\n'.join(grammar_lines))
        temp_file_path = temp_file.name
    
    extended_grammar = Grammar(temp_file_path)
    return extended_grammar

def get_production_order(grammar: Grammar) -> Dict[Tuple[str, Tuple[str, ...]], int]:
    """
    Retorna um dicionário que mapeia cada produção da gramática para um número inteiro único,
    atribuído de acordo com a ordem em que aparecem na definição da gramática.
    Útil para garantir que a numeração dos estados e transições siga a ordem das produções.
    """
    order = {}
    count = 0
    for head in grammar.get_productions():
        for body in grammar.get_productions()[head]:
            order[(head, tuple(body))] = count
            count += 1
    return order

def closure(grammar: Grammar, items: Set[LR0Item]) -> Set[LR0Item]:
    """
    Calcula o fechamento (closure) de um conjunto de itens LR(0).

    Para cada item A → α • B β no conjunto, se B for um não terminal, 
    adiciona ao conjunto todas as produções de B na forma B → • γ. 
    Repete esse processo até não haver mais itens a adicionar.

    Garante que todas as possíveis derivações indiretas estejam presentes 
    ao construir os estados do autômato LR(0).
    """
    closure_set = set(items) # Inicializa o fechamento com os itens de base fornecidoss
    added = True

    while added:
        added = False
        new_items = set()

        for item in closure_set:
            # Se o ponto não está no final da produção
            if item.dot_pos < len(item.body):
                symbol_after_dot = item.body[item.dot_pos]

                # Verifica se o símbolo após o ponto é um não terminal
                if grammar.is_non_terminal(symbol_after_dot):
                    # Para cada produção do não terminal B, adiciona o item B → • γ
                    for prod_body in grammar.get_productions()[symbol_after_dot]:
                        new_item = LR0Item(symbol_after_dot, tuple(prod_body), 0)
                        # Adiciona o novo item somente se ainda não estiver presente
                        if new_item not in closure_set and new_item not in new_items:
                            new_items.add(new_item)
                            added = True # Marca que houve adição neste ciclo

        closure_set.update(new_items) # Atualiza o conjunto com os novos itens adicionados

    return closure_set


def goto(grammar: Grammar, items: Set[LR0Item], symbol: str) -> Set[LR0Item]:
    """
    Calcula o conjunto de itens alcançável a partir de um conjunto de itens LR(0)
    quando se consome um símbolo específico (shift).

    Move o ponto (•) uma posição à direita nos itens onde o símbolo após o ponto
    é igual ao símbolo dado, e então aplica o fechamento (closure) no resultado.
    """
    moved_items = set()

    for item in items:
        if item.dot_pos < len(item.body) and item.body[item.dot_pos] == symbol:
            moved_items.add(LR0Item(item.head, item.body, item.dot_pos + 1))

    return closure(grammar, moved_items)


def canonical_collection(grammar: Grammar) -> Tuple[List[Set[LR0Item]], Dict[int, Dict[str, str]]]:
    """
    Gera a coleção canônica de conjuntos de itens LR(0) da gramática,
    incluindo a tabela de transições entre estados para cada símbolo.
    """
    # Obtém a ordem dos pares (cabeça, corpo) das produções para garantir consistência nas comparações e ordenação
    prod_order = get_production_order(grammar)

    # Pega o símbolo inicial da gramática estendida 
    start_symbol = grammar.get_start_symbol()
    # Cria o item inicial com o ponto no começo da produção inicial. Ex: S' → . S
    start_item = LR0Item(start_symbol, tuple(grammar.get_productions()[start_symbol][0]), 0)

    
    C: List[Set[LR0Item]] = [] # Coleção canônica
    transitions: Dict[int, Dict[str, str]] = {} # Transições

    # Inicializa a coleção canônica com o fechamento do item inicial
    I0 = closure(grammar, {start_item})
    C.append(I0)
    transitions[0] = {}

    added = True
    while added:
        added = False
        # Para cada conjunto de itens (estado) atual
        for i, I in enumerate(C):
            symbols_after_dot = [] # Lista dos símbolos que aparecem após o ponto
            seen = set()
            
            # Determina os símbolos após ponto nos itens (organizados pela ordem de produção)
            for item in sorted(I, key=lambda it: prod_order.get((it.head, it.body), float('inf'))):
                if item.dot_pos < len(item.body):
                    symbol = item.body[item.dot_pos]
                    if symbol not in seen: 
                        seen.add(symbol)
                        symbols_after_dot.append(symbol)

            # Para cada símbolo possível após o ponto, calcula a transição goto(I, X)
            for X in symbols_after_dot:
                goto_set = goto(grammar, I, X) # GOTO retorna o fechamento do conjunto de itens avançados pelo símbolo X
                if not goto_set:
                    continue
                
                # Ordena os itens para comparar facilmente se o conjunto já existe na coleção
                goto_sorted = sorted(goto_set, key=lambda it: (prod_order.get((it.head, it.body), float('inf')), it.dot_pos))
                match_index = None
                # Verifica se já existe um estado idêntico ao goto_set em C
                for idx, s in enumerate(C):
                    if goto_sorted == sorted(s, key=lambda it: (prod_order.get((it.head, it.body), float('inf')), it.dot_pos)):
                        match_index = idx
                        break

                if match_index is None:
                    # Se não existe, adiciona novo estado na coleção canônica
                    C.append(goto_set)
                    state_index = len(C) - 1
                    added = True # Indicamos que houve adição para continuar o loop
                else:
                    state_index = match_index # Estado já existe, usa índice encontrado

                # Registra a transição do estado i para state_index com o símbolo X
                if i not in transitions:
                    transitions[i] = {}
                transitions[i][X] = str(state_index)

            # Verifica se o estado aceita (S' → S •)
            for item in I:
                # O estado aceita se existir o item S' → S • (ponto no final da produção inicial)
                if item.head == start_symbol and item.dot_pos == len(item.body):
                    if i not in transitions:
                        transitions[i] = {}
                    transitions[i]["$"] = "accept"  # Transição explícita para 'accept'
                    break

    return C, transitions

def print_canonical_collection(canonical_collection: List[Set[LR0Item]], grammar: Grammar):
    prod_order = get_production_order(grammar)
    print("\n=== Coleção Canônica de Itens LR(0) ===\n")
    for idx, state in enumerate(canonical_collection):
        print(f"I{idx}:")
        for item in sorted(state, key=lambda it: (prod_order.get((it.head, it.body), float('inf')), it.dot_pos)):
            print(f"  {item}")
        print()