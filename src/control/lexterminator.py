from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QStyle, QFileDialog,  QLabel, QCheckBox
from PyQt5.QtCore import Qt
from pathlib import Path
from src.model.lexical_analyzer import LexicalAnalyzer
from src.model.sintatical_analyzer import SintaticalAnalyzer
from src.view.welcome_wizard import WelcomeWizard
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
        self.__view = WelcomeWizard(self)
        self.show(maximized=False)

    # exibe a view (welcome minimizada, e main maximizada)
    def show(self, maximized = True):
        if maximized:
            self.view.showMaximized()
        else:
            self.view.show()

    # carrega o arquivo de definições regulares e cria o analisador léxico
    def set_regular_definitions_file(self, path: str):
        self.__lexical_analyzer = LexicalAnalyzer(path)
    
    # carrega o arquivo da gramátila e cria o analisador sintático
    def set_grammar_file(self, path: str = ""):
        self.__sintatical_analyzer = SintaticalAnalyzer(path, set(self.lexical_analyzer.regular_definitions.tokens))
    
    # carrega o arquivo de entrada para ser reconhecido pelo AL e atualiza a view de acordo
    def set_input_file(self, path: str, ignore_whitespaces = False):
        self.__last_ignore_whitespaces = ignore_whitespaces
        self.__last_filepath = path
        try:
            self.lexical_analyzer.read_words_from_file_and_verify_pertinence(path, ignore_whitespaces)
            self.set_token_view()
            self.view.update_handle_run_sintatical()
            self.view.setup_tokens_table_view()

        except ValueError as e:
            self.show_error("Error in input file", str(e))

    def select_input_file(self):
        """
        Abre um QFileDialog com um checkbox adicional ("Ignore whitespaces from file")
        e envia o caminho + a opção marcada para o controller.
        """
        # Cria o QFileDialog como instância
        dialog = QFileDialog(self.view)
        dialog.setWindowTitle("Select a .txt file")
        dialog.setNameFilter("Text Files (*.txt)")
        dialog.setFileMode(QFileDialog.ExistingFile)

        # Cria e adiciona o checkbox personalizado
        checkbox = QCheckBox("Ignore whitespaces from file")
        checkbox.setChecked(True)

        # Espaçamento visual e adição ao layout do diálogo
        layout = dialog.layout()
        layout.addWidget(QLabel(" "), layout.rowCount(), 0, 1, layout.columnCount())
        layout.addWidget(checkbox, layout.rowCount(), 0, 1, layout.columnCount())

        # Executa o diálogo
        if dialog.exec_():
            file_path = dialog.selectedFiles()[0]
            ignore_whitespaces = checkbox.isChecked()
            self.set_input_file(file_path, ignore_whitespaces)
    
    # executa novamente a análise léxica com o mesmo arquivo aberto
    def rerun_lexical(self):
        self.set_input_file(self.__last_filepath, self.__last_ignore_whitespaces)

    # executa a análise sintática e atualiza a view de acordo
    def run_sintatical_analysis(self):
        parsing_table, passed = self.sintatical_analyzer.read_tokens_from_lexical_analyzer_output(self.lexical_analyzer.output_path) # Faz a leitura da lista de tokens gerada pelo analisador léxico
        self.view.setup_parsing_table_view(parsing_table)
        if passed:
            self.show_success("Sintatical Analysis finished", "Sintatical analysis completed successfully. No errors were found.")
        else:
            self.show_error("Sintatical Error", "An unexpected token was found that does not match the expected grammar.")

    # atualiza a view como a MainView
    def set_main_view(self):
        self.view = MainView(self)
        self.view.setup_automata_table_view(self.lexical_analyzer.table)
        self.view.setup_automata_diagram_view()
        self.view.setup_slr_table_view(self.sintatical_analyzer.pretty_table)
        self.view.setup_canonical_items_diagram_view()
        self.show()
    
    # atualiza a view como a TokenView
    def set_token_view(self):
        if not isinstance(self.view, TokenView):
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
                self.lexical_analyzer.regular_definitions.automata.to_file(file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except Exception as e:
                self.show_error("Error saving file", f"Could not save file: {e}")
    
    # trata o evento de click no botão de salvar a lista de tokens reconhecidos
    def save_token_file(self):
        print("save file")
        file_path = self.select_save_file_path()
        if file_path:
            try:
                self.lexical_analyzer.write_words_result_to_file(file_path)
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

    # trata o evento de click no botão de salvar a tabela slr
    def save_slr_table(self):
        print("save slr table")
        file_path = self.select_save_file_path(type=".csv")
        if file_path:
            try:
                shutil.copy(paths.SLR_TABLE_DIR/ "slr_table.csv", file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except:
                self.show_error("Error saving file", "Could not save file")

    # trata o evento de click no botão de salvar a tabela de parsing
    def save_parsing_table(self):
        print("save parsing table")
        file_path = self.select_save_file_path(type=".csv")
        if file_path:
            try:
                shutil.copy(paths.PARSING_TABLE_DIR/ "parsing_table.csv", file_path)
                self.show_success("File saved", f"File saved successfully in: {file_path}")
            except:
                self.show_error("Error saving file", "Could not save file")

    # trata o evento de click no botão de salvar items canônicos
    def save_canonical_items(self):
        print("save canonical items")
        file_path = self.select_save_file_path(type=".png")
        if file_path:
            try:
                shutil.copy(paths.CANONICAL_ITEMS_DIAGRAM_DIR/ "canonical_items_diagram.png", file_path)
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
        self.__view = WelcomeWizard(self)
        self.show(maximized=False)

    # abre a tela de sobre
    def show_about(self):
        self.about_window = AboutView(self.view)
        self.about_window.show()

    @property
    def lexical_analyzer(self):
        return self.__lexical_analyzer
    
    @lexical_analyzer.setter
    def lexical_analyzer(self, value):
        self.__lexical_analyzer = value

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