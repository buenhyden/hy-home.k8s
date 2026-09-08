---
title: "Consolidate Agent Governance and Quality Gates"
version: "2.5.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-08"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0001"
---

# Task: Consolidate Agent Governance and Quality Gates

## Overview

Execute the approved 2026-09-08 follow-up in SPEC-0072-PLAN-0001. Common
authority migration is complete; dated results below remain historical.
Current work corrects gate, formatter, commit and environment drift through
existing owners and creates verified logical local commits.

## Inputs

- [SPEC-0072](../spec.md)
- [SPEC-0072-PLAN-0001](../plan.md)
- [ADR-0034](../../../02.architecture/decisions/0034-stage-00-governance-and-unified-quality-gates.md)
- Migration baseline `eb4fcfe3283115388d6eb1f31d56780b3e578f77`; local main after the authorized merge is `4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`
- [ADR-0035](../../../02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | VAL-AGQ-001, VAL-AGQ-002 | Review and migrate common authority and native references | platform | Done | 53 sources migrated; static role, permission and link contracts pass | Current migration evidence below |
| [WORK-002](../plan.md#work-breakdown) | VAL-AGQ-003, VAL-AGQ-004, VAL-AGQ-008 | Preserve shared QA and hidden-path coverage; resolve baseline tooling failures | platform | Done | Hidden routes, bounded inputs and shared full/CI gate set verified | Focused negative tests and full QA |
| [WORK-003](../plan.md#work-breakdown) | VAL-AGQ-005, VAL-AGQ-007 | Reconcile documents, history, profiles and safety boundaries | platform | Done | Profiles, consumers, history and current plans reconciled; static checks pass | Disposition and link checks |
| [WORK-004](../plan.md#work-breakdown) | VAL-AGQ-006 | Validate final static tree and report native/hosted limits | platform | In progress | Local static migration passes; native and hosted evidence remains DEFER | Final validation table |
| [WORK-005](../plan.md#work-breakdown) | VAL-AGQ-013 | Correct process diagnostics | platform | Done | Bounded kernel state replaces argument reads; commit 2c9450c | Current follow-up evidence below |
| [WORK-006](../plan.md#work-breakdown) | VAL-AGQ-010, VAL-AGQ-011, VAL-AGQ-012 | Repair formatter and secret scan coverage | platform | Done | Both Providers covered; snapshot and frozen boundaries pass | Final local handoff below |
| [WORK-007](../plan.md#work-breakdown) | VAL-AGQ-009 | Align commit contracts | platform | Done | Pinned message, native temporary hook and changelog tests pass | Final local handoff below |
| [WORK-008](../plan.md#work-breakdown) | VAL-AGQ-005, VAL-AGQ-008, VAL-AGQ-014 | Remove demonstrated duplication | platform | Done | Wrapper and unused hook removed; unique domain and fixture contracts retained | Final local handoff below |
| [WORK-009](../plan.md#work-breakdown) | VAL-AGQ-001, VAL-AGQ-002, VAL-AGQ-003, VAL-AGQ-004, VAL-AGQ-006, VAL-AGQ-007 | Validate environment and handoff | platform | In progress | Local implementation and validation complete; external acceptance remains DEFER with WORK-004 | Final local handoff below |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/`, `.github/`, `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, `scripts/`, `tests/`, `.pre-commit-config.yaml`, `.markdownlint-cli2.yaml`, `.ruff.toml`, `.secrets.baseline`, `.graphifyignore`, `.cz.toml`, `.gitmessage`, `cliff.toml`, `.editorconfig`, `.gitleaks.toml`, `.hadolint.yaml`
- **Forbidden Paths**: live credentials, secret values, external provider state, cluster state, release state
- **Local Commit Authority**: the 2026-09-08 user request approves scoped logical local commits through exact-index QA and normal active hooks
- **Completed Current Local Merge**: the separately approved origin/main `49e71f9c522ee6bb70aeb917812f2e9a1e8fcad7` integration completed as `4667aa03`; that authority is consumed and grants no remote or additional merge authority
- **Conditional Finish Authority**: the later user request approves local main integration and removal of this task-owned branch/worktree only after required acceptance is complete; pending external evidence does not satisfy that condition
- **Completed Merge Authority**: the prior one-off local merge is completed historical evidence and grants no new merge authority
- **Completed Follow-up Scope**: the approved minimal integration on `codex/agq-consolidation` includes commit configuration and full-snapshot scan coverage beyond the earlier Task scope
- **Formatter-only Extension**: the full hook exposes formatting drift in `infrastructure/bootstrap-local.sh` and six `infrastructure/tests/verify-*.sh` files listed below; the approved explicit formatting repair includes these paths without executing their bodies or changing live/manifest behavior
- **Approval Required**: push, PR mutation, hosted workflow dispatch/re-run, additional merge, release, repository protection changes, global settings, paid calls, provider authentication, credential access and live deployment/reconciliation
- **Static Validation**: focused unit tests, QA profiles, pre-commit, actionlint and zizmor; existing GitHub Actions logs are read-only evidence
- **Live Validation**: DEFER — not required or authorized for repository governance consolidation
- **Secret / Vault Handling**: do not read, print, mutate, or validate secret values; retain static secret-handling gates
- **Rollback Plan**: reverse only the reviewed migration as a new change against the recorded baseline after checking later user edits and dependent commits; no blanket restore, history rewrite or live rollback
- **Evidence Location**: this Task, Git commits, pull-request checks, and workflow job logs

## Verification Summary

### Approved Follow-up Intake (2026-09-08)

Baseline HEAD is `58b32427aecdee52c601151931455bddaa317500`, including the
previous worker's diagnostic and hosted-evidence commits. The original
`fix/qa-name-the-detaching-git-call` checkout has a clean index and working tree.
The task worktree is `.worktrees/agq-consolidation` on `codex/agq-consolidation`.
Fetched origin/main and merge-base are `be2d41efe32cc9c21787d0d2c32ecc920c28c61a`.
Existing stashes remain untouched.

The user approved minimal integration through existing owners. Spec criteria
VAL-AGQ-009 through VAL-AGQ-014 extend acceptance without reopening WORK-001
through WORK-003. WORK-004 remains open for external evidence. Independent
read-only review is authorized; this worker alone owns edits and the index.
No hosted/native/live result from prior records validates the current tree.

### Process Diagnostic Correction (2026-09-08)

The former lowercase-token filter read complete process arguments before
filtering. A focused regression failed on that `cmdline` access. The correction
reads at most 4096 bytes of kernel status and retains only an admitted state
letter, alongside the existing PID/group/name. It preserves containment failure
for zombies and every timeout/output/cleanup limit. The two focused tests pass;
`tests.test_run_validation_lane` passes 69 tests in 2.386 s. Pinned Ruff 0.16.5
formatted only the two changed Python files; formatter exit 1 reflected changed
bytes and was reviewed. Exact-index validation follows those formatted bytes.

Independent read-only `diagnostic_review` (Python reviewer tool) approved the
two-file diff without findings; it independently ran Ruff 0.16.6 lint and diff
hygiene, not the pinned formatter or unit suite. The fixed code-reviewer tool
could not start because of its model quota; that attempt is not a review.

Strict profile checks pass on Spec/Plan/Task. Quick QA passes all eleven
selected gates over the initial seven-path working-tree snapshot, before
subsequent hook/test edits. This is local affected evidence, not final full QA.
Fetch succeeded; origin/main remains `be2d41efe32cc9c21787d0d2c32ecc920c28c61a`.
Linux WSL x86_64/Python 3.12.3 uses the existing CI hash lock in an isolated
`.worktrees/.agq-venv`; the installation contains pre-commit 4.6.1. In the
sandbox, platform ancestor UIDs are namespace-mapped and the strict adjacent
resolver chooses the existing account pre-commit 4.6.2 instead. No trust rule
was relaxed. Pinned message/fix calls name the isolated executable explicitly.

Narrow Git configuration inspection found effective `core.hooksPath` from the
user Git config, an executable pre-commit hook, and no commit-msg hook. Hook
contents and other private settings were not read. Actual candidate messages
therefore require the explicit pinned commit-msg invocation; normal active
hooks remain enabled for each real commit.

### Follow-up Implementation and Targeted Evidence (2026-09-08)

Commit `2c9450c84c8499b073e528807b04eaf2edf3eaa7` contains the diagnostic
correction and approved Spec/Plan/Task refresh. Its final exact-index QA passes
eleven gates in 252.54 s after reviewing/restaging the document repair. The
earlier staged run took 313.24 s on different bytes; these are observations,
not an optimization comparison. Pinned Commitizen checked the actual message
file through commit-msg in a temporary Git repository using the index's config.
The real commit then completed with normal active hooks. This does not prove a
commit-msg hook exists in the source checkout.

The follow-up retains existing owners and intentional differences:

| Surface | Disposition and preserved contract | Targeted evidence |
| --- | --- | --- |
| QA registry and affected-surface validator | One exact manual-stage pre-commit argv; full/ci keep the same gate set | Profile, direct-command and snapshot tests |
| Native Gitleaks / QA snapshot Gitleaks | Native index scan remains; manual directory scan covers unchanged and hidden snapshot files; only `.git` metadata is newly excluded | Actual Gitleaks 8.30.0 synthetic canary test passes in 1.807 s; ignored source/index remain untouched |
| ShellCheck / shfmt / Ruff / whitespace hooks | Both Provider hook paths selected; shfmt writes only explicit fix or isolated snapshot; Python-only Ruff scope remains | Selector RED/GREEN; pinned formatter temporary-repository experiment detects changed bytes and preserves source/index |
| Frozen archive | Hook-local lifecycle projection excludes existing sealed paths; new current migration paths stay selected | Lifecycle-derived corpus comparison and actual CRLF/trailing-whitespace fixture experiment; no sealed bytes edited |
| Commitizen / Git-cliff | Ordinary grammar unchanged; generated prefix defaults made explicit; changelog skip ordering, build/deps/release groups and parsed breaking footer aligned | Contract tests and actual pinned native commit-msg experiment; Git-cliff 2.13.1 temporary-history comparison |
| `scripts/validate-harness.sh` | Deleted full-plus-domain wrapper; PR/README call existing QA entry | Seven domain gates stay registered; Bash option/eval negative fixtures use the existing GitOps validator |
| Repository quality heading/residue probes | Synthetic checks move to independent tests; production parsers and diagnostics remain | AST extraction tests retain H2/H3, hidden/composite blocks, ambiguity, missing heading and residue ownership |
| `.hadolint.yaml` and unused hook | Deleted because no tracked Dockerfile consumes them; current guidance updated | Read-only target inventory; old exact path routing retained for deletion/recovery diffs |
| CI cache and summary | Cache identity adds architecture, resolved Python and lock; one QA job and fail-closed summary remain | Workflow/commit/CI-Python focused suite passes 81 tests in 8.706 s before the final small regression additions |

The pinned formatter experiment changes both Provider shell fixtures, Python
and a current migration record, while leaving Markdown code fences, frozen
archive bytes and the source/index unchanged. Formatter exit 1 and snapshot
mutation detection are expected negative results, not skipped validation.

Temporary native Git commits pass a valid subject and breaking footer and
reject a terminal period and unsupported `type(scope)!`; Commitizen is absent
from the manual file stage. These hooks are installed only in the temporary
repository. Git-cliff's official 2.13.1 asset was verified against its published
SHA-256; no global tool installation or history rewrite occurred.

Security read-only review found a missing manual-stage inheritance regression
and stale README hadolint guidance; both are corrected. Python review found
missing composite hidden-block cases in the transferred probes; those are
restored with distinct hidden rows. Reviewers ran no full QA or native hooks.
Other embedded probes and validators retain their unique rules; no unmeasured
scan/parse similarity is treated as proof of duplication.

Quick QA initially rejected the removed `.hadolint.yaml` route. Restoring only
that existing route preserves validation of deletion/recovery inputs without
restoring the unused tool. Required failures are never relabeled as SKIP.

Outside sandbox UID remapping, the strict resolver selects the locked
interpreter-adjacent pre-commit 4.6.1. Closed HOME/PATH and account-owned cache
rules remain unchanged. Cold setup is not repeated on this host given the
previous resource-pressure evidence; warm-cache timings do not establish a
cold/warm speedup. Removing the unused wrapper eliminates its extra seven
domain invocations when that old entry point was used, and moving synthetic
probes removes repeated production work; no wall-time reduction is claimed.

Final quick, staged and full evidence is recorded after the final bytes are
validated. New hosted execution, remote required-check configuration, Provider
discovery/event delivery/model resolution/enforcement and live checks remain
DEFER for the current unpublished branch. Static projection and payload tests
cannot close those external acceptance items.

### First Full Snapshot and Bounded Repairs (2026-09-08)

Quick passes twelve gates in 260.61 s after repairing the operations index date
and changelog responsibility wording. The subsequent PR checklist/CLI prose
repair is included in exact-index QA, not attributed to that earlier snapshot.
QA commit `1014bba7` passes twelve staged gates in 285.50 s; Git contract commit
`4da974e4` passes seven staged gates in 300.30 s. Each actual message passed the
pinned commit-msg invocation and each real commit used normal active hooks.
Security and Python reviewers confirmed their prior findings were resolved.

Full at `4da974e4f0633c365b6dc9617007567c9122ce0b`, tree
`d61d7def879a5f28dd5368fd41e2b90534ef80ac`, takes 1061.49 s: twenty-one gates
PASS, including unit discovery; pre-commit FAIL and snapshot mutation FAIL.
The source tree stays clean and the source index SHA-256 is unchanged.
This is a failed full result, not a completed acceptance claim.

The three failing hooks were reproduced separately in isolated snapshots;
finding values were redacted and only paths/rules/line metadata inspected.

| Failure | Bounded repair | Preserved boundary |
| --- | --- | --- |
| Gitleaks generic API-key matches on public prose | Rule-specific exact path AND anchored public-value allowances for `Prometheus/Grafana` in archived SPEC-0024 and `GH_PROMPT_DISABLED=1` in the retained SPEC-0062 plan | Both documents retain their bytes; API-shaped canaries in those same paths and both public terms outside those paths still fail |
| detect-secrets baseline drift | Pinned explicit hook updates two CI checksum line references, 95→96 and 105→106, plus native generation time | Finding hashes, verification state and filters compare equal after removing only line-number/generation-time metadata |
| shfmt existing drift | Explicit pinned fix on the nine reported Shell paths | Bash syntax passes for each; no script body or live command is executed |

The nine Shell paths are `infrastructure/bootstrap-local.sh`,
`infrastructure/tests/verify-cluster.sh`, `verify-external-services.sh`,
`verify-gitops.sh`, `verify-ingress-tls.sh`, `verify-network-policies.sh` and
`verify-secrets.sh` under that same tests directory, plus
`scripts/check-secret-handling.sh` and `scripts/validate-gitops-structure.sh`.
The diff changes indentation, redundant continuations, redirect spacing and
heredoc `then` placement only. Gitleaks, detect-secrets and shfmt then each
return zero in the repaired snapshot, with no snapshot changes. The added
public-term regression fails on the previous configuration and passes after
the narrow allowances; independent review added both out-of-path cases.

The earlier standalone heading probe executes its parser 57 times in 0.001218 s
under Python 3.12.3; its production call is now absent and independent tests
retain its cases. This small measurement is not a whole-QA speedup claim.
Full uses the existing cache; cache-miss/setup and per-gate timing were not
separately instrumented, so a controlled cold/warm comparison remains DEFER.

Pinned upstream hook manifests were read from their existing cache entries:
all applicable file hooks include manual, Commitizen is commit-msg only, and
the two Gitleaks modes have separate stages. Local Git is 2.43.0 on WSL2 Linux
6.18.33.2/x86_64. The locked environment has PyYAML 6.0.3/jsonschema 4.26.0;
system Python 3.12.3 has PyYAML 6.0.1/jsonschema 4.10.3 for Bash subcommands.
Neither cross-platform nor complete hosted-environment equivalence is claimed.

During this work the original checkout acquired external WIP in
`scripts/run-validation-lane.py` and `tests/test_run_validation_lane.py` that
exempts terminated descendants from escape reporting. Those edits are
preserved there and not imported; this branch's diagnostic change retains the
prior containment verdict. Integration requires reviewing that semantic
difference. Public GitHub API reads through the available web tool were
unavailable, so current remote check configuration and runs remain unverified.

### Updated Main Integration (2026-09-08)

The original checkout's parallel WIP became commits `0bcde241` and `0828c1b5`,
then upstream PR 61 merged as `49e71f9c522ee6bb70aeb917812f2e9a1e8fcad7`.
The user reported that update and explicitly approved a local merge into this
task branch. Fetch confirms both local main and origin/main at that SHA, with
merge-base `58b32427aecdee52c601151931455bddaa317500`. The original checkout
is clean; none of its work was replaced or imported by blanket restoration.

Repair commit `dbc80b4a44c51d2805ac624e22878a19532c0736` passes quick twelve
gates in 260.36 s and staged twelve gates in 234.08 s. Its actual message passes
pinned commit-msg validation and normal active hooks complete the commit.
Its full attempt is cancelled with SIGINT after 264.55 s, exit 130, because the
approved main integration supersedes that input. This is cancellation/FAIL,
never PASS or SKIP; the source checkout remains clean after cancellation.

The runner conflict joins main's liveness repair with the bounded diagnostic
contract. Only confirmed terminated states `Z` and `X` are excluded from escape
reporting. Live and unknown states retain failure; cleanup, timeout, output and
report bounds are unchanged, and process arguments remain unread. The earlier
diagnostic-only result above predates this approved integration and does not
define the final liveness rule. Main's fifth hosted-result history below stays
attributed to its own input, not the merged task branch.

Mechanical combination fails the existing single-read regression because it
reads status twice. Reusing one bounded state observation fixes that failure;
the regression now covers live, both terminated and malformed states. Main's
real exited-descendant case is retained. All seventy runner tests pass in
2.401 s after conflict resolution. Updated full evidence follows the merge
commit; the cancelled run cannot establish final acceptance.

### Final Local Handoff (2026-09-08)

The approved local implementation is complete on `codex/agq-consolidation` in
`.worktrees/agq-consolidation`. Integration commit
`4667aa0362f77ec0fa406479a4e7913b3d79a79c` has parents `dbc80b4a` and
`49e71f9c`; the latter is the updated main/base. The original checkout is clean
on main `49e71f9c` and its parallel work is preserved through that integration.
This worker did not push, mutate a PR, dispatch a workflow or perform live work.

| Evidence | Result | Input and limitation |
| --- | --- | --- |
| Integration runner regression | PASS | Seventy tests in 2.401 s; subsequent formatter/test-description edits are covered by final full |
| Integration quick | PASS | Eleven gates, working-tree snapshot, 256.17 s |
| Integration staged | PASS | Eleven gates, exact index, 249.35 s |
| Integration actual message and commit | PASS | Pinned commit-msg checks the actual UTF-8 file; normal active hooks create the merge commit |
| Final full | PASS | All twenty-two gates, 1200.76 s, including one unit discovery and one manual all-files pre-commit |
| Source isolation | PASS | Clean working tree; index SHA-256 unchanged; every gate reports complete cleanup |
| Full/ci equivalence | PASS, repository-static | Existing registry/workflow regression; no redundant local ci run |
| Hosted and remote required checks | DEFER | No current task-branch hosted run; remote required-check configuration unverified |
| Provider native runtime | DEFER | Static links, permissions and payload contracts pass; discovery, actual model resolution and hook delivery/enforcement need separate runtime evidence |
| Live and cross-platform behavior | DEFER | No live infrastructure invocation and no untested-platform guarantee |

The final full input is tree `90a9969165acc2c59ce57c9dafb1e0e38e782cd8` at
`4667aa03`. Its unchanged source index SHA-256 is
`4ff54a4d00d554a567266f1da438724d9094f170e977ebb077f87e439984cf02`.
The pre-commit configuration SHA-256 is
`29f2b80d5660358f62c7e53e41c12739ba497ff658e208eb08e7907826de557a`, and the
CI requirements lock SHA-256 is
`6d0685e84a4fb19b24e44c5ae965f16d7215e8608b210cbf0559d4a203a9cc13`.
These identify observed inputs, not policy pins for later work. The runtime
uses the recorded WSL/Python and locked environment with its existing cache.
The earlier failed and cancelled full attempts remain distinct evidence;
different inputs and unisolated setup costs preclude a speedup claim.

Python and security reviewers approve the liveness/diagnostic integration.
The security review's stale zombie-test description is corrected. Earlier
manual-stage, hadolint-reference and independent-probe findings are also
resolved. Reviewers did not run this final full or establish native delivery.
Frozen archive bodies and domain-owned infrastructure test locations remain
unchanged; only the explicit nine-file Shell formatting repair affects those
infrastructure scripts. No new registry, wrapper or fixture framework exists.

The implementation commits are `2c9450c8` (bounded diagnostics), `1014bba7`
(snapshot coverage and ownership), `4da974e4` (commit/changelog contracts),
`dbc80b4a` (exposed hook findings), and the approved `4667aa03` main integration.
This Task-only handoff update is authored after the full input. Its focused
document, exact-index and actual-message results are recorded in the subsequent
documentation commit body; full does not claim to have scanned this later prose.

The initial handoff kept the local branch and worktree; the later conditional
finish instruction below supersedes that selection. A scoped rollback uses reviewed forward
reverts with their paired contracts/tests. For a whole-task rollback, first
review reversal of the later handoff documentation, then the merge's second
parent (main `49e71f9c`) as the revert baseline, preserving the upstream repair.
Do not blindly revert the first-parent integration or rewrite history.

WORK-004 and WORK-009 remain open only for external acceptance. The next owner
is platform/the operator: obtain separate publication or hosted-run approval,
then collect evidence for this implementation and current required checks;
exercise each Provider's native discovery/model/hook/permission behavior in an
authorized environment. Live infrastructure testing remains outside this task.
The Task stays in progress until those lifecycle conditions are satisfied.

### Completion Audit and Conditional Finish (2026-09-08)

The user requested follow-up work and an explicit completion audit, permitting
local main integration and cleanup only once complete. Intake finds task HEAD
`0cda880c165c2bba7821fb67b446b4c554026ad2` and main/origin/main
`49e71f9c522ee6bb70aeb917812f2e9a1e8fcad7`, both checkouts clean. Fetch and
remote-ref inspection confirm the main SHA and no published task branch.
The preceding full and Task-only staged evidence still describes the unchanged
implementation; no equivalent aggregate was repeated to manufacture progress.

Unauthenticated public GitHub API reads now succeed:

| Read-only observation | Result | Acceptance meaning |
| --- | --- | --- |
| Task branch and `0cda880c` Actions run queries | Zero runs | No hosted evidence for the local implementation |
| [Main CI run 34221460082](https://github.com/buenhyden/hy-home.k8s/actions/runs/34221460082) | `push` at `49e71f9c`; qa and ci-summary success, branch-policy skipped | Valid upstream push evidence; does not validate this task branch |
| Applicable ruleset API for main | Empty list | No applicable rules returned through this public endpoint |
| Classic main protection API | HTTP 401 | Authentication required; required-check configuration remains unverified |
| Installed client version/help | Codex 0.153.4, Claude 2.1.263 | Client identity/capability metadata only, no model call or event delivery |

Codex help exposes ephemeral execution and an option to ignore user config;
Claude help exposes project-only settings and hook events in stream output.
These can bound a future authorized smoke check but are not runtime success.
Codex help also reports a read-only PATH-alias setup warning; no permission or
global installation was changed to silence it. No private configuration,
credential values, session logs or model output were collected.

Independent read-only security review agrees that repository-static work is
complete while required hosted and native acceptance is open. Conditional
merge/cleanup is therefore not executable yet. Approval has been requested
for publishing this branch plus one CI dispatch, and for one bounded native
session per Provider. Until granted, preserve the branch/worktree and keep
WORK-004/WORK-009 in progress. The next owner is the user for these protected
actions; the worker then owns result review, scoped repairs and the requested
local finish once the condition is met. Live infrastructure remains outside
the task.

### Historical Local Main Merge and Follow-up (2026-09-06)

All dated evidence from this section through the final prior hosted result is
retained history. Its former "next work", validation order, paths and one-off
approvals are not current execution instructions. The approved follow-up above
and current Spec/Plan own remaining work; sealed recovery identities below
remain evidence, not pins for the current repository state.

The user requested that the existing work be merged into local main before
remaining-work execution. The local fast-forward advanced main from
`eb4fcfe3283115388d6eb1f31d56780b3e578f77` to
`4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`, incorporating `add86fbd`,
`2b884cfa` and `4053793a`. The resulting tree is identical to the already
validated source tip; the working tree and index were clean and both stashes
were preserved. No remote state changed. The follow-up branch
`codex/governance-follow-up` starts from that merged local main.

Commit `4053793a` retains separate earlier evidence: full QA passed nineteen
gates in 927.707 s over the implementation snapshot before its Task update;
the final exact index passed eleven staged gates in 209.107 s. Those results
belong to that commit and are not validation of this documentation correction.
The unchanged merge tree did not require another full run.

The current document correction covers ADR-0035 and this package's Spec, Plan
and Task under VAL-AGQ-005 and VAL-AGQ-007. It labels migration-intake authority
as historical, routes current authority here, and leaves progress reporting in
the Task rather than duplicate Plan checkboxes. Stage 99 profiles and templates
are unchanged; ADR, Spec, Plan and Task lifecycle states are unchanged.

The attempted fixed `doc-writer` tool role failed before edits because its model
was unavailable to the current account. The existing worker performed this
bounded document assignment after reading the canonical role and required
procedures; no model or provider configuration changed. This is a tool
limitation, not native repository discovery or invocation evidence.

Author `post_merge_docs_worker` checked the four document paths before adding
this result note. `rtk proxy python3 scripts/validate-markdown-profiles.py
--root . --mode strict` with one `--include-path` per file exited 0 with no
violations. `rtk proxy markdownlint-cli2 --config .markdownlint-cli2.yaml` with
the same four paths exited 0 (CLI 0.23.0, four files, zero errors), and
`rtk proxy git diff --check` exited 0. The installed Markdown CLI check is
focused author evidence; it does not replace the pinned pre-commit gate.

`rtk proxy python3 scripts/qa.py quick` exited 0: all six selected gates passed
in 227.459 s over the four changed documents before this result update.
Independent reviewer `post_merge_doc_review` approved the four-file diff without
findings after checking links, actual Git refs and commit `4053793a`'s body.

Native provider and hosted CI evidence remain DEFER for WORK-004. Final QA
for these changed document bytes belongs to the supervising
agent's handoff. Rollback is a reviewed reversal of only these four document
changes after checking concurrent edits; it does not rewind main or discard
stashes. The next owner remains the supervisor for local validation and
remaining-work review, and the user/operator for protected external evidence.

### Migration Baseline Evidence (2026-09-06)

At migration intake, the user request authorized common `.agents/` adoption and
old hub removal; commit/merge/push/PR/deployment/global/trust changes were not
authorized at that point. The current approval boundary above supersedes those
historical execution limits. Initial index and working tree were clean; only
one worktree existed.
Two existing stashes and ignored provider personal files are preserved.
Main and origin/main both resolved to `eb4fcfe3283115388d6eb1f31d56780b3e578f77`,
confirmed by read-only GitHub main metadata. The new local work branch is
`codex/common-agents-authority`, with the same HEAD. No force update occurred.

OS is Linux/WSL2 (6.18.33.2); Codex CLI 0.140.0, Claude Code 2.1.261,
Python 3.12.3, Git 2.43.0 and pre-commit CLI 4.5.1 were observed. No private
settings, auth, shell history, secrets or personal memory content was read.
The current session loaded the old gateways before migration; new-session
loading cannot be inferred from subsequent file reads.

| Command / observation | Exit / state | Result and scope |
| --- | --- | --- |
| `python3 scripts/validate-agent-governance.py --root .` baseline | 1 / FAIL | Retired-path check rejects empty sandbox-mounted `.agents/`; no repository-owned source existed there |
| `python3 scripts/qa.py full` baseline | 1 / FAIL | 219.932 s, 985 snapshot paths, 19 gates; 13 passed, 6 failed |
| Baseline full failures | FAIL | agent-governance consumer proof; links-and-owners unavailable historical replacement; repository-quality workflow inventory and two historical executables; unittest start directory missing package marker; pre-commit CLI not resolved by the runner |
| Local branch creation | 0 / PASS | Scoped normal approval; original clean baseline and both stashes preserved; no commit |
| Native provider invocation, hooks; hosted CI; live services | NOT_RUN | Not authorized by this migration; syntax and repository contracts remain separate evidence |

### Source Disposition Manifest

All rows refer to baseline `eb4fcfe3283115388d6eb1f31d56780b3e578f77`. Source paths are relative to the former governance hub; its recorded identity is historical provenance, never a fallback loader. All 53 sources are regular tracked files. In the table, `baseline:` denotes the source hub relative path at the recorded commit; `specs:` abbreviates the Stage 03 path for provenance only. These tokens are not load paths. Preserve each source ID/status and unique contract; approval effect is unchanged permission intersection. The audit read 836 tracked text surfaces and identified 950 inbound edges and 379 outbound edges. Counts describe the baseline audit, not native execution.

| Source relative path / observation | Purpose / lifecycle | Disposition / final owner | Preserved contract / approval effect | Incoming consumers / outgoing dependencies / verification |
| --- | --- | --- | --- | --- |
| `README.md` / OBS-001 | Stage 00 owns common governance, role metadata, and reusable procedures for agent work in this GitOps workspace. Codex and Claude are the supported providers; their repository directories contain native adapters. / active | rewrite → `.agents/README.md` | Route policies, role registry, workflows and registered skills without duplicate authority; preserve memory retirement links. Approval: unchanged; Real common authority needs one hub; numbered Stage 00 route closes. | In: `.claude/README.md`; `.codex/README.md`; `README.md`; `baseline:policies/document-lifecycle.md`; `baseline:roles/README.md`; `baseline:sdlc.md`; `docs/01.requirements/0003-workspace-agent-governance-platform.md`; `docs/01.requirements/README.md`; `docs/02.architecture/README.md`; `docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`; `docs/02.architecture/decisions/README.md`; `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`; `docs/02.architecture/descriptions/README.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/plan.md`; `specs:README.md`; `docs/05.operations/README.md`; `docs/05.operations/guides/README.md`; `docs/05.operations/incidents/README.md`; `docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md`; `docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`; `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`; `docs/05.operations/policies/README.md`; `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`; `docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`; `docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`; `docs/05.operations/runbooks/0007-kiali-observability-connectivity-runbook.md`; `docs/05.operations/runbooks/0008-argocd-metrics-prometheus-runbook.md`; `docs/05.operations/runbooks/0009-k8s-observability-runbook.md`; `docs/05.operations/runbooks/README.md`; `docs/90.references/README.md`; `docs/90.references/audits/README.md`; `docs/90.references/data/README.md`; `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md`; `docs/90.references/research/README.md`; `docs/98.archive/README.md`; `docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/plan.md`; `docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/spec.md`; `docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/plan.md`; `docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/spec.md`; `docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/spec.md`; `docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`; `docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/plan.md`; `docs/99.templates/README.md`; `docs/README.md`; `scripts/validate-document-lifecycle.py`; `scripts/validate-links-and-owners.py`; `tests/test_current_executable_references.py`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/document-lifecycle.md`; `baseline:policies/formatting-and-linting.md`; `baseline:policies/git.md`; `baseline:policies/model-selection.md`; `baseline:policies/quality.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/README.md`; `baseline:roles/architecture.md`; `baseline:roles/documentation.md`; `baseline:roles/infrastructure.md`; `baseline:roles/operations.md`; `baseline:roles/quality.md`; `baseline:roles/registry.json`; `baseline:roles/security.md`; `baseline:roles/supervision.md`; `baseline:sdlc.md`; `baseline:skills/delegated-development.md`; `baseline:skills/work-lifecycle.md`; `docs/98.archive/README.md`; `docs/98.archive/migrations/0009-governance-memory-retirement.md`; `docs/99.templates/README.md`; `docs/99.templates/registry.json`; `scripts/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/agent-execution.md` / OBS-002 | Keep agent work evidence-backed, scoped, and GitOps-first for this WSL2+k3d home-lab platform. The normal outcome is a reviewable repository change, not a live infrastructure mutation. / active | move → `.agents/governance/agent-execution.md` | Common execution owner; scoped GitOps-first work; thin gateways; untrusted inputs are evidence; English contracts/Korean output; roles grant no extra permissions. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `.claude/CLAUDE.md`; `.codex/CODEX.md`; `AGENTS.md`; `CLAUDE.md`; `baseline:README.md`; `baseline:policies/approval-and-safety.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/security-auditor.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/work-lifecycle.md`; `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`; `docs/90.references/research/0001-workspace-engineering/m0002-harness-and-loop-engineering.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `docs/98.archive/migrations/0009-governance-memory-retirement.md`; `scripts/README.md`; `scripts/validate-agent-governance.py`; `tests/test_agent_governance.py`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `baseline:sdlc.md`; `baseline:skills/delegated-development.md`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/approval-and-safety.md` / OBS-003 | Agents prepare desired-state changes and local evidence within the user's scope. Protected actions require explicit human or operator authority. / active | move → `.agents/governance/approval-and-safety.md` | Protected actions need explicit authority; subagents never mutate live clusters; no secret/private runtime reads; native controls narrow only; no inferred Git/CI/remote approval. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `.claude/CLAUDE.md`; `.claude/README.md`; `.codex/CODEX.md`; `.github/PULL_REQUEST_TEMPLATE.md`; `.github/SECURITY.md`; `README.md`; `_workspace/README.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/git.md`; `baseline:policies/quality.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/infrastructure.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/security-auditor.md`; `baseline:roles/security.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/delegated-development.md`; `baseline:skills/work-lifecycle.md`; `specs:0052-document-taxonomy-consolidation/plan.md`; `docs/05.operations/README.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `docs/98.archive/migrations/0009-governance-memory-retirement.md`; `scripts/validate-agent-governance.py`; `scripts/validation/repository/quality.py`; `tests/test_agent_governance.py`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/git.md`; `baseline:policies/quality.md`; `docs/05.operations/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/context-and-memory.md` / OBS-004 | Retain only the context needed to resume safely. Repository state and the owning SDLC document, not a memory ledger, determine current truth. / active | move → `.agents/governance/context-and-memory.md` | Task owns work status/evidence; memory is advisory; re-observe Git; preserve MIG-0007 and MIG-0009 retirement; never recreate governance memory. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:skills/knowledge-map/SKILL.md`; `baseline:skills/work-lifecycle.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/plan.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0003-codex-claude-only-ai-agent-governance.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0012-progress-and-generated-current-cleanup.md`; `docs/90.references/research/0001-workspace-engineering/m0011-agent-memory-tiers-and-management.md`; `docs/98.archive/completed/03.specs/0064-agent-governance-surface-consolidation/plan.md`; `docs/98.archive/completed/03.specs/0065-transition-residue-retirement/tasks/tsk-0001-trr-000.md`; `docs/98.archive/migrations/0009-governance-memory-retirement.md`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/document-lifecycle.md`; `baseline:policies/quality.md`; `baseline:skills/work-lifecycle.md`; `docs/98.archive/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/document-authoring.md` / OBS-005 | Select the document owner by purpose, author from its canonical template, and close the change with traceable evidence. / active | move → `.agents/governance/document-authoring.md` | Stage 99 alone owns profiles/templates/identity; single owner by purpose; exact metadata order; no package README or parallel progress tree; preserve completed/sealed evidence. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `_workspace/README.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/document-lifecycle.md`; `baseline:roles/documentation.md`; `baseline:sdlc.md`; `baseline:skills/knowledge-map/SKILL.md`; `baseline:skills/work-lifecycle.md`; `docs/02.architecture/README.md`; `specs:0052-document-taxonomy-consolidation/plan.md`; `specs:0071-document-taxonomy-and-form-identity-normalization/plan.md`; `specs:0071-document-taxonomy-and-form-identity-normalization/spec.md`; `docs/05.operations/README.md`; `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md`; `docs/90.references/research/0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md`; `docs/98.archive/README.md`; `docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/spec.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `docs/99.templates/README.md`; `docs/99.templates/templates/README.md`; `docs/README.md`; `scripts/README.md`; `tests/test_archive_cutover.py`. Out: `baseline:policies/document-lifecycle.md`; `baseline:policies/quality.md`; `baseline:sdlc.md`; `baseline:skills/work-lifecycle.md`; `docs/98.archive/README.md`; `docs/99.templates/README.md`; `docs/99.templates/contracts/frontmatter.schema.json`; `docs/99.templates/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/document-lifecycle.md` / OBS-006 | This policy governs document promotion, blocking, supersession, retirement, withdrawal, sealing, and historical recovery across the repository. / active | move → `.agents/governance/document-lifecycle.md` | Registry-owned lifecycle edges/immutable IDs; reciprocal supersession; replacement, consumer and recovery coverage; terminal payload immutability. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `baseline:README.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/formatting-and-linting.md`; `baseline:sdlc.md`; `specs:0052-document-taxonomy-consolidation/plan.md`; `docs/README.md`; `scripts/validate-document-lifecycle.py`; `tests/test_document_lifecycle_archive_cutover.py`. Out: `baseline:README.md`; `baseline:policies/document-authoring.md`; `baseline:sdlc.md`; `docs/98.archive/README.md`; `docs/99.templates/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/formatting-and-linting.md` / OBS-007 | Each file type has one formatting and linting owner, each rule is declared once, and each suppression states why it exists. A configuration file that no tool reads is not a convention; it is drift that reads like one. / active | move → `.agents/governance/formatting-and-linting.md` | One formatter/linter owner per capability; editor hint and pre-commit enforcement; reason for suppression; frozen Archive bytes preserved; validation is not general mutation. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `baseline:README.md`; `baseline:policies/quality.md`. Out: `baseline:policies/document-lifecycle.md`; `baseline:policies/git.md`; `baseline:policies/quality.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/git.md` / OBS-008 | Keep local changes small, reviewable, and traceable to the active Spec and Task. `main` is the default integration base unless repository evidence or the approved Plan specifies another base. / active | move → `.agents/governance/git.md` | Requested scoped Conventional Commits; staged/diff evidence; no hooks bypass; explicit push/PR/merge/destructive/history rewrite/worktree removal authority. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `.github/repository-surface.md`; `README.md`; `baseline:README.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/formatting-and-linting.md`; `baseline:policies/quality.md`; `baseline:skills/work-lifecycle.md`; `docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/plan.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `scripts/validation/repository/quality.py`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/model-selection.md` / OBS-009 | Use capability appropriate to the task without turning model age, role names, or static configuration into claims of observed fitness. / active | move → `.agents/governance/model-selection.md` | Keep #top/#worker anchors; capability does not expand permission; preserve native model/effort; static configuration proves no runtime resolution. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `.claude/README.md`; `.codex/README.md`; `baseline:README.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/registry.json`; `baseline:skills/delegated-development.md`; `specs:0068-agent-projection-rendering-and-gate-reduction/spec.md`; `docs/90.references/research/0001-workspace-engineering/m0010-agent-model-routing-and-configuration.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `evals/README.md`; `tests/test_agent_governance.py`; `tests/test_validate_agent_core_cutover.py`. Out: `baseline:policies/quality.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `policies/quality.md` / OBS-010 | Report exactly what was checked, over which bytes and scope, and with which limitations. Passing a local command is not proof of provider or live behavior. / active | move → `.agents/governance/quality.md` | Preserve quick/staged/full/message/CI/remote evidence lanes, PASS/SKIP/FAIL/DEFER, runner envelope, completion order, exact index bytes, single logical gate and handoff fields. Approval: unchanged; Distinct active normative owner; flatten policies with SDLC under governance without optional subdirectories. | In: `.claude/CLAUDE.md`; `.claude/README.md`; `.codex/CODEX.md`; `.github/PULL_REQUEST_TEMPLATE.md`; `.github/repository-surface.md`; `AGENTS.md`; `CLAUDE.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/formatting-and-linting.md`; `baseline:policies/git.md`; `baseline:policies/model-selection.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/architecture.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/documentation.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/infrastructure.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/operations.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/quality.md`; `baseline:roles/security-auditor.md`; `baseline:roles/security.md`; `baseline:roles/supervision.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/delegated-development.md`; `baseline:skills/knowledge-map/SKILL.md`; `baseline:skills/work-lifecycle.md`; `baseline:skills/workspace-harness-audit/SKILL.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/plan.md`; `specs:0062-workspace-research-full-corpus-reverification/plan.md`; `specs:0062-workspace-research-full-corpus-reverification/spec.md`; `specs:0068-agent-projection-rendering-and-gate-reduction/spec.md`; `specs:0070-retired-provider-residue-disposition/spec.md`; `specs:0071-document-taxonomy-and-form-identity-normalization/plan.md`; `specs:0071-document-taxonomy-and-form-identity-normalization/spec.md`; `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`; `docs/90.references/research/0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md`; `docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/plan.md`; `docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/spec.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `docs/README.md`; `evals/README.md`; `policy/README.md`; `scripts/README.md`; `scripts/validate-agent-governance.py`; `tests/README.md`; `tests/test_agent_governance.py`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/formatting-and-linting.md`; `baseline:policies/git.md`; `baseline:skills/work-lifecycle.md`; `scripts/run-validation-lane.py`; `scripts/validation/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `providers/claude.md` / OBS-011 | Describe Claude-native loading, permissions, and hooks without duplicating shared execution policy or the agent roster. / active | rehome → `.claude/provider.md` | Provider loading/settings/model/runtime evidence only; shared policy/roster stay neutral; native control narrows approval; exact native metadata unchanged. Approval: unchanged; Provider-specific adapter guidance belongs at the existing native provider surface with its own governed profile. | In: `.claude/CLAUDE.md`; `.claude/README.md`; `CLAUDE.md`; `baseline:README.md`; `baseline:policies/model-selection.md`; `specs:0068-agent-projection-rendering-and-gate-reduction/spec.md`; `docs/90.references/research/0001-workspace-engineering/m0003-provider-implementation-status.md`; `docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md`; `docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/plan.md`; `docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/plan.md`; `docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md`; `tests/test_agent_governance.py`. Out: `.claude/CLAUDE.md`; `.claude/hooks/k8s-pre-edit.sh`; `.claude/settings.json`; `.claude/skills`; `baseline:policies/model-selection.md`; `baseline:policies/quality.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `providers/codex.md` / OBS-012 | Describe Codex-native loading and configuration without duplicating shared execution policy or the agent roster. / active | rehome → `.codex/provider.md` | Provider loading/settings/model/runtime evidence only; shared policy/roster stay neutral; native control narrows approval; exact native metadata unchanged. Approval: unchanged; Provider-specific adapter guidance belongs at the existing native provider surface with its own governed profile. | In: `.codex/CODEX.md`; `.codex/README.md`; `AGENTS.md`; `baseline:README.md`; `baseline:policies/model-selection.md`; `specs:0068-agent-projection-rendering-and-gate-reduction/spec.md`; `docs/90.references/research/0001-workspace-engineering/m0003-provider-implementation-status.md`; `docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md`; `docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/plan.md`; `docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/plan.md`; `docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md`; `docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md`; `scripts/validate-document-lifecycle.py`; `tests/test_agent_governance.py`; `tests/test_agent_governance_consumers.py`; `tests/test_archive_validation.py`. Out: `.codex/CODEX.md`; `baseline:policies/model-selection.md`; `baseline:policies/quality.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/README.md` / OBS-013 | Select the responsibility needed for the task, then resolve the concrete role and provider projection from the the current role registry. This router is not a duplicate roster or permission inventory. / active | move → `.agents/roles/README.md` | Seven domain responsibility lenses and canonical role body navigation; registry owns exact machine roster. Approval: unchanged; Concrete shared role discovery consumer; avoids duplicate provider rosters. | In: `.github/PULL_REQUEST_TEMPLATE.md`; `AGENTS.md`; `CLAUDE.md`; `README.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:roles/architecture.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/documentation.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/infrastructure.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/operations.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/quality.md`; `baseline:roles/security-auditor.md`; `baseline:roles/security.md`; `baseline:roles/supervision.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/delegated-development.md`; `baseline:skills/work-lifecycle.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `evals/README.md`; `tests/test_document_lifecycle_migration.py`. Out: `baseline:README.md`; `baseline:roles/architecture.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/documentation.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/infrastructure.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/operations.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/quality.md`; `baseline:roles/registry.json`; `baseline:roles/security-auditor.md`; `baseline:roles/security.md`; `baseline:roles/supervision.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:sdlc.md`; `baseline:skills/delegated-development.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/architecture.md` / OBS-014 | Keep system structure and important decisions consistent with durable requirements and change-specific contracts. / active | move → `.agents/roles/architecture.md` | Preserve architecture domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/code-reviewer.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `docs/02.architecture/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/code-reviewer.md` / OBS-015 | Review repository changes for correctness, maintainability, regression risk, and policy alignment. / active | move → `.agents/roles/code-reviewer.md` | Role code-reviewer; permission read-only-evidence; tier #worker; skills risk-report; handoffs security-auditor, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/code-reviewer.md`; `.codex/agents/code-reviewer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `tests/test_agent_governance.py`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/architecture.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/doc-writer.md` / OBS-016 | Author governed documentation at the canonical SDLC or common-document owner. / active | move → `.agents/roles/doc-writer.md` | Role doc-writer; permission scoped-authoring; tier #worker; skills docs-stage-conformance, docs-stage-routing, requirements-to-design; handoffs docs-researcher, supervisor, wiki-curator; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/doc-writer.md`; `.codex/agents/doc-writer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/documentation.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/docs-researcher.md` / OBS-017 | Collect and classify source evidence for documentation without claiming policy authority. / active | move → `.agents/roles/docs-researcher.md` | Role docs-researcher; permission read-only-evidence; tier #worker; skills docs-stage-routing, knowledge-map; handoffs doc-writer, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/docs-researcher.md`; `.codex/agents/docs-researcher.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `tests/test_document_lifecycle_agent_roster_cutover.py`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/documentation.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/documentation.md` / OBS-018 | Keep authored documents and navigation useful, traceable, and correctly routed. / active | move → `.agents/roles/documentation.md` | Preserve documentation domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/wiki-curator.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/document-authoring.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/gitops-reviewer.md` / OBS-019 | Review GitOps manifests and reconciliation behavior without assuming mutation authority. / active | move → `.agents/roles/gitops-reviewer.md` | Role gitops-reviewer; permission read-only-evidence; tier #worker; skills gitops-workflow, k8s-validate; handoffs k8s-implementer, security-auditor, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/gitops-reviewer.md`; `.codex/agents/gitops-reviewer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/infrastructure.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/incident-responder.md` / OBS-020 | Triage incidents, bound impact, and produce evidence-based response and corrective-action guidance. / active | move → `.agents/roles/incident-responder.md` | Role incident-responder; permission read-only-evidence; tier #top; skills incident-postmortem, rca-methodology; handoffs security-auditor, k8s-implementer, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/incident-responder.md`; `.codex/agents/incident-responder.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/operations.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/infrastructure.md` / OBS-021 | Keep Kubernetes and GitOps desired state reproducible, isolated, and aligned with approved system contracts. / active | move → `.agents/roles/infrastructure.md` | Preserve infrastructure domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/k8s-implementer.md` / OBS-022 | Implement explicitly scoped Kubernetes and GitOps changes and validate the affected reconciliation surface. / active | move → `.agents/roles/k8s-implementer.md` | Role k8s-implementer; permission scoped-authoring; tier #worker; skills deployment-strategies, gitops-workflow, k8s-validate; handoffs gitops-reviewer, security-auditor, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/k8s-implementer.md`; `.codex/agents/k8s-implementer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/infrastructure.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/network-reviewer.md` / OBS-023 | Review cluster networking, ingress, DNS, policy, and isolation behavior from repository evidence. / active | move → `.agents/roles/network-reviewer.md` | Role network-reviewer; permission read-only-evidence; tier #worker; skills k8s-security-audit, risk-report; handoffs security-auditor, gitops-reviewer, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/network-reviewer.md`; `.codex/agents/network-reviewer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `tests/fixtures/validation-surfaces.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/infrastructure.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/observability-reviewer.md` / OBS-024 | Review metrics, logs, alerts, dashboards, and operational observability coverage. / active | move → `.agents/roles/observability-reviewer.md` | Role observability-reviewer; permission read-only-evidence; tier #worker; skills ops-runbook, risk-report; handoffs gitops-reviewer, security-auditor, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/observability-reviewer.md`; `.codex/agents/observability-reviewer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/infrastructure.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/operations.md` / OBS-025 | Preserve safe operating procedures, recoverability, incident evidence, and escalation. / active | move → `.agents/roles/operations.md` | Preserve operations domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/incident-responder.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `docs/05.operations/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/quality-engineer.md` / OBS-026 | Design and run bounded repository validation and report reproducible quality evidence. / active | move → `.agents/roles/quality-engineer.md` | Role quality-engineer; permission scoped-authoring; tier #worker; skills k8s-validate, workspace-harness-audit; handoffs code-reviewer, security-auditor, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/quality-engineer.md`; `.codex/agents/quality-engineer.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/quality.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/quality.md` / OBS-027 | Map acceptance to reproducible checks and report failures, limitations, and regression risk. / active | move → `.agents/roles/quality.md` | Preserve quality domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/quality-engineer.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/registry.json` / OBS-028 | Preserve exact providers/gateways, 3 permission classes, 12 role IDs/responsibilities/skills/handoffs/tier anchors and 16 skill IDs; path remapping only. / not-declared | move → `.agents/roles/registry.json` | Preserve exact providers/gateways, 3 permission classes, 12 role IDs/responsibilities/skills/handoffs/tier anchors and 16 skill IDs; path remapping only. Approval: unchanged; Single provider-neutral machine authority belongs with common roles. | In: `.claude/CLAUDE.md`; `.claude/README.md`; `.claude/agents/code-reviewer.md`; `.claude/agents/doc-writer.md`; `.claude/agents/docs-researcher.md`; `.claude/agents/gitops-reviewer.md`; `.claude/agents/incident-responder.md`; `.claude/agents/k8s-implementer.md`; `.claude/agents/network-reviewer.md`; `.claude/agents/observability-reviewer.md`; `.claude/agents/quality-engineer.md`; `.claude/agents/security-auditor.md`; `.claude/agents/supervisor.md`; `.claude/agents/wiki-curator.md`; `.codex/CODEX.md`; `.codex/README.md`; `.codex/agents/code-reviewer.toml`; `.codex/agents/doc-writer.toml`; `.codex/agents/docs-researcher.toml`; `.codex/agents/gitops-reviewer.toml`; `.codex/agents/incident-responder.toml`; `.codex/agents/k8s-implementer.toml`; `.codex/agents/network-reviewer.toml`; `.codex/agents/observability-reviewer.toml`; `.codex/agents/quality-engineer.toml`; `.codex/agents/security-auditor.toml`; `.codex/agents/supervisor.toml`; `.codex/agents/wiki-curator.toml`; `AGENTS.md`; `CLAUDE.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/model-selection.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/README.md`; `baseline:roles/architecture.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/documentation.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/infrastructure.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/operations.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/quality.md`; `baseline:roles/security-auditor.md`; `baseline:roles/security.md`; `baseline:roles/supervision.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/delegated-development.md`; `baseline:skills/knowledge-map/SKILL.md`; `baseline:skills/workspace-harness-audit/SKILL.md`; `docs/01.requirements/0003-workspace-agent-governance-platform.md`; `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/spec.md`; `specs:0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md`; `docs/98.archive/migrations/0020-stage00-agent-registry-authority-transfer.md`; `scripts/README.md`; `scripts/validate-agent-governance.py`; `scripts/validate-links-and-owners.py`; `tests/fixtures/validation-surfaces.json`; `tests/test_agent_governance.py`; `tests/test_agent_governance_consumers.py`; `tests/test_archive_cutover.py`; `tests/test_document_lifecycle_agent_roster_cutover.py`. Out: `.claude/agents/code-reviewer.md`; `.claude/agents/doc-writer.md`; `.claude/agents/docs-researcher.md`; `.claude/agents/gitops-reviewer.md`; `.claude/agents/incident-responder.md`; `.claude/agents/k8s-implementer.md`; `.claude/agents/network-reviewer.md`; `.claude/agents/observability-reviewer.md`; `.claude/agents/quality-engineer.md`; `.claude/agents/security-auditor.md`; `.claude/agents/supervisor.md`; `.claude/agents/wiki-curator.md`; `.codex/agents/code-reviewer.toml`; `.codex/agents/doc-writer.toml`; `.codex/agents/docs-researcher.toml`; `.codex/agents/gitops-reviewer.toml`; `.codex/agents/incident-responder.toml`; `.codex/agents/k8s-implementer.toml`; `.codex/agents/network-reviewer.toml`; `.codex/agents/observability-reviewer.toml`; `.codex/agents/quality-engineer.toml`; `.codex/agents/security-auditor.toml`; `.codex/agents/supervisor.toml`; `.codex/agents/wiki-curator.toml`; `baseline:policies/model-selection.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/security-auditor.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/deployment-strategies/SKILL.md`; `baseline:skills/docs-stage-conformance/SKILL.md`; `baseline:skills/docs-stage-routing/SKILL.md`; `baseline:skills/execution-plan/SKILL.md`; `baseline:skills/gitops-workflow/SKILL.md`; `baseline:skills/incident-postmortem/SKILL.md`; `baseline:skills/k8s-security-audit/SKILL.md`; `baseline:skills/k8s-validate/SKILL.md`; `baseline:skills/knowledge-map/SKILL.md`; `baseline:skills/ops-runbook/SKILL.md`; `baseline:skills/rca-methodology/SKILL.md`; `baseline:skills/requirements-to-design/SKILL.md`; `baseline:skills/risk-report/SKILL.md`; `baseline:skills/task-breakdown/SKILL.md`; `baseline:skills/vulnerability-patterns/SKILL.md`; `baseline:skills/workspace-harness-audit/SKILL.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/registry.schema.json` / OBS-029 | Preserve schema identity, strict additionalProperties, required fields, provider/permission sets, size limits; update only admitted path grammar. / not-declared | move → `.agents/roles/registry.schema.json` | Preserve schema identity, strict additionalProperties, required fields, provider/permission sets, size limits; update only admitted path grammar. Approval: unchanged; Active schema consumer moves beside registry. | In: `docs/98.archive/migrations/0020-stage00-agent-registry-authority-transfer.md`; `scripts/validate-agent-governance.py`; `scripts/validate-links-and-owners.py`; `tests/test_agent_governance_consumers.py`; `tests/test_archive_cutover.py`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/security-auditor.md` / OBS-030 | Audit repository changes for secret exposure, privilege escalation, isolation failure, and policy violations. / active | move → `.agents/roles/security-auditor.md` | Role security-auditor; permission read-only-evidence; tier #top; skills k8s-security-audit, vulnerability-patterns; handoffs k8s-implementer, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/security-auditor.md`; `.codex/agents/security-auditor.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `baseline:roles/security.md`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/security.md` / OBS-031 | Review secret exposure, access control, isolation, and unsafe execution against the approved contract. / active | move → `.agents/roles/security.md` | Preserve security domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/security-auditor.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/supervision.md` / OBS-032 | Coordinate authorized work and reconcile ownership, dependencies, review, and evidence. / active | move → `.agents/roles/supervision.md` | Preserve supervision domain boundary and stage owner links; registry permission and task scope constrain actions. Approval: unchanged; Distinct active domain lens is referenced by canonical roles/router; do not duplicate into provider roles. | In: `baseline:README.md`; `baseline:roles/README.md`; `baseline:roles/supervisor.md`; `docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `baseline:skills/delegated-development.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/supervisor.md` / OBS-033 | Route bounded work, preserve approval and ownership boundaries, and reconcile final evidence. / active | move → `.agents/roles/supervisor.md` | Role supervisor; permission orchestration; tier #top; skills execution-plan, risk-report, task-breakdown; handoffs code-reviewer, doc-writer, k8s-implementer, quality-engineer, security-auditor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/supervisor.md`; `.codex/agents/supervisor.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `tests/fixtures/validation-surfaces.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `baseline:roles/supervision.md`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `roles/wiki-curator.md` / OBS-034 | Maintain knowledge navigation and canonical links without creating duplicate policy authority. / active | move → `.agents/roles/wiki-curator.md` | Role wiki-curator; permission scoped-authoring; tier #worker; skills docs-stage-conformance, knowledge-map; handoffs doc-writer, supervisor; preserve inputs/outputs/guardrails/evidence. Approval: unchanged; Existing registry and both provider projections consume this neutral responsibility. | In: `.claude/agents/wiki-curator.md`; `.codex/agents/wiki-curator.toml`; `baseline:roles/README.md`; `baseline:roles/registry.json`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/documentation.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `sdlc.md` / OBS-035 | This document owns the human flow from durable requirements through architecture, Spec-driven implementation, operations, and historical recovery. Stage numbers express ownership and navigation rather than a one-way approval waterfall. / active | move → `.agents/governance/sdlc.md` | Requirement→Architecture→Spec/Plan/Task→Operations/Reference/Archive ownership; Stage 99 exact document contract; no Stage 04 release family; proportional work. Approval: unchanged; Common human flow belongs with governance while numbered docs retain domain records. | In: `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/document-authoring.md`; `baseline:policies/document-lifecycle.md`; `baseline:roles/README.md`; `baseline:skills/docs-stage-routing/SKILL.md`; `baseline:skills/work-lifecycle.md`; `docs/README.md`; `scripts/validate-document-lifecycle.py`; `tests/test_document_lifecycle_archive_cutover.py`. Out: `baseline:README.md`; `baseline:policies/document-authoring.md`; `baseline:policies/document-lifecycle.md`; `docs/99.templates/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/delegated-development.md` / OBS-036 | Delegate bounded work through a supported runtime mechanism while preserving responsibility, least privilege, and independent evidence. / active | rehome → `.agents/workflows/delegated-development.md` | Explicit delegation authorization, registry permission intersection, disjoint owners, exact handoffs, independent evidence; orchestration is not authoring; no live/secret actions. Approval: unchanged; Plain procedure is not native SKILL.md; explicit workflows avoid accidental automatic activation. | In: `_workspace/README.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:roles/README.md`; `baseline:roles/supervision.md`; `baseline:skills/work-lifecycle.md`; `specs:0006-workspace-harness-gap-analysis/spec.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`. Out: `baseline:policies/approval-and-safety.md`; `baseline:policies/model-selection.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:roles/registry.json`; `baseline:skills/work-lifecycle.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/deployment-strategies/SKILL.md` / OBS-037 | Use when comparing or designing Kubernetes and ArgoCD deployment strategies, including Blue-Green, Canary, Rolling update, rollback, zero-downtime deployment, progressive delivery, probes, and DORA metrics. Monitoring tool setup and actual CI pipeline configuration are outside this skill / not-declared | move → `.agents/skills/deployment-strategies/SKILL.md` | Deployment strategy/reference catalog; repository-first rollback and probes. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/k8s-implementer.md`; `.codex/agents/k8s-implementer.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/docs-stage-conformance/SKILL.md` / OBS-038 | Use when repairing scoped document-profile, README, heading, or cross-link drift without changing historical meaning. / not-declared | move → `.agents/skills/docs-stage-conformance/SKILL.md` | Small authorized current-document profile/link fixes; preserve historical evidence; existing validators. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/doc-writer.md`; `.claude/agents/wiki-curator.md`; `.codex/agents/doc-writer.toml`; `.codex/agents/wiki-curator.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/docs-stage-routing/SKILL.md` / OBS-039 | Use when selecting the canonical owner and template for an authored document or rejecting parallel document trees. / not-declared | move → `.agents/skills/docs-stage-routing/SKILL.md` | Exactly one canonical document/profile/template; Stage 99 contract owner; no global/user/auth edits. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/doc-writer.md`; `.claude/agents/docs-researcher.md`; `.codex/agents/doc-writer.toml`; `.codex/agents/docs-researcher.toml`; `baseline:roles/registry.json`; `scripts/validation/repository/quality.py`. Out: `baseline:sdlc.md`; `docs/99.templates/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/execution-plan/SKILL.md` / OBS-040 | Use when turning an approved Spec and architecture constraints into ordered, testable implementation work. / not-declared | move → `.agents/skills/execution-plan/SKILL.md` | Approved Spec and architecture constraints to ordered ownership, verification, risk, rollback and existing work units. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/supervisor.md`; `.codex/agents/supervisor.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/gitops-workflow/SKILL.md` / OBS-041 | Define the approved GitOps path for workload onboarding, change review, and sync diagnosis in `hy-home.k8s`. / not-declared | move → `.agents/skills/gitops-workflow/SKILL.md` | Repository desired state only; k8s-validate; sync target ownership and secret constraints. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/gitops-reviewer.md`; `.claude/agents/k8s-implementer.md`; `.codex/agents/gitops-reviewer.toml`; `.codex/agents/k8s-implementer.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/incident-postmortem/SKILL.md` / OBS-042 | Use when writing a cluster incident postmortem or routing post-incident analysis through timeline reconstruction, root cause analysis, impact assessment, and remediation planning. Real-time on-call response, monitoring setup, and alert configuration are outside this skill / not-declared | move → `.agents/skills/incident-postmortem/SKILL.md` | Approved incident evidence to timeline/RCA/impact/remediation; operation/postmortem template; blameless uncertainty. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/incident-responder.md`; `.codex/agents/incident-responder.toml`; `baseline:roles/registry.json`. Out: `docs/99.templates/templates/operations/postmortem.template.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/k8s-security-audit/SKILL.md` / OBS-043 | Use when auditing Kubernetes RBAC, NetworkPolicy gaps, Secret handling, container security context, image supply chain, CIS benchmark posture, or related cluster security hardening. Real-time intrusion detection and WAF configuration are outside this skill / not-declared | move → `.agents/skills/k8s-security-audit/SKILL.md` | Read-only manifest evidence, severity findings, no-secret stop and role-based remediation. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/network-reviewer.md`; `.claude/agents/security-auditor.md`; `.codex/agents/network-reviewer.toml`; `.codex/agents/security-auditor.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/k8s-validate/SKILL.md` / OBS-044 | Define the validation sequence for manifest changes before GitOps review or merge preparation. / not-declared | move → `.agents/skills/k8s-validate/SKILL.md` | Repository syntax/lint/GitOps/secret validation with blocking failures and missing-tool limits. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/gitops-reviewer.md`; `.claude/agents/k8s-implementer.md`; `.claude/agents/quality-engineer.md`; `.codex/agents/gitops-reviewer.toml`; `.codex/agents/k8s-implementer.toml`; `.codex/agents/quality-engineer.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/knowledge-map/SKILL.md` / OBS-045 | Find stale navigation and duplicate authority without turning an index into a second policy or role roster. / not-declared | move → `.agents/skills/knowledge-map/SKILL.md` | Registry-owned role/skill and Stage 99 routing audit; preserve history; explicit graphify only. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/docs-researcher.md`; `.claude/agents/wiki-curator.md`; `.codex/agents/docs-researcher.toml`; `.codex/agents/wiki-curator.toml`; `baseline:roles/registry.json`. Out: `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/quality.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/ops-runbook/SKILL.md` / OBS-046 | Author and review operations runbooks (`docs/05.operations/runbooks/`) for this repository's WSL2+k3d+ArgoCD platform. Ensure runbooks are executable, verifiable, and safe for operator use without requiring cluster access delegation. / not-declared | move → `.agents/skills/ops-runbook/SKILL.md` | Prerequisites, exact steps, verification, rollback and resource references; live mutating examples OPERATOR-BOUND. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/observability-reviewer.md`; `.codex/agents/observability-reviewer.toml`; `baseline:roles/registry.json`. Out: `docs/05.operations/README.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/rca-methodology/SKILL.md` / OBS-047 | Use when performing root cause analysis with 5 Whys, Fishbone diagrams, Fault Tree Analysis, change analysis, incident cause analysis, or cognitive-bias checks. Timeline reconstruction and remediation planning are outside this skill / not-declared | move → `.agents/skills/rca-methodology/SKILL.md` | Evidence-backed 5 Whys, Fishbone, FTA, change analysis and cognitive-bias checks. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/incident-responder.md`; `.codex/agents/incident-responder.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/requirements-to-design/SKILL.md` / OBS-048 | Use when tracing Requirement Package members to relevant Architecture Descriptions, ADRs, and Spec contracts. / not-declared | move → `.agents/skills/requirements-to-design/SKILL.md` | Full requirement IDs linked to architecture/ADR/Spec; no automatic artifact creation; authorized reciprocal links. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/doc-writer.md`; `.codex/agents/doc-writer.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/risk-report/SKILL.md` / OBS-049 | Define how to identify, score, and report cluster risks in a repeatable format for `hy-home.k8s`. / not-declared | move → `.agents/skills/risk-report/SKILL.md` | Cluster-specific approved static evidence; likelihood/impact; blocking vs monitor risk and allowed handoffs. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/code-reviewer.md`; `.claude/agents/network-reviewer.md`; `.claude/agents/observability-reviewer.md`; `.claude/agents/supervisor.md`; `.codex/agents/code-reviewer.toml`; `.codex/agents/network-reviewer.toml`; `.codex/agents/observability-reviewer.toml`; `.codex/agents/supervisor.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/task-breakdown/SKILL.md` / OBS-050 | Use when decomposing an approved implementation Plan into bounded executable Task records. / not-declared | move → `.agents/skills/task-breakdown/SKILL.md` | Approved Plan to unused Task IDs, exact owners/dependencies/acceptance/evidence; no parallel ledger. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/supervisor.md`; `.codex/agents/supervisor.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/vulnerability-patterns/SKILL.md` / OBS-051 | Use when reviewing Kubernetes manifests or Helm charts for YAML anti-patterns, CIS Kubernetes Benchmark mappings, misconfigurations, manifest hardening, or secure manifest alternatives. Application-layer code vulnerabilities are outside this skill / not-declared | move → `.agents/skills/vulnerability-patterns/SKILL.md` | Manifest anti-pattern reference and severity/CIS evidence; no application-code scope. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/security-auditor.md`; `.codex/agents/security-auditor.toml`; `baseline:roles/registry.json`. Out: none. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/work-lifecycle.md` / OBS-052 | Use one intake-to-handoff procedure for substantial repository work rather than separate bootstrap, preflight, and postflight rule copies. / active | rehome → `.agents/workflows/work-lifecycle.md` | Intake, Git state, assigned ownership, templates, focused checks, ordered completion and canonical handoff; no new authority. Approval: unchanged; Plain procedure is not native SKILL.md; explicit workflows avoid accidental automatic activation. | In: `.claude/CLAUDE.md`; `.claude/agents/code-reviewer.md`; `.claude/agents/doc-writer.md`; `.claude/agents/docs-researcher.md`; `.claude/agents/gitops-reviewer.md`; `.claude/agents/incident-responder.md`; `.claude/agents/k8s-implementer.md`; `.claude/agents/network-reviewer.md`; `.claude/agents/observability-reviewer.md`; `.claude/agents/quality-engineer.md`; `.claude/agents/security-auditor.md`; `.claude/agents/supervisor.md`; `.claude/agents/wiki-curator.md`; `.codex/CODEX.md`; `.codex/README.md`; `.codex/agents/code-reviewer.toml`; `.codex/agents/doc-writer.toml`; `.codex/agents/docs-researcher.toml`; `.codex/agents/gitops-reviewer.toml`; `.codex/agents/incident-responder.toml`; `.codex/agents/k8s-implementer.toml`; `.codex/agents/network-reviewer.toml`; `.codex/agents/observability-reviewer.toml`; `.codex/agents/quality-engineer.toml`; `.codex/agents/security-auditor.toml`; `.codex/agents/supervisor.toml`; `.codex/agents/wiki-curator.toml`; `AGENTS.md`; `CLAUDE.md`; `baseline:README.md`; `baseline:policies/agent-execution.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/git.md`; `baseline:policies/quality.md`; `baseline:providers/claude.md`; `baseline:providers/codex.md`; `baseline:roles/code-reviewer.md`; `baseline:roles/doc-writer.md`; `baseline:roles/docs-researcher.md`; `baseline:roles/gitops-reviewer.md`; `baseline:roles/incident-responder.md`; `baseline:roles/k8s-implementer.md`; `baseline:roles/network-reviewer.md`; `baseline:roles/observability-reviewer.md`; `baseline:roles/quality-engineer.md`; `baseline:roles/security-auditor.md`; `baseline:roles/supervisor.md`; `baseline:roles/wiki-curator.md`; `baseline:skills/delegated-development.md`; `specs:0006-workspace-harness-gap-analysis/spec.md`; `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md`; `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`; `scripts/validate-agent-governance.py`; `tests/README.md`; `tests/test_agent_governance.py`. Out: `baseline:policies/agent-execution.md`; `baseline:policies/approval-and-safety.md`; `baseline:policies/context-and-memory.md`; `baseline:policies/document-authoring.md`; `baseline:policies/git.md`; `baseline:policies/quality.md`; `baseline:roles/README.md`; `baseline:sdlc.md`; `baseline:skills/delegated-development.md`. Verify: current link/profile, role/skill contract and source Git recovery. |
| `skills/workspace-harness-audit/SKILL.md` / OBS-053 | Keep broad workspace analysis complete, evidence-backed, and bounded to the authorized repository work. For narrow document drift use docs-stage-conformance. / not-declared | move → `.agents/skills/workspace-harness-audit/SKILL.md` | Approved requirement/owner coverage; canonical registry, Stage 99 and scripts; bounded remediation/evidence. Approval: unchanged; Registered reusable procedure with concrete role consumers; keep ID and intent with verified explicit-invocation controls. | In: `.claude/agents/quality-engineer.md`; `.codex/agents/quality-engineer.toml`; `baseline:roles/registry.json`. Out: `baseline:policies/quality.md`; `baseline:roles/registry.json`. Verify: current link/profile, role/skill contract and source Git recovery. |

Every source is retained at one reviewed destination; no policy or role is retired for count reduction. Hub/provider/workflow wording and unsafe skill steps are rewritten within the same disposition. The ignored `hooks/__pycache__/post-validate-runner-result.cpython-312.pyc` is retired generated cache from an absent source, not an authority. Personal Claude local settings/notes are preserved without reading contents; references in those private files are outside the inspected content scope.

### Directory Decisions

| Classification | Baseline / native role | Final location / decision |
| --- | --- | --- |
| governance / policies | Nine policies and SDLC, common authored documents | `.agents/governance/`; one normative owner |
| roles | Registry/schema, concrete roles and broad role routers | `.agents/roles/`; preserve identifiers and permission classes |
| agents | Both native agent directories exist | Keep `.claude/agents/` and `.codex/agents/`; no `.agents/agents/` duplicate |
| skills | Sixteen SKILL packages; Claude root symlink; no Codex skill directory | `.agents/skills/` plus individual Claude links; explicit-only invocation |
| workflows | Two plain procedures | `.agents/workflows/`; no native JavaScript workflow |
| providers | Two common-hub provider notes | `.claude/provider.md`, `.codex/provider.md`; native differences only |
| rules / knowledge / prompts / evaluations / scripts | No distinct common consumer needing another owner | Not adopted; existing docs, evals, tests and scripts retain their responsibilities |
| commands / output-styles | No project-native adoption observed | Not adopted; no empty folders |
| agent-memory / agent-memory-local / agent-memory-loca | No project adoption; private ignored state is not common authority | Not adopted; MIG-0009 remains effective |
| templates / skill resources | Stage 99 forms; native skill control sidecars needed | Keep Stage 99; only skill-local `agents/openai.yaml` for Codex invocation policy |
| hooks / settings | Claude registered pre-write hook; no Codex project hook/config | Retain Claude pre-action check; do not activate new hooks or trust |

### Installed Runtime and Official Compatibility Evidence

Sources were consulted on 2026-09-06. Installed versions: Codex CLI 0.140.0,
Claude Code 2.1.261. A documented feature is not proof that this session loaded
it. No minimum-version claim is made where the official page gives no floor.
`codex features list` exited 0: hooks, multi_agent and plugins are enabled;
memories are disabled. These feature flags do not establish project trust or
repository role discovery. Global trust/private configuration was not read.

| Feature | Official source | Minimum condition / adoption | Static result | Actual load / invocation |
| --- | --- | --- | --- | --- |
| Codex project skills | [O1](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/<id>/SKILL.md`; explicit invocation sidecar; use installed loader in fresh session | Name/description, closed package set and sidecars validated | DEFER: this session loaded old gateways; no new paid/authenticated call |
| Agent Skills package | [O13](https://agentskills.io/specification) | Required SKILL filename, name and description; scoped provider extensions | Existing IDs retain registry ownership; no prior SKILL ID/status fields lost | DEFER: parser evidence only |
| Codex agents | [O2](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Preserve `.codex/agents/*.toml`; no model/effort upgrade | TOML and role reference/permission parity | DEFER: native discovery, model access and enforcement unobserved |
| Codex entrypoint | [O3](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [O14](https://agents.md/) | Root AGENTS explicit reads; CODEX.md remains team-defined auxiliary | References resolve; no Claude-style `@` import assumption | DEFER: no new-session auto-loading test |
| Codex configuration | [O4 basics](https://learn.chatgpt.com/docs/config-file/config-basic), [O4 reference](https://learn.chatgpt.com/docs/config-file/config-reference) | No project config adopted; do not change global config | Project config absent, flags queried through CLI | N/A: project configuration not adopted |
| Protected paths | [O5](https://learn.chatgpt.com/docs/agent-approvals-security) | Normal scoped approval for `.agents`/`.codex` writes | Scoped approved writes succeeded; no mount or trust bypass | Observed tool authorization only, not subagent enforcement |
| Codex hooks | [O6](https://learn.chatgpt.com/docs/hooks) | Exact hook-definition trust required; no project hook adopted | No hooks.json/inline duplicate registration | N/A for project; global hooks not inspected |
| Claude settings and imports | [O7 directory](https://code.claude.com/docs/en/claude-directory), [O7 settings](https://code.claude.com/docs/en/settings), [O8](https://code.claude.com/docs/en/memory) | Keep permissions/hooks keys; relative imports from containing file; no Codex entry import | JSON/native keys and current relative imports checked | DEFER: no fresh Claude session or trust grant |
| Claude skill links | [O9](https://code.claude.com/docs/en/skills) | One relative directory symlink per registered skill; SKILL.md; disable-model-invocation true | Registry-derived target set and no-escape checks | DEFER: link contract tested, native load not invoked |
| Claude agents / memory | [O10](https://code.claude.com/docs/en/sub-agents) | Native tool metadata remains unchanged; no persistent memory activation | Native metadata parity; retired memory denied | DEFER: native tool enforcement unobserved |
| Claude dynamic workflows | [O11](https://code.claude.com/docs/en/workflows) | Native JavaScript differs from common Markdown workflow; not needed | No new native workflow created | N/A: not adopted |
| Claude output styles | [O12](https://code.claude.com/docs/en/output-styles) | Provider-specific; no common output-style owner needed | No project output style created | N/A: not adopted |
| Codex execution rules | [O15](https://learn.chatgpt.com/docs/agent-configuration/rules) | Native `.rules` and trusted config layer; not common Markdown rules | No new execution allow rule | N/A: not adopted |

The current Task maps user-level BLOCKED/NOT_RUN required evidence to policy
`DEFER`; FAIL remains FAIL and N/A maps to SKIP with a reason. Neither is PASS.
Direct hook-input tests observe the script adapter, not delivery by Claude.
Native permission prose is not a sandbox proof; no read-only guarantee is
inferred from an omitted Codex sandbox key.

### Template Dispositions

All 32 physical forms were read and matched to their existing consumers.
No form was removed merely to reduce a count. Counts below describe the audit
snapshot before new migration/ADR documents were finalized.

| Physical form | Owning profile | Actual routed consumers | Disposition |
| --- | --- | --- | --- |
| `docs/99.templates/templates/architecture/decision.template.md` | `sdlc/architecture-decision` | 29; `docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`, `docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md` | Keep: ADR consumers retain decision state, explicit non-goals, alternatives and lifecycle traceability. |
| `docs/99.templates/templates/architecture/description.template.md` | `sdlc/architecture-description` | 4; `docs/02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md`, `docs/02.architecture/descriptions/0005-argo-notifications-slack.md` | Keep: AD consumers retain system views, quality attributes and upstream requirement traceability. |
| `docs/99.templates/templates/archive/migration.template.md` | `archive/migration` | 20; `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md`, `docs/98.archive/migrations/0002-sdlc-document-and-governance-consolidation.md` | Update illustrative owner paths; preserve nine-field recovery ledger and immutable historical-consumer procedure. |
| `docs/99.templates/templates/archive/tombstone.template.md` | `archive/tombstone` | 25; `docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md`, `docs/98.archive/superseded/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md` | Keep: exact original-byte payload and sealed provenance differ from migration control metadata. |
| `docs/99.templates/templates/common/readme-collection-index.template.md` | `common/readme-collection-index` | 11; `.agents/roles/README.md`, `docs/02.architecture/decisions/README.md` | Keep: common roles index and SDLC/reference/form collection routers use focused item discovery. |
| `docs/99.templates/templates/common/readme-implementation.template.md` | `common/readme-implementation` | 19; `.agents/README.md`, `.claude/README.md` | Keep: common .agents hub plus provider/implementation entrypoints need structure, configuration and validation navigation. |
| `docs/99.templates/templates/common/readme-repository.template.md` | `common/readme-repository` | 1; `README.md` | Keep: root repository map and getting-started entrypoint remains distinct. |
| `docs/99.templates/templates/common/readme-runtime-governance.template.md` | `common/readme-runtime-governance` | 1; `.github/repository-surface.md` | Keep: GitHub native surface routes policy and workflow responsibility; it does not own common policy. |
| `docs/99.templates/templates/common/readme-stage-index.template.md` | `common/readme-stage-index` | 8; `docs/01.requirements/README.md`, `docs/02.architecture/README.md` | Keep: Stage 01–99 and docs hub routes remain governed; Stage 00 route removed without changing this form. |
| `docs/99.templates/templates/common/readme-workspace-staging.template.md` | `common/readme-workspace-staging` | 1; `_workspace/README.md` | Keep: _workspace staging/router boundary intentionally distinguishes disposable permitted artifacts from private state. |
| `docs/99.templates/templates/governance/contract.template.md` | `governance/contract` | 1; `.agents/governance/sdlc.md` | Keep: SDLC authority is .agents/governance/sdlc.md; semantic type/lifecycle remain stable. |
| `docs/99.templates/templates/governance/provider.template.md` | `governance/provider` | 2; `.claude/provider.md`, `.codex/provider.md` | Keep: .claude/provider.md and .codex/provider.md own their native notes, independent of common authority. |
| `docs/99.templates/templates/governance/role.template.md` | `governance/role` | 19; `.agents/roles/architecture.md`, `.agents/roles/code-reviewer.md` | Keep: neutral registered role and responsibility documents retain bounded duties and lifecycle. |
| `docs/99.templates/templates/governance/rule.template.md` | `governance/rule` | 9; `.agents/governance/agent-execution.md`, `.agents/governance/approval-and-safety.md` | Keep: policies stay flat at `.agents/governance` with English-only and lifecycle validation. |
| `docs/99.templates/templates/governance/skill.template.md` | `governance/skill` | 2; `.agents/workflows/delegated-development.md`, `.agents/workflows/work-lifecycle.md` | Clarify flat-workflow intent; work-lifecycle and delegated-development remain governed workflow documents using stable governance/skill type. Native packages use the separate native profile. |
| `docs/99.templates/templates/operations/guide.template.md` | `operation/guide` | 1; `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` | Keep: operator reader outcome and verified instruction traceability remain distinct from policy/runbook. |
| `docs/99.templates/templates/operations/incident.template.md` | `operation/incident` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: incident fact/timeline and coordination/closure contract is required before an event exists. |
| `docs/99.templates/templates/operations/policy.template.md` | `operation/policy` | 5; `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md`, `docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md` | Keep: operational controls and exception approval remain distinct from common agent policy. |
| `docs/99.templates/templates/operations/postmortem.template.md` | `operation/postmortem` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: retrospective causal analysis/actions remain distinct from incident facts. |
| `docs/99.templates/templates/operations/runbook.template.md` | `operation/runbook` | 9; `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`, `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` | Keep: repeatable operator decision and stop/rollback evidence remain distinct from guidance. |
| `docs/99.templates/templates/references/audit-pack.template.md` | `common/readme-audit-pack` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: Stage 90 audit collection requires a pack router even when no pack is current. |
| `docs/99.templates/templates/references/audit.template.md` | `reference/audit` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: audit evidence membership has its own exact route, identity and freshness semantics despite shared structural headings. |
| `docs/99.templates/templates/references/data-pack.template.md` | `common/readme-data-pack` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: Stage 90 data collection requires provenance/refresh pack routing. |
| `docs/99.templates/templates/references/data.template.md` | `reference/data` | 0; None; deliberate capacity documented in Stage 99 README | Keep deliberate empty capacity: data reference identity and ownership remain distinct from research/audit despite shared structural headings. |
| `docs/99.templates/templates/references/research-pack.template.md` | `common/readme-research-pack` | 1; `docs/90.references/research/0001-workspace-engineering/README.md` | Keep: research collection pack routing owns report navigation and freshness boundaries. |
| `docs/99.templates/templates/references/research.template.md` | `reference/research` | 13; `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md`, `docs/90.references/research/0001-workspace-engineering/m0002-harness-and-loop-engineering.md` | Keep: source-backed findings retain exact member identity and freshness semantics. |
| `docs/99.templates/templates/requirements/requirement-package.template.md` | `sdlc/requirement` | 4; `docs/01.requirements/0001-argo-rollouts-progressive-delivery.md`, `docs/01.requirements/0002-argo-notifications-slack.md` | Keep: solution-independent requirements, acceptance and complete member IDs stay owned by Stage 01. |
| `docs/99.templates/templates/runtime/claude-agent.template.md` | `common/provider-native-metadata` | 12; `.claude/agents/code-reviewer.md`, `.claude/agents/doc-writer.md` | Update explicit registry/workflow reads; preserve native metadata placeholders and tools boundary. |
| `docs/99.templates/templates/runtime/codex-agent.template.toml` | `common/codex-agent-binding` | 12; `.codex/agents/code-reviewer.toml`, `.codex/agents/doc-writer.toml` | Update explicit registry/workflow reads; preserve native TOML model/reasoning/developer instructions. |
| `docs/99.templates/templates/specs/plan.template.md` | `sdlc/plan` | 57; `docs/03.specs/0004-argo-rollouts-progressive-delivery/plan.md`, `docs/03.specs/0005-argo-notifications-slack/plan.md` | Keep: execution dependencies, work packages and verification/rollback belong in Plan. |
| `docs/99.templates/templates/specs/spec.template.md` | `sdlc/spec` | 67; `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`, `docs/03.specs/0005-argo-notifications-slack/spec.md` | Keep: behavior, interfaces, failure modes and acceptance contract belong in Spec. |
| `docs/99.templates/templates/specs/task.template.md` | `sdlc/task` | 347; `docs/03.specs/0004-argo-rollouts-progressive-delivery/tasks/tsk-0001-rol-t-001.md`, `docs/03.specs/0004-argo-rollouts-progressive-delivery/tasks/tsk-0002-rol-t-002.md` | Keep: bounded execution/evidence, approvals, secret handling and rollback remain Task-owned. |

### Implementation Review and Integration Evidence

The 53-source disposition is 48 moves, four rehomes (two provider notes and
two plain workflows), and one hub rewrite. Relative references change with the
moves; risky skill procedures now explicitly preserve approval and read-only
boundaries. Sixteen Codex sidecars and sixteen per-skill Claude links constrain
implicit activation without granting tools or native permissions. No generator
or duplicate role body was added.

The installed Superpowers 6.3.0 using-superpowers, brainstorming, writing-plans,
executing-plans, test-driven-development, systematic-debugging and
verification-before-completion procedures were read and applied. Their local
package is under the existing openai-curated-remote plugin cache; no plugin or
global installation changed. Stage 03 routing and this request's no-commit
boundary override the skills' default output paths and commit suggestions.
An actual read-only design reviewer verified all 53 source hashes and unique
destinations before implementation. The latest user instruction is the scope
approval; ADR-0035 starts at the required `proposed` state. No accepted-state
transition or reviewer signature is fabricated.

An independent Python review identified two read races in the snapshot and
registry paths. Descriptor-relative bounded I/O now pins every parent and uses
no-follow regular-file reads; deterministic harmless leaf/parent replacement,
input mutation and byte-budget regressions passed in the delegated checks.
The primary worker inspected the final diff and ran the combined bounded-I/O,
QA and migration tests: 50 cases, 196.297 s, one fixture setup error after the
old parent directory was correctly removed. Recreating the synthetic parent
fixed that case; its focused rerun passed (1 case, 7.345 s). This was a test
setup repair, not a production waiver. The requested independent re-review
was unavailable because the reviewer service rejected the turn; no second
independent approval is claimed.

| Integrated observation | Exit / state | Scope and response |
| --- | --- | --- |
| First migrated `python3 scripts/qa.py full` | 1 / FAIL | 1,033.297 s; 1,022 snapshot paths; 19 gates, 14 PASS and 5 FAIL; formatter mutation was also rejected |
| Agent, profile/registry and links gates in that run | 0 / PASS | Current snapshot and Git-backed historical successor proof; no native runtime claim |
| Archive cutover in that run | 1 / FAIL | Legacy MIG-0002 current-endpoint check; repair must use proven successors, retaining sealed bytes |
| Unit tests and pre-commit in that run | 1 / FAIL | Full discovery exposed additional fixture/process-owner failures; pre-commit found two public-identity entropy candidates, one extra blank line and six formatter changes. Detailed layer reproduction is required before rerunning full |
| `python3 scripts/qa.py quick` after initial corrections | 1 / FAIL | 1.308 s; old indexed Claude skill link remained in the changed list as a current directory; exact file-to-directory transition regression added |
| Document lifecycle in that run | 1 / FAIL | New ADR cannot be created directly accepted; corrected ADR-0035 to proposed, with direct user scope authorization recorded separately |
| Repository quality in that run | 1 / FAIL | Unimplemented projection-validator proposal retained a full executable path; corrected that historical citation without inventing executable history |

The actual pinned pre-commit tools were available. The isolated pre-commit
reproduction completed in 30.460 s and identified three failing hooks:
detect-secrets, markdownlint and ruff-format. No hook was skipped to repair them.
Two exact Hex High Entropy findings matched the already-public Gitleaks archive
checksum and the existing audit Git commit (the Git object was checked locally).
Only those two fingerprints were added to the existing secret baseline as
non-secrets; detector plugins, thresholds, filters and workflow bytes are
unchanged. A temporary static-only scanner probe passed for these identities
(rc 0) and rejected a different synthetic value in the same workflow (rc 1).
The scanner's network-verification-disable option was used only for that probe;
Git hooks were not bypassed. No actual credential values were collected.
Pinned Ruff 0.16.5 reformatted six reported Python paths; AST comparison proved
four otherwise-unchanged validator/CI-test files remained semantically identical.
The other two already belonged to this migration. One Markdown blank line was
removed. These changed bytes require new pre-commit evidence.

The isolated unit reproduction then ran 803 cases in 701.636 s and failed
16 assertions plus one helper-call error. Four process assertions concerned
already-killed fixture zombies owned by the outer QA subreaper. The fixture
now temporarily owns and waits for its exact synthetic children; the previous
subreaper state is restored and the production runner is unchanged. All 39
consumer tests passed under the outer bounded runner (1.619 s). Archive tests
now supply the required scanner through the existing secure executable selector,
use proven current successors and the current helper signature, and accept zero
historical fallback batches when current successors suffice. Four original
archive failures passed in an isolated snapshot (60.827 s); three dedicated
fallback/byte-budget refusal cases passed (35.172 s). Existing Git process and
60-second single-validation bounds remain unchanged.

The pre-edit hook now rejects the retired governance root before the QA selector:
a deletion proof may route QA to a successor, but cannot authorize recreating the
source. Old standalone forms still return the existing HOOK-DOC-RETIRED code.
The symlink write-refusal case now exercises an individual Claude skill link.
All 27 hook cases passed in the bounded snapshot (1.823 s, four linked-worktree
cases N/A because none exists); this is adapter subprocess evidence, not a
native Claude event or trust decision. No hook registration was added.

A later quick run selected 297 changed paths and eleven validators, completing
in 255.429 s with one failure: proposed ADR-0035 lacked a reciprocal Spec link.
The Spec now links the proposed decision and separately names the explicit local
user request as implementation authority. A repeated isolated pre-commit run
(35.748 s) reported only a synthetic PEM redaction fixture; its exact fake-data
line now has an explained allowlist annotation. All other hooks passed and
that snapshot had no formatter changes. The diagnostic regression still checks
redaction, escaping and output bounds. The final integrated outcome is recorded below; these failures are retained
as actual intermediate evidence.

The original Git index remains untouched. Staged and commit-message evidence
are N/A for this explicitly uncommitted handoff. Existing main QA/CI already
selects one unit discovery and one pre-commit invocation; this migration keeps
all 19 logical gates and full/CI membership equal. It removes a duplicated
mutable status map and the duplicated hub authority inventory check while
retaining profile-owned lifecycle states, exact recovery, model/permission
parity and bounded execution. No measured performance improvement is claimed.

### Final Source and Residual Classification

The direct governance command passed against the working-tree snapshot
(`python3 scripts/validate-agent-governance.py --root .`, rc 0, 43.450 s):
2 providers, 12 roles, 3 permission classes, 16 skills, 34 handoffs and
36 projections were derived from the current registry. These observed counts
are not pinned acceptance thresholds. Source-to-target registry metadata was
compared recursively after path translation; model, permission, tool and
handoff semantics were preserved.

`lstat` confirms the former root is absent, including dangling-link detection.
The final text sweep used NUL-delimited tracked plus nonignored untracked
paths, refused external symlink traversal, and decoded escaped JSON separators
and URL escapes when matching. It covered 1,006 regular UTF-8 text files and
16 internal skill links. The former indexed Claude skill leaf is now a
directory, inspected through its sixteen children rather than read as a file.
Ignored personal settings/memory, Git internals, third-party tool caches and
binary data are outside content inspection; personal-state filenames and types
were checked without reading values. No ignored former-root residue remains.

| Residual class / exhaustive path grouping | Files | Matching lines | Reason |
| --- | --- | --- | --- |
| `.claude/hooks/` and `scripts/` | 6 | 40 | Explicit old-root refusal or exact Git-backed historical source/disposition proof; no working-tree fallback loader |
| `docs/02.architecture/decisions/` | 3 | 7 | Superseded ADR-0013/0019 and explicitly narrowed ADR-0034 preserve their historical decision bodies |
| `docs/03.specs/` | 7 | 39 | Completed Task evidence, superseded proposals, and explicitly historical sections of reconciled SPEC-0054/0062; current owners are linked separately |
| `docs/90.references/` | 8 | 45 | Observation-dated research governed by its non-authoritative pack contract |
| `docs/98.archive/` | 92 | 868 | Sealed records and successor/recovery evidence; twenty existing migration records retain exact baseline bytes |
| `tests/` | 15 | 59 | Old-root refusal, historical proof, malformed-owner and reintroduction regression cases |

All 1,058 matching lines across 131 files have a category; none of the sixteen
link targets points to the retired root. Counts describe this sweep, not a
claim that textual matches were erased. Current link/profile, governance and
full-QA results passed: functional references to the removed working-tree
owners are zero within this inspected repository scope. Private ignored
provider content is not included in that statement. No provider generator exists or
was introduced; generator drift/fixed-point evidence is N/A. Repeated static
validation must leave both the working tree and old-root absence unchanged.

### Final Validation and Handoff

Code and document migration is locally complete. Native fresh-session discovery,
invocation, model access, sandbox enforcement and Claude event/trust delivery
remain DEFER; hosted GitHub Actions execution also remains DEFER. Static success
is not evidence for these boundaries, so WORK-004 and this Task stay in progress.
The migration handoff originally excluded commits. The subsequent request
authorizes local commits; remote integration, authenticated provider calls and
live operations remain excluded. The branch and workspace remain available.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| `python3 scripts/validate-agent-governance.py --root .` | 0 / PASS | Working-tree snapshot, 43.450 s; role, skill, permission and historical consumer proof |
| `python3 scripts/qa.py full` | 0 / PASS | Isolated working-tree snapshot, 1,022 paths, 19/19 gates, 942.856 s; unit discovery and all-files pre-commit included; no snapshot mutation |
| Full/CI registry equality and baseline comparison | 0 / PASS | All nineteen gate definitions and profile membership unchanged; one unit discovery and one pre-commit per profile |
| `python3 -m unittest tests.test_validation_tooling_ownership.ValidationToolingOwnershipTests.test_native_shell_hooks_share_existing_shell_validation -v` | 0 / PASS | New native Shell-route regression; original two missing-route assertions failed before the narrow configuration correction |
| Isolated `pre-commit run --all-files` after Shell-route correction | 0 / PASS | 34.498 s; existing shellcheck/shfmt now include Claude hooks; actionlint/zizmor and other applicable hooks pass; no formatter changes |
| `git diff --check` and `git diff --cached --check` | 0 / PASS | Working diff and original empty index; staged validation itself is N/A because staging/commit is not authorized |
| Final changed-path `python3 scripts/qa.py quick` | 0 / PASS | 299 changed paths, eleven gates, 215.901 s; no snapshot mutation; final result text is checked separately without repeating unit discovery |
| Final Task profile and Markdown checks | 0 / PASS | Strict markdown-profile command with only this Task selected; isolated markdownlint-cli2 with only this Task selected; final traceability matches the current Task table |
| Native runtime / hosted CI / live systems | NOT_RUN / DEFER | No new-session provider call, trust grant, remote workflow or cluster operation; no inferred success |
| Provider generation / second generation | N/A / SKIP | No generator adopted; repeated validation left the old root absent |

The full snapshot preceded the final narrow Shell-route addition and its new
regression. Those exact changed bytes were separately verified by the focused
test and all-files pre-commit; the Task evidence update is checked by the final
changed-path profile. This scopes the evidence honestly without rediscovering
and rerunning the unchanged full unit set.

The source root and fifty-three unique regular destinations were rechecked.
All twelve Claude frontmatters and Codex TOML metadata, excluding migrated
instruction text, exactly match baseline Git blobs. The registry matches the
baseline recursively after path translation. All twenty pre-existing migration
records match their original bytes. Existing main workflow bytes, native Claude
settings, manifests, Helm values, Rego policies and bootstrap implementation
remain unchanged; only the policy README authority link moved.

Fixture `validation-surfaces.json` retains all 94 cases (23 surface, 19 selection,
6 CI-range, 5 rejection, 4 argv-positive, 37 mutation). Its obsolete parallel-CI
job expectations now refer to the already-established single QA job, reducing
33,507 bytes to 30,734 bytes without removing risk cases. No runtime or hosted
speed improvement is claimed. The baseline full run could not discover tests,
so its duration is not a comparable performance baseline.

The start and handoff HEAD remain `eb4fcfe3283115388d6eb1f31d56780b3e578f77`
on `codex/common-agents-authority`, based on main. No commits or staging were
performed. Both original stashes and personal ignored files are preserved.
Rollback means reviewing and reversing only this uncommitted migration against
that baseline, including new destinations and restored source paths together;
check for later user changes first. Do not reset the workspace, discard user
work, or restore retired provider memory as part of rollback.

### Authorized Local Commit and Follow-up Review

The user subsequently requested a commit and review/progress on the next work.
This authorizes local staging and commits, superseding the earlier no-commit
boundary without changing the remote, credential, paid-call or live boundaries.
Earlier empty-index observations above remain historical evidence.

The resumed inspection found the same branch and baseline HEAD, 155 modified,
54 deleted and 91 untracked paths, an empty index and both existing stashes.
The previous temporary logs are unavailable in this session; retained Task
results are prior evidence. Record new index validation separately before
claiming a successful commit. The migration and dependent consumers form one
atomic commit; moving only the source files would leave broken consumers.

The active `core.hooksPath` is the existing user hook directory. Its pre-commit
secret check does not chain the repository's pre-commit or commit-msg hooks.
Keep it enabled and run the repository-configured checks explicitly; do not
change global hook configuration or bypass either check boundary.

Next scope is WORK-004: inspect installed provider discovery interfaces using
read-only local commands, then record observed loading and outstanding external
evidence. No fresh paid model call, trust change or hosted run is authorized.

The first actual `python3 scripts/qa.py staged` exited 1 with
`SURFACE-PATH-NODE: .claude/skills`. The staged selector retained the deleted
root symlink beside its newly staged children. Its correction uses only HEAD
blob modes and index paths, omitting the replaced leaf only when every indexed
child is selected. It neither reads unstaged files nor waives child validation.
Two regression tests first failed on the unexpected parent path; the positive
fixture then needed its skill registry to satisfy the existing link contract.
The corrected `python3 -m unittest tests.test_qa_runner -v` passed all 29 tests
in 16.262 seconds. Unknown child paths still fail and ordinary deletions remain.

The synthetic PEM redaction fixture now constructs the same 9,077-byte payload
from a visible label and envelope, avoiding a literal credential-like marker
in added source lines. No real key material, scanner exception or hook change
was introduced. Independent Python review confirmed byte equality and the four
unchanged assertions; all four focused diagnostic tests passed.

Independent read-only WORK-004 review confirmed Codex 0.140.0 and Claude
2.1.261. Version/help commands exited 0; Codex warned that its attempted PATH
alias setup was blocked by the read-only filesystem. This is help evidence,
not a successful native loader test. `claude agents` manages active sessions,
so it must not be used as a custom-role inventory check. Help for
`claude plugin validate`, `codex app-server generate-json-schema` and
`codex debug prompt-input` identifies parser/schema/context interfaces but
does not establish session-free operation without private-state access.
Those execution commands were not run. No vetted session-free discovery route
was established; this does not prove paid inference is inherently required.
WORK-004 native and hosted results therefore remain DEFER with their existing
owners, rather than claiming completion from CLI help.

The reviewed migration was committed locally as `add86fbd`:
`refactor(governance): migrate shared authority to .agents`. It contains 248
Git diff entries after rename detection (300 source/destination status paths).
The working tree and index were clean afterward; both stashes remained intact.

| Commit validation | Exit / result | Exact scope |
| --- | --- | --- |
| `python3 scripts/qa.py staged` after correction | 0 / PASS | Actual index snapshot, 299 selected paths, eleven gates; no unstaged differences |
| `python3 scripts/qa.py full` | 0 / PASS | Same code and document bytes, nineteen gates, 935.675 s; whole unit discovery and all-files pre-commit included once |
| `pre-commit run --all-files --hook-stage commit-msg --commit-msg-filename /tmp/hy-governance-commit-message.txt` | 0 / PASS | Exact commit message; commitizen passed without changing the active global hooks |
| `git diff --check`, `git diff --cached --check` and index identity comparison | 0 / PASS | Verified index unchanged through validation; zero unstaged paths |
| `git commit -F /tmp/hy-governance-commit-message.txt` | 0 / PASS | Active user pre-commit secret hook enabled; no bypass, remote action or signing override |

The first commit-message check without `--all-files` exited 3 because its
internal `git write-tree` needed protected index writes. The successful
commit-message-only invocation avoided that unnecessary index operation;
commit-message validation and the active commit hook were both retained.
Independent Python review also approved the staged path correction after its
mode, literal-path, deletion and unselected-child boundaries were checked.

#### Next local work: required reference collections

The post-commit review of SPEC-0071 C12 / VAL-DTF-012 found that the existing
topology validator skipped an entirely missing Stage 90 collection. Its three
routers and form bindings already exist. Removing only the skip delegates to
the existing bounded `lstat` directory reader, preserving no-follow behavior,
entry/byte limits and the unchanged timeout. No archive payload or new form is
needed. This narrow document-gate continuation is recorded here; the predecessor
Task retains its original lifecycle and historical outcomes.

`python3 -m unittest tests.test_reference_pack_routes.ReferencePackRouteTest.test_empty_collections_require_all_three_directories -v`
first exited 1 with three expected failures: each missing collection incorrectly
passed. After the correction, `python3 -m unittest tests.test_reference_pack_routes -v`
exited 0 with ten tests in 0.090 s. All-empty collections with their routers
remain valid; the three existing duplicate/index-drift fixtures now include the
mandatory routers so their original failure assertions remain meaningful.
Independent Python review found no issues and confirmed ordinary and dangling
directory links remain rejected. `python3 scripts/qa.py full` exited 0 with
nineteen gates in 1,020.017 s, including unit discovery and all-files pre-commit
once. This result covers the continuation's six changed files before this
evidence-only update; the first commit's full result was not reused for them.
The final `python3 scripts/qa.py staged` exited 0 with eleven gates in
221.998 s. Commit-message checks, focused Markdown lint and both diff checks
passed. The six reviewed files were committed as `2b884cfa`,
`fix(docs): reject missing reference collections`, with the active secret hook
enabled. No archive payload or remote state changed.

#### Next local work: quick selection after staging

Independent review found that `quick` still retained the deleted parent of a
file-to-directory replacement after the children were staged. At that point
the index contains only children; the previous leaf exists in HEAD. The
expanded before/after-staging regression first exited 1 with the expected
parent-path assertion failure only in the staged subcase.

The existing literal HEAD blob/mode check is now a shared helper. `quick`
accepts the previous leaf from index or HEAD only when the working path is a
directory and all children are selected. The staged selector still uses only
HEAD/index metadata. Unknown children, plain deletions, gitlinks, escaping
links and source-index identity checks retain their independent tests.
`python3 -m unittest tests.test_qa_runner -v` exited 0 with 29 tests in
17.091 s; pinned Ruff lint and formatting passed. Independent Python review
approved the two-file correction, including literal paths, allowed modes,
gitlink rejection and unchanged process/environment boundaries.

`python3 scripts/qa.py full` exited 0 with nineteen gates in 927.707 s,
including whole unit discovery and all-files pre-commit once. That snapshot
precedes only this evidence update. Focused Markdown validation checks the
updated record, and the required final `python3 scripts/qa.py staged` checks
the actual index before commit. Its exact exit, scope and duration belong to
the commit message for `fix(qa): handle staged directory transitions in quick`,
so recording the final index result does not alter the checked index.
Both native provider execution and hosted CI remain DEFER; this local result
does not advance WORK-004 or authorize external changes.

### Historical Execution Record (before the authority-location revision)

The following dated observations describe previous commits and working trees;
the current Spec and plan supersede their forward-looking topology and commit
instructions. Past failures and outcomes remain unchanged.

Execution is in progress. PR 56 merged only ADR/Spec/Plan/Task documentation;
its description lists implementation and validation that the four-file diff
does not substantiate. The existing workflow and `.agents/` remain at the
baseline, and the QA entrypoint is not implemented. No new hosted execution,
provider loading, cluster action or implementation commit is claimed.

### Resume Evidence (2026-09-05)

- Verified origin identity: `github.com/buenhyden/hy-home.k8s.git`.
- Original branch `codex/document-contract-v9`, HEAD
  `6c5ad33444fdbdbe4fb10e9d652287d89a56fe99`: preserve the other task's
  twenty-two staged paths, this task's six unstaged paths and both stashes.
- Initial sandboxed fetch failed (255: read-only FETCH_HEAD). The scoped
  approved fetch succeeded (0), updating origin/main from
  `1632ce28443b5b5bebf9abdba13543d5731f43bc` to
  `bb73116b7b09c4f257fc81baa12cfa8359495fc0`.
- The old work branch and current main diverge four commits on either side,
  with merge-base `14375f9578e26cf244df821671501979970134f7`. An approved
  worktree creation started `codex/agent-governance-qa-completion` at current
  origin/main. The original worktree/index was not switched or modified.
- Replayed only this task's quality-policy/runner-test and registry-reader/
  reader-test changes into the new worktree. The old Spec 0054 Plan/Task
  amendments remain preserved in the original workspace, not copied as a
  second execution owner; this Task now owns continuation evidence.
- Local WSL Linux uses Python 3.12.3, PyYAML 6.0.1 and jsonschema 4.10.3 from
  system packages. The separate pre-commit CLI exists; its module is not
  installed into this system interpreter. Exact tool readiness is checked by QA.

| Command / observation | Exit / state | Evidence scope and result |
| --- | --- | --- |
| Direct strict links-and-owners at clean main | 1 / FAIL | Missing Plan and Task criterion links, missing Requirement reciprocal link, missing Stage 03 index row/tree entry for Spec 0072 |
| Direct repository quality at clean main | 1 / FAIL | EXECUTABLE-HISTORY: accepted ADR-0034 references a QA executable absent from the tree/history |
| `bash scripts/validate-repo-quality-gates.sh .` at clean main | 1 / FAIL | 383.123 seconds; 1019 paths, two failed validators: links-and-owners and repository-quality; raw bounded summaries retained in temporary baseline log |
| CI run 33935010482, job 101221189172, existing log read | failure | Same two failing validator IDs; stdout digests match the clean local baseline. The log provides hashes/counts rather than the detailed errors reproduced above |
| Existing CI run 33935010482 ci-summary | failure | Hosted evidence for the baseline SHA only; not this worktree |
| Disposable venv interpreter probe | 0 / reproduced defect | Parent venv Python invokes `/usr/bin/python3` through the runner's closed PATH; child modules come from system dist-packages |
| Local branch creation | 0 / PASS | New isolated branch/worktree exists; no source migration or implementation completion implied |

### Audit and Execution Decisions

| Request item | Current path / symbol | Current authority | Conflict evidence | Disposition | Final owner | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| Common roles and skills | `.agents/registry.json`, role/skill bodies | Registry plus Stage 00 prose | Gateways still delegate exact authority outside Stage 00 | Migrate | Stage 00 roles/skills; provider metadata stays native | Registry/path/permission/handoff/skill negative tests, old-tree absence |
| Codex skill loading | provider skill symlink | Native discovery differs from file presence | Provider link alone is not repository skill registration | Modify | Root gateway explicit Stage 00 procedure reads | Reference resolution; native registration is not claimed |
| Plan authority and completion | ADR-0034, Spec/Plan/Task 0072 | Existing package | PR body claims implementation absent from merged diff | Modify | Same existing owners | Strict links, profiles, actual executable checks |
| QA registry | validation registry and planned QA registry | Existing validation registry | Draft duplicates argv and timeout ownership | Integrate | Existing registry plus ID-only profiles | Unknown/duplicate gates, full/ci parity, bounded failures |
| Python environment | runner executable resolution | Closed PATH | Parent venv selection is discarded | Modify | Exact trusted interpreter plus closed environment | Venv and PATH-shadow regression tests |
| QA/CI duplication | workflow jobs and local aggregate hooks | Multiple callers | Aggregate plus focused unit discovery, repeated setup | Integrate after consumer audit | One QA call, narrow pre-commit, fail-closed summary | Invocation graph, workflow tests, final profile timings |
| Historical/in-progress contracts | ADR-0030/31/33; Specs 0054/68/70/71 | Existing scoped owners | 0068 requires mass model upgrades; 0070 exempts closed conflicts | Modify overlapping instructions; retain independent unfinished work | Spec 0072 for this cutover, original owners otherwise | Current-reference and lifecycle checks |

Ruling: use direct native read instructions rather than a projection framework;
this follows ADR-0034 and removes manual shared-body duplication. Ruling: use
one executable validation registry, with QA profiles selecting IDs; no duplicate
command/timeout owner. Ruling: do not rerun full, ci and pre-commit over identical
bytes; verify profile parity in tests and record changed-byte reruns separately.
No ruling authorizes remote mutation or weakens a pre-action safety boundary.

### Current-State Integration Handoff (2026-09-05)

The related Task 4 retirement is committed as `2b9bf9e`; the document and
governance branches merged to main as `0540a433` and `acbdca17`, respectively;
the remote audit snapshot is `76ef4953`. The focused integrated suite ran 57
tests: 56 passed, and the
sole failure is an empty `.agents` directory created by the sandbox rather than
a repository-owned source surface; the isolated Stage 00 owner check passes.
MIG-0020's two registry/schema successor rows and narrow `.agents` sealed-edge
composition resolve the archive proof without a validator waiver. Focused
regression passed (1 test, 0.141 s) and the exact staged-snapshot archive target
passed (1 test, 17.747 s). Independent evidence and code review found no
blockers, and the `-t .` import path is corrected.
Full-suite, hosted CI, provider/runtime, and release evidence are not claimed;
this Task remains `in-progress`.

### Hosted CI Failure Reproduction and Repair (2026-09-08)

The consolidation left hosted CI failing on every push. Run `34128911521`
attempt 1 checked `de040df41f038e981963de1ac60093ea6fb80edd` on 2026-09-07 and
failed `Validate repository checkout`, which failed `ci-summary`. That FAIL is
an observed fact and is not restated as a pass anywhere below.

The cause is one line this package introduced. The QA job checks out
`${{ github.sha }}`, which `actions/checkout` performs as
`git checkout --force <sha>`, leaving a detached HEAD; the hosted checkout log
records exactly that. `current_named_durable_ref` resolved the archive
retention anchor only through `git symbolic-ref HEAD`, so the anchor could not
resolve and `archive-cutover`, `agent-governance`, `document-lifecycle`,
`links-and-owners` and the archive unit tests all failed `RECOVERY-DURABLE-REF`.
A clone detached at the same commit reproduced the hosted diagnostics
byte for byte, and the last green run was green because `ci.yml` then had no
`ref:` and checked out a branch. `pre-commit` failed separately and for an
unrelated reason: the runner resolves tools against a fixed system search path,
so the console script `pip` installs beside the interpreter was never visible
and the gate had been closing on an absent required tool rather than running.

Resolution keeps the exact-SHA checkout, which is what binds hosted evidence to
one commit. The resolver now also accepts a named ref whose tip is the
checked-out commit, and the workflow names the commit it checked out because a
`pull_request` event validates a merge commit that no fetched branch ref points
at. Both were needed; neither alone covers both events.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| `python3 scripts/qa.py full` | 0 / PASS | Isolated working-tree snapshot at `1aede195`, 22/22 gates including one unit discovery and one all-files pre-commit; no snapshot mutation |
| CI-shape simulation: clone detached at `1aede195`, workflow binding step, `python3 scripts/qa.py ci --base-ref ""` | 0 / PASS | 22/22 gates; HEAD started detached and the binding step produced `refs/heads/ci-validated-checkout` with its tip still the exact commit |
| Detached-checkout regression before the workflow binding | 0 / PASS | `tests.test_archive_validation` and `tests.test_archive_recovery`, 135 tests, on a clone with no symbolic HEAD; the same clone failed 9 tests and errored 14 before the fix |
| Baseline reproduction of the hosted failure | 1 / FAIL as expected | `archive_cutover.py`, `validate-agent-governance.py`, `validate-document-lifecycle.py` and `validate-links-and-owners.py` on a detached clone of `de040df4` returned the hosted diagnostics unchanged |
| `python3 scripts/qa.py staged` per logical unit | 0 / PASS | Exact index of each of the eight commits; selected gates only |
| Profile membership contract | 0 / PASS | `--list` shows `full` and `ci` identical at 22 gates, `quick` and `staged` identical at 15, and no duplicate gate ID in any profile |
| Hosted GitHub Actions on the repaired commit | NOT_RUN / DEFER | Push, dispatch and re-run remain unauthorized, so no hosted result exists for `1aede195`; the 2026-09-07 FAIL stands as the last hosted observation |
| Provider runtime and live systems | NOT_RUN / DEFER | No provider session, cluster, Vault or reconciliation action |

Gate ownership was consolidated in the same scope. `kube-linter` ran twice per
`full` and `ci` run, from the manifest script and the pinned pre-commit hook,
with the same config over the same objects; the script's copy was optional and
returned success when the binary was absent, which is the state hosted CI has
always been in. The pinned hook is now the only owner. The policy gate ran
Conftest and a built-in Python reimplementation of the same rules
unconditionally, and `policy/conftest/kubernetes.rego` was Rego v0 and does not
parse under OPA 1.x, so the copy was the only engine that had ever evaluated
these rules while the gate still reported PASS. The policy is ported to Rego v1
with executable rule tests, the reimplementation is deleted, and Conftest is
required rather than optional. No execution-time improvement is claimed; these
are execution-count and ownership changes, not measured speed changes.

`scripts/validate-repo-quality-gates.sh` was retired. It was a second public
entrypoint that ran the all-files lane against the live working tree with no
snapshot isolation and no profile or index semantics, and it owned no gate the
`full` profile does not. Its consumers cite `python3 scripts/qa.py full`, and
the aggregate-ownership tests keep their guarantees against `scripts/qa.py`.
`governance-audit-snapshot.yml` was retired as well: its trigger branch no
longer exists on the remote, its artifact retention has expired, and the commit
it captured is an ancestor of `origin/main`, so the bundle remains reproducible
from history.

Two limitations are recorded rather than resolved. `core.hooksPath` in this
workspace points at a user-global hooks directory, so the repository's own
pre-commit and commit-message hooks did not run at commit time; the all-files
pre-commit gate inside the `full` profile covered the same bytes and caught
formatter findings, which were committed separately, and commit messages were
checked against the tracked `.cz.toml` pattern. Global Git configuration was
not modified.

Two tests were observed failing once each under whole-suite discovery while
passing in isolation. `test_root_cli_path_remains_green_without_a_production_self_test`
is repaired: it carried two state dependencies. Its loader removes the script
directory from `sys.path` after loading, so the `import qa` inside `main` only
resolved when an earlier module had already imported it, and the module failed
on its own. It also asserted the consumer was called with the repository root,
which only holds for a clean working tree, because a dirty tree makes `main`
hand the consumer an isolated snapshot that is released when the command
returns. The test now restores the search path the way a script invocation
provides it and records what the consumer received while it is still readable,
pinning one dispatch over this repository's own registry bytes. Both branches
are verified: a dirty tree takes the snapshot path and a clean clone takes the
indexed-tree path.

`test_escaped_devnull_descendant_is_killed_and_not_reported_completed` is not
repaired, because no root cause was established. It passed 25 consecutive runs
under concurrent load, in its own module, with every alphabetically preceding
module, and under a discovery pass that imports every module, so module
interference, import side effects and load alone are excluded. The one hosted
observation pairs an inner test failure with `status=descendant_cleanup` on the
outer `unit-tests` gate, which places the escaped process outside the inner
detection window and inside the outer one; subreaper restoration ordering in
`run_bounded_command` is the open hypothesis. It is left unrepaired rather than
adjusted, because the assertion guards a real containment boundary and no
reproducible failure exists to prove a change fixes anything.

Rollback is a new change reversing the reviewed commits against
`de040df41f038e981963de1ac60093ea6fb80edd` after checking for later user edits;
no history rewrite, no blanket restore. Reversing the resolver alone would
restore the hosted failure, so the resolver and the workflow binding roll back
together. The next owner is platform, for hosted verification once push is
authorized, and for the two order-dependent tests.

### Hosted Result and the Two Gates It Exposed (2026-09-08)

The repair merged as `d284c99e` and hosted CI ran the QA job to completion for
the first time. Twenty of twenty-two gates passed, including all five that the
detached-HEAD defect had been failing, and the three added steps -- the ref
binding, the pre-commit publish, and the pinned Conftest install -- all
succeeded. The job ran 27m55s against the 9m8s of the run that used to die
early, which is the shape of a job that now reaches its slow gates instead of
failing before them.

Both remaining failures are gates that had never executed in hosted CI, so
neither was a regression from the repair; each was a latent fault the repair
made reachable.

`pre-commit` failed with pre-commit's unexpected-error exit. Its cause is
exact and was reproduced locally:

    go install ./...: failed to initialize build cache at
    /nonexistent/.cache/go-build: mkdir /nonexistent: permission denied

`HOME` is unreachable by design so no ambient startup state is read, but hook
environments that build from source ask their toolchain for a cache under
`HOME`. Every local run had passed only because its hook cache was already
warm and no toolchain ever built. The runner now names each toolchain cache
under the account-owned pre-commit directory rather than reopening `HOME`. A
cold cache with `HOME=/nonexistent` failed at that exact `mkdir` before the
change and installs and passes every Go-backed hook after it.

`unit-tests` hit the shared 1200s validator budget and was killed at `rc=-9`.
The suite takes 828s locally; `test_archive_validation` is 451.5s of that, and
twelve of its tests hold 81% of the module because each runs a full
link-diagnostics pass over its own variant of the corpus. That work is
per-test and does not cache away, so the budget is what changes. Raising the
shared constant would weaken the bound on every gate that has no reason to run
long, so the registry schema gained an optional per-gate `timeoutSeconds`,
only `unit-tests` declares one, and the job wall clock moved to 75 minutes
because a gate budget above its job's wall clock can never be reached. Hook
environments are cached between runs, which removes the largest single cost
the pre-commit repair introduced.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| Hosted CI run `34174869492` | 1 / FAIL | `push` on `d284c99e`; 20/22 gates PASS, `unit-tests` timeout and `pre-commit` cold-cache failure |
| Hosted CI run `34174794127` | 1 / FAIL | `pull_request` on `c7b239f0`; same two gates |
| Cold-cache reproduction of the pre-commit failure | 1 / FAIL as expected | `HOME=/nonexistent` with an empty hook cache returned the hosted `mkdir /nonexistent` error; the same command with a warm cache passed, which is why no earlier run saw it |
| Cold-cache verification after the fix | 0 / PASS | Same cold cache and unreachable `HOME`; every Go-backed hook installs and passes |
| `test_archive_validation` per-test timing | measured | 96 tests, 451.5s, top twelve hold 81%; recorded so the budget is chosen against a measurement rather than a guess |
| Hosted CI on the follow-up | NOT_RUN / DEFER | No hosted result exists for the follow-up commits; the two failures above stand as the current hosted observation |

The `unit-tests` budget and the cache change what the job costs, not what it
proves. No execution-time improvement is claimed for the cache until a hosted
run measures one.

### Second Hosted Result and the Dependency Divergence (2026-09-08)

Run `34183991155` on `3643aac6` shows both earlier repairs working and moves
the remaining failures to new causes. `branch-policy` executed for the first
time and passed; every setup step including the hook cache passed. The
`unit-tests` gate no longer times out, which is the declared budget doing its
job, and `pre-commit` returned `rc=0` with every hook passing, which is the
toolchain-cache fix doing its job.

`unit-tests` then failed one case:
`test_repository_snapshot_is_complete_and_atomic`, which asserts the archive
cutover command writes nothing to stderr. The cause is dependency identity.
CI installs the locked `jsonschema==4.26.0`, which deprecates `RefResolver`
and prints that deprecation when the shared schema evaluator imports it; the
developer machine here carries `4.10.3`, which does not. A validator writes
evidence, so noise on its stderr is a defect rather than a detail.

That class of fault cannot be seen from a local run at all, so a virtualenv
built from `.github/requirements/ci-validation.txt` was used to hold the
hosted dependency identity. It reproduced the warning and the failing case
exactly, and both clear after the evaluator uses the `referencing` registry
where the interpreter has it and keeps the resolver path where it does not.
The boundary the module exists for is unchanged and tested on both: external
schema resources are never retrieved, embedded definitions resolve, and an
invalid schema fails closed without leaking schema values. `scripts/README.md`
now records the reproduction so the next such divergence does not need to be
rediscovered.

The hosted `unit-tests` failure also named a case and nothing else, because
the bounded snippet kept only lines opening with `FAIL:`, `ERROR:` or a hook
marker and a unittest assertion opens with neither. Assertion lines now carry
through under the same byte bound and redaction.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| Hosted CI run `34183991155` | 1 / FAIL | `pull_request` on `3643aac6`; `branch-policy` PASS, 20/22 gates PASS, `unit-tests` `rc=1`, `pre-commit` `rc=0` with `descendant_cleanup` |
| CI-identity virtualenv reproduction | 1 / FAIL as expected | Locked `jsonschema==4.26.0` reproduced the deprecation and the failing case that no local interpreter here could show |
| CI-identity virtualenv after the fix | 0 / PASS | Same interpreter; `unit-tests` passes and 21/22 gates pass, the remaining one being formatter output on newly written code |
| Older interpreter after the fix | 0 / PASS | `jsonschema==4.10.3` without `referencing`; the resolver path still resolves and still refuses external resources |
| Hosted CI on these commits | NOT_RUN / DEFER | No hosted result exists for the follow-up; run `34183991155` stands as the current observation |

Two limitations remain open. `descendant_cleanup` was reported for both slow
gates on the hosted runner and for neither locally, including under the
CI-identity interpreter, so no root cause is established; the containment
boundary it guards is real, so it is left intact rather than widened against a
fault that has never been reproduced. The escaped-descendant test from the
previous section is still unrepaired for the same reason.

One repository hazard was confirmed the hard way and is now recorded in
`scripts/README.md`: formatters must run through `pre-commit`. The hook
narrows `ruff-format` to Python deliberately, and the bare command also claims
Markdown and rewrote fenced snippets inside eleven authored and archived
documents. Those edits were reverted before staging and no archived byte
changed, but the configuration comment predicting it was already there.

### Third Hosted Result, Local Main Merge, and the Trusted-Path Cause (2026-09-08)

Run `34188398622` on `b1275fa6` returned twenty of twenty-two gates and left
the same two gates failing. The dependency-identity repair worked: the case
that failed on evaluator stderr now passes that assertion and stops at the
next one in the same test, which had been masked behind it. That next
assertion was legible only because assertion lines now survive the bounded
snippet, and it named its own cause: `required secure Gitleaks executable
unavailable`.

The cause is a directory ownership contract, not a missing binary. The
workflow installs Gitleaks root-owned and non-writable, and the file itself
satisfies the strict resolver. The resolver also requires the containing
directory to be root-owned and neither group- nor other-writable, because that
write bit lets a non-root account swap the executable between resolution and
execution. A runner image may publish `/usr/local/bin` writable so that
actions can install into it without `sudo`. No local run could show this: the
developer machine here carries Gitleaks in `~/.local/bin`, which the resolver
accepts through its passwd-home branch, so the system-directory branch is
never exercised. The workflow now claims the ownership it depends on before
publishing anything into that directory, and a workflow contract test fixes
the step ordering and the mode, because nothing in the contract covered this
and the gap was therefore invisible to every local gate.

The `descendant_cleanup` status was reproduced as a mechanism, though not as
the hosted fault. A throwaway probe against the bounded runner shows a plain
child returning `completed` and a `setsid` grandchild that outlives the leader
returning `descendant_cleanup` with `rc=0`, which matches the hosted shape
exactly: `pre-commit` passed every hook and still failed the gate. The earlier
hypothesis that `VALIDATOR_CLEANUP_SECONDS` was too tight is refuted, since
that path yields `cleanup_failure` rather than `descendant_cleanup`. The
offending process is still unidentified and did not appear locally when idle
or under CPU contention, so the runner emits the identity of each escaping
descendant with the verdict. Only `comm` is read, never `cmdline`, so an
argument vector cannot carry a credential into the report, and a test fixes
that boundary. The verdict logic is unchanged.

The archive cutover assertion reports the candidates it walked with their
ownership when it refuses, so the next hosted result is conclusive whether or
not the workflow change is the correct repair.

PR #59 was merged as `0152369b` on explicit instruction with the follow-up
work accepted as a separate branch. `git diff b1275fa6 main` is empty, so the
merged content is exactly the state that passed locally. The merge required an
administrative override of the failing required check `ci-summary`; the
repository sets `enforce_admins` to false, so this used an allowance the owner
had already configured rather than a settings change, and no protection,
workflow gate or test was altered to obtain it. `main` remains red and its own
run `34190920724` returned the same twenty of twenty-two with the same two
gates, which is the predicted result rather than a new observation.

Branch protection was re-read because a review requirement was suspected of
blocking a single-maintainer repository. It does not:
`required_approving_review_count` is zero, `require_code_owner_reviews` and
`require_last_push_approval` are false, and the repository declares no
rulesets. The only required check is `ci-summary`. No review setting needs
changing and none was changed.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| Hosted CI run `34188398622` | 1 / FAIL | `pull_request` on `b1275fa6`; `branch-policy` PASS, 20/22 gates PASS, `unit-tests` `rc=1` naming the Gitleaks assertion, `pre-commit` `rc=0` with `descendant_cleanup` |
| Hosted CI run `34190920724` | 1 / FAIL | `push` on merged `main` `0152369b`; same twenty of twenty-two and the same two gates |
| Bounded-runner escape probe | expected | Plain child `completed`; `setsid` grandchild outliving the leader `descendant_cleanup` with `rc=0` |
| Local reproduction attempts for the hosted escape | NOT_REPRODUCED | Idle and two-CPU contention; no runaway process remained |
| `python3 -m unittest discover -s tests -t .` | 0 / PASS | 928 tests, `OK (skipped=4)`; measured without a pipeline so the exit status is the suite's own |
| `pre-commit run --all-files` | 1 then stable | Hooks applied Python-only formatting and a baseline rewrite; the second run applied no further change |
| `.secrets.baseline` comparison | equivalent | Same version, files, entries and audit flags; two line numbers moved by the inserted workflow step and key order normalized |
| Hosted CI on these commits | NOT_RUN / DEFER | No hosted result exists for `449dffb1`, `6bb6a7bc` or `e4cd542a` |

Three limitations remain open. The escaping descendant on the hosted runner
has no identified cause and the containment boundary it guards is real, so it
is left intact and now reports what escaped rather than being widened. The
escaped-descendant test from the earlier section is still unrepaired for the
same reason. Whether the directory ownership claim is the correct repair for
the Gitleaks resolution is unverified until a hosted run executes these
commits; the failing assertion will name the rejecting fact either way.

### Fourth Hosted Result and Naming the Escaping Call (2026-09-08)

Run `34200871694` on `55a6714e` confirms the trusted-path repair and isolates
the remaining cause. The directory ownership claim worked: `unit-tests` moved
from `rc=1` to `rc=0`, so the strict resolver now accepts the Gitleaks the
workflow publishes. Twenty gates pass and the two that fail both return
`rc=0`, meaning every validator command succeeded and only the containment
verdict remains.

The identity report answered the question it was added for. Both gates named
their escaping descendants, and every one of them is `git` with `pid == pgid`:

    escaped=54600:54600:git,54641:54641:git,54682:54682:git, ... (cap reached)

A process whose group id equals its own pid became a group leader, so git
itself detached rather than inheriting a group from a wrapper. Git detaches in
`gc --auto --detach`, `maintenance run --detach` and `fsmonitor--daemon`, and
the regular pid spacing points at sequential creation by the same workload
rather than at recycled identities. Which of those three it is stayed open, so
the report now carries the subcommand: git names its call in the second
argument, and that argument is admitted only when it is a bare lowercase
token. The forms that can carry a credential put an option in that position
first, so refusing options refuses them, and a test renders an argument vector
holding an authorization header and asserts the header does not appear.

Probing that change surfaced a sharper question than the name. An
exited-but-unreaped process has no argument vector at all, so it would have
reported as nothing to name — the same as a running process whose argument was
refused. Those two are not the same finding. A zombie is an unreaped exit
record and not work outliving the gate; a running process is. The reader now
distinguishes them, and a local comparison is suggestive: an escape that had
already exited produced `descendant_cleanup` while a live one produced
`descendant_pipe_hold`, and `descendant_cleanup` is what every hosted run has
reported. That is a lead and not a conclusion, and the verdict logic is
unchanged until a hosted result settles it.

Two local reproduction attempts for git's detached auto-gc failed, including
one with 7,002 loose objects, which is above the default threshold. A cold
`pre-commit` reproduction was attempted and abandoned: building every hook
toolchain at once exhausted memory on a workstation that also runs the local
cluster, and the kernel killed the probe. Repeating it risks the operator's
workloads for a result the next hosted run produces anyway, so it was not
retried and the scratch it left was removed.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| Hosted CI run `34200871694` | 1 / FAIL | `pull_request` on `55a6714e`; `branch-policy` PASS, 20/22 PASS, both failures `rc=0` with `descendant_cleanup`, all escapes named `git` with `pid == pgid` |
| Hosted CI run `34204101088` | observed | `push` on merged `main` `be2d41ef` after PR #60 |
| Trusted-path repair | CONFIRMED | `unit-tests` `rc=1` to `rc=0` across the two runs |
| `install -d -m 0755` on an existing directory | 0 / PASS | 0775 normalized to 0755, satisfying the resolver predicate the repair depends on |
| Escape identity probe, live process | expected | `escaped=<pid>:<pid>:git:hash-object` with `descendant_pipe_hold` |
| Escape identity probe, exited process | expected | `escaped=<pid>:<pid>:git:zombie` with `descendant_cleanup` |
| Local git detached auto-gc reproduction | NOT_REPRODUCED | Two attempts, one above the default loose-object threshold |
| Cold `pre-commit` reproduction | ABANDONED | Killed for memory pressure on a host running the local cluster; not retried |
| `python3 scripts/qa.py full` | 0 / PASS | 22 gates on the narrowed diagnostic |
| Hosted CI on this commit | NOT_RUN / DEFER | No hosted result exists for `f13fbe9e` |

The open limitation is unchanged in substance and narrower in scope: the
escaping call is `git`, the subcommand and liveness are now reportable, and no
repair is attempted until a hosted run says which call it is and whether it
was still running.

### Fifth Hosted Result: the Escape Was a Definition Defect (2026-09-08)

Run `34211376210` on `58b32427` closed the question the previous four runs
could not. Both failing gates named every escaping descendant, and all sixteen
of them across the two gates read the same way:

    escaped=10016:10016:git:zombie,10026:10026:git:zombie, ... (cap reached)
    escaped=54604:54604:git:zombie,54645:54645:git:zombie, ... (cap reached)

Not one was running. Every escape was a `git` that had already exited and had
not yet been reaped.

That makes the fault a definition defect rather than an environment problem.
An escape is work that can outlive the gate that owns it. A terminated entry
runs no code, holds nothing beyond its slot in the process table, and can
never run again; it is waiting for the reap that the cleanup immediately
following performs. Counting it failed a gate for work that does not exist,
which is exactly why `pre-commit` failed while returning `rc=0` with every
hook passing, across four consecutive runs.

Exited states are now excluded from the escape determination and nothing else
changes. The boundary is not widened: a live descendant holding a foreign
process group still fails the gate, and now names itself while doing so. A
test reproduces the hosted shape locally for the first time -- an exited
`setsid` descendant produced `descendant_cleanup` before the change and
`completed` after -- and the neighbouring test keeps a live escape failing.

The narrowing that produced this answer is worth recording as method. The
report first carried the status alone, which named nothing. It then carried
the process identity, which showed `git` with `pid == pgid` and established
that git had detached rather than inherited a group. It then carried the
subcommand and the liveness, and the liveness -- added because a zombie has no
argument vector and would otherwise have reported as nothing to name -- was
the field that answered the question. Three of the four hosted runs spent on
this gate produced no diagnosis because the evidence emitted was thinner than
the fault.

| Command / bounded observation | Exit / result | Input and evidence |
| --- | --- | --- |
| Hosted CI run `34211376210` | 1 / FAIL | `pull_request` on `58b32427`; 20/22 PASS, both failures `rc=0`, all sixteen escapes `git:zombie` |
| Local reproduction of the hosted shape | 1 then 0 | An exited `setsid` descendant produced `descendant_cleanup`; `completed` after the change |
| Live-escape boundary after the change | unchanged | A live `setsid` descendant still fails and reports `git:hash-object` |
| Plain child control | 0 / PASS | `completed` before and after |
| `python3 -m unittest tests.test_run_validation_lane` | 0 / PASS | 70 tests |
| `pre-commit run --all-files` | 0 / PASS | No hook applied a change |
| `python3 scripts/qa.py full` | 0 / PASS | 22 gates |
| Hosted CI on this commit | NOT_RUN / DEFER | No hosted result exists for `0bcde241` |

Two limitations from earlier sections close here and one stays open. The
escaping descendant now has an established cause and a repair. Whether the
earlier `test_escaped_devnull_descendant_is_killed_and_not_reported_completed`
flake shares that cause is untested; that test uses a live descendant, so the
change does not affect its assertion and it remains unrepaired.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done: local static migration | All 53 source dispositions, unchanged permission metadata, direct governance PASS and old-root absence |
| [WORK-002](../plan.md#work-breakdown) | Done: local QA | Bounded-input/process and Shell-route regressions; full 19/19 and quick 11/11 PASS; full/CI registry parity |
| [WORK-003](../plan.md#work-breakdown) | Done: document reconciliation | Profile/link/lifecycle PASS, 32 template dispositions, current successor proof and classified historical evidence |
| [WORK-004](../plan.md#work-breakdown) | In progress: external evidence DEFER | Static workflow and final local QA PASS; the hosted failure this package introduced is reproduced and repaired with a CI-shape run; native runtime and hosted CI on the repaired commit NOT_RUN; no remote or live authority |
| [WORK-005](../plan.md#work-breakdown) | In progress | Approved follow-up intake; implementation evidence pending |
| [WORK-006](../plan.md#work-breakdown) | In progress | Approved follow-up intake; implementation evidence pending |
| [WORK-007](../plan.md#work-breakdown) | In progress | Approved follow-up intake; implementation evidence pending |
| [WORK-008](../plan.md#work-breakdown) | In progress | Approved follow-up intake; implementation evidence pending |
| [WORK-009](../plan.md#work-breakdown) | In progress | Approved follow-up intake; implementation evidence pending |
