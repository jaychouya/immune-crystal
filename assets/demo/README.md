# Demo Asset Guide

Expected file:

```text
assets/demo/immune-crystal-demo.gif
```

## Generated Storyboard (repo default)

This repo ships `immune-crystal-demo.gif` built by `scripts/generate_demo_gif.py` (Pillow). Regenerate after edits:

```bash
pip install -e ".[dev]"
python scripts/generate_demo_gif.py
```

For a **screen recording** of the live API/dashboard, follow below.

## Recommended Flow

Record a 60-90 second demo:

1. Start API and web dashboard.
2. Bootstrap sample domains.
3. Trigger a cross-domain pollution request.
4. Show `blocked=true` with reason.
5. Run a safe query and show `purity`, `lineage`, and `audit_id`.
6. Open the audit stream.

## Recording Tips

- Use 1200px width for GitHub readability.
- Keep the clip under 10 MB if possible.
- Blur real company data and secrets.
- Prefer a single uninterrupted flow.

## README Integration

After adding the GIF, replace the placeholder in `README.md` and `README.zh-CN.md` with:

```markdown
![immune-crystal demo](./assets/demo/immune-crystal-demo.gif)
```
