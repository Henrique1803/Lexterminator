class RegularDefinitions:
    
    def __init__(self):
        
        self.__regular_definitions = dict() #mapeia o nome da definição pra regex / grupo
    
    def _read_regular_definitions(self): #lê o arquivo de definições
        ...
    
    def convert_regular_definitions_to_regular_expressions(self): # instancia as regexs e atualia o regular_definitions
        ...