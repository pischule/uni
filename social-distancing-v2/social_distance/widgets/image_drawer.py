import PySide6
from PySide6 import QtCore, QtGui, QtWidgets


class ImageDrawer(QtWidgets.QGraphicsView):
    pixmapChanged = QtCore.Signal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().paintEvent(event)

    @property
    def pixmap(self) -> QtGui.QPixmap:
        return self._pixmap_item.pixmap()

    @pixmap.setter
    def pixmap(self, pixmap):
        self._pixmap_item.setPixmap(pixmap)
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.pixmapChanged.emit(pixmap)

