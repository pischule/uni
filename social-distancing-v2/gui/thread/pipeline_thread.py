import os.path
from enum import Enum
from typing import Optional
import time

import PySide6
import numpy as np
from PySide6.QtCore import QThread, Slot

from lib.mappers.calculators.absolute_positions_calculator import AbsolutePositionsCalculator
from lib.mappers.calculators.safe_unsafe_classifier import SafeUnsafeClassifier
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.detector.opencv_detector import OpenCVDetector
from lib.mappers.filter.polygon_filter import PolygonFilter


class Networks(Enum):
    YOLOv3 = 'yolov3'
    YOLOv3_TINY = 'yolov3-tiny'
    # SSD_MOBILENET = 'ssd_mobilenet'


class PipelineThread(QThread):
    frameProcessed = PySide6.QtCore.Signal(FrameContext)

    def __init__(self, parent=None, network: Networks = Networks.YOLOv3):
        super(PipelineThread, self).__init__(parent)
        self._image: Optional[np.ndarray] = None
        self._keep_running = False
        # self._frame_processor = FrameProcessor()
        self.detector = OpenCVDetector(
            model_config=os.path.join('models', network.value + '.cfg'),
            model_weights=os.path.join('models', network.value + '.weights'),
            conf_threshold=0.6, nms_threshold=0.4)
        self.roi_filter = PolygonFilter()
        self.position_calculator = AbsolutePositionsCalculator()
        self.safety_classifier = SafeUnsafeClassifier()

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
        context = FrameContext()
        context.frame = image

        result = self.detector.map(context)
        result = self.roi_filter.map(result)
        result = self.position_calculator.map(result)
        result = self.safety_classifier.map(result)
        return result

    def quit(self) -> None:
        self._keep_running = False
        super(PipelineThread, self).quit()
