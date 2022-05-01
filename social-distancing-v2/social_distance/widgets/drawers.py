import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPixmap


class PolygonDrawer(QtWidgets.QGraphicsView):
    polygonChanged = QtCore.Signal(QtGui.QPolygonF)

    def __init__(self, parent=None, line_width=1):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)

        self._polygon_item = QtWidgets.QGraphicsPolygonItem(self._pixmap_item)
        self._polygon_item.setPen(QtGui.QPen(QtCore.Qt.black, line_width, QtCore.Qt.SolidLine))
        self._polygon_item.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.VerPattern))

    @property
    def pixmap(self):
        return self._pixmap_item.pixmap()

    @pixmap.setter
    def pixmap(self, pixmap):
        self._pixmap_item.setPixmap(pixmap)
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().paintEvent(event)

    @property
    def polygon(self) -> QtGui.QPolygonF:
        return self._polygon_item.polygon()

    @polygon.setter
    def polygon(self, polygon: QtGui.QPolygonF):
        self._polygon_item.setPolygon(polygon)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        sp: QPointF = self.mapToScene(event.position().toPoint())
        lp: QPointF = self._pixmap_item.mapFromScene(sp)

        poly = self._polygon_item.polygon()
        poly.append(lp)
        self._polygon_item.setPolygon(poly)
        self.polygonChanged.emit(self.polygon)

    def reset(self):
        self._polygon_item.setPolygon(QtGui.QPolygonF())


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


class SquareDrawer(QtWidgets.QGraphicsView):
    polygonChanged = QtCore.Signal(QtGui.QPolygonF)

    def __init__(self, parent=None, point_radius: int = 10, line_width: int = 5):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)

        self._polygon_item = QtWidgets.QGraphicsPolygonItem([
            QtCore.QPoint(100, 100),
            QtCore.QPoint(100, 400),
            QtCore.QPoint(400, 400),
            QtCore.QPoint(400, 100)
        ], self._pixmap_item)
        self._polygon_item.setPen(QtGui.QPen(QtCore.Qt.black, line_width, QtCore.Qt.SolidLine))
        self._polygon_item.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.VerPattern))
        self._point_radius = point_radius

        self._selected_point_index = None

        self._point_items = []

        # draw points
        for point in self._polygon_item.polygon():
            item = QtWidgets.QGraphicsEllipseItem(point.x() - self._point_radius, point.y() - self._point_radius,
                                                  self._point_radius * 2, self._point_radius * 2, self._polygon_item)
            item.setPen(QtGui.QPen(QtCore.Qt.black, line_width, QtCore.Qt.SolidLine))
            item.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.SolidPattern))
            self._point_items.append(item)

    @property
    def polygon(self) -> QtGui.QPolygonF:
        return QtGui.QPolygonF([self.mapToScene(p.toPoint()) for p in self._polygon_item.polygon()])

    @property
    def polygon_item(self):
        return self._polygon_item

    @property
    def pixmap(self) -> QPixmap:
        return self._pixmap_item.pixmap()

    @pixmap.setter
    def pixmap(self, pixmap: QPixmap) -> None:
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self._pixmap_item.setPixmap(pixmap)

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().paintEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self._selected_point_index = None
        self.polygonChanged.emit(self.polygon)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        sp = self.mapToScene(event.position().toPoint())
        lp = self._pixmap_item.mapFromScene(sp)

        for i, point in enumerate(self._point_items):
            if point.contains(lp):
                self._selected_point_index = i
                return

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self._selected_point_index is None:
            return

        sp = self.mapToScene(event.position().toPoint())
        lp = self._pixmap_item.mapFromScene(sp)

        selected_point = self._point_items[self._selected_point_index]

        poly = self._polygon_item.polygon()
        poly[self._selected_point_index] = lp
        self._polygon_item.setPolygon(poly)

        selected_point.setRect(lp.x() - self._point_radius, lp.y() - self._point_radius,
                               self._point_radius * 2, self._point_radius * 2)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Polygon Editor")
    window.resize(800, 600)
    window.setCentralWidget(PolygonDrawer(window))
    window.show()
    app.exec()
