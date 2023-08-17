import anyio
from currency_exchange.exchange import Exchange
from currency_exchange.exchange_client import FrankfurterExchangeService
from currency_exchange.input_handler import Arguments
from currency_exchange.input_handler import HandleFile


async def main():

    args = Arguments()
    input_file_path = args.get_file_path()

    # TODO: Async file handling
    from_curr, to_curr, values = HandleFile.handle_input(input_file_path)

    exchange_service = FrankfurterExchangeService()

    try:
        exchange = await Exchange.create(from_curr, to_curr, exchange_service)
        for value in values:
            print(f"{exchange.convert(value)}")

    except (ConnectionError, KeyError) as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    anyio.run(main)

