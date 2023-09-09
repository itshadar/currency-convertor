from .exchange_http_client import HTTPExchangeClient
from pydantic import BaseModel, ValidationError
from typing import Optional, Final


class FrankfurterJsonResponse(BaseModel):
    amount: Optional[float]
    base: Optional[str]
    date: Optional[str]
    rates: dict[str, float]


class FrankfurterHTTPExchangeClient(HTTPExchangeClient):

    BASE_URL: Final[str] = "https://api.frankfurter.app"

    def __init__(self):
        super().__init__(base_url=FrankfurterHTTPExchangeClient.BASE_URL)

    async def fetch_currency_rate(self, from_curr: str, to_curr: str) -> float:

        response = await self.client.get(f"/latest?from={from_curr}&to={to_curr}")
        response.raise_for_status()

        try:
            json_res = FrankfurterJsonResponse(**response.json())

        except ValidationError as e:
            raise ValueError from e

        return float(json_res.rates[to_curr])
