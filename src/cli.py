"""
Unified CLI entrypoint for the Binance Futures Testnet trading bot.

Usage examples:
    # Market order
    python -m src.cli market BTCUSDT BUY 0.001

    # Limit order
    python -m src.cli limit BTCUSDT SELL 0.001 75000

    # Stop-limit order
    python -m src.cli stop-limit BTCUSDT BUY 0.001 --price 75000 --stop-price 74000

    # TWAP strategy
    python -m src.cli twap BTCUSDT BUY 0.01 --slices 5 --interval 10
"""

from __future__ import annotations

import argparse

from .advanced.stop_limit import place_stop_limit_order
from .advanced.twap import run_twap_strategy
from .limit_orders import place_limit_order
from .logging_config import get_logger, setup_logging
from .market_orders import place_market_order
from .validators import ValidationError


logger = get_logger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Market
    mkt = subparsers.add_parser("market", help="Place a MARKET order.")
    mkt.add_argument("symbol")
    mkt.add_argument("side")
    mkt.add_argument("quantity", type=float)

    # Limit
    lmt = subparsers.add_parser("limit", help="Place a LIMIT order.")
    lmt.add_argument("symbol")
    lmt.add_argument("side")
    lmt.add_argument("quantity", type=float)
    lmt.add_argument("price", type=float)

    # Stop-limit
    sl = subparsers.add_parser("stop-limit", help="Place a STOP_LIMIT order.")
    sl.add_argument("symbol")
    sl.add_argument("side")
    sl.add_argument("quantity", type=float)
    sl.add_argument("--price", type=float, required=True)
    sl.add_argument("--stop-price", type=float, required=True)

    # TWAP
    tw = subparsers.add_parser("twap", help="Run a basic TWAP strategy using MARKET orders.")
    tw.add_argument("symbol")
    tw.add_argument("side")
    tw.add_argument("quantity", type=float)
    tw.add_argument("--slices", type=int, default=5)
    tw.add_argument("--interval", type=int, default=10)

    return parser


def main() -> None:
    setup_logging()
    parser = _build_parser()
    args = parser.parse_args()

    try:
        if args.command == "market":
            resp = place_market_order(args.symbol, args.side, args.quantity)
            print("=== MARKET ORDER ===")
            print(resp)
        elif args.command == "limit":
            resp = place_limit_order(args.symbol, args.side, args.quantity, args.price)
            print("=== LIMIT ORDER ===")
            print(resp)
        elif args.command == "stop-limit":
            resp = place_stop_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
                stop_price=args.stop_price,
            )
            print("=== STOP_LIMIT ORDER ===")
            print(resp)
        elif args.command == "twap":
            responses = run_twap_strategy(
                symbol=args.symbol,
                side=args.side,
                total_quantity=args.quantity,
                slices=args.slices,
                interval_seconds=args.interval,
            )
            print("=== TWAP RESPONSES ===")
            for r in responses:
                print(r)
        else:
            parser.error(f"Unknown command {args.command}")
    except ValidationError as ve:
        logger.error("Validation error: %s", ve, exc_info=True)
        print(f"Validation error: {ve}")
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("CLI command failed: %s", exc)
        print(f"Command failed: {exc}")


if __name__ == "__main__":
    main()



