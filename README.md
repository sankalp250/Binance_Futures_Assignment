## Binance Futures Testnet Trading Bot (CLI)

Python trading bot for Binance **USDT-M Futures Testnet** (`https://testnet.binancefuture.com`), implementing:

- **Market** and **Limit** orders (core requirement)
- **Stop-Limit-like** orders (via Futures `STOP` order with limit price)
- **TWAP** (Time-Weighted Average Price) strategy using repeated market orders
- **Unified CLI** with validation, logging, and error handling

### 1. Setup

- **Python**: 3.10+ recommended
- **Clone repo**:

```bash
git clone https://github.com/sankalp250/Binance_Futures_Assignment.git
cd Binance_Futures_Assignment
```

- **Install dependencies**:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

- **Set Binance Testnet API keys** (USDT-M Futures):

  1. Copy the example file:

     ```bash
     cp env.example .env   # on Windows PowerShell: copy env.example .env
     ```

  2. Edit `.env` and fill in your **testnet** API key and secret:

     ```env
     BINANCE_API_KEY=your_testnet_api_key
     BINANCE_API_SECRET=your_testnet_api_secret
     ```

  These are read by the app through `src/config.py`. The real `.env` is **git‑ignored** so that secrets are never committed.

### 2. Project Structure

```
[project_root]/
├── src/
│   ├── __init__.py
│   ├── binance_client.py      # REST client wrapper for Futures Testnet
│   ├── config.py              # API key loading, base URL
│   ├── logging_config.py      # Central logging to bot.log
│   ├── validators.py          # Input validation and normalization
│   ├── market_orders.py       # MARKET order CLI and logic
│   ├── limit_orders.py        # LIMIT order CLI and logic
│   ├── cli.py                 # Unified CLI with subcommands
│   └── advanced/
│       ├── __init__.py
│       ├── stop_limit.py      # STOP_LIMIT-like orders (STOP + limit)
│       └── twap.py            # TWAP strategy using repeated MARKET orders
├── historical_data.csv        # Provided data (optional for further work)
├── requirements.txt
├── README.md
└── bot.log                    # Created automatically when you run the bot
```

> **Note**: `report.pdf` is not generated in this environment; you can export a report (with screenshots of CLI runs and explanation) from this README or your own notes into PDF.

### 3. Running Core Orders (Direct Modules)

From the project root (ensure your virtualenv is activated):

#### 3.1 MARKET order

```bash
python -m src.market_orders BTCUSDT BUY 0.001
```

#### 3.2 LIMIT order

```bash
python -m src.limit_orders BTCUSDT SELL 0.001 75000
```

Both commands will:

- Validate inputs (symbol format, side, quantity, price)
- Place an order on **Binance Futures Testnet** (`/fapi/v1/order`)
- Print a clear summary including `orderId`, `status`, `executedQty`, `avgPrice` (if available)
- Log request and response details (and any errors) to `bot.log`

### 4. Advanced Orders & Strategies

#### 4.1 STOP-LIMIT-like order

Uses Futures **STOP** order with `price` (limit) and `stopPrice` (trigger):

```bash
python -m src.advanced.stop_limit BTCUSDT BUY 0.001 --price 75000 --stop-price 74000
```

#### 4.2 TWAP strategy

Split a larger order into multiple **MARKET** orders over time:

```bash
python -m src.advanced.twap BTCUSDT BUY 0.01 --slices 5 --interval 10
```

- `--slices`: number of chunks (orders)
- `--interval`: seconds between each order

All slices and responses are logged to `bot.log`.

### 5. Unified CLI (Recommended UX)

Instead of calling each module separately, you can use the unified CLI:

```bash
python -m src.cli market BTCUSDT BUY 0.001
python -m src.cli limit BTCUSDT SELL 0.001 75000
python -m src.cli stop-limit BTCUSDT BUY 0.001 --price 75000 --stop-price 74000
python -m src.cli twap BTCUSDT BUY 0.01 --slices 5 --interval 10
```

The CLI:

- Uses subcommands (`market`, `limit`, `stop-limit`, `twap`)
- Validates inputs and prints a concise summary/result
- Logs all actions and errors

### 6. Logging

- Logs are written to `bot.log` in the project root.
- Format:

  `YYYY-MM-DD HH:MM:SS | LEVEL | logger.name | message`

- Includes:
  - Request path and parameters (excluding raw signatures)
  - Response HTTP status and body
  - Validation errors
  - Exceptions with stack traces

> To satisfy the assignment requirement of **one MARKET** and **one LIMIT** order log:
> - Run one `market` and one `limit` command as shown above.
> - Submit the resulting `bot.log` together with the repository.

### 7. Assumptions

- You already have a working **Binance USDT-M Futures Testnet** account and API keys.
- Symbols like `BTCUSDT` are already enabled and margin available on the testnet account.
- Network connectivity to `https://testnet.binancefuture.com` is available when you run the bot.

### 8. GitHub & Submission

- This repo (`Binance_Futures_Assignment`) contains all source code under `src/`.
- After testing locally:

```bash
git add .
git commit -m "Implement Binance Futures Testnet trading bot"
git push origin main  # or master, depending on your default branch
```

Include:

- `bot.log` with at least one MARKET and one LIMIT order
- This `README.md`
- Optionally, a `report.pdf` (screenshots and design explanation) for the extended assignment.


