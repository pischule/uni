from PySide6 import QtGui, QtCore
from PySide6 import QtWidgets
from PySide6.QtGui import Qt, QPixmap


class SquareDrawer(QtWidgets.QLabel):
    def __init__(self, image: QPixmap):
        super().__init__()
        self.image = image

        self.points = [
            [100, 100],
            [200, 100],
            [200, 200],
            [100, 200]
        ]
        self.pointRadius = 7

        self.pointPen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1)
        self.pointBrush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 127))

        self.polygonPen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1)
        self.polygonBrush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 50))

        self.setPixmap(self.image)
        self.setMouseTracking(True)
        self.movingPoint = None

        self.draw_points()

    def draw_points(self):
        canvas = self.image.copy()
        painter = QtGui.QPainter(canvas)

        painter.setPen(self.polygonPen)
        painter.setBrush(self.polygonBrush)
        painter.drawPolygon([QtCore.QPoint(x, y) for x, y in self.points])

        painter.setPen(self.pointPen)
        painter.setBrush(self.pointBrush)
        for point in self.points:
            painter.drawEllipse(point[0] - self.pointRadius, point[1] - self.pointRadius, self.pointRadius * 2,
                                self.pointRadius * 2)

        painter.end()
        self.setPixmap(canvas)


    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.movingPoint is not None:
            position = ev.position()
            self.points[self.movingPoint][0] = position.x()
            self.points[self.movingPoint][1] = position.y()
            self.draw_points()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        position = ev.position()
        for i, point in enumerate(self.points):
            if (position.x() - point[0]) ** 2 + (position.y() - point[1]) ** 2 < self.pointRadius ** 2:
                self.movingPoint = i
                break

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.movingPoint = None


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    canvas = QtGui.QPixmap(600, 400)
    canvas.fill(Qt.white)
    drawer = SquareDrawer(canvas)
    drawer.show()
    sys.exit(app.exec())
