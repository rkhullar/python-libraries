from __future__ import annotations

from typing import Self, Union

from pydantic import BaseModel, RootModel, conlist, model_validator

from .eval.operator import ComparisonOperator, LogicalOperator

primitive_types = bool, int, float, str
PrimitiveValue = Union[primitive_types]


class ComparisonCondition(BaseModel):
    operator: ComparisonOperator.type
    field: str
    value: PrimitiveValue | list[PrimitiveValue]

    @model_validator(mode='after')
    def check_value_type(self) -> Self:
        if isinstance(self.value, list):  # and operator is meant for collections
            raise ValueError
        return self

    def eval(self, data: dict) -> bool:
        handler = ComparisonOperator.data[self.operator]
        return handler(data.get(self.field), self.value)


class LogicalCondition(BaseModel):
    operator: LogicalOperator.type
    conditions: conlist(item_type=Condition, min_length=1)

    def eval(self, data: dict) -> bool:
        handler = LogicalOperator.data[self.operator]
        nested_stream = (condition.eval(data) for condition in self.conditions)
        return handler(nested_stream)


class Condition(RootModel):
    root: ComparisonCondition | LogicalCondition

    def eval(self, data: dict) -> bool:
        return self.root.eval(data)
