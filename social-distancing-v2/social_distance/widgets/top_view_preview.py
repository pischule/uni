import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget

from social_distance.generated_ui.top_view_preview import Ui_Form
from social_distance.util import cv_to_qimage

import cv2 as cv
import numpy as np


class TopViewPreview(QWidget, Ui_Form):
    def __init__(self, frame: np.ndarray, source_square: np.ndarray, parent=None):
        super(TopViewPreview, self).__init__()
        self.setupUi(self)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(cv_to_qimage(frame)))
        self.scene.addItem(self.pixmap_item)
        self.graphicsView.setScene(self.scene)

        self.image = frame
        self.source_square = source_square

        self.square_size = self.scaleSlider.value()
        self.x = self.horizontalSlider.value()
        self.y = self.verticalSlider.value()

        self.transform_matrix = np.ones((3, 3), dtype=np.float32)
        self.update_view()

        self.horizontalSlider.valueChanged.connect(self.update_x)
        self.verticalSlider.valueChanged.connect(self.update_y)
        self.scaleSlider.valueChanged.connect(self.update_scale)

    def update_view(self):
        dest_square = np.asarray([
            [self.x, self.y],
            [self.x + self.square_size, self.y],
            [self.x + self.square_size, self.y + self.square_size],
            [self.x, self.y + self.square_size]
        ], dtype=np.float32)
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
        transformed = cv.warpPerspective(self.image, self.transform_matrix, (1000, 1000))
        self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(cv_to_qimage(transformed)))
        self.graphicsView.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().paintEvent(event)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        print(repr(self.transform_matrix))



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    source_square = np.asarray([(519.0, 235.0), (672.5, 232.0), (695.0, 385.5), (510.5, 388.5)],
                               dtype=np.float32)
    frame = cv.imread('/Users/maksim/Projects/SocialDistance/SocialDistance/social_distance/core/vid1.jpg')
    w = TopViewPreview(frame, source_square)
    w.show()
    sys.exit(app.exec())
