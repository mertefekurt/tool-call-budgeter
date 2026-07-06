# Tool Call Budgeter

Summarize latency, token, and cost budgets from agent tool-call traces.

![Tool Call Budgeter cover](assets/readme-cover.svg)

## What the report is for

Use it when a trace feels slow or expensive and you want a small table that says where the budget went.

```bash
git clone https://github.com/mertefekurt/tool-call-budgeter.git
cd tool-call-budgeter
python -m pip install -e ".[dev]"
tool-call-budgeter examples/tools.jsonl --latency-target-ms 1200 --cost-budget 0.10
```

## Maintainer checks

```bash
ruff check .
pytest
python -m tool_call_budgeter --help
```
