from typing import Collection
from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext


class ClassFilter(ContextMapper):
    def __init__(self, allowed_classes: Collection[str] = tuple()):
        super().__init__()
        self._allowed_classes = allowed_classes

    def map(self, context: FrameContext) -> FrameContext:
        context.detected_objects = [o for o in context.detected_objects
                                    if o.class_name in self._allowed_classes]
        return context
