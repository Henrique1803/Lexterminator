from typing import List, Tuple
from src.node import Node
from src.tree import Tree
from src.finite_automata import FiniteAutomata


class RegularExpression:

    PRECEDENCE = {
        "*": 2,
        ".": 1,
        "|": 0
    }

    OPERATORS = ['(', ")", "[", "]", "*", "|", ".", "?", "+", "&", "-"]

    def __init__(self, value: str, token_name:str = ""):
        self.__infix: List[Tuple[str, str]] = list()
        self.__postfix: list = list()
        self.__token_name: str = token_name
        self.__automata: FiniteAutomata = None
        self.generate_infix(value)
        self.generate_postfix()
        self.convert_to_finite_automata()

    def _remove_whitespaces(self, value: str):
        return value.replace(" ", "").replace("\n", "").replace("\t", "")

    def _tokenize(self, value: str):
        brackets_stack = []
        last_char = "#"
        for c in value:
            if (c == "\\" or c == ".") and last_char != "\\":
                last_char = c
                continue

            token_type = "LITERAL"
            if c in self.OPERATORS and last_char != "\\":
                token_type = "OPERATOR"
                if c == "(":
                    brackets_stack.append("(")
                elif c == ")":
                    try:
                        if brackets_stack.pop() != "(":
                            raise ValueError(f"Expressão com má formação de parênteses")
                    except:
                        raise ValueError(f"Expressão com má formação de parênteses")
                elif c == "[":
                    brackets_stack.append("[")
                elif c == "]":
                    try:
                        if brackets_stack.pop() != "[":
                            raise ValueError(f"Expressão com má formação de colchetes")
                    except:
                        raise ValueError(f"Expressão com má formação de colchetes")

            self.infix.append((token_type, c))
            last_char = "#" if c == "\\" and last_char == "\\" else c

        if len(brackets_stack) > 0:
            raise ValueError(f"Expressão com má formação de parênteses e/ou colchetes")
        

    def _update_to_primitive_operators(self):
        stack = []
        last_token = ("OPERATOR", str())
        is_sequence = False
        for type, char in self.infix:
            token = (type, char)
            insert_concat = not is_sequence and \
                            ((last_token[0] == "OPERATOR" and last_token[1] not in ["", "(", "[", "|", ".", "-"]) or (last_token[0] == "LITERAL")) and \
                            ((type == "OPERATOR" and char not in ["", "?", "*", "+", ".", "|", "]", ")", "-"]) or (type == "LITERAL"))
            invalid_expr_pairs = {
                                    (("OPERATOR", "("), ("OPERATOR", sym)) for sym in "*?+.|"
                                }.union({
                                    (("OPERATOR", "["), ("OPERATOR", sym)) for sym in "*?+.|"
                                }).union({
                                    (("OPERATOR", ""), ("OPERATOR", sym)) for sym in "*?+.|"
                                }).union({
                                    (("OPERATOR", "|"), ("OPERATOR", sym)) for sym in "*?+.|"
                                }).union({
                                    (("OPERATOR", "*"), ("OPERATOR", sym)) for sym in "*?+."
                                })
            if (last_token, token) in invalid_expr_pairs:
                raise ValueError(f"Expressão inválida: {last_token[1]}{char}. Considere, se for o caso, o uso de parênteses para evitar ambiguidade.")
            concat_token = ("OPERATOR", ".")
            if type == "OPERATOR":
                match char:
                    case ']':
                        is_sequence = False
                        group = self._find_last_group_by_stack(stack, is_sequence=True)
                        group_expanded = self._expand_group(group)
                        if insert_concat:
                            group_expanded.insert(0, concat_token)
                        stack.extend(group_expanded)
                    case '?':
                        last_type, last_char = stack.pop()
                        group_optional = None
                        if last_type == "LITERAL": #substitui a? por (a|&)
                            group_optional = [("OPERATOR", "("), ("LITERAL", last_char), ("OPERATOR", "|"), ("OPERATOR", "&"), ("OPERATOR", ")")]
                        elif last_char == ")": #substitui (expr)? por (expr | &)
                            group_optional = [("OPERATOR", "|"), ("OPERATOR", "&"), ("OPERATOR", ")")]
                        else:
                            ValueError(f"Expressão com operador '?' inválida: {last_char}?")
                        if insert_concat:
                            group_optional.insert(0, concat_token)
                        stack.extend(group_optional)
                    case '+':
                        last_type, last_char = stack.pop()
                        group = None
                        if last_type == "LITERAL": #substitui a+ por (aa*)
                            group = [("OPERATOR", "("), ("LITERAL", last_char), concat_token, ("LITERAL", last_char), ("OPERATOR", "*"), ("OPERATOR", ")")]
                        elif last_char == ")": #substitui (expr)+ por ((expr)(expr)*)
                            group = self._find_last_group_by_stack(stack)
                            aux = group[:]
                            aux.insert(0, concat_token)
                            group.extend(aux)
                            group.insert(0, ("OPERATOR", "("))
                            group.extend([("OPERATOR", "*"), ("OPERATOR", ")")])
                        else:
                            ValueError(f"Expressão com operador '+' inválida: {last_char}?")
                        if insert_concat:
                            group.insert(0, concat_token)
                        stack.extend(group)
                    case _:
                        if char == "[":
                            is_sequence = True
                        elif char == "-" and not is_sequence:
                            raise ValueError("Operador '-' permitido apenas dentro de sequências. Para usar o literal '-' escape com '\\-'")
                        token_inserted = [token]
                        if insert_concat:
                            token_inserted.insert(0, concat_token)
                        stack.extend(token_inserted)
            else:
                token_inserted = [token]
                if insert_concat:
                    token_inserted.insert(0, concat_token)
                stack.extend(token_inserted)
            last_token = stack[-1]
        self.infix = stack

    def _find_last_group_by_stack(self, stack: list, is_sequence: bool = False):
        open_char = "[" if is_sequence else "("
        close_char = "]" if is_sequence else ")"
        substack = []
        group = [("OPERATOR", close_char)]
        while len(stack) > 0:
            token_type, token_char = stack.pop()
            group.insert(0, (token_type, token_char))
            if token_type == "OPERATOR":
                if token_char == open_char:
                    if len(substack) == 0:
                        return group
                    else:
                        substack.pop()
                elif token_char == close_char:
                    substack.append(token_char)
        raise ValueError(f"Expressão com má formação de '{open_char}{close_char}'")

    def _expand_group(self, group: list):
        index_token = 1
        sequence = set()
        for token_type, token_char in group[1:-1]:
            token = (token_type, token_char)
            prev = group[index_token-1]
            pos = group[index_token+1]
            if token_type == "LITERAL" or token_char == "&":
                sequence.add(token)
            elif token_char == "-":
                if prev[0] != "OPERATOR" and pos[0] != "OPERATOR":
                    sequence = sequence.union(self._generate_sequence(prev, pos))
                else:
                    raise ValueError(f"Grupo inválido: {prev[1]}-{pos[1]}")
            else:
                raise ValueError(f"Grupo inválido: [...{token_char}...]")

            index_token += 1
        
        sequence = list(sequence)
        expanded_group = [("OPERATOR", "("), sequence.pop(0)]
        for token in sequence:
            expanded_group.extend([("OPERATOR", "|"), token])
        expanded_group.append(("OPERATOR", ")"))
        return expanded_group

    def _generate_sequence(self, prev: Tuple, pos: Tuple):
        start, end = prev[1], pos[1]
        if start.isalpha() and end.isalpha() and start.isupper() and end.isupper() and start <= end:
            return set([("LITERAL", chr(c)) for c in range(ord(start), ord(end) + 1)])
        elif start.isalpha() and end.isalpha() and start.islower() and end.islower() and start <= end:
            return set([("LITERAL", chr(c)) for c in range(ord(start), ord(end) + 1)])
        elif start.isdigit() and end.isdigit() and start <= end:
            return set([("LITERAL", chr(c)) for c in range(ord(start), ord(end) + 1)])
        else:
            raise ValueError(f"Sequência inválida: [{start}-{end}]")
        
    def generate_infix(self, value: str):
        value = self._remove_whitespaces(value)
        self._tokenize(value)
        self._update_to_primitive_operators()
        self.infix.insert(0, ("OPERATOR", "("))
        self.infix.extend([("OPERATOR", ")"), ("OPERATOR", "."), ("LITERAL", "#")])

    def generate_postfix(self):
        stack = []

        for type, char in self.infix:
            token = (type, char)
            if type == "OPERATOR" and char != "&":
                if char == "(":
                    stack.append(token)
                elif char == ")":
                    while stack and stack[-1][0] == "OPERATOR" and stack[-1][1] != "(":
                        self.postfix.append(stack.pop())
                    stack.pop()
                else:
                    while (stack and stack[-1][0] == "OPERATOR" and stack[-1][1] != "(" and
                           self.PRECEDENCE.get(char, 0) <= (0 if stack[-1][0] == "LITERAL" else self.PRECEDENCE.get(stack[-1][1], 0))):
                        self.postfix.append(stack.pop())
                    stack.append(token)
            else:
                self.postfix.append(token)

        while stack:
            self.postfix.append(stack.pop())

    def convert_regular_expression_to_tree(self) -> Tree:
        stack = list()
        counter = 0

        tree = Tree()

        for type, char in self.postfix:
            node = None
            if type == "OPERATOR":
                match char:
                    case "*":
                        son = stack.pop()
                        node = Node(char, son)

                    case "|" | ".":
                        right_son = stack.pop()
                        left_son = stack.pop()
                        node = Node(char, left_son, right_son)
                    
                    case _:
                        node = Node(char)
            else:
                counter += 1
                node = Node(char, value=str(counter), operator=False)
                tree.node_value_to_token[str(counter)] = char

                if char == "#":
                    tree.acceptance_node = node
            
            stack.append(node)
            tree.add_node(node)
        
        return tree
    
    def convert_to_finite_automata(self):
        tree = self.convert_regular_expression_to_tree()
        tree.calculate_nodes_data()
        self.automata = tree.generate_automata(self.token_name)

    @property
    def postfix(self):
        return self.__postfix
    
    @postfix.setter
    def postfix(self, value):
        self.__postfix = value

    @property
    def infix(self):
        return self.__infix
    
    @infix.setter
    def infix(self, value):
        self.__infix = value
    
    @property
    def token_name(self):
        return self.__token_name

    @property
    def automata(self):
        return self.__automata
    
    @automata.setter
    def automata(self, automata: FiniteAutomata):
        self.__automata = automata

    def __str__(self):
        return "".join(self.infix)
    
    def __repr__(self):
        return self.__str__()