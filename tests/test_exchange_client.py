import pytest
from tests.conftest import mock_exchange_client
from currency_exchange.exchange_client import ExchangeClientBase
from tests.utils.constants import USD_CODE, ILS_CODE


class TestExchangeClient:

    def test_args_order_of_fetch_currency_rate(self):
        args = ExchangeClientBase.fetch_currency_rate.__code__.co_varnames
        excepted_args_orders = (("from_curr", "to_curr"), ("to_curr", "from_curr"))
        actual_args_order = args[1:3]
        assert actual_args_order in excepted_args_orders

    @pytest.mark.asyncio
    async def test_exchange_get_same_currency_rate(self, mock_exchange_client):
        actual_currency_rate = await mock_exchange_client.get_exchange_currency_rate(from_curr=USD_CODE, to_curr=USD_CODE)
        excepted_rate = 1.0
        assert actual_currency_rate == excepted_rate

    @pytest.mark.asyncio
    async def test_exchange_get_currency_rate(self, mock_exchange_client):
        actual_currency_rate = await mock_exchange_client.get_exchange_currency_rate(from_curr=USD_CODE, to_curr=ILS_CODE)
        excepted_rate = mock_exchange_client.MOCK_RATE
        assert actual_currency_rate == excepted_rate
