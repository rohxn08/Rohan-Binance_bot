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
Run commands from project root. All commands accept `--testnet/--no-testnet` to override `.env`.

- Market order:
```bash
python src/market_orders.py BTCUSDT BUY 0.01 --leverage 10 --testnet
```

- Limit order:
```bash
python src/limit_orders.py BTCUSDT BUY 0.01 --price 60000 --time-in-force GTC --testnet
```

- Stop-Limit order:
```bash
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 --stop-price 59800 --limit-price 59950 --testnet
```

- OCO emulation (TP + SL):
```bash
python src/advanced/oco.py BTCUSDT SELL 0.01 --take-profit 61000 --stop-loss 59500 --testnet
```

- TWAP strategy:
```bash
python src/advanced/twap.py BTCUSDT BUY 0.1 --slices 10 --interval-sec 30 --testnet
```

- Grid strategy:
```bash
python src/advanced/grid_strategy.py BTCUSDT BUY 0.1 --lower 58000 --upper 62000 --grids 10 --testnet
```

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
│  ├─ limit_orders.py
│  └─ advanced/
│     ├─ stop_limit.py
│     ├─ oco.py
│     ├─ twap.py
│     └─ grid_strategy.py
├─ bot.log
├─ report.pdf
├─ README.md
└─ requirements.txt
```

## Report
Add `report.pdf` with screenshots, explanations, and evaluation notes.

## License
MIT
