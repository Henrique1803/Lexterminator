from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFontDatabase, QFont


class WelcomeView(QtWidgets.QMainWindow):
    """
    Classe que representa a view inicial, de acordo com o layout 'src/ui/welcome.ui'.
    Trata eventos relacionados a interface e interage com o controller.
    """

    def __init__(self, controller):
        super(WelcomeView, self).__init__()
        uic.loadUi('src/ui/welcome.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        """
        Configura eventos nos componentes para determinados métodos.
        Carrega a fonte estilizada utilizada no título.
        """
        self.setFixedSize(862, 452)
        font_id = QFontDatabase.addApplicationFont("src/ui/resources/Audiowide-Regular.ttf")
        if font_id == -1:
            print("Error loading Audiowide font!")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(20)
            self.title.setFont(font)
        self.buttonSelectFile.clicked.connect(self.select_regular_definitions_file)

    def select_regular_definitions_file(self):
        """
        Método que abre um dialog para seleção de um arquivo .txt de entrada
        referente ao arquivo de definições regulares.
        Envia o caminho do arquivo para o controller.
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
            self.close()
            self.controller.set_regular_definitions_file(file_path)

    @property
    def controller(self):
        return self.__controller
    
    @controller.setter
    def controller(self, value):
        self.__controller = value