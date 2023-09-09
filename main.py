import anyio
import sys
from currency_exchange.exchange import Exchange
from currency_exchange.exchange_frankfurter_http_client import FrankfurterHTTPExchangeClient
from currency_exchange.input_handler import Arguments
from currency_exchange.input_handler import HandleFile


async def main():

    args = Arguments()
    input_file_path = args.get_file_path()

    from_curr, to_curr, amounts = await HandleFile.handle_input(input_file_path)

    exchange_client = FrankfurterHTTPExchangeClient()

    try:
        exchange = await Exchange.create(from_curr, to_curr, exchange_client)

        # TODO: use for Composite design pattern maybe
        [sys.stdout.write(f"{exchange.convert_currency(amount)}\n") for amount in amounts]

    except (ConnectionError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    anyio.run(main)

