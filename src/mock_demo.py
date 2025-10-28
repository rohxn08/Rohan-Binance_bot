import sys
import click
import time
import random
from datetime import datetime

# Add the project root to Python path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import get_logger
from src.utils.validation import OrderInput


logger = get_logger("mock_demo")


@click.command()
@click.argument("symbol")
@click.argument("side")
@click.argument("quantity", type=float)
@click.option("--order-type", type=click.Choice(["MARKET", "LIMIT", "OCO", "TWAP", "GRID"], case_sensitive=False), default="MARKET", help="Type of order to simulate")
@click.option("--price", type=float, help="Price for LIMIT orders")
@click.option("--slices", type=int, default=5, help="Number of slices for TWAP")
@click.option("--grids", type=int, default=5, help="Number of grids for GRID strategy")
def main(symbol: str, side: str, quantity: float, order_type: str, price: float, slices: int, grids: int):
	"""Mock trading demo that simulates successful orders for demonstration.

	Example: python -m src.mock_demo BTCUSDT BUY 0.001 --order-type MARKET
	"""
	try:
		input_data = OrderInput(symbol=symbol, side=side, quantity=quantity)
		if order_type == "LIMIT" and not price:
			raise ValueError("Price is required for LIMIT orders")
	except Exception as e:
		logger.error(f"Validation error: {e}")
		sys.exit(1)

	logger.info(f"Simulating {order_type} {input_data.side} {input_data.quantity} {input_data.symbol}")
	print(f"Simulating {order_type} Order")
	print(f"Symbol: {input_data.symbol}")
	print(f"Side: {input_data.side}")
	print(f"Quantity: {input_data.quantity}")
	print(f"Order Type: {order_type}")
	print("-" * 50)

	try:
		if order_type == "MARKET":
			simulate_market_order(input_data)
		elif order_type == "LIMIT":
			simulate_limit_order(input_data, price)
		elif order_type == "OCO":
			simulate_oco_order(input_data)
		elif order_type == "TWAP":
			simulate_twap_order(input_data, slices)
		elif order_type == "GRID":
			simulate_grid_order(input_data, grids)
		
		print("-" * 50)
		print("Demo completed successfully!")
		logger.info(f"Mock {order_type} order simulation completed")
		
	except Exception as e:
		logger.exception(f"Mock simulation failed: {e}")
		print(f"Demo failed: {e}")
		sys.exit(2)


def simulate_market_order(input_data):
	"""Simulate a market order execution."""
	order_id = random.randint(100000, 999999)
	executed_price = 60000 + random.randint(-1000, 1000)
	executed_qty = input_data.quantity
	commission = executed_qty * executed_price * 0.001  # 0.1% commission
	
	print(f"Market Order Executed")
	print(f"Order ID: {order_id}")
	print(f"Status: FILLED")
	print(f"Executed Qty: {executed_qty}")
	print(f"Executed Price: ${executed_price:,.2f}")
	print(f"Commission: ${commission:.4f}")
	print(f"Total Value: ${executed_qty * executed_price:,.2f}")


def simulate_limit_order(input_data, price):
	"""Simulate a limit order placement."""
	order_id = random.randint(100000, 999999)
	
	print(f"Limit Order Placed")
	print(f"Order ID: {order_id}")
	print(f"Status: NEW")
	print(f"Price: ${price:,.2f}")
	print(f"Quantity: {input_data.quantity}")
	print(f"Time in Force: GTC")
	print(f"Note: Order is waiting to be filled at ${price:,.2f}")


def simulate_oco_order(input_data):
	"""Simulate an OCO order placement."""
	order_list_id = random.randint(100000, 999999)
	limit_price = 60000 + random.randint(-500, 500)
	stop_price = limit_price - 1000
	
	print(f"OCO Order Placed")
	print(f"Order List ID: {order_list_id}")
	print(f"Contingency Type: OCO")
	print(f"List Status: EXECUTED")
	print(f"Limit Price: ${limit_price:,.2f}")
	print(f"Stop Price: ${stop_price:,.2f}")
	print(f"Quantity: {input_data.quantity}")


def simulate_twap_order(input_data, slices):
	"""Simulate a TWAP strategy execution."""
	slice_qty = input_data.quantity / slices
	successful_slices = 0
	
	print(f"TWAP Strategy Started")
	print(f"Total Quantity: {input_data.quantity}")
	print(f"Slices: {slices}")
	print(f"Slice Quantity: {slice_qty}")
	print(f"Interval: 30 seconds")
	print()
	
	for i in range(slices):
		time.sleep(1)  # Simulate delay
		order_id = random.randint(100000, 999999)
		executed_price = 60000 + random.randint(-500, 500)
		
		if random.random() > 0.1:  # 90% success rate
			successful_slices += 1
			print(f"Slice {i+1}/{slices}: {slice_qty} @ ${executed_price:,.2f} - Order ID: {order_id}")
		else:
			print(f"Slice {i+1}/{slices}: Failed")
	
	print()
	print(f"TWAP Summary:")
	print(f"Successful slices: {successful_slices}/{slices}")
	print(f"Success rate: {(successful_slices/slices)*100:.1f}%")


def simulate_grid_order(input_data, grids):
	"""Simulate a grid strategy execution."""
	lower_price = 58000
	upper_price = 62000
	price_range = upper_price - lower_price
	grid_step = price_range / (grids - 1)
	grid_qty = input_data.quantity / grids
	
	print(f"Grid Strategy Started")
	print(f"Price Range: ${lower_price:,.2f} - ${upper_price:,.2f}")
	print(f"Grid Levels: {grids}")
	print(f"Grid Step: ${grid_step:.2f}")
	print(f"Quantity per Grid: {grid_qty}")
	print()
	
	successful_orders = 0
	for i in range(grids):
		grid_price = lower_price + (i * grid_step)
		order_id = random.randint(100000, 999999)
		
		if random.random() > 0.05:  # 95% success rate
			successful_orders += 1
			print(f"Grid {i+1}/{grids}: {grid_qty} @ ${grid_price:,.2f} - Order ID: {order_id}")
		else:
			print(f"Grid {i+1}/{grids}: @ ${grid_price:,.2f} - Failed")
	
	print()
	print(f"Grid Summary:")
	print(f"Successful orders: {successful_orders}/{grids}")
	print(f"Success rate: {(successful_orders/grids)*100:.1f}%")


if __name__ == "__main__":
	main()
