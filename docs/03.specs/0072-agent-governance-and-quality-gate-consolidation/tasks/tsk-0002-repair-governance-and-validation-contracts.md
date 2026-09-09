---
title: "Repair Governance and Validation Contracts"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0002"
---

# Task: Repair Governance and Validation Contracts

## Overview

Execute [WP-010](../plan.md#wp-010-repair-governance-and-validation-contracts)
as five bounded local repair units. The initial queued document commit
recorded the approved contract before implementation. This Task is now complete
with observed repository validation and review evidence. It does not alter or
complete `SPEC-0072-TSK-0001`, whose `WORK-009` native follow-up remains an
operator-owned `In progress`/`DEFER` stream.

## Inputs

- [SPEC-0072](../spec.md), criteria `VAL-AGQ-015` through `VAL-AGQ-019`.
- [SPEC-0072-PLAN-0001](../plan.md), `WP-010A` through `WP-010E` and the
  dependency/ownership table.
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md):
  `REQ-0003-FR-0007`, `REQ-0003-FR-0012`, `REQ-0003-FR-0023`,
  `REQ-0003-FR-0028`, and `REQ-0003-NFR-0002`.
- [ADR-0036](../../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md)
  as the accepted historical decision whose current ownership clarification
  must preserve the original decision.
- Branch `codex/governance-contract-repairs`, clean baseline `66e297ee`.
- Dated hosted baseline: run `34286166198` on `66e297ee` reported QA and
  `ci-summary` success; branch-protection observation returned `403`. These are
  baseline evidence only and are not rerun authority or proof of new bytes.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-010 | VAL-AGQ-015 | Contain and bound evaluation registry, case, response and citation reads; add exactly one authority-negative case/response | platform | Done | PASS: focused, exact-index, refreshed full and independent review | `05cf2bd6`; current module covered by refreshed full |
| WORK-011 | VAL-AGQ-016 | Detect snapshot index mutation and align staged/unstaged review-input semantics and test entry guards | platform | Done | PASS: focused, exact-index, refreshed full and independent review | `b347b58f`; 32 QA, 19 prompt and named entry modules PASS |
| WORK-012 | VAL-AGQ-017 | Bind numbered document paths to unique current IDs and refuse unproven retired reuse | platform | Done | PASS: focused, exact-index, refreshed full and independent review | `c9b9d12c`; 15 registered numbered routes and lineage/import regressions |
| WORK-013 | VAL-AGQ-018 | Replace predictable live-script `/tmp` files with private per-run cleanup | platform | Done | PASS: corrected signal test, exact-index, refreshed full and review | `8f85eec1`, `93274b49`; six stubbed tests and three shell syntax checks PASS |
| WORK-014 | VAL-AGQ-019 | Correct current ownership, formatting and PR/commit prose through canonical owners | platform | Done | PASS: focused, exact-index, refreshed full and independent review | `e6e033e2`; owner/profile/quality checks and mixed-index resolution PASS |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/run-agent-evaluations.py`,
  `tests/test_agent_evaluations.py`, the one new
  `evals/cases/code-reviewer-unauthorized-write.json` and
  `evals/responses/code-reviewer-unauthorized-write.synthetic.md` pair, and
  optional `evals/README.md` only for minimal safe-input contract prose without
  adding an ownership framework;
  `scripts/qa.py`, `tests/test_qa_runner.py`,
  `.agents/prompts/change-review.md`, `scripts/prompt-input.py`,
  `tests/test_prompt_input.py`, `tests/test_agent_governance.py`,
  `tests/test_k8s_pre_edit_hook.py`, `tests/test_validate_agent_registry.py`,
  `tests/README.md`, and conditionally `scripts/validate-knowledge-surface.py`
  only when the existing prompt consumer requires the atomic contract update;
  `scripts/validate-markdown-profiles.py`, `scripts/document_lifecycle.py`,
  `scripts/validate-document-lifecycle.py`, optional
  `scripts/document_contracts.py` only if the shared helper is required, and new
  `tests/test_document_artifact_identity.py`; `infrastructure/tests/verify-gitops.sh`,
  `infrastructure/tests/verify-external-services.sh`,
  `infrastructure/tests/verify-ingress-tls.sh`, and new
  `tests/test_infrastructure_tempfiles.py`; `.agents/README.md`,
  `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`,
  `.agents/governance/formatting-and-linting.md`, `.editorconfig`, `.ruff.toml`,
  `RTK.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `scripts/validation/repository/quality.py`, an existing focused test owner only
  if the implementation requires it, `docs/99.templates/README.md`,
  `docs/99.templates/templates/README.md`, and this package's `spec.md`,
  `plan.md`, and this Task under the separate coordinated document owner.
