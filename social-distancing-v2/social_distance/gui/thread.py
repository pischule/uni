import os
import time
from enum import Enum
from typing import Optional, Union

import PySide6
import cv2
import numpy as np
from PySide6 import QtCore
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage

from social_distance.gui.camera_model import Camera
from social_distance.lib.mappers.calculator import AbsolutePositionsCalculator
from social_distance.lib.mappers.classifier import SafeDistanceClassifier
from social_distance.lib.mappers.detector import OpenCVDetector
from social_distance.lib.mappers.drawer import BoxesDrawer, FrameScaler, PolygonDrawer
from social_distance.lib.mappers.filter import PolygonFilter
from social_distance.lib.types import FrameContext


class CameraThread(QThread):
    changePixmap = Signal(QImage)
    dataChange = Signal(FrameContext)
    _draw_boxes = BoxesDrawer(thickness=2, label=False, only_tracked=False)
    camera_mutex = QtCore.QMutex()

    def __init__(self, parent: Optional[QtCore.QObject] = ..., source: Optional[Union[str, int]] = None):
        super(CameraThread, self).__init__(parent)
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self._continue_loop = False
        self._source = source
        self._cap = None
        self._pipeline_thread = PipelineThread(self, Networks.YOLOv3)
        self._pipeline_thread.frameProcessed.connect(self.update_pipeline_result)
        self._pipeline_thread.start()
        self._last_pipeline_data = FrameContext()
        self._last_pipeline_data.detected_objects = []

        self._scaler = FrameScaler(new_size=(1280, 720))

        self._delay = 0.01
        self._skip_result = False

        self._polygon_drawer = PolygonDrawer(None, (0, 0, 255), alpha=0.2, inverted=True)
        self.data = []

    def run(self):
        self._continue_loop = True
        while self._continue_loop:
            self.process_tick()
            time.sleep(self._delay)

    @Slot(FrameContext)
    def update_pipeline_result(self, result: FrameContext) -> None:
        if self._skip_result:
            self._skip_result = False
            return
        self._last_pipeline_data = result
        self.dataChange.emit(result)

        self.data += [{
            "time": time.time(),
            "detected_objects": [
                obj.to_dict() for obj in result.detected_objects
            ]
        }]

    def process_tick(self) -> None:
        self.camera_mutex.lock()
        if self._cap is None:
            self.camera_mutex.unlock()
            return
        ret, frame = self._cap.read()
        self.camera_mutex.unlock()
        if not ret:
            return

        # draw boxes
        # if self._show_detection:
        context = FrameContext.from_frame(frame)
        context = self._scaler.map(context)
        self._pipeline_thread.pass_image(context.frame)
        context = self._polygon_drawer.map(context)
        context.detected_objects = self._last_pipeline_data.detected_objects
        context = self._draw_boxes.map(context)
        self.changePixmap.emit(self._cv_to_qt_image(context.frame))

    def reset_pipeline(self):
        self._last_pipeline_data.detected_objects = list()
        self._last_pipeline_data.frame = None

    def update_video_source(self, cam: Camera) -> None:
        source = cam.address
        if source == '0':
            source = 0
        new_cap = cv2.VideoCapture(source)
        if not new_cap.isOpened():
            return
        self.camera_mutex.lock()
        if self._cap is not None:
            self._cap.release()
        self._cap = new_cap
        self._source = source
        self._skip_result = True
        self.camera_mutex.unlock()

        fps = self._cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            self._delay = 1 / fps
        else:
            self._delay = 0.01

        self._polygon_drawer.polygon = cam.roi
        self._pipeline_thread.roi_filter.polygon = cam.roi
        self.data = []
        self._pipeline_thread.position_calculator.transform_matrix = cam.transform_matrix

    @staticmethod
    def _cv_to_qt_image(frame) -> QImage:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

    def set_safe_distance(self, distance: float):
        self._pipeline_thread.safety_classifier.safe_distance = distance

    def quit(self) -> None:
        self._continue_loop = False
        if self._cap:
            self._cap.release()
        self._pipeline_thread.quit()
        self._pipeline_thread.wait()

        super().quit()


class Networks(Enum):
    YOLOv3 = 'yolov3'
    YOLOv3_TINY = 'yolov3-tiny'


class PipelineThread(QThread):
    frameProcessed = PySide6.QtCore.Signal(FrameContext)

    def __init__(self, parent=None, network: Networks = Networks.YOLOv3):
        super(PipelineThread, self).__init__(parent)
        self._image: Optional[np.ndarray] = None
        self._keep_running = False
        self.detector = OpenCVDetector(
            model_config=os.path.join('data', 'models', network.value + '.cfg'),
            model_weights=os.path.join('data', 'models', network.value + '.weights'),
            conf_threshold=0.6, nms_threshold=0.4)
        self.roi_filter = PolygonFilter()
        self.position_calculator = AbsolutePositionsCalculator()
        self.safety_classifier = SafeDistanceClassifier()

    @Slot(np.ndarray)
    def pass_image(self, image):
        if self._image is None:
            self._image = image.copy()

    def run(self):
        self._keep_running = True
        while self._keep_running:
            if (self._image is not None) and (self._image.size > 0):
                result = self.process_image(self._image)
                self.frameProcessed.emit(result)
                self._image = None
            else:
                time.sleep(0.01)

    def process_image(self, image: np.ndarray) -> FrameContext:
        c = FrameContext()
        c.frame = image

        c = self.detector.map(c)
        c = self.roi_filter.map(c)
        c = self.position_calculator.map(c)
        c = self.safety_classifier.map(c)
        return c

    def quit(self) -> None:
        self._keep_running = False
        super(PipelineThread, self).quit()
