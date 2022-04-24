from typing import List

import cv2
import numpy as np

from social_distance.lib.types import DetectedObject


class PolygonFilter:
    def __init__(self, polygon=None, inside: bool = True):
        if polygon is None:
            polygon = []
        self._inside: bool = inside
        self.polygon = polygon

    def filter(self, objects: List[DetectedObject]) -> List[DetectedObject]:
        if (self.polygon is None) or (len(self.polygon) == 0):
            return objects

        filtered_objects = []
        for obj in objects:
            x, y = obj.rect.bottom_center
            dist = cv2.pointPolygonTest(contour=self._polygon, pt=(int(x), int(y)), measureDist=False)

            if (dist >= 0) == self._inside:
                filtered_objects.append(obj)
        return filtered_objects

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon: list):
        self._polygon = np.asarray(polygon, np.int32).reshape((-1, 1, 2))
