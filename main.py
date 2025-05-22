from src.lexical_analyzer import LexicalAnalyzer
from src.utils.paths import LEXICAL_ANALYZER_INPUT_DIR


if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyzer()
    #lexical_analyzer.read_words_from_file_and_verify_pertinence(LEXICAL_ANALYZER_INPUT_DIR / "words.txt")
    #lexical_analyzer.read_words_from_file_and_verify_pertinence(LEXICAL_ANALYZER_INPUT_DIR/ "words2.txt")