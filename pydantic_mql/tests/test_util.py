from unittest import TestCase

from ..util import to_literal


class UtilTest(TestCase):

    def test_to_literal(self):
        mapping = {'a': 1, 'b': 2}
        type_data = to_literal(mapping)
        self.assertEqual("typing.Literal['a', 'b']", str(type_data.type))
        self.assertEqual(mapping, type_data.data)
