from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication


class PolygonDrawerWidget(QtWidgets.QLabel):
    data_changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

        self.setMouseTracking(True)
        self.thickness = 1
        self.image = None
        self.point_radius = 0.02
        self.moving_index = -1
        self.scaled_image_size = QPointF(1, 1)

        self.show()

    def init(self, image: QImage):
        self.image = image
        self.points = []
        self.data_changed.emit([p.toTuple() for p in self.get_absolute_points()])
        self.update()

    def paintEvent(self, event):
        if self.image is None:
            return
        qp = QtGui.QPainter(self)
        scaled_image = self.image.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.scaled_image_size = scaled_image.size()
        qp.drawImage(0, 0, scaled_image)
        pn = QtGui.QPen(Qt.black, self.thickness)
        br = QtGui.QBrush(QtGui.QColor(255, 255, 0, 80))
        qp.setPen(pn)
        qp.setBrush(br)
        qp.drawPolygon([self.image_relative_pos_to_widget_pos(p) for p in self.points])

    def mousePressEvent(self, event):
        if self.image is None:
            return
        relative_pos = self.widget_pos_to_image_relative_pos(event.position())
        self.moving_index = self.get_clicked_point(relative_pos)
        if event.button() == Qt.RightButton:
            if len(self.points) > 0:
                self.points.pop()
                self.update()
            else:
                return
        else:
            if self.moving_index >= 0:
                self.setCursor(QtCore.Qt.ClosedHandCursor)
            else:
                self.points.append(relative_pos)
                self.update()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.moving_index = -1
        self.data_changed.emit([p.toTuple() for p in self.get_absolute_points()])

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.image is None:
            return
        relative_pos = self.widget_pos_to_image_relative_pos(ev.position())
        if self.moving_index >= 0:
            self.points[self.moving_index] = relative_pos
            self.update()
        else:
            if self.get_clicked_point(relative_pos) != -1:
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)

    def widget_pos_to_image_relative_pos(self, widget_pos):
        return QPointF(widget_pos.x() / self.scaled_image_size.width(), widget_pos.y() / self.scaled_image_size.height())

    def image_relative_pos_to_widget_pos(self, image_pos):
        return QPointF(self.scaled_image_size.width() * image_pos.x(), self.scaled_image_size.height() * image_pos.y())

    def image_relative_to_absolute_pos(self, image_pos):
        image_size = self.image.size()
        return QPointF(image_pos.x() * image_size.width(), image_pos.y() * image_size.height())

    def get_clicked_point(self, cursor_pos):
        for i, point in enumerate(self.points):
            if (point - cursor_pos).manhattanLength() < self.point_radius:
                return i
        return -1

    def get_absolute_points(self):
        return [self.image_relative_to_absolute_pos(p) for p in self.points]


if __name__ == "__main__":
    import sys

    image = QImage('/Users/maksim/Projects/SocialDistance/SocialDistance/data/video/first_frame.jpg')

    app = QApplication(sys.argv)
    window = PolygonDrawerWidget()
    window.init(image)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
