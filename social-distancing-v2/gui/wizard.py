from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton

from gui.opencv_util import *
from gui.drawer2 import SquareDrawer


class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)

        self.setTitle("Connect to camera")
        self.setSubTitle("Input camera address")
        self._is_complete = False

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Camera address:"))

        address_layout = QHBoxLayout()
        self._address_edit = QLineEdit()
        self._address_edit.textChanged.connect(self._address_changed)
        address_layout.addWidget(self._address_edit)

        self._connect_button = QPushButton("Connect")
        self._connect_button.clicked.connect(self._connect_button_clicked)
        self._connect_button.setEnabled(False)
        address_layout.addWidget(self._connect_button)
        layout.addLayout(address_layout)

        self._preview_label = QLabel()
        self._preview_label.setFixedSize(800, 400)
        self._preview_label.setAlignment(Qt.AlignCenter)
        self._frame = None
        layout.addWidget(self._preview_label)

        self.setLayout(layout)

        self.registerField("address", self._address_edit)
        self.registerField("frame", self)

    def _address_changed(self, text):
        self._connect_button.setEnabled(len(text) > 0)
        self._is_complete = False
        self.completeChanged.emit()
        self._address_edit.setStyleSheet("")

    def _connect_button_clicked(self):
        self._frame = get_frame(self._address_edit.text())
        if self._frame is None:
            self._address_edit.setStyleSheet("background-color: red")
            return

        qt_image = cv_to_qimage(self._frame)
        qt_image = qt_image.scaled(self._preview_label.size(), Qt.KeepAspectRatio)
        self._preview_label.setPixmap(QPixmap.fromImage(qt_image))
        self._is_complete = True
        self.completeChanged.emit()
        self.setField("frame", self._frame)

    def get_frame(self):
        return self._frame

    def isComplete(self):
        return self._is_complete


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle("Calibrate camera")
        self.setSubTitle("Select a calibration pattern")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Calibration pattern:"))
        self._frame = None
        self._square_drawer = SquareDrawer(self, point_radius=10)
        layout.addWidget(self._square_drawer)

        self.setLayout(layout)

    def initializePage(self) -> None:
        qt_image = cv_to_qimage(self.field("frame"))
        pixmap = QPixmap.fromImage(qt_image)
        self._square_drawer.setPixmap(pixmap)

    def _points_updated(self, points):
        print(self._square_drawer.getPoints())


class Page3(QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.setTitle("Calibrate camera")
        self.setSubTitle("Set square size")


class Demo(QWizard):
    def __init__(self):
        super().__init__()

        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.addPage(Page3(self))

        self.setWindowTitle("Add a new camera")

        self.setWizardStyle(QWizard.ModernStyle)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec())
