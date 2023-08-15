from abc import ABC, abstractmethod
from typing import Final
import httpx

class ExchangeService(ABC):

    SAME_CURR_RATE: Final[float] = 1.0

    async def get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """"Get the currency rate."""
        if from_curr == to_curr:
            return ExchangeService.SAME_CURR_RATE
        else:
            try:
                return await self.fetch_currency_rate(from_curr, to_curr)
            except httpx.HTTPError:
                raise ConnectionError(f"An http error occurred while fetching the currency rate")
            except KeyError:
                raise KeyError("Internal Server Error")


    @abstractmethod
    async def fetch_currency_rate(self, from_curr, to_curr):
        """Fetch the currency rate from a data source."""


class FrankfurterExchangeService(ExchangeService):

    async def fetch_currency_rate(self, from_curr: str, to_curr: str) -> float:

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.frankfurter.app/latest?from={from_curr}&to={to_curr}")

            response.raise_for_status()
            response_data = response.json()
            return float(response_data["rates"][to_curr])

        except (httpx.HTTPError, KeyError) as e:
            raise e
