import os
from typing import Union, Optional

import cv2

from vision.mappers.core.context_mapper import ContextMapper
from vision.mappers.core.frame_context import FrameContext


class VideoCapture(ContextMapper[FrameContext]):

    def __init__(self, video_source: Union[int, str] = 0):
        super().__init__()
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self.cap = cv2.VideoCapture(video_source)
        # self.cap = cv2.VideoCapture('rtsp://192.168.100.6:5554/back', cv2.CAP_FFMPEG)
        fps_str = self.cap.get(cv2.CAP_PROP_FPS)
        self.fps: Optional[int] = fps_str or int(fps_str)
        self.frame_number = 0

    def map(self, context: FrameContext) -> FrameContext:
        ret, frame = self.cap.read()
        if not ret:
            raise StopIteration
        self.frame_number += 1

        context.frame_number = self.frame_number
        context.frame = frame
        return context

    def cleanup(self):
        self.cap.release()
