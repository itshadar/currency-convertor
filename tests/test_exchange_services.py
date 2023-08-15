import httpx
import pytest
from httpx import AsyncClient
from tests.utils.samples import ExchangeServiceTestSample
from tests.utils.constants import USD_CODE, ILS_CODE, MOCK_EXCHANGE_RATE


class TestExchangeService:

    @pytest.mark.asyncio
    async def test_exchange_get_currency_rate(self, mock_exchange_service):
        currency_rate = await mock_exchange_service.get_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)
        assert currency_rate == MOCK_EXCHANGE_RATE

    @pytest.mark.asyncio
    async def test_exchange_get_same_currency_rate(self, mock_exchange_service):
        currency_rate = await mock_exchange_service.get_currency_rate(from_curr=USD_CODE, to_curr=USD_CODE)
        assert currency_rate == 1.0

    @pytest.mark.asyncio
    async def test_exchange_get_currency_rate_return_float(self, mock_exchange_service):
        currency_rate = await mock_exchange_service.get_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)
        assert isinstance(currency_rate, float)


class TestFrankfurterExchangeService:

    @pytest.mark.asyncio
    async def test_exchange_get_same_currency_rate(self, frankfurter_exchange_service):
        currency_rate = await frankfurter_exchange_service.get_currency_rate(from_curr=USD_CODE, to_curr=USD_CODE)
        assert currency_rate == 1.0

    @pytest.mark.parametrize("rate", ExchangeServiceTestSample.valid_rates_format)
    @pytest.mark.asyncio
    async def test_fetch_currency_rate(self, rate, httpx_mock, frankfurter_exchange_service):
        mock_response_data = {"rates": {"ILS": rate}}
        httpx_mock.add_response(json=mock_response_data)
        async with AsyncClient() as mock_client:
            currency_rate = await frankfurter_exchange_service.fetch_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)

        assert currency_rate == float(rate)

    @pytest.mark.asyncio
    async def test_raise_key_error_fetch_currency_rate(self, httpx_mock, frankfurter_exchange_service, frankfurter_exchange_service_get_key_error):
        with pytest.raises(KeyError, match=".*rates.*"):
            async with AsyncClient() as mock_client:
                await frankfurter_exchange_service.fetch_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)

    @pytest.mark.asyncio
    async def test_raise_http_error_fetch_currency_rate(self, httpx_mock, frankfurter_exchange_service):
        httpx_mock.add_exception(httpx.HTTPError("http error message"))
        async with AsyncClient() as mock_client:
            with pytest.raises(httpx.HTTPError):
                await frankfurter_exchange_service.fetch_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)
