from __future__ import annotations

import argparse
from pathlib import Path

from tool_call_budgeter.core import load_calls, render_json, render_table, summarize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize agent tool-call budgets from JSONL traces.")
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--latency-target-ms", type=int, default=1000)
    parser.add_argument("--cost-budget", type=float, default=0.05)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    budgets = summarize(load_calls(args.jsonl), args.latency_target_ms, args.cost_budget)
    print(render_json(budgets) if args.json else render_table(budgets), end="")
    return 0
