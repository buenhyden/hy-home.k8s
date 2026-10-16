---
title: "Ingress Controller Identity in Validators"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0119"
---

# Ingress Controller Identity in Validators Technical Specification (Spec)

## Overview

The cluster's ingress-nginx controller is retired upstream and must be
replaced; the replacement is an ADR decision that has not been made. The
repository validators spell the controller's identity as literals: the
ingress class, namespace, Service, Argo CD Application, annotation keys and
NodePorts appear about 35 times in `scripts/validation/platform/ingress.py`,
and `scripts/validate-infrastructure-contracts.sh` repeats several of the same
assertions. A controller swap would therefore rewrite the QA layer at the
same time as the manifests. This Spec, item 18 of the 2026-10-16 local QA
review, moves the identity to one declaration and removes the shell
duplicates while keeping today's behavior for ingress-nginx unchanged. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-ingress-controller-identity.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - one controller identity declaration in `ingress.py`, read by every check
    that used a literal;
  - nginx-specific chart value checks grouped behind that identity;
  - removal of `validate-infrastructure-contracts.sh` assertions that
    `ingress.py` already enforces, each proven covered first.
- Non-goals:
  - choosing or deploying a replacement controller, or any manifest change;
  - Gateway API (`HTTPRoute`, `Gateway`) validation, schema or AppProject
    support, which belongs to the replacement ADR;
  - `infrastructure/verify/verify-ingress-tls.sh` (live lane) and policy or
    README wording, which change with the replacement;
  - patching the running controller.

## Contracts

- `ingress.py` declares the controller identity once (`CONTROLLER`): kind,
  ingress class, namespace, Application name, chart, repository and release,
  controller Service name, HTTP port and NodePorts, annotation prefix, the
  annotation spelling for each intent (TLS redirect, permanent redirect, mesh
  upstream, upstream vhost, app root) and the forbidden snippet suffix.
- No other literal for those values remains in `ingress.py`; `validate()`
  accepts an injected identity so tests can swap it.
- Chart value checks that are specific to ingress-nginx run only when the
  declared kind is `ingress-nginx`.
- With the current identity every existing ingress test passes unchanged.
- Each removed shell assertion is shown, by a mutation of the checked
  manifest, to fail `ingress.py` before it is deleted.

## Core Design

The identity is a module constant beside the existing `ROUTES` table, not a
new file: a controller swap edits it in the same change as the manifests, and
the existing Application, Service and Ingress checks fail when the two
disagree, so it cannot drift silently. The replacement ADR must add Gateway
API validators in the same change that admits Gateway kinds to platform
assurance, so no route type becomes unvalidated.

## Data Modeling & Storage Strategy

No new data file. The identity is a Python mapping in the validator.

## Interfaces & Data Structures

`validate(root, docs, controller=CONTROLLER)`; rule codes (`INGRESS_ROUTE`,
`INGRESS_OWNER`, `INGRESS_REDIRECT`, `INGRESS_MESH`, `INGRESS_APP_ROOT` and
others) are unchanged.

## Edge Cases & Error Handling

- A swapped identity whose ingress class differs from the manifests reports
  `INGRESS_ROUTE` for each route.
- A swapped namespace leaves the current apex routes missing or unknown.
- A renamed redirect annotation reports `INGRESS_REDIRECT`.

## Failure Modes & Fallback / Human Escalation

If a shell assertion cannot be shown covered by `ingress.py`, it stays and
the Task records why.

## Verification Commands

- `python -m unittest tests.test_platform_ingress`.
- `python scripts/validation/platform/assurance.py --root .`.
- `bash scripts/validate-infrastructure-contracts.sh`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-ICI-001 | `ingress.py` reads one declared identity; existing ingress tests pass unchanged and identity-swap tests fail as stated; assurance passes on the repository. |
| VAL-ICI-002 | Duplicate shell assertions are removed after mutation proof; the shell validator passes; independent review passes. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-ICI-001 | Focused tests, assurance and staged QA |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-ICI-002 | Mutation proof, shell validator and review |
