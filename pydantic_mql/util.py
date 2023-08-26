from typing import Literal, Type


def to_literal(data: dict) -> Type[str]:
    return Literal[tuple(data.keys())]
