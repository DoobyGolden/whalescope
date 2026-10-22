# Discord entry post — DO NOT POST (owner's tap)

**Post in:** Unusual Whales Discord → `#vibe-and-api-projects` forum
**Forum link:** https://discord.com/channels/710524439133028512/1525246043460079729
**Title (exact):** `Hackathon1: WhaleScope`
**Check first:** the forum's pinned rules — hackathon trial codes are sometimes posted there.

---

## Post body (copy/paste ready)

**WhaleScope** — an agent-native unusual-flow scanner + backtest engine for
micro-traders, built on the Unusual Whales API.

What it does:
- Scans **unusual options sweeps ($500K+)**, **dark-pool divergence**
  (off-exchange prints moving against the visible flow), and **IV-rank +
  bullish-flow** setups — the signals a small account can actually act on.
- **Backtests every rule** against real price history before a dollar moves —
  replay flow alerts through `/api/analytics/window` and see hit rate, avg
  return, best/worst per ticker.
- Runs three ways: Python CLI, a dashboard, and **plain-English MCP prompts**
  on the official UW MCP server — any agent can drive it.

Why I built it: I run a micro-trading program and kept getting alerts with no
way to know if the rule worked. WhaleScope proves the signal first, then feeds
my live sleeve.

Demo: [LINK DEMO CLIP — record Oct 20, ≤3 min]
GitHub: [LINK REPO — public]

> **Staged locally (Oct 20) — replace the two placeholders above once the
> owner's steps are done:** recording script ready at `demo/DEMO_SCRIPT.md`
> (one take, ≤3 min, mock data, ends on the backtest view); dashboard
> previews already captured at `demo/dashboard-preview.html` and
> `demo/dashboard-preview.png`. Still owner-only: record/upload the clip →
> paste its link on the Demo line; push the repo public → paste its link on
> the GitHub line.

Stack: Python, UW REST API (trial key), official UW MCP server.
Built Oct 18–21, 2026.
