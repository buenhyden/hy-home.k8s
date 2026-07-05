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
workspace contract governance normalization plan. WCGN-001 created the Stage
04 evidence record and baseline inventory, WCGN-002 established the
`_workspace` staging boundary, and WCGN-003 audited and remediated
frontmatter, template, section, README, and cross-link drift. WCGN-004 and
WCGN-005 remain planned for CI/CD and QA wording, validator coverage, closure
evidence, and progress memory.

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

- Keep each WCGN change scoped to its task-specific write set and evidence
  owner.
- Modify shared governance, template, README, script, or control surfaces only
  when the active task explicitly owns that surface.
- Keep this task record English-first and keep human-facing README updates in
  their existing Korean style.
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
| WCGN-003 | Audit and remediate frontmatter, template, section, README, and cross-link drift | doc | VAL-SPC-020-003, VAL-SPC-020-004, VAL-SPC-020-005, VAL-SPC-020-007 | Task 3 | Focused scans classify active violations vs templates/historical evidence | platform | Done |
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
| WCGN-AUD-006 | `docs`, root shims, `.github`, `scripts` | frontmatter | WCGN-003 frontmatter scan returned no simple un-namespaced `type` values. The broad metadata-key scan showed namespaced profiles and canonical key order across active routed frontmatter. | No frontmatter remediation required. |
| WCGN-AUD-007 | `docs`, root shims, `.github`, `scripts` | template / section | WCGN-003 template residue matches were limited to Stage 99 template files, scanner-command evidence, and explicit cleanup-rule or legacy-route headings. | No active authored template residue or deprecated related-document section needed removal. |
| WCGN-AUD-008 | README entrypoints | README | README inventory returned repository, workspace, docs, examples, GitOps, infrastructure, scripts, tests, and Traefik README files. The literal README duplication scan reported missing `.codex/README.md` and `.claude/README.md` operands because those provider README files do not exist; a focused rerun over existing operands found concise owner pointers, not duplicated Stage 00 or Stage 99 policy bodies. | No README body rewrite required. Do not create provider README files without a future route need. |
| WCGN-AUD-009 | `docs/90.references/data/agent-reference-index.md`, `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | route | Two active reference documents still used the old Stage 03 placeholder `docs/03.specs/<feature-id>/...` as current guidance. | Update both references to `docs/03.specs/<###-Numbering>-<feature-id>/...`. |
| WCGN-AUD-010 | Stage 00 rules, active Stage 03 specs/guardrails, Stage 99 templates, Stage 04 migration evidence, Stage 90 audits, progress memory | route / cross-link | Remaining route scan matches are current deny-route guardrails (`docs/superpowers/**`, `docs/api/**`), active Stage 03 spec or guardrail references that reject off-taxonomy paths or record approved numbering contracts, template examples that explicitly reject `docs/api/**`, scanner-command evidence, completed migration evidence for old PRD filenames, dated Stage 90 audit evidence, or dated progress memory. | Leave accepted historical, active spec, and guardrail evidence in place; do not rewrite completed migration records into false current-state history. |

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
| 2026-07-05 | WCGN-003 | Updated active Stage 90 route guidance to the numbered Stage 03 placeholder. | `docs/90.references/data/agent-reference-index.md` now points feature-local Agent design to `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md`; `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` now points the Stage 03 spec lifecycle to `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`. |
| 2026-07-05 | WCGN-003 | Reviewed folder README impact for the two Stage 90 reference edits. | `docs/90.references/data/README.md` and `docs/90.references/research/2026-07-04-wer/README.md` remain current because their index rows summarize document ownership and do not embed the old route placeholder. |
| 2026-07-05 | WCGN-003 | Recorded frontmatter, template residue, legacy section, README duplication, and route/cross-link scan classifications. | WCGN-003 status is `Done`; remaining noisy matches are documented as templates, explicit route guardrails, scanner-command evidence, migration evidence, Stage 90 audits, or progress memory. |

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
bash scripts/validate-repo-quality-gates.sh .
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references docs/98.archive docs/99.templates/support docs/00.agent-governance
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]|command ""1|pytest ""tests|Example""Contract" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^## (Deprecated|Legacy|Related Refer""ences|Related Fold""ers|Related Fi""les|References|See Also|Links)\\b" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
find . -name README.md -not -path './.git/*' -not -path './.agents/*' -not -path './.agent-work/*' -print | sort
# Initial README duplication probe; expected to exit 2 because provider README
# operands do not exist in this repository.
rg -n "must|forbidden|required|canonical owner|contract owner|approval boundary|protected surface" README.md docs/**/README.md .codex/README.md .claude/README.md
# Focused existing-operand README duplication rerun.
rg -n "must|forbidden|required|canonical owner|contract owner|approval boundary|protected surface" README.md docs/**/README.md
rg -n "docs/superpowers|docs/api/|docs/01\\.requirements/YYYY-MM-DD-|docs/03\\.specs/<feature-id>" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs .github scripts docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(governance): Normalize document contract drift"
```

## Verification Summary

- **Test Commands**:
  - `git check-ignore -v _workspace/probe.log`
  - `git check-ignore -v _workspace/README.md`
  - `git ls-files _workspace`
  - `git diff --check`
  - `git diff --cached --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: Runtime evals are not applicable for WCGN-001 through
  WCGN-003 because the completed work is documentation and governance evidence.
  Verification used repository-static quality gates and focused scans only.
