import pytest
from main import main
from tests.utils.constants import USD_CODE, ILS_CODE
from tests.conftest import mock_exchange_client
from currency_exchange.input_handler import HandleFile


def pytest_addoption(parser):
    parser.addoption("--file", action="store", default="test_input.txt")


@pytest.fixture(scope="session")
def mock_file_path(pytestconfig):
    return pytestconfig.getoption("file")


@pytest.fixture()
def mock_main_arguments(mocker):
    mock_arguments = mocker.patch('main.Arguments')
    mock_args = mocker.Mock()
    mock_args.get_file_path.return_value = mock_file_path
    mock_arguments.return_value = mock_args
    return mock_arguments


class TestMain:

    @staticmethod
    def excepted_print_out(values, currency_rate):
        return "".join([f"{float(value) * currency_rate}\n" for value in values[HandleFile.VALUES_INDEX]])

    @pytest.mark.parametrize("mock_input, excepted_rate", [
                             ((USD_CODE, ILS_CODE, [100.0, 200]), "mock_exchange_client.MOCK_RATE"),
                             ((USD_CODE, USD_CODE, [100.0, 200]), "1.0")])
    @pytest.mark.asyncio
    async def test_main_conversion(self, mocker, capsys, mock_exchange_client, mock_main_arguments, excepted_rate, mock_input):

        excepted_rate = eval(excepted_rate)
        mocker.patch('main.FrankfurterHTTPExchangeClient', return_value=mock_exchange_client)
        mocker.patch('main.HandleFile.handle_input', mocker.AsyncMock(return_value=mock_input))

        await main()

        out, err = capsys.readouterr()
        assert out == TestMain.excepted_print_out(mock_input, excepted_rate)