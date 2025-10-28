from __future__ import annotations

from pydantic import BaseModel, field_validator


class OrderInput(BaseModel):
	symbol: str
	side: str  # BUY or SELL
	quantity: float
	price: float | None = None
	stop_price: float | None = None
	limit_price: float | None = None
	leverage: int | None = None
	tif: str | None = None  # GTC/IOC/FOK

	@field_validator("side")
	@classmethod
	def validate_side(cls, v: str) -> str:
		v_up = v.upper()
		if v_up not in {"BUY", "SELL"}:
			raise ValueError("side must be BUY or SELL")
		return v_up

	@field_validator("symbol")
	@classmethod
	def validate_symbol(cls, v: str) -> str:
		if not v or not v.endswith("USDT"):
			raise ValueError("symbol must be like BTCUSDT, ETHUSDT, etc.")
		return v.upper()

	@field_validator("quantity")
	@classmethod
	def validate_qty(cls, v: float) -> float:
		if v <= 0:
			raise ValueError("quantity must be > 0")
		return v

	@field_validator("price", "stop_price", "limit_price")
	@classmethod
	def validate_prices(cls, v: float | None):
		if v is not None and v <= 0:
			raise ValueError("price values must be > 0")
		return v
