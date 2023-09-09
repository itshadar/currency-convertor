import pytest
from currency_exchange.exchange import Exchange
from tests.utils.constants import USD_CODE, ILS_CODE
from tests.conftest import mock_exchange_client


class TestExchange:

    @pytest.mark.asyncio
    async def test_exchange_same_currency_conversion(self, mock_exchange_client):

        exchange = await Exchange.create(USD_CODE, USD_CODE, mock_exchange_client)
        amount = 100.0
        excepted_convert_amounts = amount
        actual_convert_amounts = exchange.convert_currency(amount)
        assert actual_convert_amounts == excepted_convert_amounts

    @pytest.mark.asyncio
    async def test_exchange_currency_conversion(self, mock_exchange_client):

        exchange = await Exchange.create(USD_CODE, ILS_CODE, mock_exchange_client)
        amount = 100.0
        actual_convert_amounts = exchange.convert_currency(amount)
        excepted_convert_amounts = amount * mock_exchange_client.MOCK_RATE
        assert actual_convert_amounts == excepted_convert_amounts
