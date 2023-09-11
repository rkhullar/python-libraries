from unittest import TestCase

from ..condition import Condition


class EvalTest(TestCase):

    def test_serialize_simple(self):
        condition = Condition(operator='$eq', field='label', value='lab')
        expected_data = {'operator': '$eq', 'field': 'label', 'value': 'lab'}
        self.assertEqual(expected_data, condition.model_dump())

        serialized_json = condition.model_dump_json()
        incoming_condition = Condition.model_validate_json(serialized_json)
        self.assertEqual(condition, incoming_condition)

    def test_serialize_nested(self):
        condition = Condition(operator='$and', conditions=[
            Condition(operator='$eq', field='label', value='lab'),
            Condition(operator='$lte', field='rating', value=80)
        ])
        expected_data = {'operator': '$and', 'conditions': [
            {'operator': '$eq', 'field': 'label', 'value': 'lab'},
            {'operator': '$lte', 'field': 'rating', 'value': 80}
        ]}
        self.assertEqual(expected_data, condition.model_dump())

        serialized_json = condition.model_dump_json()
        incoming_condition = Condition.model_validate_json(serialized_json)
        self.assertEqual(condition, incoming_condition)

    def test_eval(self):
        condition = Condition(operator='$and', conditions=[
            Condition(operator='$eq', field='label', value='lab'),
            Condition(operator='$lte', field='rating', value=80)
        ])
        test_data = {'rating': 60, 'label': 'lab'}
        self.assertTrue(condition.eval(test_data))
