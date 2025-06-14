from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QStyle, QFileDialog
from PyQt5.QtCore import Qt
from pathlib import Path
from src.model.lexical_analyzer import LexicalAnalyzer
from src.model.sintatical_analyzer import SintaticalAnalyzer
from src.view.welcome_view import WelcomeView
from src.view.main_view import MainView 
from src.view.token_view import TokenView 
from src.view.about_view import AboutView
import shutil

from src.utils import paths


class LexicalAndSintaticalAnalyzerController:
    """
    Classe que representa o controlador da interface, associando View com Model.
    """
    def __init__(self):
        self.__view = WelcomeView(self)
        
        self.set_grammar_file() # Deve ser removido com a implementação da janela de input para o arquivo da gramática (apenas para testes temporários)

        self.show()

    # exibe a view maximizada
    def show(self):
        self.view.showMaximized()

    # carrega o arquivo de definições regulares e atualiza a view de acordo
    def set_regular_definitions_file(self, path: str):
        try:
            self.__analyzer = LexicalAnalyzer(path)
            self.set_main_view()
            self.view.setup_table_view(self.analyzer.table)
            self.view.setup_diagram_view()
        except ValueError as e:
            self.show_error("Error in regular definitions file", str(e))
    
    def set_grammar_file(self, path: str = ""):
        try:
            path = paths.SINTATICAL_ANALYZER_INPUT_DIR /"grammar_example.txt" # Temporário até a janela para ler o arquivo da grámatica ser feita
            self.__sintatical_analyzer = SintaticalAnalyzer(path)
        except ValueError as e:
            self.show_error("Error in grammar file", str(e))
    
    # carrega o arquivo de entrada para ser reconhecido pelo AL e atualiza a view de acordo
    def set_input_file(self, path: str):
        try:
            self.analyzer.read_words_from_file_and_verify_pertinence(path)
            self.set_token_view()
            self.view.setup_table_view()
            self.sintatical_analyzer.read_tokens_from_lexical_analyzer_output(self.analyzer.output_path) # Faz a leitura da lista de tokens gerada pelo analisador léxico

        except ValueError as e:
            self.show_error("Error in input file", str(e))

    # atualiza a view como a MainView
    def set_main_view(self):
        self.view = MainView(self)
        self.show()
    
    # atualiza a view como a TokenView
    def set_token_view(self):
        self.view.deleteLater()
        self.view = TokenView(self)
        self.show()

    # exibe modal de erro
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

    # exibe modal de sucesso
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

    # trata o evento de click no botão de salvar o arquivo do autômato
    def save_automata_file(self):
        print("save token file")
        file_path = self.select_save_file_path()
        if file_path:
            try:
                self.analyzer.regular_definitions.automata.to_file(file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except Exception as e:
                self.show_error("Error saving file", f"Could not save file: {e}")
    
    # trata o evento de click no botão de salvar a lista de tokens reconhecidos
    def save_token_file(self):
        print("save file")
        file_path = self.select_save_file_path()
        if file_path:
            try:
                self.analyzer.write_words_result_to_file(file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except Exception as e:
                self.show_error("Error saving file", f"Could not save file: {e}")

    # trata o evento de click no botão de salvar o diagrama do autômato
    def save_automata_diagram(self):
        print("save diagram")
        file_path = self.select_save_file_path(type=".png")
        if file_path:
            try:
                shutil.copy(paths.AUTOMATA_DIAGRAM_DIR/ "automata_diagram.png", file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except:
                self.show_error("Error saving file", "Could not save file")

    # abre dialog com seletor de arquivos para salvar, de acordo com tipo especificado
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
    
    # retorna para a tela de welcome, permitindo criar um novo AL
    def return_to_welcome(self):
        self.view.deleteLater()
        self.view = WelcomeView(self)
        self.show()

    def show_about(self):
        self.about_window = AboutView(self.view)
        self.about_window.show()

    @property
    def analyzer(self):
        return self.__analyzer
    
    @analyzer.setter
    def analyzer(self, value):
        self.__analyzer = value

    @property
    def sintatical_analyzer(self):
        return self.__sintatical_analyzer
    
    @sintatical_analyzer.setter
    def sintatical_analyzer(self, value):
        self.__sintatical_analyzer = value

    @property
    def view(self):
        return self.__view
    
    @view.setter
    def view(self, value):
        self.__view = value
