# Binance Futures Testnet Trading Bot

This is a Python CLI application built to interact with the Binance Futures Testnet (USDT-M). It allows you to place various types of orders from the command line while keeping track of API interactions.

## Features
- Places **Market, Limit, and Stop Market** orders on the testnet.
- Supports both **BUY (Long)** and **SELL (Short)** directions.
- I've added an interactive CLI built with `click` and `rich` to make inputs easier to read and validate before placing orders.
- Code is split between the core API logic (`bot/`) and the command-line interface (`cli.py`).
- Saves logs of all API interactions to `trading_bot.log`.
- Includes a `--dry-run` flag so you can test the CLI without hitting the Binance API.

## How to Set It Up

1. **Clone the repository or extract the folder.**

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **API Credentials:**
   You can either let the script prompt you for your keys, or create a `.env` file in the root directory like this:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```

## Running the Bot

Note: If you are running this from the root directory, you can just execute `python trading_bot/cli.py`.

### Interactive Mode
```bash
python cli.py
```

### CLI Arguments Mode
You can also pass arguments directly:

**1. Market Order (Buy 0.01 BTC):**
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

**2. Limit Order (Sell 0.01 BTC at 90,000 USDT):**
```bash
python trading_bot/cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 90000
```

**3. Stop Market Order (Sell 0.01 BTC when price drops to 50,000 USDT):**
```bash
python cli.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.01 --stop-price 50000
```

## Logs
Check `trading_bot.log` in the root folder for a history of API responses and orders.

## A Few Assumptions
- The bot is hardcoded to connect to the Binance Futures Testnet. It won't work on the mainnet unless you change `testnet=True` in `client.py`.
- It relies on standard Binance exceptions for catching things like invalid tick sizes or missing funds.
