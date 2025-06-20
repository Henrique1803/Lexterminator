from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from prettytable import PrettyTable

class TokenView(QtWidgets.QMainWindow):
    """
    Classe que representa a view da lista de tokens, de acordo com o layout 'src/ui/token.ui'.
    Trata eventos relacionados a interface e interage com o controller.
    """

    def __init__(self, controller):
        super(TokenView, self).__init__()
        uic.loadUi('src/ui/token.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        """
        Configura eventos nos componentes para determinados métodos.
        """
        self.returnButton.clicked.connect(self.return_to_main)
        self.actionSave_Token_List_File.triggered.connect(self.controller.save_token_file)
        self.actionSaveParsingTable.triggered.connect(self.controller.save_parsing_table)
        self.actionCompile_New_File.triggered.connect(self.controller.select_input_file)
        self.runSintatical.clicked.connect(self.handle_button_run_click)

    def handle_button_run_click(self):
        """
        Trata o evento de click no botão de run, de acordo com a análise sintática,
        ou executa novamente a análise léxica
        """
        if "Sintatical" in self.runSintatical.text():
            self.controller.run_sintatical_analysis()
        else:
            self.controller.rerun_lexical()

    def update_handle_run_sintatical(self):
        """
        Atualiza a view após a análise léxica, liberando para a análise sintática ou não.
        """
        if self.controller.lexical_analyzer.lexical_error:
            self.runSintatical.setEnabled(False)
            self.runSintatical.setVisible(False)
            self.controller.show_error("Lexical Error", "Lexical analysis failed due to unrecognized characters.")
        else:
            self.runSintatical.setEnabled(True)
            self.runSintatical.setVisible(True)
            self.controller.show_success("Lexical Analysis finished", "Lexical analysis completed successfully. No errors were found.")

    def setup_tokens_table_view(self):
        """
        Configura widget que exibe a lista de tokens em formato de tabela,
        de acordo com words_result do analyzer.
        """
        self.runSintatical.setText("Run Sintatical Analysis")
        self.actionSaveParsingTable.setEnabled(False)
        words_result = self.controller.lexical_analyzer.words_result
        headers = ["Word", "Token"]
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(words_result))
        self.table.setHorizontalHeaderLabels(headers)

        for i, (word, token) in enumerate(words_result):
            word_item = QTableWidgetItem(word)
            word_item.setTextAlignment(Qt.AlignCenter)
            word_item.setFlags(word_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            token_item = QTableWidgetItem(token)
            token_item.setTextAlignment(Qt.AlignCenter)
            token_item.setFlags(token_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            if token.lower() == "erro!":
                token_item.setForeground(QColor("red"))

            self.table.setItem(i, 0, word_item)
            self.table.setItem(i, 1, token_item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()

    def setup_parsing_table_view(self, pretty_table: PrettyTable):
        """
        Atualiza o widget que exibe a tabela de parsing da análise sintática, de acordo com um PrettyTable.
        """
        self.runSintatical.setText("Rerun Lexical Analysis")
        self.actionSaveParsingTable.setEnabled(True)
        rows = pretty_table.rows
        headers = pretty_table.field_names
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if str(cell).lower() == "erro":
                    item.setForeground(QColor("red"))
                elif str(cell).lower() == "accept":
                    item.setForeground(QColor("green"))
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def return_to_main(self):
        """
        Retorna par a main view.
        """
        self.close()
        self.controller.set_main_view()
        self.controller.view.setup_automata_table_view(self.controller.lexical_analyzer.table)
        self.controller.view.setup_automata_diagram_view()

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value