# WhaleScope build plan — finish by Oct 21

Scope guard: the Oct 22–27 Open Agent Hackathon build week is untouchable.
Everything here lands on or before Oct 21.

## Day 0 — Sun Oct 18 (today) ✅ PREP
- [x] Verify hackathon rules + entry mechanics (Substack announcement, live)
- [x] Pull public OpenAPI spec, catalog 225 endpoints (`docs/ENDPOINTS.md`)
- [x] Confirm MCP endpoint + auth shape (Bearer key)
- [x] Scaffold repo: client, alerts engine, backtest harness, mock data, dashboard stub
- [x] Draft Discord entry post (`entry-draft.md`)
- [ ] **OWNER TAP:** sign up for the 7-day API trial at
      https://unusualwhales.com/pricing?product=api
      ($0 today, $150/mo billed after day 7 if not cancelled — cancel by ~Oct 25).
      Trial keys are explicitly allowed for hackathon entry. The earlier the key
      lands, the sooner the live run + demo clip can be recorded. Suggested: Oct 19–20.

## Day 1 — Mon Oct 19: live data + first signals
- [ ] Insert trial key, run scanner against real `/api/option-trades/flow-alerts`
      and `/api/darkpool/recent` for a watchlist (NVDA, SPY, TSLA, AAPL)
- [ ] Tune the three alert rules on live data (premium thresholds, sweep vs block
      classification, bid/ask-side sentiment)
- [ ] Backtest harness: wire `/api/analytics/window` price windows against
      replayed flow alerts for the past 30 trading days on 2 tickers

## Day 2 — Tue Oct 20: dashboard + proof
- [x] Turn `dashboard.py` into a simple web view — shipped as a standalone HTML
      snapshot (`python -m src.dashboard --html <path>`, inline CSS, no server
      or extra dependency) with the full alerts feed + backtest scorecards;
      text CLI unchanged. Mock output made deterministic (stable seeds).
- [x] Capture dashboard previews: `demo/dashboard-preview.html` +
      `demo/dashboard-preview.png` (+ `.txt`); recording script staged at
      `demo/DEMO_SCRIPT.md` (≤3 min, one take, ends on backtest results)
- [ ] Record the demo clip from `demo/DEMO_SCRIPT.md` (owner records; live data
      if the trial key has landed, mock otherwise)
- [ ] Push code to GitHub (repo must be public for the entry post) — OWNER TAP

## Day 3 — Wed Oct 21: polish + entry
- [ ] README demo section with clip + screenshots; final code cleanup
- [ ] Sanity check: mock mode still runs with zero config (judges without keys)
- [ ] **OWNER TAP:** post the entry in Discord `#vibe-and-api-projects`
      (forum: https://discord.com/channels/710524439133028512/1525246043460079729),
      titled **"Hackathon1: WhaleScope"** — text ready in `entry-draft.md`.
      Check the forum's pinned rules first: hackathon trial codes are sometimes
      posted there.

## Entry checklist (Thu Oct 22, 8:59 PM PDT deadline — submitting Oct 21)
- [ ] Public GitHub repo with working code
- [ ] Demo clip (or screenshots) linked in the post
- [ ] Trial key active and working at entry time

## What judges see (pitch)
"WhaleScope is an agent-native scanner that turns Unusual Whales flow data into
micro-trader alerts — unusual sweeps over $500K, dark-pool divergence, GEX
levels — and backtests every rule against real price history before a dollar
moves. It runs as Python, as a dashboard, and as plain-English MCP prompts, so
any AI agent can drive it. Built to feed a real live micro-trading program."
