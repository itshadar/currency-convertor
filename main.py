import anyio
import sys
from currency_exchange.exchange import Exchange
from currency_exchange.exchange_frankfurter_http_client import FrankfurterHTTPExchangeClient
from currency_exchange.input_handler import HandleFile
import typer

app = typer.Typer()


@app.command()
def main(file: str = typer.Option(..., "-f", "--file", help="The file path for the currency exchange file.")):
    anyio.run(run_async, file)


async def run_async(file: str):

    input_file_path = file

    from_curr, to_curr, amounts = await HandleFile.handle_input(input_file_path)

    exchange_client = FrankfurterHTTPExchangeClient()

    try:
        exchange = await Exchange.create(from_curr, to_curr, exchange_client)
        [sys.stdout.write(f"{exchange.convert_currency(amount)}\n") for amount in amounts]
    except (ConnectionError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()

