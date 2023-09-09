from abc import abstractmethod, ABC
from typing import Final, Protocol


class IExchangeClient(Protocol):

    async def get_exchange_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """
        """

    async def _get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """
        """

    async def fetch_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """
        """


class ExchangeClientBase(IExchangeClient, ABC):
    """All subclasses of this class can raise ConnectionError / ValueError."""

    SAME_CURR_RATE: Final[float] = 1.0

    def __init_subclass__(cls):
        cls.fetch_currency_rate = cls.check_same_currency(cls.fetch_currency_rate)

    async def get_exchange_currency_rate(self, from_curr: str, to_curr: str) -> float:
        try:
            return await self._get_currency_rate(from_curr, to_curr)

        except ConnectionError as e:
            raise ConnectionError(f"An connection error occurred while fetching the currency rate") from e

        except ValueError as e:
            raise ValueError("Internal Server Error") from e

    @staticmethod
    def check_same_currency(func):
        async def inner(*args, **kwargs):


            if len(args) > 2:
                from_curr_val, to_curr_val = args[1], args[2]

            elif set(["from_curr", "to_curr"]).issubset(kwargs.keys()):
                from_curr_val, to_curr_val = kwargs["from_curr"], kwargs["to_curr"]

            if from_curr_val == to_curr_val:
                return ExchangeClientBase.SAME_CURR_RATE

            return await func(*args, *kwargs)

        return inner

    @abstractmethod
    async def _get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """calls the fetch_currency_rate method. """

    @abstractmethod
    async def fetch_currency_rate(self, from_curr, to_curr) -> float:
        """Fetch the currency rate from a data source. Raise connection error if failed"""
