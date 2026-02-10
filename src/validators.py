"""
Input validation helpers for CLI arguments and order parameters.
"""

from dataclasses import dataclass
from typing import Literal


Side = Literal["BUY", "SELL"]
OrderType = Literal["MARKET", "LIMIT", "STOP_LIMIT"]


@dataclass
class OrderInput:
    symbol: str
    side: Side
    order_type: OrderType
    quantity: float
    price: float | None = None
    stop_price: float | None = None


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def _normalize_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s.isalnum():
        raise ValidationError("Symbol must be alphanumeric, e.g. BTCUSDT.")
    if len(s) < 5 or len(s) > 20:
        raise ValidationError("Symbol length must be between 5 and 20 characters.")
    return s


def _normalize_side(side: str) -> Side:
    s = side.strip().upper()
    if s not in ("BUY", "SELL"):
        raise ValidationError("Side must be BUY or SELL.")
    return s  # type: ignore[return-value]


def _normalize_order_type(order_type: str) -> OrderType:
    t = order_type.strip().upper()
    if t not in ("MARKET", "LIMIT", "STOP_LIMIT"):
        raise ValidationError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
    return t  # type: ignore[return-value]


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
) -> OrderInput:
    """
    Validate user-supplied order parameters and return a normalized dataclass.
    """
    norm_symbol = _normalize_symbol(symbol)
    norm_side = _normalize_side(side)
    norm_type = _normalize_order_type(order_type)

    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")

    if norm_type in ("LIMIT", "STOP_LIMIT"):
        if price is None or price <= 0:
            raise ValidationError("Price must be positive for LIMIT and STOP_LIMIT orders.")

    if norm_type == "STOP_LIMIT":
        if stop_price is None or stop_price <= 0:
            raise ValidationError("stop_price must be positive for STOP_LIMIT orders.")

    return OrderInput(
        symbol=norm_symbol,
        side=norm_side,
        order_type=norm_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price,
    )



