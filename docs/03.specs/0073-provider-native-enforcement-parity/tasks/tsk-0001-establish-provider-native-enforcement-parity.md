---
title: "Establish Provider Native Enforcement Parity"
version: "1.5.1"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0073-TSK-0001"
---

# Task: Establish Provider Native Enforcement Parity

## Overview

Execute SPEC-0073-PLAN-0001 as fourteen ordered work packages, each delivered
as one logical commit gated by its exact index snapshot, with the full profile
run once on the final tree before handoff. This record owns execution results,
per-lane evidence, and the limits that remain unobserved.

Execution is under way. WORK-006 delivered the model alignment that WORK-008
and WORK-009 had planned separately, because a binding validator cannot land
before the values it validates; WORK-009 now carries only the permission mode.

## Inputs

- [SPEC-0073](../spec.md)
- [SPEC-0073-PLAN-0001](../plan.md)
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
- [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [ADR-0035](../../../02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md)
- [SPEC-0072](../../0072-agent-governance-and-quality-gate-consolidation/spec.md)
- Baseline commit `a57887cbf8d34eed248cb33438073635380966e3` on branch
  `codex/governance-follow-up`; local `main` and `origin/main` both at
  `4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`
- Client identity observed 2026-09-06: `claude 2.1.261`, `codex-cli 0.140.0`,
  `python 3.12.3`, `pre-commit 4.5.1`

## Task Table

| ID                                    | Upstream criterion | Work item                                                                       | Owner    | Status | Result       | Evidence                                                   |
| ------------------------------------- | ------------------ | ------------------------------------------------------------------------------- | -------- | ------ | ------------ | ---------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-PNP-001 | Record the decision lineage for the current governance topology | platform | Done | ADR-0034 superseded with a reciprocal successor row; ADR-0035 accepted; the index, AD-0006 and REQ-0003 name the current owner | Commit `7bfbf1dd`; staged profile, six gates |
| [WORK-002](../plan.md#work-breakdown) | VAL-PNP-009 | Remove retired-provider and retired-path residue from tracked configuration | platform | Done | Dead pre-commit exclusion, two removed-provider globs, one deleted-test index row and one contradicted stage claim removed | Commit `ce0adb53`; staged profile, six gates |
| [WORK-003](../plan.md#work-breakdown) | VAL-PNP-005 | Make the GitHub Actions security validator reachable from a supported profile | platform | Done | Gate registered on the all-files and CI lanes; its first run found a one-day artifact retention against the seven-day contract | Commit `1f6420ee`; reachability test RED then GREEN |
| [WORK-004](../plan.md#work-breakdown) | VAL-PNP-006 | Reduce duplicated rule implementations and profile membership to one owner | platform | Done | Duplicate Vault and ESO heredoc removed, 441 to 306 lines, both gates still passing; two reported duplications kept as distinct rules | Commit `41648686`; staged profile, seven gates |
| [WORK-005](../plan.md#work-breakdown) | VAL-PNP-007 | Set the commit and handoff evidence proportion in Git policy | platform | Done | The staged profile gates a logical commit; the full profile gates branch finish and handoff | Commit `43711f02`; staged profile, six gates |
| [WORK-006](../plan.md#work-breakdown) | VAL-PNP-003 | Add the per-provider capability-to-model binding to the registry and schema | platform | Done | Binding declared for both providers; twenty-three of twenty-four projections realigned; drift now fails on both sides | Binding tests RED then GREEN; governance validator |
| [WORK-007](../plan.md#work-breakdown) | VAL-PNP-002 | Declare a native execution scope for every Codex role and widen the parity rule | platform | Done | Each permission class binds one Codex sandbox scope; twelve projections carry it and widening or dropping it fails closed | Commit `edf960a3`; scope tests RED then GREEN |
| [WORK-008](../plan.md#work-breakdown) | VAL-PNP-003 | Align every Codex role model with the observed client catalog | platform | Done | Delivered inside WORK-006; the installed client catalog listed only `gpt-5.5`, `gpt-5.4-mini` and `gpt-5.3-codex-spark`, so eleven of twelve prior values named absent models | Governance validator; catalog observed 2026-09-06 |
| [WORK-009](../plan.md#work-breakdown) | VAL-PNP-002 | Align every Claude role model and permission mode with the registry binding | platform | Done | Models delivered inside WORK-006. The `tools` allowlist now resolves through the registry's `permission_scopes` like the Codex `sandbox_mode` does, and the one coded role exception became a declared `native_scope_override`, closing C-PNP-001 on the Claude side. `permissionMode` stays unapplied: `tools` is the enforced structured scope, and the subagent effect of `permissionMode` was not observed on this client | Twelve projections reproduced from the declaration; narrowing the registry scope fails closed. `permissionMode` remains `DEFER` |
| [WORK-010](../plan.md#work-breakdown) | VAL-PNP-004 | Extend the pre-action guard to the shell tool class and name the residual class | platform | Done | Guard matcher covers the shell tool; redirect, tee and in-place sed targets are reported; out-of-repo, read-only and unparsed commands stay silent and exit zero | Commit `3093e158`; five new guard cases |
| [WORK-011](../plan.md#work-breakdown) | VAL-PNP-008 | Correct provider notes to describe native capability against a named client | platform | Done | Capability statements name the client they were observed against; the Codex hook denial is replaced by a supported-but-not-adopted statement | Commit `5c017dde`; observed `claude 2.1.261` and `codex-cli 0.140.0` |
| [WORK-012](../plan.md#work-breakdown) | VAL-PNP-007 | Add the untrusted input, cost and throughput, and loop termination boundaries | platform | Done | Untrusted input, cost and throughput, and loop termination boundaries added at their policy owners | Commit `724719fb`; profile and link validation |
| [WORK-013](../plan.md#work-breakdown) | VAL-PNP-010 | Reconcile Stage 90 research baseline rows with the current tree | platform | Done | Six baselines framed as dated observation with current owners named; two present-tense column headers corrected; one duplicated router link removed | Commit `de1f7858`; path sweep and staged profile |
| [WORK-014](../plan.md#work-breakdown) | VAL-PNP-004 | Mirror the pre-action guard as a Codex native hook after observing the payload | platform | Done | The gating observation now exists: `codex-cli 0.153.4` documents `<repo>/.codex/hooks.json`, the `PreToolUse` event, the `command` handler, and `tool_name`/`tool_input`/`tool_input.command`. The guard is registered on `Bash\|apply_patch` and the frozen Claude hook literal is replaced by one property contract both providers are judged under | `tests.test_agent_governance` 35 OK, `tests.test_k8s_pre_edit_hook` 35 OK; native event delivery stays `DEFER` |
| [WORK-015](../plan.md#work-breakdown) | VAL-PNP-009 | Route current documents to sealed evidence through the archive index | platform | Done | The retention commit removed the navigational exemption for Migration ledgers; four current documents still linked one directly and the index reached neither ledger they cite. Index navigation added, four links rerouted, seven terminal Task records left untouched | `archive-cutover` PASS, records=25; `tests.test_archive_cutover` 37 cases OK |
| [WORK-016](../plan.md#work-breakdown) | VAL-PNP-007 | Carry the snapshot and approval boundary across a cross-provider handoff | platform | Done | Handoff evidence now records branch, HEAD, and divergence base, and the approval boundary in force, so a resuming provider learns which state a passing record described and which authorizations were already spent. Memory policy names the domain layer and routes it to its operating or reference owner | Commit `88fae58e`; staged profile, six gates |
| [WORK-017](../plan.md#work-breakdown) | VAL-PNP-005 | Give the evaluation boundary a case set and an execution path | platform | Done | `evals/` held only a README, so role behavior had no evidence path. Three cases, one per permission class, are graded on groundedness, authority, boundary, and handoff, every criterion derived from the role registry. Building the cases found a false positive in the boundary criterion and it was narrowed | Commits `40acfe46`, `6de18963`, `a8049811`; `tests.test_agent_evaluations` 12 OK; gate on all four profiles as `agent-evaluation-cases` |
| [WORK-018](../plan.md#work-breakdown) | VAL-PNP-009 | Expose the QA entry points as project editor tasks | platform | Done | `.vscode/tasks.json` ran the existing entry points and added no runner. The `.vscode/` ignore pattern was directory-level, which stops Git descending, so the tracked `!.vscode/extensions.json` exception below it had never worked. The workspace later stopped using VS Code, so the file was removed; the directory-level ignore that remains keeps any replacement untracked, and the QA entry points are unchanged and are invoked from the shell | Commit `66d2c26c`; affected-surface contract 1036 paths, uncovered=0 |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/README.md`, `.agents/governance/`,
  `.agents/roles/registry.json`, `.agents/roles/registry.schema.json`,
  `.agents/workflows/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.claude/agents/`, `.claude/settings.json`, `.claude/hooks/`,
  `.claude/provider.md`, `.claude/README.md`, `.codex/agents/`,
  `.codex/provider.md`, `.codex/README.md`, `.codex/hooks.json`,
  `.github/labeler.yml`, `.github/workflows/governance-audit-snapshot.yml`,
  `.gitignore`, `.pre-commit-config.yaml`, `.vscode/`, `README.md`,
  `docs/02.architecture/decisions/`, `docs/02.architecture/descriptions/`,
  `docs/03.specs/0073-provider-native-enforcement-parity/`,
  `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks/`
  (current records only), `docs/98.archive/README.md`,
  `docs/03.specs/README.md`, `docs/90.references/research/`,
  `docs/99.templates/registry.json`, `docs/99.templates/templates/runtime/`,
  `evals/`, `scripts/README.md`, `scripts/run-agent-evaluations.py`,
  `scripts/validate-agent-governance.py`, `scripts/validation/`,
  `infrastructure/tests/verify-contracts-static.sh`, `tests/`, and the single
  failing line of a record this package does not own when a gate rejects that
  line, recorded with the gate that forced it
- **Forbidden Paths**: the user's staged index and every path it touches,
  `.claude/settings.local.json`, `.claude/*.local.md`, `_workspace/` contents,
  `policy/`, `gitops/`, `infrastructure/` outside the named contract script,
  `secrets/`, sealed record bodies under `docs/98.archive/`
- **Approval Required**: commit authorization per logical package; separate
  authorization for push, pull-request creation, merge, branch cleanup, and any
  hosted or provider-authenticated execution. The operator approved local
  integration into `main` and cleanup of this development branch after the
  final handoff gate passed. Neither was executed: this environment's command
  guard refuses `git merge`, so the integration and the branch deletion that
  depends on it are handed to the operator with the exact commands. Push,
  pull-request creation, publication, and any hosted or provider-authenticated
  execution were not approved and were not performed
- **Static Validation**: `python3 -m unittest` for the focused modules,
  `python3 scripts/validate-agent-governance.py --root .`,
  `python3 scripts/qa.py staged` per package, `python3 scripts/qa.py full` once
  before handoff, `git diff --check` and `git diff --cached --check`
- **Live Validation**: `DEFER` — no cluster, Argo CD, Vault, cloud, remote Git,
  or hosted CI operation is authorized by this Task
- **Secret / Vault Handling**: no credential, token, authentication file,
  environment dump, plaintext secret, shell history, or provider transcript is
  read, printed, or recorded; validator failure messages name paths and
  expected values only
- **Rollback Plan**: `git revert` of the owning package commit; a corrective
  change is a new forward commit, never a history rewrite
- **Evidence Location**: this record

## Verification Summary

Every work package landed as a logical commit, each gated by the staged
profile against its exact index. WORK-009 and WORK-014 both reopened after
their gating conditions changed. WORK-014 completed after its gating observation arrived:
the installed Codex client moved from `0.140.0` to `0.153.4` and its published
hook contract names the payload shape the guard already reads.

**Snapshot.** Branch `codex/governance-follow-up`; divergence base
`4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`, which is also local and
`origin/main`. Client identity re-observed 2026-09-06 on the later session:
`claude 2.1.263`, `codex-cli 0.153.4`, `python 3.12.3`, `pre-commit 4.5.1`.
Both clients moved during execution, which is what reopened WORK-014.

**Repository-static lanes.** Every commit passed `python3 scripts/qa.py staged`
on its own index. The first handoff `python3 scripts/qa.py full` selected
twenty gates over 1026 paths and returned twenty `PASS` after the dispositions
below. Its first run returned seventeen `PASS` and three `FAIL`.

- `archive-cutover` failed `ARCHIVE-DIRECT-CURRENT-LINK` on `.agents/README.md`
  and three `blocked` SPEC-0062 Task records that linked a Migration ledger
  directly, and `unit-tests` failed three `tests/test_archive_cutover.py` cases
  from the same cause. The rule that made those links illegal arrived with the
  Spec 0052 retention commit, which removed the navigational exemption for
  Migration ledgers; `archive-cutover` runs only on the all-files and CI lanes,
  so no staged run could have selected it. WORK-015 repaired both: the archive
  index now reaches MIG-0004 and MIG-0009, the four current documents cite them
  through the index, and the seven `done` SPEC-0062 records stay untouched
  because a terminal record is exempt from the rule and must not be rewritten.
- `pre-commit` reported that `ruff format` rewrote three test files this change
  added. The formatter output was reviewed and committed explicitly.

All three are resolved; that rerun over its final tree passed every gate.

The second handoff `full` run, over the tree the late packages produced,
returned eighteen `PASS` and three `FAIL`, and both underlying defects belong
to work the staged lane structurally cannot see.

- `pre-commit` reported one `ruff-check` defect and four files `ruff-format`
  would rewrite. The defect is real: a groundedness note carried an f-string
  with no placeholder and named no path, so it could not be acted on, while the
  note on the following line already names the citation it rejects. The note
  now reports the citation and the remaining hunks are the pinned formatter's
  own output.
- `unit-tests` failed two cases. `test_full_and_ci_keep_the_same_unique_gate_set`
  is a literal gate inventory that a twenty-first gate legitimately changed.
  `test_transition_wrappers_and_registry_aliases_are_absent` is a retired-alias
  ban, and WORK-017 had registered its gate under the retired identifier
  `agent-evaluations`. That surface was retired by `fa3d5a9d`, which gave each
  validation rule one owner; the retired rule read
  `contracts/agent-evaluations.json` and its twelve declarative suites, so the
  identifier would have returned carrying a different rule. The reason for the
  retirement still holds, so the ban stays and the gate is renamed
  `agent-evaluation-cases`.

Both are resolved. The final handoff run of `python3 scripts/qa.py full` over
the settled clean tree at `8e9f4a51` returned twenty-one `PASS` and no `FAIL`,
`SKIP`, or `DEFER` in the repository-static lane, and exited zero. That run is
the branch-finish evidence; no gate result was downgraded to reach it.

**Write-boundary audit.** Every path this package changed was compared against
the declared boundary after execution. Seventeen of eighty-nine sat outside the
`Allowed Paths` list as it then read, and every one of them belongs to work the
Plan authorized: the loop-termination package writes `.agents/workflows/`, the
decision-lineage package writes `AD-0006`, the gate-registration package writes
the audit workflow, the archive routing package writes `.agents/README.md`, and
the two late packages write `evals/`, `.vscode/`, `.gitignore`, and the runner
and index row under `scripts/`. The list was never extended when those packages
were added, so the declared boundary trailed the authorized one. It is
reconciled above rather than backdated: the writes happened before the list
named them.

No forbidden path was written. `_workspace/`, `policy/`, `gitops/`, `secrets/`,
`.claude/settings.local.json`, `.claude/*.local.md`, `infrastructure/` outside
the one named contract script, and every sealed record body under
`docs/98.archive/completed/` and `docs/98.archive/migrations/` are unchanged
across this package's range. One record this package does not own,
`SPEC-0054`'s `tsk-0013`, changed by exactly one line: the repository-quality
gate rejected an absolute local checkout path, and the correction is limited to
the line the gate named. The user's index and both stashes are untouched.

**Document reconciliation.** The Specification and Plan were audited against
what was built and corrected in commit `5911a2ee`, then brought under
VAL-PNP-010 in a follow-up: the Overview had described the pre-change tree in
the present tense, which a current document may not do once its work has
landed. The conditions this package addressed are now stated as observed at
drafting, and what holds instead is stated separately. The Task keeps
`done` on the operator's integration approval; before that approval it stayed
`in-progress`, because a terminal record must not be rewritten and the branch
was neither merged nor handed off.

**Negative evidence recorded.** A drifting model on either provider, a widened
or missing Codex sandbox scope, a validator with no profile membership, and a
Codex projection carrying an unknown key all fail closed, each demonstrated
before its fix and shown passing after it.

**Lanes that produced no evidence.** Native discovery, native enforcement,
model resolution, authenticated provider operation, hosted CI execution, and
live infrastructure behavior are `DEFER`: no fresh provider session was run, no
push was made, and no cluster was inspected. No editor-extension behavior was
observed either, because neither provider extension is installed here.

**Review disposition.** Self-reviewed against the diff of each commit. No
independent reviewer has examined this work.

**Rollback.** Each package is one commit; `git revert` of that commit reverses
it. No history was rewritten and no branch was pushed, merged, or deleted.

**Residual risk.** The capability binding, both providers' scope
declarations, and both hook registrations are tracked configuration whose
runtime effect is unobserved. The write-path guard still cannot see a program
that opens files itself. A rule that only the all-files and CI lanes select can
be broken by a staged-only change and stay invisible until handoff, which is
how WORK-015's defect reached a commit and how both second-run defects did.

Two conditions widened that window here. `pre-commit` and `unit-tests` are
declared on the all-files and CI lanes only, so no per-commit `staged` gate
selects the formatter or the suite. And this clone sets
`core.hooksPath` to a directory outside the repository, which is where Git
reads hooks from when it is set, so the pre-commit framework's installed
`.git/hooks/pre-commit` never ran on any commit in this branch. The setting is
the operator's and was left as found; the effect is that the commit-time
formatter lane produced no evidence and the handoff gate was the first check
to see these files.

Two limits belong to the work added late. The evaluation grader checks the
shape of a response, not the truth of its content: a case may cite a path that
exists and still describe it wrongly, which is how a synthetic response came to
assert a stale sentence that the approval boundary does not contain. Every
case carries a `synthetic` response, so the gate proves the harness and its
criteria work and proves nothing about any agent. And the governance
validator's Codex reasoning-effort allowlist is narrower than the installed
client's — the client accepts `max` and `ultra`, the validator does not. It
fails closed and no role uses either value, so it was left as observed rather
than widened without a driver.

**Next owner.** platform, for any authorized native observation. Every work
package has landed. Integration into local `main` is approved and pending: the
operator authorized it, and `git merge` is refused by this environment's
command guard, so the merge is the operator's to run. The branch is retained
until it succeeds, and no cleanup was performed. What remains unobserved is runtime: native discovery,
event delivery, model resolution, and whether `permissionMode` changes a
subagent's authority at all. A registered hook and a declared scope are
configuration, not enforcement evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item                 | Result                                                    | Evidence                                                          |
| ------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Recorded the decision lineage without rewriting either decision body | Commit `7bfbf1dd`; document lifecycle and link validation |
| [WORK-002](../plan.md#work-breakdown) | Removed five tracked entries that could never match or hold true | Commit `ce0adb53`; repository quality and filesystem sweep |
| [WORK-003](../plan.md#work-breakdown) | Registered the orphan gate and fixed the violation its first run found | Commit `1f6420ee`; reachability test and profile listing |
| [WORK-004](../plan.md#work-breakdown) | Removed one duplicate implementation; kept three distinct rules | Commit `41648686`; both gates re-run after removal |
| [WORK-005](../plan.md#work-breakdown) | Stated the commit and handoff evidence proportion | Commit `43711f02`; quality policy cross-reference |
| [WORK-006](../plan.md#work-breakdown) | Capability tier now determines the native model on both providers | Binding tests and governance validator negative cases |
| [WORK-007](../plan.md#work-breakdown) | Codex roles now carry an enforced structured scope | Commit `edf960a3`; widening and removal both fail closed |
| [WORK-008](../plan.md#work-breakdown) | Codex models realigned to the observed client catalog | Governance validator; recorded catalog identity |
| [WORK-009](../plan.md#work-breakdown) | Claude scope moved from validator code into the registry; `permissionMode` still deferred | Registry scope negative case; declared override case |
| [WORK-010](../plan.md#work-breakdown) | Shell writes are observed advisorily; the residual class is named | Commit `3093e158`; approval boundary text |
| [WORK-011](../plan.md#work-breakdown) | Native capability claims carry a client identity | Commit `5c017dde` |
| [WORK-012](../plan.md#work-breakdown) | Three missing boundaries added at their owners | Commit `724719fb` |
| [WORK-013](../plan.md#work-breakdown) | Stage 90 baselines read as dated observation | Commit `de1f7858` |
| [WORK-014](../plan.md#work-breakdown) | Codex guard registered under a contract shared with Claude; the dead guard environment variable removed | Governance validator; three Codex-payload guard cases |
| [WORK-015](../plan.md#work-breakdown) | Archive cutover and its unit cases recovered without editing a terminal record | `archive-cutover` PASS; 37 archive cutover cases OK |
| [WORK-016](../plan.md#work-breakdown) | A handoff now names the snapshot it describes and the boundary it ran under | Document lifecycle and link validation |
| [WORK-017](../plan.md#work-breakdown) | The evaluation boundary owns cases, a runner, and a registered gate under a name no retired rule held | Twelve grading cases; affected-surface contract at 21 validators; retired-alias ban intact |
| [WORK-018](../plan.md#work-breakdown) | QA entry points reachable from the editor; a dead ignore exception repaired | Affected-surface contract; reviewed ignore semantics |
