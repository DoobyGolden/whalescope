"""Dashboard: today's unusual-flow scan across the watchlist.

Two views over the same scan, so judges can use whichever fits:

* Text (default) — ``python -m src.dashboard``
* HTML snapshot — ``python -m src.dashboard --html demo/dashboard-preview.html``
  writes a standalone page (inline CSS, no dependencies, no server) with the
  alerts feed plus backtest scorecards. Open it in any browser.

Everything runs in mock mode with synthetic data when no UW_API_KEY is set.
"""
from __future__ import annotations

import argparse
import html
from typing import Dict, List

from . import alerts, config, mock_data


def collect_scan() -> Dict[str, List[alerts.Alert]]:
    """Run the alert rules for every watchlist ticker (mock or live)."""
    scan: Dict[str, List[alerts.Alert]] = {}
    for ticker in config.WATCHLIST:
        if config.MOCK_MODE:
            events = mock_data.flow_alerts(ticker)
        else:
            from . import client as client_mod

            c = client_mod.UWClient()
            data = c.flow_alerts(ticker=ticker, min_premium=config.MIN_SWEEP_PREMIUM)
            events = data.get("data", data if isinstance(data, list) else [])
        scan[ticker] = alerts.scan(events)
    return scan


def render_text(scan: Dict[str, List[alerts.Alert]]) -> str:
    mode = "MOCK (set UW_API_KEY for live)" if config.MOCK_MODE else "LIVE"
    lines = [f"=== WhaleScope scan [{mode}] ==="]
    total = 0
    for ticker in config.WATCHLIST:
        hits = scan.get(ticker, [])
        total += len(hits)
        lines.append(f"\n--- {ticker}: {len(hits)} sweep alerts ---")
        for alert in hits[:5]:
            lines.append(alert.plain_english())
    lines.append(f"\n{total} alerts across {len(config.WATCHLIST)} tickers")
    return "\n".join(lines)


def _bias_label(bullish) -> tuple[str, str]:
    return {True: ("bullish", "🐂 bullish"), False: ("bearish", "🐻 bearish"),
            None: ("neutral", "➖ neutral")}[bullish]


def render_html(scan: Dict[str, List[alerts.Alert]], backtests=None) -> str:
    """Standalone HTML snapshot of a scan (+ optional backtest scorecards)."""
    mode = "MOCK — synthetic data (set UW_API_KEY for live)" if config.MOCK_MODE else "LIVE"
    total = sum(len(v) for v in scan.values())
    sections = []
    for ticker in config.WATCHLIST:
        hits = scan.get(ticker, [])
        rows = []
        for alert in hits:
            cls, label = _bias_label(alert.bullish)
            rows.append(
                "<tr>"
                f"<td><span class='badge {cls}'>{label}</span></td>"
                f"<td>${alert.premium:,.0f}</td>"
                f"<td>{html.escape(alert.headline)}</td>"
                f"<td>{html.escape(alert.detail)}</td>"
                "</tr>"
            )
        body = "".join(rows) or "<tr><td colspan='4'>No alerts for this ticker.</td></tr>"
        sections.append(
            f"<section><h2>{html.escape(ticker)} — {len(hits)} sweep alerts</h2>"
            "<table><thead><tr><th>Bias</th><th>Premium</th><th>Alert</th>"
            f"<th>Detail</th></tr></thead><tbody>{body}</tbody></table></section>"
        )
    backtest_html = ""
    if backtests:
        cards = []
        for result in backtests:
            cards.append(
                "<tr>"
                f"<td>{html.escape(result.ticker)}</td><td>{html.escape(result.rule)}</td>"
                f"<td>{result.trades}</td><td>{result.hit_rate:.0%}</td>"
                f"<td>{result.avg_return_pct:+.1f}%</td>"
                f"<td>{result.best_pct:+.1f}%</td><td>{result.worst_pct:+.1f}%</td>"
                "</tr>"
            )
        backtest_html = (
            "<section><h2>Backtest scorecards — unusual-sweep rule, 5d hold</h2>"
            "<table><thead><tr><th>Ticker</th><th>Rule</th><th>Signals</th>"
            "<th>Hit rate</th><th>Avg return</th><th>Best</th><th>Worst</th></tr></thead>"
            f"<tbody>{''.join(cards)}</tbody></table></section>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>WhaleScope — unusual-flow scan</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 1080px;
         padding: 0 1rem; background: #0b0f14; color: #e6edf3; }}
  h1 {{ margin-bottom: .25rem; }} .mode {{ color: #9fb0c3; margin-top: 0; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }}
  th, td {{ text-align: left; padding: .45rem .6rem; border-bottom: 1px solid #223; vertical-align: top; }}
  th {{ color: #9fb0c3; font-size: .85rem; text-transform: uppercase; letter-spacing: .04em; }}
  .badge {{ padding: .1rem .5rem; border-radius: 999px; font-size: .85rem; white-space: nowrap; }}
  .bullish {{ background: #12351f; color: #4ade80; }} .bearish {{ background: #3a1620; color: #fb7185; }}
  .neutral {{ background: #26303d; color: #cbd5e1; }}
</style>
</head>
<body>
<h1>🐋 WhaleScope — unusual-flow scan</h1>
<p class="mode">{html.escape(mode)} · {total} alerts across {len(config.WATCHLIST)} tickers
({html.escape(', '.join(config.WATCHLIST))} watchlist; sweeps ≥ $500K)</p>
{''.join(sections)}
{backtest_html}
<p class="mode">WhaleScope — agent-native flow scanner + backtest engine on the
Unusual Whales API. Mock data mirrors the real UW REST payload shapes.</p>
</body>
</html>
"""


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="WhaleScope dashboard (mock mode w/o key)")
    parser.add_argument("--html", metavar="PATH",
                        help="also write a standalone HTML snapshot (with backtest scorecards) to PATH")
    args = parser.parse_args(argv)

    scan = collect_scan()
    print(render_text(scan))

    if args.html:
        from . import backtest as backtest_mod

        results = []
        for ticker in config.WATCHLIST:
            results.extend(backtest_mod.run(ticker))
        with open(args.html, "w", encoding="utf-8") as fh:
            fh.write(render_html(scan, backtests=results))
        print(f"\nHTML snapshot written to {args.html}")


if __name__ == "__main__":
    main()
