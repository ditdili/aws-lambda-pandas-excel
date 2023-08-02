import json
import unittest
from src.handler import main
from unittest.mock import patch
import pandas as pd
from src.utils.serialize import serialize


mock_event = json.loads(open("mocks/event.json", "r").read())
parsed_data = {
    "values": [
        {
            "date": pd.Timestamp("2021-01-01T00:00:00+00:00"),
            "amount": 100,
            "currency": "USD",
            "location": "Test location",
            "description": "Test description",
        }
    ]
}


class TestHandler(unittest.TestCase):
    @patch("src.handler.parse_excel", return_value=parsed_data)
    def test_happy_path(self, mock_parse_excel):
        result = main(mock_event, {})
        print(result)

        self.assertTrue(mock_parse_excel.called)
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"], serialize(parsed_data))

    @patch("src.handler.parse_excel", side_effect=Exception("Unknown error occurred"))
    def test_raise_exception(self, mock_parse_excel):
        result = main(mock_event, {})

        self.assertTrue(mock_parse_excel.called)
        self.assertEqual(result["statusCode"], 500)
        self.assertEqual(
            result["body"],
            "Error converting file mocks/invoices.xlsx: Unknown error occurred",
        )
