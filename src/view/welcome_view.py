from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog


class WelcomeView(QtWidgets.QWidget):

    def __init__(self, controller):
        super(WelcomeView, self).__init__()
        uic.loadUi('src/ui/welcome.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        self.setFixedSize(862, 452)
        self.buttonSelectFile.clicked.connect(self.select_regular_definitions_file)

    def select_regular_definitions_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a .txt file",
            "",
            "Text Files (*.txt)",
            options=options
        )
        
        if file_path:
            self.controller.set_regular_definitions_file(file_path)

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value