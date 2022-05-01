from PySide6 import QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizardPage, QLabel, QVBoxLayout

from social_distance.widgets.drawers import SquareDrawer


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
