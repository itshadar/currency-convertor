from currency_exchange.exchange_client import ExchangeService
from .constants import MOCK_EXCHANGE_RATE


class ExchangeServiceMock(ExchangeService):

    async def fetch_currency_rate(self, from_curr, to_curr):
        return MOCK_EXCHANGE_RATE

