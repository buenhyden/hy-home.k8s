---
title: "Quoted Secret Output Scanner Follow-up"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0002"
parent_ids: ["SPEC-0105-PLAN-0001"]
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

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | [VAL-P01-002](../spec.md#success-criteria--verification-plan) | Reproduce and repair quoted Secret output matching in the shared rule; retain inert prose grammar | quality-engineer | completed | PASS | accepted | Focused checks and independent re-review observations below |
| WORK-005 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | Validate, obtain independent read-only review and commit local handoff | platform | completed | PASS | accepted | Implementation commit, local full QA and delivery limits below |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P01-004 | [VAL-P01-002](../spec.md#success-criteria--verification-plan) | WORK-004 | Quoted-output focused regression and re-review | Scanner change and focused synthetic cases recorded below | PASS | [Verification Summary](#verification-summary) | accepted |
| EVD-P01-005 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | WORK-005 | Local validation and delivery | Exact-index, full QA and commit evidence recorded below | PASS | [Verification Summary](#verification-summary) | accepted |

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

`python3 scripts/qa.py quick` passed all 12 selected gates on the three
working-tree implementation paths against base `c620f641`. The final
implementation index used the same three paths and base; `python3
scripts/qa.py staged --base-ref HEAD` passed all 12 required gates. The
actual `.git/COMMIT_EDITMSG` text
`fix(governance): recognize quoted Secret output safely` passed the explicit
pinned Commitizen commit-msg check. Normal
`git commit -F .git/COMMIT_EDITMSG` with the existing hooks produced logical
implementation commit `6746750c29d711aaf1c81b19db75456f517b219a` and
tree `839a3066655b2774df34f1763134e253c2804e8a`; the working tree was
clean after commit. The exact validated index and committed tree matched.

On that clean implementation snapshot, `rtk proxy python3 scripts/qa.py full
--base-ref HEAD` returned 0: all 24 required gates PASS across 1,295
all-files paths, with base resolved to `6746750c29d711aaf1c81b19db75456f517b219a`.
Unit discovery and manual all-files pre-commit each ran once inside the full
profile, not as separate repeated checks. Unit stdout/stderr byte counts and
SHA-256 were 2,170 /
`963625a972a510be2c8bc6c17e938fb0ffd71ff0058d1badb921e34506f18357`
and 2,408 /
`7985ed1f8af157c00acf0a1c9534d185144b77a8c7852c0a2984a2ee7da29fcb`.
Manual pre-commit returned 0 with 1,680 stdout bytes, SHA-256
`ed873238f5f28f072a6c188ccf9690cf67d65abe1554872445869f431282d5ae`.
Kustomize 5.8.1 render and built-in jsonschema 4.10.3 / Kubernetes 1.35.0
schema checks passed. External CRD schema-policy depth remains DEFER for
unavailable schemas, live observation remains DEFER to the operator, syntax
depth remains DEFER to its separately passing required gate, and sample-app
product-semantic depth is SKIP as not applicable. These depths are not
included in the required-gate PASS claim.

Across this follow-up, Spec and Plan links were updated, this Task was added,
the shared scanner regex was modified, and its existing regression tests were
expanded. No file was deleted. Role, provider, hook and common policy bytes
were unchanged. The remaining scanner ceiling is static line matching: it
does not classify every shell form, Secret `.data` jsonpath or custom output
template. Current approval-source authentication remains the documented
manual operator path; structural evidence and review cannot authenticate it.
No remote PR, push, merge, archive disposition, live action or worktree
removal occurred. Rollback is a reviewed forward corrective code/test commit
that preserves this Task and Git history.

This is the Task-only closure candidate after the implementation full QA.
Fresh exact-index document gates, the closing commit-message check and the
third logical commit have not run on these closing Task bytes. Their actual
outcomes belong in the final handoff rather than a self-referential commit
claim. Hosted CI, provider runtime and live behavior remain unobserved.
