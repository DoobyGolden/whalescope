"""Smoke tests for the alert rules."""
from src import alerts, mock_data


def test_sweep_rule_fires_on_big_unusual_sweep():
    event = {
        "ticker": "NVDA", "side": "call", "trade_type": "sweep",
        "premium": 1_200_000, "volume": 5000, "open_interest": 800,
        "strike": 200.0, "expiry": "2026-11-21", "unusual": True,
    }
    alert = alerts.rule_unusual_sweep(event)
    assert alert is not None and alert.ticker == "NVDA"


def test_sweep_rule_skips_small_prints():
    event = {"ticker": "NVDA", "side": "call", "trade_type": "sweep",
             "premium": 50_000, "unusual": True}
    assert alerts.rule_unusual_sweep(event) is None


def test_darkpool_divergence_fires():
    alert = alerts.rule_darkpool_divergence(flow_sentiment=3_000_000, dp_net=-5_000_000,
                                           ticker="SPY")
    assert alert is not None and alert.bullish is False


def test_darkpool_divergence_skips_aligned():
    assert alerts.rule_darkpool_divergence(3_000_000, 5_000_000, "SPY") is None


def test_scan_runs_on_mock_data():
    events = mock_data.flow_alerts("NVDA", n=25)
    hits = alerts.scan(events)
    assert len(hits) > 0, "mock data should produce at least one sweep alert"


if __name__ == "__main__":
    test_sweep_rule_fires_on_big_unusual_sweep()
    test_sweep_rule_skips_small_prints()
    test_darkpool_divergence_fires()
    test_darkpool_divergence_skips_aligned()
    test_scan_runs_on_mock_data()
    print("all alert tests passed")
