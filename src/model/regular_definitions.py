from src.model.regular_expression import RegularExpression
from src.model.finite_automata import FiniteAutomata
from src.utils.paths import FA_OUTPUT_DIR

from pathlib import Path
from typing import Dict, List


class RegularDefinitions:
    
    def __init__(self, regular_definitions_file: Path):
        self.__tokens: List[str] = list()
        self.__regular_definitions: Dict[str, str|RegularExpression] = dict() #mapeia o nome da definição pra regex / grupo
        self.__regular_definitions_file: Path = regular_definitions_file
        self.__automata: FiniteAutomata = None
    
        self._read_regular_definitions()
        self.convert_regular_definitions_to_regular_expressions()
        self.regular_expressions_automata_union()

    
    def _read_regular_definitions(self): 
        """
        Lê o arquivo de definições regulares, e constrói o dict regular_definitions
        """
        with open(self.regular_definitions_file, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file]
        
        for line in lines:
            token_index = line.find(":")
            token, regular_expression = (str(), str())
            if token_index != -1:
                token = line[0:token_index]
                regular_expression = line[token_index+1:len(line)]
            else:
                raise ValueError("Má formação: definições regulares esperadas na forma 'token: expressao'")
            self.tokens.append(token)
            self.regular_definitions[token] = regular_expression

    def _verify_subexpressions(self, regex: str):
        stack = []
        subexpressions = set()
        subexpression = ""
        last_char = ""
        for char in regex:
            is_scape = last_char in ["", "\\"]
            if subexpression:
                subexpression = f"{subexpression}{char}"
            match char:
                case '<':
                    if not is_scape:
                        stack.append("<")
                        subexpression = f"{subexpression}{char}"
                case '>':
                    if not is_scape:
                        try:
                            stack.pop()
                            subexpressions.add(subexpression)
                            subexpression = ""
                        except:
                            raise ValueError(f"Expressão má formada: {regex}")
            last_char = char
        
        if len(stack) > 0:
            raise ValueError(f"Expressão má formada: {regex}")
        
        for subexpression in subexpressions:
            try:
                regex_from_token = self.regular_definitions[subexpression[1:-1]]
            except:
                raise ValueError(f"Subexpressão má formada: definição {subexpression[1:-1]} inexistente")
            regex = regex.replace(subexpression, f"({regex_from_token})")
        
        return regex
    
    def convert_regular_definitions_to_regular_expressions(self): # instancia as regexs e atualia o regular_definitions
        for token in self.regular_definitions:
            for token_to_update, regular_expression_to_update in self.regular_definitions.items():
                new_regular_expression = self._verify_subexpressions(regular_expression_to_update)
                self.regular_definitions[token_to_update] = new_regular_expression
                        
        for token, regular_expression in self.regular_definitions.items():
            self.regular_definitions[token] = RegularExpression(regular_expression, token)
        
    def regular_expressions_automata_union(self):
        automatas: List[FiniteAutomata] = list()
        for regular_expression in self.regular_definitions.values():
            automatas.append(regular_expression.automata)
        
        while len(automatas) != 1:
            automata1, automata2 = automatas[0:2]
            new_automata = FiniteAutomata.union(automata1, automata2)
            automatas = automatas[2:]
            automatas.append(new_automata)
        
        self.automata = automatas[0].determinize(self.__tokens)
        self.automata.to_file(str(FA_OUTPUT_DIR / "af_output.txt"))       
        
    def __str__(self):
        return

    @property
    def tokens(self):
        return self.__tokens

    @property
    def regular_definitions(self):
        return self.__regular_definitions
    
    @property
    def regular_definitions_file(self):
        return self.__regular_definitions_file
    
    @property
    def automata(self):
        return self.__automata
    
    @automata.setter
    def automata(self, automata: FiniteAutomata):
        self.__automata = automata