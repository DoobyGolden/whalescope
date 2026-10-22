"""Thin REST wrapper over the Unusual Whales API.

Paths verified against the public OpenAPI spec (https://api.unusualwhales.com/api/openapi)
on 2026-10-18. Auth: ``Authorization: Bearer <UW_API_KEY>``.

With no key set, every method raises RuntimeError — callers should fall back to
``mock_data`` when ``config.MOCK_MODE`` is True.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from . import config


class UWClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        self.api_key = (api_key or config.UW_API_KEY).strip()
        if not self.api_key:
            raise RuntimeError("UW_API_KEY is not set — use mock_data instead")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "User-Agent": "whalescope-hackathon/0.1",
            }
        )

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = self.session.get(f"{config.BASE_URL}{path}", params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    # --- options flow -----------------------------------------------------
    def flow_alerts(self, ticker: Optional[str] = None, min_premium: Optional[float] = None,
                    unusual: bool = True, limit: int = 100) -> Dict[str, Any]:
        """GET /api/option-trades/flow-alerts"""
        params: Dict[str, Any] = {"unusual": unusual, "limit": limit}
        if ticker:
            params["ticker_symbol"] = ticker
        if min_premium:
            params["min_premium"] = min_premium
        return self._get("/api/option-trades/flow-alerts", params)

    def unusual_activity(self, ticker: Optional[str] = None, min_premium: Optional[float] = None,
                         limit: int = 100) -> Dict[str, Any]:
        """GET /api/option-activity/unusual"""
        params: Dict[str, Any] = {"limit": limit}
        if ticker:
            params["ticker_symbol"] = ticker
        if min_premium:
            params["min_premium"] = min_premium
        return self._get("/api/option-activity/unusual", params)

    def ticker_flow_alerts(self, ticker: str, limit: int = 50) -> Dict[str, Any]:
        """GET /api/stock/{ticker}/flow-alerts"""
        return self._get(f"/api/stock/{ticker}/flow-alerts", {"limit": limit})

    # --- dark pool ---------------------------------------------------------
    def darkpool_recent(self, limit: int = 100, min_premium: Optional[float] = None) -> Dict[str, Any]:
        """GET /api/darkpool/recent"""
        params: Dict[str, Any] = {"limit": limit}
        if min_premium:
            params["min_premium"] = min_premium
        return self._get("/api/darkpool/recent", params)

    def darkpool_ticker(self, ticker: str, limit: int = 50) -> Dict[str, Any]:
        """GET /api/darkpool/{ticker}"""
        return self._get(f"/api/darkpool/{ticker}", {"limit": limit})

    # --- gamma exposure ----------------------------------------------------
    def greek_exposure(self, ticker: str) -> Dict[str, Any]:
        """GET /api/stock/{ticker}/greek-exposure (daily GEX/DEX sums)"""
        return self._get(f"/api/stock/{ticker}/greek-exposure")

    def gex_levels(self, ticker: str) -> Dict[str, Any]:
        """GET /api/stock/{ticker}/gex-levels"""
        return self._get(f"/api/stock/{ticker}/gex-levels")

    # --- volatility ---------------------------------------------------------
    def iv_rank(self, ticker: str, timespan: str = "1Y") -> Dict[str, Any]:
        """GET /api/stock/{ticker}/iv-rank"""
        return self._get(f"/api/stock/{ticker}/iv-rank", {"timespan": timespan})

    def options_pulse(self, ticker: str) -> Dict[str, Any]:
        """GET /api/stock/{ticker}/options-pulse"""
        return self._get(f"/api/stock/{ticker}/options-pulse")

    # --- price history for backtesting --------------------------------------
    def ohlc(self, ticker: str, candle_size: str = "1d", limit: int = 60) -> Dict[str, Any]:
        """GET /api/stock/{ticker}/ohlc/{candle_size}"""
        return self._get(f"/api/stock/{ticker}/ohlc/{candle_size}", {"limit": limit})

    def analytics_window(self, symbols: str, range: str = "30D", interval: str = "1D",
                         calculations: Optional[str] = None) -> Dict[str, Any]:
        """GET /api/analytics/window — fixed-window analytics incl. returns"""
        params: Dict[str, Any] = {"symbols": symbols, "range": range, "interval": interval}
        if calculations:
            params["calculations"] = calculations
        return self._get("/api/analytics/window", params)
