from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication


class PolygonDrawerWidget(QtWidgets.QLabel):
    def __init__(self, image: QImage, parent=None, points=None, point_radius=0.02):
        super().__init__()
        self.points = points or []

        self.setMouseTracking(True)
        self.thickness = 1
        self.image = image
        self.point_radius = point_radius
        self.moving_index = -1
        self.scaled_image_size = self.image.size()

        self.show()

    def paintEvent(self, event):
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
        relative_pos = self.widget_pos_to_image_relative_pos(event.position())
        self.moving_index = self.get_clicked_point(relative_pos)
        if self.moving_index >= 0:
            self.setCursor(QtCore.Qt.ClosedHandCursor)
        else:
            self.points.append(relative_pos)
            self.update()

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        self.moving_index = -1
        if ev.key() == Qt.Key_Delete or ev.key() == Qt.Key_Backspace:
            if self.points:
                self.points.pop()
                self.update()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.moving_index = -1

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
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


if __name__ == "__main__":
    import sys

    image = QImage('/Users/maksim/Projects/SocialDistance/SocialDistance/data/video/first_frame.jpg')

    app = QApplication(sys.argv)
    window = PolygonDrawerWidget(image=image, parent=app)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
