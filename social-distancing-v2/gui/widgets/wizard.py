import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import Slot, QPointF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QDoubleSpinBox, QGridLayout

from gui.util import *
from gui.widgets.drawers import SquareDrawer, ImageView, PolygonDrawer
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.display.frame_scaler import FrameScaler


class CamaraUrlPage(QWizardPage):
    def __init__(self, parent=None):
        super(CamaraUrlPage, self).__init__(parent)

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
        self.registerField("frame", self)
        self._scaler = FrameScaler(new_size=(1280, 720))

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

        self._frame = self._scaler.map(FrameContext.from_frame(self._frame, list())).frame

        qt_image = cv_to_qimage(self._frame)
        self._preview_view.pixmap = QPixmap.fromImage(qt_image)
        self.update()
        self.setField("preview", self._preview_view.pixmap)
        self.setField("frame", self._frame)
        self._is_complete = True
        self.completeChanged.emit()

    def get_frame(self):
        return self._frame

    def isComplete(self):
        return self._is_complete


class SquareEditPage(QWizardPage):
    def __init__(self, parent=None):
        super(SquareEditPage, self).__init__(parent)
        self.setTitle("Calibrate camera")
        self.setSubTitle("Select a calibration pattern")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Calibration pattern:"))
        self._frame = None
        self._square_drawer = SquareDrawer(self, point_radius=5, line_width=1)
        self._square_drawer.polygonChanged.connect(self.polygon_changed)
        layout.addWidget(self._square_drawer)

        self.setLayout(layout)
        self.registerField("square_polygon", self._square_drawer)

    def initializePage(self) -> None:
        preview: QPixmap = self.field("preview")
        self._square_drawer.pixmap = preview
        self.setField("square_polygon", self._square_drawer.polygon)

    @Slot(QtGui.QPolygonF)
    def polygon_changed(self, polygon):
        self.setField("square_polygon", polygon)


class DetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DetailsPage, self).__init__(parent)
        self.setTitle("Square side length")
        self.setSubTitle("Input square side length")

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Square side length:"), 0, 0)

        self._length_edit = QDoubleSpinBox()
        self._length_edit.setRange(0.1, 100)
        self._length_edit.setSingleStep(0.1)
        self._length_edit.setValue(1)
        self._length_edit.setSuffix(" m")

        layout.addWidget(self._length_edit, 0, 1)

        layout.addWidget(QLabel("Camera name:"), 1, 0)

        self._camera_name_edit = QLineEdit()
        self._camera_name_edit.setText(self.field("address"))

        layout.addWidget(self._camera_name_edit, 1, 1)

        self.setLayout(layout)
        self.registerField("square_length", self._length_edit, "value", "valueChanged")
        self.registerField("camera_name", self._camera_name_edit)

    def initializePage(self) -> None:
        self._camera_name_edit.setText(self.field("address"))


class RoiPage(QWizardPage):
    def __init__(self, parent=None):
        super(RoiPage, self).__init__(parent)
        self.setTitle("ROI")
        self.setSubTitle("Select ROI")

        layout = QVBoxLayout()

        self._roi_edit = PolygonDrawer(self, line_width=1)
        self._roi_edit.polygonChanged.connect(self.polygon_changed)
        layout.addWidget(self._roi_edit)

        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._reset_button_clicked)
        layout.addWidget(self._reset_button)

        self.setLayout(layout)

        self.registerField("roi_polygon", self._roi_edit)

    def _reset_button_clicked(self):
        self._roi_edit.reset()

    def initializePage(self) -> None:
        pixmap: QPixmap = self.field("preview")
        self._roi_edit.pixmap = pixmap
        self._roi_edit.polygon = QPolygonF(
            [
                QPointF(0, 0),
                QPointF(pixmap.width(), 0),
                QPointF(pixmap.width(), pixmap.height()),
                QPointF(0, pixmap.height()),
            ]
        )

        self.setField("roi_polygon", self._roi_edit.polygon)


    @Slot(QtGui.QPolygonF)
    def polygon_changed(self, polygon):
        self.setField("roi_polygon", polygon)


class PreviewSettingsPage(QWizardPage):
    def __init__(self, parent=None):
        super(PreviewSettingsPage, self).__init__(parent)
        self.setTitle("Preview settings")
        self.setSubTitle("Select preview settings")

        layout = QGridLayout()

        layout.addWidget(QLabel("Scale:"), 0, 0)
        self._scale_edit = QDoubleSpinBox()
        self._scale_edit.setRange(0.1, 1000)
        self._scale_edit.setSingleStep(20)
        self._scale_edit.setValue(100)
        self._scale_edit.valueChanged.connect(lambda v: self._update_preview())

        layout.addWidget(self._scale_edit, 0, 1)

        layout.addWidget(QLabel("X offset:"), 1, 0)
        self._x_offset_edit = QDoubleSpinBox()
        self._x_offset_edit.setRange(-1000, 1000)
        self._x_offset_edit.setSingleStep(100)
        self._x_offset_edit.setValue(0)
        self._x_offset_edit.valueChanged.connect(lambda v: self._update_preview())

        layout.addWidget(self._x_offset_edit, 1, 1)

        layout.addWidget(QLabel("Y offset:"), 2, 0)
        self._y_offset_edit = QDoubleSpinBox()
        self._y_offset_edit.setRange(-1000, 1000)
        self._y_offset_edit.setSingleStep(100)
        self._y_offset_edit.setValue(0)
        self._y_offset_edit.valueChanged.connect(lambda v: self._update_preview())

        layout.addWidget(self._y_offset_edit, 2, 1)
        self._preview = ImageView(self)
        layout.addWidget(self._preview, 3, 0, 1, 2)

        self.setLayout(layout)

        self.registerField("preview_transform", self)

    def initializePage(self) -> None:
        self._update_preview()

    def _update_preview(self):
        self._preview.pixmap = self.field("preview")

        # q_input_square: QPolygonF = self.field("square_polygon")
        s = self._scale_edit.value()
        x = self._x_offset_edit.value()
        y = self._y_offset_edit.value()
        print("s:", s, "x:", x, "y:", y)
        output_square = np.asarray(
            [
                (x, y),
                (x, y + s),
                (x + s, y + s),
                (x + s, y),
            ], dtype=np.float32
        )
        square_pts = np.asarray(qpolygonf_to_list(self.field("square_polygon")), np.float32)
        m = cv2.getPerspectiveTransform(square_pts, output_square)
        self.setField("preview_transform", m)
        warped = cv2.warpPerspective(
            self.field("frame"),
            m,
            (500, 500),

        )
        q_image = cv_to_qimage(warped)
        self._preview.pixmap = QPixmap.fromImage(q_image)


class CameraAddWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.addPage(CamaraUrlPage(self))
        self.addPage(SquareEditPage(self))
        # self.addPage(PreviewSettingsPage(self))
        self.addPage(RoiPage(self))
        self.addPage(DetailsPage(self))

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
    camera_name = demo.field("camera_name")
    square_length = demo.field("square_length")
    square_polygon = demo.field("square_polygon")
    roi_polygon = demo.field("roi_polygon")
    preview_transform = demo.field("preview_transform")

    print('address:', address)
    print('camera_name:', camera_name)
    print('square_length:', square_length)
    print('square_polygon:', square_polygon)
    print('roi_polygon:', roi_polygon)
    print('preview_transform:', preview_transform)
