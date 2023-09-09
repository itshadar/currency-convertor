from polyfactory.factories.pydantic_factory import ModelFactory
from currency_exchange.exchange_frankfurter_http_client import FrankfurterJsonResponse
from currency_exchange.exchange_frankfurter_http_client import FrankfurterHTTPExchangeClient
from .utils.constants import USD_CODE, ILS_CODE
import pytest
from pytest_httpx import httpx_mock


class FrankfurterJsonResponseFactory(ModelFactory[FrankfurterJsonResponse]):
    __model__ = FrankfurterJsonResponse


@pytest.fixture
def mock_frankfurter_exchange_service():
    return FrankfurterHTTPExchangeClient()

@pytest.fixture
def mock_to_curr_ils_json_response():
    fields_meta = {"rates": {ILS_CODE: 3.5}}
    mock_response_obj = FrankfurterJsonResponseFactory.build(**fields_meta)
    return mock_response_obj.model_dump()


class TestFrankfurterHttpClient:

    @pytest.mark.asyncio
    async def test_valid_response_fetch_currency_rate(self, httpx_mock, mock_frankfurter_exchange_service,
                                                      mock_to_curr_ils_json_response):

        httpx_mock.add_response(json=mock_to_curr_ils_json_response)
        excepted_rate = 3.5

        async with mock_frankfurter_exchange_service as client:
            currency_rate = await client.fetch_currency_rate(USD_CODE, ILS_CODE)

        assert currency_rate == excepted_rate

    @pytest.mark.asyncio
    async def test_invalid_response_fetch_currency_rate(self, httpx_mock, mock_frankfurter_exchange_service) -> None:

        mock_response_data = {"some_rates": {ILS_CODE: 4.5}}
        httpx_mock.add_response(json=mock_response_data)

        with pytest.raises(ValueError):
            async with mock_frankfurter_exchange_service as client:
                await client.fetch_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)

    @pytest.mark.asyncio
    async def test_called_url_fetch_currency_rate(self, httpx_mock, mock_frankfurter_exchange_service,
                                                  mock_to_curr_ils_json_response) -> None:

        httpx_mock.add_response(json=mock_to_curr_ils_json_response)

        async with mock_frankfurter_exchange_service as client:
            await client.fetch_currency_rate(USD_CODE, ILS_CODE)

        excepted_request_url = f"{mock_frankfurter_exchange_service.BASE_URL}/latest?from={USD_CODE}&to={ILS_CODE}"
        actual_request_url = httpx_mock.get_request().url

        assert actual_request_url == excepted_request_url