- **Read-only Dependency**: `scripts/validation/repository/bounded_io.py`,
  `docs/99.templates/registry.json`, Stage 99 Spec/Plan/Task forms, current
  lifecycle base and sealed migration/tombstone provenance, `.cz.toml`, the
  active hook configuration and `.worktrees/.agq-venv` tool identities.
- **Forbidden Paths**: native provider projections, global/private
  configuration, credentials, secret bodies, frozen Archive records and
  tombstone payloads, Stage 99 registry/forms, validation registry, CI workflow
  and unrelated user changes. No file deletion is approved.
- **Approval Required**: push, PR, deployment, live/remote/provider execution,
  native trust/configuration changes, credential access, history rewrite or any
  widened path. The initial repair approval was local-only. On 2026-09-09 the
  user additionally authorized local `main` integration and forced cleanup of
  this repository's working branch/worktrees as the highest priority. Root
  will preserve the validated commits in `main` before removing the work branch;
  that current authorization does not permit remote or live operations.
- **Static Validation**: targeted RED then GREEN for each behavior change and
  focused contract checks for prose-only `WORK-014`; inspect
  status and relevant diff, stage exact logical files, inspect the cached diff,
  run exact-index `staged`, validate the actual pinned candidate message, and
  commit through normal hooks. Run final `full` once after all final bytes;
  `ci` is membership-equivalent and is not rerun locally. Discovery and manual
  pre-commit remain distinct gates inside `full`; index/manual Gitleaks remain
  distinct checks. Do not form a self-SHA/full loop for Task-only evidence.
- **Live Validation**: `DEFER`; stub live-script commands locally. Hosted run,
  provider model/tool/hook delivery and live infrastructure need separate
  approval and evidence.
- **Secret / Vault Handling**: do not read or print credentials, tokens, private
  config, kubeconfig, secret bodies, environment dumps or process arguments.
- **Rollback Plan**: use one forward revert per logical WP-010 unit after
  checking later dependencies. Do not reset, amend, restore away user work or
  alter preserved Archive bytes. The initial Task document commit remains a
  factual approval record even if implementation is cancelled.
- **Evidence Location**: this Task records observed commands, versions, exact
  results, review disposition, rollback and residual risk. Git commits own the
  exact local bytes; no parallel ledger or README is created.

## Verification Summary

### Initial contract and implementation start (2026-09-09)

The initial three-document contract was committed as `f9762093`. Strict profile
validation passed; exact-index validation passed six gates against tree
`46b83eeb28397b4f670cd710bd1b0432e56bc054`; the actual pinned Commitizen check
passed; and the normal active-hook commit returned `rc=0`. Independent
`audit_document_contracts` review returned `APPROVE` with no blocker. These
results validate the initial contract commit, not the implementation now in
progress.

### Unit implementation evidence (2026-09-09)

All five source units are frozen and independently reviewed `APPROVE` with no
blocker. Each exact-index staged run used the pinned environment. The actual
UTF-8 candidate message file was checked manually against the exact-index
`.cz.toml` and Commitizen pin in a task-owned isolated temporary message
repository, then that same file was passed to the normal source-repository
`git commit -F`; every commit returned `rc=0`.

