import cv2
import numpy as np

from social_distance.lib.types import Color, FrameContext


class PolygonDrawer:
    def __init__(self, polygon=None, color: Color = (0, 255, 0), alpha=0.5, inverted=False):
        if polygon is None:
            polygon = list()
        self._color = color
        self._polygon = polygon
        self._alpha = alpha
        self._inverted = inverted

    def map(self, context: FrameContext) -> FrameContext:
        if self._inverted:
            img_red = np.zeros_like(context.frame)
            img_red[:, :, -1] = 255
            mask = np.full_like(context.frame, (1, 1, 1), dtype=np.float32)
            mask = cv2.fillPoly(mask, [self.polygon], (0, 0, 0), lineType=cv2.LINE_AA)
            result = cv2.add(context.frame * (1 - mask), img_red * mask).astype(np.uint8)
            context.frame = cv2.addWeighted(context.frame, 1 - self._alpha, result, self._alpha, 0)
        else:
            # frame = cv2.polylines(context.frame.copy(), [self.polygon], True, self._color, 2)
            frame = cv2.fillPoly(context.frame.copy(), [self.polygon], self._color, lineType=cv2.LINE_AA)
            context.frame = cv2.addWeighted(context.frame, 1 - self._alpha, frame, self._alpha, 0)
        return context

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon: list):
        self._polygon = np.asarray(polygon, np.int32).reshape((-1, 1, 2))
