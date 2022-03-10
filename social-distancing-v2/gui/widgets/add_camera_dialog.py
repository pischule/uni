from PySide6.QtWidgets import QDialog, QWidget

from gui.ui.add_camera_dialog import Ui_AddCameraDialog


class AddCameraDialog(QDialog, Ui_AddCameraDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)