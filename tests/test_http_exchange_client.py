import pytest
from currency_exchange.exchange_http_client import HTTPExchangeClient
from httpx import HTTPError, Response, Request, HTTPStatusError, MockTransport, AsyncClient
from pytest_mock import mocker


@pytest.fixture
def mock_http_exchange_client():
    return MockHTTPExchangeClient(base_url="http://test/")


class MockHTTPExchangeClient(HTTPExchangeClient):

    async def fetch_currency_rate(self, from_curr, to_curr):
        pass


class TestHTTPExchangeClient:

    @pytest.mark.asyncio
    async def test_http_status_error_catching(self, mocker, mock_http_exchange_client):

        # Mock the fetch_currency_rate method to always raise HTTPStatusError"""
        mocked_response = Response(400, request=None, content="Mocked bad request")
        mocker.patch.object(MockHTTPExchangeClient, 'fetch_currency_rate',
                            side_effect=HTTPStatusError(message="Mocked http status error", response=mocked_response, request=None))

        with pytest.raises(ConnectionError):
            async with mock_http_exchange_client as client:
                await client.fetch_currency_rate("USD", "EUR")

    @pytest.mark.asyncio
    async def test_general_http_error_catching(self, mocker, mock_http_exchange_client):
        # Mock the fetch_currency_rate method to always raise HTTPError"""

        mocker.patch.object(MockHTTPExchangeClient, 'fetch_currency_rate',
                            side_effect=HTTPError(message="Mocked http status error"))

        with pytest.raises(ConnectionError):
            async with mock_http_exchange_client as client:
                await client.fetch_currency_rate("USD", "EUR")

    @pytest.mark.asyncio
    async def test_catching_value_error(self, mock_http_exchange_client):
        with pytest.raises(ValueError):
            async with mock_http_exchange_client:
                raise ValueError
