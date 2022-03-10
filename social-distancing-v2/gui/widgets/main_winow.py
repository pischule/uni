from typing import Optional

import PySide6
from PySide6.QtCore import QThread, Slot, Signal
from PySide6.QtGui import QImage, QPixmap, Qt

from gui.ui.main_window import Ui_MainWindow
from gui.widgets.add_camera_dialog import AddCameraDialog
from PySide6.QtWidgets import QMainWindow, QApplication
import sys

import cv2


class CameraThread(QThread):
    changePixmap = Signal(QImage)

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...):
        super().__init__(parent)
        self.continue_loop = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.continue_loop:
            ret, frame = cap.read()
            if ret:
                p = self.convertToQImage(frame)
                self.changePixmap.emit(p)

    def convertToQImage(self, frame) -> QImage:
        # https://stackoverflow.com/a/55468544/6622587
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        return convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

    def quit(self) -> None:
        self.continue_loop = False
        super().quit()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Main Window')
        self.setupUi(self)

        self.addCameraButton.clicked.connect(self.add_camera)
        self.detectionEnabledCheckBox.stateChanged.connect(self.toggle_detection())

        self.camThread = CameraThread(self)
        self.camThread.changePixmap.connect(self.set_image)
        self.camThread.start()

    def add_camera(self):
        print('add camera')
        dlg = AddCameraDialog()
        dlg.exec()

    @Slot(QImage)
    def set_image(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def toggle_detection(self):
        print('toggle detection')
        if self.detectionEnabledCheckBox.isChecked():
            print('detection enabled')
        else:
            print('detection disabled')

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.camThread.quit()
        self.camThread.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
