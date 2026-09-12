from abc import ABC, abstractmethod
from collections.abc import Iterable


class ValueObject(ABC):
    """Optional equality base; concrete value objects must keep their values immutable."""

    @abstractmethod
    def get_equality_components(self) -> Iterable[object]: ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject) or type(other) is not type(self):
            return NotImplemented
        return tuple(self.get_equality_components()) == tuple(other.get_equality_components())

    def __hash__(self) -> int:
        return hash((type(self), tuple(self.get_equality_components())))
