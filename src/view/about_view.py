from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from pathlib import Path

class AboutView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Path("src/ui/about.ui"), self)
