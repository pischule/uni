import cv2

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.util.custom_types import Color, Polygon
from lib.mappers.util.helper_functions import polygon_to_numpy_array


class DrawPolygon(ContextMapper[FrameContext]):
    def __init__(self, polygon: Polygon = (), color: Color = (255, 255, 0)):
        self._color = color
        self._polygon = polygon_to_numpy_array(polygon)

    def map(self, context: FrameContext) -> FrameContext:
        cv2.polylines(context.frame, [self._polygon], True, self._color)
        return context
