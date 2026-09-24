---
title: "Close the Stage 03 Backlog"
version: "0.4.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0084-TSK-0001"
---

# Task: Close the Stage 03 Backlog

## Overview

This Task records the round: the survey each disposition starts from, the two
contract gaps it closes, the edges it takes, the retentions, the repairs those
retentions prove necessary, and the closure. It records observed results only
and never promotes a repository-static result to hosted, provider-runtime, or
live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: on 2026-09-16 the request owner approved this round with blanket
  authorization for individual completion, move, and deletion, and chose the
  registry gap-fills, the frontmatter reader consolidation, and the retention
  moves over the narrower alternatives offered.
- The survey reads the registry's own domain, profile, unit, mode, and class
  definitions, so a candidate here is a candidate the gates recognize.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SBC-001 | Record the survey of every remaining Stage 03 package | platform | Done | Sixteen packages recorded below with anchor state, non-terminal members, and consumers | This Task |
| WORK-002 | VAL-SBC-002 | Close the two registry gaps as gap-fills | platform | Done | Two profiles and one domain changed, 14 added and 4 removed lines, no existing document newly in violation | Recorded below |
| WORK-003 | VAL-SBC-003 | Close SPEC-0071, SPEC-0078, SPEC-0062, and SPEC-0054 | platform | Done | SPEC-0071, SPEC-0078, SPEC-0062, and SPEC-0054 are `done`; SPEC-0078 took both declared edges | Lifecycle gate PASS strict |
| WORK-004 | VAL-SBC-004 | Withdraw SPEC-0048 and SPEC-0051 and cancel their Tasks | platform | Done | Both are `withdrawn` over the new `draft` to `withdrawn` edge; twelve Tasks cancelled through `queued` to `in-progress` to `cancelled` | Lifecycle gate PASS strict |
| WORK-005 | VAL-SBC-005 | Repair SPEC-0006's stale sibling path and close it | platform | Done | The stale sibling path in SPEC-0006's body was repaired before the move, and the package closed `done` | Link gate PASS; the path was a code span the gate never resolved |
| WORK-006 | VAL-SBC-006 | Retain SPEC-0068 and SPEC-0070 in `superseded/` | platform | Done | Both carry `superseded_by: "SPEC-0072"` and are retained in `superseded/`, the first spec packages in that class | Archive gates PASS; catalog rows name envelope `b4a1db91` |
| WORK-007 | VAL-SBC-007 | Record the dated disposition note of every package that stays | platform | Done | SPEC-0008, SPEC-0047, SPEC-0049, SPEC-0050 and SPEC-0072 carry dated notes; SPEC-0072's Task moved `in-progress` to `blocked` | This Task and the stage index |
| WORK-008 | VAL-SBC-008 | Resolve the duplicated frontmatter readers to one owner | platform | Done | `validate-links-and-owners.py` lost its private `_frontmatter` and reads `frontmatter_mapping` from the single owner | Gate stdout sha256 `e1925925` identical before and after; 87 archive contract tests; 182 tests over four modules |
| WORK-009 | VAL-SBC-009 | Retain every package that reached `done` in `completed/` | platform | Partial | Seven of nine units retained. SPEC-0054 and SPEC-0062 reached `done` but stay at their Stage 03 paths, recorded as named deferrals below | Link, lifecycle and archive gates PASS over the seven |
| WORK-010 | VAL-SBC-010 | Repair the consumers the retention proves wrong | platform | Done | REQ-0003, the stage index, `tests/test_archive_citation_decision.py` and SPEC-0083's self-reference were repaired; no pin was lowered | Full QA and the unit-test suite |
| WORK-011 | VAL-SBC-011 | Close SPEC-0077 with its blocked criteria recorded as deferrals | platform | Done | SPEC-0077 is `done` with two authority-blocked criteria recorded as deferrals with named owners | Lifecycle gate and this Task |
| WORK-012 | VAL-SBC-012 | Close this package with its results | platform | Done | This package closes with the results recorded here, including the two deferred retentions | Staged QA PASS; full QA 23 PASS, recorded below |

## Approval and Safety Boundaries

- **Allowed Paths**: the sixteen Stage 03 packages this round disposes of, their
  consumers in documents, in `scripts/` and in `tests/`, the `sdlc/spec` profile
  and the `spec-plan` domain in `docs/99.templates/registry.json`, the Stage 98
  index, the Stage 03 index, `.gitleaks.toml`, and this package.
