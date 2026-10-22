# Unusual Whales endpoints used by WhaleScope

Verified 2026-10-18 against the public spec at
`https://api.unusualwhales.com/api/openapi` (225 paths). Base: `https://api.unusualwhales.com`,
auth `Authorization: Bearer <UW_API_KEY>`.

## Core scanner

| Endpoint | Purpose | Key params |
|---|---|---|
| `GET /api/option-trades/flow-alerts` | UW-flagged flow alerts | `ticker_symbol`, `unusual`, `min_premium`, `max_premium`, `min_size`, `min_volume` |
| `GET /api/option-activity/unusual` | Market-wide unusual options activity | `ticker_symbol`, `min_premium`, `max_dte`, `issue_types[]` |
| `GET /api/stock/{ticker}/flow-alerts` | Per-ticker flow alerts | `limit`, `is_ask_side`, `is_bid_side` |
| `GET /api/stock/{ticker}/flow-recent` | Recent flows | `side`, `min_premium` |

## Dark pool

| Endpoint | Purpose |
|---|---|
| `GET /api/darkpool/recent` | Recent prints, filterable by `min_premium`/`min_size` |
| `GET /api/darkpool/{ticker}` | Per-ticker prints |
| `GET /api/darkpool/{ticker}/price-levels` | Lit/off-lit volume per price level |

## Gamma + volatility context

| Endpoint | Purpose |
|---|---|
| `GET /api/stock/{ticker}/greek-exposure` | Daily GEX/DEX sums |
| `GET /api/stock/{ticker}/gex-levels` | GEX levels by strike |
| `GET /api/stock/{ticker}/spot-exposures/strike` | Per-strike spot GEX |
| `GET /api/stock/{ticker}/iv-rank` | IV rank (`timespan=1Y`) |
| `GET /api/stock/{ticker}/options-pulse` | Per-ticker pulse score |
| `GET /api/options-pulse/top` | Market-wide pulse scanner |

## Backtest price legs

| Endpoint | Purpose |
|---|---|
| `GET /api/stock/{ticker}/ohlc/{candle_size}` | OHLC candles for forward-return math |
| `GET /api/analytics/window` | Fixed-window analytics (`symbols`, `range`, `interval`, `calculations`) |
| `GET /api/stock/{ticker}/option-contract/{id}/historic` | Contract history |

## MCP server

Official endpoint: `https://api.unusualwhales.com/api/mcp` with
`Authorization: Bearer <redacted>`. 100+ typed tools mirroring the REST API
(flow alerts, dark pool, GEX, congress, prediction markets, screeners) —
any MCP client (Claude Desktop/Code, ChatGPT, Cursor, VS Code, Windsurf) can
drive WhaleScope's scans in plain English.

## Data-shop note

Bulk historical datasets (flow, OHLC, dark pool, GEX) are available for
purchase for deeper backtests — out of hackathon scope; the API's 2-year
lookback is enough.
