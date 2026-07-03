from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolBudget:
    tool: str
    calls: int
    tokens: int
    cost_usd: float
    p95_latency_ms: int
    note: str


def load_calls(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, math.ceil((pct / 100) * len(ordered)) - 1)
    return ordered[index]


def summarize(calls: list[dict], latency_target_ms: int, cost_budget: float) -> list[ToolBudget]:
    buckets: dict[str, list[dict]] = {}
    for call in calls:
        buckets.setdefault(str(call.get("tool", "unknown")), []).append(call)
    budgets: list[ToolBudget] = []
    for tool, rows in buckets.items():
        tokens = sum(int(row.get("tokens", 0) or 0) for row in rows)
        cost = sum(float(row.get("cost_usd", 0.0) or 0.0) for row in rows)
        p95 = percentile([int(row.get("latency_ms", 0) or 0) for row in rows], 95)
        notes = []
        if p95 > latency_target_ms:
            notes.append("latency target missed")
        if cost > cost_budget:
            notes.append("cost budget exceeded")
        if len(rows) > 5:
            notes.append("cache candidate")
        budgets.append(ToolBudget(tool, len(rows), tokens, cost, p95, "; ".join(notes) or "within budget"))
    return sorted(budgets, key=lambda item: (-item.cost_usd, item.tool))


def render_table(budgets: list[ToolBudget]) -> str:
    lines = ["tool\tcalls\ttokens\tcost_usd\tp95_ms\tnote"]
    for budget in budgets:
        lines.append(
            f"{budget.tool}\t{budget.calls}\t{budget.tokens}\t{budget.cost_usd:.4f}\t"
            f"{budget.p95_latency_ms}\t{budget.note}"
        )
    return "\n".join(lines) + "\n"


def render_json(budgets: list[ToolBudget]) -> str:
    return json.dumps([asdict(budget) for budget in budgets], indent=2)
