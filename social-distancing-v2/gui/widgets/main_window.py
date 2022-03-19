import dataclasses
import json
import os
import sys
import time

import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QImage, QPolygon
from PySide6.QtWidgets import QMainWindow, QFileDialog

from gui.camera_model import Camera
from gui.pyui.main_window import Ui_MainWindow
from gui.thread.camera_thread import CameraThread
from gui.widgets.wizard.wizard import CameraAddWizard


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camThread = CameraThread(self)
        self.camThread.changePixmap.connect(self.set_image)
        self.camThread.start()
        self.setupUi(self)

        self._load_cameras()

        self.cameraComboBox.currentIndexChanged.connect(self.switch_camera)
        self.addCameraPushButton.clicked.connect(self.add_camera)

        self.saveDataPushButton.clicked.connect(self.save_data)

        self._scene = QtWidgets.QGraphicsScene(self)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.cameraGraphicsView.setScene(self._scene)

        for k in self._cameras:
            self.cameraComboBox.addItem(k.name)

        self.camThread.update_video_source(self._cameras[0])
        self.cameraComboBox.currentIndexChanged.connect(self.switch_camera)

        self.distanceSpinBox.valueChanged.connect(self.set_distance)
        self.set_distance(self.distanceSpinBox.value())

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def set_image(self, image: QImage):
        pixmap = PySide6.QtGui.QPixmap.fromImage(image)
        self._pixmap_item.setPixmap(pixmap)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def add_camera(self) -> bool:
        dlg = CameraAddWizard(self)
        if not dlg.exec():
            return False
        address = dlg.field("address")
        square_length = dlg.field("square_length")
        square_polygon: QPolygon = dlg.field("square_polygon")
        roi_polygon: QPolygon = dlg.field("roi_polygon")
        camera_name: str = dlg.field("camera_name")

        self._cameras.append(Camera.from_wizard(
            camera_name,
            address,
            float(square_length),
            [p.toTuple() for p in square_polygon.toList()],
            [p.toTuple() for p in roi_polygon.toList()]
        ))
        self.cameraComboBox.addItem(camera_name)
        self.switch_camera(self.cameraComboBox.count() - 1)
        return True

    @QtCore.Slot(int)
    def switch_camera(self, index: int):
        self.camThread.update_video_source(self._cameras[index])

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.camThread.quit()
        self.camThread.wait()

        with open(os.path.join('conf', 'cameras.json'), 'w') as f:
            json.dump([dataclasses.asdict(c) for c in self._cameras], f)

    def set_distance(self, distance: float):
        self.camThread.set_safe_distance(float(distance))

    def _load_cameras(self):
        self._cameras = []
        try:
            with open(os.path.join('conf', 'cameras.json'), 'r') as f:
                self._cameras = [Camera(**c) for c in json.load(f)]
        except FileNotFoundError:
            pass
        if not self._cameras:
            if not self.add_camera():
                self.camThread.quit()
                self.camThread.wait()
                sys.exit(1)

    def save_data(self):
        data = json.dumps(self.camThread.data)
        if not data:
            return
        fname = f"{'_'.join(self.cameraComboBox.currentText().split())}-{int(time.time())}.json"
        QFileDialog.saveFileContent(bytes(data, 'utf-8'), fname)