- **Forbidden Paths**: frozen records, sealed ledgers, and retained bodies under
  `docs/98.archive/`; every registry key, profile, domain, state, and edge other
  than the two named; `gitops/`, `infrastructure/`, `policy/`, `secrets/`,
  `.github/`.
- **Approval Required**: the disposition of each package in this round, granted
  on 2026-09-16. Push, pull request, and merge are not approved.
- **Static Validation**: focused checks per work item, `python3 scripts/qa.py
  staged` per logical commit, and one `python3 scripts/qa.py full` on the final
  tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed. The `.gitleaks.toml` change moves one path-exact
  allowlist entry and reads no secret.
- **Rollback Plan**: Revert the commits before integration; after integration a
  retained unit is frozen and only a forward decision changes it.
- **Evidence Location**: This Task record.

### Survey

Read on 2026-09-16 at `e062290e`, the tree SPEC-0083 closed on. Every package
below is one SPEC-0083 surveyed and returned. The disposition column states the
terminal state this round takes it to, and the reason column states the observed
fact that decides it.

| Package | Anchor state | Non-terminal members | Disposition | Reason |
| --- | --- | --- | --- | --- |
| SPEC-0006 | active | none | `done` | Fifty-eight of its fifty-nine criteria name artifacts that exist; the residue is operator-owned runtime, which `completed/` admits. Its own text scopes it to a dated 2026-05-24 snapshot, and the gate it depended on was retired by SPEC-0072 |
| SPEC-0008 | active | none | stays `active` | It owns the current platform contract. Six accepted ADRs name it as their Spec, REQ-0004 traces to it, four operations documents carry it in a RACI row, and three test files pin its path. No successor exists |
| SPEC-0047 | active | five queued Tasks | stays `active` | Its CSASR-004 is obsolete by SPEC-0078's record, and its stash obligation is unowned: no validator covers the stash its Plan names. The obligation outlives the package |
| SPEC-0048 | draft | six queued Tasks | `withdrawn` | Its own dated note of 2026-09-14 recommends withdrawal and names the missing edge as the only blocker. GRCE-002 and 005 are met by CODEOWNERS, the labeler and the surface document, 004 by SPEC-0072 and SPEC-0073, 007 by the recorded main protection. The residual contract location `.agents/contracts/` does not exist |
| SPEC-0049 | draft | seven queued Tasks | stays `draft` | Genuinely unowned work: no `kustomize`, `kubeconform`, `kubeval` or `helm template` invocation exists anywhere in the repository, so PVSE-002 and 003 have no substitute. Its contract location must be re-planned before activation |
| SPEC-0050 | draft | seven queued Tasks | stays `draft` | The validation registry declares zero Terraform and zero Bicep validators, while two example READMEs publish commands no gate owns. The same re-planning applies |
| SPEC-0051 | draft | six queued Tasks | `withdrawn` | Its own dated note of 2026-09-14 recommends withdrawal: it requires a local-only fast-forward from a worktree that no longer exists while CI enforces pull requests into `main`, and it depends on a retired ledger |
| SPEC-0054 | active | tsk-0009 queued, tsk-0013 in-progress, tsk-0014 queued | `done` | Eleven of fourteen Tasks carry committed evidence. tsk-0009 is written against record forms ADR-0039 froze and names a `tombstones/` directory that does not exist; tsk-0013 holds accepted evidence with its residual scope reassigned; tsk-0014 is the closure record and its branch-completion half is overtaken |
| SPEC-0062 | active | three blocked Tasks, tsk-0011 in-progress | `done` | Seven Tasks are done and the 2026-08-29 closeout replaced the unfinished execution. The three blocked Tasks wait on an approved destructive replay and an execution environment the record itself states is absent; tsk-0011 states its work is complete and only the `done` edge remains |
| SPEC-0068 | superseded | none | retained in `superseded/` | Its body names SPEC-0072 as successor; the frontmatter could not carry it because the `sdlc/spec` profile declares an empty optional key list. Twenty-four sibling profiles declare `superseded_by` optional and no profile forbids it |
| SPEC-0070 | superseded | none | retained in `superseded/` | The same gap and the same successor. Its one live residue is three `.gitignore` lines that name a provider the roster no longer carries |
| SPEC-0071 | active | tsk-0001 in-progress | `done` | All thirteen criteria carry recorded evidence, and both its Spec and its Plan already state that closing to `done` is the next reviewed change |
| SPEC-0072 | active | tsk-0001 in-progress | stays `active` | Its native-runtime criteria need an operator observation the worker cannot perform. Closing would promote a repository-static result to runtime evidence, which its own record forbids. Its Task moves to `blocked`, which states that honestly |
| SPEC-0077 | active | tsk-0001 in-progress | `done` after WORK-005 | Five of eight criteria are met. Two gaps are authority-blocked: retiring two skills needs a new sealed migration, and routing `evals` needs a Stage 99 route. The third, resolving the duplicated frontmatter readers, has no blocker and is executed in this round |
| SPEC-0078 | draft | tsk-0001 queued | `done` | All six criteria carry evidence and all four of its commits are in history. Its own Task states that activation and closure are the first reviewed change after the merge that landed it, and that merge has happened |
| SPEC-0083 | done | none | retained in `completed/` | It closed its own round on this tree. Every member is terminal, so it is a finished unit awaiting disposition exactly as ADR-0039 describes |

