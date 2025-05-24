from src.model.lexical_analyzer import LexicalAnalyzer
from src.utils.paths import LEXICAL_ANALYZER_INPUT_DIR


import sys
from PyQt5.QtWidgets import QApplication
from src.control.lexterminator import LexicalAnalyzerController

def main():
    app = QApplication(sys.argv)
    
    controller = LexicalAnalyzerController()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

