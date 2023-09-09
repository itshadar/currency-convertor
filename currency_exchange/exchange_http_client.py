from .exchange_client import ExchangeClientBase
from httpx import AsyncClient, HTTPError, HTTPStatusError


class HTTPExchangeClient(ExchangeClientBase):
    """
    All subclasses of this instance can raise HTTPError / Value Error.
    """

    def __init__(self, base_url):
        self.client = AsyncClient(base_url=base_url)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        if exc_type in (HTTPError, HTTPStatusError):
            raise ConnectionError from exc_val

        if exc_type is ValueError:
            raise ValueError from exc_val

        await self.client.aclose()

    async def _get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """Gets the currency rate for Http Async Connection Pool."""
        async with self:
            return await self.fetch_currency_rate(from_curr, to_curr)

    async def fetch_currency_rate(self, from_curr, to_curr) -> float:
        """
        Fetch the currency rate from http request.
        """
