"""Realistic synthetic flow data so judges/devs can run everything with no API key.

Shapes mirror the real UW REST payloads (see docs/ENDPOINTS.md) so switching to
live data is a one-line change.
"""
from __future__ import annotations

import hashlib
import random
from typing import Dict, List


def _seed_for(ticker: str, base: int) -> int:
    # Deterministic across processes: the builtin hash() is randomized per
    # interpreter (PYTHONHASHSEED), which made the same mock scan return a
    # different alert count on every run — bad for demos and judges.
    digest = hashlib.md5(ticker.encode("utf-8")).hexdigest()
    return base + (int(digest[:8], 16) % 100_000)


def flow_alerts(ticker: str, n: int = 25, seed: int = 7) -> List[Dict]:
    rng = random.Random(_seed_for(ticker, seed))
    events: List[Dict] = []
    for i in range(n):
        side = rng.choice(["call", "call", "put"])
        premium = rng.choice(
            [120_000, 240_000, 480_000, 750_000, 1_200_000, 2_400_000, 5_000_000]
        )
        events.append(
            {
                "id": f"mock-{ticker}-{i}",
                "ticker": ticker,
                "side": side,
                "trade_type": rng.choice(["sweep", "sweep", "block", "single"]),
                "premium": premium,
                "volume": rng.randint(500, 20_000),
                "open_interest": rng.randint(100, 30_000),
                "strike": round(rng.uniform(80, 600), 1),
                "expiry": "2026-11-21",
                "unusual": premium >= 500_000,
            }
        )
    return events


def darkpool(ticker: str, n: int = 15, seed: int = 11) -> List[Dict]:
    rng = random.Random(_seed_for(ticker, seed))
    return [
        {
            "ticker": ticker,
            "premium": rng.uniform(500_000, 8_000_000) * rng.choice([1, -1]),
            "size": rng.randint(5_000, 200_000),
            "side": rng.choice(["buy", "sell"]),
        }
        for _ in range(n)
    ]
