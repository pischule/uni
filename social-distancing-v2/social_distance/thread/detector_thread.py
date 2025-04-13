import numpy as np
from PySide6 import QtCore
from PySide6.QtCore import Slot

from social_distance.core.detector import OpenCVPersonDetector


class DetectorThread(QtCore.QThread):
    done = QtCore.Signal(np.ndarray)

    def __init__(self, parent=None):
        super(DetectorThread, self).__init__(parent)
        self.current_image = None
        self.keep_running = False
        self.detector = None

    @QtCore.Slot(np.ndarray)
    def pass_image(self, image: np.ndarray):
        if self.current_image is None:
            self.current_image = image.copy()

    def run(self):
        self.keep_running = True
        while self.keep_running:
            if self.current_image is not None and self.detector:
                result = self._process_frame(self.current_image)
                self.done.emit(result)
                self.current_image = None
            else:
                QtCore.QThread.msleep(10)

    def _process_frame(self, image: np.ndarray) -> np.ndarray:
        return self.detector.detect(image)

    def quit(self) -> None:
        self.keep_running = False

    @Slot(OpenCVPersonDetector)
    def set_detector(self, detector: OpenCVPersonDetector):
        self.detector = detector
