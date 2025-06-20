from typing import Dict, List, Set, Tuple
from src.model.lr0_item import LR0Item
from src.model.grammar import Grammar
from prettytable import PrettyTable
from src.utils import paths


class SLRTable:
    """
    Classe que representa a tabela SLR.
    """
    def __init__(
        self,
        grammar: Grammar,
        canonical_collection: List[Set[LR0Item]],
        transitions: Dict[int, Dict[str, str]],
        prod_order: Dict[Tuple[str, Tuple[str, ...]], int]
    ):
        """
        Inicializa a tabela SLR a partir da gramática, coleção canônica de itens e transições.
        """
        self.grammar = grammar
        self.states = canonical_collection
        self.transitions = transitions
        self.prod_order = prod_order
        self.table: Dict[int, Dict[str, str]] = {}

        self.build_table()

    def build_table(self):
        """
        Constrói a tabela SLR com ações (shift, reduce, accept) e GOTO.
        """

        # Símbolo inicial da gramática
        start_symbol = self.grammar.get_start_symbol()

        # Itera sobre todos os estados do autômato canônico de itens LR(0)
        for state_index, state in enumerate(self.states):
            self.table[state_index] = {}

            # Itera sobre todos os itens LR(0) presentes neste estado
            for item in state:
                # Se o ponto (·) ainda não está no final da produção
                if item.dot_pos < len(item.body):
                    # Shift
                    symbol = item.body[item.dot_pos]
                    target_state = self.transitions.get(state_index, {}).get(symbol)
                    # Se houver transição, adiciona ação "shift" para o terminal
                    if target_state:
                        self.table[state_index][symbol] = f"s{target_state}"
                else:
                    # Reduce ou Accept
                    # O ponto está no final → é uma produção do tipo [A → α ·]
                    if item.head == start_symbol:
                        # Se A é o símbolo inicial aumentado (S'), aceita a entrada
                        self.table[state_index]["$"] = "accept"
                    else:
                        # Redução: ACTION[i, a] = reduce A → α para todo a ∈ FOLLOW(A)
                        prod_index = self.prod_order.get((item.head, item.body))
                        if prod_index is not None:
                            for terminal in self.grammar.get_follow(item.head):
                                # Apenas adiciona se não houver outra ação já definida
                                if terminal not in self.table[state_index]:
                                    self.table[state_index][terminal] = f"r{prod_index}"

            # GOTO separadamente para não-terminais
            for symbol, target in self.transitions.get(state_index, {}).items():
                if self.grammar.is_non_terminal(symbol):
                    self.table[state_index][symbol] = target  # GOTO é só o número do estado

    def build_pretty_table(self):
        """
        Imprime a tabela SLR usando PrettyTable.
        """
        terminals = sorted(self.grammar.terminals) + ["$"]
        non_terminals = sorted(self.grammar.non_terminals - {self.grammar.get_start_symbol()})
        headers = ["STATE"] + terminals + non_terminals

        pretty_table = PrettyTable()
        pretty_table.field_names = headers

        for state in sorted(self.table.keys()):
            row = [str(state)]
            for symbol in terminals + non_terminals:
                row.append(self.table[state].get(symbol, ""))
            pretty_table.add_row(row)
        
        csv_str = pretty_table.get_csv_string()
        output_path = paths.SLR_TABLE_DIR / "slr_table.csv"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(csv_str)

        return pretty_table