---
title: 'Task: SDLC Lifecycle Contract'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: SDLC Lifecycle Contract

## Overview

This document tracks implementation and verification work for the SDLC
lifecycle contract. The work aligns lifecycle routing, numeric PRD/spec
contracts, archive tombstone metadata, `_workspace` staging boundaries, and
repository-static validation evidence.

## Inputs

- **Parent Spec**: [../../03.specs/021-sdlc-lifecycle-contract/spec.md](../../03.specs/021-sdlc-lifecycle-contract/spec.md)
- **Parent Plan**: [../plans/2026-07-06-sdlc-lifecycle-contract.md](../plans/2026-07-06-sdlc-lifecycle-contract.md)

## Approval and Safety Boundaries

- Documentation-only work still needs validation evidence.
- Contract bodies stay in Stage 00 and Stage 99 owners; README files route and
  index rather than duplicating governance bodies.
- Repo-static validation must not be reported as live runtime readiness unless
  a separate live check was approved and run.
- `_workspace` may stage only temporary, non-secret repo-support artifacts.
- Archive tombstones preserve traceability metadata in frontmatter and keep
  tombstone bodies concise by default.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| T-001 | Align lifecycle, numbering, handoff, archive, active-surface, and workspace staging contract surfaces. | doc | Contracts; Core Design | PLN-001 | Commit `c24c2b7`; follow-up placeholder correction commit `ec29174`; reviewed by subagents; `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .`. | platform | Done |
| T-002 | Add archive tombstone metadata contract, update current tombstones, and keep archive validator support passing. | doc/test | Archive Contract; Data Modeling & Storage Strategy | PLN-002 | Commit `b7eeac9`; amended after semantic archive reason review; `git diff --check`; `bash -n scripts/validate-repo-quality-gates.sh`; `bash scripts/validate-repo-quality-gates.sh .`. | platform | Done |
| T-003 | Record active route evidence, `_workspace` boundary evidence, and this Stage 04 task record. | doc | Numbering Contract; Workspace Staging Contract | PLN-003 | Active route scans confirmed numeric Stage 01 PRDs and numeric Stage 03 spec folders; `_workspace/README.md` boundary wording; task README index update; `bash scripts/validate-repo-quality-gates.sh .`. | platform | Done |
| T-004 | Add remaining deterministic lifecycle route gates and close final validation evidence. | test/doc | Core Design; Acceptance Criteria | PLN-004 | Validator now rejects date-based active PRDs, nonnumeric active PRDs, nonnumeric active Spec folders, invalid archive tombstone metadata, and Stage 04 README index status/updated drift; final `git diff --check`, shell syntax check, full repository quality gate, and active route scans passed. | platform | Done |

### Suggested Types

This task uses `doc` for contract and evidence updates and `test` for
repository-static validation gate changes. It does not include runtime `impl`
or `ops` work.

### Phase View

### Phase 1

- [x] T-001 Align lifecycle contract surfaces.
- [x] T-002 Extend archive tombstone metadata.

### Phase 2

- [x] T-003 Align active surface evidence and workspace boundary.
- [x] T-004 Add validation gates and close evidence.

## Verification Summary

- **Test Commands**:
  - `git diff --check`: pass, no output.
  - `bash -n scripts/validate-repo-quality-gates.sh`: pass, no output.
  - `bash scripts/validate-repo-quality-gates.sh .`: pass,
    `[PASS] repository quality gates passed`.
  - `find docs/01.requirements -maxdepth 1 -type f -name '*.md' -printf '%f\n' | sort`: pass.
  - `find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort`: pass.
  - `find docs/01.requirements -maxdepth 1 -type f -name '*.md' ! -name README.md -printf '%f\n' | awk '!/^[0-9][0-9][0-9]-.+\.md$/ { print; bad=1 } END { exit bad }'`: pass, no output.
  - `find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | awk '!/^[0-9][0-9][0-9]-.+/ { print; bad=1 } END { exit bad }'`: pass, no output.
- **Eval Commands**:
  - Subagent spec compliance review for Task 1.
  - Subagent quality review for Task 1.
  - Subagent spec compliance review for Task 2.
  - Subagent quality review for Task 2.
  - Subagent spec compliance review for Task 3.
  - Subagent quality review for Task 3, with follow-up evidence fix applied.
- **Logs / Evidence Location**:
  - Git commits on branch `codex/sdlc-lifecycle-contract`.
  - This task record.
  - Parent implementation plan linked above.

### Active Route Scan Results

Stage 01 active PRD files:

```text
001-argo-rollouts-progressive-delivery.md
002-argo-notifications-slack.md
003-workspace-agent-governance-platform.md
004-current-local-gitops-platform.md
README.md
```

Stage 03 active Spec folders:

```text
004-argo-rollouts-progressive-delivery
005-argo-notifications-slack
006-workspace-harness-gap-analysis
008-current-local-gitops-platform
009-workspace-harness-research-pack
010-workspace-harness-implementation-audit-pack
011-template-contract-governance-migration
012-template-governance-audit-enhancement
013-workspace-document-governance-hardening
014-workspace-document-contract-normalization
015-agent-governance-contract-normalization
016-active-control-surface-governance-hardening
017-workspace-engineering-research-pack
018-workspace-engineering-implementation-audit-pack
019-template-path-numbering-contract
020-workspace-contract-governance-normalization
021-sdlc-lifecycle-contract
```

## Traceability

- **Spec**: [../../03.specs/021-sdlc-lifecycle-contract/spec.md](../../03.specs/021-sdlc-lifecycle-contract/spec.md)
- **Plan**: [../plans/2026-07-06-sdlc-lifecycle-contract.md](../plans/2026-07-06-sdlc-lifecycle-contract.md)
- **SDLC Governance**: [../../99.templates/support/sdlc-governance.md](../../99.templates/support/sdlc-governance.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
