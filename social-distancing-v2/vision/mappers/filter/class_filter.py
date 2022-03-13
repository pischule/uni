from typing import Collection
from vision.mappers.core.context_mapper import ContextMapper
from vision.mappers.core.frame_context import FrameContext


class ClassFilter(ContextMapper[FrameContext]):
    def __init__(self, allowed_classes: Collection[str] = tuple()):
        super().__init__()
        self.allowed_classes = allowed_classes

    def map(self, context: FrameContext) -> FrameContext:
        context.detected_objects = [o for o in context.detected_objects if o.class_name in self.allowed_classes]
        return context
