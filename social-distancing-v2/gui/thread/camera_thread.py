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
    draw_boxes = DrawBoxes(color=(0, 200, 0), thickness=2, label=True)

    def __init__(self, parent: Optional[QtCore.QObject] = ..., source: Optional[Union[str, int]] = 0):
        super(CameraThread, self).__init__(parent)
        self._continue_loop = False
        self._source = source
        self._cap = None
        self._pipeline_thread = PipelineThread(self)
        self._pipeline_thread.frameProcessed.connect(self.update_pipeline_result)
        self._pipeline_thread.start()
        self._last_pipeline_data = FrameContext()
        self._last_pipeline_data.detected_objects = []

    def run(self):
        self._continue_loop = True
        while self._continue_loop:
            self.process_tick()
            time.sleep(0.01)

    @Slot(FrameContext)
    def update_pipeline_result(self, result: FrameContext) -> None:
        self._last_pipeline_data = result

    def process_tick(self) -> None:
        if self._cap is None:
            return

        ret, frame = self._cap.read()
        if not ret:
            return
        self._pipeline_thread.pass_image(frame)

        # draw boxes
        fc = FrameContext()
        fc.frame = frame
        fc.detected_objects = self._last_pipeline_data.detected_objects or []
        fc = self.draw_boxes.map(fc)
        self.changePixmap.emit(self._cv_to_qt_image(fc.frame))

    def update_video_source(self, source: str) -> None:
        if self._source != source:
            return
        self._source = 0 if source == "0" else source
        if self._cap is not None:
            self._cap.release()
        self._cap = cv2.VideoCapture(self._source)

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
