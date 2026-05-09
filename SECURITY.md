# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| `main` | Best effort |
| `< 0.1.0` | No |

## Reporting a Vulnerability

Please open a private security advisory on GitHub when available, or contact the maintainer through the repository owner profile.

Include:

- Affected component
- Reproduction steps
- Expected impact
- Logs or payloads with secrets removed

## Response Targets

| Severity | Initial response | Target fix |
| --- | ---: | ---: |
| Critical | 72 hours | 14 days |
| High | 7 days | 30 days |
| Medium/Low | Best effort | Best effort |

## Scope

In scope:

- API behavior
- Cross-domain leakage controls
- Audit log integrity
- Prompt-injection defense logic

Out of scope:

- Misconfigured deployments
- Third-party model behavior outside this middleware
- Secrets committed by downstream users

## Disclosure

Please do not publicly disclose a vulnerability before a fix or mitigation is available.
