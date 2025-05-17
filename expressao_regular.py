

class ExpressaoRegular:

    PRECEDENCIA = {
        "*": 0,
        "+": 0,
        "?": 0,
        ".": 1,
        "|": 2
    }

    def __init__(self, value: str):
        self.__posfixa = []
        self.__infixa = []
        self.gerar_infixa(value.replace(" ", "").replace("\n", "").replace("\t", "").replace(".", ""))
        print(self.infixa)

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
                        remove_concat_inicial = len(self.infixa) == 0
                        self.infixa.extend(grupo_expandido)
                        if remove_concat_inicial:
                            self.infixa.pop(0)

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

if __name__ == "__main__":
    er = ExpressaoRegular("[a-c]\\[?f")