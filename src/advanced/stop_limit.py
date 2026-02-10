"""
CLI for placing STOP_LIMIT-like orders on Binance USDT-M Futures Testnet.

Implementation detail:
- Uses Binance Futures STOP or STOP_MARKET type via the standard order endpoint.

Example:
    python -m src.advanced.stop_limit BTCUSDT BUY 0.001 --price 75000 --stop-price 74000
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from ..binance_client import BinanceClient
from ..config import load_config
from ..logging_config import get_logger, setup_logging
from ..validators import ValidationError, validate_order_input


logger = get_logger(__name__)


def place_stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
) -> Dict[str, Any]:
    """
    Validate input and place a STOP_LIMIT-like order.
    On Binance Futures this is done via type=STOP with price + stopPrice.
    """
    order_input = validate_order_input(
        symbol=symbol,
        side=side,
        order_type="STOP_LIMIT",
        quantity=quantity,
        price=price,
        stop_price=stop_price,
    )

    cfg = load_config()
    client = BinanceClient(cfg)

    logger.info(
        "Placing STOP_LIMIT order: symbol=%s side=%s qty=%s price=%s stop_price=%s",
        order_input.symbol,
        order_input.side,
        order_input.quantity,
        order_input.price,
        order_input.stop_price,
    )

    response = client.place_order(
        symbol=order_input.symbol,
        side=order_input.side,
        order_type="STOP",
        quantity=order_input.quantity,
        price=order_input.price,
        stop_price=order_input.stop_price,
        time_in_force="GTC",
    )
    return response


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place a STOP_LIMIT order on Binance Futures Testnet."
    )
    parser.add_argument("symbol", help="Trading pair symbol, e.g. BTCUSDT.")
    parser.add_argument("side", help="BUY or SELL.")
    parser.add_argument("quantity", type=float, help="Order quantity.")
    parser.add_argument("--price", type=float, required=True, help="Limit price.")
    parser.add_argument(
        "--stop-price",
        type=float,
        required=True,
        help="Stop trigger price.",
    )
    return parser


def main() -> None:
    setup_logging()
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        resp = place_stop_limit_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
        print("=== STOP_LIMIT ORDER REQUEST ===")
        print(f"Symbol      : {args.symbol}")
        print(f"Side        : {args.side}")
        print(f"Quantity    : {args.quantity}")
        print(f"Price       : {args.price}")
        print(f"Stop Price  : {args.stop_price}")
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
        logger.exception("Failed to place STOP_LIMIT order: %s", exc)
        print(f"Failed to place STOP_LIMIT order: {exc}")


if __name__ == "__main__":
    main()



