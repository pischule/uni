from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext
from sort import Sort


class BackgroundSubtractorDetector(ContextMapper[FrameContext]):
    def __init__(self):
        mot_tracker = Sort()

    def map(self, context: FrameContext) -> FrameContext:


        return context
