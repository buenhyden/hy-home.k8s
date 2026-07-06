---
title: 'Task: Control Surface and Cloud Example Documentation Normalization'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-06
---

# Task: Control Surface and Cloud Example Documentation Normalization

## Overview

This document tracks implementation and verification work for the control
surface and cloud example documentation normalization effort. It keeps the
approved spec and plan traceable to concrete commits and validation evidence.

## Inputs

- **Parent Spec**: [../../03.specs/022-control-cloud-doc-normalization/spec.md](../../03.specs/022-control-cloud-doc-normalization/spec.md)
- **Parent Plan**: [../plans/2026-07-06-control-cloud-doc-normalization.md](../plans/2026-07-06-control-cloud-doc-normalization.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- README files and GitHub-native Markdown must remain frontmatter-free.
- Example-local cloud docs may receive SDLC frontmatter only through the
  approved route contract.
- Repo-static validation must not be reported as live runtime readiness unless
  a separate live check was approved and run.
- Do not inspect, write, or record secret values.
- Do not mutate live clusters, cloud providers, GitHub remote resources, or
  credentials.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CCDN-001 | Establish spec, plan, task, README indexes, and progress memory. | doc | Core Design | PLN-001 | Pending first commit and `git diff --check`. | platform | In Progress |
| CCDN-002 | Update Stage 99 and Stage 00 route contracts for example-local SDLC snapshot docs. | doc/test | Contracts; Core Design | PLN-002 | Contract docs updated; `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .`. Validator frontmatter enforcement follows after provider docs receive frontmatter. | platform | In Progress |
| CCDN-003 | Normalize active control-surface routing text while preserving frontmatter-free README/GitHub-native boundaries. | doc | Control-Surface Config Contract | PLN-003 | Pending README/GitHub-native scan and repo-quality gate. | platform | Todo |
| CCDN-004 | Normalize AWS example-local SDLC snapshot docs. | doc | Example-Local SDLC Snapshot Contract | PLN-004 | Pending frontmatter/section/cross-link validation. | platform | Todo |
| CCDN-005 | Normalize Azure example-local SDLC snapshot docs. | doc | Example-Local SDLC Snapshot Contract | PLN-005 | Pending frontmatter/section/cross-link validation. | platform | Todo |
| CCDN-006 | Close validation and execution evidence. | test/doc | Verification Commands | PLN-006 | Pending final validation bundle and task/progress update. | platform | Todo |

## Suggested Types

- `doc`
- `test`
- `eval`
- `ops`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [ ] CCDN-001 Establish design and execution tracking docs.
- [ ] CCDN-002 Update route and validation contracts.

### Phase 2

- [ ] CCDN-003 Normalize active control-surface routing text.
- [ ] CCDN-004 Normalize AWS example-local docs.
- [ ] CCDN-005 Normalize Azure example-local docs.

### Phase 3

- [ ] CCDN-006 Close validation and evidence.

## Verification Summary

- **Test Commands**:
  - `git diff --check`: pass, no output for CCDN-002 contract patch.
  - Pending: `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`: pass,
    `[PASS] repository quality gates passed` for CCDN-002 contract patch.
  - Pending: `bash scripts/validate-k8s-manifests.sh .`
  - Pending: `bash scripts/check-secret-handling.sh .`
  - Pending: `bash scripts/validate-policy-gates.sh .`
- **Eval Commands**:
  - Pending self-review against the parent spec.
- **Logs / Evidence Location**:
  - This task record.
  - `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Spec**: [../../03.specs/022-control-cloud-doc-normalization/spec.md](../../03.specs/022-control-cloud-doc-normalization/spec.md)
- **Plan**: [../plans/2026-07-06-control-cloud-doc-normalization.md](../plans/2026-07-06-control-cloud-doc-normalization.md)
- **Previous Control Surface Spec**: [../../03.specs/016-active-control-surface-governance-hardening/spec.md](../../03.specs/016-active-control-surface-governance-hardening/spec.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
