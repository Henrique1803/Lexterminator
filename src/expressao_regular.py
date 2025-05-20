from node import Node
from tree import Tree


class ExpressaoRegular:

    PRECEDENCIA = {
        "*": 2,
        ".": 1,
        "|": 0
    }

    def __init__(self, value: str, token_name:str = ""):
        self.__posfixa = []
        self.__infixa = []
        self.__token_name = token_name
        value = self.tratar_caracteres(value)
        self.gerar_infixa(value)
        self.gerar_posfixa()
        self.convert_to_finite_automata()

    def tratar_caracteres(self, value: str):
        value = value.replace(" ", "").replace("\n", "").replace("\t", "")
        value = value.replace(".", "")
        value = value.replace(")?", "|&)").replace("]?", "&]")

        index = value.find("?")
        while index != -1:
            try:
                left_simbol = value[index-1]
            except:
                raise ValueError("O símbolo '?' não pode estar no começo de uma ER!")

            if left_simbol in ["*", "|", ".", "?", "+", "(", "["]:
                raise ValueError("A sua ER não é uma expressão válida!")
            
            value = value.replace(f"{left_simbol}?", f"({left_simbol}|&)")

            index = value.find("?")
        
        index = value.find("+")
        while index != -1:
            try:
                left_simbol = value[index-1]
            except:
                raise ValueError("O símbolo '+' não pode estar no começo de uma ER!")

            if left_simbol in ["*", "|", ".", "?", "+", "(", "["]:
                raise ValueError("A sua ER não é uma expressão válida!")
        
            if left_simbol not in [")", "]"]:
                value = value.replace(f"{left_simbol}+", f"{left_simbol}{left_simbol}*")
            else:
                stack = list(left_simbol)
                string = list(left_simbol)
                close_char = str()

                if left_simbol == ")":
                    close_char = "("

                else:
                    close_char = "["

                for i in range(index-2, -1, -1):
                    char = value[i]
                    string.insert(0, char)

                    if char == left_simbol:
                        stack.append(char)
                    elif char == close_char:
                        stack.pop()
                    
                    if len(stack) == 0:
                        break
                
                string = "".join(string)
                value = value.replace(f"{string}+", f"{string}{string}*")
            
            index = value.find("+")
        
        return value

    def gerar_infixa(self, value: str):
        isGrupo = False
        scape = False
        brackets = []
        last = None
        grupo = ""
        for s in value:
            if scape:
                scape = False
                remove_concat_inicial = len(self.infixa) == 0
                self.infixa.extend([".", f"\\{s}"])
                if remove_concat_inicial:
                    self.infixa.pop(0)
                last = f"\\{s}"
                continue
            else:
                if s == '\\':
                    scape = True
                    continue
                
            match s:
                case '[':
                    if not isGrupo:
                        isGrupo = True
                        grupo = "["
                        last = s
                        continue
                    else:
                        raise ValueError("Formação incorreta de '[]'")
                case ']':
                    if isGrupo:
                        isGrupo = False
                        grupo = f"{grupo}]"
                        grupo_expandido = self.expandir_grupo(grupo)
                        is_grupo_first = len(self.infixa) == 0
                        is_parentheses_first = len(self.infixa) > 0 and self.infixa[-1] == "("

                        if is_grupo_first or is_parentheses_first:
                            grupo_expandido.pop(0) # remove a concatenação desnecessária

                        print("infixa atual, no grupo: ", self.infixa)
                        print("grupo a ser incluido: ", grupo_expandido)
                        self.infixa.extend(grupo_expandido)

                case '(':
                    if isGrupo:
                        grupo = f"{grupo}("
                        raise ValueError(f"Grupo inválido: {grupo}")
                    brackets.append('(')
                    self.infixa.append("(")
                case ')':
                    if isGrupo:
                        grupo = f"{grupo})"
                        raise ValueError(f"Grupo inválido: {grupo}")
                    try:
                        brackets.pop()
                        self.infixa.append(')')
                    except:
                        raise ValueError("Formação incorreta de '()'")
                case _:
                    if isGrupo:
                        grupo = f"{grupo}{s}"
                        last = s
                        continue
                    self.infixa.append(s)

            if last != None and s not in ['|', '*', '+', '?', ')', ']'] and last not in ['|', '(', '[']:
                self.infixa.insert(-1, '.')
            
            last = s

        if len(brackets) != 0:
            raise ValueError("Formação incorreta de '()'")
        
        self.infixa.append(".")
        self.infixa.append("#")


    def expandir_grupo(self, grupo: str):
        grupo_expandido = []
        seq = set()
        for i, s in enumerate(grupo):
            if s in ['[',']']:
                continue
            try:
                prev, pos = grupo[i-1], grupo[i+1]
            except:
                raise ValueError(f"Grupo inválido: {grupo}")
            
            match s:
                case '-':
                    seq = seq.union(set(self.gerar_sequencia(f"{prev}-{pos}")))
                case _:
                    if pos != '-' and prev != '-':
                        seq.add(s)
        
        grupo_expandido.extend(seq)
        grupo_expandido = list('|'.join(grupo_expandido))
        grupo_expandido.insert(0, '(')
        grupo_expandido.insert(0, '.')
        grupo_expandido.append(')')
        return grupo_expandido

    def gerar_sequencia(self, sequencia: str):
        start, end = sequencia[0], sequencia[2]
        if start.isalpha() and end.isalpha() and start.isupper() and end.isupper() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        elif start.isalpha() and end.isalpha() and start.islower() and end.islower() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        elif start.isdigit() and end.isdigit() and start <= end:
            return [chr(c) for c in range(ord(start), ord(end) + 1)]
        else:
            raise ValueError(f"Sequência inválida: [{sequencia}]")
        
    def gerar_posfixa(self):
        pilha = []
        print(f"infixa: {self.infixa}")

        for s in self.infixa:
            if s == '(':
                pilha.append(s)
            elif s == ')':
                while pilha and pilha[-1] != '(':
                    self.posfixa.append(pilha.pop())
                pilha.pop()
            elif s in list(self.PRECEDENCIA.keys()):
                while (pilha and pilha[-1] != '(' and
                    self.PRECEDENCIA.get(s, 0) <= self.PRECEDENCIA.get(pilha[-1], 0)):
                    self.posfixa.append(pilha.pop())
                pilha.append(s)
            else:
                self.posfixa.append(s)

        while pilha:
            self.posfixa.append(pilha.pop())
        
    def convert_regular_expression_to_tree(self) -> Tree:
        stack = list()
        counter = 0

        tree = Tree()

        print(self.posfixa)

        for simbol in self.posfixa:
            node = None
            if simbol == "*":
                son = stack.pop()
                node = Node(simbol, son)

            elif simbol in ["|", "."]:
                right_son = stack.pop()
                left_son = stack.pop()
                node = Node(simbol, left_son, right_son)

            elif simbol != "&":
                counter += 1
                node = Node(simbol, value=str(counter))
                tree.node_value_to_token[str(counter)] = simbol

                if simbol == "#":
                    tree.acceptance_node = node

            else:
                node = Node(simbol)
            

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
    def posfixa(self):
        return self.__posfixa
    
    @posfixa.setter
    def posfixa(self, value):
        self.__posfixa = value

    @property
    def infixa(self):
        return self.__infixa
    
    @infixa.setter
    def infixa(self, value):
        self.__infixa = value

    def __str__(self):
        return "".join(self.infixa)
    
    def __repr__(self):
        return self.__str__()