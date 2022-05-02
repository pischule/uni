import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget

from social_distance.generated_ui.top_view_preview import Ui_Form
from social_distance.util import cv_to_qimage

import cv2 as cv
import numpy as np


class TopViewPreview(QWidget, Ui_Form):
    data_changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.graphicsView.setScene(self.scene)

        self.image = None
        self.source_square = None

        self.square_size = self.scaleSlider.value()
        self.x = self.horizontalSlider.value()
        self.y = self.verticalSlider.value()

        self.transform_matrix = np.ones((3, 3), dtype=np.float32)
        self.update_view()

        self.horizontalSlider.valueChanged.connect(self.update_x)
        self.verticalSlider.valueChanged.connect(self.update_y)
        self.scaleSlider.valueChanged.connect(self.update_scale)

    def init(self, frame: np.ndarray, source_square: list):
        self.image = frame
        self.source_square = np.asarray(source_square, dtype=np.float32)
        self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(cv_to_qimage(frame)))
        self.update_view()

    def update_view(self):
        if self.source_square is None or self.image is None:
            return
        dest_square = np.asarray([
            [self.x, self.y],
            [self.x + self.square_size, self.y],
            [self.x + self.square_size, self.y + self.square_size],
            [self.x, self.y + self.square_size]
        ], dtype=np.float32)
        self.data_changed.emit(dest_square.tolist())
        self.transform_matrix = cv.getPerspectiveTransform(self.source_square, dest_square)
        self.update()

    def update_x(self, x):
        self.x = x
        self.update_view()

    def update_y(self, y):
        self.y = y
        self.update_view()

    def update_scale(self, scale):
        self.square_size = scale
        self.update_view()

    def paintEvent(self, event):
        if self.image is None or self.source_square is None:
            return
        transformed = cv.warpPerspective(self.image, self.transform_matrix, (1000, 1000))
        self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(cv_to_qimage(transformed)))
        self.graphicsView.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().paintEvent(event)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    source_square = [(265.0, 461.0), (427.5, 459.5), (399.5, 628.0), (208.5, 633.0)]
    frame = cv.imread('/Users/maksim/Projects/SocialDistance/SocialDistance/social_distance/core/vid1.jpg')
    w = TopViewPreview()
    w.init(frame, source_square)
    w.show()
    sys.exit(app.exec())
