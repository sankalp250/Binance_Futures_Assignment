"""
Simple TWAP (Time-Weighted Average Price) strategy for Binance Futures Testnet.

Splits a larger desired quantity into N smaller MARKET orders spaced over time.

Example:
    python -m src.advanced.twap BTCUSDT BUY 0.01 --slices 5 --interval 10
"""

from __future__ import annotations

import argparse
import time
from typing import Any, Dict, List

from ..binance_client import BinanceClient
from ..config import load_config
from ..logging_config import get_logger, setup_logging
from ..validators import ValidationError, validate_order_input


logger = get_logger(__name__)


def run_twap_strategy(
    symbol: str,
    side: str,
    total_quantity: float,
    slices: int,
    interval_seconds: int,
) -> List[Dict[str, Any]]:
    """
    Run a basic TWAP strategy by submitting a sequence of MARKET orders.
    """
    if slices <= 0:
        raise ValidationError("slices must be a positive integer.")
    if interval_seconds < 0:
        raise ValidationError("interval must be non-negative.")

    per_order_qty = total_quantity / slices
    validate_order_input(
        symbol=symbol,
        side=side,
        order_type="MARKET",
        quantity=per_order_qty,
    )

    cfg = load_config()
    client = BinanceClient(cfg)

    logger.info(
        "Starting TWAP: symbol=%s side=%s total_qty=%s slices=%s interval=%ss "
        "(per_order_qty=%s)",
        symbol,
        side,
        total_quantity,
        slices,
        interval_seconds,
        per_order_qty,
    )

    responses: List[Dict[str, Any]] = []
    for i in range(slices):
        logger.info("TWAP slice %s/%s: placing MARKET order qty=%s", i + 1, slices, per_order_qty)
        resp = client.place_order(
            symbol=symbol,
            side=side,
            order_type="MARKET",
            quantity=per_order_qty,
        )
        responses.append(resp)
        if i < slices - 1 and interval_seconds > 0:
            time.sleep(interval_seconds)

    logger.info("Completed TWAP with %s slices.", slices)
    return responses


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a basic TWAP strategy using MARKET orders on Binance Futures Testnet."
    )
    parser.add_argument("symbol", help="Trading pair symbol, e.g. BTCUSDT.")
    parser.add_argument("side", help="BUY or SELL.")
    parser.add_argument("quantity", type=float, help="Total quantity to execute.")
    parser.add_argument(
        "--slices",
        type=int,
        default=5,
        help="Number of slices (orders) to split the total quantity into.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Seconds to wait between each order.",
    )
    return parser


def main() -> None:
    setup_logging()
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        responses = run_twap_strategy(
            symbol=args.symbol,
            side=args.side,
            total_quantity=args.quantity,
            slices=args.slices,
            interval_seconds=args.interval,
        )
        print("=== TWAP REQUEST ===")
        print(f"Symbol        : {args.symbol}")
        print(f"Side          : {args.side}")
        print(f"Total qty     : {args.quantity}")
        print(f"Slices        : {args.slices}")
        print(f"Interval (s)  : {args.interval}")
        print("=== RESPONSES PER SLICE ===")
        for idx, resp in enumerate(responses, start=1):
            print(f"[Slice {idx}] orderId={resp.get('orderId')}, status={resp.get('status')}, "
                  f"executedQty={resp.get('executedQty')}, avgPrice={resp.get('avgPrice')}")
        print("Result        : SUCCESS")
    except ValidationError as ve:
        logger.error("Validation error in TWAP: %s", ve, exc_info=True)
        print(f"Validation error: {ve}")
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to run TWAP strategy: %s", exc)
        print(f"Failed to run TWAP strategy: {exc}")


if __name__ == "__main__":
    main()



