from __future__ import annotations

from typing import Union

from pydantic import BaseModel, RootModel, conlist

from .operator import (ComparisonOperator, LogicalOperator,
                       comparison_operations, logical_operations)

primitive_types = bool, int, float, str
PrimitiveValue = Union[primitive_types]


class ComparisonCondition(BaseModel):
    operator: ComparisonOperator
    field: str
    value: PrimitiveValue | list[PrimitiveValue]

    def eval(self, data: dict) -> bool:
        handler = comparison_operations[self.operator]
        return handler(data.get(self.field), self.value)


class LogicalCondition(BaseModel):
    operator: LogicalOperator
    conditions: conlist(item_type=Condition, min_length=1)

    def eval(self, data: dict) -> bool:
        handler = logical_operations[self.operator]
        nested_stream = (condition.eval(data) for condition in self.conditions)
        return handler(nested_stream)


class Condition(RootModel):
    root: ComparisonCondition | LogicalCondition

    def eval(self, data: dict) -> bool:
        return self.root.eval(data)
