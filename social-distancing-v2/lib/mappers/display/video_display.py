import cv2
import uuid

from lib.mappers.core.frame_context import FrameContext
from lib.mappers.core.context_mapper import ContextMapper


class VideoDisplay(ContextMapper):
    def __init__(self, window_name: str = uuid.uuid4().hex):
        super().__init__()
        self._window_name = window_name
        cv2.startWindowThread()
        cv2.namedWindow(self._window_name, cv2.WINDOW_AUTOSIZE)

    def map(self, context: FrameContext) -> FrameContext:
        cv2.imshow(self._window_name, context.frame)
        # Press ESC or q to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            raise StopIteration
        return context

    def cleanup(self):
        cv2.destroyWindow(self._window_name)
