import time

from vision.mappers.core.context_mapper import ContextMapper
from vision.mappers.core.frame_context import FrameContext


class FpsCounter(ContextMapper[FrameContext]):
    def __init__(self, every: int = 5):
        super().__init__()
        self._prev_timestamp = time.time()
        self._every = every
        self._frame_count = 0
        self._fps = -1

    def map(self, context: FrameContext) -> FrameContext:
        if self._frame_count >= self._every:
            current_timestamp = time.time()
            self._fps = int(1 / (current_timestamp - self._prev_timestamp) * self._every)
            self._prev_timestamp = current_timestamp
            self._frame_count = -1
        context.fps = self._fps
        self._frame_count += 1
        return context
