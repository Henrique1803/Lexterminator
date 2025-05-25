from src.view.utils.zoomable_graphics_view import ZoomableGraphicsView
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from prettytable import PrettyTable

from src.utils import paths


class MainView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(MainView, self).__init__()
        uic.loadUi('src/ui/main.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        pass

    def setup_diagram_view(self, image_path: str = paths.AUTOMATA_DIAGRAM_DIR/ "automata_diagram.png"):
        print(image_path)
        self.automataDiagram.setImagePath(str(image_path))

    def setup_table_view(self, pretty_table: PrettyTable):
        rows = pretty_table.rows
        headers = pretty_table.field_names
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value