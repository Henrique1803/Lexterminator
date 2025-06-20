import re
from collections import defaultdict
from typing import Dict, List, Optional, Set
from collections import defaultdict
from typing import Dict, List, Set, Optional


class Grammar:
    """
    Classe que representa uma gramática SLR(1).
    """
    def __init__(self, grammar_file: str, expected_tokens: Set = None):
        self.productions: Dict[str, List[List[str]]] = defaultdict(list)
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        self.start_symbol: Optional[str] = None
        self.first_sets: Dict[str, Set[str]] = {}
        self.follow_sets: Dict[str, Set[str]] = {}

        self._load_grammar(grammar_file)
        self._compute_terminals(expected_tokens)
        self._initialize_first_sets()
        self._compute_first_sets()
        self._compute_follow_sets()

    def _load_grammar(self, filename: str):
        """"Lê um arquivo de gramática com regras no formato
            NãoTerminal ::= produção1 | produção2 | ...."""
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()

                # Ignora linhas vazias ou que não contém a produção (::=)
                if not line or "::=" not in line:
                    continue
                
                # Divide a linha no símbolo da cabeça (head) e nas produções (bodies)
                head, bodies = line.split("::=", 1)
                head = head.strip() # Remove espaços no head
                self.non_terminals.add(head) # Adiciona o símbolo head como não terminal

                # Define o primeiro símbolo lido como símbolo inicial da gramática
                if self.start_symbol is None:
                    self.start_symbol = head

                 # As produções podem ser alternativas separadas por '|'
                for body in bodies.split("|"):
                    symbols = body.strip().split()
                    self.productions[head].append(symbols)

    def _compute_terminals(self, expected_tokens: Set):
        """Identifica os símbolos terminais da gramática"""
        symbols_in_productions: Set[str] = set()

        # Percorre todas as produções da gramática
        for bodies in self.productions.values():
            for body in bodies:
                if "&" in body:
                    body.remove("&")
                symbols_in_productions.update(body) # Adiciona todos os símbolos da produção ao conjunto

        # Atualiza os terminais
        self.terminals = symbols_in_productions - self.non_terminals

        if expected_tokens:
            expected_tokens.update(["&"])
            diff = self.terminals - expected_tokens
            if len(diff) > 0:
                raise ValueError(f"Há tokens considerados na gramática que não fazem parte das definições regulares: {diff}")

    def _initialize_first_sets(self):
        """
        Inicializa os conjuntos FIRST para todos os símbolos.
        Para terminais, FIRST contém o próprio símbolo; para os demais, começa vazio.
        """
        all_symbols = self.non_terminals.union(self.terminals)
        self.first_sets = {symbol: set() for symbol in all_symbols}
        for terminal in self.terminals:
            self.first_sets[terminal].add(terminal)

    def _compute_first_sets(self):
        """
        Calcula os conjuntos FIRST para todos os símbolos da gramática
        aplicando repetidamente as regras:
        - FIRST(terminal) = { terminal }
        - Se A ::= a..., então a ∈ FIRST(A)
        - Se A ::= ε, então ε ∈ FIRST(A)
        - Se A ::= Y1 Y2 ... Yk, então todos os FIRST(Yi) (exceto ε) são adicionados a FIRST(A),
            e ε só é adicionado se todos os Yi puderem gerar ε.
        O processo se repete até que nenhum conjunto FIRST mude.
        """
        changed = True
        # Continua o loop enquanto houver alterações em algum conjunto FIRST
        while changed:
            changed = False

            # Para cada produção A ::= α (onde A é o head e α ∈ bodies)
            for head, bodies in self.productions.items():
                for body in bodies:
                    # Se a produção é A ::= ε
                    if body == ['&']:
                        if '&' not in self.first_sets[head]:
                            self.first_sets[head].add('&') # ε ∈ FIRST(A)
                            changed = True
                        continue

                    # Caso geral: A ::= Y1 Y2 ... Yk
                    # Tentativa para adicionar os FIRST(Yi) (sem ε) em FIRST(A)
                    for i, symbol in enumerate(body):
                        # Salva o tamanho anterior do conjunto FIRST(A)
                        before = len(self.first_sets[head])

                        # Adiciona os símbolos de FIRST(Yi), exceto ε, ao FIRST(A)
                        self.first_sets[head].update(self.first_sets[symbol] - {'&'})

                        # Verifica se houve mudança no tamanho do conjunto
                        after = len(self.first_sets[head])
                        if after > before:
                            changed = True

                        # Se FIRST(Yi) não contém ε, paramos (não propaga FIRST(Y(i+1)))
                        if '&' not in self.first_sets[symbol]:
                            break
                    else:
                        # Se todos os Yi têm ε, adiciona ε no FIRST(A)
                        if '&' not in self.first_sets[head]:
                            self.first_sets[head].add('&')
                            changed = True
    
    def _compute_follow_sets(self):
        """
        Calcula os conjuntos FOLLOW para todos os não terminais da gramática.
        Regras aplicadas repetidamente até estabilidade:
        1. Adiciona '$' ao FOLLOW do símbolo inicial.
        2. Para A ::= α B β, adiciona FIRST(β) (exceto ε) ao FOLLOW(B).
        3. Se β é vazio ou pode derivar ε, adiciona FOLLOW(A) ao FOLLOW(B).
        """
        # Inicializa os conjuntos FOLLOW com conjuntos vazios
        self.follow_sets = {nt: set() for nt in self.non_terminals}

        # Adiciona $ ao FOLLOW do símbolo inicial
        if self.start_symbol:
            self.follow_sets[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False

            # Para cada produção A ::= body
            for head, bodies in self.productions.items():
                for body in bodies:
                    # Percorre os símbolos da produção
                    for i, B in enumerate(body):
                        
                        apply_follow_of_head = False

                        if B not in self.non_terminals:
                            continue  # Só processa FOLLOW de não terminais

                        # β é a sequência após B (pode estar vazia)
                        beta = body[i + 1:]

                        if beta:
                            # Adiciona FIRST(β) (exceto ε) ao FOLLOW(B)
                            first_of_beta = set()
                            for symbol in beta:
                                first_of_beta.update(self.first_sets[symbol] - {'&'})
                                if '&' in self.first_sets[symbol]:
                                    continue # Continua para o próximo símbolo de β
                                else:
                                    break # Se não contém ε, não precisa olhar os próximos
                            else:
                                # Todos os símbolos em β podem derivar ε
                                # Isso significa que tudo que pode seguir A também pode seguir B
                                apply_follow_of_head = True

                            # Adiciona FIRST(β) (sem ε) ao FOLLOW(B)
                            before = len(self.follow_sets[B])
                            self.follow_sets[B].update(first_of_beta)
                            if len(self.follow_sets[B]) > before:
                                changed = True
                        else:
                            # Se B está no final da produção (não há β),
                            # então tudo que pode seguir A também pode seguir B
                            apply_follow_of_head = True

                        # Se a sequência β pode derivar ε ou está vazia:
                        # Adicionamos FOLLOW(A) a FOLLOW(B)
                        if apply_follow_of_head:
                            before = len(self.follow_sets[B])
                            self.follow_sets[B].update(self.follow_sets[head])
                            if len(self.follow_sets[B]) > before:
                                changed = True
                            apply_follow_of_head = False  # Limpa a flag para o próximo loop

    # retorna o conjunto first de algum não terminal
    def get_first(self, symbol: str) -> Set[str]:
        return self.first_sets.get(symbol, set())
    
    # retorna o conjunto follow de algum não terminal
    def get_follow(self, symbol: str) -> Set[str]:
        return self.follow_sets.get(symbol, set())

    # método auxiliar que printa os conjuntos first
    def print_first_sets(self):
        for symbol in sorted(self.first_sets):
            first = ', '.join(sorted(self.first_sets[symbol]))
            print(f"FIRST({symbol}) = {{ {first} }}")

    # método auxiliar que printa os conjuntos follow
    def print_follow_sets(self):
        for symbol in sorted(self.follow_sets):
            follow = ', '.join(sorted(self.follow_sets[symbol]))
            print(f"FIRST({symbol}) = {{ {follow} }}")

    # retorna as produções
    def get_productions(self) -> Dict[str, List[List[str]]]:
        return dict(self.productions)

    # retorna o símbolo inicial
    def get_start_symbol(self) -> Optional[str]:
        return self.start_symbol

    # verifica se um dado símbolo é terminal
    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.terminals

    # verifica se um dado símbolo é não terminal
    def is_non_terminal(self, symbol: str) -> bool:
        return symbol in self.non_terminals

    def __str__(self) -> str:
        output = []
        for head, bodies in self.productions.items():
            bodies_str = ' | '.join([' '.join(prod) for prod in bodies])
            output.append(f"{head} ::= {bodies_str}")
        return '\n'.join(output)
