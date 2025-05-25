from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)

    def setup(self):
        print(self.__image_path)
        pixmap = QPixmap(self.__image_path)
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.setScene(scene)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom_factor, zoom_factor)

    def setImagePath(self, image_path: str):
        self.__image_path = image_path
        self.setup()