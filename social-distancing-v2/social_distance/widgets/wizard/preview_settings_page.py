import numpy as np
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizardPage, QLabel, QDoubleSpinBox, QGridLayout

from social_distance.util import *
from social_distance.widgets.drawers import ImageDrawer


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
        self._preview = ImageDrawer(self)
        layout.addWidget(self._preview, 3, 0, 1, 2)

        self.setLayout(layout)

        self.registerField("preview_transform", self)

    def initializePage(self) -> None:
        self._update_preview()

    def _update_preview(self):
        self._preview.pixmap = self.field("preview")

        s = self._scale_edit.value()
        x = self._x_offset_edit.value()
        y = self._y_offset_edit.value()
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
