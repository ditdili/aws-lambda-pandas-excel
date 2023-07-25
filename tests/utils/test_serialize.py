import unittest
from decimal import Decimal
from unittest.mock import patch, Mock

from utils.serialize import serialize


class TestSerialize(unittest.TestCase):
    def test_serialize_decimal(self):
        obj = {"value": Decimal("5.67")}
        expected_output = '{\n    "value": "5.67"\n}'
        self.assertEqual(serialize(obj), expected_output)

    def test_mock_isinstance(self):
        with patch("utils.serialize.DecimalEncoder.default", side_effect=TypeError):
            with self.assertRaises(TypeError) as e:
                serialize(Decimal("5.67"))
            self.assertEqual(
                e.exception.args[0],
                "Object of type <class 'decimal.Decimal'> is not JSON serializable",
            )

    def test_serialize_none(self):
        self.assertEqual(serialize(None), "null")
