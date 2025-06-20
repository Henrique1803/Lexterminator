from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QObject):
    """
    Executa uma função longa em segundo plano (thread separada),
    emitindo sinais ao finalizar ou em caso de erro.
    """

    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, fn, on_success, on_error=None, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self._thread = QThread()
        self.moveToThread(self._thread)

        # Conexões
        self._thread.started.connect(self.run)
        self.finished.connect(on_success)
        self.finished.connect(self._thread.quit)
        self.finished.connect(self.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        if on_error:
            self.error.connect(on_error)
            self.error.connect(self._thread.quit)
            self.error.connect(self.deleteLater)

    def start(self):
        """Inicia a thread de execução"""
        self._thread.start()

    def run(self):
        """Executa a função em background"""
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))