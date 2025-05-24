from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path
from src.model.lexical_analyzer import LexicalAnalyzer
from src.view.welcome import WelcomeView  # que carrega o .ui

class LexicalAnalyzerController:
    def __init__(self):
        self.view = WelcomeView()
        self.analyzer = LexicalAnalyzer()
        self.show()


    def show(self):
        self.view.show()
