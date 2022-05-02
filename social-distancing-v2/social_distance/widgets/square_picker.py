from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication


class SquarePickerWidget(QtWidgets.QLabel):
    def __init__(self, image, parent=None, points=None, circle_radius=0.02):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)

        self.points = points or [
            QtCore.QPointF(0.3, 0.3),
            QtCore.QPointF(0.7, 0.3),
            QtCore.QPointF(0.7, 0.7),
            QtCore.QPointF(0.3, 0.7),
        ]

        self.setMouseTracking(True)
        self.circle_radius = circle_radius
        self.moving_index = -1
        self.thickness = 1
        self.image = image
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
        relative_position = self.widget_pos_to_image_relative_pos(event.position())
        self.moving_index = self.get_clicked_point(relative_position)
        # change cursor
        if self.moving_index >= 0:
            self.setCursor(QtCore.Qt.ClosedHandCursor)

        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        relative_position =  self.widget_pos_to_image_relative_pos(event.position())
        self.move_point(relative_position)

        if self.moving_index == -1:
            if self.get_clicked_point(relative_position) != -1:
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        relative_position = self.widget_pos_to_image_relative_pos(event.position())
        self.move_point(relative_position)
        self.moving_index = -1
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def move_point(self, new_pos):
        if self.moving_index == -1:
            return
        self.points[self.moving_index] = new_pos
        self.update()

    def get_clicked_point(self, cursor_pos):
        for i, point in enumerate(self.points):
            if (point - cursor_pos).manhattanLength() < self.circle_radius:
                return i
        return -1

    def widget_pos_to_image_relative_pos(self, widget_pos):
        return QPointF(widget_pos.x() / self.scaled_image_size.width(), widget_pos.y() / self.scaled_image_size.height())

    def image_relative_pos_to_widget_pos(self, image_pos):
        return QPointF(self.scaled_image_size.width() * image_pos.x(), self.scaled_image_size.height() * image_pos.y())

    def image_relative_to_absolute_pos(self, image_pos):
        image_size = self.image.size()
        return QPointF(image_pos.x() * image_size.width(), image_pos.y() * image_size.height())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        q_points = [self.image_relative_to_absolute_pos(p) for p in self.points]
        print(repr(list(map(lambda p: p.toTuple(), q_points))))


if __name__ == "__main__":
    import sys

    image = QImage('/Users/maksim/Projects/SocialDistance/SocialDistance/data/video/first_frame.jpg')

    app = QApplication(sys.argv)
    window = SquarePickerWidget(image=image)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
