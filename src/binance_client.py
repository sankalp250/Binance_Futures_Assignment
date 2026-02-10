"""
Lightweight Binance USDT-M Futures Testnet REST client.

Implements signed order endpoints using HMAC SHA256.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from .config import BinanceConfig
from .logging_config import get_logger


logger = get_logger(__name__)


class BinanceApiError(Exception):
    """Represents an error response from the Binance API."""

    def __init__(self, status_code: int, code: Optional[int], msg: str):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        super().__init__(f"Binance API error {status_code} (code={code}): {msg}")


class BinanceClient:
    """
    Minimal REST client for Binance USDT-M Futures Testnet.
    Supports placing MARKET, LIMIT, and STOP_LIMIT orders.
    """

    def __init__(self, config: BinanceConfig, session: Optional[requests.Session] = None):
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.config.api_key})

    def _sign_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign parameters using the exact same ordering/encoding that will be
        sent to Binance.

        We rely on `urlencode` so that the query string used for signing
        matches what `requests` will generate for the GET/POST params.
        """
        query = urlencode(params, doseq=True)
        signature = hmac.new(
            self.config.api_secret.encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(
        self, path: str, params: Dict[str, Any], signed: bool = True
    ) -> Dict[str, Any]:
        url = f"{self.config.base_url}{path}"
        params = dict(params)
        params.setdefault("timestamp", int(time.time() * 1000))
        params.setdefault("recvWindow", self.config.recv_window)

        if signed:
            params = self._sign_params(params)

        logger.info("POST %s params=%s", path, {k: v for k, v in params.items() if k != "signature"})
        resp = self.session.post(url, params=params, timeout=10)
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text}

        logger.info("RESPONSE %s status=%s body=%s", path, resp.status_code, data)

        if resp.status_code >= 400 or ("code" in data and data.get("code", 0) != 0):
            raise BinanceApiError(
                status_code=resp.status_code,
                code=data.get("code"),
                msg=str(data.get("msg") or data),
            )

        return data

    # Public methods -----------------------------------------------------

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: Optional[str] = None,
        stop_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Place a futures order (MARKET, LIMIT, or STOP / STOP_LIMIT-like).
        """
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if price is not None:
            params["price"] = price

        if time_in_force is not None:
            params["timeInForce"] = time_in_force

        if stop_price is not None:
            params["stopPrice"] = stop_price

        return self._post("/fapi/v1/order", params=params, signed=True)



