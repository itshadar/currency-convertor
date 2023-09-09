import pytest
from currency_exchange.exchange_http_client import HTTPExchangeClient
from httpx import HTTPError, Response, HTTPStatusError


@pytest.fixture
def mock_http_exchange_client():
    return HTTPExchangeClient(base_url="http://test/")


def mock_fetch_currency_rate(mocker, side_effect):
    """mock the fetch_currency_rate method with different side effect."""
    mocker.patch.object(HTTPExchangeClient, 'fetch_currency_rate', side_effect=side_effect)


class TestHTTPExchangeClient:

    @pytest.mark.asyncio
    async def test_http_status_error_catching(self, mocker, mock_http_exchange_client):
        mocked_response = Response(400, request=None, content="Mocked bad request")
        side_effect = HTTPStatusError(message="Mocked http status error", response=mocked_response, request=None)

        mock_fetch_currency_rate(mocker, side_effect)

        with pytest.raises(ConnectionError):
            async with mock_http_exchange_client:
                await mock_http_exchange_client.fetch_currency_rate("USD", "EUR")

    @pytest.mark.asyncio
    async def test_general_http_error_catching(self, mocker, mock_http_exchange_client):
        side_effect = HTTPError(message="Mocked http error")

        mock_fetch_currency_rate(mocker, side_effect)

        with pytest.raises(ConnectionError):
            async with mock_http_exchange_client:
                await mock_http_exchange_client.fetch_currency_rate("USD", "EUR")

    @pytest.mark.asyncio
    async def test_catching_value_error(self, mock_http_exchange_client):
        with pytest.raises(ValueError):
            async with mock_http_exchange_client:
                raise ValueError
