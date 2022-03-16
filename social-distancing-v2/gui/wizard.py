from PySide6 import QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, \
    QDoubleSpinBox
from gui.opencv_util import *
from gui.drawer2 import SquareDrawer, ImageView, PolygonDrawer


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

        self._preview_view = ImageView(self)
        self._preview_view.setMinimumSize(600, 300)
        layout.addWidget(self._preview_view)

        self.setLayout(layout)

        self.registerField("address", self._address_edit)
        self.registerField("preview", self._preview_view)

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
        self._preview_view.setPixmap(QPixmap.fromImage(qt_image))
        self._preview_view.resize(600, 300)
        self.update()
        self.setField("preview", self._preview_view.pixmap)
        self._is_complete = True
        self.completeChanged.emit()

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
        self._square_drawer = SquareDrawer(self, point_radius=10, line_width=2)
        self._square_drawer.polygonChanged.connect(self.polygon_changed)
        layout.addWidget(self._square_drawer)

        self.setLayout(layout)
        self.registerField("square_polygon", self._square_drawer)
        self.setField("square_polygon", self._square_drawer.polygon)

    def initializePage(self) -> None:
        preview: QPixmap = self.field("preview")
        self._square_drawer.setPixmap(preview)

    @Slot(QtGui.QPolygonF)
    def polygon_changed(self, polygon):
        self.setField("square_polygon", polygon)


class Page3(QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.setTitle("Square side length")
        self.setSubTitle("Input square side length")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Square side length:"))

        self._length_edit = QDoubleSpinBox()
        self._length_edit.setRange(0.1, 100)
        self._length_edit.setSingleStep(0.1)
        self._length_edit.setValue(1)
        self._length_edit.setSuffix(" m")

        layout.addWidget(self._length_edit)

        self.setLayout(layout)
        self.registerField("square_length", self._length_edit, "value", "valueChanged")


class Page4(QWizardPage):
    def __init__(self, parent=None):
        super(Page4, self).__init__(parent)
        self.setTitle("ROI")
        self.setSubTitle("Select ROI")

        layout = QVBoxLayout()

        self._roi_edit = PolygonDrawer(self, line_width=2)
        self._roi_edit.polygonChanged.connect(self.polygon_changed)
        layout.addWidget(self._roi_edit)

        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._reset_button_clicked)
        layout.addWidget(self._reset_button)

        self.setLayout(layout)

        self.registerField("roi_polygon", self._roi_edit)
        self.setField("roi_polygon", self._roi_edit.polygon)

    def _reset_button_clicked(self):
        self._roi_edit.reset()

    def initializePage(self) -> None:
        self._roi_edit.setPixmap(self.field("preview"))

    @Slot(QtGui.QPolygonF)
    def polygon_changed(self, polygon):
        self.setField("roi_polygon", polygon)


class CameraAddWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.addPage(Page3(self))
        self.addPage(Page4(self))

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("Add a new camera")




if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    demo = CameraAddWizard()
    demo.show()
    app.exec()

    address = demo.field("address")
    square_length = demo.field("square_length")
    square_polygon = demo.field("square_polygon")
    roi_polygon = demo.field("roi_polygon")

    print('address:', address)
    print('square_length:', square_length)
    print('square_polygon:', square_polygon)
    print('roi_polygon:', roi_polygon)

    sys.exit(0)
