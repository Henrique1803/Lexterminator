from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

class AboutView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Path("src/ui/about.ui"), self)
        with open("README.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()

        self.mdText.setTextFormat(Qt.MarkdownText)
        self.mdText.setText(markdown_content)
        self.mdText.setWordWrap(True)
