import pytest
from main import main
from tests.utils.constants import MOCK_EXCHANGE_RATE
from currency_exchange.input_handler import HandleFile
from tests.utils.samples import MainTestSample


class TestMain:

    @staticmethod
    def excepted_print_out(values, currency_rate):
        return "".join([f"{float(value) * currency_rate}\n" for value in values[HandleFile.VALUES_INDEX]])

    @pytest.mark.parametrize("parsed_input", MainTestSample.usd_ils_samples)
    @pytest.mark.asyncio
    async def test_usd_ils_convertor(self, mocker, capsys, mock_exchange_service, mock_main_arguments, parsed_input):

        self.patch_mock_main(mocker, mock_exchange_service, parsed_input)
        await main()

        out, err = capsys.readouterr()
        assert out == TestMain.excepted_print_out(parsed_input, MOCK_EXCHANGE_RATE)

    @pytest.mark.parametrize("parsed_input", MainTestSample.same_curr_samples)
    @pytest.mark.asyncio
    async def test_same_curr_convertor(self, mocker, capsys, mock_exchange_service, mock_main_arguments, parsed_input):

        TestMain.patch_mock_main(mocker, mock_exchange_service, parsed_input)
        await main()

        out, err = capsys.readouterr()
        assert out == TestMain.excepted_print_out(parsed_input, 1.0)

    @staticmethod
    def patch_mock_main(mocker, mock_exchange_service, parsed_input):
        mocker.patch('main.FrankfurterExchangeService', return_value=mock_exchange_service)
        mock_handle_file = mocker.patch('main.HandleFile')
        mock_handle_file.handle_input.return_value = parsed_input