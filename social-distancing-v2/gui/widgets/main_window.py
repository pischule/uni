import sys
from typing import Optional, Union

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QMainWindow, QApplication

from gui.thread.camera_thread import CameraThread
from gui.pyui.main_window import Ui_MainWindow
from gui.wizard import CameraAddWizard


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camThread = CameraThread(self)
        self.camThread.changePixmap.connect(self.set_image)
        self.camThread.start()
        self.setupUi(self)

        # self.addCameraPushButton.clicked.connect(self.add_camera)
        # self.detectionEnabledCheckBox.stateChanged.connect(self.toggle_detection())

        self._cameras = [
            ('webcam', 0),
            ('people_walking.mp4', 'people_walking.mp4'),
        ]

        self._scene = QtWidgets.QGraphicsScene(self)
        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.cameraGraphicsView.setScene(self._scene)

        for k, v in self._cameras:
            self.cameraComboBox.addItem(k)

        self.addCameraPushButton.clicked.connect(self.add_camera)

        self.camThread.update_video_source(self._cameras[0][1])

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def set_image(self, image: QImage):
        pixmap = PySide6.QtGui.QPixmap.fromImage(image)
        self._pixmap_item.setPixmap(pixmap)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def add_camera(self):
        dlg = CameraAddWizard(self)
        if not dlg.exec():
            return
        address = dlg.field("address")
        square_length = dlg.field("square_length")
        square_polygon = dlg.field("square_polygon")
        roi_polygon = dlg.field("roi_polygon")

        print('address:', address)
        print('square_length:', square_length)
        print('square_polygon:', square_polygon)
        print('roi_polygon:', roi_polygon)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.camThread.quit()
        self.camThread.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
