"""
CLI for placing LIMIT orders on Binance USDT-M Futures Testnet.

Example:
    python -m src.limit_orders --symbol BTCUSDT --side SELL --quantity 0.001 --price 75000
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from .binance_client import BinanceClient
from .config import load_config
from .logging_config import get_logger, setup_logging
from .validators import ValidationError, validate_order_input


logger = get_logger(__name__)


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
    """
    Validate input and place a LIMIT order (GTC).
    """
    order_input = validate_order_input(
        symbol=symbol,
        side=side,
        order_type="LIMIT",
        quantity=quantity,
        price=price,
    )

    cfg = load_config()
    client = BinanceClient(cfg)

    logger.info(
        "Placing LIMIT order: symbol=%s side=%s qty=%s price=%s",
        order_input.symbol,
        order_input.side,
        order_input.quantity,
        order_input.price,
    )

    response = client.place_order(
        symbol=order_input.symbol,
        side=order_input.side,
        order_type="LIMIT",
        quantity=order_input.quantity,
        price=order_input.price,
        time_in_force="GTC",
    )
    return response


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Place a LIMIT order on Binance Futures Testnet.")
    parser.add_argument("symbol", help="Trading pair symbol, e.g. BTCUSDT.")
    parser.add_argument("side", help="BUY or SELL.")
    parser.add_argument("quantity", type=float, help="Order quantity.")
    parser.add_argument("price", type=float, help="Limit price.")
    return parser


def main() -> None:
    setup_logging()
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        resp = place_limit_order(args.symbol, args.side, args.quantity, args.price)
        print("=== LIMIT ORDER REQUEST ===")
        print(f"Symbol      : {args.symbol}")
        print(f"Side        : {args.side}")
        print(f"Quantity    : {args.quantity}")
        print(f"Price       : {args.price}")
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
        logger.exception("Failed to place LIMIT order: %s", exc)
        print(f"Failed to place LIMIT order: {exc}")


if __name__ == "__main__":
    main()



