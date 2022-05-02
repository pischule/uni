from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizardPage, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton

from social_distance.util import *
from social_distance.widgets.drawers import ImageDrawer


class CamaraUrlPage(QWizardPage):
    def __init__(self, parent):
        super(CamaraUrlPage, self).__init__(parent)
        self.parent = parent

        self.setTitle("Connect to camera")
        self.setSubTitle("Input camera address")
        self._is_complete = False

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Camera address:"))

        address_layout = QHBoxLayout()
        self._address_edit = QLineEdit()
        self._address_edit.textChanged.connect(self._address_changed)
        address_layout.addWidget(self._address_edit)
        self.registerField("address", self._address_edit)

        self._connect_button = QPushButton("Connect")
        self._connect_button.clicked.connect(self._connect_button_clicked)
        self._connect_button.setEnabled(False)
        address_layout.addWidget(self._connect_button)
        layout.addLayout(address_layout)

        self._preview_view = ImageDrawer(self)
        self._preview_view.setMinimumSize(600, 300)
        layout.addWidget(self._preview_view)

        self.setLayout(layout)

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
        self._preview_view.pixmap = QPixmap.fromImage(qt_image)
        self.update()
        self.parent.frame = self._frame
        self._is_complete = True
        self.completeChanged.emit()

    def get_frame(self):
        return self._frame

    def isComplete(self):
        return self._is_complete
