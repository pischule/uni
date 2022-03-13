import cv2

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext


class InfoOverlay(ContextMapper[FrameContext]):
    def __init__(self, show_fps: bool = True):
        super().__init__()
        self._x = 10
        self._y = None
        self._y_offset = 30
        self._show_fps = show_fps

    def map(self, context: FrameContext) -> FrameContext:
        self._y = 30

        if self._show_fps:
            self._draw_field(context.frame, 'fps', f'{context.fps:.2f}')

        return context

    def _draw_field(self, img, key: str, value: str):
        cv2.putText(img=img,
                    text=f'{key}: {value}',
                    org=(self._x, self._y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=.8,
                    thickness=2,
                    color=(255, 255, 255))
        self._y += self._y_offset
