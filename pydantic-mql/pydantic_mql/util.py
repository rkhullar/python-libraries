from dataclasses import dataclass
from typing import Literal, Type

StringDict = dict[str, ...]
LiteralType = Type[str]


@dataclass(frozen=True)
class LiteralTypeWithData:
    type: LiteralType
    data: StringDict


def to_literal(data: StringDict, with_data: bool = True) -> LiteralType | LiteralTypeWithData:
    _type = Literal[tuple(data.keys())]
    if with_data:
        # NOTE: cannot assign directly with `_type.data = data`; attributes on Literal don't seem to be isolated
        return LiteralTypeWithData(type=_type, data=data)
    else:
        return _type