- **Logs / Evidence Location**: This task record and the WCGN implementation
  commits.

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
| 2026-07-05 | WCGN-003 initial repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed` before WCGN-003 scans or edits. |
| 2026-07-05 | WCGN-003 contract reads | PASS; read `frontmatter-schema.md`, `template-routing.md`, `documentation-contract.md`, and `legacy-cleanup-rules.md`; also read Stage 00 documentation protocol and route rules through the repo-local docs-stage-conformance workflow. |
| 2026-07-05 | WCGN-003 frontmatter scans | PASS; simple legacy `type` scan returned no matches. The metadata-key scan was reviewed for routed frontmatter and showed namespaced profile values with key order `title`, `type`, `status`, `owner`, `updated`. |
| 2026-07-05 | WCGN-003 template and section scans | PASS; matches were Stage 99 templates, scanner-command evidence, explicit cleanup rules, or legacy route headings. No active authored document retained template residue or deprecated related-document headings. |
| 2026-07-05 | WCGN-003 README scans | PASS with noted literal-command limitation; sorted README inventory completed. The literal duplication scan exited 2 only because `.codex/README.md` and `.claude/README.md` do not exist; focused rerun over existing README operands found concise owner pointers rather than duplicated policy bodies. |
| 2026-07-05 | WCGN-003 route and cross-link scans | PASS after remediation; active Stage 90 references were updated from `docs/03.specs/<feature-id>/...` to `docs/03.specs/<###-Numbering>-<feature-id>/...`. Remaining matches are current route-deny guardrails, templates, scanner-command evidence, completed migration evidence, Stage 90 audits, or progress memory. |
| 2026-07-05 | WCGN-003 working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors after WCGN-003 edits. |
| 2026-07-05 | WCGN-003 repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed` after WCGN-003 edits. |

## Deferrals

- WCGN-004 owns CI/CD, QA, formatting, linting, syntax, automation, workflow,
  and security wording remediation.
- WCGN-005 owns final validator coverage, final validation, and progress memory
  closure. Progress memory remains deferred to WCGN-005 under the plan's
  ownership boundary for WCGN-001 through WCGN-004.

## Related Documents

- **Spec**: [../../03.specs/020-workspace-contract-governance-normalization/spec.md](../../03.specs/020-workspace-contract-governance-normalization/spec.md)
- **Plan**: [../plans/2026-07-05-workspace-contract-governance-normalization.md](../plans/2026-07-05-workspace-contract-governance-normalization.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Task Stage Index**: [./README.md](./README.md)
