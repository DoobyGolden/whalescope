"""Config: API key from environment, mock-mode flag when no key is set."""
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is optional
    pass

UW_API_KEY: str = os.getenv("UW_API_KEY", "").strip()
BASE_URL = "https://api.unusualwhales.com"
MCP_URL = "https://api.unusualwhales.com/api/mcp"
MOCK_MODE: bool = not UW_API_KEY

# Micro-trader defaults: small-account friendly thresholds.
WATCHLIST = [t.strip() for t in os.getenv("WHALESCOPE_TICKERS", "NVDA,SPY,TSLA,AAPL").split(",")]
MIN_SWEEP_PREMIUM = float(os.getenv("WHALESCOPE_MIN_SWEEP_PREMIUM", "500000"))  # $500K+
MIN_DARKPOOL_PREMIUM = float(os.getenv("WHALESCOPE_MIN_DARKPOOL_PREMIUM", "1000000"))  # $1M+