Three facts in the table were read directly rather than taken from the survey
that reported them. The `sdlc/spec` profile declares `required` with eight keys,
`optional` empty and `forbidden` empty; `superseded_by` is optional in
twenty-four profiles, required in none and forbidden in none. The `spec-plan`
domain declares `draft` to `active`, `active` to `done`, `active` to
`superseded` and `active` to `withdrawn`, while the sibling
`requirement-architecture` domain declares `draft` to `withdrawn`.
`docs/98.archive/` holds `completed/`, `migrations/` and `superseded/` and no
`retired/`, so a withdrawn package stays at its Stage 03 path in this round.

### The two registry gap-fills

Applied on 2026-09-16. The change is fourteen added and four removed lines in
`docs/99.templates/registry.json`, and it was proved by comparing the parsed
registry before and after rather than by reading the diff alone.

| Gap | Before | After | Scope proof |
| --- | --- | --- | --- |
| A superseded spec cannot name its successor | `sdlc/spec` declared `optional` empty, so the allowed key set was exactly the eight required keys | `superseded_by` is optional and last in `order` | The only profiles that differ from their previous form are `sdlc/spec` and its template pair; `required` and `forbidden` are unchanged |
| A draft spec or plan cannot be withdrawn | `spec-plan` declared `draft` to `active`, `active` to `done`, `active` to `superseded`, and `active` to `withdrawn` | `draft` to `withdrawn` is declared, grouped with the other `draft` edge | The only domain that differs is `spec-plan`; its `states` are unchanged and the `task` domain is unchanged, so `queued` still reaches no terminal state directly |

Neither is a relaxation. The allowed key set is computed as required plus
optional, so widening `optional` admits one key and exempts no document from any
assertion; `superseded_by` is now optional in twenty-five profiles, required in
none, and forbidden in none. The `withdrawn` state already existed in the
`spec-plan` domain and only its approach was missing, which the sibling
`requirement-architecture` domain has always declared.

The template pair was not optional. `_assert_template_source_parity` in
`scripts/validate-document-contract-registry.py` requires every template profile
to inherit its source profile's class, frontmatter, headings, and body contract
exactly, exempting only `artifact_id` and `layer`. Changing `sdlc/spec` alone
split that pair, so `common/template-sdlc-spec` carries the same key. The
template document itself gains nothing, because the key is optional.

Observed after the change, on the same index: `document-contract-registry` PASS
over 800 paths with no uncovered or ambiguous path, `markdown-profiles` PASS
with no violation, `document-lifecycle` PASS in strict mode, `links-and-owners`
PASS over the whole corpus, and `python3 scripts/run-archive-contract-tests.py`
PASS with five modules and 87 tests. No existing document became a violation,
which is the evidence that distinguishes a gap-fill from a relaxation.

### Consumers that must move before a retention

| Consumer | Pins | Repair |
| --- | --- | --- |
| `tests/test_archive_validation.py` | SPEC-0054 as its stand-in for a present current document | Repoint to a package that stays |
| `tests/test_archive_cutover.py` | SPEC-0054 as its stand-in for an active package | Repoint to a package that stays |
| `.gitleaks.toml` and `tests/test_qa_runner.py` | a path-exact allowlist entry inside SPEC-0062's Plan | Move the entry with the retention |
| `.codex/provider.md` | SPEC-0072's Task path | No move; SPEC-0072 stays active |
| `docs/01.requirements/0003-workspace-agent-governance-platform.md` | SPEC-0006, SPEC-0071, SPEC-0077, SPEC-0078, SPEC-0083 | Repoint each to its retained path |
| This package | SPEC-0083 in its Spec, Plan and Task | Repoint when SPEC-0083 is retained in this same round |

### The two retentions this round deferred

VAL-SBC-009 asks that every package reaching `done` be retained. Seven units
were. Two were not, and each is recorded here with the observed fact that
stopped it rather than counted as met.

