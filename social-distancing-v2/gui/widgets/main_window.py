import sys
from typing import Optional, Union

import PySide6
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication

from gui.ui.main_window import Ui_MainWindow
from gui.widgets.add_camera_dialog import AddCameraDialog
from gui.widgets.camera_thread import CameraThread


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camThread = None
        self.setWindowTitle('Main Window')
        self.setupUi(self)

        self.addCameraButton.clicked.connect(self.add_camera)
        self.detectionEnabledCheckBox.stateChanged.connect(self.toggle_detection())

        self.cameras = [
            ('webcam', 0),
            ('people_walking.mp4', 'people_walking.mp4'),
        ]
        for k, v in self.cameras:
            self.camerasComboBox.addItem(k)

        self.camerasComboBox.currentIndexChanged.connect(self.camera_changed)

        self.init_camera()

    def camera_changed(self, index: int):
        self.terminate_camera()
        self.init_camera(self.cameras[index][1])

    def init_camera(self, source: Optional[Union[str, int]] = 0):
        self.camThread = CameraThread(self, source)
        self.camThread.changePixmap.connect(self.set_image)
        self.camThread.start()
        
    def terminate_camera(self):
        if self.camThread:
            self.camThread.quit()
            self.camThread.wait()
            self.camThread = None

    def add_camera(self):
        print('add camera')
        dlg = AddCameraDialog()
        dlg.exec()

    @Slot(QImage)
    def set_image(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def toggle_detection(self):
        if self.detectionEnabledCheckBox.isChecked():
            print('detection enabled')
        else:
            print('detection disabled')

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.terminate_camera()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
