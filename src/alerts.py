"""Alert rules engine.

Each rule consumes a flow event (real from UWClient or synthetic from mock_data)
and emits a plain-English alert dict. Rules are deliberately small-account aware:
they target institutional-size prints that a micro-trader can mirror or fade.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from . import config


@dataclass
class Alert:
    rule: str
    ticker: str
    headline: str
    detail: str
    bullish: Optional[bool]  # True=bullish, False=bearish, None=neutral
    premium: float = 0.0

    def plain_english(self) -> str:
        bias = {True: "🐂 bullish", False: "🐻 bearish", None: "➖ neutral"}[self.bullish]
        return f"[{self.rule}] {self.ticker} {bias}\n{self.headline}\n{self.detail}"


def _bullish_from_sides(buy_calls: float, sell_puts: float, buy_puts: float, sell_calls: float) -> bool:
    return (buy_calls + sell_puts) >= (buy_puts + sell_calls)


def rule_unusual_sweep(event: Dict) -> Optional[Alert]:
    """Sweeps >= $500K flagged unusual by UW."""
    premium = float(event.get("premium", 0) or 0)
    if premium < config.MIN_SWEEP_PREMIUM:
        return None
    if not event.get("unusual"):
        return None
    if event.get("trade_type") not in ("sweep", "sweep_buy", "sweep_sell"):
        return None
    side = str(event.get("side", "")).lower()
    bullish = "call" in side or side in ("ask",)  # ask-side prints are typically buys
    return Alert(
        rule="unusual-sweep",
        ticker=event.get("ticker", "?"),
        headline=f"${premium:,.0f} {event.get('side', '')} sweep on the "
        f"{event.get('expiry', '')} ${event.get('strike', '')}s",
        detail=f"Volume {event.get('volume', '?')}x vs open interest {event.get('open_interest', '?')}; "
        f"printed {event.get('trade_type', 'sweep')}. Institutional urgency print.",
        bullish=bullish,
        premium=premium,
    )


def rule_darkpool_divergence(flow_sentiment: float, dp_net: float, ticker: str) -> Optional[Alert]:
    """Dark-pool prints diverging from options-flow sentiment.

    flow_sentiment: net call-buy premium minus put-buy premium (USD, positive = bullish).
    dp_net: net dark-pool premium (USD, positive = lifting the offer / buying).
    """
    if abs(dp_net) < config.MIN_DARKPOOL_PREMIUM:
        return None
    diverges = (flow_sentiment > 0) != (dp_net > 0) and flow_sentiment != 0 and dp_net != 0
    if not diverges:
        return None
    bullish = dp_net > 0  # trust the dark pool over the tape on divergence
    return Alert(
        rule="darkpool-divergence",
        ticker=ticker,
        headline=f"${abs(dp_net):,.0f} dark-pool net {'buying' if dp_net > 0 else 'selling'} "
        f"vs options flow leaning {'bullish' if flow_sentiment > 0 else 'bearish'}",
        detail="Institutions are positioning off-exchange against the visible flow. "
        "Fade the tape, follow the dark pool — size your position for a 1-2 day hold.",
        bullish=bullish,
        premium=abs(dp_net),
    )


def rule_iv_rank_with_bullish_flow(iv_rank: float, ticker: str, bullish_flow: float) -> Optional[Alert]:
    """High IV rank + bullish flow = premium-selling candidates for defined-risk spreads."""
    if iv_rank < 50 or bullish_flow <= 0:
        return None
    return Alert(
        rule="iv-bullish-flow",
        ticker=ticker,
        headline=f"IV rank {iv_rank:.0f} with ${bullish_flow:,.0f} net bullish call premium",
        detail="Volatility is expensive AND smart money is buying upside — defined-risk "
        "bull spreads (not naked longs) capture the edge with capped risk.",
        bullish=True,
        premium=bullish_flow,
    )


RULES: List[Callable[..., Optional[Alert]]] = [
    rule_unusual_sweep,
]


def scan(events: List[Dict]) -> List[Alert]:
    """Run all per-event rules over a list of flow events."""
    alerts: List[Alert] = []
    for event in events:
        for rule in RULES:
            alert = rule(event)
            if alert:
                alerts.append(alert)
    return alerts
