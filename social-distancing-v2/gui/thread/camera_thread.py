import os
import time
from typing import Optional, Union

import cv2
from PySide6 import QtCore
from PySide6.QtCore import Signal, QThread, Slot
from PySide6.QtGui import QImage

from gui.thread.pipeline_thread import PipelineThread
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.overlay.draw_boxes import DrawBoxes


class CameraThread(QThread):
    changePixmap = Signal(QImage)
    draw_boxes = DrawBoxes(color=(0, 200, 0), thickness=2, label=False, only_tracked=False)
    camera_mutex = QtCore.QMutex()

    def __init__(self, parent: Optional[QtCore.QObject] = ..., source: Optional[Union[str, int]] = None):
        super(CameraThread, self).__init__(parent)
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self._continue_loop = False
        self._source = source
        self._cap = None
        self._pipeline_thread = PipelineThread(self)
        self._pipeline_thread.frameProcessed.connect(self.update_pipeline_result)
        self._pipeline_thread.start()
        self._last_pipeline_data = FrameContext()
        self._last_pipeline_data.detected_objects = []

        self._delay = 0.01
        self._skip_result = False

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
        self._pipeline_thread.pass_image(frame)
        fc = self.draw_boxes.map(FrameContext.from_frame(frame, self._last_pipeline_data.detected_objects))
        self.changePixmap.emit(self._cv_to_qt_image(fc.frame))

    def reset_pipeline(self):
        self._last_pipeline_data.detected_objects = list()
        self._last_pipeline_data.frame = None

    def update_video_source(self, source: str) -> None:
        if source == '0':
            source = 0
        if self._source == source:
            return
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

    @staticmethod
    def _cv_to_qt_image(frame) -> QImage:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

    def quit(self) -> None:
        self._continue_loop = False
        if self._cap:
            self._cap.release()
        self._pipeline_thread.quit()
        self._pipeline_thread.wait()
        super().quit()
