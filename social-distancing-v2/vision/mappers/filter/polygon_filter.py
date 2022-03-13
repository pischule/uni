import cv2

from vision.mappers.core.context_mapper import ContextMapper

from vision.mappers.core.frame_context import FrameContext
from vision.mappers.util.custom_types import Polygon, Point
from vision.mappers.util.helper_functions import polygon_to_numpy_array


class PolygonFilter(ContextMapper[FrameContext]):
    def __init__(self, polygon: Polygon, inside: bool = True):
        self.inside: bool = inside
        self.polygon = polygon_to_numpy_array(polygon)

    def map(self, context: FrameContext) -> FrameContext:

        filtered_objects = []
        for obj in context.detected_objects:
            ((p1_x, p1_y), (p2_x, p2_y)) = obj.box
            bottom_center: Point = (int(p1_x + p2_x) // 2, int(p2_y))
            dist = cv2.pointPolygonTest(contour=self.polygon, pt=bottom_center, measureDist=False)

            if (dist >= 0) == self.inside:
                filtered_objects.append(obj)
        context.detected_objects = filtered_objects
        return context
