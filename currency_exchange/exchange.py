from currency_exchange.exchange_service import ExchangeService
from dataclasses import dataclass


@dataclass
class Exchange:

    from_curr: str
    to_curr: str
    currency_rate: float
    exchange_service: ExchangeService

    @classmethod
    async def create(cls, from_curr: str, to_curr: str, exchange_service: ExchangeService):
        currency_rate: float = await exchange_service.get_currency_rate(from_curr, to_curr)
        self = cls(from_curr, to_curr, currency_rate, exchange_service)
        return self

    def convert(self, value: float):
        return value * self.currency_rate
