---
title: "Survey Status and Local Gaps"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0125-TSK-0001"
parent_ids: ["SPEC-0125-PLAN-0001"]
---

# Task: Survey Status and Local Gaps

## Overview

Record the status of the survey's 148 requirements and close the local gaps
that need no operator decision. It executes [SPEC-0125](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: the operator's repository survey specification (STATE-01 and
  CR-01.01 to CR-21.05). On 2026-10-27 the operator asked whether every item
  was complete and then said to proceed as recommended: record the status in
  a new Spec and fix the local gaps first.
- Audit: four read-only reviewers audited main `bc7da828` by CR group.
- Start: main `bc7da828`, branch `docs/cr-status-and-local-gaps`.

### Survey CR Status

Counts at `bc7da828`: 58 `KEEP`, 6 `DONE_THIS_CYCLE`, 5 `GAP`, 60
`PARTIAL`, 8 `EXTERNAL`, 11 `PROCESS`. "Fixed here" means WORK-002 of this
Task. "Next slice B" (architecture views, ADR lineage, branch strategy) and
"Next slice C" (templates and governance prompts) are later Specs. An
operator decision or another repository is named where it blocks a row.

| CR | Status at `bc7da828` | Evidence | Disposition |
| --- | --- | --- | --- |
| CR-01.01 | `PROCESS` | The survey specification is operator input in ignored `_workspace/`; SPEC-0124 and this Task cite it | none |
| CR-01.02 | `EXTERNAL` | Atom and relation tables exist only in ignored `_workspace/` | Operator supplies the original text for rewritten rows |
| CR-01.03 | `PROCESS` | `.agents/workflows/work-lifecycle.md` Intake and Resume; `context-and-memory.md` resume decision | none |
| CR-01.04 | `PARTIAL` | `quality.md` handoff snapshot named branch, HEAD and base only | Fixed here: candidate, verified and delivered commits named |
| CR-01.05 | `PARTIAL` | Resume decision exists; no stale rule for an old result | Fixed here: a result over a changed commit is stale |
| CR-01.06 | `KEEP` | `.claude/provider.md` observations carry client version and date; SPEC-0124 EVD-004 run IDs | none |
| CR-01.07 | `PARTIAL` | `scripts/qa.py` uses `git ls-files -z`; a missing-path or zero-match negative case was not confirmed | Next slice C: confirm or add one negative case |
| CR-01.08 | `PROCESS` | `work-lifecycle.md` Implementation and Completion; other repositories read-only | none |
| CR-01.09 | `PROCESS` | `quality.md` DEFER vocabulary and handoff residual risk | none |
| CR-02.01 | `PROCESS` | Research README Research Contract; SPEC-0124 order of work | none |
| CR-02.02 | `KEEP` | `m0012` register columns: source type, final URL, version, checked date, section, limits | none |
| CR-02.03 | `PARTIAL` | Research README kept unretrieved sources as limits only | Fixed here: internal-decision non-applicability sentence |
| CR-02.04 | `DONE_THIS_CYCLE` | SPEC-0124, PR #179 | none |
| CR-02.05 | `PARTIAL` | ADR-0050, ADR-0051, SPEC-0121, research m0007 and m0008 | Per-technology advisory and supported-version coverage not verified |
| CR-02.06 | `DONE_THIS_CYCLE` | SPEC-0124 ten-by-six matrix in `m0012`, PR #179 | none |
| CR-02.07 | `PARTIAL` | `m0012` leaves adoption to canonical owners | Operator decision per `DERIVED_PROPOSAL` cell |
| CR-02.08 | `PARTIAL` | `SRC-WERPC-015` cited SSDF 1.1 without the 1.2 draft | Fixed here: `m0012` SSDF edition check |
| CR-03.01 | `PARTIAL` | Single governance owners under `.agents/governance/`; `.agents/knowledge/domains.md` is draft | Seven-area mapping optional; low value |
| CR-03.02 | `PARTIAL` | ADR-0033 and Stage 99 artifact IDs | A joint approved edition needs the other repositories |
| CR-03.03 | `PARTIAL` | `agent-execution.md` and provider notes document local extensions | Common-versus-local split not tabulated |
| CR-03.04 | `PROCESS` | `approval-and-safety.md` approval table | none |
| CR-03.05 | `PROCESS` | `agent-execution.md` candidate, approval and adoption recorded separately | none |
| CR-03.06 | `EXTERNAL` | Needs the other three repositories' adopted revisions | none |
| CR-03.07 | `EXTERNAL` | Needs the other three repositories and a joint edition approval | none |
| CR-04.01 | `PARTIAL` | `domains.md`, `project-map.md`; Archive retention classes | Sentence-level conflict classification absent; maps are draft |
| CR-04.02 | `DONE_THIS_CYCLE` | SPEC-0122, PR #165: seven units to `git-history-only` | none |
| CR-04.03 | `KEEP` | `agent-execution.md` single-owner and touched-duplicate rules; SPEC-0122 consumer search | none |
| CR-04.04 | `PARTIAL` | `quality.md` retirement rules; pair screening exists only in ignored `_workspace/` | Pair review unverifiable from the repository |
| CR-04.05 | `KEEP` | `quality.md` no new ledger to retire QA; MIG-0007 | none |
| CR-05.01 | `KEEP` | `docs/99.templates/` contracts and templates; `tests/test_repository_form_contracts.py` | none |
| CR-05.02 | `KEEP` | `scripts/validate-document-contract-registry.py` template-source parity | none |
| CR-05.03 | `KEEP` | `registry.json` profile frontmatter; `frontmatter.schema.json` | Cross-repository enum alignment is external |
| CR-05.04 | `KEEP` | `registry.json` lifecycle domains; `document-lifecycle.md` | Four-repository vocabulary is external |
| CR-05.05 | `KEEP` | Registry, schemas and templates under the registry gate | none |
| CR-05.06 | `KEEP` | Migration admission generation 9 to 10, SPEC-0106; strict cutover tests | none |
| CR-05.07 | `KEEP` | `tests/test_document_lifecycle_migration.py`; parity check | none |
| CR-05.08 | `KEEP` | ADR-0030 numbering census clarification, PR #178 | none |
| CR-05.09 | `KEEP` | MIG-0002 mapping; ADR-0030 | none |
| CR-05.10 | `KEEP` | ADR-0030: gaps are not closed by renumbering | none |
| CR-05.11 | `KEEP` | `quality.md` completion sequence; Task form separates evidence | none |
| CR-05.12 | `PARTIAL` | `m0012` source rows are not mapped to Stage 99 fields | Operator decision on adoption |
| CR-05.13 | `KEEP` | Separate lifecycle domains; `tests/test_task_acceptance_boundaries.py` | none |
| CR-06.01 | `KEEP` | `.agents/governance/sdlc.md` flow and terminology | none |
| CR-06.02 | `KEEP` | `document-authoring.md`; `tests/test_task_summary_derivation.py` | none |
| CR-06.03 | `KEEP` | `document-lifecycle.md` approval separate from completion | none |
| CR-06.04 | `PARTIAL` | Task Evidence columns; exit code, time and checker not structured | Next slice C: author prompt |
| CR-06.05 | `PROCESS` | `work-lifecycle.md` keeps Task evidence current | none |
| CR-06.06 | `KEEP` | Task Criterion Acceptance; Plan Promotion | none |
| CR-06.07 | `PARTIAL` | Spec template lacks scenario prompts; Plan template lacks interface and migration prompts | Next slice C: author prompts |
| CR-06.08 | `KEEP` | Spec Kit not installed; `sdlc.md` and ADR-0033 keep Task records | none |
| CR-06.09 | `PARTIAL` | `sdlc.md` transitions; security and feedback touchpoints not stated | Next slice C |
| CR-06.10 | `PARTIAL` | `quality.md` ordinary-document selection; no change-kind table | Next slice C |
| CR-07.01 | `KEEP` | `registry.json` README navigation; `tests/test_readme_navigation.py` | none |
| CR-07.02 | `KEEP` | `registry.json` document language; `tests/test_document_language.py` | none |
| CR-07.03 | `PROCESS` | Direct prose enforced by semantic review | none |
| CR-07.04 | `PARTIAL` | A link-only section passes `_substantive_section_body` | Next slice C: one negative case |
| CR-07.05 | `PARTIAL` | Operations guides, policies and runbooks split by role | No duplicate-procedure survey recorded |
| CR-07.06 | `KEEP` | `98.templates` appears only in a Task row | none |
| CR-07.07 | `PARTIAL` | Guide template names the four Diátaxis modes | Operator decision on further fields |
| CR-08.01 | `EXTERNAL` | ADR-0039, ADR-0040 and the Archive catalogue; comparison needs the other repositories | none |
| CR-08.02 | `KEEP` | ADR-0039; SPEC-0122 Task unit count | none |
| CR-08.03 | `PARTIAL` | Seven units removed; 57 kept for consumers | Operator decision on consumer migration |
| CR-08.04 | `KEEP` | SPEC-0122 EVD-004 isolated recovery; `tests/test_archive_recovery.py` | none |
| CR-08.05 | `KEEP` | `document-lifecycle.md` Plan Promotion; `document-authoring.md` successor citation | none |
| CR-08.06 | `KEEP` | SPEC-0122 added no permanent pipeline | none |
| CR-08.07 | `KEEP` | `document-lifecycle.md` dispositions; Archive disposition tests | none |
| CR-09.01 | `PARTIAL` | Requirement and architecture pairs cover four areas | Next slice B: area list in Stage 02 README |
| CR-09.02 | `PARTIAL` | Architecture template lacks risks, glossary, runtime and cross-cutting prompts | Next slice B |
| CR-09.03 | `PARTIAL` | Only AD-0007 traces quality scenarios to evidence | Next slice B |
| CR-09.04 | `EXTERNAL` | Other areas live in the other repositories; acceptance needs the cluster | none |
| CR-09.05 | `GAP` | No C4 view in `docs/02.architecture/descriptions/` | Next slice B |
| CR-09.06 | `PARTIAL` | ADR template and reciprocal supersession check; no lineage negative tests | Next slice B |
| CR-09.07 | `GAP` | No arc42 coverage note | Next slice B |
| CR-10.01 | `PARTIAL` | `scripts/validation/registry.json` lanes; no single leaf table | none |
| CR-10.02 | `KEEP` | `quality.md` separate rules by input and failure meaning | none |
| CR-10.03 | `KEEP` | `tests/test_qa_runner.py` index and source non-mutation | none |
| CR-10.04 | `KEEP` | `quality.md` ordinary-document selection | none |
| CR-10.05 | `PARTIAL` | `quality.md` delivery ownership table; no deploy workflow | none |
| CR-10.06 | `DONE_THIS_CYCLE` | SPEC-0123, PR #177 | none |
| CR-10.07 | `PARTIAL` | `quality.md` result vocabulary; owner-accepted risk in `.github/repository-surface.md` | none |
| CR-10.08 | `PARTIAL` | Lifecycle conformance tests; template drift case absent | Next slice C |
| CR-11.01 | `PARTIAL` | SPEC-0117, SPEC-0118, SPEC-0120 retirement rounds | No fresh enumeration this cycle |
| CR-11.02 | `KEEP` | `quality.md` QA admission and retirement | none |
| CR-11.03 | `PARTIAL` | SPEC-0117 fixture removals | No per-fixture cost inventory |
| CR-11.04 | `PARTIAL` | `quality.md` measure before claiming | Timing evidence absent in SPEC-0117 and SPEC-0118 |
| CR-11.05 | `PARTIAL` | Dispositions in each Spec's Task | Acceptable without a new ledger |
| CR-12.01 | `EXTERNAL` | Branch protection here; other repositories unobserved | none |
| CR-12.02 | `DONE_THIS_CYCLE` | `.github/rulesets/main-protection.md` read-backs; GET on 2026-10-27 | none |
| CR-12.03 | `PARTIAL` | Base-SHA tooling; `independent-review` App check | Candidate commit not documented |
| CR-12.04 | `KEEP` | `ci.yml` least privilege; `tests/test_validate_github_actions_security.py` | none |
| CR-12.05 | `PROCESS` | `quality.md` NOT_RUN and DEFER; SPEC-0121 operator-run evidence | none |
| CR-13.01 | `KEEP` | `.agents/governance/git.md` branch and integration routing | none |
| CR-13.02 | `KEEP` | `.gitmessage`, commitizen, `tests/test_commit_contracts.py` | none |
| CR-13.03 | `KEEP` | `core.hooksPath` `scripts/githooks`; `tests/test_chained_git_hooks.py` | none |
| CR-13.04 | `KEEP` | `tests/test_chained_git_hooks.py` push stdin and exit codes | none |
| CR-13.05 | `PARTIAL` | `scripts/release.py`, `tests/test_release.py`; no release yet | Operator decision: first release |
| CR-13.06 | `KEEP` | `tests/test_release.py`; immutable tag rulesets | none |
| CR-13.07 | `GAP` | No dated branch-strategy comparison | Next slice B: ADR |
| CR-14.01 | `PARTIAL` | Issue templates; `.github/repository-surface.md` ownership split | Issues unused; Projects unobserved |
| CR-14.02 | `PARTIAL` | No projection exists | none |
| CR-14.03 | `EXTERNAL` | Projects need `read:project` and an operator choice | none |
| CR-15.01 | `KEEP` | Thin `AGENTS.md` and `CLAUDE.md`; `agent-execution.md` | none |
| CR-15.02 | `PARTIAL` | `m0003` provider status table | Per-file support rows absent |
| CR-15.03 | `KEEP` | `model-selection.md`; provider bindings | none |
| CR-15.04 | `PARTIAL` | `.claude/provider.md` precedence; local settings ignored | Output-style scope not stated |
| CR-15.05 | `PARTIAL` | Fail-closed pre-edit guard; `tests/test_k8s_pre_edit_hook.py` | Duplicate-hook cases untested |
| CR-15.06 | `GAP` | No MCP configuration and no recorded non-use | Fixed here: provider notes |
| CR-15.07 | `PARTIAL` | No IDE configuration tracked | Fixed here: non-adoption recorded |
| CR-15.08 | `PARTIAL` | Independent review App check uses no model API | Fixed here: test-case generation non-adoption recorded |
| CR-15.09 | `KEEP` | SPEC-0114; `.claude/settings.json`; `.codex/config.toml` | none |
| CR-15.10 | `KEEP` | `.claude/skills` links to `.agents/skills`; `validate-agent-governance.py` | none |
| CR-15.11 | `GAP` | Four local agent files were not ignored | Fixed here: `.gitignore` |
| CR-15.12 | `PARTIAL` | `m0009` comparison; no role adopted | Operator decision |
| CR-15.13 | `PARTIAL` | `work-lifecycle.md`; `quality.md` handoff | Run and permission-decision fields not captured |
| CR-15.14 | `PARTIAL` | Resume decision; memory idempotency tests | Late-result and cancel cases untested |
| CR-16.01 | `PARTIAL` | SPEC-0115 Task 0002 skill status | Some skills have no status; user-scope skills external |
| CR-16.02 | `PROCESS` | Per-Task skill notes | none |
| CR-16.03 | `PARTIAL` | 18 skills with `SKILL.md` | Three skills lack a verification section |
| CR-16.04 | `PARTIAL` | `.agents/evaluations/results.md` has no admitted cycle | none |
| CR-17.01 | `KEEP` | `scripts/workspace_memory.py`; SPEC-0109 evidence | none |
| CR-17.02 | `KEEP` | `context-and-memory.md` tiers; `TIER_LIMITS` | none |
| CR-17.03 | `KEEP` | No delete API; backup keeps all revisions (test) | none |
| CR-17.04 | `KEEP` | Default query excludes stale sources (test) | none |
| CR-17.05 | `KEEP` | Capacity limits and refusal test | none |
| CR-17.06 | `PARTIAL` | Concurrent-writer tests; cross-provider writes unobserved | Live provider observation external |
| CR-17.07 | `PARTIAL` | Backup verified; restore never tested | Fixed here: restore test and procedure |
| CR-17.08 | `PARTIAL` | Native memory disabled; subagent memory directories not ignored | Fixed here: `.gitignore`; projection keys already exact-set checked |
| CR-17.09 | `PARTIAL` | SPEC-0109 own store; SPEC-0124 recorded ai-memory | Operator decision |
| CR-17.10 | `PARTIAL` | No decay or delete in the own store | Moot while nothing is adopted |
| CR-17.11 | `PARTIAL` | No hook collection exists | Fixed here: non-adoption recorded |
| CR-18.01 | `KEEP` | `work-lifecycle.md` no business deadline | none |
| CR-18.02 | `KEEP` | `work-lifecycle.md` bounded attempts | none |
| CR-18.03 | `KEEP` | `context-and-memory.md`; `model-selection.md` | none |
| CR-18.04 | `PARTIAL` | `model-selection.md` provider limits | GitHub API limits not documented |
| CR-18.05 | `KEEP` | No nested retry in delivery scripts | none |
| CR-18.06 | `EXTERNAL` | Needs live provider limit responses | none |
| CR-19.01 | `DONE_THIS_CYCLE` | Seven `_workspace` READMEs tracked | none |
| CR-19.02 | `PARTIAL` | `_workspace/diagnostics/README.md` implied a producer | Fixed here: no automatic producer stated |
| CR-19.03 | `PARTIAL` | `_workspace/README.md` promotion rules | No sanitizer step |
| CR-19.04 | `PARTIAL` | `.worktrees/` ignored; `git.md` worktree safety | Unregistered folders under `.worktrees/` need an operator decision |
| CR-20.01 | `KEEP` | REQ-0004 cites public ISO overviews without a conformity claim | none |
| CR-20.02 | `PARTIAL` | REQ-0004 quality scenarios for this repository | Other repositories external |
| CR-20.03 | `KEEP` | Quality content stays in REQ-0004 | none |
| CR-21.01 | `KEEP` | SPEC-0116 non-goals: no model API in CI | none |
| CR-21.02 | `KEEP` | SPEC-0116 head-bound review check | none |
| CR-21.03 | `KEEP` | `agent-execution.md` scoped policy repair | none |
| CR-21.04 | `KEEP` | `approval-and-safety.md`; `.claude/provider.md` | none |
| CR-21.05 | `PARTIAL` | `agent-execution.md` external text is data | No injected-instruction negative fixture |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CS-001](../spec.md#success-criteria--verification-plan) | Record the 148-CR status table | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-CS-002](../spec.md#success-criteria--verification-plan) | Fix the local gaps | platform | in-progress | PASS | EVD-004 closes EVD-002 |
| WORK-003 | [VAL-CS-003](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Status table and independent sample | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Ignore checks and restore test | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-CS-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-CS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Ignore checks and restore test | Branch `docs/cr-status-and-local-gaps`: `git check-ignore --no-index` for each new entry, `python3 -m unittest tests.test_workspace_memory`, `pre-commit run detect-secrets --hook-stage manual` on m0012, NIST SP 800-218 Rev. 1 pages read on 2026-10-27 | PASS | `CLAUDE.local.md`, `AGENTS.override.md`, `.claude/agent-memory/` and `.codex/config.local.toml` were not ignored before the change and are after it. The new restore test damages the store, copies the backup over it, and reads the same records with an `ok` integrity check; 26 tests pass. Provider notes record MCP, IDE, test-generation and hook-collection non-adoption; the diagnostics README no longer implies a producer; `quality.md` names candidate, verified and delivered commits and stale results; the research contract records internal-decision non-applicability. NIST lists SSDF 1.2 as an initial public draft (2025-12-17, comments closed 2026-01-30) and `r1/final` returns 404, recorded in m0012. The m0012 baseline line numbers moved first in `0ec80f29`, and the secret scan passes | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CS-001](../spec.md#success-criteria--verification-plan) | pending | none | Status table and review remain | platform |
| [VAL-CS-002](../spec.md#success-criteria--verification-plan) | pending | none | Local fixes remain | platform |
| [VAL-CS-003](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.gitignore`, `.agents/governance/quality.md`,
  `.agents/governance/context-and-memory.md`, `.claude/provider.md`,
  `.codex/provider.md`, `_workspace/diagnostics/README.md`,
  `docs/90.references/research/0001-workspace-engineering/README.md`,
  `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`,
  the m0012 line numbers in `.secrets.baseline` and
  `tests/test_workspace_memory.py`.
- **Forbidden Paths**: provider settings, permission rules, credentials,
  `.worktrees/` content and the other three repositories.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended. Push, pull request and merge follow RUN-0013.
- **Static Validation**: focused tests and `qa.py staged` on the exact index.
- **Live Validation**: none; the hosted checks on the pull request.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
