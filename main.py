import anyio
from currency_exchange.exchange import Exchange
from currency_exchange.exchange_frankfurter_http_client import FrankfurterHTTPExchangeClient
from currency_exchange.input_handler import HandleTXTFile, ParsedInput
from currency_exchange.output_emitter import ConsoleOutputEmitter
import typer

app = typer.Typer()


@app.command()
def main(file: str = typer.Option(..., "-f", "--file", help="The file path for the currency exchange file.")):
    anyio.run(run_async, file)


async def run_async(file: str):

    exchange_client = FrankfurterHTTPExchangeClient()
    output_emitter = ConsoleOutputEmitter()
    input_handler = HandleTXTFile()

    parsed_input: ParsedInput = await input_handler.handle_input(file)

    try:
        exchange = await Exchange.create(parsed_input.from_curr, parsed_input.to_curr, exchange_client)
        [output_emitter.emit_output(output=f"{exchange.convert_currency(amount)}\n") for amount in parsed_input.values]

    except (ConnectionError, ValueError) as e:
        output_emitter.emit_output(output=f"Error: {e}")

if __name__ == "__main__":
    app()

