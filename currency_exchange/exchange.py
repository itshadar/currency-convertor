from currency_exchange.exchange_client import ExchangeClientBase
from dataclasses import dataclass
from typing_extensions import Self

@dataclass(frozen=True)
class Exchange:

    from_curr: str
    to_curr: str
    currency_rate: float

    @classmethod
    async def create(cls: Self, from_curr: str, to_curr: str, exchange_service: ExchangeClientBase) -> Self:

        currency_rate: float = await exchange_service.get_exchange_currency_rate(from_curr, to_curr)
        self = cls(from_curr, to_curr, currency_rate)
        return self

    def convert_currency(self, amount: float) -> float:
        return amount * self.currency_rate
