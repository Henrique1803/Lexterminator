from PyQt5 import QtWidgets, uic


class WelcomeView(QtWidgets.QWidget):

    def __init__(self):
        super(WelcomeView, self).__init__()
        uic.loadUi('src/ui/welcome.ui', self)
        self.setup()

    def setup(self):
        pass