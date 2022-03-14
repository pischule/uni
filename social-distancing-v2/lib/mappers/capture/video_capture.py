import math
import os
from time import sleep
from typing import Union, Optional

import cv2
import numpy as np

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext


class VideoCapture(ContextMapper):

    def __init__(self, video_source: Union[int, str] = 0, limit_fps=False):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self._cap = cv2.VideoCapture(video_source)
        # self.cap = cv2.VideoCapture('rtsp://192.168.100.6:5554/back', cv2.CAP_FFMPEG)
        fps_str = self._cap.get(cv2.CAP_PROP_FPS)
        self._fps: float = fps_str
        self._frame_number = 0
        self._limit_fps = limit_fps

    def map(self, context: FrameContext) -> FrameContext:
        ret, frame = self._cap.read()
        if not ret:
            raise StopIteration
        self._frame_number += 1

        if self._fps and self._limit_fps:
            sleep(1 / self._fps)

        context.frame_number = self._frame_number
        context.frame = frame
        return context

    def cleanup(self):
        self._cap.release()
