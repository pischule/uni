import cv2

from lib.mappers.core.context_mapper import ContextMapper

from lib.mappers.core.frame_context import FrameContext
from lib.mappers.util.custom_types import Polygon, Point
from lib.mappers.util.helper_functions import polygon_to_numpy_array


class PolygonFilter(ContextMapper[FrameContext]):
    def __init__(self, polygon: Polygon, inside: bool = True):
        self._inside: bool = inside
        self._polygon = polygon_to_numpy_array(polygon)

    def map(self, context: FrameContext) -> FrameContext:

        filtered_objects = []
        for obj in context.detected_objects:
            ((p1_x, p1_y), (p2_x, p2_y)) = obj.box
            bottom_center: Point = (int(p1_x + p2_x) // 2, int(p2_y))
            dist = cv2.pointPolygonTest(contour=self._polygon, pt=bottom_center, measureDist=False)

            if (dist >= 0) == self._inside:
                filtered_objects.append(obj)
        context.detected_objects = filtered_objects
        return context
