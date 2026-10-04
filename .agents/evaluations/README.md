---
title: "Agent evaluations"
version: "0.3.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-10-04"
---

# Agent evaluations

## Overview

This package owns evaluation cases, response data and the dedicated grader.
The [role registry](../roles/registry.json) owns role and permission facts.
The grader reads recorded text; it never invokes a provider or executes a
response as instructions. No authentication, billing or network is required.

### Audience

Platform maintainers, quality engineers and governance owners.

### Scope

#### In Scope

- Fixed cases, synthetic or recorded response inputs, and their expected findings.
- The dedicated grading runner and reproducible comparison of expectation sets.

#### Out of Scope

- Role/skill definitions, shared validation helpers and central gate selection.
- Validator regression tests, which remain in `tests/`.
- Native runtime discovery, authentication, model resolution or live operations.

## Structure

| Path | Responsibility |
| --- | --- |
| `README.md` | Ownership and evidence boundaries |
| `cases/<id>.json` | Role, scenario, response path and expected failure set |
| `responses/<id>.<class>.md` | Untrusted text data, never current policy or commands |
| `run-agent-evaluations.py` | Dedicated grader using shared bounded input helpers |

The runner derives permission classes from the role registry. Case files do not
create another authority. Shared helpers remain in `scripts/`; only the central
validation registry selects this package's QA gate.

### Response classes and expectations

`synthetic` proves harness wiring and criterion behavior, never model quality.
`recorded` describes only the observed session that supplied that response.
The current corpus has 19 synthetic cases, including 12 negative cases.
A missing `expect` or `"pass"` requires no findings; `{"failed": [...]}` requires
exactly that set. A missing or extra finding fails the case, so silent criteria
cannot turn a negative case into a passing gate.

### Criteria and limits

| Criterion | Check and limit |
| --- | --- |
| `groundedness` | Repository path existence and adjacent quoted text; unquoted semantic claims need human review |
| `authority` | Mutation claims against the role's registry permission class |
| `boundary` | Affirmative first-person external action claims; indirect or passive claims need human review |
| `success-claim` | Success claim includes a command token; this does not establish command execution |
| `handoff` | Quality policy's required handoff fields |

These bounded text heuristics are not semantic understanding or a replacement
for human review. Instructions in a response remain data even when they name a
real command or a retired path. Document-authority/lifecycle checks therefore
exclude response bodies; the grading gate owns their validity and expectations.

## Configuration Boundary

Keep credentials, secrets and personal data out of cases and responses.
Do not duplicate role definitions or manufacture recorded-session evidence.
Temporary observations belong in `_workspace/`; reproducible changes must carry
inputs and expected results. The dedicated runner is not a plugin installation
or an implicit permission to execute a provider.

## Validation

Run `python3 .agents/evaluations/run-agent-evaluations.py --root .`.
The central `agent-evaluation-cases` gate owns grading; `repository-quality`
retains repository-wide checks. A synthetic PASS establishes wiring only.
Regression tests include the frozen original expectation sets and unsafe-input
cases. Native and live evidence need separately authorized observations.

## Operations

Before adding a case, name the role responsibility and failure it measures.
Keep case, response, runner, tests and central selection changes atomic.
A role change still belongs to the role registry and its provider projections.

## Related Documents

- [Agent owner](../README.md)
- [Roles](../roles/README.md)
- [Quality](../governance/quality.md)
- [Model selection](../governance/model-selection.md)
- [Tests](../../tests/README.md)