| Package | Observed blocker | Next owner |
| --- | --- | --- |
| SPEC-0054 | `tests/test_document_strict_cutover.py` asserts this package's own structure: `tasks.md` absent and exactly fourteen append-only `tsk-*.md` records carrying matching identifiers and sections. Retention freezes those bytes, so the assertion becomes permanently true and stops detecting the drift it was written for. No other package can stand in, because the count is this package's own fact | Whoever decides what that test asserts once the package is frozen |
| SPEC-0062 | `.gitleaks.toml` carries a path-exact allowlist entry naming this package's `plan.md`, and `tests/test_qa_runner.py` pins the same path to prove the entry is read. Because the entry is path-exact rather than a prefix, retention edits a protected security surface inside a retention commit | Whoever moves the allowlist entry together with the retention |

Both packages are correctly `done`; only the move is outstanding. ADR-0039
admits a finished unit waiting at its own stage for a disposition decision, so
neither is a contract violation. Each carries the same dated note in its own
Spec and in the stage index row, so a reader reaches the reason from the
package rather than only from this record.

### What the retention round actually moved

| Class | Units | Envelope |
| --- | --- | --- |
| `completed/03.specs/` | SPEC-0006, SPEC-0071, SPEC-0077, SPEC-0078 | `500092f52e283356aa125e67ff46ca8d8baa95bd` |
| `superseded/03.specs/` | SPEC-0068, SPEC-0070 | `b4a1db9143fac30df39c23183432f3495d96a8ed` |
| `completed/03.specs/` | SPEC-0083 | `2eb5e079f8ca9f6d139fc7085fe8bebb886768ec` |

Three envelopes rather than one, because a unit's retained bytes must equal the
bytes of its envelope commit. SPEC-0068 and SPEC-0070 gained `superseded_by`
before the move, so their key had to land in its own commit and the envelope had
to name that commit. Writing the key and moving together was tried first and
failed with four diagnostics at once, `LIFECYCLE-CREATE`, `LIFECYCLE-EVIDENCE`,
`LIFECYCLE-IDENTITY-REUSE` and `ARCHIVE-CATALOG-RETENTION`. The four
`completed/` units of the first commit matched their envelope while these two
differed, which located the cause. Consumer repointing goes in the same commit
as the move; body edits go in an earlier one.

## Verification Summary

Every work item is recorded above with its observed result. Eleven are done and
one, WORK-009, is partial with two named deferrals.

Sixteen packages were disposed of: seven reached `done`, two reached
`withdrawn`, five stay with a dated note, and SPEC-0068 and SPEC-0070 were
already `superseded`. Seven units were retained, two registry gaps were closed
as gap-fills, and one duplicated frontmatter reader was resolved to a single
owner with a byte-identical gate output.

No gate, contract, or test pin was lowered at any point in this round. Where a
criterion could not be met, it is recorded as a deferral with a named owner: the
two retentions above, SPEC-0077's two authority-blocked criteria, and
SPEC-0072's native-runtime half.

### Full QA on the final tree

`python3 scripts/qa.py full` over 1172 paths returns 23 PASS after two repairs
the lane itself surfaced. It first returned 22 PASS and one FAIL, and neither
failure was weakened to pass: one was a regression this round introduced, and
the other was a cost pin that the round was required to move with an
attribution.

The run first reported two failures and one was repaired. The frozen-generation
fixture in `tests/archive_generation_fixture.py` derives the pre-ADR-0038
registry by reversing what later decisions added to the current one, then proves
the derivation equals the blob merged at `c652331c`. The two registry gap-fills
of WORK-002 were additions of exactly that kind, and no matching reversal was
written, so the derivation stopped reproducing the frozen blob. A parsed
comparison of derived against frozen showed five differences and no others, all
five being this round's own additions: `superseded_by` in the `optional` and
`order` lists of `sdlc/spec` and `common/template-sdlc-spec`, and the `draft` to
`withdrawn` pair in the `spec-plan` domain. The derivation now reverses them,
and its proof passes with the whole fixture-consuming set, 126 tests over four
modules, passing with it. This was a regression introduced in `238eac6a` and
carried undetected for twenty-six commits, because `unit-tests` runs only in the
full lane while every commit in this round touched paths whose surfaces select
the staged lane's six gates.

| Gate | First run | Final run |
| --- | --- | --- |
| Twenty-two gates, `archive-cutover` and `archive-contract-tests` among them | PASS | PASS |
| `unit-tests` | FAIL, two assertions | PASS |

