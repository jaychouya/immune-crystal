# immune-crystal

[![CI](https://github.com/jaychouya/immune-crystal/actions/workflows/ci.yml/badge.svg)](https://github.com/jaychouya/immune-crystal/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-22c55e)](#roadmap)
[![Enterprise](https://img.shields.io/badge/Focus-Enterprise%20AI-7c3aed)](#enterprise-use-cases)

English | [简体中文](./README.zh-CN.md)

General-purpose Enterprise AI Immune-Memory Symbiote: a defensive memory layer that combines dynamic domain isolation with periodic time-crystal self-repair.

> Build enterprise AI that is safe, stateful, and auditable.

## One-Minute Demo

![immune-crystal demo](./assets/demo/immune-crystal-demo.gif)

Storyboard walkthrough (~60s). To reproduce locally: `python examples/generic/bootstrap_and_chat.py`. Regenerate GIF: `pip install -e ".[dev]"` then `python scripts/generate_demo_gif.py`. Full recording checklist: [`assets/demo/README.md`](./assets/demo/README.md).

## What You Get

- Domain-agnostic isolation (`customer_support`, `engineering`, `hr`, `finance`, etc.)
- Cross-domain leakage and prompt-injection interception
- Periodic memory reinforcement and noise decay
- Full audit signals on each response: `purity`, `lineage`, `audit_id`

## Proof Signals

| Signal | Where |
| --- | --- |
| Legal use | [`LICENSE`](./LICENSE) |
| Security disclosure | [`SECURITY.md`](./SECURITY.md) |
| Contribution path | [`CONTRIBUTING.md`](./CONTRIBUTING.md) |
| Release history | [`CHANGELOG.md`](./CHANGELOG.md) |
| Enterprise PoC checklist | [`docs/enterprise-evaluation.md`](./docs/enterprise-evaluation.md) |

## Comparison (vs RAG / Guardrails)

| Capability | Vanilla RAG | Guardrails-only | immune-crystal |
| --- | --- | --- | --- |
| Cross-domain isolation | Partial | Partial | Strong |
| Prompt injection resistance | Weak | Strong | Strong |
| Long-session memory self-repair | Weak | None | Strong |
| Conflict-state handling | Weak | Rule-based | Dynamic quarantine phase |
| Output traceability | Medium | Medium | Strong (`purity` + `lineage`) |

## 5-Minute Integration

### 1) Inject domain knowledge

```bash
curl -X POST "http://localhost:8000/inject" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"Support can only use public docs and authorized tickets.\",\"domain\":\"customer_support\",\"compliance_tags\":[\"support-policy\",\"least-privilege\"]}"
```

### 2) Query through immune layer

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Can support access engineering release keys?\",\"domain\":\"customer_support\"}"
```

### 3) Observe governance state

```bash
curl "http://localhost:8000/domains"
curl "http://localhost:8000/crystal/state"
curl "http://localhost:8000/audit"
```

### Optional: bootstrap multiple domains

```bash
curl -X POST "http://localhost:8000/bootstrap" \
  -H "Content-Type: application/json" \
  -d "{\"items\":[{\"domain\":\"customer_support\",\"content\":\"Support can only use public docs.\"},{\"domain\":\"engineering\",\"content\":\"Engineering tokens are sensitive.\"}]}"
```

## Quick Start

```bash
pip install -e .
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

```bash
cd web
npm install
npm run dev
```

## API

- `POST /inject`
- `POST /bootstrap`
- `POST /chat`
- `POST /poison/test`
- `GET /domains`
- `GET /crystal/state`
- `GET /audit`
- `GET /audit/{id}`
- `POST /crystal/reset/{cell_id}`

## Demos

```bash
python examples/generic/bootstrap_and_chat.py
python examples/finance/loan_conflict.py
python examples/medical/cross_domain_poison.py
```

## Benchmarks

```bash
python benchmarks/pollution_intercept.py
python benchmarks/memory_repair.py
python benchmarks/audit_latency.py
```

## Enterprise Use Cases

- Internal copilot safety gateway
- RAG access guard across team boundaries
- Agent memory governor for long-running workflows
- Compliance evidence layer in regulated environments

## Trust and Governance

- Security reporting: [`SECURITY.md`](./SECURITY.md)
- Enterprise evaluation: [`docs/enterprise-evaluation.md`](./docs/enterprise-evaluation.md)
- Demo asset guide: [`assets/demo/README.md`](./assets/demo/README.md)
- Screenshot guide: [`assets/screenshots/README.md`](./assets/screenshots/README.md)

## Roadmap

- [ ] Domain profile import/export
- [ ] Policy DSL for enterprise guardrails
- [ ] Streaming API and async workers
- [ ] Multi-tenant dashboard
- [ ] Larger benchmark datasets

## Contributing

- Read [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Open issues with scenario, expected behavior, and sample payload
- Add reproducible benchmark/test for major logic changes
