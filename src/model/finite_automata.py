from src.utils.paths import AUTOMATA_DIAGRAM_DIR

from collections import deque, defaultdict
from typing import List, Set, Dict, Tuple
from pprint import pprint

from prettytable import PrettyTable
from graphviz import Digraph


class FiniteAutomata:
    """
    Classe que representa o Autômato Finito, de acordo com a definição formal.
    Inclui métodos de operações com o autômato como união e determinização.
    """
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        initial_state: str,
        final_states: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]]
    ):
        self.states: Set[str] = states
        self.alphabet: Set[str] = alphabet
        self.initial_state: str = initial_state
        self.final_states: Set[str] = final_states
        self.transitions: Dict[Tuple[str, str], Set[str]] = transitions
        self.final_state_to_token: Dict[str, str] = {}  # Mapeia estados finais para nomes de tokens

    def get_transitions(self, state: str, symbol: str) -> Set[str]:
        """
        Retorna o conjunto de estados alcançáveis a partir de um estado dado,
        lendo um determinado símbolo.
        """
        return self.transitions.get((state, symbol), set())

    def transition_table(self):
        """
        Imprime a tabela de transições do autômato utilizando prettytable,
        com nomes de estados encurtados (q0, q1, ...) e tokens nos estados finais.
        """
        from collections import defaultdict

        all_symbols = self.alphabet.copy()
        if any(sym == '&' for (_, sym) in self.transitions):
            all_symbols.add('&')

        headers = ['State'] + sorted(all_symbols)
        table = PrettyTable()
        table.field_names = headers

        # Cria mapeamento: nome longo do estado → q0, q1, ...
        state_names = sorted(self.states)
        base_name_map = {state: f"q{i}" for i, state in enumerate(state_names)}

        # Gerar nomes descritivos para estados finais com base nos tokens
        token_counts = defaultdict(int)
        final_name_map = {}

        for state in self.final_states:
            token = self.final_state_to_token.get(state, None)
            if token:
                token_counts[token] += 1
                if token_counts[token] == 1:
                    final_name_map[state] = token
                else:
                    final_name_map[state] = f"{token}_{token_counts[token]}"
            else:
                final_name_map[state] = base_name_map[state]  # fallback

        for state in state_names:
            # Define marcador e nome do estado
            if state in self.final_states:
                name = final_name_map[state]
                marker = '*'
            else:
                name = base_name_map[state]
                marker = ''

            if state == self.initial_state:
                marker = '→' + marker

            display_state = f"{marker}{name}"
            row = [display_state]

            for symbol in sorted(all_symbols):
                dests = self.get_transitions(state, symbol)
                if dests:
                    dest_str = ','.join(
                        final_name_map[d] if d in self.final_states else base_name_map[d]
                        for d in sorted(dests)
                    )
                else:
                    dest_str = '-'
                row.append(dest_str)

            table.add_row(row)

        return table


    def to_file(self, file_path: str):
        """
        Salva o autômato em um arquivo, usando nomes encurtados para estados:
        - estados finais recebem nomes descritivos com base no token associado
        - demais estados recebem nomes como q0, q1, ...
        """

        # Nome curto base: q0, q1, ...
        ordered_states = sorted(self.states)

        final_map = self._rename_states()

        with open(file_path, 'w', encoding='utf-8') as f:
            # Número de estados
            f.write(f"{len(ordered_states)}\n")

            # Estado inicial
            f.write(f"{final_map[self.initial_state]}\n")

            # Estados finais
            final_state_str = ','.join(final_map[s] for s in sorted(self.final_states))
            f.write(final_state_str + '\n')

            # Alfabeto
            f.write(','.join(sorted(self.alphabet)) + '\n')

            # Transições
            for (origin, symbol), destinations in sorted(self.transitions.items()):
                for dest in sorted(destinations):
                    f.write(f"{final_map[origin]},{symbol},{final_map[dest]}\n")

    def _epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Retorna o ε-fecho do conjunto de estados fornecido.
        """
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in self.get_transitions(state, '&'):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure
    
    def run(self, input_str: str) -> Tuple[bool, str]:
        """
        Executa o autômato sobre a string de entrada.
        Retorna uma tupla:
        (True, nome_do_token) se a entrada for aceita,
        (False, "") se a entrada for rejeitada.
        """
        current_states = self._epsilon_closure({self.initial_state})

        for symbol in input_str:
            next_states: Set[str] = set()
            for state in current_states:
                for target in self.get_transitions(state, symbol):
                    next_states.update(self._epsilon_closure({target}))

            if not next_states:
                return (False, "")

            current_states = next_states

        # Verifica se algum estado atual é final e retorna o token correspondente
        for state in current_states:
            if state in self.final_states:
                token_name = self.final_state_to_token.get(state, "")
                return (True, token_name)

        return (False, "")

    def determinize(self, token_priority: List[str]) -> 'FiniteAutomata':
        """
        Determiniza o autômato (AFND → AFD) e retorna um novo objeto AF.
        Preserva o mapeamento de estados finais para tokens.
        """
        def _name_from_set(state_set: Set[str]) -> str:
            return '_'.join(sorted(state_set))

        # Mapeia conjuntos de estados do AFND → nome do novo estado determinístico
        state_map: Dict[frozenset, str] = {}

        # Elementos para o novo AFD
        transitions: Dict[Tuple[str, str], Set[str]] = {}
        new_states: Set[str] = set()
        new_final_states: Set[str] = set()
        new_alphabet: Set[str] = self.alphabet.copy()
        
        # Dicionário para mapear novos estados finais para tokens
        new_final_state_to_token: Dict[str, str] = {}

        # Cálculo do ε-fecho do estado inicial do AFND
        initial_closure = self._epsilon_closure({self.initial_state})
        initial_fset = frozenset(initial_closure)
        initial_name = _name_from_set(initial_closure)

        # Mapeamos o ε-fecho como o primeiro estado determinístico
        state_map[initial_fset] = initial_name
        queue = deque([initial_fset]) # fila de estados compostos a serem processados

        # Processa todos os estados compostos (conjuntos de estados do AFND)
        while queue:
            current_set = queue.popleft()
            current_name = state_map[current_set]
            new_states.add(current_name)

            # Verifica se algum estado no conjunto atual é final no AFND original
            final_states_in_set = current_set & self.final_states
            if final_states_in_set:
                new_final_states.add(current_name)
                
                # Determina qual token corresponde a este estado final
                # Prioriza o token mais antigo (definido primeiro no arquivo de definições regulares)
                best_token = None
                best_priority = float('inf')  # Menor índice na lista = maior prioridade

                for state in final_states_in_set:
                    token = self.final_state_to_token.get(state)
                    if token and token in token_priority:
                        priority = token_priority.index(token)
                        if priority < best_priority:
                            best_priority = priority
                            best_token = token

                if best_token:
                    new_final_state_to_token[current_name] = best_token
            
            # Para cada símbolo do alfabeto, calcula os estados alcançáveis
            for symbol in self.alphabet:
                next_set = set()

                # Para cada estado no conjunto atual, pega transições com o símbolo
                for state in current_set:
                    targets = self.get_transitions(state, symbol)
                    # Aplica ε-fecho em cada destino
                    for t in targets:
                        next_set.update(self._epsilon_closure({t}))

                if not next_set:
                    continue # nenhuma transição válida com esse símbolo

                next_fset = frozenset(next_set)

                # Se o conjunto resultante ainda não tem nome, cria um e coloca na fila
                if next_fset not in state_map:
                    next_name = _name_from_set(next_set)
                    state_map[next_fset] = next_name
                    queue.append(next_fset)

                # Adiciona a transição ao novo autômato
                transitions[(current_name, symbol)] = {state_map[next_fset]}

        # Cria o novo autômato determinizado
        determinized = FiniteAutomata(
            states=set(state_map.values()),
            alphabet=new_alphabet,
            initial_state=initial_name,
            final_states=new_final_states,
            transitions=transitions
        )
        # Atualiza o mapeamento de tokens para os novos estados finais
        determinized.final_state_to_token = new_final_state_to_token

        return determinized

    def _generate_finite_automata_diagram(self):
        final_map = self._rename_states()
        transitions = defaultdict(list)
    
        diagram = Digraph("Finite Automata Diagram")

        diagram.attr("node", shape="doublecircle", height="1")
        for state in self.final_states:
            diagram.node(final_map[state])

        for (origin, symbol), destinations in sorted(self.transitions.items()):
            for dest in sorted(destinations):
                transitions[(origin, dest)].append(symbol)
        
        diagram.attr("node", shape="circle", height="1")
        for (origin, dest), symbols_list in sorted(transitions.items()):
            symbols = str()
            for symbol in symbols_list:
                symbols += f"{symbol}|"
            symbols = list(symbols)
            symbols.pop()
            symbols = "".join(symbols)

            diagram.edge(final_map[origin], final_map[dest], symbols)
        
        diagram.node("", shape="none")
        diagram.edge("", final_map[self.initial_state])

        diagram.render(filename="automata_diagram", format="png", directory=str(AUTOMATA_DIAGRAM_DIR))
    
    def _rename_states(self) -> dict:
        from collections import defaultdict

        # Nome descritivo para estados finais com base em tokens
        token_counts = defaultdict(int)
        final_name_map = {}
        for state in self.final_states:
            token = self.final_state_to_token.get(state)
            if token:
                token_counts[token] += 1
                if token_counts[token] == 1:
                    final_name_map[state] = token
                else:
                    final_name_map[state] = f"{token}_{token_counts[token]}"

        # Nome curto base: q0, q1, ...
        ordered_states = sorted(self.states - self.final_states)
        base_name_map = {state: f"q{i}" for i, state in enumerate(ordered_states)}

        # Mapa final: estado original → nome final (token ou qN)
        final_map = {
            state: final_name_map[state] if state in self.final_states else base_name_map[state]
            for state in self.states
        }

        return final_map

    @staticmethod
    def from_file(file_path: str) -> 'FiniteAutomata':
        """
        Lê um autômato no formato do trabalho e retorna um objeto AF.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        initial_state = lines[1]
        final_states = set(lines[2].split(','))
        alphabet = set(lines[3].split(','))

        transitions: Dict[Tuple[str, str], Set[str]] = {}
        states: Set[str] = set()

        for line in lines[4:]:
            origin, symbol, dest = line.split(',')
            key = (origin, symbol)
            if key not in transitions:
                transitions[key] = set()
            transitions[key].add(dest)
            states.update([origin, dest])

        return FiniteAutomata(
            states=states,
            alphabet=alphabet,
            initial_state=initial_state,
            final_states=final_states,
            transitions=transitions
        )

    @staticmethod
    def union(af1: 'FiniteAutomata', af2: 'FiniteAutomata') -> 'FiniteAutomata':
        """
        Retorna um novo autômato que é a união dos autômatos af1 e af2,
        renomeando os estados de af2 somente se houver conflito com os estados de af1.
        Cria um novo estado inicial com transições epsilon para os estados iniciais de af1 e af2.
        """
        new_initial = 'qi'

        # Estados já usados no af1
        states_af1 = af1.states

        # Mapa de renomeação dos estados do af2 (somente renomeia se conflito)
        rename_map = {}

        for s in af2.states:
            if s in states_af1:
                rename_map[s] = 'af2-' + s
            else:
                rename_map[s] = s

        # Renomear elementos de af2 para evitar conflitos de nomes iguais
        af2_renamed_states = set(rename_map.values())

        af2_renamed_transitions = {}
        for (origin, symbol), dests in af2.transitions.items():
            new_origin = rename_map[origin]
            new_dests = {rename_map[d] for d in dests}
            af2_renamed_transitions.setdefault((new_origin, symbol), set()).update(new_dests)

        af2_renamed_finals = {rename_map[s] for s in af2.final_states}
        af2_renamed_initial = rename_map[af2.initial_state]
        new_states = states_af1 | af2_renamed_states | {new_initial}
        new_alphabet = af1.alphabet | af2.alphabet

        # Unir transições
        new_transitions = {}

        # Copiar transições do af1
        for (origin, symbol), dests in af1.transitions.items():
            new_transitions.setdefault((origin, symbol), set()).update(dests)

        # Copiar transições renomeadas do af2
        for (origin, symbol), dests in af2_renamed_transitions.items():
            new_transitions.setdefault((origin, symbol), set()).update(dests)

        # Transições epsilon do novo estado inicial para os estados iniciais dos dois autômatos
        new_transitions.setdefault((new_initial, '&'), set()).update({af1.initial_state, af2_renamed_initial})

        # Estados finais são união dos finais dos dois autômatos
        new_final_states = af1.final_states | af2_renamed_finals

        # Criar o novo autômato
        new_automata = FiniteAutomata(
            states=new_states,
            alphabet=new_alphabet,
            initial_state=new_initial,
            final_states=new_final_states,
            transitions=new_transitions
        )

        # Copiar mapeamentos dos estados finais para tokens do af1
        for state, token in af1.final_state_to_token.items():
            new_automata.final_state_to_token[state] = token

        # Copiar mapeamentos dos estados finais para tokens do af2 (com nomes renomeados)
        for original_state, renamed_state in rename_map.items():
            if original_state in af2.final_state_to_token:
                token = af2.final_state_to_token[original_state]
                new_automata.final_state_to_token[renamed_state] = token

        return new_automata



