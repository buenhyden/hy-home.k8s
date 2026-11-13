---
title: "W03 YAML 1.2.2 Frontmatter Loader"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0183-TSK-0001"
parent_ids: ["SPEC-0183-PLAN-0001"]
---

# Task: W03 YAML 1.2.2 Frontmatter Loader

## Overview

This Task records handoff W03-H26, the YAML 1.2 frontmatter loader, for [SPEC-0183](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-yaml-frontmatter-loader` from `534ddae7` (the SPEC-0182 closure; PR #247 open), stacked on that PR and checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D29 (YAML 1.2.2), W03-H17 and W03-H26, and EVD-018; SPEC-0181's `frontmatter_dialect` and its dialect tests.
- **Dialect strings:** `frontmatter_dialect` keeps the target `YAML 1.2.2` and records the current dialect as `YAML 1.2 (ruamel.yaml 0.19.1, with stated refusals)`; the dialect test is updated to these strings and asserts the target.
- **Amendment of W03-H26:** W03-H26 named four loaders with unchanged timestamp rules; the read found five frontmatter loads, and this package keeps timestamps as text in all five.
- **Accepted deviations from YAML 1.2 recorded here:** `ruamel.yaml` accepts the numeric forms `1_000` and `0b11`, which the loader keeps; every explicit tag, including core tags such as `!!str`, is refused.
- **User action:** before the implementation commit the user installs the library into the local validation environment with the command in the Git policy.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | Loader module, five call sites, tests, one-time comparison. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | Lock, dialect record, policy text; the user's install; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007; implementation commit `9dc6bc53` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `9c15185b…` and plan.md `c692e5e2…`, with scratch environments for `ruamel.yaml` 0.18.17 and 0.19.1, a `pip-compile` regeneration of the lock and a comparison of all tracked frontmatter blocks; 2026-11-13 | FAIL | REJECT: BLOCK the hook does not compare the environment with the lock, so a missing library fails as an import in the validators; BLOCK the drafts conflicted with SPEC-0181's dialect record and tests; FIXes on the call sites' diagnostics, refusals ruamel does not make by default, the pin, the one-time comparison, routing and README rows, CI checks and the risk scoring. The reviewer found 248 of 248 frontmatter blocks equal and the lock regeneration adding one entry. | no | none |
| EVD-002 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"aede0a841e7f1df061a05ca02c24b6399222ee7b8402248844c5b938f7468a11","plan_sha256":"73f46abfc621b3303bd959c2a495faf1dcae8f263d3a786270ee08c7e5ff03c1"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed over spec.md `19b18b0d…`; verdict APPROVE with NITs. The author then added the SPEC-0181 dependency sentence and the explicit-tag wording to the Spec as two of those NITs, giving the bytes named here; the other NITs are recorded under Inputs. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0183 approval question naming spec.md aede0a84 and plan.md 73f46abf dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0183","SPEC-0183-PLAN-0001"],"reviewed_spec_sha256":"aede0a841e7f1df061a05ca02c24b6399222ee7b8402248844c5b938f7468a11","reviewed_plan_sha256":"73f46abfc621b3303bd959c2a495faf1dcae8f263d3a786270ee08c7e5ff03c1","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | One loader, five call sites, tests and the one-time comparison, red then green | Working tree over `a8da75e5`; implementer quality-engineer subagent in a scratch environment built from the regenerated lock, re-checked by the author; 2026-11-13 | PASS | Red: the new loader tests failed on import against the base and, with only the module added, 12 call-site and Hookify cases failed. Green: `tests.test_frontmatter_yaml` 23 OK and `tests.test_frontmatter_key_contract` 50 OK. `scripts/frontmatter_yaml.py` loads one block with `ruamel.yaml` 0.19.1 (safe, pure, YAML 1.2, one pass) and refuses with reason codes `duplicate-key` (with the key), `directive`, `anchor`, `alias`, `tag`, `non-scalar-key`, `merge-key`, `multi-document`, `too-deep` and `invalid-yaml`; timestamps stay text; a missing library names the lock and the Git policy command. Call sites keep their diagnostics (`FM-DUPLICATE-KEY` with the key, the lifecycle unique-key message, `AGENT-NATIVE-METADATA`, links treat a refusal as no frontmatter, Hookify reports the reason code); newly refused anchors, tags and non-scalar keys are recorded per call site; the `agents/openai.yaml` and `quality.py` workflow loads stay on PyYAML. One-time comparison: 249 tracked frontmatter blocks, 0 refused, 0 differences. | yes | none |
| EVD-005 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Lock, dialect record, policy text and the user's install | Staged diff over `a8da75e5` | PASS | `.github/requirements/ci-validation.in` gains `ruamel.yaml==0.19.1`; the lock regenerated with its header command adds exactly one hashed entry and moves no pin; `validate-ci-python-contract.py` and `validate-github-actions-security.py` pass. `frontmatter_dialect` names the one loader for all five entries with timestamps kept as text, current `YAML 1.2 (ruamel.yaml 0.19.1, with stated refusals)`, target `YAML 1.2.2` asserted by the dialect test. `document-authoring.md` 3.20.0 and `scripts/README.md` 0.14.0. The user installed the lock into the local validation environment on 2026-11-13 (`Successfully installed ruamel-yaml-0.19.1`). No registry baseline line moved. | yes | none |
| EVD-006 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Implementer runs in the scratch environment, then the commit hooks over the exact index, 2026-11-13 | PASS | The four strict document validators give output byte-identical to the before run at `a8da75e5`. Suites: `document` 667 (3 skipped), `document-lifecycle` 24, `agent-governance` 105, `ci-metadata` 87, `validation-routing` 173, `tooling` 166 OK; `validate-affected-surfaces.py` PASS; `ruff check` and `ruff format --check` clean; markdownlint 0 issues; `graphify update .` done. The first commit attempt failed exact-index QA with `SURFACE-PATH-AMBIGUOUS` on `scripts/frontmatter_yaml.py` (the new exact route and the `scripts` surface regex both matched); the author added the module to that regex's exclusion list beside `document_contracts.py`, after which `validate-affected-surfaces.py` reported `ambiguous=0`, and exact-index QA runs in the commit hooks of the implementation commit. | yes | none |
| EVD-007 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 15 files over `a8da75e5` | PASS | Risk class `medium` (five validators, one new dependency in the CI lock, tests). Checklist: scope matches the Spec; non-frontmatter YAML loads untouched; one exact pin, hashed, binary-only wheel with no required dependency, released 2026-01-02; W03-H26 amended as recorded under Inputs; no document body or frontmatter value changed; no secret read; recovery is reverting the implementation commit and the lock line. No permission, trigger, hook or workflow file changed. | yes | none |
| EVD-008 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. This package closes W03-H26. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0183 criterion question naming implementation commit `9dc6bc53`) | platform |
| [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0183 criterion question naming implementation commit `9dc6bc53`) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy and `frontmatter_dialect` in the registry (Plan Promotion row). No new handoff arises. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Code comments that name SPEC-0183 use it as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, an evidence row and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: non-frontmatter YAML loaders, `.github/workflows/`, document bodies, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`; installing into the user's environment
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, `validate-ci-python-contract.py`, `validate-github-actions-security.py`, `document`, `document-lifecycle`, `agent-governance`, `ci-metadata`, `validation-routing` and `tooling` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); implementation commit `9dc6bc53`. The user accepted both criteria on 2026-11-13, and the approval of commit, push and PR covers the package exit (EVD-008); this package closes W03-H26. Risk class `medium`. Next owner: W03 for SPEC-0184.
