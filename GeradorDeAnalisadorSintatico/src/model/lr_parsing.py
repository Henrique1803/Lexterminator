from typing import List, Tuple, Optional
from prettytable import PrettyTable

from src.model.grammar import Grammar
from src.model.slr_table import SLRTable


class LRParsing:
    def __init__(self, grammar: Grammar, slr_table: SLRTable):
        self.grammar: Grammar = grammar
        self.slr_table: SLRTable = slr_table

    def parse(self, w: List[str]) -> Tuple[PrettyTable, bool]:
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
