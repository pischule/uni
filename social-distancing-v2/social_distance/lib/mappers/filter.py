import cv2
import numpy as np

from social_distance.lib.types import Point, ContextMapper, FrameContext


class PolygonFilter(ContextMapper):
    def __init__(self, polygon=None, inside: bool = True):
        if polygon is None:
            polygon = []
        self._inside: bool = inside
        self.polygon = polygon

    def map(self, context: FrameContext) -> FrameContext:
        if (self.polygon is None) or (len(self.polygon) == 0):
            return context

        filtered_objects = []
        for obj in context.detected_objects:
            ((p1_x, p1_y), (p2_x, p2_y)) = obj.box
            bottom_center: Point = (int(p1_x + p2_x) // 2, int(p2_y))
            dist = cv2.pointPolygonTest(contour=self._polygon, pt=bottom_center, measureDist=False)

            if (dist >= 0) == self._inside:
                filtered_objects.append(obj)
        context.detected_objects = filtered_objects
        return context

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon: list):
        self._polygon = np.asarray(polygon, np.int32).reshape((-1, 1, 2))
