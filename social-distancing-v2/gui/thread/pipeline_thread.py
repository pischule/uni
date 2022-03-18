from typing import Optional
import time

import PySide6
import numpy as np
from PySide6.QtCore import QThread, Slot

from lib.composite_frame_mapper import FrameProcessor
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.filter.polygon_filter import PolygonFilter


class PipelineThread(QThread):
    frameProcessed = PySide6.QtCore.Signal(FrameContext)

    def __init__(self, parent=None):
        super(PipelineThread, self).__init__(parent)
        self._image: Optional[np.ndarray] = None
        self._keep_running = False
        self._frame_processor = FrameProcessor()
        self.roi_filter = PolygonFilter()

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
        result = self._frame_processor.map(image)
        result = self.roi_filter.map(result)
        return result

    def quit(self) -> None:
        self._keep_running = False
        super(PipelineThread, self).quit()
