from PySide6 import QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWizardPage, QVBoxLayout

from social_distance.util import cv_to_qimage
from social_distance.widgets.square_picker import SquarePickerWidget


class SquareEditPage(QWizardPage):
    def __init__(self, parent):
        super(SquareEditPage, self).__init__(parent)
        self.parent = parent

        self.setTitle("Calibrate camera")
        self.setSubTitle("Select a calibration pattern")

        self.square_drawer = SquarePickerWidget(self)
        self.square_drawer.data_changed.connect(self.square_changed)
        layout = QVBoxLayout()
        layout.addWidget(self.square_drawer, stretch=1)
        self.setLayout(layout)

    def initializePage(self) -> None:
        q_image = cv_to_qimage(self.parent.frame)
        self.square_drawer.init(q_image)

    @Slot(QtGui.QPolygonF)
    def square_changed(self, polygon):
        self.parent.square = polygon


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    page = SquareEditPage(app)
    page.show()
    sys.exit(app.exec())