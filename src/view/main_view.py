from src.view.utils.zoomable_graphics_view import ZoomableGraphicsView
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from prettytable import PrettyTable

from src.utils import paths


class MainView(QtWidgets.QMainWindow):
    """
    Classe que representa a View Principal, de acordo com o layout 'src/ui/main.ui'.
    Trata eventos relacionados a interface e interage com o controller.
    """

    def __init__(self, controller):
        super(MainView, self).__init__()
        uic.loadUi('src/ui/main.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        """
        Configura eventos nos componentes para determinados métodos.
        """
        self.tabWidget.currentChanged.connect(self.change_tab)
        self.saveButton.setText("Save Automata File")
        self.saveButton.clicked.connect(self.controller.save_automata_file)
        self.actionClose.triggered.connect(self.close_and_return_to_welcome)
        self.actionOpen_file_to_recognize.triggered.connect(self.select_input_file)
        self.actionAbout.triggered.connect(self.controller.show_about)
    
    def change_tab(self, index):
        """
        Método que trata o evento de troca de tab no tabWidget
        """
        self.saveButton.clicked.disconnect()
        if index == 0:
            self.saveButton.setText("Save Automata File")
            self.saveButton.clicked.connect(self.controller.save_automata_file)
        elif index == 1:
            self.saveButton.setText("Save Automata Diagram")
            self.saveButton.clicked.connect(self.controller.save_automata_diagram)
        elif index == 2:
            self.saveButton.setText("Save SLR Table")
            self.saveButton.clicked.connect(self.controller.save_slr_table)
        else:
            self.saveButton.setText("Save Canonical Items")
            self.saveButton.clicked.connect(self.controller.save_canonical_items)

    def setup_automata_diagram_view(self, image_path: str = paths.AUTOMATA_DIAGRAM_DIR/ "automata_diagram.png"):
        """
        Atualiza a imagem do diagrama no ZoomableGraphicsView widget utilizado.
        """
        print(image_path)
        self.automataDiagram.setImagePath(str(image_path))

    def setup_automata_table_view(self, pretty_table: PrettyTable):
        """
        Atualiza o widget que exibe a tabela de transições do autômato, de acordo com um PrettyTable.
        """
        rows = pretty_table.rows
        headers = pretty_table.field_names
        self.automataTable.setColumnCount(len(headers))
        self.automataTable.setRowCount(len(rows))
        self.automataTable.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.automataTable.setItem(i, j, item)
        self.automataTable.resizeColumnsToContents()

    def setup_slr_table_view(self, pretty_table: PrettyTable):
        """
        Atualiza o widget que exibe a tabela slr, de acordo com um PrettyTable.
        """
        headers = pretty_table.field_names
        rows = pretty_table.rows

        total_columns = len(headers)
        total_rows = len(rows)

        dollar_index = headers.index("$")

        action_start = 1  # após STATE
        action_end = dollar_index
        action_span = action_end - action_start + 1  # inclusive o "$"

        goto_start = dollar_index + 1
        goto_span = total_columns - goto_start

        # Tabela com 2 linhas extras (agrupamento + headers)
        self.slrTable.setColumnCount(total_columns)
        self.slrTable.setRowCount(total_rows + 2)

        # Linha 0: cabeçalho agrupado
        state_item = QTableWidgetItem("")
        state_item.setFlags(state_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slrTable.setItem(0, 0, state_item)

        if action_span > 0:
            self.slrTable.setSpan(0, action_start, 1, action_span)
            action_item = QTableWidgetItem("ACTION")
            action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.slrTable.setItem(0, action_start, action_item)

        if goto_span > 0:
            self.slrTable.setSpan(0, goto_start, 1, goto_span)
            goto_item = QTableWidgetItem("GOTO")
            goto_item.setFlags(goto_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            goto_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.slrTable.setItem(0, goto_start, goto_item)

        # Linha 1: headers reais
        for col, header in enumerate(headers):
            item = QTableWidgetItem(str(header))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.slrTable.setItem(1, col, item)

        # Demais linhas: dados da tabela
        for row_idx, row in enumerate(rows):
            for col_idx, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.slrTable.setItem(row_idx + 2, col_idx, item)

        self.slrTable.resizeColumnsToContents()

    def setup_canonical_items_diagram_view(self, image_path: str = paths.CANONICAL_ITEMS_DIAGRAM_DIR/ "canonical_items_diagram.png"):
        """
        Atualiza a imagem dos items canônicos no ZoomableGraphicsView widget utilizado.
        """
        print(image_path)
        self.slrItems.setImagePath(str(image_path))

    def close_and_return_to_welcome(self):
        """
        Retorna a tela inicial.
        """
        self.controller.return_to_welcome()

    def select_input_file(self):
        """
        Método que abre um dialog para seleção de um arquivo .txt de entrada
        referente ao arquivo a ser reconhecido pelo Analisador Léxico.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a .txt file",
            "",
            "Text Files (*.txt)",
            options=options
        )
        
        if file_path:
            self.controller.set_input_file(file_path)

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value