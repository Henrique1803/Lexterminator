from src.regular_expression import RegularExpression
from src.finite_automata import FiniteAutomata
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
            token, regular_expression = line.split()
            self.tokens.append(token[0:-1])
            self.regular_definitions[token[0:-1]] = regular_expression        
    
    def convert_regular_definitions_to_regular_expressions(self): # instancia as regexs e atualia o regular_definitions
        for token in self.regular_definitions:
            for token_to_update, regular_expression_to_update in self.regular_definitions.items():
                if token in regular_expression_to_update:
                    regex_from_token = self.regular_definitions[token]
                    new_regular_expression = regular_expression_to_update.replace(token, f"({regex_from_token})")
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
        
        self.automata = automatas[0].determinize()
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