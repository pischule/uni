from typing import TypeVar, Generic

from lib.mappers.core.frame_context import FrameContext

F = TypeVar('F')
T = TypeVar('T')


class GenericMapper(Generic[F, T]):

    def map(self, context: F) -> T:
        return None

    def cleanup(self):
        pass


class ContextMapper(GenericMapper[FrameContext, FrameContext]):
    def map(self, context: FrameContext) -> FrameContext:
        pass

    def cleanup(self):
        pass
