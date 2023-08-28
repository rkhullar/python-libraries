from ..util import to_literal

equality_operations = {
    '$eq': lambda a, b: a == b,
    '$ne': lambda a, b: a != b
}

numeric_operations = {
    '$gt': lambda a, b: a > b,
    '$lt': lambda a, b: a < b,
    '$gte': lambda a, b: a >= b,
    '$lte': lambda a, b: a <= b
}

logical_operations = {
    '$and': lambda flags: all(flags),
    '$or': lambda flags: any(flags),
    '$not': lambda flags: not flags[0]
}

comparison_operations = {**equality_operations, **numeric_operations}

EqualityOperator = to_literal(equality_operations)
NumericOperator = to_literal(numeric_operations)
ComparisonOperator = to_literal(comparison_operations)
LogicalOperator = to_literal(logical_operations)