The second failure was the Git subprocess bound in
`tests/test_archive_validation.py`: the archive snapshot makes 254 subprocesses
against a budget of 252. That budget is a documented ledger of justified
increases, 242 to 246 to 248 to 252, each recorded with the structural reason
that moved it. Raising it on a cost model that merely fits, without a baseline
that proves the attribution, would be indistinguishable from lowering a pin to
pass. The request owner directed that the baseline be measured and the increase
recorded the way every previous one was, which is what happened.

The baseline was taken on a linked worktree at `e062290e`, the commit this round
started from. A linked worktree shares the object database and refs while
carrying its own checkout and index, so the archived-bytes recovery reads the
same history the main worktree reads. It was created on a branch rather than
detached, because a detached checkout adds a fixed eight `--points-at HEAD`
batches that would have inflated the baseline and inverted the attribution. The
loaded module was asserted to come from the baseline tree, and its registry was
confirmed to carry the pre-gap-fill `optional` list.

The baseline ran 252 and this tree runs 254. Comparing the two command sets with
the `-C` root and the branch-ref name normalized away, so that only what was
asked is compared, leaves three added `ls-tree` calls and one removed
`cat-file --batch`, a net two.

| Change | Effect |
| --- | --- |
| `ls-tree` at `16574635` for SPEC-0006, at `a5bad5ff` for SPEC-0071, at `b4a1db91` for SPEC-0068 and SPEC-0070 together | +3 |
| The `log --diff-filter=AM` operand list grew from two paths to seven | 0, one process either way |
| Three recovery groups merged into one `cat-file --batch` where the base needed two | -1 |
| SPEC-0077, SPEC-0078 and SPEC-0083 | 0, their paths join groups that already exist |

That refines the cost model the comment block states. The fixed four a vacating
rename costs is not four per package: only the exact tree entry is per recovery
group, while branch resolution, the last add-or-modify `log`, and the batched
object read are shared. A retention round therefore costs one process per
distinct last add-or-modify commit among the vacated paths a sealed record still
names, less the `cat-file` batches it merges. Seven packages cost two because
they resolve to three such commits and merge one batch.

The budget is 254 with that attribution recorded beside the four increases
before it, and the gate passes. No assertion was relaxed: the bound still pins
the exact measured cost, so the next structural change will fail it again, which
is the whole value of the pin.

This record, its Spec and its Plan were created in their zero-indegree states
because the lifecycle gate compares a change with its base, where this package
did not yet exist. Activation followed as its own reviewed change in `10847dc2`,
and WORK-001 is recorded from that point.

Every result recorded here is repository-static. No hosted CI run, provider
runtime, live cluster, or network action is claimed by any of them, and push,
pull request, and merge stay with the request owner.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | The survey of all sixteen packages is recorded below. |
| [WORK-002](../plan.md#work-breakdown) | Done. | Registry gap-fill recorded below; five focused gates and 87 archive contract tests pass. |
| [WORK-003](../plan.md#work-breakdown) | Done. | SPEC-0071, SPEC-0078, SPEC-0062 and SPEC-0054 are `done`; the lifecycle gate passes in strict mode. |
| [WORK-004](../plan.md#work-breakdown) | Done. | SPEC-0048 and SPEC-0051 are `withdrawn`; their twelve Tasks are `cancelled` through the declared two-step path. |
| [WORK-005](../plan.md#work-breakdown) | Done. | SPEC-0006's stale sibling path was repaired in its own commit before the move, then the package closed. |
| [WORK-006](../plan.md#work-breakdown) | Done. | SPEC-0068 and SPEC-0070 carry `superseded_by` and are retained in `superseded/` with one catalog row each. |
| [WORK-007](../plan.md#work-breakdown) | Done. | Five staying packages carry dated notes; SPEC-0072's Task is `blocked`. |
| [WORK-008](../plan.md#work-breakdown) | Done. | One reader remains; the link gate's stdout sha256 is unchanged at `e1925925`. |
| [WORK-009](../plan.md#work-breakdown) | Partial, with two named deferrals. | Seven units retained; SPEC-0054 and SPEC-0062 recorded below with their observed blockers and next owners. |
| [WORK-010](../plan.md#work-breakdown) | Done. | Four consumers repaired; no gate, contract or test pin lowered. |
| [WORK-011](../plan.md#work-breakdown) | Done. | SPEC-0077 is `done` with two deferrals carrying named owners. |
| [WORK-012](../plan.md#work-breakdown) | Done. | Full QA returns 23 PASS after repairing a regression this round introduced and raising a cost pin with a measured baseline attribution. |
