---
title: 'Task: Workspace Contract Governance Normalization'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-05
---

# Task: Workspace Contract Governance Normalization

## Overview

This task record tracks implementation and verification evidence for the
workspace contract governance normalization plan. Task 1 is evidence-first: it
creates the Stage 04 task record, captures the requested baseline inventory,
and updates the Task stage index before later tasks modify `_workspace`, Stage
00, Stage 99, README, validator, or control-surface files.

No live Kubernetes, Argo CD, Vault, ESO, cloud, GitHub remote, credential,
secret value, paid job, push, merge, pull request, or third-party mutation is
in scope for this task.

## Inputs

- **Parent Spec**: [../../03.specs/020-workspace-contract-governance-normalization/spec.md](../../03.specs/020-workspace-contract-governance-normalization/spec.md)
- **Parent Plan**: [../plans/2026-07-05-workspace-contract-governance-normalization.md](../plans/2026-07-05-workspace-contract-governance-normalization.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)

## Working Rules

- Keep this task scoped to Stage 04 evidence and index maintenance.
- Do not edit `.gitignore`, `_workspace/README.md`, Stage 00 governance, Stage
  99 support docs, root README, scripts, or control-surface files in WCGN-001.
- Keep the task record English-first and the Task stage README Korean.
- Use summary evidence for large inventories; do not paste bulky raw command
  output into this task record.
- Treat repository-static validation as static evidence only. It does not
  prove live runtime readiness.
- Preserve unrelated user or parallel-agent work and do not revert edits made
  by others.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WCGN-001 | Create task evidence and baseline inventory | doc | VAL-SPC-020-003, VAL-SPC-020-004, VAL-SPC-020-006, VAL-SPC-020-007 | Task 1 | Baseline inventory, `_workspace` baseline, frontmatter/template drift scans, task README index, staged whitespace check, controller/spec/quality review follow-up | platform | Done |
| WCGN-002 | Establish `_workspace` contract and ignore boundary | doc | VAL-SPC-020-001, VAL-SPC-020-002, VAL-SPC-020-005 | Task 2 | `_workspace/README.md` tracked, scratch files ignored, contract owners aligned, quality gate | platform | Done |
| WCGN-003 | Audit and remediate frontmatter, template, section, README, and cross-link drift | doc | VAL-SPC-020-003, VAL-SPC-020-004, VAL-SPC-020-005, VAL-SPC-020-007 | Task 3 | Focused scans classify active violations vs templates/historical evidence | platform | Planned |
| WCGN-004 | Audit and remediate CI/CD, QA, formatting, linting, syntax, automation, workflow, and security drift | qa | VAL-SPC-020-006 | Task 4 | Control-surface descriptions match current scripts/workflows or recorded deferrals | platform | Planned |
| WCGN-005 | Add validator coverage, close evidence, and record memory | qa | VAL-SPC-020-008, VAL-SPC-020-009, VAL-SPC-020-010 | Task 5 | `git diff --check`, repository quality gate, final evidence, progress memory | platform | Planned |

## Suggested Types

- `doc`
- `qa`

## Baseline Inventory

| Date | Command | Result Class |
| --- | --- | --- |
| 2026-07-05 | `git status --short --branch` | PASS; branch was `codex/workspace-engineering-audit-pack` and the working tree had no pre-existing changes. |
| 2026-07-05 | `sed -n '1,220p' docs/99.templates/templates/sdlc/execution/task.template.md` | PASS; template frontmatter uses `type: sdlc/task`, `status: draft`, `owner: platform`, and the required Stage 04 task evidence structure. |
| 2026-07-05 | `sed -n '1,460p' docs/03.specs/020-workspace-contract-governance-normalization/spec.md` | PASS; the parent spec defines VAL-SPC-020-001 through VAL-SPC-020-010. |
| 2026-07-05 | `find AGENTS.md CLAUDE.md GEMINI.md README.md _workspace .agents .claude .codex .github docs examples gitops infrastructure policy scripts secrets tests traefik -maxdepth 3 -print \| sort` | PASS; pre-edit target inventory returned 592 paths across root shims, agent adapters, GitHub controls, docs, examples, GitOps, infrastructure, policy, scripts, secrets, tests, and Traefik surfaces. |
| 2026-07-05 | `find _workspace -maxdepth 4 -type f -print \| sort` | PASS; no files were present under `_workspace` before implementation. |
| 2026-07-05 | `git check-ignore -v _workspace/probe.log` | PASS; `_workspace/probe.log` is ignored by `.gitignore:31:_workspace/`. |
| 2026-07-05 | `rg -n "^type: (prd\|ard\|adr\|spec\|plan\|task\|guide\|policy\|runbook\|incident\|postmortem\|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | PASS; no active simple `type` values matched. Command exited with no matches. |
| 2026-07-05 | `rg -n "Target: d""ocs/\|Use this ""template\|SNIPPET LIBRARY\|\\{Folder or Project Name\\}\|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | PASS; pre-edit scan returned 50 matching lines across 23 files. Result class was Stage 99 template files plus scanner-command evidence in the active implementation plan; no active authored residue outside those classes was identified. |

