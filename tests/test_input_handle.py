import pytest
from tests.utils.constants import USD_CODE, ILS_CODE
from currency_exchange.input_handler import HandleFile


class TestHandleFile:

    def test_parsed_input_len(self):
        mock_file_lines = [USD_CODE, ILS_CODE, '3.6', '4', '100', '25']
        parsed_input = HandleFile.parse_input(mock_file_lines)
        excepted_parsed_input_len = 3
        actual_parsed_input_len = len(parsed_input)
        assert excepted_parsed_input_len == actual_parsed_input_len

    def test_parsed_input_from_curr_index(self):
        mock_file_lines = [USD_CODE, ILS_CODE, '3.6', '4', '100', '25']
        parsed_input = HandleFile.parse_input(mock_file_lines)
        actual_from_curr = parsed_input[HandleFile.FROM_CURR_INDEX]
        excepted_from_curr = USD_CODE
        assert actual_from_curr == excepted_from_curr

    def test_parsed_input_to_curr_index(self):
        mock_file_lines = [USD_CODE, ILS_CODE, '3.6', '4', '100', '25']
        parsed_input = HandleFile.parse_input(mock_file_lines)
        actual_to_curr = parsed_input[HandleFile.TO_CURR_INDEX]
        excepted_to_curr = ILS_CODE
        assert actual_to_curr == excepted_to_curr

    def test_parsed_input_amount_to_convert(self):
        mock_file_lines = [USD_CODE, ILS_CODE, '3.6', '4', '100', '25']
        parsed_input = HandleFile.parse_input(mock_file_lines)
        actual_amount_to_convert = parsed_input[HandleFile.VALUES_INDEX]
        excepted_amount_to_convert = [3.6, 4.0, 100.0, 25.0]
        assert actual_amount_to_convert == excepted_amount_to_convert
