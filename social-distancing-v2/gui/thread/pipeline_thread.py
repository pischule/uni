from typing import Optional
import time

import PySide6
import numpy as np
from PySide6.QtCore import QThread, Slot


class PipelineThread(QThread):
    frameProcessed = PySide6.QtCore.Signal(np.ndarray)

    def __init__(self, parent=None):
        super(PipelineThread, self).__init__(parent)
        self._image: Optional[np.ndarray] = None
        self._keep_running = False

    @Slot(np.ndarray)
    def pass_image(self, image):
        if self._image is None:
            self._image = image

    def run(self):
        self._keep_running = True
        while self._keep_running:
            if (self._image is not None) and (self._image.size > 0):
                result = self.process_image(self._image)
                self.frameProcessed.emit(result)
                self._image = None
            else:
                time.sleep(0.1)

    def process_image(self, image: np.ndarray) -> np.ndarray:
        print("Processing image...")
        return image

    def quit(self) -> None:
        self._keep_running = False
        super(PipelineThread, self).quit()
