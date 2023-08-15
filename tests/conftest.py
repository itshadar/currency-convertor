import pytest
from tests.utils.mocks import ExchangeServiceMock
from tests.utils.constants import USD_CODE, ILS_CODE
from currency_exchange.exchange import Exchange
from currency_exchange.exchange_service import FrankfurterExchangeService
from httpx import AsyncClient



def pytest_addoption(parser):
    parser.addoption("--file", action="store", default="input.txt")


@pytest.fixture(scope="session")
def file_path(pytestconfig):
    return pytestconfig.getoption("file")


@pytest.fixture()
def mock_main_arguments(mocker):
    mock_arguments = mocker.patch('main.Arguments')
    mock_args = mocker.Mock()
    mock_args.get_file_path.return_value = file_path
    mock_arguments.return_value = mock_args
    return mock_arguments

@pytest.fixture
def mock_exchange_service():
    return ExchangeServiceMock()


@pytest.fixture
def frankfurter_exchange_service():
    return FrankfurterExchangeService()


@pytest.fixture()
async def usd_usd_mock_currency_exchange(mock_exchange_service):
    return await Exchange.create(from_curr=USD_CODE, to_curr=USD_CODE, exchange_service=mock_exchange_service)


@pytest.fixture
async def usd_ils_mock_currency_exchange(mock_exchange_service):
    return await Exchange.create(from_curr=USD_CODE, to_curr=ILS_CODE, exchange_service=mock_exchange_service)


@pytest.fixture
def frankfurter_exchange_service_get_key_error(httpx_mock):
    mock_response_data = {"notRates": {"ILS": 3.5}}
    httpx_mock.add_response(json=mock_response_data)
    return httpx_mock
