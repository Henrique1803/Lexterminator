import os
from src.model.lexical_analyzer import LexicalAnalyzer
from src.utils.paths import LEXICAL_ANALYZER_INPUT_DIR


import sys
from PyQt5.QtWidgets import QApplication
from src.control.lexterminator import LexicalAndSintaticalAnalyzerController

def main():
    if sys.platform.startswith("linux") and os.environ.get("XDG_SESSION_TYPE") == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"  # Força Wayland caso esteja usando Ubuntu
    
    app = QApplication(sys.argv)
    
    controller = LexicalAndSintaticalAnalyzerController()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()