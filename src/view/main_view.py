from PyQt5 import QtWidgets, uic


class MainView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(MainView, self).__init__()
        uic.loadUi('src/ui/main.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        self.label.setText("Teste")
        self.showMaximized()

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value