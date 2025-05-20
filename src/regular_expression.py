from node import Node
from tree import Tree


class RegularExpression:

    PRECEDENCE = {
        "*": 2,
        ".": 1,
        "|": 0
    }

    def __init__(self, value: str, token_name:str = ""):
        self.__postfix = []
        self.__infix = []
        self.__token_name = token_name
        value = self.treat_characters(value)
        self.generate_infix(value)
        self.generate_postfix()
        self.convert_to_finite_automata()

    def treat_characters(self, value: str):
        value = value.replace(" ", "").replace("\n", "").replace("\t", "")
        value = value.replace(".", "")
        value = value.replace(")?", "|&)").replace("]?", "&]")

        index = value.find("?")
        while index != -1:
            try:
                left_symbol = value[index-1]
            except:
                raise ValueError("O símbolo '?' não pode estar no começo de uma ER!")

            if left_symbol in ["*", "|", ".", "?", "+", "(", "["]:
                raise ValueError("A sua ER não é uma expressão válida!")
            
            value = value.replace(f"{left_symbol}?", f"({left_symbol}|&)")

            index = value.find("?")
        
        index = value.find("+")
        while index != -1:
            try:
                left_symbol = value[index-1]
            except:
                raise ValueError("O símbolo '+' não pode estar no começo de uma ER!")

            if left_symbol in ["*", "|", ".", "?", "+", "(", "["]:
                raise ValueError("A sua ER não é uma expressão válida!")
        
            if left_symbol not in [")", "]"]:
                value = value.replace(f"{left_symbol}+", f"{left_symbol}{left_symbol}*")
            else:
                stack = list(left_symbol)
                string = list(left_symbol)
                close_char = str()

                if left_symbol == ")":
                    close_char = "("

                else:
                    close_char = "["

                for i in range(index-2, -1, -1):
                    char = value[i]
                    string.insert(0, char)

                    if char == left_symbol:
                        stack.append(char)
                    elif char == close_char:
                        stack.pop()
                    
                    if len(stack) == 0:
                        break
                
                string = "".join(string)
                value = value.replace(f"{string}+", f"{string}{string}*")
            
            index = value.find("+")
        
        return value

    def generate_infix(self, value: str):
        isGroup = False
        scape = False
        brackets = []
        last = None
        group = ""
        for s in value:
            if scape:
                scape = False
                is_first_character = len(self.infix) == 0
                self.infix.extend([".", f"\\{s}"])
                if is_first_character:
                    self.infix.pop(0)
                last = f"\\{s}"
                continue
            else:
                if s == '\\':
                    scape = True
                    continue
                
            match s:
                case '[':
                    if not isGroup:
                        isGroup = True
                        group = "["
                        last = s
                        continue
                    else:
                        raise ValueError("Formação incorreta de '[]'")
                case ']':
                    if isGroup:
                        isGroup = False
                        group = f"{group}]"
                        expanded_group = self.expand_group(group)
                        is_group_first = len(self.infix) == 0
                        is_parentheses_first = len(self.infix) > 0 and self.infix[-1] == "("

                        if is_group_first or is_parentheses_first:
                            expanded_group.pop(0) # remove a concatenação desnecessária

                        print("infix atual, no grupo: ", self.infix)
                        print("grupo a ser incluido: ", expanded_group)
                        self.infix.extend(expanded_group)

                case '(':
                    if isGroup:
                        group = f"{group}("
                        raise ValueError(f"Grupo inválido: {group}")
                    brackets.append('(')
                    self.infix.append("(")
                case ')':
                    if isGroup:
                        group = f"{group})"
                        raise ValueError(f"Grupo inválido: {group}")
                    try:
                        brackets.pop()
                        self.infix.append(')')
                    except:
                        raise ValueError("Formação incorreta de '()'")
                case _:
                    if isGroup:
                        group = f"{group}{s}"
                        last = s
                        continue
                    self.infix.append(s)

            if last != None and s not in ['|', '*', '+', '?', ')', ']'] and last not in ['|', '(', '[']:
                self.infix.insert(-1, '.')
            
            last = s

        if len(brackets) != 0:
            raise ValueError("Formação incorreta de '()'")
        
        self.infix.append(".")
        self.infix.append("#")


    def expand_group(self, group: str):
        expanded_group = []
        seq = set()
        for i, s in enumerate(group):
            if s in ['[',']']:
                continue
            try:
                prev, pos = group[i-1], group[i+1]
            except:
                raise ValueError(f"Grupo inválido: {group}")
            
            match s:
                case '-':
                    seq = seq.union(set(self.generate_sequence(f"{prev}-{pos}")))
                case _:
                    if pos != '-' and prev != '-':
                        seq.add(s)
        
        expanded_group.extend(seq)
        expanded_group = list('|'.join(expanded_group))
        expanded_group.insert(0, '(')
        expanded_group.insert(0, '.')
        expanded_group.append(')')
        return expanded_group

    def generate_sequence(self, sequence: str):
        start, end = sequence[0], sequence[2]
        if start.isalpha() and end.isalpha() and start.isupper() and end.isupper() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        elif start.isalpha() and end.isalpha() and start.islower() and end.islower() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        elif start.isdigit() and end.isdigit() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        else:
            raise ValueError(f"Sequência inválida: [{sequence}]")
        
    def generate_postfix(self):
        stack = []
        print(f"infix: {self.infix}")

        for s in self.infix:
            if s == '(':
                stack.append(s)
            elif s == ')':
                while stack and stack[-1] != '(':
                    self.postfix.append(stack.pop())
                stack.pop()
            elif s in list(self.PRECEDENCE.keys()):
                while (stack and stack[-1] != '(' and
                    self.PRECEDENCE.get(s, 0) <= self.PRECEDENCE.get(stack[-1], 0)):
                    self.postfix.append(stack.pop())
                stack.append(s)
            else:
                self.postfix.append(s)

        while stack:
            self.postfix.append(stack.pop())
        
    def convert_regular_expression_to_tree(self) -> Tree:
        stack = list()
        counter = 0

        tree = Tree()

        print(self.postfix)

        for symbol in self.postfix:
            node = None
            if symbol == "*":
                son = stack.pop()
                node = Node(symbol, son)

            elif symbol in ["|", "."]:
                right_son = stack.pop()
                left_son = stack.pop()
                node = Node(symbol, left_son, right_son)

            elif symbol != "&":
                counter += 1
                node = Node(symbol, value=str(counter))
                tree.node_value_to_token[str(counter)] = symbol

                if symbol == "#":
                    tree.acceptance_node = node

            else:
                node = Node(symbol)
            

            stack.append(node)
            tree.add_node(node)

            print(stack)

        
        return tree
    
    def convert_to_finite_automata(self):
        tree = self.convert_regular_expression_to_tree()
        tree.calculate_nodes_data()
        automata = tree.generate_automata() # passar o nome do token da regex aqui como parâmetro

        automata.to_file("output_af/af_output.txt")

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

    def __str__(self):
        return "".join(self.infix)
    
    def __repr__(self):
        return self.__str__()