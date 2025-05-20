from regular_expression import RegularExpression

from typing import Dict


class RegularDefinitions:
    
    def __init__(self):
        
        self.__regular_definitions: Dict[str, str|RegularExpression] = dict() #mapeia o nome da definição pra regex / grupo
        self.__regular_definitions_file = "input_regular_definitions/regular_definitions.txt"
    
        self._read_regular_definitions()
        self.convert_regular_definitions_to_regular_expressions()

    @property
    def regular_definitions(self):
        return self.__regular_definitions
    
    @property
    def regular_definitions_file(self):
        return self.__regular_definitions_file
    
    def _read_regular_definitions(self): 
        """
        Lê o arquivo de definições regulares, e constrói o dict regular_definitions
        """
        with open(self.regular_definitions_file, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file]
        
        for line in lines:
            lexeme, regular_expression = line.split()
            self.regular_definitions[lexeme[0:-1]] = regular_expression
    
    def convert_regular_definitions_to_regular_expressions(self): # instancia as regexs e atualia o regular_definitions
        for lexeme in self.regular_definitions:
            for lexeme_to_update, regular_expression_to_update in self.regular_definitions.items():
                if lexeme in regular_expression_to_update:
                    regex_from_lexeme = self.regular_definitions[lexeme]
                    new_regular_expression = regular_expression_to_update.replace(lexeme, f"({regex_from_lexeme})")
                    self.regular_definitions[lexeme_to_update] = new_regular_expression
        
        print(self.regular_definitions)
        
        for lexeme, regular_expression in self.regular_definitions.items():
            self.regular_definitions[lexeme] = RegularExpression(regular_expression)
        
        print(self.regular_definitions)

    def __str__(self):
        return 
