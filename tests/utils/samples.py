from .constants import USD_CODE, ILS_CODE


class HandleFileTestSample:

    file_lines: list[str] = [USD_CODE, ILS_CODE, '3.6', '4', '100', '25']


class ExchangeTestSample:

    rates = [1.2, 0.1, 0.001, 100.0, 21393.1234, 1, 2, 3]


class ExchangeServiceTestSample:

    valid_rates_format: list = ["1.0", 10, "1000.2334", "0.12", "8", 1.7]


class MainTestSample:

    usd_ils_samples = [(USD_CODE, ILS_CODE, [3.6]),
                       (USD_CODE, ILS_CODE, [100, 200, 300]),
                       (USD_CODE, ILS_CODE, [1, 0, 1111.11111, 22222222.2222222222])]

    same_curr_samples = [(USD_CODE, USD_CODE, [100.0, 200]), (ILS_CODE, ILS_CODE, [1, 0])]



