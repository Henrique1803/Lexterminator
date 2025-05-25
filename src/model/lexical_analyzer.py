from src.model.regular_definitions import RegularDefinitions
from src.utils.paths import LEXICAL_ANALYZER_OUTPUT_DIR, REGULAR_DEFINITIONS_INPUT_DIR

from pathlib import Path
from typing import List


class LexicalAnalyzer:

    def __init__(self, regular_definitions_path: str):
        self.__words: List[str] = list()
        self.__regular_definitions = RegularDefinitions(regular_definitions_path)
        self.__table = self.__regular_definitions.automata.transition_table()
    
    def read_words_from_file_and_verify_pertinence(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as file:
            self.words = [str(word).strip() for word in file]
        
        self.verify_words_pertinence(Path(LEXICAL_ANALYZER_OUTPUT_DIR / "tokens_output.txt"))
    
    def verify_words_pertinence(self, output_path: Path):
        regular_definitions_automata = self.regular_definitions.automata
        output_lines = []

        for word in self.words:
            accepted, token = regular_definitions_automata.run(word)
            if accepted:
                output_lines.append(f"<{word},{token}>")
            else:
                output_lines.append(f"<{word},erro!>")

        with open(output_path, "w", encoding="utf-8") as out_file:
            for line in output_lines:
                out_file.write(line + "\n")


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