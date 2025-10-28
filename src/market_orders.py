import sys
import time
import click

from src.utils.client import get_futures_client
from src.utils.logger import get_logger
from src.utils.validation import OrderInput


logger = get_logger("market_orders")


@click.command()
@click.argument("symbol")
@click.argument("side")
@click.argument("quantity", type=float)
@click.option("--leverage", type=int, default=None, help="Optional leverage to set before order")
@click.option("--reduce-only", is_flag=True, default=False, help="Use reduceOnly flag")
@click.option("--testnet/--no-testnet", default=None, help="Override testnet setting")
@click.option("--position-side", type=click.Choice(["BOTH", "LONG", "SHORT"], case_sensitive=False), default="BOTH")
@click.option("--recv-window", type=int, default=5000)
def main(symbol: str, side: str, quantity: float, leverage: int | None, reduce_only: bool, testnet: bool | None, position_side: str, recv_window: int):
	"""Place a MARKET order on Binance USDT-M Futures.

	Example: python -m src.market_orders BTCUSDT BUY 0.01 --leverage 10 --testnet
	"""
	try:
		input_data = OrderInput(symbol=symbol, side=side, quantity=quantity)
	except Exception as e:
		logger.error(f"Validation error: {e}")
		sys.exit(1)

	client = get_futures_client(testnet=testnet)
	logger.info(f"Placing MARKET {input_data.side} {input_data.quantity} {input_data.symbol} | testnet={testnet}")

	try:
		if leverage:
			logger.info(f"Setting leverage={leverage} for {input_data.symbol}")
			client.change_leverage(symbol=input_data.symbol, leverage=leverage, recvWindow=recv_window)

		resp = client.new_order(
			symbol=input_data.symbol,
			side=input_data.side,
			type="MARKET",
			quantity=input_data.quantity,
			reduceOnly=reduce_only,
			positionSide=position_side.upper(),
			recvWindow=recv_window,
		)
		logger.info(f"Order response: {resp}")
		print(resp)
	except Exception as e:
		logger.exception(f"Failed to place market order: {e}")
		sys.exit(2)


if __name__ == "__main__":
	main()
