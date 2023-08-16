from currency_exchange.exchange_service import ExchangeService
from dataclasses import dataclass
from typing_extensions import Self

# TODO: Change to regular class
# TODO: Make class reusable with @setter.property (when changing from/to_curr)
@dataclass
class Exchange:

    from_curr: str
    to_curr: str
    currency_rate: float
    exchange_service: ExchangeService

    @classmethod
    async def create(cls: Self, from_curr: str, to_curr: str, exchange_service: ExchangeService) -> Self:
        currency_rate: float = await exchange_service.get_currency_rate(from_curr, to_curr)
        self = cls(from_curr, to_curr, currency_rate, exchange_service)
        return self

    # TODO: change naming with function and param(value)
    def convert(self, value: float) -> float:
        return value * self.currency_rate
