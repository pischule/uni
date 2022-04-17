import cv2
import numpy as np

from social_distance.lib.types import ContextMapper, FrameContext

from social_distance.lib.util import box_bottom_center_point


class AbsolutePositionsCalculator(ContextMapper):
    def __init__(self, transform_matrix: np.ndarray = np.diag(np.ones(3, dtype=np.float32))) -> None:
        self._transform_matrix = transform_matrix

    def map(self, context: FrameContext) -> FrameContext:
        if not context.detected_objects:
            return context
        box_bottom_centers = [box_bottom_center_point(o.box) for o in context.detected_objects]
        np_points = np.asarray([box_bottom_centers], dtype=np.float32)
        absolute_points = cv2.perspectiveTransform(np_points, self._transform_matrix)[0]
        for o, p in zip(context.detected_objects, absolute_points):
            o.absolute_position = tuple(p)
        return context

    @property
    def transform_matrix(self):
        return self._transform_matrix

    @transform_matrix.setter
    def transform_matrix(self, value: list):
        self._transform_matrix = np.asarray(value, dtype=np.float32)