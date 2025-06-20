from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QWizardPage
from PyQt5.QtGui import QFontDatabase, QFont, QMovie

from src.view.worker import Worker


class WelcomeWizard(QtWidgets.QWizard):
    """
    Classe que representa o assistente inicial, de acordo com o layout 'src/ui/welcome-wizard.ui'.
    Cada página representa uma etapa do carregamento de arquivos.
    """

    def __init__(self, controller):
        super(WelcomeWizard, self).__init__()
        uic.loadUi('src/ui/welcome-wizard.ui', self)
        self.__controller = controller
        self.setup()

    def setup(self):
        # Carregar fonte personalizada
        font_id = QFontDatabase.addApplicationFont("src/ui/resources/Audiowide-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(20)

        # seta barras de carregamento
        self.loading1_gif = QMovie("src/ui/resources/loading.gif")
        self.loading2_gif = QMovie("src/ui/resources/loading.gif")
        self.loading1.setMovie(self.loading1_gif)
        self.loading1.setVisible(False)
        self.loading2.setMovie(self.loading2_gif)
        self.loading2.setVisible(False)

        # Seta variáveis de controle
        self.lexical_ready = False
        self.sintatical_ready = True

        # Página 1: Seleção do arquivo de definições regulares
        self.buttonSelectFile.clicked.connect(self.select_regular_definitions_file)
        self.regular_definitions_filepath = None
        self.page(0).isComplete = self.page1_is_complete
        self.page(0).completeChanged.emit()

        # Página 2: Seleção do segundo arquivo
        self.buttonSelectFile_2.clicked.connect(self.select_grammar_file)
        self.grammar_filepath = None
        self.page(1).isComplete = self.page2_is_complete
        self.page(1).completeChanged.emit()

        # Botão finalizar (Finish)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish)

    def page1_is_complete(self):
        return self.lexical_ready

    def page2_is_complete(self):
        return self.sintatical_ready

    def select_regular_definitions_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o primeiro arquivo (.txt)", "", "Text Files (*.txt)"
        )
        if file_path:
            self.lexical_ready = False
            self.loading1_gif.start()
            self.loading1.setVisible(True)
            self.buttonSelectFile.setEnabled(False)
            self.worker_lexical = Worker(
                fn=self.__controller.set_regular_definitions_file,
                on_success=self.on_lexical_analyzer_ready,
                on_error=self.show_error_lexical_analyzer,
                path=file_path
            )
            self.worker_lexical.start()
    
    def select_grammar_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o segundo arquivo (.txt)", "", "Text Files (*.txt)"
        )
        if file_path:
            self.sintatical_ready = False
            self.loading2_gif.start()
            self.loading2.setVisible(True)
            self.buttonSelectFile_2.setEnabled(False)
            self.worker_sintatical = Worker(
                fn=self.__controller.set_grammar_file,
                on_success=self.on_sintatical_analyzer_ready,
                on_error=self.show_error_sintatical_analyzer,
                path=file_path
            )
            self.worker_sintatical.start()

    def show_error_lexical_analyzer(self, error_message: str):
        self.buttonSelectFile.setEnabled(True)
        self.loading1_gif.stop()
        self.loading1.setVisible(False)
        self.__controller.show_error("Error in regular definitions file", error_message)

    def show_error_sintatical_analyzer(self, error_message: str):
        self.buttonSelectFile_2.setEnabled(True)
        self.loading2_gif.stop()
        self.loading2.setVisible(False)
        self.__controller.show_error("Error in grammar file", error_message)

    def on_lexical_analyzer_ready(self):
        self.buttonSelectFile.setEnabled(True)
        self.loading1_gif.stop()
        self.loading1.setVisible(False)
        self.lexical_ready = True
        self.page(0).completeChanged.emit()

    def on_sintatical_analyzer_ready(self):
        self.buttonSelectFile_2.setEnabled(True)
        self.loading2_gif.stop()
        self.loading2.setVisible(False)
        self.sintatical_ready = True
        self.page(1).completeChanged.emit()

    def finish(self):
        self.close()
        self.__controller.set_main_view()

    @property
    def controller(self):
        return self.__controller

    @controller.setter
    def controller(self, value):
        self.__controller = value