Requested target inventory notes:

| Target | Status | Notes |
| --- | --- | --- |
| `AGENTS.md` | Present | Root Codex/GPT gateway. |
| `CLAUDE.md` | Present | Root Claude gateway. |
| `GEMINI.md` | Present | Root Gemini gateway. |
| `README.md` | Present | Root human-facing repository entrypoint. |
| `_workspace` | Present | Empty and fully ignored before WCGN-002. |
| `.agents` | Present | Shared agent asset owner. |
| `.claude` | Present | Claude provider adapter surface. |
| `.codex` | Present | Codex provider adapter surface. |
| `.github` | Present | GitHub-native control surface. |
| `docs` | Present | Canonical documentation taxonomy. |
| `examples` | Present | Sample and cloud example surfaces. |
| `gitops` | Present | Desired-state GitOps manifests. |
| `infrastructure` | Present | Local bootstrap and verification scripts. |
| `policy` | Present | Policy-as-code surface. |
| `scripts` | Present | Repository validation and helper scripts. |
| `secrets` | Present | Repository-local certificate fixture boundary; secret values were not inspected. |
| `tests` | Present | Repository test evidence boundary. |
| `traefik` | Present | Local Traefik route examples. |
| `DESIGN.md` | Absent | User-requested target; no canonical route currently exists. Do not create without a future approved design-doc contract. |

## Audit Findings

| Finding ID | Surface | Category | Current State | Action |
| --- | --- | --- | --- | --- |
| WCGN-AUD-001 | `DESIGN.md` | route | The requested target is absent, and current template routing has no canonical design-doc route. | Record absence only; do not create in this plan without future approved contract work. |
| WCGN-AUD-002 | `_workspace` | workspace | `_workspace` exists but contains no files before implementation; `_workspace/probe.log` is ignored by the current whole-directory ignore rule. | WCGN-002 owns contract and ignore-boundary changes. |
| WCGN-AUD-003 | `docs`, root shims, `.github`, `scripts` | frontmatter | Simple legacy `type` values returned no matches in the requested baseline scan. | Keep as baseline PASS for WCGN-003. |
| WCGN-AUD-004 | `docs/99.templates/**`, Stage 04 plan | template | Template residue scan returned only template files and scanner-command evidence in the current plan before this task record was created. | Keep templates as allowed; future scans may classify task evidence command literals as scanner evidence. |
| WCGN-AUD-005 | Stage 04 indexes | README | `docs/04.execution/tasks/README.md` did not yet list this task record before WCGN-001. | Update the Task stage structure and document index in WCGN-001. |

## Remediation Evidence

| Date | Task | Change | Evidence |
| --- | --- | --- | --- |
| 2026-07-05 | WCGN-001 | Created this Stage 04 task evidence record from the canonical task template and parent spec/plan. | Frontmatter uses `type: sdlc/task`; required sections are present in the requested order. |
| 2026-07-05 | WCGN-001 | Updated `docs/04.execution/tasks/README.md` with the new WCGN document index row and structure block entries for WCGN plus two already-indexed 2026-07-05 task files that were missing from the structure block. | README keeps `## Link Basis` and `## Related Documents`. |
| 2026-07-05 | WCGN-001 | Reviewed `docs/04.execution/plans/README.md`. | Existing plan structure and index already include `2026-07-05-workspace-contract-governance-normalization.md`; no edit was needed. |
| 2026-07-05 | WCGN-001 | Completed controller/spec/quality review follow-up. | WCGN-001 status is `Done`; the verification command list now includes every command claimed by validation evidence. |
| 2026-07-05 | WCGN-002 | Narrowed the `_workspace` ignore rule to ignore scratch while allowing the directory and `_workspace/README.md` to be tracked. | `git check-ignore -v _workspace/probe.log` returned `.gitignore:31:_workspace/*	_workspace/probe.log`; `git check-ignore -v _workspace/README.md` exited 1 with no output, recorded as NOT IGNORED. |
| 2026-07-05 | WCGN-002 | Created `_workspace/README.md` as the frontmatter-free checked-in contract and added the root README structure entry. | `git ls-files _workspace` returned only `_workspace/README.md` after staging the README. |
| 2026-07-05 | WCGN-002 | Aligned Stage 00 governance and Stage 99 support contracts with the `_workspace` staging boundary. | `git diff --check` returned no whitespace errors and `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | WCGN-002 | Followed up on quality review by tightening dry-run scratch wording from logs to redacted, non-secret summaries. | `rg -n "Dry-run logs\|dry-run\|logs\|summaries" _workspace/README.md` no longer returns `Dry-run logs`; validation passed with `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .`. |

## Verification Commands

```bash
git status --short --branch
sed -n '1,220p' docs/99.templates/templates/sdlc/execution/task.template.md
sed -n '1,460p' docs/03.specs/020-workspace-contract-governance-normalization/spec.md
find AGENTS.md CLAUDE.md GEMINI.md README.md _workspace .agents .claude .codex .github docs examples gitops infrastructure policy scripts secrets tests traefik -maxdepth 3 -print | sort
find _workspace -maxdepth 4 -type f -print | sort
git check-ignore -v _workspace/probe.log
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
which rtk
/home/hy/.local/bin/rtk --version
/home/hy/.local/bin/rtk gain
git check-ignore -v _workspace/probe.log
git check-ignore -v _workspace/README.md
git ls-files _workspace
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git add .gitignore _workspace/README.md README.md docs/00.agent-governance/subagent-protocol.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/approval-boundaries.md docs/99.templates/support/documentation-contract.md docs/99.templates/support/frontmatter-schema.md docs/99.templates/support/legacy-cleanup-rules.md docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(governance): Define workspace staging boundary"
rg -n "Dry-run logs|dry-run|logs|summaries" _workspace/README.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add _workspace/README.md docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(governance): Clarify workspace dry-run boundary"
```

## Verification Summary

- **Test Commands**:
  - `git check-ignore -v _workspace/probe.log`
  - `git check-ignore -v _workspace/README.md`
  - `git ls-files _workspace`
  - `git diff --check`
  - `git diff --cached --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: Not applicable; WCGN-001 is documentation evidence and
  baseline inventory work.
