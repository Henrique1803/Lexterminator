from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

class ZoomableGraphicsView(QGraphicsView):
    """
    Classe Widget do PyQt que abstrai a criação do QGraphicsView,
    inserindo uma imagem como cena, e permitindo eventos de zoom e drag
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def setup(self):
        """
        Configura widget com o caminho da imagem de entrada.
        """
        print(self.__image_path)
        pixmap = QPixmap(self.__image_path)
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.setScene(scene)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        """
        Trata o evento de zoom na imagem.
        """
        zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom_factor, zoom_factor)

    def setImagePath(self, image_path: str):
        """
        Setter público utilizado pelas demais classes ao utilizar este Widget.
        """
        self.__image_path = image_path
        self.setup()