from typing import List, Tuple, Optional
from prettytable import PrettyTable
from graphviz import Digraph

from src.model.grammar import Grammar
from src.model.slr_table import SLRTable

from src.utils.closure_and_canonnical_collection import *
from src.utils import paths


class SintaticalAnalyzer:
    def __init__(self, grammar_file: str, expected_tokens: Set = None):
        self.grammar: Grammar = Grammar(grammar_file, expected_tokens)

        extended_grammar = extend_grammar(self.grammar)
        collection, transitions = canonical_collection(extended_grammar)
        self.generate_canonical_items_diagram(collection, transitions)
        prod_order = get_production_order(extended_grammar)

        self.slr_table: SLRTable = SLRTable(extended_grammar, collection, transitions, prod_order)
        self.pretty_table = self.slr_table.build_pretty_table()
        self.tokens_list: list = list()
    
    def read_tokens_from_lexical_analyzer_output(self, file_path: str):
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                line = line.replace("<", "").replace(">", "")
                token = line.split(",")[1]
                self.tokens_list.append(token)

        pretty_table, input_passed = self.parse_tokens(self.tokens_list)

        input_string = ""
        for token in self.tokens_list:
            input_string += token + " "

        self.print_parse_tokens_data(input_string, input_passed, pretty_table)
        
    def parse_tokens(self, w: List[str]) -> Tuple[PrettyTable, bool]:
        """"
        Método principal que tenta reconhecer uma cadeia, 
        retornando a tabela de etapas e um booleano indicando sucesso ou erro
        """
        stack = [0]
        input_buffer = w + ['$'] # Acrescenta o símbolo terminal $ ao final da entrada
        a_index = 0 # Índice do símbolo atual de entrada
        a = input_buffer[a_index] # Símbolo atual da entrada

        table = PrettyTable()
        table.field_names = ["#", "Stack", "Input", "Action"]

        step = 1

        while True:
            s = stack[-1] # Estado atual no topo da pilha
            action = self.slr_table.table.get(s, {}).get(a) # Ação definida na tabela SLR para o estado 's' e símbolo 'a'

            # Representações em string da pilha e da entrada restante
            stack_repr = ' '.join(map(str, stack))
            input_repr = ' '.join(input_buffer[a_index:])
            
            # Caso a ação não esteja definida: erro de análise
            if action is None: 
                table.add_row([step, stack_repr, input_repr, "ERRO"])
                return table, False
            # Ação de deslocamento (shift)
            elif action.startswith('s'):
                t = int(action[1:]) # Novo estado a ser empilhado
                stack.append(t)
                table.add_row([step, stack_repr, input_repr, f"s{t}"])
                a_index += 1 # Avança na entrada
                a = input_buffer[a_index] # Atualiza o símbolo atual
            # Ação de redução (reduce)
            elif action.startswith('r'):
                prod_index = int(action[1:]) # Índice da produção a ser reduzida
                rev = {v: k for k, v in self.slr_table.prod_order.items()} # Recupera a produção correspondente (inverso do mapeamento)
                head, body = rev[prod_index]
                body_list = list(body)

                # Remove da pilha tantos símbolos quanto o corpo da produção
                for _ in body_list:
                    stack.pop()

                # Estado no topo da pilha após o pop
                t = stack[-1]

                # Busca o estado de transição após redução (desvio)
                goto_state = self.slr_table.table[t][head]
                stack.append(int(goto_state))
                table.add_row([step, stack_repr, input_repr, f"r{prod_index} ({head} → {' '.join(body_list)})"])
            # Ação de aceitação
            elif action == 'accept':
                table.add_row([step, stack_repr, input_repr, "accept"])
                return table, True
            # Ação inválida (não é shift, reduce ou accept)
            else:
                table.add_row([step, stack_repr, input_repr, f"ERRO: ação inválida '{action}'"])
                return table, False

            step += 1

    def generate_canonical_items_diagram(self, collection, transitions):
        dot = Digraph(comment="Canonical LR0 Items", format='png')
        dot.attr(rankdir='LR', fontsize='12')

        # Criar nós
        for idx, itemset in enumerate(collection):
            # Cada item é LR0Item, usar o método to_string() para mostrar o ponto
            label_lines = [f"I{idx}:"]
            label_lines += [repr(item) for item in sorted(itemset, key=lambda x: (x.head, x.body, x.dot_pos))]
            label = "\n".join(label_lines)
            dot.node(str(idx), label=label, shape='box', fontsize='10')

        # Criar arestas (transições)
        for from_state, edges in transitions.items():
            for symbol, to_state in edges.items():
                if to_state == "accept":
                    dot.node("accept", label="ACCEPT", shape="doublecircle", style="filled", fillcolor="lightgreen")
                    dot.edge(str(from_state), "accept", label=symbol)
                else:
                    dot.edge(str(from_state), str(to_state), label=symbol)

        # 3. Renderiza o grafo
        dot.render(filename="canonical_items_diagram", format="png", directory=str(paths.CANONICAL_ITEMS_DIAGRAM_DIR))
        
    def print_parse_tokens_data(self, input_str: str, input_passed: bool, pretty_table: PrettyTable): # Método usado para mostrar os dados da análise sintática temporariamente no terminal (será removido depois)
        print("Entrada: ", input_str)
        print("Passou? ",input_passed)
        print(pretty_table)