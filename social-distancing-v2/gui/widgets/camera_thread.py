import time
from typing import Optional, Union

import cv2
from PySide6 import QtCore
from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QImage, Qt


class CameraThread(QThread):
    changePixmap = Signal(QImage)

    def __init__(self, parent: Optional[QtCore.QObject] = ..., source: Optional[Union[str, int]] = 0):
        super().__init__(parent)
        self.continue_loop = True
        self.source = source
        self.fps = 30

    def run(self):
        cap = cv2.VideoCapture(self.source)
        cap_fps = cap.get(cv2.CAP_PROP_FPS)
        if cap_fps > 0:
            self.fps = cap_fps
        while self.continue_loop:
            ret, frame = cap.read()
            if ret:
                p = self.convertToQImage(frame)
                self.changePixmap.emit(p)
                time.sleep(1 / self.fps)

    def convertToQImage(self, frame) -> QImage:
        # https://stackoverflow.com/a/55468544/6622587
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)

    def quit(self) -> None:
        self.continue_loop = False
        super().quit()