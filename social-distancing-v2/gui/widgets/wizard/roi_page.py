from PySide6 import QtGui
from PySide6.QtCore import Slot, QPointF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QPushButton

from gui.util import *
from gui.widgets.drawers import PolygonDrawer


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
