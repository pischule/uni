from PySide6.QtWidgets import QWizardPage, QVBoxLayout

from social_distance.util import *
from social_distance.widgets.polygon_drawer import PolygonDrawerWidget


class RoiPage(QWizardPage):
    def __init__(self, parent):
        super(RoiPage, self).__init__(parent)
        self.parent = parent
        self.setTitle("ROI")
        self.setSubTitle("Select ROI")

        layout = QVBoxLayout()

        self.polygon_drawer = PolygonDrawerWidget(self)
        self.polygon_drawer.data_changed.connect(self.polygon_changed)
        layout.addWidget(self.polygon_drawer, stretch=1)
        self.setLayout(layout)

    def initializePage(self) -> None:
        qimage = cv_to_qimage(self.parent.frame)
        self.polygon_drawer.init(qimage)

    def polygon_changed(self, polygon):
        self.parent.roi = polygon
        self.completeChanged.emit()

    def isComplete(self):
        return self.parent.roi is not None and len(self.parent.roi) >= 3