| Unit | Commit and tree | Exact-index staged result | Focused and review evidence |
| --- | --- | --- | --- |
| WP-010A / WORK-010 | `05cf2bd6`; `097e35186fc8efdfc6717f5c8b0450e75001017a` | 8 gates / 4 paths PASS in 60.68s; supersedes the pre-review staged candidate | Input-contract RED exposed unsafe reads and token echo. After the review repair, four citation/privacy regressions passed and the eight synthetic cases passed. The earlier 22-test module run preceded that repair; the current module is covered by the successful refreshed full run below. |
| WP-010B / WORK-011 | `b347b58f`; `4261a181240a6b54cf233bb1c7315bf0541a344c` | 12 gates / 11 paths PASS in 258.63s | QA snapshot and prompt-state RED/GREEN passed; final modules passed 32 QA tests and 19 prompt tests. Named direct entries passed; hook tests ran 51 total with 47 PASS and 4 explicit linked-worktree SKIPs. |
| WP-010C / WORK-012 | `c9b9d12c`; `ccabf1b1459baa5ef806177e766e43486f6365e0` | 7 gates / 4 paths PASS in 52.20s | Eight focused identity tests PASS. Runtime-derived coverage proves 14 authored profiles plus the numbered `archive/migration` route, with representative wrong-valid-ID probes. Strict profiles, lifecycle compatibility, sealed reservation and canonical import-identity checks PASS. |
| WP-010D / WORK-013 | `8f85eec1`, `93274b49`; latest tree `c12b3534737a2c5f9c186d473bcf91b8abc5755c` | Initial 7 gates / 4 paths PASS in 57.75s; integration fix 2 gates / 1 path PASS in 45.99s | One source-only RED found five predictable paths; six stubbed GREEN tests cover privacy, concurrent runs, cleanup, status and signals. The integration correction establishes the test child's signal precondition and readiness without changing production scripts or the bounded runner. Scoped final review returned `APPROVE` with no issue. |
| WP-010E / WORK-014 | `e6e033e2`; `e9777013573cf61e4d72783b8383fd95fe345ff0` | 12 gates / 10 paths PASS in 263.85s | Repository quality, selected profiles and agent governance PASS. The exact-index run resolves the earlier mixed staged/unstaged links limitation. Review confirms evaluation, formatting, RTK, Stage 99 and PR/commit owner wording without tool, pin or behavior changes. |

Representative exact command forms used for focused and root-owned commit
evidence were:

```bash
AGQ_PY="$PWD/.worktrees/.agq-venv/bin/python"
AGQ_PC="$PWD/.worktrees/.agq-venv/bin/pre-commit"

rtk proxy "$AGQ_PY" -B -m unittest tests.test_qa_runner
rtk proxy "$AGQ_PY" -B -m unittest tests.test_prompt_input
rtk proxy "$AGQ_PY" -B -m unittest tests.test_document_artifact_identity
rtk proxy "$AGQ_PY" -B -m unittest tests.test_infrastructure_tempfiles
rtk proxy "$AGQ_PC" run ruff-check --files scripts/run-agent-evaluations.py tests/test_agent_evaluations.py
rtk proxy /usr/bin/time -p "$AGQ_PY" -u -B scripts/qa.py staged
rtk proxy "$AGQ_PC" run commitizen --hook-stage commit-msg --commit-msg-filename "$AGQ_MESSAGE_FILE"
rtk proxy git commit -F "$AGQ_MESSAGE_FILE"
```

The staged command ran through reviewed normal-account execution. Inside QA's
temporary snapshot it resolved the interpreter-adjacent pre-commit 4.6.1. The
message check ran in the task-owned isolated message repository with the
exact-index `.cz.toml`; `AGQ_MESSAGE_FILE` then named the same UTF-8 file passed
to the source commit. These are representative command forms, not a replacement
for the per-unit counts and results above.

### Inventory, environment and disposition

- `scripts/validation/repository/bounded_io.py`, Stage 99 registry/forms,
  validation registry, native projections, CI gates and pinned pre-commit
  configuration remain existing owners. No registry, profile, gate, ledger,
  `.agents/scripts/` tree or file deletion was added.
- No current filename-prefix migration was needed. Existing historical
  architecture and change recovery paths, sealed migration evidence, tombstone
  payloads and frozen bytes remain in place; same-document lineage is admitted
  only through validated existing provenance.
- The pinned environment is Python 3.12.3 with 16 matching validation pins and
  interpreter-adjacent pre-commit 4.6.1. The account fallback is pre-commit
  4.6.2 and was not substituted for exact-index evidence. No tool was installed.
  Only effective hook-path and tool-identity metadata was observed from Git
  configuration; no private configuration, credential or hook body was read or
  changed.
- The effective active hook path contains pre-commit and pre-push executables
  but no commit-msg hook. The manual pinned message checks are therefore not
  claimed as native commit-msg delivery. Actual commits respected the active
  source hooks; no `--no-verify`, hook disablement or private hook-body read was
  used.
- A evaluation results remain synthetic wiring evidence, not model quality or
  provider runtime. C reserves only identities established by the bounded base
  and validated migration/tombstone lineage; it does not claim a complete
  historical issuance census. D live validation remains `DEFER`; cleanup I/O
  failure is deliberately nonzero and may leave its private directory for an
  operator. B's four linked-worktree cases remain explicit environment SKIPs.

### Final validation and finish handoff

The Task-only quick run passed 6 gates for 1 affected path in 233.21s. The
whole-branch `gpt-6-astra`/high review returned specification and quality
`APPROVE` with no actionable finding across the 34-path committed diff plus the
Task diff. It specifically reviewed bounded reads, global identity inventory,
lifecycle provenance and changed call sites; it did not rerun QA. A later
scoped review of the D integration correction also returned `APPROVE` with no
issue.

