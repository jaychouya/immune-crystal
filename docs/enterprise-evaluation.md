# Enterprise Evaluation Guide

This guide helps teams evaluate immune-crystal for an enterprise PoC.

## Evaluation Summary

| Area | What to validate |
| --- | --- |
| Domain isolation | Can sensitive knowledge stay inside the right domain? |
| Pollution interception | Are cross-domain and injection attempts blocked? |
| Memory repair | Does trusted memory stay reinforced over repeated use? |
| Auditability | Can every response be traced by `purity`, `lineage`, and `audit_id`? |
| Integration effort | Can the team connect existing services through REST APIs? |

## Reference PoC Flow

1. Define 3-5 enterprise domains.
2. Bootstrap 10-50 policy or knowledge items.
3. Run safe queries for each domain.
4. Run cross-domain leakage attempts.
5. Review `/audit`, `/domains`, and `/crystal/state`.
6. Export findings and decide rollout scope.

## PoC Checklist

| Check | Target | Result |
| --- | --- | --- |
| API starts locally | `GET /health` returns ok | TBD |
| Domain bootstrap | `/bootstrap` creates all test cells | TBD |
| Safe query | `blocked=false` with usable answer | TBD |
| Pollution query | `blocked=true` with reason | TBD |
| Audit record | `audit_id` is retrievable | TBD |
| Lineage | response includes contributing cells | TBD |
| Dashboard | web app shows cell pool and audit stream | TBD |
| Latency | audit p95 under accepted threshold | TBD |

## Success Criteria

Recommended minimum:

- Pollution interception rate: >= 95% on PoC dataset
- Memory repair rate: >= 80% on repeated-use scenario
- Audit p95 latency: < 50 ms on local benchmark
- No sensitive cross-domain leakage in manual review

## Data Handling

immune-crystal stores:

- Domain profiles in `data/domains.json`
- B-Cell memory in `data/cells.json`
- Audit records in `data/audit.db`
- Antibody patterns in `data/antibodies.json`

Before production:

- Move data storage to managed persistence.
- Define backup and retention rules.
- Encrypt disks and backups.
- Avoid injecting raw secrets unless required for controlled tests.

## Deployment Notes

Supported baseline:

- Python 3.11+
- FastAPI API service
- React dashboard
- Docker Compose for local deployment

Production hardening recommendations:

- Add authentication in front of the API.
- Restrict `/inject`, `/bootstrap`, and `/crystal/reset`.
- Put audit data on durable storage.
- Add request logging and metrics.
- Use private networking for model and storage services.

## Open Risks

- Current PoC detector uses lightweight routing and pattern logic.
- Real enterprise deployment should add domain-specific evaluation data.
- Third-party model outputs are not guaranteed by this middleware alone.
- Multi-tenant isolation requires additional authentication and tenancy controls.

## Decision Template

| Decision | Notes |
| --- | --- |
| Proceed to larger pilot? | TBD |
| Required blockers | TBD |
| Domains in first rollout | TBD |
| Security owner | TBD |
| Success metrics | TBD |
| Target rollout date | TBD |