- **Logs / Evidence Location**: This task record and the commit
  `docs(tasks): Start workspace contract governance evidence`.

## Validation Evidence

| Date | Check | Result |
| --- | --- | --- |
| 2026-07-05 | Branch and clean state | PASS; `git status --short --branch` returned only `## codex/workspace-engineering-audit-pack` before edits. |
| 2026-07-05 | Template and spec read | PASS; required task template and parent spec were read, including VAL-SPC-020-001 through VAL-SPC-020-010. |
| 2026-07-05 | Baseline scans | PASS; requested target inventory, `_workspace` baseline, ignore baseline, frontmatter scan, and template-residue scan were recorded as summarized above. |
| 2026-07-05 | Scope control | PASS; staged files are this task record and `docs/04.execution/tasks/README.md`. `docs/04.execution/plans/README.md` was reviewed, added by the requested staging command, and left unchanged because it was already current. |
| 2026-07-05 | Template heading validation | PASS; the repository quality gate initially required the task-template headings `## Suggested Types` and `## Verification Summary`; they were added and the quality gate passed. |
| 2026-07-05 | Working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | Repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | Staged whitespace check | PASS; `git diff --cached --check` returned no whitespace errors after staging. |
| 2026-07-05 | Runtime tooling note | PASS with limitation recorded; `which rtk` returned `rtk not found`, `/home/hy/.local/bin/rtk --version` returned `rtk 0.34.3`, and `/home/hy/.local/bin/rtk gain` failed to initialize its tracking database, so validation commands ran directly without inspecting private runtime state. |
| 2026-07-05 | `_workspace` ignore probe | PASS; `git check-ignore -v _workspace/probe.log` returned `.gitignore:31:_workspace/*	_workspace/probe.log`. |
| 2026-07-05 | `_workspace` README unignore probe | PASS; `git check-ignore -v _workspace/README.md` exited 1 with no output, recorded as NOT IGNORED. |
| 2026-07-05 | `_workspace` tracked-file boundary | PASS; `git ls-files _workspace` returned only `_workspace/README.md`. |
| 2026-07-05 | WCGN-002 working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | WCGN-002 repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | WCGN-002 quality review follow-up scan | PASS; `_workspace/README.md` now says `Redacted, non-secret dry-run summaries.` and no longer says `Dry-run logs.`. Remaining `logs` mentions are the prohibited `Secret-bearing local logs` out-of-scope boundary. |
| 2026-07-05 | WCGN-002 follow-up whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | WCGN-002 follow-up repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |

## Deferrals

- WCGN-003 owns active frontmatter, template, section, README, and cross-link
  remediation.
- WCGN-004 owns CI/CD, QA, formatting, linting, syntax, automation, workflow,
  and security wording remediation.
- WCGN-005 owns final validator coverage, final validation, and progress memory
  closure. WCGN-001 does not update
  `docs/00.agent-governance/memory/progress.md` because the Task 1 write set
  explicitly excludes Stage 00 files.

## Related Documents

- **Spec**: [../../03.specs/020-workspace-contract-governance-normalization/spec.md](../../03.specs/020-workspace-contract-governance-normalization/spec.md)
- **Plan**: [../plans/2026-07-05-workspace-contract-governance-normalization.md](../plans/2026-07-05-workspace-contract-governance-normalization.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Task Stage Index**: [./README.md](./README.md)
