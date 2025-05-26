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
    
    def change_tab(self, index):
        """
        Método que trata o evento de troca de tab no tabWidget
        """
        self.saveButton.clicked.disconnect()
        if index == 0:
            self.saveButton.setText("Save Automata File")
            self.saveButton.clicked.connect(self.controller.save_automata_file)
        else:
            self.saveButton.setText("Save Automata Diagram")
            self.saveButton.clicked.connect(self.controller.save_automata_diagram)

    def setup_diagram_view(self, image_path: str = paths.AUTOMATA_DIAGRAM_DIR/ "automata_diagram.png"):
        """
        Atualiza a imagem do diagrama no ZoomableGraphicsView widget utilizado.
        """
        print(image_path)
        self.automataDiagram.setImagePath(str(image_path))

    def setup_table_view(self, pretty_table: PrettyTable):
        """
        Atualiza o widget que exibe a tabela de transições do autômato, de acordo com um PrettyTable.
        """
        rows = pretty_table.rows
        headers = pretty_table.field_names
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

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