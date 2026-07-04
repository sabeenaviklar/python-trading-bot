# Binance Futures Testnet Trading Bot

A Python CLI application to place orders (Market, Limit, Stop Market) on the Binance Futures Testnet (USDT-M).

## Features
- **Place Orders**: Supports Market, Limit, and Stop Market orders.
- **Both Sides**: Supports BUY (Long) and SELL (Short).
- **Interactive CLI**: Enhanced user experience with interactive prompts, colorful tables, and confirmations using `click` and `rich`.
- **Structured Code**: Clean separation between API interactions and CLI logic.
- **Robust Validation**: Pre-validates user input before making API calls.
- **Detailed Logging**: Logs API requests, responses, and errors to `trading_bot.log`.

## Setup Steps

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
   You can run the script and it will prompt you for your API credentials and optionally save them to a `.env` file for future use. Alternatively, create a `.env` file in the root directory:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```

## How to Run Examples

Navigate to the `trading_bot` directory:
```bash
cd trading_bot
```

### Interactive Mode (Prompts for inputs)
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
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 90000
```

**3. Stop Market Order (Sell 0.01 BTC when price drops to 50,000 USDT):**
```bash
python cli.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.01 --stop-price 50000
```

## Logs
All actions, API responses, and errors are saved into `trading_bot/trading_bot.log`.

## Assumptions
- Designed explicitly for **Binance Futures Testnet (USDT-M)**. Spot trading or mainnet usage will require modifying `testnet=True` or switching endpoints.
- Assumes valid quantity precision and price tick sizes as provided by Binance; standard API errors will be caught and logged if invalid amounts are submitted.