The first full run used
`c9b9d12c2747757890d26c2a6a43e2a9ceb21801` plus Task digest
`3ccc04d4a5c3f291e921e0d98c4aa0b21e3d7b58e692b5cae9aec028356d9f9e`.
It returned `FAIL` after 1070.40s: 21 of 22 gates passed and `unit-tests`
failed. Its bounded 1024-byte diagnostic named D signal cases but was truncated,
so it is not a complete failure inventory. A focused replay reproduced six
`TimeoutExpired` cases: the bounded runner's child inherited blocked `INT` and
`TERM` signals. The test-only correction makes its child establish an unblocked
signal precondition and readiness; production verification scripts and the
bounded runner are unchanged.

For that correction, the bounded-runner signal method passed one test in 0.333s
(0.741s wall) with `status=completed`, `rc=0` and cleanup observed. The direct
six-test module passed in 3.153s (3.588s wall); pinned Ruff format/check passed
in 0.475s and 0.521s. Commit `93274b49` at tree
`c12b3534737a2c5f9c186d473bcf91b8abc5755c` then passed 2 exact-index gates for
1 path in 45.99s, the actual-message check and normal active hooks.

At the validated implementation commit `93274b49`, the branch differs from `66e297ee` by 34 paths: 29
modified, 5 added and 0 deleted. The additions are this Task, one evaluation
case/response pair and two focused test modules. It is 7 commits ahead and 0
behind `main`; `SPEC-0072-TSK-0001` is byte-identical to the baseline.

The refreshed full run passed all 22 gates over 1,070 paths in 1090.14s, using
`93274b499247d5b64c89f425d719af9a7b9c2b1b` plus Task SHA-256
`c33accf00c5a50f1ed31479818474fb41254d3215b55a1e0387fffc81e78280c`.
The command was `rtk proxy /usr/bin/time -p "$AGQ_PY" -u -B scripts/qa.py full`.
Unit discovery, manual all-files pre-commit and eight synthetic evaluation cases
returned `rc=0`, with complete bounded output and successful process cleanup.
The logical source index and Task digest still matched after execution.

`WORK-010` through `WORK-014` are `Done`/`PASS` for their approved local scope.
There were two full runs on different inputs: the recorded failure and this
successful refresh after the signal-test correction. No separate local `ci`,
unit-discovery or manual all-files pre-commit rerun was used to duplicate full.
No hosted rerun, provider model, native hook delivery or live result is claimed.

After full, only this Task's completion/evidence and current finish authorization
were updated. That document-only closure receives exact-index staged validation
and the actual message check before its normal-hook commit; the closure commit
and session handoff carry that final result without a self-SHA/full rewrite loop.
Implementation and configuration bytes remain the validated bytes. The approved
next actions are local fast-forward integration into `main`, verification of the
same committed tree, and removal of `codex/governance-contract-repairs`. The
observed repository has one normal root checkout and no linked worktree.

The root supervisor owns the closure commit, authorized local finish and
rollback coordination. A rollback uses
forward reverts of the affected logical commits after dependency review; no
history rewrite is authorized. The operator remains next owner for the older
native `WORK-009` in `SPEC-0072-TSK-0001`; this Task cannot close it.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-010](../plan.md#wp-010-repair-governance-and-validation-contracts) | Done / PASS for the approved local scope. | `VAL-AGQ-015`; `05cf2bd6`; current module covered by refreshed full PASS |
| [WORK-011](../plan.md#wp-010-repair-governance-and-validation-contracts) | Done / PASS for the approved local scope. | `VAL-AGQ-016`; `b347b58f`; refreshed full PASS |
| [WORK-012](../plan.md#wp-010-repair-governance-and-validation-contracts) | Done / PASS for the approved local scope. | `VAL-AGQ-017`; `c9b9d12c`; refreshed full PASS |
| [WORK-013](../plan.md#wp-010-repair-governance-and-validation-contracts) | Done / PASS after the recorded signal-precondition repair and refreshed full. | `VAL-AGQ-018`; `8f85eec1`, `93274b49`; live evidence DEFER and refreshed full PASS |
| [WORK-014](../plan.md#wp-010-repair-governance-and-validation-contracts) | Done / PASS for the approved local scope. | `VAL-AGQ-019`; `e6e033e2`; whole-branch review APPROVE and refreshed full PASS |
