import unittest
from unittest.mock import patch, Mock
from src.functions.parse_excel import parse_excel, read_to_df
import pandas as pd


class TestReadToDf(unittest.TestCase):
    @patch(
        "src.functions.parse_excel.pd.read_excel",
        return_value=pd.DataFrame({"test": [1]}),
    )
    def test_read_to_df_without_s3(self, mock_read_excel):
        df = read_to_df("bucket_name", "key_name")
        mock_read_excel.assert_called_once_with(
            "bucket_name/key_name", sheet_name="Invoices"
        )
        self.assertEqual(df["test"].iloc[0], 1)

    @patch(
        "src.functions.parse_excel.pd.read_excel",
        return_value=pd.DataFrame({"test": [1]}),
    )
    def test_read_to_df_with_s3(self, mock_read_excel):
        mock_s3_client = Mock()
        mock_s3_client.get_object.return_value = {
            "Body": Mock(read=Mock(return_value=b"test_content"))
        }

        df = read_to_df("bucket_name", "key_name", mock_s3_client)

        mock_read_excel.assert_called_once()
        self.assertEqual(df["test"].iloc[0], 1)


class TestParseExcel(unittest.TestCase):
    @patch(
        "src.functions.parse_excel.read_to_df",
        return_value=pd.DataFrame(
            {
                "Invoice Date": ["2022-01-01", "2022-01-02"],
                "Invoice Amount": ["123 USD", "456 USD"],
                "Location Name": ["Location 1", "Location 2"],
                "Item Description": ["Item 1", "Item 2"],
            }
        ),
    )
    def test_parse_excel(self, mock_read_to_df):
        result = parse_excel("bucket_name", "key_name")

        expected_values = [
            {
                "amount": 123,
                "currency": "USD",
                "date": pd.Timestamp("2022-01-01")
                .tz_localize("US/Eastern")
                .tz_convert("UTC"),
                "description": "Item 1",
                "location": "Location 1",
            },
            {
                "amount": 456,
                "currency": "USD",
                "date": pd.Timestamp("2022-01-02")
                .tz_localize("US/Eastern")
                .tz_convert("UTC"),
                "description": "Item 2",
                "location": "Location 2",
            },
        ]

        mock_read_to_df.assert_called_once()
        self.assertEqual(result["values"], expected_values)

    @patch(
        "src.functions.parse_excel.read_to_df",
        return_value=pd.DataFrame(
            {
                "Invoice Amount": ["123 USD", "456 USD"],
                "Location Name": ["Location 1", "Location 2"],
                "Item Description": ["Item 1", "Item 2"],
            }
        ),
    )
    def test_parse_excel_missing_columns(self, mock_read_to_df):
        with self.assertRaises(ValueError) as context:
            parse_excel("bucket_name", "key_name")

        mock_read_to_df.assert_called_once()
        expected_error_msg = "Missing columns: Invoice Date"
        self.assertEqual(str(context.exception), expected_error_msg)

    @patch(
        "src.functions.parse_excel.read_to_df", side_effect=Exception("Failed to read")
    )
    def test_parse_excel_raises_exception(self, mock_read_to_df):
        with self.assertRaises(Exception) as context:
            parse_excel("bucket_name", "key_name")

        mock_read_to_df.assert_called_once()
        self.assertEqual(str(context.exception), "Failed to read")
