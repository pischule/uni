import time
from typing import Optional, Union

import cv2
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Signal, QThread, Slot
from PySide6.QtGui import QImage, Qt
from numpy import ndarray

from gui.thread.pipeline_thread import PipelineThread
from lib.composite_frame_mapper import FrameProcessor


class CameraThread(QThread):
    changePixmap = Signal(QImage)

    def __init__(self, parent: Optional[QtCore.QObject] = ..., source: Optional[Union[str, int]] = 0):
        super(CameraThread, self).__init__(parent)
        self._continue_loop = False
        self._source = source
        self._cap = None
        self._pipeline_thread = PipelineThread(self)
        self._pipeline_thread.frameProcessed.connect(self.update_pipeline_result)
        self._pipeline_thread.start()
        self._last_pipeline_data = None

    def run(self):
        self._continue_loop = True
        while self._continue_loop:
            self.process_tick()

    @Slot(QtGui.QImage)
    def update_pipeline_result(self, result: ndarray) -> None:
        print('called')
        self._last_pipeline_data = result
        print('pipeline result is done')

    def process_tick(self) -> None:
        if self._cap is None:
            return

        ret, frame = self._cap.read()
        if not ret:
            return
        self._pipeline_thread.pass_image(frame)
        self.changePixmap.emit(self._cv_to_qt_image(frame))

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
