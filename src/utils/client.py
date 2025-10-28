import os
from binance.um_futures import UMFutures
from dotenv import load_dotenv


def get_futures_client(testnet: bool | None = None) -> UMFutures:
	"""Create and return a Binance USDT-M Futures client using env vars.

	If testnet is True, uses testnet base URL.
	"""
	load_dotenv()
	api_key = os.getenv("BINANCE_API_KEY", "")
	api_secret = os.getenv("BINANCE_API_SECRET", "")
	if not api_key or not api_secret:
		raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment/.env")

	if testnet is None:
		testnet = os.getenv("BINANCE_FUTURES_TESTNET", "true").lower() == "true"

	base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
	return UMFutures(key=api_key, secret=api_secret, base_url=base_url)
