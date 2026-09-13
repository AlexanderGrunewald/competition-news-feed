import pytest

from src.parser.tavily_parser import CompetitorSearchEngine


@pytest.fixture
def engine(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "dummy-key-for-tests")
    return CompetitorSearchEngine()


@pytest.fixture
def captured_search(engine, monkeypatch):
    """Replace the inherited TavilyClient.search with a spy that records kwargs."""
    calls = {}

    def fake_search(**kwargs):
        calls.update(kwargs)
        return {"results": []}

    monkeypatch.setattr(engine, "search", fake_search)
    return engine, calls


def test_init_requires_api_key(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    with pytest.raises(ValueError):
        CompetitorSearchEngine()


def test_init_accepts_explicit_api_key(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    engine = CompetitorSearchEngine(api_key="explicit-key")
    assert engine.api_key == "explicit-key"


def test_monitor_competitor_builds_default_query(captured_search):
    engine, calls = captured_search
    engine.monitor_competitor("Makita")

    assert calls["query"] == '"Makita" new power tool accessories'
    assert calls["exact_match"] is True
    assert calls["time_range"] == "y"
    assert calls["search_depth"] == "advanced"
    assert calls["max_results"] == 10


def test_monitor_competitor_custom_query_overrides_default(captured_search):
    engine, calls = captured_search
    engine.monitor_competitor("Makita", custom_query="Makita battery recall")

    assert calls["query"] == "Makita battery recall"


def test_monitor_competitor_filters_unknown_kwargs(captured_search):
    engine, calls = captured_search
    engine.monitor_competitor("Makita", max_results=5, not_a_real_param="x")

    assert calls["max_results"] == 5
    assert "not_a_real_param" not in calls


def test_monitor_competitor_ignores_none_valued_kwargs(captured_search):
    engine, calls = captured_search
    engine.monitor_competitor("Makita", max_results=None)

    # None should be filtered out, leaving the default of 10 in place
    assert calls["max_results"] == 10


def test_monitor_competitor_start_date_drops_time_range(captured_search):
    engine, calls = captured_search
    engine.monitor_competitor("Makita", start_date="2026-01-01")

    assert "time_range" not in calls
    assert calls["start_date"] == "2026-01-01"
