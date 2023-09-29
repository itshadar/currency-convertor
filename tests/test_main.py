import pytest
import main
from tests.utils.constants import USD_CODE, ILS_CODE
from currency_exchange.exchange import Exchange
from currency_exchange.input_handler import ParsedInput


class TestMain:

    @pytest.mark.asyncio
    async def test_run_async_success(self, mocker, capsys):

        mocked_handle_input = mocker.patch('currency_exchange.input_handler.HandleTXTFile.handle_input',
                                           new_callable=mocker.AsyncMock,
                                           return_value=ParsedInput(from_curr=USD_CODE, to_curr=ILS_CODE, values=[100, 200]))

        mock_exchange = mocker.MagicMock(spec=Exchange)
        mock_exchange.convert_currency.side_effect = lambda x: x * 3.5
        mocker.patch('currency_exchange.exchange.Exchange.create', return_value=mock_exchange)

        # Call the function
        await main.run_async('fake_file_path')

        # Check the captured output
        captured = capsys.readouterr()
        excepted_out = "350.0\n700.0\n"
        assert excepted_out == captured.out

        # Ensure the mock methods were called
        mocked_handle_input.assert_called_once_with('fake_file_path')
        mock_exchange.convert_currency.assert_has_calls([mocker.call(100), mocker.call(200)])
