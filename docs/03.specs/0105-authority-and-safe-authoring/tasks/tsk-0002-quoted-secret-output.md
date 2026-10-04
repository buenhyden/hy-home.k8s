---
title: "Quoted Secret Output Scanner Follow-up"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0002"
---

# Task: Quoted Secret Output Scanner Follow-up

## Overview

The current user's explicit implementation request authorizes one bounded
follow-up to the completed SPEC-0105 implementation. Paired single- or
double-quoted `yaml`/`json` output values can miss the raw Secret command
scanner. This Task owns the follow-up state, observations and handoff; the
completed [prior Task](tsk-0001-authority-and-authoring.md) remains intact.

## Inputs

- [Spec](../spec.md) VAL-P01-002 and VAL-P01-006; [Plan](../plan.md) WP-002
  and WP-003.
- Intake snapshot: clean `codex/p01-authority-safety` at `d21f535`; current
  Secret rule in `scripts/validation/repository/quality.py` near line 2037 is
  consumed by the command scan near line 2139. Its inert-prohibition helper is
  also used by the direct-push scan. Existing focused regression owner is
  `tests/test_repository_quality_rules.py`.
- Independent read-only re-audit at that snapshot found this scanner gap.
  Approval and safety review found no new permission contradiction; the
  completed Spec/Plan may link a new authorized Task without reopening the
  completed prior Task. These findings identify work, not acceptance or
  authorization by the reviewers.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | VAL-P01-002 | Reproduce and repair quoted Secret output matching in the shared rule; retain inert prose grammar | quality-engineer | Completed | Focused checks and independent re-review accepted | Implementation and review evidence below |
| WORK-005 | VAL-P01-006 | Validate, obtain independent read-only review and commit local handoff | platform | In progress | Intake committed; implementation delivery pending | Intake command and commit evidence below |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validation/repository/quality.py`,
  `tests/test_repository_quality_rules.py`,
  `docs/03.specs/0105-authority-and-safe-authoring/spec.md`,
  `docs/03.specs/0105-authority-and-safe-authoring/plan.md` and
  `docs/03.specs/0105-authority-and-safe-authoring/tasks/tsk-0002-quoted-secret-output.md`
  only.
- **Forbidden Paths**: real Secret values, live state, remote repositories,
  native/provider trust settings, global configuration and frozen history.
- **Approval Required**: the user's current implementation request authorizes
  scoped reversible local authoring and logical commits. It grants no Secret
  read, live operation, remote push/PR/merge, archive disposition or destructive
  cleanup. The operator route in `.agents/governance/approval-and-safety.md`
  governs any separately protected action; none is planned here.
- **Static Validation**: demonstrate one failing quoted-output regression,
  then focused passing cases for `-o`/`--output` with space/equals and paired
  single/double quotes; retain raw-command rejection despite adjacent redaction,
  explicit inert Markdown prose allowance, runnable/comment denial, metadata
  jsonpath and ExternalSecret negatives. Run affected, exact-index staged and
  one final local full QA at the declared input snapshots. Validate each
  commit message through the current Commitizen contract.
- **Live Validation**: DEFER; no live command is authorized or needed.
- **Secret / Vault Handling**: synthetic command text only; no real Secret
  read, output or credential handling.
- **Rollback Plan**: forward corrective commit for the code/test change while
  preserving this Task and Git history; no reset or archive rewrite.
- **Evidence Location**: this Task alone owns actual commands, snapshots,
  results, review and residual limits.

## Verification Summary

Root preflight observed Python 3.12.3, pre-commit 4.6.1, RTK and
CI-pinned Kustomize v5.8.1 still installed at `/usr/local/bin/kustomize`
with the digest recorded in the prior Task. The effective hooks path remains
`scripts/githooks`; the runner retains its existing bounded envelope. The
existing pinned Conftest Docker fallback image was present locally; no pull
or new installation was required.
The default shell sandbox failed to start with `bwrap: loopback: Failed
RTM_NEWADDR`; bounded supported escalation enabled read-only inspection.
Independent read-only intake reviewer `/root/approval_trace` found one LOW
path-clarity issue in Allowed Paths; the exact repository-relative paths above
resolve it, with no remaining intake finding reported. No focused regression
or implementation-diff review had run at intake.
The superseded original-index staged QA was intentionally interrupted (exit
130) after the Task wording changed; it is not PASS evidence. The actual
`.git/COMMIT_EDITMSG` contained
`docs(governance): prepare quoted Secret output follow-up` and passed the
explicit pinned pre-commit Commitizen commit-msg check. Pre-commit stashed
and restored the unstaged Task without loss; its observed hash matched.
The command was `pre-commit run commitizen --hook-stage commit-msg
--commit-msg-filename .git/COMMIT_EDITMSG`; this explicit PASS is not evidence
that a workspace commit-msg hook was installed or delivered.

The final intake `rtk proxy python3 scripts/qa.py staged --base-ref HEAD`
compared the three-document index to base `d21f535`. All six required gates
passed: agent-governance, document-contract-registry, document-lifecycle,
links-and-owners, markdown-profiles and repository-quality. Scoped pinned
`pre-commit run --files` on the exact three documents passed all applicable
hooks, including Markdownlint, detect-secrets and gitleaks; nonapplicable
hooks remained SKIP. `git commit -F .git/COMMIT_EDITMSG` used the validated
message and existing hooks without unstaged drift. Intake commit
`c620f641872c0f4c1628a485ff31ca24a4c0d39d` has tree
`ff7d8a6d23c171b331a683a5a7fde6babd8086cb`.

Implementation author `/root/doc_guard_fix` first ran
`rtk proxy python3 -m unittest
tests.test_repository_quality_rules.RepositoryQualityRuleTests.test_secret_value_output_is_detected_with_or_without_namespace_flag
tests.test_repository_quality_rules.RepositoryQualityRuleTests.test_raw_secret_output_rejects_nearby_safety_claims`.
Before editing production code, its two methods had 12 subtest assertion
failures. Eleven exposed the target behavior: eight quoted-output misses,
two adjacent-redaction decisions and one fenced quoted-output miss. One
expectation treated malformed bare `--output=json'` text as a valid command;
review requires dropping that expectation. The same command passed both
methods on the first repair candidate. Its first method expanded to a
16-combination matrix of quote, output type and option form and passed as
one test method on that candidate, not as 16 separate unit tests.

