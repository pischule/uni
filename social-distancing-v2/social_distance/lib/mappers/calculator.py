from typing import List

import cv2
import numpy as np

from social_distance.lib.types import FrameContext, DetectedObject


class AbsolutePositionsCalculator:
    def __init__(self, transform_matrix: np.ndarray = np.diag(np.ones(3, dtype=np.float32))) -> None:
        self._transform_matrix = transform_matrix

    def calc(self, objects: List[DetectedObject]) -> FrameContext:
        if not objects:
            return objects
        box_bottom_centers = [o.rect.bottom_center for o in objects]
        np_points = np.asarray([box_bottom_centers], dtype=np.float32)
        absolute_points = cv2.perspectiveTransform(np_points, self._transform_matrix)[0]
        for o, p in zip(objects, absolute_points):
            o.absolute_position = tuple(p)
        return objects

    @property
    def transform_matrix(self):
        return self._transform_matrix

    @transform_matrix.setter
    def transform_matrix(self, value: list):
        self._transform_matrix = np.asarray(value, dtype=np.float32)