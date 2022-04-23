import dataclasses
import json
import os
import sys
import time

import PySide6
import cv2
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QImage, QPolygon
from PySide6.QtWidgets import QMainWindow, QFileDialog

from social_distance.gui.camera_model import Camera
from social_distance.gui.generated_ui.main_window import Ui_MainWindow
from social_distance.gui.thread import CameraThread
from social_distance.gui.widgets.wizard.wizard import CameraAddWizard
from social_distance.lib.types import FrameContext


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
        self.set_stats_label()
        self.camThread.dataChange.connect(self.data_changed)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def set_image(self, context: FrameContext):
        qimage = self._cv_to_qt_image(context.frame)
        scale_factor = min(self.cameraGraphicsView.width() / qimage.width(), self.cameraGraphicsView.height() / qimage.height())
        qimage = qimage.scaled(qimage.width() * scale_factor, qimage.height() * scale_factor)
        qpainter = QtGui.QPainter()
        qpainter.begin(qimage)
        qpainter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2))
        red_pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2)
        green_pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
        for o in context.detected_objects:
            pen = green_pen if o.safe else red_pen
            qpainter.setPen(pen)
            box = o.box
            scaled_box = [
                box[0][0] * scale_factor,
                box[0][1] * scale_factor,
                box[1][0] * scale_factor,
                box[1][1] * scale_factor
            ]
            qpainter.drawRect(scaled_box[0], scaled_box[1], scaled_box[2] - scaled_box[0], scaled_box[3] - scaled_box[1])
        qpainter.end()
        self._pixmap_item.setPixmap(QtGui.QPixmap.fromImage(qimage))

    @staticmethod
    def _cv_to_qt_image(frame) -> QImage:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

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
        return True

    @QtCore.Slot(int)
    def switch_camera(self, index: int):
        self.camThread.update_video_source(self._cameras[index])

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.camThread.quit()
        self.camThread.wait()

        with open(os.path.join('data', 'conf.json'), 'w') as f:
            json.dump([dataclasses.asdict(c) for c in self._cameras], f, indent=2, sort_keys=True)

    def set_distance(self, distance: float):
        self.camThread.set_safe_distance(float(distance))

    def _load_cameras(self):
        self._cameras = []
        try:
            with open(os.path.join('data', 'conf.json'), 'r') as f:
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

    def data_changed(self, context: FrameContext):
        self.set_stats_label(context.violators,
                             len(context.detected_objects) - context.violators,
                             context.violations,
                             context.violation_clusters)

    def set_stats_label(self, safe_count: int = 0, unsafe_count: int = 0,
                        violation_count: int = 0, violation_cluster_count: int = 0):
        text = (f'Safe: {safe_count}\n'
                f'Unsafe: {unsafe_count}\n'
                f'Total: {safe_count + unsafe_count}\n'
                f'Violations: {violation_count}\n'
                f'Violation Clusters: {violation_cluster_count}\n')
        self.statisticsBodyLabel.setText(text)
