## Pydantic MQL

This library can parse and evaluate conditions using pydantic. The usage is similar to the MongoDB Query Language.
But instead of filtering documents within a database collection you can use the library to filter arbitrary application
data in memory.

### Example Usage

#### Parsing
```python
from pydantic_mql import Condition
test_json = '{"operator": "$eq", "field": "label", "value": "lab"}'
condition = Condition.model_validate_json(test_json)
print(condition)
```

#### Serializing
```python
from pydantic_mql import Condition
condition = Condition(operator='$and', conditions=[
    Condition(operator='$eq', field='label', value='lab'),
    Condition(operator='$lte', field='rating', value=80)
])
print(condition.model_dump())
```

#### Condition Eval
```python
test_data = {'rating': 60, 'label': 'lab'}
result = condition.eval(test_data)
print(result)
```
