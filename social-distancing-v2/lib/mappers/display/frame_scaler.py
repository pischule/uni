from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext

import cv2

from lib.mappers.util.custom_types import Point


class FrameScaler(ContextMapper):
    def __init__(self, new_size: Point):
        self.new_size = new_size

    def map(self, context: FrameContext) -> FrameContext:
        min_scale = min(self.new_size[0] / context.frame.shape[0], self.new_size[1] / context.frame.shape[1])
        context.frame = cv2.resize(context.frame, (0, 0), fx=min_scale, fy=min_scale)
        return context