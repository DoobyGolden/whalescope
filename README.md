# WhaleScope — Unusual-Whales agent-native flow scanner + backtest engine

**Entry for the Unusual Whales Hackathon** (submissions close Thu Oct 22, 8:59 PM PDT).
Post in Discord `#vibe-and-api-projects`, titled **"Hackathon1: WhaleScope"** — see `entry-draft.md`.

## What it is

An agent-native build on the Unusual Whales API:

1. **Flow scanner** — unusual options flow alerts, dark-pool divergence, GEX level
   alerts, IV-rank + bullish-flow combos — the exact signals a micro-trader needs,
   delivered as plain-English alerts an AI agent can act on.
2. **Backtest harness** — replays flow-alert history against real price action via
   the UW analytics endpoints, so a signal is *proven* before money touches it.
3. **MCP-ready** — the same scanner logic is exposed through the official
   Unusual Whales MCP server (`https://api.unusualwhales.com/api/mcp`), so any
   agent (Claude, ChatGPT, Codex, Cursor) can run it in plain English.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env        # add your UW_API_KEY (trial keys work for the hackathon)
python -m src.dashboard    # scan today's unusual flow (mock mode if no key)
python -m src.dashboard --html demo/dashboard-preview.html   # standalone HTML view + backtest scorecards
python -m src.backtest --ticker NVDA --days 30   # backtest the sweep rule
python -m pytest tests/ -v   # 5 tests, all mock mode
```

Demo evidence staged in `demo/`: `DEMO_SCRIPT.md` (≤3-min recording script),
`dashboard-preview.html` / `dashboard-preview.png` (mock-mode captures —
the scan is seeded deterministically, so they reproduce exactly).

No key yet? Everything runs in **mock mode** with realistic synthetic flow data,
so judges and devs can explore the full logic offline. Set `UW_API_KEY` to go live.

## Build status

See `BUILD_PLAN.md` for the day-by-day plan through Oct 21. Live-key integration
points are stubbed against the real UW REST paths (verified against the public
OpenAPI spec, Oct 18 2026) — one env var flip takes the scanner live.

## Terms note

UW API data is for personal use (no redistribution). This repo ships code only —
no UW data is included, and API keys are never committed.
