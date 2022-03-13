from typing import TypeVar, Generic

T = TypeVar('T')


class ContextMapper(Generic[T]):

    def map(self, context: T) -> T:
        return None

    def cleanup(self):
        pass
