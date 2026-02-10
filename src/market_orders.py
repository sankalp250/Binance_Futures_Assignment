"""
CLI for placing MARKET orders on Binance USDT-M Futures Testnet.

Example:
    python -m src.market_orders --symbol BTCUSDT --side BUY --quantity 0.001
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from .binance_client import BinanceClient
from .config import load_config
from .logging_config import get_logger, setup_logging
from .validators import ValidationError, validate_order_input


logger = get_logger(__name__)


def place_market_order(symbol: str, side: str, quantity: float) -> Dict[str, Any]:
    """
    Validate input and place a MARKET order.
    """
    order_input = validate_order_input(
        symbol=symbol,
        side=side,
        order_type="MARKET",
        quantity=quantity,
    )

    cfg = load_config()
    client = BinanceClient(cfg)

    logger.info(
        "Placing MARKET order: symbol=%s side=%s qty=%s",
        order_input.symbol,
        order_input.side,
        order_input.quantity,
    )

    response = client.place_order(
        symbol=order_input.symbol,
        side=order_input.side,
        order_type="MARKET",
        quantity=order_input.quantity,
    )
    return response


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Place a MARKET order on Binance Futures Testnet.")
    parser.add_argument("symbol", help="Trading pair symbol, e.g. BTCUSDT.")
    parser.add_argument("side", help="BUY or SELL.")
    parser.add_argument("quantity", type=float, help="Order quantity.")
    return parser


def main() -> None:
    setup_logging()
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        resp = place_market_order(args.symbol, args.side, args.quantity)
        print("=== MARKET ORDER REQUEST ===")
        print(f"Symbol      : {args.symbol}")
        print(f"Side        : {args.side}")
        print(f"Quantity    : {args.quantity}")
        print("=== RESPONSE ===")
        print(f"orderId     : {resp.get('orderId')}")
        print(f"status      : {resp.get('status')}")
        print(f"executedQty : {resp.get('executedQty')}")
        print(f"avgPrice    : {resp.get('avgPrice')}")
        print("Result      : SUCCESS")
    except ValidationError as ve:
        logger.error("Validation error: %s", ve, exc_info=True)
        print(f"Validation error: {ve}")
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to place MARKET order: %s", exc)
        print(f"Failed to place MARKET order: {exc}")


if __name__ == "__main__":
    main()



