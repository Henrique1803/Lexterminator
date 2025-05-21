from src.regular_definitions import RegularDefinitions
from src.utils.paths import REGULAR_DEFINITIONS_INPUT_DIR

from pathlib import Path
from typing import List


class LexicalAnalyzer:

    def __init__(self):
        self.__words: List[str] = list()
        self.__regular_definitions = RegularDefinitions(REGULAR_DEFINITIONS_INPUT_DIR / "regular_definitions.txt")
    
    def read_words_from_file_and_verify_pertinence(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as file:
            self.words = [str(word).strip() for word in file]
        
        self.verify_words_pertinence()
    
    def verify_words_pertinence(self):
        regular_definitions_automata = self.regular_definitions.automata
        for word in self.words:
            print(regular_definitions_automata.run(word))
        
        print()

    @property
    def words(self):
        return self.__words

    @words.setter
    def words(self, words: List[str]):
        self.__words = words

    @property
    def regular_definitions(self):
        return self.__regular_definitions