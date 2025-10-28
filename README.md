# Binance USDT-M Futures Order Bot

A CLI-based trading bot for Binance USDT-M Futures supporting market, limit, and advanced order strategies (stop-limit, OCO emulation, TWAP, grid). Includes robust validation and structured logging.

## Features
- Market and limit orders with validation
- Advanced strategies: Stop-Limit, OCO (emulated), TWAP, Grid
- Centralized logging to `bot.log` with timestamps and error traces
- Testnet toggle and `.env` based credentials

## Requirements
- Python 3.10+
- See `requirements.txt`

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in project root with your keys:
```env
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
BINANCE_FUTURES_TESTNET=true  # set to false for mainnet
LOG_LEVEL=INFO
```

## Usage

### Working Demo (No API Keys Required)
Test all order types with simulated trading:
```bash
# Market order simulation
python -m src.mock_demo BTCUSDT BUY 0.001 --order-type MARKET

# TWAP strategy simulation
python -m src.mock_demo BTCUSDT BUY 0.001 --order-type TWAP --slices 5

# Grid strategy simulation
python -m src.mock_demo BTCUSDT BUY 0.001 --order-type GRID --grids 5

# OCO order simulation
python -m src.mock_demo BTCUSDT BUY 0.001 --order-type OCO

# Limit order simulation
python -m src.mock_demo BTCUSDT BUY 0.001 --order-type LIMIT --price 60000
```

### Live Trading (Requires API Keys with Trading Permissions)
Run commands from project root. All commands accept `--testnet/--no-testnet` to override `.env`.

- Futures Market order:
```bash
python -m src.market_orders BTCUSDT BUY 0.01 --leverage 10 --testnet
```

**Note:** Live trading requires API keys with Futures trading permissions enabled on Binance.

## Notes
- This bot is for educational use. Use Binance Futures Testnet for testing.
- OCO is emulated via separate TP/SL orders with cancel-on-fill logic.
- Ensure your symbol and step sizes match Binance filters.

## Project Structure
```
project_root/
├─ src/
│  ├─ utils/
│  │  ├─ client.py
│  │  ├─ logger.py
│  │  └─ validation.py
│  ├─ market_orders.py
│  └─ mock_demo.py
├─ bot.log
├─ README.md
└─ requirements.txt
```

## Report
Add `report.pdf` with screenshots, explanations, and evaluation notes.

## License
MIT
