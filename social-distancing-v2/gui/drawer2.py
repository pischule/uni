from PySide6 import QtCore, QtGui, QtWidgets


class PolygonDrawer(QtWidgets.QGraphicsView):
    polygonChanged = QtCore.Signal(QtGui.QPolygonF)

    def __init__(self, parent=None, line_width=2):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap_item)

        self._polygon_item = QtWidgets.QGraphicsPolygonItem(self.pixmap_item)
        self._polygon_item.setPen(QtGui.QPen(QtCore.Qt.black, line_width, QtCore.Qt.SolidLine))
        self._polygon_item.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.VerPattern))

    @property
    def pixmap_item(self):
        return self._pixmap_item

    def setPixmap(self, pixmap):
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.pixmap_item.setPixmap(pixmap)

    def resizeEvent(self, event):
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    @property
    def polygon(self) -> QtGui.QPolygonF:
        return QtGui.QPolygonF([self.mapToScene(p.toPoint()) for p in self._polygon_item.polygon()])

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        sp = self.mapToScene(event.position().toPoint())
        lp = self.pixmap_item.mapFromScene(sp)

        poly = self._polygon_item.polygon()
        poly.append(lp)
        self._polygon_item.setPolygon(poly)
        self.polygonChanged.emit(self.polygon)

    def reset(self):
        self._polygon_item.setPolygon(QtGui.QPolygonF())


class ImageView(QtWidgets.QGraphicsView):
    pixmapChanged = QtCore.Signal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap_item)

    @property
    def pixmap_item(self):
        return self._pixmap_item

    @property
    def polygon_item(self):
        return self._polygon_item

    def setPixmap(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.pixmapChanged.emit(pixmap)

    def resizeEvent(self, event):
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    @property
    def pixmap(self) -> QtGui.QPixmap:
        print('pixmap')
        return self.pixmap_item.pixmap()


class SquareDrawer(QtWidgets.QGraphicsView):
    polygonChanged = QtCore.Signal(QtGui.QPolygonF)

    def __init__(self, parent=None, point_radius: int = 10, line_width: int = 5):
        super().__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap_item)

        self._polygon_item = QtWidgets.QGraphicsPolygonItem([
            QtCore.QPoint(100, 100),
            QtCore.QPoint(100, 400),
            QtCore.QPoint(400, 400),
            QtCore.QPoint(400, 100)
        ], self.pixmap_item)
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
    def pixmap_item(self):
        return self._pixmap_item

    @property
    def polygon_item(self):
        return self._polygon_item

    def setPixmap(self, pixmap):
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.pixmap_item.setPixmap(pixmap)

    def resizeEvent(self, event):
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self._selected_point_index = None
        self.polygonChanged.emit(self.polygon)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        sp = self.mapToScene(event.position().toPoint())
        lp = self.pixmap_item.mapFromScene(sp)

        for i, point in enumerate(self._point_items):
            if point.contains(lp):
                self._selected_point_index = i
                return

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self._selected_point_index is None:
            return

        sp = self.mapToScene(event.position().toPoint())
        lp = self.pixmap_item.mapFromScene(sp)

        selected_point = self._point_items[self._selected_point_index]

        poly = self._polygon_item.polygon()
        poly[self._selected_point_index] = lp
        self._polygon_item.setPolygon(poly)

        selected_point.setRect(lp.x() - self._point_radius, lp.y() - self._point_radius,
                               self._point_radius * 2, self._point_radius * 2)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        view = SquareDrawer()
        self.setCentralWidget(view)

        view.setPixmap(QtGui.QPixmap("img.jpg"))

        self.resize(640, 480)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
