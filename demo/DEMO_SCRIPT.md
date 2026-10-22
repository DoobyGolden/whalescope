# WhaleScope — demo recording script (≤3 minutes, one take)

**Format:** screen recording, terminal + one browser tab. Mock data throughout —
say so on camera (line is in the narration). Everything below is deterministic:
the commands print the exact numbers quoted here, every run.

**Before you hit record (2 min setup, off camera):**
1. Open a terminal in the project folder (`unusual-whales/`).
2. Run once off camera: `pip install -r requirements.txt`
3. Make sure no key is set so it records in mock mode: `unset UW_API_KEY`
   (or just don't create a `.env` — no `.env` = mock mode).
4. Pre-open `demo/dashboard-preview.html` in a browser tab — you'll regenerate
   it live in Shot 3, this is only a fallback.
5. Font size up (terminal ~16pt+), window ~1280×720. Start recording.

---

## Shot list + narration (verbatim)

### Shot 1 — Hook (0:00–0:20) · Screen: terminal, empty prompt
> "This is WhaleScope — an agent-native scanner for the Unusual Whales API.
> It turns unusual options flow into plain-English alerts a micro-trader can
> actually act on — and then it backtests every rule before a dollar moves.
> This demo runs on synthetic mock data, so anyone can reproduce it. No API
> key needed."

### Shot 2 — The scan (0:20–1:05) · Type and run:
```
python -m src.dashboard
```
Screen shows: `=== WhaleScope scan [MOCK (set UW_API_KEY for live)] ===`, then
per-ticker sections — NVDA 12 alerts, SPY 7, TSLA 7, AAPL 5,
`31 alerts across 4 tickers`. Scroll slowly to the top of the NVDA section.
> "One command scans my watchlist — NVDA, SPY, TSLA, AAPL. Thirty-one alerts.
> The rule firing here is the unusual sweep: Unusual Whales-flagged sweeps of
> five hundred thousand dollars or more. Anything smaller never reaches me —
> that's the small-account filter."

### Shot 3 — One alert, walked through (1:05–1:40) · Screen: stay on the first NVDA alert
The first alert on screen reads:
`$750,000 call sweep on the 2026-11-21 $548.0s — Volume 4740x vs open interest 6892`
> "Take the first one. Seven hundred fifty thousand dollars, call sweep,
> November twenty-first expiry, five-forty-eight strike. Volume forty-seven
> forty against open interest of sixty-eight ninety-two — somebody wanted in
> now, not later. Every alert reads like this: the print, the size, and why
> it matters, in plain English. Two more rules sit next to it — dark-pool
> divergence, and IV-rank with bullish flow — same format, same feed. And
> because it's plain text, any AI agent can read it, rank it, and act on it."

### Shot 4 — The dashboard view (1:40–2:10) · Type and run:
```
python -m src.dashboard --html demo/dashboard-preview.html
```
Then switch to the browser tab and refresh `demo/dashboard-preview.html`.
Scroll from the header (`31 alerts across 4 tickers`) down one ticker table.
> "Same scan, as a dashboard. The HTML view renders the full feed — every
> alert with its bias, premium, and detail — no server, no dependencies,
> just one file a judge can open. Scroll to the bottom and you'll find the
> part I care about most."

### Shot 5 — Backtest results — END HERE (2:10–2:55) · Type and run:
```
python -m src.backtest --ticker NVDA --days 30
```
Screen shows exactly:
`[unusual-sweep] NVDA: 14 signals, hit rate 93%, avg 5d return +13.2% (best +21.2% / worst -2.5%)`
Leave this line on screen while you close.
> "An alert with no track record is just noise — so WhaleScope replays the
> rule. Fourteen NVDA signals over thirty days, ninety-three percent hit
> rate, plus thirteen point two percent average five-day return in mock
> replay. In live mode, the same harness pulls real price windows from the
> Unusual Whales analytics endpoints — set one environment variable,
> UW_API_KEY, and the whole thing goes live. Scanner, dashboard, backtest,
> and plain-English MCP prompts on the official Unusual Whales MCP server.
> That's WhaleScope. Prove the signal first — then trade it."

**Stop recording on the backtest line.** Total ≈ 2:55 at a natural pace.

---

## If a take goes wrong
- Wrong numbers on screen? You have a stale checkout — the mock data is
  seeded deterministically, so the counts above (31 alerts; NVDA backtest
  14 / 93% / +13.2%) must match exactly. Re-pull the project folder and retry.
- Want the other tickers' scorecards for B-roll (same deterministic output):
  SPY 9 signals / 67% / +6.8% · TSLA 13 / 77% / +11.4% · AAPL 9 / 78% / +5.4%
  via `python -m src.backtest --ticker SPY --days 30` (etc.).
- Sanity check any time: `python -m pytest tests/ -v` → `5 passed`.
