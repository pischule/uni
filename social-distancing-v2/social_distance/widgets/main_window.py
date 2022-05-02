import dataclasses
import json
import os
import sys
import time
from typing import Dict

import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QImage, QPolygon
from PySide6.QtWidgets import QMainWindow, QFileDialog

from social_distance.core.camera_model import Camera
from social_distance.generated_ui.main_window import Ui_MainWindow
from social_distance.thread.camera_thread import CameraThread
from social_distance.widgets.wizard.wizard import CameraAddWizard
from social_distance.core.processing import NETWORK_NAMES


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.camera_thread = CameraThread(self)
        self.camera_thread.pixmap_changed.connect(self.set_image)
        self.camera_thread.start()

        self.load_config()

        self.cameraComboBox.currentIndexChanged.connect(self.switch_camera)
        self.addCameraPushButton.clicked.connect(self.add_camera)
        self.saveDataPushButton.clicked.connect(self.save_data)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.cameraGraphicsView.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.cameraGraphicsView.setScene(self.scene)

        self.camera_thread.set_camera(self._cameras[0])
        self.cameraComboBox.currentIndexChanged.connect(self.switch_camera)

        self.distanceSpinBox.valueChanged.connect(self.set_distance)
        self.set_distance(self.distanceSpinBox.value())
        self.camera_thread.data_changed.connect(self.set_stats_label)

        self.modelComboBox.currentIndexChanged.connect(self.camera_thread.set_model)
        self.modelComboBox.addItems(NETWORK_NAMES)

        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        super().paintEvent(event)
        self.cameraGraphicsView.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)

    def set_image(self, image: QImage):
        pixmap = PySide6.QtGui.QPixmap.fromImage(image)
        self.pixmap_item.setPixmap(pixmap)
        self.cameraGraphicsView.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)

    def add_camera(self) -> bool:
        dlg = CameraAddWizard(self)
        if not dlg.exec():
            return False

        address = dlg.field("address")
        camera_name: str = dlg.field("camera_name")
        side_length = dlg.field("side_length")
        roi = dlg.roi
        square = dlg.square
        preview_square = dlg.preview_square

        camera = Camera(
            name=camera_name,
            address=address,
            side_length=side_length,
            roi=roi,
            square=square,
            preview_square=preview_square
        )

        self._cameras.append(camera)
        self.cameraComboBox.addItem(camera_name)
        return True

    def switch_camera(self, index: int):
        self.camera_thread.set_camera(self._cameras[index])

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.camera_thread.quit()
        self.camera_thread.wait()

        with open(os.path.join('data', 'conf.json'), 'w') as f:
            json.dump([dataclasses.asdict(c) for c in self._cameras], f, indent=2, sort_keys=True)

    def set_distance(self, distance: float):
        self.camera_thread.set_safe_distance(float(distance))
        pass

    def load_config(self):
        self._cameras = []
        try:
            with open(os.path.join('data', 'conf.json'), 'r') as f:
                self._cameras = [Camera(**c) for c in json.load(f)]
        except FileNotFoundError:
            pass
        if not self._cameras:
            if not self.add_camera():
                self.camera_thread.quit()
                self.camera_thread.wait()
                sys.exit(1)

        for k in self._cameras:
            self.cameraComboBox.addItem(k.name)

    def save_data(self):
        data = json.dumps(self.camera_thread.data)
        if not data:
            return
        fname = f"{'_'.join(self.cameraComboBox.currentText().split())}-{int(time.time())}.json"
        QFileDialog.saveFileContent(bytes(data, 'utf-8'), fname)

    def set_stats_label(self, stats: Dict[str, int]):
        text = '\n'.join(f"{k}: {v}" for k, v in stats.items())
        self.statisticsBodyLabel.setText(text)
