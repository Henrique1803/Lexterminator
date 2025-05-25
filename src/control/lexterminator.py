from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QStyle, QFileDialog
from PyQt5.QtCore import Qt
from pathlib import Path
from src.model.lexical_analyzer import LexicalAnalyzer
from src.view.welcome_view import WelcomeView # que carrega o .ui
from src.view.main_view import MainView  # que carrega o .ui
import shutil

from src.utils import paths

class LexicalAnalyzerController:
    def __init__(self):
        self.__view = WelcomeView(self)
        self.show()

    def show(self):
        self.view.showMaximized()

    def set_regular_definitions_file(self, path: str):
        try:
            self.__analyzer = LexicalAnalyzer(path)
            self.set_main_view()
            self.view.setup_table_view(self.analyzer.table)
            self.view.setup_diagram_view()
        except ValueError as e:
            self.show_error("Error in regular definitions file", str(e))

    def set_main_view(self):
        self.view.close()
        self.view = MainView(self)
        self.show()

    def show_error(self, title: str, error_message: str):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Error")
        dialog.setMinimumSize(500, 250)

        layout = QVBoxLayout()

        icon_label = QLabel()
        icon = self.view.style().standardIcon(QStyle.SP_MessageBoxCritical)
        icon_label.setPixmap(icon.pixmap(32, 32))

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        text_box.setFixedHeight(100)
        text_box.setText(error_message)
        layout.addWidget(text_box)

        button = QPushButton("OK")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button, alignment=Qt.AlignRight)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_success(self, title: str, success_message: str):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Success")
        dialog.setMinimumSize(500, 250)

        layout = QVBoxLayout()

        icon_label = QLabel()
        icon = self.view.style().standardIcon(QStyle.SP_DialogApplyButton)
        icon_label.setPixmap(icon.pixmap(32, 32))

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label)
        layout.addLayout(top_layout)

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        text_box.setFixedHeight(100)
        text_box.setText(success_message)
        layout.addWidget(text_box)

        button = QPushButton("OK")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button, alignment=Qt.AlignRight)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_automata_file(self):
        print("save file")
        file_path = self.select_save_file_path()
        if file_path:
            try:
                self.analyzer.regular_definitions.automata.to_file(file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except Exception as e:
                self.show_error("Error saving file", f"Could not save file: {e}")

    def save_automata_diagram(self):
        print("save diagram")
        file_path = self.select_save_file_path(type=".png")
        if file_path:
            try:
                shutil.copy(paths.AUTOMATA_DIAGRAM_DIR/ "automata_diagram.png", file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except:
                self.show_error("Error saving file", "Could not save file")

    def select_save_file_path(self, type: str = ".txt"):
        options = QFileDialog.Options()

        ext = type.lstrip(".")
        filtro = f"{ext.upper()} Files (*.{ext})"

        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            f"Select a {type} file",
            "",
            filtro,
            options=options
        )

        if file_path:
            if not file_path.endswith(type):
                file_path += type
            return file_path

        return None

    @property
    def analyzer(self):
        return self.__analyzer
    
    @analyzer.setter
    def analyzer(self, value):
        self.__analyzer = value

    @property
    def view(self):
        return self.__view
    
    @view.setter
    def view(self, value):
        self.__view = value
