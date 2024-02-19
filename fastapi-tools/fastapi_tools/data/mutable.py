from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass
class Proxy(Generic[T]):
    _data: T

    def set(self, data: T) -> None:
        self._data = data

    def get(self) -> T:
        return self._data

    def __repr__(self) -> str:
        return str(self._data)

    @classmethod
    def field(cls, default: T = None, **kwargs):
        return field(init=False, default_factory=lambda: Proxy(_data=default), **kwargs)
