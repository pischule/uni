import cv2
import numpy as np

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext

from lib.util import box_bottom_center_point


class AbsolutePositionsCalculator(ContextMapper):
    def __init__(self, transform_matrix: np.ndarray):
        self._transform_matrix = transform_matrix

    def map(self, context: FrameContext) -> FrameContext:
        if not context.detected_objects:
            return context
        box_bottom_centers = [box_bottom_center_point(o.box) for o in context.detected_objects]
        np_points = np.asarray([box_bottom_centers], dtype=np.float32)
        absolute_points = cv2.perspectiveTransform(np_points, self._transform_matrix)[0]
        for o, p in zip(context.detected_objects, absolute_points):
            o.absolute_position = tuple(p)
            print(f"{o.track_id} absolute position: {o.absolute_position}")
        return context
