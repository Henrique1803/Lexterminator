from regular_definitions import RegularDefinitions


class LexicalAnalyzer:

    def __init__(self):
        self.__regular_definitions = RegularDefinitions()


if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyzer()