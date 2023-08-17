import pytest
from currency_exchange.exchange import Exchange
from tests.utils.samples import ExchangeTestSample
from tests.utils.constants import USD_CODE, ILS_CODE

# TODO:
class TestExchange:

    @pytest.mark.parametrize("rate", ExchangeTestSample.rates)
    def test_exchange_currency_rate_convert(self, rate, mock_exchange_service):

        amount = 100.0
        exchange = Exchange(from_curr=USD_CODE, to_curr=ILS_CODE, currency_rate=rate,
                            exchange_service=mock_exchange_service)
        assert rate * amount == exchange.convert(amount)

    @pytest.mark.asyncio
    async def test_exchange_same_currency_conversion(self, usd_usd_mock_currency_exchange):

        usd_usd_mock_currency_exchange = await usd_usd_mock_currency_exchange
        amount = 100.0
        converted_amount = usd_usd_mock_currency_exchange.convert(amount)
        assert converted_amount == amount

    @pytest.mark.asyncio
    async def test_exchange_currency_conversion(self, usd_ils_mock_currency_exchange):

        usd_ils_mock_currency_exchange = await usd_ils_mock_currency_exchange
        amount = 100.0
        converted_amount = usd_ils_mock_currency_exchange.convert(amount)
        assert converted_amount == usd_ils_mock_currency_exchange.currency_rate * amount
