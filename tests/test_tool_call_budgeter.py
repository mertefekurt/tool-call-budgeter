from __future__ import annotations

import json

from tool_call_budgeter.cli import main
from tool_call_budgeter.core import percentile, render_json, render_table, summarize

CALLS = [
    {"tool": "search", "latency_ms": 100, "tokens": 10, "cost_usd": 0.01},
    {"tool": "search", "latency_ms": 900, "tokens": 20, "cost_usd": 0.02},
    {"tool": "db", "latency_ms": 50, "tokens": 0, "cost_usd": 0.0},
]


def test_percentile() -> None:
    assert percentile([1, 2, 100], 95) == 100


def test_summarize_groups_by_tool() -> None:
    assert summarize(CALLS, 500, 1)[0].tool == "search"


def test_latency_note() -> None:
    assert "latency" in summarize(CALLS, 50, 1)[0].note


def test_table_contains_header() -> None:
    assert render_table(summarize(CALLS, 500, 1)).startswith("tool")


def test_json_render() -> None:
    assert json.loads(render_json(summarize(CALLS, 500, 1)))[0]["tool"] == "search"


def test_empty_trace() -> None:
    assert summarize([], 10, 1) == []


def test_cli_help(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "tool-call" in capsys.readouterr().out
