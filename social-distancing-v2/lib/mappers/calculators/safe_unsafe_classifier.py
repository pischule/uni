import math

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext


class SafeUnsafeClassifier(ContextMapper):
    def __init__(self):
        self.safe_distance = 0.0

    def map(self, context: FrameContext) -> FrameContext:
        for p in context.detected_objects:
            p.safe = True
        for i, p1 in enumerate(context.detected_objects):
            for j, p2 in enumerate(context.detected_objects):
                if i != j:
                    p1x, p1y = tuple(p1.absolute_position)
                    p2x, p2y = tuple(p2.absolute_position)
                    distance = math.hypot(p1x - p2x, p1y - p2y)
                    if distance < self.safe_distance:
                        p1.safe = False
                        p2.safe = False
        return context
