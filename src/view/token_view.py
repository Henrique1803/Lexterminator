from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class TokenView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(TokenView, self).__init__()
        uic.loadUi('src/ui/token.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        self.returnButton.clicked.connect(self.return_to_main)
        self.saveButton.clicked.connect(self.controller.save_token_file)

    def setup_table_view(self):
        words_result = self.controller.analyzer.words_result
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


    def return_to_main(self):
        self.close()
        self.controller.set_main_view()
        self.controller.view.setup_table_view(self.controller.analyzer.table)
        self.controller.view.setup_diagram_view()

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value