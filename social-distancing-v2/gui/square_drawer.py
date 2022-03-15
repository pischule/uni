import math

from PySide6 import QtGui, QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF
from PySide6.QtGui import Qt, QPixmap, QPolygonF

from lib.mappers.util.custom_types import Point


class SquareDrawer(QtWidgets.QLabel):
    def heightForWidth(self, arg__1: int) -> int:
        return arg__1

    # pointsUpdated = QtCore.Signal(bool)
    #
    # def __init__(self, image: QPixmap,
    #              point_radius: int = 7,
    #              point_color: QtGui.QColor = Qt.red,
    #              area_color: QtGui.QColor = Qt.green,
    #              line_color: QtGui.QColor = Qt.black,
    #              min_size: Point = (800, 600),
    #              ):
    #     super().__init__()
    #
    #     self._original_image = image
    #     self._moving_point = None
    #
    #     self._points = [QPointF(0, 0), QPointF(0, 0), QPointF(0, 0), QPointF(0, 0)]
    #
    #     self.setSizePolicy(
    #         QtWidgets.QSizePolicy.MinimumExpanding,
    #         QtWidgets.QSizePolicy.MinimumExpanding
    #     )
    #
    #     self._point_radius = point_radius
    #     self._line_pen = QtGui.QPen(line_color)
    #     self._point_brush = QtGui.QBrush(point_color)
    #
    #     self._polygon_brush = QtGui.QBrush(area_color)
    #
    # def heightForWidth(self, width: int) -> int:
    #     return 100
    #
    # def original_image_points(self):
    #     width = float(self._original_image.width())
    #     height = float(self._original_image.height())
    #     return [
    #         [int(point.x() * width), int(point.y() * height)]
    #         for point in self._points
    #     ]
    #
    # def pixmap_points(self):
    #     width = float(self.width())
    #     height = float(self.height())
    #
    #     return [
    #         [int(point.x() * width), int(point.y() * height)]
    #         for point in self._points
    #     ]
    #
    # def paintEvent(self, e: QtGui.QPaintEvent) -> None:
    #     painter = QtGui.QPainter(self)
    #     scaled_image = self._original_image.scaled(self.size(), Qt.KeepAspectRatio)
    #     painter.drawPixmap(0, 0, scaled_image)
    #
    #     points = self.pixmap_points()
    #
    #     painter.setPen(self._line_pen)
    #     painter.setBrush(self._polygon_brush)
    #     painter.drawPolygon([QtCore.QPoint(x, y) for x, y in points])
    #
    #     for i, point in enumerate(points):
    #         painter.setPen(self._line_pen)
    #         painter.setBrush(self._point_brush)
    #         radius = self._point_radius
    #
    #         painter.drawEllipse(point[0] - self._point_radius,
    #                             point[1] - self._point_radius,
    #                             radius * 2,
    #                             radius * 2)
    #     painter.end()
    #
    # def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if self._moving_point is not None:
    #         position = event.position()
    #         self._points[self._moving_point] = QPointF(position.x(), position.y())
    #         self.update()
    #
    # def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
    #     position = ev.position()
    #     points = self.pixmap_points()
    #     for i, point in enumerate(points):
    #         if math.hypot(position.x() - point[0], position.y() - point[1]) < self._point_radius + 2:
    #             self._moving_point = i
    #             return
    #
    # def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
    #     self._moving_point = None
    #     self.pointsUpdated.emit(True)
    #     self.update()
    #
    # def getPoints(self) -> list[list[int]]:
    #     return self._points
    #
    # def setImage(self, image: QPixmap):
    #     self._original_image = image
    #     self.update()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    canvas = QtGui.QPixmap(600, 400)
    canvas.fill(Qt.white)

    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setCentralWidget(SquareDrawer(canvas))
    mainWindow.setVisible(True)

    sys.exit(app.exec())
