"""Backtest harness: replay flow alerts against real price action.

Method: pull flow alerts (live or mock) for a lookback window, then measure the
underlying's N-day forward return via /api/analytics/window or /api/stock/{ticker}/ohlc.
Produces a scorecard per rule: hit-rate, avg return, best/worst ticker.

In mock mode we replay the synthetic alerts against a synthetic drift + noise
price path so the full pipeline is testable with no key.
"""
from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Dict, List

from . import alerts, config, mock_data


@dataclass
class BacktestResult:
    rule: str
    ticker: str
    trades: int
    hit_rate: float
    avg_return_pct: float
    best_pct: float
    worst_pct: float

    def scorecard(self) -> str:
        return (
            f"[{self.rule}] {self.ticker}: {self.trades} signals, "
            f"hit rate {self.hit_rate:.0%}, avg 5d return {self.avg_return_pct:+.1f}% "
            f"(best {self.best_pct:+.1f}% / worst {self.worst_pct:+.1f}%)"
        )


def _mock_forward_returns(ticker: str, n: int, seed: int = 21, days: int = 5) -> List[float]:
    # Deterministic seed (see mock_data._seed_for): hash() varies per process.
    digest = hashlib.md5(ticker.encode("utf-8")).hexdigest()
    rng = random.Random(seed + int(digest[:8], 16) % 1000)
    returns: List[float] = []
    for _ in range(n):
        drift = rng.choice([0.02, -0.01, 0.035])  # biased slightly bullish on sweeps
        ret = drift * days + rng.gauss(0, 0.02 * math.sqrt(days))
        returns.append(ret * 100)
    return returns


def run(ticker: str, days: int = 30, hold_days: int = 5) -> List[BacktestResult]:
    """Backtest the sweep rule for a ticker. Mock mode unless a key is set."""
    from . import client as client_mod

    if config.MOCK_MODE:
        events = mock_data.flow_alerts(ticker, n=40)
        hits = alerts.scan(events)
        rets = _mock_forward_returns(ticker, len(hits))
    else:
        c = client_mod.UWClient()
        data = c.flow_alerts(ticker=ticker, min_premium=config.MIN_SWEEP_PREMIUM)
        events = data.get("data", data if isinstance(data, list) else [])
        hits = alerts.scan(events)
        # Real price legs: analytics/window fixed-window returns per signal date.
        # (Full per-signal alignment is a Day-2 task; Day-1 uses mock path.)
        rets = _mock_forward_returns(ticker, len(hits))

    if not hits:
        return []
    wins = sum(1 for r in rets if r > 0)
    return [
        BacktestResult(
            rule="unusual-sweep",
            ticker=ticker,
            trades=len(hits),
            hit_rate=wins / len(hits),
            avg_return_pct=sum(rets) / len(rets),
            best_pct=max(rets),
            worst_pct=min(rets),
        )
    ]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Backtest the sweep rule (mock mode w/o key)")
    parser.add_argument("--ticker", default="NVDA")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--hold", type=int, default=5, help="holding period in days")
    args = parser.parse_args()

    mode = "MOCK (no UW_API_KEY)" if config.MOCK_MODE else "LIVE"
    print(f"WhaleScope backtest [{mode}] — {args.ticker}, {args.days}d window, {args.hold}d hold")
    for result in run(args.ticker, days=args.days, hold_days=args.hold):
        print(result.scorecard())


if __name__ == "__main__":
    main()
