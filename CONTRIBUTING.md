# Contributing

Thanks for helping improve immune-crystal.

## Local Setup

```bash
pip install -e .
uvicorn api.app:app --reload
```

```bash
cd web
npm install
npm run dev
```

## Before Opening a PR

Run the checks that match your change:

```bash
python -m compileall core api benchmarks examples
python benchmarks/pollution_intercept.py
python benchmarks/memory_repair.py
python benchmarks/audit_latency.py
```

```bash
cd web
npm run build
```

## PR Checklist

- Explain the scenario and expected behavior.
- Include a minimal reproduction payload when changing API behavior.
- Update README or docs when changing public workflows.
- Keep API compatibility unless the change is explicitly breaking.

## Commit Style

Use short, action-oriented messages:

- `Add domain profile export`
- `Fix audit latency regression`
- `Update enterprise evaluation guide`

## Issue Template

Include:

- Use case
- Current behavior
- Expected behavior
- Sample request/response
- Environment details
