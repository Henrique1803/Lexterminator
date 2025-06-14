from src.model.regular_definitions import RegularDefinitions
from src.utils.paths import LEXICAL_ANALYZER_OUTPUT_DIR, REGULAR_DEFINITIONS_INPUT_DIR

from pathlib import Path
from typing import List


class LexicalAnalyzer:
    """
    Classe que representa o Analisador Léxico considerando as definições regulares de entrada.
    Utilizando as estruturas internas, gera o autômato finito determinístico para o AL.
    """

    def __init__(self, regular_definitions_path: str):
        self.__words: List[str] = list()
        self.__regular_definitions = RegularDefinitions(regular_definitions_path)
        self.__table = self.__regular_definitions.automata.transition_table()
        self.__words_result = None
        self.__output_path: Path = LEXICAL_ANALYZER_OUTPUT_DIR / "tokens_output.txt"
    
    def read_words_from_file_and_verify_pertinence(self, file_path: Path):
        """
        Lê arquivo de entrada e salva a lista de tokens reconhecidos em um diretório padrão
        """
        with open(file_path, "r", encoding="utf-8") as file:
            self.words = [str(word).strip() for word in file]
        
        self.verify_words_pertinence(self.output_path)
    
    def verify_words_pertinence(self, output_path: Path):
        """
        Itera pelas palavras buscando reconhecê-las com o autômato.
        Constrói a lista de tokens de acordo com o estado de aceitação
        retornado pelo autômato, ou erro.
        Salva a lista de tokens em um arquivo de saída, com diretório padrão.
        """
        regular_definitions_automata = self.regular_definitions.automata
        output_lines = []
        results = []

        for word in self.words:
            accepted, token = regular_definitions_automata.run(word)
            if accepted:
                results.append((word, token))
                output_lines.append(f"<{word},{token}>")
            else:
                results.append((word, "erro!"))
                output_lines.append(f"<{word},erro!>")

        self.words_result = results

        with open(output_path, "w", encoding="utf-8") as out_file:
            for line in output_lines:
                out_file.write(line + "\n")
        
    def write_words_result_to_file(self, output_path: Path):
        """
        Escreve os resultados de self.words_result no formato <word,token>
        em um arquivo escolhido pelo usuário
        """
        if self.words_result is None:
            raise ValueError("Nenhum resultado encontrado. Execute verify_words_pertinence() antes.")

        with open(output_path, "w", encoding="utf-8") as file:
            for word, token in self.words_result:
                file.write(f"<{word},{token}>\n")

    @property
    def words(self):
        return self.__words

    @words.setter
    def words(self, words: List[str]):
        self.__words = words

    @property
    def regular_definitions(self):
        return self.__regular_definitions
    
    @property
    def table(self):
        return self.__table
    
    @property
    def words_result(self):
        return self.__words_result

    @words_result.setter
    def words_result(self, words_result: List[str]):
        self.__words_result = words_result

    @property
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, output_path: Path):
        self.__output_path = output_path