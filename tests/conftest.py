import pytest
from typing import Final
from currency_exchange.exchange_client import ExchangeClientBase


class MockExchangeClientBase(ExchangeClientBase):

    MOCK_RATE: Final[float] = 3.5

    async def _get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        return await self.fetch_currency_rate(from_curr, to_curr)

    async def fetch_currency_rate(self, from_curr: str, to_curr: str) -> float:
        return MockExchangeClientBase.MOCK_RATE


@pytest.fixture
def mock_exchange_client():
    return MockExchangeClientBase()
