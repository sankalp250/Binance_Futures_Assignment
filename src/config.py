"""
Configuration utilities for the Binance Futures Testnet trading bot.

API credentials are read from environment variables or a local .env file:
- BINANCE_API_KEY
- BINANCE_API_SECRET
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv  # type: ignore[import]


@dataclass
class BinanceConfig:
    api_key: str
    api_secret: str
    base_url: str = "https://testnet.binancefuture.com"
    recv_window: int = 5_000


def load_config() -> BinanceConfig:
    # Load .env once (safe to call repeatedly; it’s idempotent)
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        raise RuntimeError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in the environment "
            "or in a .env file in the project root."
        )

    return BinanceConfig(api_key=api_key, api_secret=api_secret)



