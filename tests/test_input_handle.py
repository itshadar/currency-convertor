from currency_exchange.input_handler import HandleFile
from tests.utils.samples import HandleFileTestSample


# TODO:
class TestHandleFile:

    @staticmethod
    def excepted_mock_lines_parsed_values():
        return list(map(float, HandleFileTestSample.file_lines[HandleFile.VALUES_INDEX:]))

    def test_parse_input_len(self):
        parsed_input = HandleFile.parse_input(HandleFileTestSample.file_lines)
        assert len(parsed_input) == 3

    def test_parse_input_from_curr(self):
        parsed_input = HandleFile.parse_input(HandleFileTestSample.file_lines)
        assert parsed_input[HandleFile.FROM_CURR_INDEX] == 'USD'

    def test_parse_input_to_curr(self):
        parsed_input = HandleFile.parse_input(HandleFileTestSample.file_lines)
        assert parsed_input[HandleFile.TO_CURR_INDEX] == 'ILS'

    def test_parse_input_values_to_convert(self):
        parsed_input = HandleFile.parse_input(HandleFileTestSample.file_lines)
        assert parsed_input[HandleFile.VALUES_INDEX] == TestHandleFile.excepted_mock_lines_parsed_values()