The first candidate changed only the shared regex in
`scripts/validation/repository/quality.py` and regression cases in
`tests/test_repository_quality_rules.py`: 32 lines added, one removed across
the two files, with no new parser, API or prohibition grammar. Pinned Ruff
format and check passed those candidate bytes without mutation;
`git diff --check` passed. Their superseded SHA-256 values are
`4f44039487e0ee65be16ff56b9c58c7884251ec98f078d163f6dcff2ce7581ba`
for the quality source and
`37fc597f88060af7ec6caf600d0f050b1bdb406aefba0bf9f014e2e72b18e093`
for its test. These checks do not validate the next revision.

Independent reviewers `/root/secret_boundary_review` and `/root/guard_trace`
found two real regex regressions: the first candidate misses previously
recognized raw `-o yaml""` / `--output=json''` forms, and its quoted branch
misclassifies metadata `-o 'json'path='{.type}'` as raw JSON. The quality
author reproduced those findings with seven assertion failures across the
same two methods: two valid bare-plus-empty-quote misses, two quoted-jsonpath
false positives, two redaction-decision misses and one metadata-decision false
positive. The final candidate restores the existing bare-output branch and
requires a non-word character after a paired quoted output value. The same
two methods passed in 0.210 seconds on this revision. Existing tests now
cover the 16 quote/output/option combinations plus bare empty quotes,
metadata, inert prose and fenced raw-command controls. Pinned Ruff format
and check on both files passed without mutation; `git diff --check` passed.
The final two-file diff against intake HEAD is 47 additions and one deletion.
Current SHA-256 values are
`dd1fef2848235ebe25134a31ebe053908b949b68e6c95189a857c3ad3923a763`
for the quality source and
`e1827e138d07b6eddff07d92d6e4cbb2b3a2ace5e7a6150c60ae2a94fb6c2e18`
for its test. Independent read-only reviewers `/root/guard_trace` and
`/root/secret_boundary_review`, neither an author of this change, inspected
these exact code/test bytes and reported no remaining scoped finding. The
first checked paired quotes, the metadata post-close boundary, preserved bare
raw matching, unchanged real caller and Spec/Plan/Task scope; the second
confirmed the previously weakened Secret boundary was repaired and no
role, native, policy or hook setting changed. Neither reviewer ran tests or
wrote files, and neither claimed native/runtime authorization evidence.
Affected, exact-index and full QA, implementation message check and further
logical commits remain pending. Hosted CI, provider runtime and live behavior
remain unobserved.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-004](../plan.md#work-breakdown) | Completed | VAL-P01-002 / WP-002; final focused checks and independent re-review above |
| [WORK-005](../plan.md#work-breakdown) | In progress | VAL-P01-006 / WP-003; intake staged QA, scoped hooks, message and commit above; implementation delivery pending |
