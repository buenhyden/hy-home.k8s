---
title: 'Workspace Research Full-Corpus Reverification Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-23
artifact_id: "PLAN-0062"
---

# Workspace Research Full-Corpus Reverification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reverify every existing WER research owner against current primary
external sources and current workspace evidence, then append the reviewed delta
to the sole existing research pack without creating a duplicate owner.

**Architecture:** Five read-only research agents produce immutable structured
reports for one closed thirty-six-row corpus. A single controller validates the
union, assigns source and claim IDs centrally, and dispatches sequential
integration tasks that edit disjoint topical owners before one shared-ledger and
cross-link reconciliation path.

**Tech Stack:** Markdown, JSON, Python 3 standard library, Git, GitHub CLI
read-only metadata queries, repository document validators, pre-commit, and the
Superpowers subagent-driven development workspace.

**Spec:**
[`spec.md`](spec.md)

## Global Constraints

- The existing `docs/90.references/research/2026-08-08-wer/` directory remains
  the sole research pack; create no new research folder, topic report, parallel
  ledger, or `REQ-WERPC-*` owner.
- Process exactly thirty-six owner rows, `REQ-WERPC-001` through
  `REQ-WERPC-036`, once each.
- The immutable starting census is fourteen Markdown files, thirty-six request
  rows, ninety unique source IDs, and one hundred thirty-five unique claim IDs.
- All current version, release, feature, permission, and policy facts use the
  truthful observation date `2026-08-20`.
- New sources begin at `SRC-WERPC-091`. New claims use
  `CLM-WERPC-013-NN`, beginning at `CLM-WERPC-013-01`.
- External and workspace results are independent. Never infer one from the
  other.
- `unreachable` is not `unchanged`; `superseded` and `contradicted` retain both
  old and current evidence identities.
- Provider runtime, hosted CI outcome, live infrastructure, and human judgement
  remain `DEFER` without separately authorized evidence of that class.
- Research agents are read-only. They write only their assigned JSON report in
  this Plan's ignored SDD workspace and never edit, stage, commit, or allocate
  final IDs.
- The controller is the sole identifier allocator. Integration implementers may
  use only their immutable allocation-map slice.
- Remote GitHub access is read-only, allowlisted, sanitized, and at most once
  per evidence class. No workflow dispatch, rerun, approval, merge, settings
  mutation, raw log, token, or secret-bearing output is allowed.
- Existing pack text, dates, IDs, and claims are append-only. Corrections are
  additive.
- The primary checkout's pre-existing staged RIA changes are foreign to this
  Plan and must not be read as this branch's delta, modified, staged, reverted,
  committed, or cleaned.
- Every task-owned transient is a current-user regular file under this Plan's
  ignored SDD workspace with mode `0600`; symlinks and foreign files fail
  closed.
- Each tracked work package is one logical commit and receives an independent
  spec-compliance and quality review. Python or security-sensitive changes also
  receive the corresponding specialist review.
- No push, merge, publication, branch deletion, worktree deletion, or other
  external side effect occurs before `superpowers:finishing-a-development-branch`
  presents the human choice.

### Guarded SDD artifact protocol

The Plan-owned SDD workspace is a closed artifact boundary. Its durable
inventory is `artifact-inventory.json`. The allowed artifact classes are the
SDD ledger, task briefs, implementer reports, review packages, the task-local
checker, baseline, five research reports, allocation map, sanitized remote
summary, and affected/staged NUL pathsets. No other file class is admitted.

The canonical Plan remains the registry-routed `plan.md`. The exact temporary
alias `/tmp/0062-workspace-research-full-corpus-reverification-plan.md` was
authorized only to give the initial `sdd-workspace` call a unique basename and
create
`.superpowers/sdd/0062-workspace-research-full-corpus-reverification-plan/`.
The completed bootstrap helper calls consumed that alias before its loss. On
2026-08-21 the alias was observed absent and non-symlink; the cause is not
proved. It must not be recreated, synchronized, or passed to another helper,
and the checker `helper-sync` command is not authorized for any remaining
execution.

Every remaining `task-brief` or `review-package` call uses the canonical Plan
path directly and supplies its output argument explicitly under the existing
exact SDD workspace. The controller must never call `sdd-workspace` again and
must never allow either helper to select a default output. Before each call,
the controller guarded-reads the canonical Plan as a current-user regular
non-symlink, captures its complete FileVersion and SHA-256, and freezes that
version against tracked or concurrent mutation until the helper returns. It
also proves the exact SDD workspace is the recorded current-user-owned
non-symlink directory at mode `0700`, proves the explicit output absent and
non-symlink, and sets `umask 077`. After the call it requires the canonical Plan
FileVersion unchanged, postvalidates the output as a current-user mode-`0600`
regular non-symlink inside that exact workspace, and immediately registers the
output before any consumer runs. A mismatch stops execution without alias
recovery, helper synchronization, or a second call.

Before the checker exists, WRFR-000 records every helper-returned artifact path
in `progress.md` after resolving it under the exact SDD root, rejecting a
symlink or non-regular file, confirming current-user ownership, and setting
mode `0600`. WRFR-001 initializes `artifact-inventory.json` from that exact
record and then registers the checker and inventory itself. Thereafter, every
`task-brief` and `review-package` result and every named output is registered
immediately through the checker before another consumer runs. Registration is
version-bound and fails on an outside-root path, duplicate, missing file,
symlink, wrong owner, wrong mode, or unapproved artifact class.

One material, one-time WRFR-001 recovery exception is authorized after direct
checker review legitimately changes the already registered checker and appends
review evidence to the already registered Task 2 implementer report. The only
recovery surface is:

```text
artifact-rebind-checker-review --workspace DIR --inventory FILE \
  --expected-inventory-sha256 OLD_INVENTORY \
  --expected-old-checker-sha256 OLD_CHECKER \
  --approved-new-checker-sha256 NEW_CHECKER \
  --expected-old-report-sha256 OLD_REPORT \
  --approved-new-report-sha256 NEW_REPORT
```

The two targets are implicit and fixed to `DIR/full-corpus-check.py` and
`DIR/task-2-report.md`; the parser exposes no target-path argument. Before the
Task 2 report is frozen, its post-registration review evidence is summarized in
mutable `progress.md`. The final amendment and direct-review preparation are
then appended to `task-2-report.md`, its approved new SHA-256 is captured, and
the report is never written again. Every later WRFR-001 result is recorded only
in mutable `progress.md`. There is no generic report rebind, and
`artifact-register` retains its duplicate rejection unchanged.

The recovery command requires lowercase 64-hex, changed old/new checker and
report identities; exact current inventory content SHA-256 equal to
`OLD_INVENTORY`; the exact direct-child inventory path; the existing inventory
schema, allowed classes, mutable entries, unique names, and exactly one
immutable record for each fixed target; old record SHA-256 values equal to the
two expected-old flags; and guarded current checker/report versions whose
SHA-256 values equal the two approved-new flags. It validates every other
immutable artifact against its complete registered FileVersion and revalidates
both mutable artifacts. Wrong mode, owner, symlink, missing target, third-file
drift, stale inventory content/version, unchanged identity, or an additional
target fails closed.

The command retains the complete old inventory bytes and FileVersion, reads
both fixed targets before mutation, re-reads them immediately before the
inventory CAS, and constructs an artifact list of identical length and order.
Exactly the two existing records at their original indices are replaced with
guarded current FileVersions; every other value is unchanged. The inventory
replacement uses the old complete FileVersion as its CAS expectation. After
CAS, the command re-reads both targets, requires their FileVersions unchanged,
reads the new inventory at the exact CAS-returned FileVersion, and postvalidates
the complete inventory and every artifact. It never mutates checker or report
bytes.

If any post-CAS target read or postvalidation fails, rollback may restore the
exact old inventory bytes only when the inventory still has the exact new
FileVersion returned by the command's CAS. Successful rollback is verified and
then reports a fixed recovery failure. A concurrent update or failed rollback
must not be overwritten and returns a fixed rollback-failed diagnostic. No
stateful recovery runs until the amended tracked contract and exact new checker
and frozen-report hashes receive fresh Python and security direct approval.

The terminal residue check requires directory contents and inventory to be
equal. The SDD finish procedure runs only after the final consumer, removes
only the exact resolved Plan workspace, and proves that exact path absent. The
helper Plan alias has an absent final desired state. If it remains absent and
non-symlink, terminal cleanup skips `remove-owned-helper-plan`; if it reappears,
execution stops and must not delete an unproved file.

The shared parent `.superpowers/sdd/.gitignore` was initially absent. The
current helper-created marker was observed on 2026-08-21 as the recorded
current-user regular non-symlink containing exactly `*\n` with its recorded
FileVersion, but mode `0644`; `restore-shared-marker` would reject that state.
Do not chmod it, update its provenance, or call `restore-shared-marker`. Only
after every helper and reviewer consumer is complete, residue passes, final
reviews approve, and the exact SDD workspace satisfies its finish preconditions
may a separately reviewed fd-bound terminal cleanup remove the marker. That
cleanup must open the exact `.superpowers/sdd` parent without following a
symlink, prove the marker still matches the recorded owner, regular-file type,
non-symlink status, exact bytes, and complete FileVersion, and prove no foreign
sibling exists; it may then unlink only that exact directory entry through the
validated parent descriptor and prove it absent. Any identity drift, wrong
type, symlink, foreign sibling, or review gap stops cleanup without chmod,
provenance change, generic deletion, or a completion claim. The terminal marker
state remains the recorded initial state: absent.

For every Task, the controller records `WRFR_TASK_BASE=$(git rev-parse HEAD)`
before dispatch. The implementer completes focused validation and commits the
logical unit before returning its report. Only then does the controller run
`review-package` against the canonical Plan over `WRFR_TASK_BASE..HEAD`, with
an explicit absent output path in the existing SDD workspace under the guarded
protocol above, and dispatch the task reviewer. A required fix is a new scoped
commit followed by a new explicit-output review package from the same original
base through the new `HEAD` and one scoped re-review. The successor Task is not
dispatched until both Spec compliance and task quality are approved. Every
helper output is validated and registered before a reviewer consumes it.
Every implementer and research-agent prompt requires its report path to be
absent/non-symlink and created with `O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`,
same-file write/flush/version checks, and no reopen-by-path mutation. The private
SDD directory is mode `0700`; no parallel implementers run, and parallel
research agents own disjoint report paths.

---

## Overview

This Plan executes [Spec 0062](spec.md) as ten work packages. It retains one
Plan because the five research areas share the same closed corpus, identifier
space, source and claim ledger, scope index, pack index, and terminal count
projection. Separate Plans would create competing allocators and duplicate
owner risk.

Execution uses `superpowers:subagent-driven-development`. The controller first
creates the plan-specific ignored workspace and progress ledger. `WRFR-001`
then dispatches five read-only research agents in parallel, validates their
combined thirty-six-row result, and writes one immutable allocation map. The
next five tasks consume disjoint allocation slices and edit only their topical
owners. The final three tasks write shared ledgers, reconcile lifecycle and
cross-links, and close validation.

## Context

Predecessor Spec 0059 completed a full-corpus observation on 2026-08-17 and
corrected one Kubernetes claim on 2026-08-18. The current pack contains
fourteen Markdown files, thirty-six owners, ninety source IDs, and one hundred
thirty-five claim IDs. Its
status matrix contains twenty-three `Verified`, one `Verified gap`, and twelve
`Partial` rows.

The predecessor also assigned one blocking class per retained boundary:
twelve rows are unblocked, ten remain reachable by repository-static work, and
fourteen require provider-runtime, hosted-CI, live-cluster, or human-judgement
evidence. This cycle still re-observes public and repository-static evidence for
all rows; it does not present the structural absence of deeper evidence as a new
finding or promote it from static proof.

The authoring branch is already isolated at
`.worktrees/2026-08-20-full-corpus-reverification` on
`codex/2026-08-20-full-corpus-reverification`. The pre-authoring aggregate
quality gate passed. The primary checkout remains dirty with unrelated staged
RIA changes and is outside this Plan.

## Goals & In-Scope

- Activate one direct-approval standalone Spec/Plan/Task relation for Spec 0062.
- Build a fail-closed baseline, research-report, allocation, pathset, remote
  summary, integration, and residue checker in the ignored SDD workspace.
- Re-observe every registered external source and run one bounded current-source
  discovery query per owner to detect relocation, replacement, and new official
  versions.
- Re-observe every workspace selector at the exact branch baseline and terminal
  tree.
- Append one dated section to every affected topical owner, using concise rows
  for unchanged owners and detailed comparisons for changed owners.
- Add reviewed source and claim records, re-project all ten governance scopes,
  and reconcile pack and collection indexes.
- Inspect both tracked workflow configuration and the approved remote GitHub
  Actions metadata classes.
- Preserve all deeper-evidence limits and route implementation candidates to
  their canonical owner without implementing them.
- Close with logical commits, task-scoped reviews, one whole-branch review,
  terminal repository-static gates, and owned-transient cleanup.

## Non-Goals & Out-of-Scope

- New research folders, reports, request owners, policies, manifests, workflows,
  application code, runtime configuration, deployment state, or credentials.
- Live cluster, provider runtime, registry, Vault, ESO, Argo CD, gateway,
  recovery, user, operator, stakeholder, or accessibility observation.
- Paid-standard clause retrieval or inference from public catalog abstracts.
- Retrying or replacing a failed remote GitHub query outside the exact recovery
  encoded in this Plan.
- Updating an existing observation in place instead of appending its new state.
- Cleaning another Plan's ignored workspace, `/tmp` file, linked worktree,
  untracked artifact, or staged change.
- Pushing, merging, publishing, or deleting branch/worktree state.

**Controller Setup (pre-dispatch, not a Task)**

The controller performs this setup after Plan approval and before generating or
dispatching Task 1. It is not part of any extracted `Task N` brief and is never
replayed by an implementer.

1. Record the initial state of `.superpowers/sdd`, its shared `.gitignore`
   marker, and the exact helper-Plan alias. Reject a symlink, foreign owner,
   non-directory parent, non-regular marker, or marker bytes other than `*\n`.
2. Run the exact bootstrap commands:

   ```bash
   WRFR_PLAN=docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md
   WRFR_HELPER_PLAN=/tmp/0062-workspace-research-full-corpus-reverification-plan.md
   test ! -e "$WRFR_HELPER_PLAN"
   test ! -L "$WRFR_HELPER_PLAN"
   umask 077
   install -m 600 "$WRFR_PLAN" "$WRFR_HELPER_PLAN"
   cmp -- "$WRFR_PLAN" "$WRFR_HELPER_PLAN"
   WRFR_SDD=$(bash /home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/subagent-driven-development/scripts/sdd-workspace "$WRFR_HELPER_PLAN")
   test -d "$WRFR_SDD"
   test ! -L "$WRFR_SDD"
   chmod 700 "$WRFR_SDD"
   ```

3. Require `$WRFR_SDD/progress.md` and `$WRFR_SDD/task-1-brief.md` absent and
   non-symlink. Create the ledger as a current-user mode-`0600` regular file
   whose first line is exactly:

   ```markdown
   # SDD ledger — plan: docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md
   ```

4. Run `task-brief` against `WRFR_HELPER_PLAN` for Task 1 with explicit output
   `$WRFR_SDD/task-1-brief.md` under `umask 077`. Verify both files are
   current-user regular mode `0600`, record their hashes and the initial shared
   marker state in the ledger, and only then dispatch the Task 1 implementer.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WRFR-000 | Lifecycle activation | Written Spec and Plan approved | Clean isolated branch at Spec commit | Active Spec/Plan/Task relation, focused validators, commit |
| WRFR-001 | Closed-corpus evidence intake and allocation | WRFR-000 | Exact baseline census and guarded SDD workspace | Five reviewed JSON reports, 36/36 union, allocation map, commit |
| WRFR-002 | Agent engineering integration | WRFR-001 | Approved report and allocation slice | Four topical owners, focused validators, review, commit |
| WRFR-003 | Provider and common-environment integration | WRFR-001 | Approved report and allocation slice | Two topical owners, focused validators, review, commit |
| WRFR-004 | SDLC and documentation integration | WRFR-001 | Approved report and allocation slice | Three topical owners, focused validators, review, commit |
| WRFR-005 | Platform and security integration | WRFR-001 | Approved report and allocation slice | Kubernetes owner, static platform validators, review, commit |
| WRFR-006 | Delivery and quality integration | WRFR-001 | Pre-remote security approval and allocation slice | CI/QA owner, sanitized remote summary, review, commit |
| WRFR-007 | Source, claim, scope, and pack integration | WRFR-002..006 | All topical sections reviewed | Shared ledger and projections exact, review, commit |
| WRFR-008 | Cross-link and lifecycle reconciliation | WRFR-007 | Terminal counts and links known | Indexes, lifecycle state, progress, review, commit |
| WRFR-009 | Terminal validation, whole-branch review, and cleanup | WRFR-008 | Exact branch diff and task inventory frozen | Green terminal tree, no open Critical/Important, owned residue absent |

### Task 1: WRFR-000 — lifecycle activation

**Files:**

- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Modify: `docs/99.templates/registry.json`
- Modify: `scripts/validate-links-and-owners.py`
- Modify: `tests/test_document_strict_cutover.py`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the approved `SPEC-0062`, this Plan, direct approval dated
  `2026-08-20`, and ADR 0022's standalone-execution relation.
- Produces: active `SPEC-0062`/`PLAN-0062`/`TASK-0062`, registry relation
  `spec=0062`, exact approval statement validation, and a durable activation
  record consumed by every later task.

- [ ] **Step 1: verify the controller bootstrap**

  Consume, but do not recreate, the controller-owned bootstrap. Run:

  ```bash
  WRFR_PLAN=docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md
  WRFR_HELPER_PLAN=/tmp/0062-workspace-research-full-corpus-reverification-plan.md
  WRFR_SDD=.superpowers/sdd/0062-workspace-research-full-corpus-reverification-plan
  test -f "$WRFR_HELPER_PLAN"
  test ! -L "$WRFR_HELPER_PLAN"
  cmp -- "$WRFR_PLAN" "$WRFR_HELPER_PLAN"
  test -d "$WRFR_SDD"
  test ! -L "$WRFR_SDD"
  test -f "$WRFR_SDD/progress.md"
  test ! -L "$WRFR_SDD/progress.md"
  test -f "$WRFR_SDD/task-1-brief.md"
  test ! -L "$WRFR_SDD/task-1-brief.md"
  ```

  Verify current-user ownership, workspace mode `0700`, file modes `0600`, the
  exact ledger identity line, and the recorded initial shared-marker state. Any
  mismatch is a bootstrap blocker; Task 1 never repairs or replays setup.

- [ ] **Step 2: write the failing standalone-approval regression**

  Add a focused test in `tests/test_document_strict_cutover.py` that imports the
  cross-document validator module, parses the two validator-recognized
  standalone approval sentences from the Spec 0062 body, and asserts:

  ```python
  assert validator.STANDALONE_APPROVAL_STATEMENTS["0062"] == expected_from_spec
  ```

  The parser accepts only the existing exact standalone grammar, Spec ID `0062`,
  and approval date `2026-08-20`; it is not a second wording owner. Run the exact
  test and record RED because the draft Spec and validator relation are not yet
  activated:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover.DocumentStrictCutoverTests.test_spec_0062_standalone_approval_contract
  ```

- [ ] **Step 3: activate the lifecycle relation**

  Apply these exact changes:

  - set Spec, Plan, and Task frontmatter `status: active`;
  - replace the entire three-sentence draft approval paragraph in the Spec with
    only the validator-established final direct-approval and lifecycle-exclusion
    sentences for Spec `0062` on `2026-08-20`, so no
    `Execution remains unauthorized` sentence survives activation;
  - replace Task Overview/Task Table evidence that says Plan review or execution
    approval is pending with the active authorization date, activation commit,
    and next owner `WRFR-001`;
  - add Spec 0062's Plan and Task to the Spec's Related Documents;
  - expand the Stage 03 tree entry to `spec.md`, `plan.md`, and `tasks.md`, and
    change the index row to `Active`;
  - append ADR 0022's tenth standalone lineage row for Spec 0062;
  - append this sorted registry row after `0054`:

    ```json
    {
      "spec": "0062",
      "plan": "docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md",
      "task": "docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md",
      "state": "active",
      "reason": "Direct human-approved full-corpus external-source and workspace reverification over the existing WER research pack",
      "decision": "0022",
      "approvalMode": "spec-body-record"
    }
    ```

  - add the exact `0062` tuple to `STANDALONE_APPROVAL_STATEMENTS`;
  - append the activation evidence and next owner `WRFR-001` to durable
    progress.

- [ ] **Step 4: run the focused GREEN checks**

  ```bash
  python3 -m unittest tests.test_document_strict_cutover.DocumentStrictCutoverTests.test_spec_0062_standalone_approval_contract
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Expected: the focused test passes, registry reports zero uncovered or
  ambiguous paths, Markdown reports zero violations, and links report
  `PASS CROSS-DOCUMENT`.

- [ ] **Step 5: commit the activation**

  ```bash
  git add docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/03.specs/README.md \
    docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md \
    docs/99.templates/registry.json \
    scripts/validate-links-and-owners.py \
    tests/test_document_strict_cutover.py \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: activate full-corpus research reverification"
  ```

- [ ] **Step 6: review the committed activation and prepare Task 2**

  This completed bootstrap step is historical and must not be replayed after
  the 2026-08-21 alias-loss observation.

  Generate the SDD review package for the recorded Task 1 base through the
  activation `HEAD`. Dispatch one task reviewer for Spec compliance and quality
  and one `python-reviewer` for the validator and test changes. Resolve every
  Critical or Important finding in a separate fix commit and perform one scoped
  re-review before WRFR-001 begins.

  Write a closed bootstrap artifact list to `progress.md` containing only the
  ledger itself, the exact helper-returned WRFR-000 brief path, implementer
  report path, review package paths, and the Task 2 brief path created below.
  Resolve each below the SDD root, reject symlinks/non-regular or foreign-owned
  files, and set mode `0600`; `artifact-init` consumes this exact list in
  WRFR-001. Synchronize the updated canonical Plan to `WRFR_HELPER_PLAN` through
  a mode-`0600` temporary regular file and atomic replacement, verify byte
  equality, then generate the explicit `$WRFR_SDD/task-2-brief.md` output for
  the WRFR-001 implementer and append that exact path to the bootstrap list.

### Task 2: WRFR-001 — closed-corpus evidence intake and allocation

**Files:**

- Create in ignored SDD workspace: `full-corpus-check.py`
- Create in ignored SDD workspace: `artifact-inventory.json`
- Create in ignored SDD workspace: `baseline.json`
- Create in ignored SDD workspace: `research-agent-engineering.json`
- Create in ignored SDD workspace: `research-provider-common.json`
- Create in ignored SDD workspace: `research-sdlc-documentation.json`
- Create in ignored SDD workspace: `research-platform-security.json`
- Create in ignored SDD workspace: `research-delivery-quality.json`
- Create in ignored SDD workspace: `allocation.json`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: active lifecycle, pack README coverage matrix, source and claim
  ledger, scope index, branch baseline, the exact five workstream row sets.
- Produces: guarded baseline, five immutable reviewed reports whose row union is
  exactly `001..036`, and one allocation map beginning at `SRC-WERPC-091` and
  `CLM-WERPC-013-01`.

- [x] **Step 1: write the checker self-test before implementation**

  Require `full-corpus-check.py` absent/non-symlink and create it with
  `O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`, under the private SDD directory
  before applying the test-first body.

  The checker uses only Python 3 standard-library modules. Define these exact
  constants and command surface:

  ```python
  EXPECTED_WORKSTREAMS = {
      "agent-engineering": ("001", "002", "026", "027", "028", "029", "030", "031", "032"),
      "provider-common": ("003", "004", "005", "006"),
      "sdlc-documentation": ("007", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "034", "035", "036"),
      "platform-security": ("008", "009", "025"),
      "delivery-quality": ("022", "023", "024", "033"),
  }
  EXTERNAL_RESULTS = {"changed", "unchanged", "unreachable", "superseded", "contradicted"}
  WORKSPACE_RESULTS = {"confirmed", "absent", "drifted"}
  DISPOSITIONS = {"Verified", "Verified gap", "Partial", "Contradicted"}
  SOURCE_START = 91
  CLAIM_BLOCK = 13
  ```

  Required subcommands:

  ```text
  self-test
  baseline --root ROOT --output FILE
  validate-research --baseline FILE --report-dir DIR
  allocate --baseline FILE --report-dir DIR --output FILE
  validate-integration --root ROOT --baseline FILE --allocation FILE
  remote-init --root ROOT --output FILE
  remote-query --root ROOT --summary FILE --class CLASS -- COMMAND...
  remote-validate --summary FILE
  helper-sync --source FILE --target FILE
  artifact-init --workspace DIR --inventory FILE --bootstrap-ledger FILE
  artifact-register --workspace DIR --inventory FILE --path FILE
  artifact-rebind-checker-review --workspace DIR --inventory FILE --expected-inventory-sha256 OLD_INVENTORY --expected-old-checker-sha256 OLD_CHECKER --approved-new-checker-sha256 NEW_CHECKER --expected-old-report-sha256 OLD_REPORT --approved-new-report-sha256 NEW_REPORT
  artifact-rebind-checker-only --workspace DIR --inventory FILE --expected-inventory-sha256 OLD_INVENTORY --expected-old-checker-sha256 OLD_CHECKER --approved-new-checker-sha256 NEW_CHECKER
  remove-owned-gh-state-residue --root ROOT
  remote-recover-auth-context --workspace DIR --inventory FILE --summary FILE --expected-inventory-sha256 OLD_INVENTORY --expected-summary-sha256 OLD_SUMMARY
  remote-recover-oidc-schema --workspace DIR --inventory FILE --summary FILE --expected-inventory-sha256 OLD_INVENTORY --expected-summary-sha256 OLD_SUMMARY
  pathset --root ROOT --base SHA --lane affected|staged|all-files --output FILE
  residue --workspace DIR --inventory FILE
  remove-owned-helper-plan --path FILE
  restore-shared-marker --workspace DIR --bootstrap-ledger FILE
  ```

  Self-test cases must exercise exact 36-row coverage, missing/extra/duplicate
  rows, every closed vocabulary, source and claim start IDs, duplicate or
  noncontiguous allocation, source URL HTTPS/host/date validation, selector
  normalization, symlink/outside-root rejection, same-inode mutation,
  exclusive-create contention, pathset wildcard/Git-magic/control-character
  rejection, remote argv allowlisting, remote scalar/schema rejection, remote
  query timeout, per-class documented-unavailable recording, helper Plan
  synchronization/removal, shared-marker existing/absent/foreign-sibling
  restoration, and duplicate/foreign residue.
  Artifact tests also cover unregistered extras, missing inventory members,
  duplicate registration, disallowed file classes, wrong mode/owner, and
  symlink substitution.

  Run before implementing the parser and record RED for the first missing
  command handler:

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" self-test
  ```

- [x] **Step 2: implement and verify the guarded checker**

  Implement same-file guarded I/O with `os.open`, mandatory `O_NOFOLLOW`,
  `O_CREAT|O_EXCL` for creation, mode `0600`, current UID, regular-file checks,
  pre/post read version checks over inode, size, `mtime_ns`, `ctime_ns`, and
  SHA-256, and atomic compare-and-swap for sanctioned updates. Never include raw
  untrusted payload values in diagnostics.

  Run:

  ```bash
  python3 -m py_compile "$WRFR_SDD/full-corpus-check.py"
  python3 "$WRFR_SDD/full-corpus-check.py" self-test
  sha256sum "$WRFR_SDD/full-corpus-check.py"
  ```

  Before invoking any stateful checker subcommand, dispatch one
  `python-reviewer` and one `security-reviewer` with the checker path, exact
  SHA-256, complete self-test output, Spec, and this Task brief. They review the
  ignored source directly, including guarded I/O, remote argv/output handling,
  pathset creation, artifact inventory, synchronization, and removal. Resolve
  every Critical or Important finding in the checker, rerun compile/self-test,
  and obtain scoped re-review. Record the approved hash in Task/progress. Any
  later checker byte change invalidates that approval and requires the same
  compile/self-test/direct-review gate before reuse.

  After approval, initialize the artifact inventory:

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-init \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --bootstrap-ledger "$WRFR_SDD/progress.md"
  ```

  Expected: every named mutation case and terminal `PASS self-test` print once;
  the inventory contains `progress.md`, the checker, itself, and the exact Task
  1 brief/report/review-package plus Task 2 brief paths recorded in the bootstrap
  ledger.

- [x] **Step 3: capture the exact baseline**

  ```bash
  WRFR_BASE=$(git rev-parse HEAD)
  python3 "$WRFR_SDD/full-corpus-check.py" baseline \
    --root . \
    --output "$WRFR_SDD/baseline.json"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_SDD/baseline.json"
  ```

  The checker must reject any census other than fourteen Markdown pack files,
  request IDs `001..036`, ninety unique sources ending at `090`, one hundred
  thirty-five unique claims ending at `012-04`, and the exact 36-row status and
  blocking-class mappings parsed from current canonical owners. Record
  `WRFR_BASE`, baseline SHA-256, file mode, and census in the Task.

- [x] **Step 4: dispatch five read-only research agents**

  Dispatch the five evidence agents in parallel. Each agent receives only its
  exact request-ID tuple, the relevant topical owner paths, the source ledger,
  workspace authority files, and the output schema. Each writes one guarded JSON
  report named above and returns no repository edit.

  Each prompt repeats the guarded report creation contract from the global
  protocol. The five output paths must be absent/non-symlink before dispatch;
  no reviewer or allocator reads a report until the controller validates and
  registers that exact file after the agent returns.

  Every report row must contain:

  ```json
  {
    "requestId": "REQ-WERPC-NNN",
    "externalResult": "changed|unchanged|unreachable|superseded|contradicted",
    "checkedOn": "2026-08-20",
    "sources": [{"url": "https://official.example/path", "revision": "observed identity", "sourceClass": "official-primary", "uncertainty": "bounded text"}],
    "workspaceResult": "confirmed|absent|drifted",
    "workspaceCommit": "40-hex commit",
    "selectors": ["repository/path#exact-selector"],
    "asIs": "bounded statement",
    "gap": "bounded statement",
    "target": "bounded descriptive target",
    "adoptedClaim": "supported claim",
    "rejectedInference": "unsupported inference",
    "evidenceDepth": "public-documentation|repository-static|hosted-metadata",
    "disposition": "Verified|Verified gap|Partial|Contradicted",
    "blockingClass": "none|repo-static|provider-runtime|hosted-ci|live-cluster|human-judgement",
    "missingEvidence": "named evidence or N/A",
    "owner": "canonical owner",
    "safeFollowUp": "bounded follow-up",
    "refreshTrigger": "material trigger",
    "sourceProposals": [],
    "claimProposals": [],
    "limitations": []
  }
  ```

  Agents must re-open every registered official URL for their rows and execute
  one official-domain discovery query per row for a replacement, current release,
  or superseding specification. Search snippets are locator evidence only; the
  original page or official repository revision must be read before adoption.

  After all five agents return, register the five fixed report paths before
  review:

  ```bash
  for WRFR_REPORT in \
    research-agent-engineering.json \
    research-provider-common.json \
    research-sdlc-documentation.json \
    research-platform-security.json \
    research-delivery-quality.json
  do
    python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
      --workspace "$WRFR_SDD" \
      --inventory "$WRFR_SDD/artifact-inventory.json" \
      --path "$WRFR_SDD/$WRFR_REPORT"
  done
  ```

- [x] **Step 5: independently review each research report**

  Dispatch one source-fidelity reviewer per workstream and one cross-workstream
  quality reviewer after all five reports exist. Reviews check source identity,
  checked-on date, claim support, selector existence, evidence depth, exact row
  membership, duplicate research, and DEFER boundaries. Resolve every Critical
  or Important finding in the report and re-review before allocation.

- [x] **Step 6: validate the union and allocate IDs**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-research \
    --baseline "$WRFR_SDD/baseline.json" \
    --report-dir "$WRFR_SDD"
  python3 "$WRFR_SDD/full-corpus-check.py" allocate \
    --baseline "$WRFR_SDD/baseline.json" \
    --report-dir "$WRFR_SDD" \
    --output "$WRFR_SDD/allocation.json"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_SDD/allocation.json"
  ```

  Expected: five reports, exact union `001..036`, zero duplicate owner, every
  selector present at `WRFR_BASE`, sources assigned contiguously from `091`, and
  claims assigned contiguously from `013-01`. Record report and allocation
  SHA-256 values in the Task.

- [x] **Step 7: update execution evidence and run focused checks**

  Record the intake implementation and evidence commit as complete only after
  the report reviews and allocation pass. Do not mark the complete WRFR-001 work
  package Done or transfer ownership to `WRFR-002` until Step 9's post-commit
  task review approves. Record the exact observed counts, hashes, review
  verdicts, source-access failures, and out-of-ledger observations, and update
  durable progress with the review-pending gate.

  ```bash
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Completion evidence on 2026-08-20: the five final registered report hashes
  are `f0dd1038b056d3f2bdc5e6c5e457e4f3c6cd93cdd5ab75375780101da9eca5b1`,
  `bf5728c6d4f69dce90cff533058372e243ffed28ed5b5ee8949444212250ce86`,
  `be273b3dad1b6b4f50d12285cf9114406ba5c3af94ded7646a71ceda5b47ae85`,
  `edff89e3b29fdcaa658044ffc768b7c297e39a02936bd39657c90bb759a7fbce`,
  and `f55cc2285577530544c48f26fb497184b43bb9822236e46a736294ed8695d993`.
  All five source-fidelity reviews returned `Approved`; the cross-workstream
  quality review returned `Approved` with Critical/Important/Minor `0/0/0`.

  The allocation SHA-256 is
  `04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`;
  the registered inventory SHA-256 is
  `39ef8f41848340daf9a0756a80611bcb549960080fc4bb5c8007a4ce625c8567`.
  The exact 36-row union produced one contiguous source
  `SRC-WERPC-091` and six contiguous claims `CLM-WERPC-013-01..06`,
  with no duplicate, gap, or reservation.

  `REQ-WERPC-033` records the unavailable registered NASA traceability URL as
  `unreachable`; `REQ-WERPC-022` and `023` record an unavailable official
  GitHub Environments URL without adopting environment claims. The sole
  out-of-ledger source proposal is the official K3s v1.35 release-family source
  for `REQ-WERPC-009`, allocated as `SRC-WERPC-091`; no new request owner was
  created. The immutable row-020 baseline observation remains preserved, its
  known legacy selector is normalized to the real `#ditaxis-baseline` anchor,
  and every report row includes its normalized baseline selector while allowing
  additional exact owner selectors.

- [x] **Step 8: commit evidence intake**

  ```bash
  git add docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: record full-corpus research evidence intake"
  ```

  The Task 2 tracked commit sequence from base
  `8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c` through the evidence commit is
  `ab1dcbae4b0b85a20e6b8c2236249ffa6559ca1f`,
  `ce74dc29c3be4fd5a4198bafd01998881ffdd969`,
  `19c270b17f8b8e303516eea8da68bf852d229e6f`, and
  `802193d33a08423f055615b621fb2667b0a99a1e`. The logical evidence commit is
  complete. At that commit boundary, post-commit packaging and task review were
  not complete; Step 9 records their later closure.

  Two separately owned remediation commits follow the Task 2 evidence commit in
  the shared branch topology:
  `a8fffa6100b3178337cb72deaf56e24c7f14d008` modifies only the Spec 0059
  Task, and `09f7cf1d70f7f533f7323343bad8de02c1ace3f4` modifies only
  `.secrets.baseline`. They are not WRFR-001 implementation evidence and remain
  under their separate reviews and owners.

- [x] **Step 9: review the committed evidence intake**

  Package A is already registered as `task-2-review-package.md`, SHA-256
  `5ab1b0da2e51f8c2ece16a43265e2e3c02633bb969f4fc65d20b6799991867ec`,
  for exact range `8d8c8e56..802193d3`. Its registration produced inventory
  SHA-256 `255628ef76ca95e3dd1b41797bd58089c12fa06fc0a4a764672c683ff3cc46b5`.
  Preserve both identities; do not regenerate or re-register Package A.

  The first Package B attempt used rejected basename
  `task-2-helper-loss-fix-review-package.md` for exact range
  `09f7cf1d..2716ce9f`. The helper created one current-user mode-`0600`
  50,861-byte regular non-symlink with SHA-256
  `84776c9a4343572cb0bb0ef8c6cb634f7d30abbadf42ede1b3ee9799b71795bb`,
  but `artifact-register` returned exactly `ERROR ARTIFACT_CLASS`. The inventory
  remained at the Package A identity, no reviewer consumed the unregistered
  file, and no retry occurred. Before regeneration, the controller used `stat`
  to verify regular-file type, mode `0600`, owner `hy`, and size `50861`,
  confirmed the SHA-256 above, ran `test ! -L`, and proved the exact basename
  absent from inventory. It then ran `rm -f` against the exact absolute path and
  proved that path absent and `residue` PASS. Package A and inventory hashes
  remained unchanged.

  This cleanup did not record device, inode, `mtime_ns`, or `ctime_ns`, did not
  retain a complete FileVersion, and did not unlink through a bound directory
  descriptor. It therefore does not prove same-file continuity between the
  checks and `rm -f`; record that residual limitation without upgrading the
  evidence. No further deletion or retry is authorized by this exception.

  After the tracked artifact-class correction is committed directly on
  `2716ce9f`, create regenerated Package B for only the earlier helper-loss
  amendment and Package C for only this correction. Before each
  `review-package` call, independently apply the guarded canonical-Plan freeze
  and explicit-output preconditions from the global protocol. Then run exactly:

  ```bash
  WRFR_PLAN=docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md
  WRFR_SDD=.superpowers/sdd/0062-workspace-research-full-corpus-reverification-plan
  WRFR_HELPER_LOSS_BASE=09f7cf1d70f7f533f7323343bad8de02c1ace3f4
  WRFR_HELPER_LOSS_HEAD=2716ce9fbbffc2de362839d08314ec33d265a705
  WRFR_CORRECTION_BASE=2716ce9fbbffc2de362839d08314ec33d265a705
  WRFR_CORRECTION_HEAD=$(git rev-parse HEAD)
  WRFR_HELPER_LOSS_REVIEW_OUT="$WRFR_SDD/task-2-fix-1-review-package.md"
  WRFR_CORRECTION_REVIEW_OUT="$WRFR_SDD/task-2-fix-2-review-package.md"
  WRFR_REVIEW_HELPER=/home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.3.0/skills/subagent-driven-development/scripts/review-package
  test "$(git log -1 --format=%s "$WRFR_CORRECTION_HEAD")" = \
    "docs: correct helper review artifact class"
  test "$(git rev-parse "$WRFR_CORRECTION_HEAD^")" = "$WRFR_CORRECTION_BASE"
  test ! -e "$WRFR_SDD/task-2-helper-loss-fix-review-package.md"
  test ! -L "$WRFR_SDD/task-2-helper-loss-fix-review-package.md"
  test ! -e "$WRFR_HELPER_LOSS_REVIEW_OUT"
  test ! -L "$WRFR_HELPER_LOSS_REVIEW_OUT"
  umask 077
  bash "$WRFR_REVIEW_HELPER" \
    "$WRFR_PLAN" "$WRFR_HELPER_LOSS_BASE" "$WRFR_HELPER_LOSS_HEAD" \
    "$WRFR_HELPER_LOSS_REVIEW_OUT"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_HELPER_LOSS_REVIEW_OUT"
  python3 "$WRFR_SDD/full-corpus-check.py" residue \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json"
  test ! -e "$WRFR_CORRECTION_REVIEW_OUT"
  test ! -L "$WRFR_CORRECTION_REVIEW_OUT"
  umask 077
  bash "$WRFR_REVIEW_HELPER" \
    "$WRFR_PLAN" "$WRFR_CORRECTION_BASE" "$WRFR_CORRECTION_HEAD" \
    "$WRFR_CORRECTION_REVIEW_OUT"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_CORRECTION_REVIEW_OUT"
  python3 "$WRFR_SDD/full-corpus-check.py" residue \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json"
  ```

  Both calls must use the canonical Plan and their explicit absent outputs; they
  must not call `sdd-workspace`, omit an output, recreate the alias, or invoke
  `helper-sync`. After each call, postvalidate the unchanged canonical Plan
  version and generated output before its immediate registration and residue
  check. Provide registered Package A, regenerated Package B, and Package C
  together to the same task reviewer. Package B remains exactly
  `09f7cf1d..2716ce9f`; Package C is exactly
  `2716ce9f..WRFR_CORRECTION_HEAD`. Do not widen or conflate either range. The
  separately owned `a8fffa61` Spec 0059 fix and `09f7cf1d` secrets-baseline fix
  remain outside all Task 2 evidence. Resolve WRFR-001 Critical or Important
  findings with a scoped fix commit and a new checker-admitted explicit-output
  re-review before Task 3.

  Completion evidence on 2026-08-21: registered Package A remains
  `task-2-review-package.md`, SHA-256
  `5ab1b0da2e51f8c2ece16a43265e2e3c02633bb969f4fc65d20b6799991867ec`,
  for `8d8c8e56..802193d3`. Regenerated Package B is
  `task-2-fix-1-review-package.md`, SHA-256
  `84776c9a4343572cb0bb0ef8c6cb634f7d30abbadf42ede1b3ee9799b71795bb`,
  for `09f7cf1d..2716ce9f`. Package C is
  `task-2-fix-2-review-package.md`, SHA-256
  `81700dd345b9940c433cd8fb7d6e84a5506109c71547353753f5bec4e8dcfd11`,
  for `2716ce9f..4f25be8b`. The final registered inventory SHA-256 is
  `021421d7341679884fed0976060465a5022c4ba72acc38e19c95cbf52d7038a4`,
  and final `residue` returned `PASS`.

  The same independent Task 2 reviewer consumed registered Packages A, B, and
  C together and returned `APPROVED` with Critical/Important/Minor `0/0/0`,
  explicitly unblocking `WRFR-002`. The final
  `pre-commit run --all-files` rerun exited `0`; every hook passed and reported
  no mutation. WRFR-001 is complete. `WRFR-002` is queued and ready, but no
  WRFR-002 implementation has been executed.

### WRFR-002 one-time allocation-order checker recovery gate

Task 3 dispatch froze base commit
`e8edd3fddb4171aad634ee31a278d136fd3e4529` and registered
`task-3-brief.md` before the integration RED. On 2026-08-21 that first actual
RED returned `ERROR ALLOCATION_REFERENCE`, before any dated owner section was
edited. The registered allocation is not corrupt: its global claim list is
contiguous `CLM-WERPC-013-01..06`, while the closed row map encounters the same
claims in valid request-row order `04,05,01,02,03,06`. The checker incorrectly
required row traversal order to equal global allocation order. The Task 3
implementer was paused and changed no tracked file.

The proposed semantic correction compares exact reference cardinality,
uniqueness, and sorted membership while retaining the existing per-row owner
check. Its real self-test reverses two valid claim-bearing row insertions and
also proves that missing, duplicate, and wrong-owner references still fail.
Because the checker itself is an immutable registered artifact, this repair
invalidates only its old inventory record. `WRFR-002` remains blocked until the
one-time recovery below completes; the frozen baseline, allocation, reports,
review packages, Task 3 brief, and every other inventory record remain
immutable.

The only authorized recovery command is
`artifact-rebind-checker-only`. It has no generic target or report argument. It
accepts only the exact inventory SHA-256, registered old checker SHA-256, and
freshly approved new checker SHA-256; validates the complete inventory schema,
the old checker record, both mutable records, and every other immutable record
against its current complete FileVersion; and replaces only the checker record
at its existing index. It re-reads the checker before and after the inventory
CAS, postvalidates the exact resulting inventory, and attempts rollback to the
exact old inventory bytes only against the CAS-returned FileVersion. Target or
inventory contention, postvalidation failure, and rollback contention all fail
closed. Existing `artifact-register` and the earlier two-record recovery
command remain unchanged.

The first independent Python review of candidate
`71f4b499f1663c2aba2b8e31de5caeeb9b1ef2593dd1f4c95b3e891a43a3fac3`
found an Important post-lock race: the generic CAS helper read its return
FileVersion after releasing the update lock, so a concurrent writer could be
mistaken for the helper's own result and then overwritten by rollback. TDD
reproduced that exact window. The helper now captures and validates its
replacement FileVersion while holding the lock; a post-unlock replacement makes
rollback CAS fail and preserves the concurrent bytes. The earlier Python and
security review results are invalid for the changed bytes.

The revised candidate checker is mode `0600`, current-user owned, 196902 bytes, and
SHA-256
`584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d`.
Normal and optimized self-tests pass all 89 named cases; `py_compile`, Ruff
check, and Ruff format check pass. Fresh independent Python and security
reviewers must approve the exact checker bytes and this tracked contract with
no Critical or Important finding before any stateful invocation. A later byte
change invalidates both approvals and this tuple.

After those approvals and the reviewed three-document contract commit, the
controller may run exactly once:

```bash
WRFR_SDD=.superpowers/sdd/0062-workspace-research-full-corpus-reverification-plan
python3 "$WRFR_SDD/full-corpus-check.py" artifact-rebind-checker-only \
  --workspace "$WRFR_SDD" \
  --inventory "$WRFR_SDD/artifact-inventory.json" \
  --expected-inventory-sha256 \
    79bd0803f575a594a7f7b9ee3dc59a9100c09790668c6cf438866c91ade49f63 \
  --expected-old-checker-sha256 \
    425b2eac6616cbf986960070b38061d76a6584fa4c139748a97d2c6da3d3fc7d \
  --approved-new-checker-sha256 \
    584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d
```

Do not retry. Postvalidate that inventory length and order are unchanged, only
the same-index checker record differs, checker SHA-256 is the approved value,
and `task-2-report.md` remains
`bb5e198e7c99a7c510296d12cf9c7f94eb8af4eed4ea9a6eedec91e085379598`.
Then run `residue`, both self-test modes, and the unchanged Task 3 Step 1 probe.
The expected post-recovery RED is `ERROR INTEGRATION_SECTION`, proving the
allocation was admitted but the four dated owner sections are still absent.
Only that evidence unblocks the paused implementer. No allocation, report,
baseline, task brief, tracked topical owner, remote, or live mutation is part
of this recovery.

### Task 3: WRFR-002 — agent engineering integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/harness-and-loop-engineering.md`
- Modify: `docs/90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md`
- Modify: `docs/90.references/research/2026-08-08-wer/agent-model-routing-and-configuration.md`
- Modify: `docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: immutable `research-agent-engineering.json` and only its exact
  `allocation.json` slice for request IDs `001`, `002`, and `026..032`.
- Produces: reviewed 2026-08-20 sections for harness, loop, agency-agents, model
  routing, and memory without writing the shared source/claim ledger.

- [x] **Step 1: pass the checker-recovery gate and reproduce the missing-section RED**

  Complete the separately reviewed one-time checker-only inventory recovery
  above. Then use the same read-only probe that requires the exact dated H3 in
  all four owner files and the exact nine request IDs in the report. Expected
  before owner edits: `ERROR INTEGRATION_SECTION` and exit 1. The earlier
  `ERROR ALLOCATION_REFERENCE` is the recorded checker defect and is not the
  accepted Task 3 RED.

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . \
    --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" \
    --workstream agent-engineering
  ```

  The original pre-recovery run exited `1` with
  `ERROR ALLOCATION_REFERENCE`. After reviewed checker-only recovery, the same
  fail-fast probe exited `1` with `ERROR INTEGRATION_SECTION`, before any owner
  edit. The checker reports the first failing section, so the accepted RED is
  one exact diagnostic rather than the four diagnostics stated in the frozen
  Task 3 brief.

- [x] **Step 2: append the agent-engineering findings**

  Under the existing review/freshness owner in each file, append exactly one
  `### 2026-08-20 full-corpus reverification` section. Use the allocation map's
  final IDs verbatim. Cover these exact topics:

  - `REQ-WERPC-001`: harness components, role/tool/permission/evidence contracts,
    orchestration, isolation, checkpoints, recovery, observability, and cost;
  - `REQ-WERPC-002`: loop states, termination, retry budgets, no-progress
    detection, escalation, handoff, and deterministic replay;
  - `REQ-WERPC-026` and `027`: general agent systems and the current
    `msitarzewski/agency-agents` repository contract, separated from local
    adoption;
  - `REQ-WERPC-028`: task-to-model/provider/effort/tool mapping and fitness
    evidence without runtime promotion;
  - `REQ-WERPC-029..032`: long-term, short-term, domain, checkpoint, retention,
    provenance, compaction, deletion, and provider-native memory boundaries.

  Every owner section records source identities, workspace selectors, As-Is,
  Gap, Target, evidence depth, rejected inference, retained DEFER, owner, safe
  follow-up, and trigger. Do not duplicate unchanged baseline prose.

  Exactly one dated H3 was appended to each of the four owners. The nine rows
  use their existing source identities because the allocation slice contains
  no new source or claim ID. All external results remain `unchanged`, all
  workspace results remain `confirmed`, and provider-runtime evidence remains
  `DEFER` for rows `001`, `002`, `026`, `028`, and `032`.

- [x] **Step 3: run agent-focused GREEN checks**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream agent-engineering
  python3 scripts/validate-agent-harness-contract.py --root .
  python3 scripts/validate-agent-loop-lifecycle.py --root .
  python3 scripts/validate-agent-roster-currentness.py .
  python3 scripts/validate-agent-evaluations.py --root .
  python3 scripts/validate-agent-model-fitness.py --root .
  python3 scripts/validate-agent-checkpoint.py --root .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Expected: the task-local probe reports nine integrated rows and every canonical
  agent validator passes while runtime/fitness/promotion remains explicitly
  `DEFER` where the owner contract says so.

  The task-local probe passed for all nine rows. The harness, loop, roster,
  evaluation, model-fitness, and checkpoint validators passed; strict Markdown
  reported zero violations; strict links/owners passed; and `git diff --check`
  passed. These are repository-static results only.

- [x] **Step 4: commit and review agent findings**

  Update Task/Plan/progress and commit only the seven named tracked files:

  ```bash
  git add docs/90.references/research/2026-08-08-wer/harness-and-loop-engineering.md \
    docs/90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md \
    docs/90.references/research/2026-08-08-wer/agent-model-routing-and-configuration.md \
    docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify agent engineering research"
  ```

  Generate the committed package, then dispatch one source-fidelity reviewer
  and one task reviewer. Resolve Critical or Important findings in a scoped fix
  commit and re-review before Task 4.

  Before staging, an independent source-fidelity/content reviewer and an
  independent spec-compliance/quality reviewer both returned `APPROVED` with
  Critical/Important/Minor `0/0/0`. The first affected lane selected and passed
  every agent and document validator, then failed only at the aggregate's
  expected `CLOSURE-WORKTREE-INDEX-DRIFT` because the seven-file logical unit
  was not yet staged. Stage exactly those seven files, replay affected, then
  run staged, plain pre-commit, all-files, formatter review, and diff checks.

  Commit `06b3d681b11e0a373afcbe6bc86031dba615f590` contains exactly the
  seven named paths. Registered report SHA-256 is
  `9f589540cadf2893133d5a04b8fa8ee5b34747980117e4889fe98eaf9f1843ce`;
  registered review-package SHA-256 is
  `3fb6e7af4e5073e9ddde872c152a5332366763398654ca0eee15a1bf9e61f535`
  for exact range `e8edd3fddb4171aad634ee31a278d136fd3e4529..06b3d681b11e0a373afcbe6bc86031dba615f590`;
  final inventory SHA-256 is
  `ec9863801083b29107e438a92998b40d121eca2183d6834cbfa3a5621b76fcfa`.
  The post-commit reviewer returned `APPROVED WITH MINOR`,
  Critical/Important/Minor `0/0/1`, and explicitly allowed WRFR-003 to
  unblock. The sole Minor was stale Task-table evidence that still said the
  commit/package review was pending; this closure unit corrects that evidence.
  WRFR-002 is complete and WRFR-003 is queued and ready, not executed.

### Task 4: WRFR-003 — provider and common-environment integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/workspace-governance-and-common-agent-environment.md`
- Modify: `docs/90.references/research/2026-08-08-wer/provider-implementation-status.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: immutable `research-provider-common.json` and its allocation slice
  for request IDs `003..006`.
- Produces: reviewed common-environment and Claude/Codex status sections with
  repository-static versus provider-native evidence separated.

- [x] **Step 1: reproduce the two-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream provider-common
  ```

  Expected before edits: two missing-section diagnostics and exit 1.

  The unchanged pre-edit probe exited `1` with
  `ERROR INTEGRATION_SECTION`. The checker is fail-fast and therefore reports
  the first missing owner section rather than both missing sections in one run.

- [x] **Step 2: append the provider/common findings**

  Add one dated H3 to each owner. Cover `REQ-WERPC-003..006` exactly:

  - the workspace governance chain, shared contract, environment, permission,
    tool, checkpoint, evaluation, and evidence rules;
  - Claude's current official agent, subagent, settings, permissions, hooks,
    memory, model, and context contracts;
  - Codex's current official AGENTS, config, subagent, sandbox, approval, hooks,
    memory, model, and MCP contracts;
  - the shared provider-neutral projection and the provider-specific capabilities
    that cannot be normalized without losing meaning.

  Record tracked configuration separately from native discovery, installation,
  authentication, entitlement, and execution. No local installation or provider
  runtime fact may be inferred from an official product page.

  Exactly one dated H3 was appended to each of the two owners. The four rows
  consume no new source or claim identifier, retain their normalized baseline
  selectors, and record As-Is, Gap, Target, evidence depth, rejected inference,
  retained `DEFER`, owner, safe follow-up, and refresh trigger. The Claude
  changelog advance remains public-documentation evidence only; the failed
  Codex MCP re-fetch supports no new current MCP-specific claim.

- [x] **Step 3: run provider-focused GREEN checks**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream provider-common
  python3 scripts/validate-agent-provider-config.py --root .
  python3 scripts/validate-agent-provider-evidence.py --root .
  python3 scripts/validate-agent-roster-admission.py --root .
  python3 scripts/validate-agent-roster-currentness.py .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  The task-local probe passed all four rows. Provider config/evidence and both
  roster validators passed; strict Markdown reported zero violations; strict
  links/owners passed; and `git diff --check` passed. These results establish
  repository-static integration only.

- [x] **Step 4: commit and review provider findings**

  Update Task/Plan/progress and commit only the five named tracked files:

  ```bash
  git add docs/90.references/research/2026-08-08-wer/workspace-governance-and-common-agent-environment.md \
    docs/90.references/research/2026-08-08-wer/provider-implementation-status.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify provider and common environment research"
  ```

  Generate the committed package, dispatch source-fidelity and task reviews,
  and resolve Critical or Important findings in a scoped fix commit followed by
  re-review before Task 5.

  The first independent source-fidelity review found one Important omission:
  the Codex row consumed the existing memory observation without listing
  `SRC-WERPC-068` in its source boundary. The owner now lists
  `SRC-WERPC-009..013` and `SRC-WERPC-068`. Covering checks passed, and the
  independent source-fidelity re-review and spec/quality/security review both
  returned `APPROVED` with Critical/Important/Minor `0/0/0`.

  Commit `a41def9e570ed798c87d6a17adb766df394f4768` contains exactly the five
  named paths. Registered report SHA-256 is
  `39c9bdcd9710d66ea57c06e5404da326f07d8424423e85900d559fba60ddc996`;
  registered review-package SHA-256 is
  `889801d930e7e25e5beb828fea743e6a9ccb652ecc6ae0f979c474dc924d74d7`
  for exact range
  `8cd4721f06943f16302ada0c993187c9328d503b..a41def9e570ed798c87d6a17adb766df394f4768`;
  final inventory SHA-256 is
  `e949e9f191b8153486e1f2d43c9f903f65df583cb5f436ef91dd0a60a3bb3cce`.
  The post-commit reviewer returned `APPROVED WITH MINOR`,
  Critical/Important/Minor `0/0/1`, and explicitly allowed WRFR-004 to
  unblock. The sole Minor was stale Task evidence that still described
  settlement and review as pending; this closure unit corrects it. WRFR-003 is
  complete and WRFR-004 is queued and ready, not executed.

### Task 5: WRFR-004 — SDLC and documentation integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md`
- Modify: `docs/90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md`
- Modify: `docs/90.references/research/2026-08-08-wer/llm-wiki-and-knowledge-routing.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: immutable `research-sdlc-documentation.json` and its allocation
  slice for request IDs `007`, `010..021`, and `034..036`.
- Produces: reviewed Spec-driven, document-family, Diataxis, and LLM-WIKI
  sections without inventing a universal document standard.

- [x] **Step 1: reproduce the three-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream sdlc-documentation
  ```

  Expected before edits: three missing-section diagnostics and exit 1.

  The actual pre-edit probe exited `1` with exactly
  `ERROR INTEGRATION_SECTION`. The checker is fail-fast and reports only the
  first missing owner rather than three simultaneous diagnostics.

- [x] **Step 2: append the SDLC and document-family findings**

  Add one dated H3 to each owner and cover all sixteen assigned rows:

  - Spec-driven development and lifecycle gates;
  - the six development document families assigned to
    `REQ-WERPC-010..015`, including roles, inputs, outputs, approval,
    traceability, failure meaning, and evidence;
  - Guide, Incident, Postmortem, Policy, Release, and Runbook roles, operations
    lifecycle, rehearsal, review, release identity, rollback, and learning;
  - Diataxis's tutorial, how-to, reference, and explanation purposes, including
    the local decision not to create empty families;
  - LLM-WIKI ingestion, source provenance, routing, currentness, retrieval,
    generated-index, MCP, publication, and validation boundaries.

  Preserve the explicit `Verified gap` for the absent Release family unless new
  canonical workspace evidence changes it. Public ISO catalog evidence supports
  edition/status/scope only. NASA, NIST, Google SRE, Diataxis, and vendor guidance
  are benchmarks, not compliance claims or universal local formats.

  Exactly one dated H3 was appended immediately before terminal
  `## Related Documents` in each existing owner. All sixteen rows are present.
  `REQ-WERPC-011..013` use only `CLM-WERPC-013-01..03` for additive
  current-form AD corrections; no source, request owner, report, or research
  folder was created. Release, Diataxis, and LLM-WIKI deeper-evidence
  boundaries remain fail-closed. Independent source-fidelity and
  spec/quality/security reviews both returned `APPROVED` with
  Critical/Important/Minor `0/0/0`.

- [x] **Step 3: run documentation-focused GREEN checks**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream sdlc-documentation
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-active-corpus-role-audit.py --root .
  python3 scripts/validate-reference-information-architecture.py --self-test
  bash scripts/generate-llm-wiki-index.sh --check
  git diff --check
  ```

  The first strict-links run exposed that two required append targets were
  complete-blob-pinned historical alias sources. Separate reviewed commits
  `bdd36f09` and `42222c33` changed only the validator/test authority and its
  Spec 0062 expectation; they remain outside this six-file work unit. After
  Python and security approval, the full focused sequence was rerun at
  `42222c33`: every command passed, including `PASS CROSS-DOCUMENT` and the
  LLM-WIKI generator check. The latter proves only deterministic output against
  declared inputs.

- [x] **Step 4: commit and review SDLC findings**

  Update Task/Plan/progress and commit only the six named tracked files:

  ```bash
  git add docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md \
    docs/90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md \
    docs/90.references/research/2026-08-08-wer/llm-wiki-and-knowledge-routing.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify SDLC and documentation research"
  ```

  Generate the committed package, dispatch source-fidelity and task reviews,
  and resolve Critical or Important findings in a scoped fix commit followed by
  re-review before Task 6.

  Commit `7bbe6517a014cbc3e79c896d5097a3ae8b99a283` contains exactly the six
  named paths. It follows the separately reviewed prerequisite commits
  `bdd36f09` and `42222c33`. Registered report SHA-256 is
  `c7749874d884d0cd4af617537cd583eb11432ff0ffd537b68212248a84845918`;
  registered review-package SHA-256 is
  `b996e1022dd709d3a0b70d21df9c58ef9d29c1122810041b377d90aca9cb709e`
  for exact three-commit range
  `615c3a87..7bbe6517`. Final inventory SHA-256 is
  `0d60d1d3602fc357bbabe382dd4ede0bfedaba640e2742d367de021fed5936c0`.
  The post-commit reviewer returned `APPROVED WITH MINOR`,
  Critical/Important/Minor `0/0/1`, and allowed WRFR-005 to unblock. The sole
  Minor was stale lifecycle evidence that still described settlement and
  review as pending; this closure unit corrects it. WRFR-004 is complete and
  WRFR-005 is queued and ready, not executed.

### Task 6: WRFR-005 — platform and security integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: immutable `research-platform-security.json` and its allocation slice
  for request IDs `008`, `009`, and `025`.
- Produces: one reviewed Kubernetes/infrastructure/security section with live
  cluster and secret boundaries preserved.

- [x] **Step 1: reproduce the platform-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream platform-security
  ```

  Expected before edits: one missing-section diagnostic and exit 1.

  The pre-edit probe exited `1` with exactly `ERROR INTEGRATION_SECTION`.
  The checker is fail-fast and reported the one missing platform owner before
  any owner or lifecycle edit.

- [x] **Step 2: append the platform and security findings**

  The dated H3 must distinguish Kubernetes desired state, infrastructure
  scripts/contracts, and security controls. Reverify RBAC least privilege,
  Secret API exposure, service-account tokens, workload hardening, NetworkPolicy,
  admission, GitOps revision identity, Helm provenance, image digests, signatures,
  attestations, SLSA provenance, Vault/ESO identity, and recovery evidence.

  Compare official sources with exact repository selectors. Do not run `kubectl`,
  `k3d`, `helm`, `argocd`, `vault`, `docker`, a registry client, or any live
  infrastructure command. Never inspect a Secret value.

  Exactly one dated H3 was appended immediately before terminal Related
  Documents in the existing owner. It contains the exact three-row slice,
  `SRC-WERPC-091`, and `CLM-WERPC-013-04..06`, and separates Kubernetes
  desired state, infrastructure execution contracts, and security controls.
  Effective RBAC, admission, CNI, Argo reconciliation, Vault/ESO, artifact
  trust, registry, recovery, and runtime results remain `DEFER`. Independent
  source-fidelity, spec/quality, and security reviews returned `APPROVED` with
  Critical/Important/Minor `0/0/0` each.

- [x] **Step 3: run platform-focused GREEN checks**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream platform-security
  bash scripts/validate-gitops-structure.sh
  bash infrastructure/tests/verify-contracts-static.sh
  bash scripts/validate-k8s-manifests.sh .
  python3 scripts/validate-vault-eso-contracts.py --root .
  bash scripts/check-secret-handling.sh .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  If any named script has moved, locate its current canonical successor through
  the affected-surface registry and record the exact replacement in the Task;
  do not silently drop the check.

  Every named script remained at its canonical path. The integration probe,
  GitOps structure, static infrastructure contracts, 106-manifest syntax and
  kube-linter lane, Vault/ESO contracts, secret handling, strict Markdown,
  strict links/owners, and diff check all passed. These are repository-static
  results only; no prohibited live or secret-bearing command was invoked.

- [x] **Step 4: commit platform findings**

  ```bash
  git add docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify platform and security research"
  ```

  Commit `63efc8de90227e1d3c32e2c4388876d4b850a94b` contains exactly the four
  named paths. It preserves every `Partial`, `live-cluster`, Secret-value, and
  no-live-command boundary recorded by the approved pre-commit reviews.

- [x] **Step 5: review the committed platform findings**

  Generate the committed package and dispatch source-fidelity, task, and
  `security-reviewer` reviews. The security review must verify no secret payload,
  live command, identity mutation, unbounded permission claim, or supply-chain
  equivalence entered the report. Resolve every Critical or Important finding
  in a scoped fix commit and re-review before Task 7.

  Registered report SHA-256 is
  `dfe45681c38ec2312936315a465f8069b6f6d1474afda5f6a86d7e34f5804e78`;
  registered review-package SHA-256 is
  `88111b614c7bda7305cf0d2686d57bda598106c2e66a4bce38333ba32c5682c0`
  for exact one-commit range `8ed7fae3..63efc8de`. Final inventory SHA-256 is
  `d844156bdfe0dab8ab90009e89ad7807aab6987571955aa8a2783f4784047f24`.
  The post-commit reviewer returned `APPROVED WITH MINOR`,
  Critical/Important/Minor `0/0/1`. Its sole Minor was the intentional
  pre-closure lifecycle state in these three records; this closure corrects
  it. WRFR-005 is complete. WRFR-006 passed its pre-remote security review,
  both fixed local recoveries, the untouched `artifacts` query, nine-class
  remote validation, owner integration, and its delivery-focused GREEN checks.
  Its exact implementation commit, registered report/package, and post-commit
  review are complete. The sole intentional pre-closure lifecycle Minor is
  corrected in this closure; WRFR-007 is queued and ready.

### Task 7: WRFR-006 — delivery and quality integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/ci-cd-github-actions-and-qa.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Create in ignored SDD workspace: `remote-github-summary.json`

**Interfaces:**

- Consumes: immutable `research-delivery-quality.json`, its allocation slice for
  request IDs `022`, `023`, `024`, and `033`, and a pre-remote security approval.
- Produces: one CI/CD, GitHub Actions, QA, and V&V section plus one guarded,
  sanitized nine-class remote summary.

- [x] **Step 1: obtain pre-remote security approval**

  Before any `gh` or GitHub API command, dispatch `security-reviewer` with the
  exact repository, branch, the two preflight argv vectors from Step 3, the nine
  evidence-query argv vectors from Step 4, every projected field, stdout/stderr
  treatment, timeout, one-query-per-class budget, guarded output contract, and
  no-retry rule. The reviewer must approve both preflight output minimization and
  the checker's per-class documented-unavailable path. Stop remote evidence
  collection if that review reports an unresolved Critical or Important issue.

- [x] **Step 2: reproduce local and remote RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream delivery-quality
  python3 "$WRFR_SDD/full-corpus-check.py" remote-validate \
    --summary "$WRFR_SDD/remote-github-summary.json"
  ```

  Expected before edits/initialization: one missing-section diagnostic and one
  missing guarded summary diagnostic.

- [x] **Step 3: initialize and verify the remote target**

  ```bash
  gh auth status --hostname github.com
  gh repo view buenhyden/hy-home.k8s --json nameWithOwner,url,defaultBranchRef
  python3 "$WRFR_SDD/full-corpus-check.py" remote-init \
    --root . --output "$WRFR_SDD/remote-github-summary.json"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_SDD/remote-github-summary.json"
  ```

  Continue only when the projected identity is exactly
  `buenhyden/hy-home.k8s`, the URL is the GitHub HTTPS repository URL, and the
  default branch is `main`. Authentication output is not copied into evidence.

- [x] **Step 4: run each approved remote query once**

  Invoke every query through `remote-query`; the checker verifies the argv,
  applies a bounded timeout, projects only the named fields, and performs a
  version-bound atomic update. The exact evidence classes and argv are:

  Current execution consumed all nine budgets in order. `workflows` and `oidc`
  were each converted only through their fixed reviewed local recovery;
  `runs` through `environments` and then the untouched `artifacts` class were
  observed exactly once. No preflight or evidence class was retried.

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" --class workflows -- \
    gh workflow list --repo buenhyden/hy-home.k8s --all \
    --json id,name,path,state
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" --class runs -- \
    gh run list --repo buenhyden/hy-home.k8s --limit 20 \
    --json databaseId,workflowName,headSha,status,conclusion,createdAt,updatedAt,event
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" \
    --class actions-permissions -- gh api \
    repos/buenhyden/hy-home.k8s/actions/permissions \
    --jq '{enabled,allowed_actions,selected_actions_url}'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" \
    --class workflow-permissions -- gh api \
    repos/buenhyden/hy-home.k8s/actions/permissions/workflow \
    --jq '{default_workflow_permissions,can_approve_pull_request_reviews}'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" --class rulesets -- gh api \
    'repos/buenhyden/hy-home.k8s/rulesets?includes_parents=false' --paginate \
    --jq '[.[]|{id,name,enforcement,target,source_type}]'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" \
    --class branch-protection -- gh api \
    repos/buenhyden/hy-home.k8s/branches/main/protection \
    --jq '{required_status_checks:{strict:.required_status_checks.strict,contexts:.required_status_checks.contexts,checks:.required_status_checks.checks},enforce_admins:.enforce_admins.enabled,required_pull_request_reviews:{required_approving_review_count:.required_pull_request_reviews.required_approving_review_count,dismiss_stale_reviews:.required_pull_request_reviews.dismiss_stale_reviews}}'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" \
    --class environments -- gh api \
    repos/buenhyden/hy-home.k8s/environments \
    --jq '{total_count,environments:[.environments[]|{name,protection_rules:[.protection_rules[].type],deployment_branch_policy}]}'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" --class oidc -- gh api \
    repos/buenhyden/hy-home.k8s/actions/oidc/customization/sub \
    --jq '{use_default,include_claim_keys}'
  python3 "$WRFR_SDD/full-corpus-check.py" remote-query --root . \
    --summary "$WRFR_SDD/remote-github-summary.json" \
    --class artifacts -- gh api \
    'repos/buenhyden/hy-home.k8s/actions/artifacts?per_page=100' \
    --jq '{total_count,artifacts:[.artifacts[]|{id,name,size_in_bytes,expired,created_at,expires_at,workflow_run:{id,head_sha}}]}'
  ```

  Execute the nine commands above in their listed order. The quoted URL and jq
  arguments are part of the executable contract and prevent shell globbing or
  brace expansion from changing the approved argv.

  For each class independently, `remote-query` either appends the approved
  sanitized projection or, on an allowlisted documented 403/404 or a
  checker-supported nullable response, appends a fixed `unavailable` record for
  that same class with empty identities, bounded reason code, and fresh UTC.
  Multiple classes may therefore be unavailable without a retry or a second
  network path. Any other nonzero exit, schema mismatch, extra field, or raw
  output condition stops the workstream; it is not converted to unavailable.

#### WRFR-006 remote incident and fixed recovery gate

The pre-remote security review returned `Approved With Minor`, with
Critical/Important/Minor `0/0/1`; the bounded 403/404 recognition was the sole
Minor and did not block execution. The controller then ran each approved
preflight exactly once. `gh auth status --hostname github.com` succeeded, and
the projected repository identity from the second preflight was exactly
`buenhyden/hy-home.k8s`, the GitHub HTTPS URL, and default branch `main`.
Authentication output was discarded. The local integration RED was exactly
`ERROR INTEGRATION_SECTION`; the pre-initialization remote RED was exactly
`ERROR PATH_INVALID`.

The remote summary was initialized and registered. The first and only
`workflows` query then exited with `ERROR REMOTE_COMMAND`. The registered
summary contains only the sanitized state `failed`, reason
`non-allowlisted-failure`, and an empty data object for that class. The bounded
checker captured and classified stdout/stderr in memory, but raw output was not
exposed to the controller or a human, copied into evidence, or persisted. No
retry, fallback, alternate endpoint, or second preflight was attempted, and the
remaining eight classes have not been invoked. The frozen incident identities
are:

- checker SHA-256
  `584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d`;
- summary SHA-256
  `cc77a8ae007b71f32328ce159dd03f60d3a32390131710cb6eee675bdbee4b56`;
- inventory SHA-256
  `1dc24b116bbd09cb8e36f96a0bfb6c332dac8793f15b3cf33cc858efd8c9c22b`.

The child process received the checker's minimal locale and executable search
environment but no authenticated GitHub configuration or state location. It
therefore created repository-local `.local/state/gh/device-id`; its 36 bytes
were not directly inspected by the controller or checker. The exact metadata-only residue contract, with nanosecond times
and no atime, is:

| Path | Device | Inode | Size | `mtime_ns` / `ctime_ns` | Mode | UID | Exact entries |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `.local` | 2096 | 1747675 | 4096 | 1787287593754570540 | `0755` | 1000 | `state` |
| `.local/state` | 2096 | 2221665 | 4096 | 1787287593754570540 | `0755` | 1000 | `gh` |
| `.local/state/gh` | 2096 | 3263846 | 4096 | 1787287593754570540 | `0755` | 1000 | `device-id` |
| `.local/state/gh/device-id` | 2096 | 3276459 | 36 | 1787287593754570540 | `0600` | 1000 | regular file; not directly inspected by controller/checker |

At this first incident checkpoint, WRFR-006 was `In Progress` and blocked. No
delivery owner edit or remaining remote query could proceed until the following
material recovery sequence completed in order:

1. Commit this three-document incident contract before modifying the ignored
   checker or any stateful artifact.
2. Extend the checker test-first with the fixed
   `artifact-rebind-checker-only`, `remove-owned-gh-state-residue`, and
   `remote-recover-auth-context` interfaces and transactional registered-summary
   updates. Run compile, normal and optimized self-tests, Ruff checks, and fresh
   independent Python and security direct review over the exact bytes. Any
   Critical or Important finding, later byte change, or incomplete rollback
   test keeps the gate closed.
3. Invoke `artifact-rebind-checker-only` exactly once against the incident
   inventory/checker tuple above and the newly approved checker SHA-256. It may
   change only the same-index checker record. Do not retry.
4. Invoke `remove-owned-gh-state-residue --root .` exactly once. The command has
   no generic target. It opens the repository and each literal component with
   directory file descriptors and `O_NOFOLLOW`, binds every row above by
   `(device,inode,size,mtime_ns,ctime_ns,mode,uid)`, checks the exact entry set,
   revalidates with `fstat`, unlinks only `device-id`, removes only the three now
   empty directories, and proves `.local` absent afterward. Any mismatch,
   symlink, new entry, non-empty directory, or contention stops without broader
   deletion. The same-UID actor race between final validation and unlink/rmdir
   is a documented platform limitation; dirfd binding, exact entry checks, and
   post-absence proof bound but cannot eliminate it.
   Precondition failure guarantees no mutation, but unlink plus three `rmdir`
   operations are not one POSIX atomic action. A failure after unlink may leave
   a monotonic partial cleanup; the checker must return fixed
   `CLEANUP_PARTIAL`, must not retry, and must never call that state success.
   Success requires the complete absence of `.local`.
5. Invoke `remote-recover-auth-context` exactly once with the then-current exact
   inventory and incident summary hashes. It performs no network process,
   preserves the existing `observedAt`, and replaces only the existing
   `workflows` state with fixed `unavailable`, reason
   `checker-auth-context-incompatible`, and empty data. It must update the
   registered summary and its same-index inventory record as a compensating
   two-file transaction: validate and lock both identities, retain both old raw
   byte sequences and FileVersions, CAS the summary, CAS the inventory, and
   postvalidate both. Summary-only rollback is allowed only when the inventory
   CAS demonstrably did not commit. If inventory CAS committed and later
   postvalidation fails, compensate the inventory first against the exact
   FileVersion returned by its CAS, then compensate the summary against its
   exact returned FileVersion, and postvalidate the restored old pair.
   Because two-file atomic replacement is unavailable, rollback contention or
   failure is a distinct fail-closed incident and never a consistency claim.
6. Prove `.local` absent before and after every remaining query, do not repeat
   either preflight or `workflows`, and invoke `runs`, `actions-permissions`,
   `workflow-permissions`, `rulesets`, `branch-protection`, `environments`,
   `oidc`, and `artifacts` once each in the existing listed order. Stop on the
   first non-allowlisted failure; do not consume later budgets.

For each recovery or remaining-query child, construct a fresh environment from
the existing minimal `PATH`, `LC_ALL`, and `LANG`, the fixed
`GH_CONFIG_DIR=/home/hy/.config/gh` and
`XDG_STATE_HOME=/home/hy/.local/state`, and only these fixed non-secret controls:
`GH_PROMPT_DISABLED=1`, `GH_PAGER=/usr/bin/cat`,
`GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1`, `NO_COLOR=1`,
and `GIT_TERMINAL_PROMPT=0`. Do not inherit or inject `HOME`, token variables,
`GH_HOST`, `GH_REPO`, `GH_DEBUG`, `LD_*`, proxy variables, `PAGER`,
`XDG_CONFIG_HOME`, or any other credential/configuration variable. Walk
both absolute paths component-by-component without following symlinks and bind
all relevant objects before and after the child by the same metadata identity.
The controller and checker must never directly read, hash, copy, print, or
persist configuration/state contents. Only the approved `/usr/bin/gh` child may
consume those standard-path bytes for authentication/state operation, and it
must not expose them through raw output or evidence. The
fixed `/home/hy/...` spellings are part of the allowlist; `Path.resolve()` or
another string-only canonicalization is not a substitute for the dirfd walk.
Snapshot `/` and `/home` as trusted system directories: user-namespace UID
`65534` is permitted there, but they must be non-symlinks, not group/world
writable, not writable by the current process, and stable by retained-dirfd
`(device,inode,mode,uid)` before and after. From `/home/hy` downward every
component must instead be current-UID-owned, non-symlink, non-group/world
writable, and stable by its retained dirfd; owner-write permission is allowed
on these user-owned leaves. Any ancestor mismatch closes the gate. The
current metadata-only snapshot that a reviewed execution must either match or
replace through a new tracked amendment is:

| Object | Device | Inode | Size | `mtime_ns` / `ctime_ns` | Mode | UID | Constraint |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `/home/hy/.config/gh` | 2096 | 77048 | 4096 | 1771840087477040631 | `0751` | 1000 | entries exactly `config.yml`, `hosts.yml` |
| `/home/hy/.config/gh/hosts.yml` | 2096 | 83227 | 210 | 1784175379048299565 | `0600` | 1000 | required regular file; not directly inspected by controller/checker |
| `/home/hy/.config/gh/config.yml` | 2096 | 83791 | 1660 | 1771840087477040631 | `0600` | 1000 | regular file; not directly inspected by controller/checker |
| `/home/hy/.local/state/gh` | 2096 | 11400 | 4096 | 1778049370412048559 | `0755` | 1000 | entries exactly `device-id` |
| `/home/hy/.local/state/gh/device-id` | 2096 | 11405 | 36 | 1778049370412048559 | `0600` | 1000 | required regular file; not directly inspected by controller/checker |

The checker may support a metadata snapshot in which `config.yml` is absent,
but only when both pre- and post-checks return `ENOENT`; a dangling symlink,
appearance during execution, or any other transition fails closed. `hosts.yml`
and the host state `device-id` remain required, current-user-owned, regular,
mode `0600`, and bounded. Every summary mutation, including each remaining
query, uses the same transactional summary/inventory CAS and compensating
rollback contract. The unavoidable same-UID mutation window remains explicit;
metadata stability is not proof that secret contents were inspected or valid.
Any compensation drift, contention, or failure is a distinct fail-closed
registered-pair inconsistency and never a rollback-success claim.

#### WRFR-006 OIDC schema incident and fixed recovery gate

The first recovery gate completed in its prescribed order. The exact-byte
checker reviews approved the revised checker, its checker-only inventory rebind
completed, the repository `.local` residue was removed exactly once,
`remote-recover-auth-context` performed only the fixed local `workflows`
transition, and `.local` absence plus `residue` passed. No preflight or
`workflows` retry occurred. The delivery integrator then invoked `runs`,
`actions-permissions`, `workflow-permissions`, `rulesets`,
`branch-protection`, and `environments` exactly once each, in order, and the
registered summary retained their sanitized observations.

The sole `oidc` invocation returned `ERROR REMOTE_SCHEMA`. The registered OIDC
record is exactly state `failed`, reason `schema-invalid`, and empty data. The
checker captured and classified raw output in process memory but did not expose
it to the controller or a human, copy it, or persist it. The raw response is no
longer available. No retry, fallback, alternate endpoint, later query, or
preflight occurred; `artifacts` remains absent from the summary. The fixed
second-incident identities are:

- checker SHA-256
  `31a14c46f18bdaa690360f67d263ad78aa440a8345d76c9160c150ba1b4f56a3`;
- summary SHA-256
  `6255a3734325aab127e81b5730a121c9bf97c38b0611d91c21b9c6f1f7dc9ee2`;
- inventory SHA-256
  `008be406a418348269cf5c58c3becf9cac024ba1db6adf1f430e0d9ae5fd927e`.

GitHub's primary
[OIDC REST documentation](https://docs.github.com/en/rest/actions/oidc)
defines `use_default` as boolean and `include_claim_keys` as optional and
ignored when `use_default` is true. A nullable or absent projected claim-key
value is therefore plausible, but the lost raw response prevents a factual
finding about what this invocation returned. The root cause remains unproven;
the recovery is a checker-compatibility disposition, not a remote-state claim.
The fixed jq object always emits the `include_claim_keys` key, so an absent raw
field becomes post-projection `null`; a post-projection object missing that key
remains invalid.

The checker must expose only this fixed interface, with no caller-selected
class or reason:

```text
remote-recover-oidc-schema --workspace DIR --inventory FILE --summary FILE \
  --expected-inventory-sha256 OLD --expected-summary-sha256 OLD
```

At this second incident checkpoint, WRFR-006 remained `In Progress` and
blocked. Continuation was limited to this exact sequence:

1. Commit this second three-document incident amendment while the checker,
   summary, inventory, `.local` absence, and credential/state paths remain
   untouched.
2. Add failing tests first for the OIDC projection rule and fixed recovery.
   The projection validator may accept `include_claim_keys: null` only when
   `use_default` is exactly `true`; false, missing/invalid `use_default`, or any
   other invalid type remains `ERROR REMOTE_SCHEMA`. Implement the minimal
   validator change and `remote-recover-oidc-schema`, then run compile, normal
   and optimized self-tests, and Ruff. Obtain fresh independent Python and
   security approvals over the exact checker bytes; any Critical or Important
   finding or later byte change blocks stateful execution.
3. Invoke `artifact-rebind-checker-only` exactly once with old checker
   `31a14c46f18bdaa690360f67d263ad78aa440a8345d76c9160c150ba1b4f56a3`,
   old inventory
   `008be406a418348269cf5c58c3becf9cac024ba1db6adf1f430e0d9ae5fd927e`,
   and the newly approved checker SHA-256. Only the checker's existing inventory
   record may change. Do not retry.
4. Invoke `remote-recover-oidc-schema` exactly once with old summary
   `6255a3734325aab127e81b5730a121c9bf97c38b0611d91c21b9c6f1f7dc9ee2`
   and the then-current exact inventory SHA-256. The command performs no
   network or child-process action. It requires the exact repository identity,
   exactly the logical first-eight class membership, no `artifacts` record, the
   first seven records unchanged, and OIDC exactly `failed` / `schema-invalid`
   / `{}`. The query-budget order remains the Plan command sequence, while the
   persisted JSON class map must use the canonical lexicographic order emitted
   by `_json_bytes(sort_keys=True)`, namely
   `tuple(sorted(REMOTE_CLASSES[:8]))`; map order is not evidence of invocation
   order. It preserves every pre-OIDC record, the OIDC `observedAt`, repository
   identity, canonical persisted class-map order, and `artifacts` absence; it
   changes only OIDC to
   `unavailable` / `checker-oidc-schema-incompatible` / `{}`.
5. The recovery uses the existing registered-summary/inventory compensating CAS
   contract without weakening identity checks, commit ordering, rollback
   ordering, or postvalidation. Any mismatch, contention, compensation failure,
   or unexpected class/data change is fail-closed and consumes no network
   budget.
6. Prove `.local` absent and run `residue`. Then, and only then, invoke the
   untouched `artifacts` query once through the already approved command and
   child environment. Prove `.local` absent again, run `residue`, and execute
   `remote-validate`. Do not invoke either preflight or any of the first eight
   classes again.

This second gate superseded only the first gate's then-current handoff and
preserves the first incident and recovery as historical evidence. It completed
on 2026-08-22: exact-byte checker review and checker-only rebind passed, the
fixed no-network OIDC recovery preserved the bounded unavailable disposition,
`.local` absence and residue passed, `artifacts` ran exactly once, and the final
nine-class summary SHA-256 is
`da137936a4ec5cbb10c06303b96e22cc933188fec7042b8aa0dd774e627d4d21`.

- [x] **Step 5: validate the remote summary**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" remote-validate \
    --summary "$WRFR_SDD/remote-github-summary.json"
  ```

  Expected: exactly nine unique evidence classes, every class either sanitized
  metadata or explicit unavailable, no raw URLs other than the approved repo
  identity, no token/log/body field, and no evidence tied to a revision other
  than the returned `headSha` values.

  Completion evidence on 2026-08-22: `PASS remote-validate` over the exact
  summary above. Seven classes are observed; `workflows` is unavailable with
  fixed reason `checker-auth-context-incompatible`, and `oidc` is unavailable
  with fixed reason `checker-oidc-schema-incompatible`.

- [x] **Step 6: append the delivery and quality findings**

  Add one dated H3 covering:

  - local CI/CD trigger, job, concurrency, artifact, environment, promotion, and
    rollback structure;
  - local GitHub Actions permissions, full-SHA actions, shell/script ownership,
    supply-chain evidence, and remote repository policy metadata;
  - formatting, lint, syntax, unit, integration, end-to-end, mutation, affected,
    staged, all-files, and diff lanes;
  - Requirements Validation, Product/Artifact Verification, Product/System
    Validation, testing-as-method, traceability, discrepancy, independence, and
    representative-user/environment boundaries.

  A historical hosted run cannot prove current local HEAD. `VAL-*` is a local
  criterion identifier, not a validation outcome. Static PASS never proves
  intended use or stakeholder acceptance.

- [x] **Step 7: run delivery-focused GREEN checks**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream delivery-quality
  python3 scripts/validate-github-actions-security.py --root .
  python3 scripts/validate-ci-python-contract.py --root .
  python3 scripts/validate-affected-surfaces.py --root .
  python3 scripts/validate-agent-governance-ci.py --root .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Completion evidence on 2026-08-22: the pre-edit probe returned exact
  fail-fast `ERROR INTEGRATION_SECTION`. The integrated probe returned
  `PASS validate-integration`; GitHub Actions security, CI Python contract,
  affected surfaces, agent-governance CI, strict Markdown, strict links/owners,
  and `git diff --check` all passed. The owner retains exactly one dated H3 and
  all four allocated request IDs. These results are repository-static and do
  not prove hosted current-HEAD execution, enforcement, intended use, or live
  delivery.

- [x] **Step 8: commit and review delivery findings**

  Update Task/Plan/progress, then commit:

  ```bash
  git add docs/90.references/research/2026-08-08-wer/ci-cd-github-actions-and-qa.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify delivery and quality research"
  ```

  Generate the committed package and dispatch source-fidelity, task, and
  post-remote security reviews. The post-remote reviewer receives only the
  sanitized summary schema/counts and the committed package, not credentials or
  raw command output. Resolve Critical or Important findings in a scoped fix
  commit and re-review before Task 8.

  Commit `ae7a22620ede8bfdb387c4528952f156e82a7aa2` contains exactly the
  four named paths. Registered report SHA-256 is
  `00856efaed17e3d5267e13d1c83399529bab7203201167d873bf83712aaec6a9`;
  registered review-package SHA-256 is
  `71a09244cce2ddb51bc2f1a1568ed874d1614837423e430fb8d3bbe816b3b876`
  for exact one-commit range `fcbcd869..ae7a2262`. Final inventory SHA-256 is
  `68b4173514a287eaff1e9e1c3b50c7ad57d3e6dbce2eb01b6dcd10ba9d08c1bc`.
  The post-commit reviewer returned `APPROVED WITH MINOR`,
  Critical/Important/Minor `0/0/1`, and found no material implementation
  defect. This closure corrects its sole intentional pre-closure lifecycle
  Minor. WRFR-006 is complete and WRFR-007 is queued and ready.

### WRFR-007 pre-integration checker recovery gate

The first Task 8 command ran from clean tracked commit
`cb494def67049706670e63d5157676886885faa7` before any shared-ledger owner
edit. It exited `1` with exactly `ERROR ARGUMENTS_INVALID` because the checker
parser accepts only the five topical workstreams. The same checker also treats
an omitted `--workstream` as those five topical checks only, so it can falsely
pass terminal validation without checking the shared ledger, scope projection,
pack census, or lifecycle reconciliation. The frozen identities at this
checkpoint are:

- checker SHA-256
  `2308481b8b0ded1647c105a4ab9aad0292db1459e53b8989a49f1fd3bdd7b038`;
- inventory SHA-256
  `68b4173514a287eaff1e9e1c3b50c7ad57d3e6dbce2eb01b6dcd10ba9d08c1bc`;
- allocation SHA-256
  `04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`;
- baseline SHA-256
  `41d56cb71092d0cd9dee7caa90ddaf57183473170472695882e14707fe04ae5d`.

This defect is broader than an argparse choice. The repair must preserve the
five topical modes and add two closed pseudo-modes, `shared-ledger` and
`reconciliation`. An invocation without `--workstream` must compose all five
topical validators plus both pseudo-mode validators. Unknown mode names remain
`ERROR ARGUMENTS_INVALID`.

The shared-ledger mode has this exact contract:

1. Compare the existing source owner rows `SRC-WERPC-001..090` and all existing
   135 claim owner rows with their lines at the immutable baseline commit and
   reject any byte change as `INTEGRATION_LEDGER_LEGACY`.
2. Require exactly one dated addition section in the ledger. To preserve the
   old headers and rows byte-for-byte, that section uses new tables with these
   exact headers and does not widen or reflow an existing table:

   ```text
   Source ID | Request owner | URL | Revision | Source class | Checked on | Adopted scope | Rejected scope | Uncertainty | Refresh trigger
   Claim ID | Request owner | Claim | Source IDs | Workspace selectors | Evidence depth | Disposition | Missing evidence | Safe boundary | Canonical owner | Refresh trigger
   ```

   It projects `SRC-WERPC-091` and `CLM-WERPC-013-01..06` in numeric order from
   the immutable allocation. Scalar cells equal the corresponding allocation
   string after rejecting newline or literal `|`; the URL cell wraps only the
   exact allocated URL in angle brackets. Array cells retain allocation order
   and join values with a comma followed by one space; an empty source-ID array
   is exactly `None`.
   `Canonical owner` is the request's immutable baseline owner path. Missing,
   duplicate, reordered, wrong-owner, or
   allocation-divergent source and claim rows fail respectively with
   `INTEGRATION_SOURCE_PROJECTION` or `INTEGRATION_CLAIM_PROJECTION`.
3. Require exact terminal census `14/36/91/141`, all 36 report rows with both
   external and workspace observations, exactly one owner row for every
   referenced source/claim ID, and no unallocated addition. Identifier census
   or reference failures use `INTEGRATION_IDENTIFIER_CENSUS` or
   `INTEGRATION_IDENTIFIER_REFERENCE`.
4. Require exactly one `### 2026-08-20 full-corpus reverification` section in
   the scope index and all ten Plan scopes. Each scope must project contributing
   REQ IDs, evidence depth, changed/unchanged outcome, retained limitation, and
   canonical owner. Section and entry failures use `INTEGRATION_SCOPE_SECTION`
   and `INTEGRATION_SCOPE_PROJECTION`.
5. Recompute the pack README reconciliation from the five registered reports
   and immutable allocation. It must record census `14/36/91/141`; external
   `changed=3`, `unchanged=32`, `unreachable=1`; workspace `confirmed=29`,
   `drifted=6`, `absent=1`; dispositions `Verified=20`, `Verified gap=4`,
   `Partial=12`; evidence depths `repository-static=28`,
   `public-documentation=8`; blocking classes `none=12`, `repo-static=10`,
   `provider-runtime=5`, `hosted-ci=2`, `live-cluster=3`,
   `human-judgement=4`; changed request IDs `004`, `006`, `008`, `009`, `011`,
   `012`, `013`, `018`, `025`; unreachable request `033`; the allocated K3s
   observation; and the six allocated claim additions, distinguished as three
   current-form terminology corrections and three repository-static drift
   records. Missing reconciliation and mismatched derived values use
   `INTEGRATION_README_RECONCILIATION` and
   `INTEGRATION_DISTRIBUTION`.

The reconciliation mode must first satisfy shared-ledger validation, then
require the collection README to retain `2026-08-08-wer` as the sole current
pack and agree on terminal census; Stage 03, Spec, Plan, Task, ADR 0022, and
`standaloneExecutions` must be reciprocal and lifecycle-consistent; and durable
progress must list WRFR-002..007 completion with next owner WRFR-009 without
terminal approval. Before Task 9 edits, absence of the required dated collection
reconciliation fails first with `INTEGRATION_RECONCILIATION_SECTION`. Other
failures close with `INTEGRATION_COLLECTION_CURRENT`,
`INTEGRATION_COLLECTION_CENSUS`, `INTEGRATION_LIFECYCLE`,
`INTEGRATION_STAGE_INDEX`, `INTEGRATION_STANDALONE_ADR`,
`INTEGRATION_STANDALONE_REGISTRY`, or `INTEGRATION_PROGRESS`. Explicit
`reconciliation` validates the Task 9 pre-terminal active/In-Review state. The
no-workstream terminal composition accepts only a mutually consistent active
pre-closure state or mutually consistent done post-closure state.

Continuation is closed and ordered:

1. Commit this three-document recovery contract before changing the ignored
   checker, inventory, ledger, scope index, or pack README.
2. Add failing self-tests first for parser acceptance, mode dispatch, the exact
   production parsers, terminal composition, every fail-code family above, and
   mutations of legacy rows, allocated IDs, references, scope entries,
   distributions, current-pack census, lifecycle, ADR/registry reciprocity, and
   progress. Implement the minimum repair; compile it, run normal and optimized
   self-tests, run Ruff check and format-check, and obtain fresh independent
   Python and security approvals over the exact candidate bytes. Any Critical
   or Important finding or later byte change closes the gate.
3. Amend these same three tracked documents with the approved candidate hash
   and review verdicts, and commit that amendment before stateful execution.
4. Invoke fixed `artifact-rebind-checker-only` exactly once with inventory
   `68b4173514a287eaff1e9e1c3b50c7ad57d3e6dbce2eb01b6dcd10ba9d08c1bc`, old
   checker `2308481b8b0ded1647c105a4ab9aad0292db1459e53b8989a49f1fd3bdd7b038`,
   and the approved new checker hash. It may update only the existing checker
   record. Do not retry.
5. Run residue and normal/optimized self-tests, then rerun the unchanged Task 8
   command. Before owner edits it must reach semantic RED
   `ERROR INTEGRATION_SOURCE_PROJECTION`, not argument parsing. Only that result
   unblocks the sole shared-ledger integrator.

#### Approved checker candidate and integration serialization

The test-first repair is complete. The initial parser test reproduced
`ERROR ARGUMENTS_INVALID`; later mutation-first review cycles closed legacy
header/order drift, scope derivation and confinement, exact README sets,
collection/progress negation, registered `main()` dispatch, reciprocal-link
overconstraint, out-of-ledger lifecycle ambiguity, production collection-table
shape, and terminal ledger placement. Intermediate candidates were never
rebound and are superseded.

The approved checker SHA-256 is
`3cdaf66628e817663d9306b8e31c95788db0111fb30f1dcdcedc027fbdab338a`;
its size, mode, and owner are `367108` bytes, `0600`, and `hy:hy`. All 128
self-tests pass in normal and explicit optimized mode. `py_compile` with a
`/tmp` bytecode prefix, Ruff check, and Ruff format-check pass. Fresh exact-byte
Python and security reviews both returned `APPROVED`,
Critical/Important/Minor `0/0/0`.

The owner writers must use these dated-section serialization contracts:

- The ledger preserves every baseline byte and inserts its sole dated H3 and
  the already-defined source/claim tables immediately before the unique
  `## Sources` heading. The complete baseline `## Sources`,
  `## Review and Freshness`, and `## Related Documents` suffix remains exact.
- The scope section table header is exactly
  `Scope | Requests | Evidence depths | Outcome | Blocking classes | Canonical owners`.
  Its ten rows retain Plan order and partition the corpus exactly as follows:

  ```text
  repository governance=003
  harness and loop=001,002
  provider and common environment=004,005,006
  agents, model, and memory=026..032
  SDLC and document contracts=007,010..019,034..036
  documentation and knowledge routing=020,021
  Kubernetes and infrastructure=008,009
  security and approval=025
  CI/CD and QA=022,023,024
  verification and validation=033
  ```

  `Evidence depths` is the sorted unique report-derived set. `Outcome` is
  exactly `changed` when any contributing row has external `changed` or
  workspace `drifted`/`absent`, otherwise `unchanged`. `Blocking classes` is
  the sorted unique non-`none` set, or exactly `none`. `Canonical owners` is the
  sorted exact baseline-owner set with each path backticked.
- The pack dated reconciliation uses `Field | Value` and these exact ordered
  rows:

  ```text
  Census | markdownFiles=14, requests=36, sources=91, claims=141
  External results | changed=3, unchanged=32, unreachable=1
  Workspace results | confirmed=29, drifted=6, absent=1
  Dispositions | Verified=20, Verified gap=4, Partial=12
  Evidence depths | repository-static=28, public-documentation=8
  Blocking classes | none=12, repo-static=10, provider-runtime=5, hosted-ci=2, live-cluster=3, human-judgement=4
  Changed requests | REQ-WERPC-004, REQ-WERPC-006, REQ-WERPC-008, REQ-WERPC-009, REQ-WERPC-011, REQ-WERPC-012, REQ-WERPC-013, REQ-WERPC-018, REQ-WERPC-025
  Unreachable requests | REQ-WERPC-033
  Allocated K3s observation | SRC-WERPC-091; request=REQ-WERPC-009
  Allocated claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03, CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06
  Terminology claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03
  Drift claims | CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06
  Out-of-ledger observations | observed proposals=1; allocated=1; unallocated=0; outside-request/new-owner=0; SRC-WERPC-091->REQ-WERPC-009
  ```

- The Task 9 collection reconciliation uses `Field | Value | State` with exact
  rows `Current pack | 2026-08-08-wer | sole`, then Markdown files `14`,
  Requests `36`, Sources `91`, and Claims `141`, each state `exact`. The
  production four-column Research Pack Index remains
  `Material | Status | Role | Authority Boundary`; every `Active pack` or
  `Current pack` Status row must form the exact canonical fourteen-file dated
  pack set.
- The Task 9 durable-progress section uses `Field | Value`: WRFR-002 through
  WRFR-007 each equal `complete`, followed by `Next Owner | WRFR-009` and
  `Terminal Approval | not-claimed`.

One unregistered review residue must be removed before rebind. Its fixed
identity is:

| Object | Device | Inode | Size | `mtime_ns` / `ctime_ns` | Mode | UID:GID | Constraint |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SDD workspace parent | 2096 | 4406235 | 4096 | not a cleanup equality field | `0700` | 1000:1000 | existing non-symlink directory; fixed cleanup parent |
| `__pycache__` | 2096 | 1694147 | 4096 | 1787398444410567416 | `0755` | 1000:1000 | non-symlink directory; entries exactly the file below |
| `__pycache__/full-corpus-check.cpython-312.pyc` | 2096 | 1754901 | 404505 | 1787398444410567416 | `0600` | 1000:1000 | regular non-symlink; SHA-256 `4589e081b801c768b74f855815e0d67f6a9c452dd8e2f1d54c6dabd43815f68e` |

After this amendment commit, cleanup uses the literal SDD path and no generic
target. Open the SDD parent and `__pycache__` with directory file descriptors,
`O_DIRECTORY`, and `O_NOFOLLOW`; bind the parent and directory identities above;
require the child entry set to be exactly the named file; and obtain the child
with `lstat`/`stat(..., follow_symlinks=False)` plus an `O_NOFOLLOW` file
descriptor. Match device, inode, size, nanosecond mtime/ctime, mode, UID/GID,
regular-file type, and SHA-256 through that descriptor. Recheck the directory
entry against the retained file descriptor immediately before a dirfd-relative
`unlink`, then `fsync` the directory. Require the retained directory to be
empty, rebind it from the retained SDD-parent descriptor, remove only that exact
empty directory with dirfd-relative `rmdir`, `fsync` the SDD parent, and prove
the literal entry absent without following a symlink. Any mismatch, extra
entry, rename, substitution, symlink, hash drift, or postcondition failure stops
without broader deletion. The remaining same-UID race between final identity
check and unlink is explicit; retained dirfds and post-absence bound but cannot
eliminate it. This cleanup is not a checker or inventory rebind and creates no
authority to remove any other artifact.

No remote query, live action, push, merge, publication, or new research owner is
authorized by this recovery.

#### Task 8 Stage 90 frozen-blob transition-guard recovery

Task 8 Steps 2 through 4 produced the required shared projection, and the exact
shared integration, strict document-registry, strict Markdown-profile, and
`git diff --check` commands passed. The exact strict links command exited `2`
with `configuration error: reviewed Stage 90 move source differs from its frozen blob`.
The failing reviewed source is
`docs/90.references/research/2026-08-08-wer/README.md`: the guard accepts only
base Git blob `6bfec251d8927dd82f5c12b49c013a598c64d088`, while the reviewed Task 8
successor is Git blob `11719d258d0454d68f3e6b6ed0377c3d3b9de6b2`.

This is a validator transition defect, not authority to relax immutable-history
validation. The repair must retain the current Stage 90 reviewed move-edge count
of `29` and the immutable historical alias source/edge/occurrence counts of
`27/93/169`. Define one closed source-specific `(base, target)` Git-blob
transition map containing only the path and blob pair above, and apply that same
map in both the Stage 90 reviewed-move and immutable-historical-alias source
checks. A source not in the map remains pinned to its existing single blob.
The target is accepted only as the complete current source blob; it does not
authorize an open-ended append or prefix/suffix exception.

The transition parser and validators fail closed on every foreign key, base
mismatch, value that is not lowercase 40-hex, target equal to base, insertion or
prefix overlap, and arbitrary source mutation. The map must not change link
targets, redirect membership, edge derivation, occurrence counting, path
resolution, or archive authority. The exact implementation scope is limited to
`scripts/validate-links-and-owners.py` and
`tests/test_archive_validation.py`; no research owner, README, ledger, scope,
registry, inventory, report, or remote state belongs to this repair.

Execution order is fixed: commit this tracked three-document recovery contract;
write focused mutation tests and record RED; implement the minimum shared
transition helper and record GREEN; run compile, Ruff check and format-check,
the focused tests, full `tests.test_archive_validation`, validator self-test,
strict links validation, and `git diff --check`; obtain fresh independent code
and security review; then commit the exact two-file guard repair. Only after
that commit may Task 8 Step 5 be rerun. WRFR-007 remains blocked/in progress;
Steps 1 through 5 and completion remain unchecked until every original Step 5
command passes, and Step 6 remains controller-owned review and commit work.

### Task 8: WRFR-007 — source, claim, scope, and pack integration

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/90.references/research/2026-08-08-wer/scope-application-index.md`
- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: five immutable reviewed reports, the immutable allocation map, and
  all reviewed topical sections from WRFR-002..006.
- Produces: one contiguous source sequence beginning at `091`, one contiguous
  `013` claim block, ten re-projected scopes, and terminal pack counts.

- [x] **Step 1: reproduce ledger and projection RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream shared-ledger
  ```

  Expected before shared integration: allocated source/claim IDs absent from the
  ledger, scope projection absent, and pack counts still at the baseline.
  After the approved checker-only recovery and before owner edits, the unchanged
  command exited `1` with accepted semantic RED
  `ERROR INTEGRATION_SOURCE_PROJECTION`.

- [x] **Step 2: append source and claim records**

  Use `allocation.json` exactly. Append sources in numeric order, then append the
  `CLM-WERPC-013-NN` cycle block in numeric order. Each source row contains owner,
  official URL/revision, source class, checked-on date, adopted scope, rejected
  scope, uncertainty, and trigger. Each claim row contains request owner, claim,
  source IDs, exact workspace selectors, evidence depth, disposition, missing
  evidence, safe boundary, owner, and trigger.

  Preserve every pre-existing row byte-for-byte. If Markdown table formatting
  would rewrite old rows, stop and switch to an append operation that touches
  only the new section; do not accept mechanical whole-ledger reflow.

- [x] **Step 3: re-project the ten governance scopes**

  Append one 2026-08-20 H3 to `scope-application-index.md` that derives, rather
  than restates, the refreshed evidence for:

  ```text
  repository governance
  harness and loop
  provider and common environment
  agents, model, and memory
  SDLC and document contracts
  documentation and knowledge routing
  Kubernetes and infrastructure
  security and approval
  CI/CD and QA
  verification and validation
  ```

  Every scope entry names the contributing request IDs, current evidence depth,
  changed/unchanged outcome, retained limitation, and canonical owner.

- [x] **Step 4: reconcile the pack README**

  Append a dated reconciliation section with exact terminal file/request/source/
  claim counts, external outcome distribution, workspace outcome distribution,
  disposition distribution, changed request IDs, corrections, unreachable
  sources, out-of-ledger observations, and retained blocking-class distribution.

  Update only mutable snapshot/count cells that are contractually current. Do
  not rewrite earlier dated reconciliation sections.

- [x] **Step 5: validate shared integration**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream shared-ledger
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Expected: all allocated IDs occur exactly once as owner rows, every topical
  reference resolves, exact 36 dual observations exist, all ten scopes exist,
  and README counts equal the parsed terminal corpus.

  Executed evidence is GREEN after recovery-contract commit
  `0a9a9e656c0655617e1c9ea3c3df28b98ad56d34` and exact two-file guard commit
  `545f114dd5080ac541ba2ae9bec9a18d24f58129`. Fresh independent final guard
  review returned Critical/Important/Minor `0/0/0`. Shared integration returned
  `PASS validate-integration`; the strict registry returned `540 paths`; the
  strict Markdown validator returned `0` violations; strict links returned
  `PASS CROSS-DOCUMENT`; and `git diff --check` passed.

- [ ] **Step 6: commit and review shared integration** — **Blocked**

  Review the local diff for accidental old-row reflow, then commit:

  ```bash
  git add docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md \
    docs/90.references/research/2026-08-08-wer/scope-application-index.md \
    docs/90.references/research/2026-08-08-wer/README.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: integrate full-corpus research evidence"
  ```

  Generate the committed package and dispatch one ledger/source-fidelity
  reviewer and one task reviewer. Resolve Critical or Important findings in a
  scoped fix commit and re-review before Task 9.

  The exact six-file integration commit is
  `fef53976b97c560de0a9f020e87be1e7e0e1c3b8`
  (`docs: integrate full-corpus research evidence`). The registered
  implementer report SHA-256 is
  `f781967ffc14a7e1d23421c06859a3eea0fc78cc510ea2df059165ab487ef7bd`;
  the registered review-package SHA-256 is
  `9c68c5f77a6473f6c6c4c106669514d90080d7a88f5558ef67e6db363e60952c`
  for exact range `cb494def..fef53976`. Post-commit owner review of the
  ledger/source-fidelity projection and task/spec quality returned
  `APPROVED`, Critical/Important/Minor `0/0/0`. The required shared
  integration, strict registry, strict Markdown, strict links/owners,
  `git diff --check`, and artifact `residue` lanes were rerun after commit and
  passed. WRFR-007 is complete; WRFR-008 is queued and ready.

#### 2026-08-22 Task 8 provenance incident

The preceding closure record is retained as the evidence available when it was
written, but it no longer controls current status. `task-8-brief.md` was
generated and registered only after integration commit
`fef53976b97c560de0a9f020e87be1e7e0e1c3b8`; it therefore cannot prove that the
implementer consumed a registered brief before dispatch. The late brief,
implementer report, and review package are immutable evidence and must not be
rewritten to simulate an earlier event.

Independent task/spec re-review withdrew its earlier `APPROVED` result and
classified one Important provenance finding, Critical/Important/Minor
`0/1/0`. The independent ledger/source content review remains `APPROVED`,
Critical/Important/Minor `0/0/0`; the integration commit, source and claim
owners, ten-scope projection, pack reconciliation, and all GREEN validation
evidence remain preserved. Step 6 and WRFR-007 are blocked because provenance,
not content, is unresolved. WRFR-008 must not begin before an explicit human
decision.

Exactly two next paths are allowed, both requiring explicit human direction:

- **A — documented one-time exception:** accept the exact full Plan and scoped
  prompt as the implementation input despite the missing registered
  pre-dispatch brief, record the exception without rewriting any artifact, and
  obtain a new scoped closure review.
- **B — closed re-execution:** withdraw and then reapply the three research
  projections only after a new registered pre-dispatch brief is demonstrably
  consumed, followed by a new fix package and independent review. The existing
  commit and late evidence remain historical rather than being rewritten.

##### Separate mandatory SDD cleanup-recovery gate

After the provenance correction, the controller mistakenly invoked the
forbidden canonical `sdd-workspace` helper while recovering context. It created
the empty sibling `.superpowers/sdd/plan` with device/inode `2096/4541614`, mode
`0755`, UID:GID `1000:1000`, and mtime/ctime
`1787407543766841537` ns. It also rewrote `.superpowers/sdd/.gitignore` with
identical bytes `*\n` and unchanged SHA-256
`cdbcae15105d6b781e620813c79c7e868740d4e9cc53ce6f5fcbbc12387adf4b`.
The marker remains device/inode `2096/4410802`, mode `0644`, UID:GID
`1000:1000`, but its mtime/ctime changed from recorded
`1787208168057628362` ns to `1787407543770964835` ns.

The canonical Plan workspace remains device/inode `2096/4406235`, mode `0700`.
Inventory SHA-256 remains
`058cad35454e285dcc4c7b9b2be8ede06e111090ec45f78762cd5a001c14b545`,
and no canonical task-artifact bytes changed. Nevertheless, the marker
FileVersion is invalidated and the foreign sibling makes the WRFR-009 cleanup
preconditions false. No deletion, restoration, chmod, or recovery was attempted.

This is a separate mandatory gate, not a third Task 8 resolution path. The two
Task 8 paths remain exactly A/B above. Independently of that choice, the exact
empty sibling and rewritten marker identity require explicit human direction
and a one-time cleanup-recovery design plus independent review before any
recovery action or WRFR-009 cleanup. This Plan does not invent or authorize the
procedure.

No completion, exception, re-execution, or WRFR-008 authorization is claimed by
this incident record.

#### 2026-08-23 Path B ruling and closed replay contract

This section additively supersedes only the unresolved A/B decision above. The
human selected **Path B**. The incident facts, integration commit, late brief,
implementer report, and every prior review package remain immutable historical
evidence; none may be edited, replaced, re-registered, or represented as timely
pre-dispatch evidence. This replay is Task 8B within `WRFR-007`, not Plan Task
11, not a new WRFR, and not `WRFR-010`. The `task-11-*` artifact prefix is only
the ignored replay-evidence namespace admitted by the existing inventory
grammar.

The frozen projection transition is exact:

| Research projection | Predecessor commit/blob | Reviewed successor commit/blob |
| --- | --- | --- |
| `source-coverage-and-migration-ledger.md` | `545f114dd5080ac541ba2ae9bec9a18d24f58129` / `a6feed2026d19261f42f475f52f3f746eeee4122` | `fef53976b97c560de0a9f020e87be1e7e0e1c3b8` / `e4ed30b5602278b212a5e035a9dded222fae8d85` |
| `scope-application-index.md` | `545f114dd5080ac541ba2ae9bec9a18d24f58129` / `f7e4b60cce6a7d5ee5c706ab3a6a8fae663e9bed` | `fef53976b97c560de0a9f020e87be1e7e0e1c3b8` / `6c2d4723c69821a9681fa45151ea70b528ff66fa` |
| `README.md` | `545f114dd5080ac541ba2ae9bec9a18d24f58129` / `6bfec251d8927dd82f5c12b49c013a598c64d088` | `fef53976b97c560de0a9f020e87be1e7e0e1c3b8` / `11719d258d0454d68f3e6b6ed0377c3d3b9de6b2` |

Replay must follow this closed order:

1. Before brief creation, require every `task-11-*` entry absent and
   non-symlink. Create `task-11-brief.md` through the guarded artifact protocol,
   register its complete FileVersion, and freeze the post-registration
   inventory. After registration and before dispatch, require exactly that
   registered brief in the `task-11-*` namespace; any other `task-11-*` entry is
   foreign. Prove the frozen brief was consumed before implementer dispatch and
   freeze the starting `HEAD`, clean index/worktree, and three successor blobs.
   A brief FileVersion, inventory, foreign-path, staging, or blob mismatch stops
   the replay before mutation.
2. Create one withdrawal commit whose parent is the frozen starting `HEAD` and
   whose complete pathset is only the three table rows. Each resulting blob must
   equal its predecessor blob. Run the unchanged shared-ledger integration
   command and require semantic RED `ERROR INTEGRATION_SOURCE_PROJECTION`; an
   infrastructure/configuration failure or any different semantic result is not
   accepted. Record the commit and command evidence in `task-11-report.md`, then
   generate `task-11-review-package.md` for exactly that one adjacent commit and
   obtain independent projection/task review before reapplication.
3. Create the immediately adjacent reapplication commit with no intervening
   tracked commit and the same exact three-path pathset. Each resulting blob
   must equal its reviewed successor blob. Rerun shared integration, strict
   registry, strict Markdown profiles, strict links/owners, affected/staged
   lanes, exact-index pre-commit, repository-quality gates selected for the
   three paths, and both diff checks; every applicable repository-static check
   must be GREEN. Generate `task-11-fix-1-review-package.md` for exactly that
   one reapplication commit and obtain a fresh independent projection/task
   review.
4. Register the completed replay report and both adjacent review packages only
   after their immutable bytes and FileVersions are final. A combined net-zero
   range is supplemental only and cannot replace either single-commit package.
   Any correction uses another admitted `task-11-fix-N-review-package.md` and
   preserves earlier artifacts. Only a fresh scoped `WRFR-007` closure review
   with no open Critical or Important finding may close Task 8 Step 6.

The two commits may change no Plan, Task, progress, checker, test, inventory,
Spec, lifecycle, or other research file. Their net tree must restore the three
successor blobs exactly, while their adjacent commit and review identities make
the withdrawal and reapplication independently observable. `WRFR-008` remains
blocked until the post-reapplication `WRFR-007` closure review is approved and
recorded; Path B selection alone authorizes neither replay completion nor
successor execution.

##### Human-approved cleanup-recovery design pending independent re-review

The human approved this design contract, but the first independent security
review rejected it. It remains pending fresh independent security and task/spec
re-review and does not authorize creation or execution. It changes no checker
and does not revise original bootstrap or incident provenance. The marker's
pre-incident FileVersion remains permanently invalid because ctime cannot be
restored. Its incident successor identity is device/inode `2096/4410802`,
regular non-symlink, mode `0644`, UID:GID `1000:1000`, size `2`, mtime/ctime
`1787407543770964835` ns, SHA-256
`cdbcae15105d6b781e620813c79c7e868740d4e9cc53ce6f5fcbbc12387adf4b`, bytes
`*\n`. The foreign empty directory is device/inode `2096/4541614`, mode `0755`,
UID:GID `1000:1000`, mtime/ctime `1787407543766841537` ns. The canonical Plan
workspace is device/inode `2096/4406235`, mode `0700`; its timestamps, entries,
protected content, and inventory remain mutable until the last pre-cleanup
consumer finishes.

The future executable is fixed at
`/tmp/wrfr-009-sdd-incident-recovery.py` under `C-WRFR-011`. Before any
separately approved creation, that exact path must be absent and non-symlink.
Creation must be exclusive and no-follow, producing a current-user regular
non-symlink of mode `0600`. Freeze and independently review its exact source and
executed bytes, size, mode, UID:GID, and SHA-256. Invoke it from the frozen
worktree root only as
`PYTHONDONTWRITEBYTECODE=1 python3 -I -B /tmp/wrfr-009-sdd-incident-recovery.py
<mode>`, where `<mode>` is exactly `--self-test`, `--check`, or `--execute`.
It accepts one mode and no filesystem path argument. This correction authorizes
neither creation, execution, nor later deletion of the temporary executable.

After the last pre-cleanup consumer, one final approval manifest must freeze
every bound object, not reuse a historical inventory hash:

- the worktree root, `.superpowers`, and `sdd` directories: directory and
  non-symlink type, device, inode, mode, UID:GID, size, mtime, ctime, exact
  sorted entry sets, and SHA-256 of the canonical NUL-delimited entry-set bytes;
- incident `plan`: the same identity fields and an exact empty entry set;
- successor `.gitignore`: regular and non-symlink type, every identity field,
  size, timestamps, bytes, and SHA-256;
- the canonical Plan workspace: directory identity and exact final entry set,
  plus the final inventory bytes/SHA-256 and every protected artifact's complete
  FileVersion and content SHA-256 after its last consumer; and
- the separately created executable identity and source/executed-byte hash.

Current stable device/inode values are provisional manifest inputs only:
worktree `2096/2229923`, `.superpowers` `2096/3023848`, `sdd`
`2096/4404277`, incident `plan` `2096/4541614`, successor marker
`2096/4410802`, and canonical workspace `2096/4406235`. The terminal manifest
must freshly bind all fields above. A missing field, changed identity, unexpected
entry, content mismatch, or use of the current historical inventory as terminal
identity is `RECOVERY_PRECONDITION` before mutation.

The procedure opens each fixed component one at a time with directory-relative
descriptors and `O_NOFOLLOW`, retains them through completion, and compares
`fstat` to non-following entry stat before every mutation. Use `O_NOATIME` for
regular-file reads when supported; lack of permission for `O_NOATIME` permits a
no-follow read but grants no authority to weaken any other check. Hold a
non-blocking advisory exclusive `flock` on the retained `sdd` descriptor through
check, mutation, fsync, and proof. This quiesces cooperating actors only. A
non-cooperating same-UID writer remains a residual race addressed by repeated
descriptor/entry checks and fail-closed results, not claimed away.

After one complete precondition pass, `--execute` may call only
descriptor-relative `rmdir(plan)`, then `fsync(sdd_fd)`, prove `plan` absent and
all protected state unchanged, then descriptor-relative `unlink(.gitignore)`,
then `fsync(sdd_fd)`, and finally prove both names absent/non-symlink, the
canonical workspace is the sole `sdd` child, final protected inventory/content
is unchanged, and residue validation passes. Do not chmod, rewrite, restore
timestamps, rename, quarantine, recreate, update provenance, recursively
delete, follow a symlink, or remove the canonical workspace. The existing SDD
finish remains a later, separate operation.

Exit and terminal-marker semantics are closed:

| Exit | State | Meaning |
| --- | --- | --- |
| `0` | `PASS` | Selected mode completed with its required proof. |
| `20` | `RECOVERY_PRECONDITION` | Failure before any namespace/data mutation; a last-check replacement before `rmdir` is included. |
| `21` | `RECOVERY_PARTIAL` | Any failure after the first mutation, including either `fsync`, final absence/exclusivity proof, protected-content proof, or residue proof. |
| `22` | `RECOVERY_ALREADY_COMPLETE` | Both incident names are already absent and the canonical workspace/protected state proves the approved recovered state. |
| `23` | `RECOVERY_ARGUMENTS` | Mode count/value or any path argument is invalid. |

Every mode emits exactly one stable terminal line:
`WRFR_SDD_RECOVERY mode=<mode> code=<state> mutations=<0|1|2>
state=<precondition|partial|recovered|already-complete|arguments|self-test>`.
Zero mutation excludes access-time effects but requires equality of namespace,
data, size, mode, ownership, mtime, and ctime. Failure after `rmdir`, including
its following `fsync`, is partial; both names removed with any proof failure is
partial. Never recreate either name or retry a partial result without a new
manifest, independent review, and explicit human approval.

Before destructive approval, the exact source must pass `--self-test` fixtures
for success, arguments, already-complete, symlink/type/identity/owner/mode/time/
bytes/hash/entry-set mismatch, non-empty sibling, lock contention,
replacement/race, pre-mutation failure, both `fsync` failures, between-call
failure, final-proof failure, and residue failure. `--check` must pass against
the final manifest without mutation. Fresh security and task/spec reviews must
approve the source, executable identity, manifest, tests, exact command,
quiescence boundary, and partial semantics before a separate human approval.
No cleanup or finish is authorized by this amendment.

##### Task 12 fix-round evidence boundary

Registered `task-13-brief.md` is Task 12 correction evidence only, not Plan
Task 13 or a WRFR. Registered `task-14-brief.md` is a clerical correction to
that brief only, not Plan Task 14 or a WRFR; it replaces the absent mistyped
third blob fixture with tracked blob
`a21d2cfeae6dfcd4cdc98f6661c1f7a190c49523`. Both briefs, Task 12 artifacts,
the inventory, and ignored progress remain immutable. Exact test-only Commit A
is `0577d1c0` (`test: allowlist reviewed blob fixtures`); this three-document
contract is the separate Commit B. `task-13-report.md` will record the complete
two-commit and validation evidence without becoming a Plan task. The design is
human-approved pending fresh independent security and task/spec re-review. No
Path B replay, WRFR-008, incident-recovery executable action, cleanup, remote or
live mutation, or lifecycle transition is authorized or performed by this fix.

### Task 9: WRFR-008 — cross-link and lifecycle reconciliation

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Modify: `docs/99.templates/registry.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: terminal parsed counts and every reviewed topical/shared commit.
- Produces: mutually consistent pack, collection, Stage 03, standalone relation,
  ADR, Spec, Plan, Task, and durable-progress current-state projections.

- [ ] **Step 1: run the pre-reconciliation link/count probe**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream reconciliation
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  ```

  Record every expected stale current-count, missing reciprocal link, or status
  mismatch as RED. If both commands already pass, record that no reconciliation
  delta is required instead of fabricating one.

- [ ] **Step 2: reconcile final content and lifecycle truth**

  Apply only the deltas emitted by Step 1. The collection README continues to
  identify `2026-08-08-wer` as the sole current research owner. The pack README
  and collection README use the same terminal census. Spec/Plan/Task remain
  `active` or `In Review` until the whole-branch review and terminal gates are
  complete. ADR 0022 and `standaloneExecutions` remain exact and reciprocal.

  Update durable progress with completed WRFR-002..007 commits and next owner
  `WRFR-009`; do not claim terminal approval yet.

- [ ] **Step 3: validate reconciliation**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream reconciliation
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-reference-information-architecture.py --self-test
  git diff --check
  ```

- [ ] **Step 4: commit and review reconciliation**

  If Python or registry code changed unexpectedly, stop: this task is
  documentation-only and must not absorb tooling changes. Commit:

  ```bash
  git add docs/90.references/research/README.md \
    docs/90.references/research/2026-08-08-wer/README.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/03.specs/README.md \
    docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md \
    docs/99.templates/registry.json \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reconcile research lifecycle and cross-links"
  ```

  Generate the committed package and dispatch one task reviewer. Resolve
  Critical or Important findings in a scoped fix commit and re-review before
  Task 10.

### Task 10: WRFR-009 — terminal validation, whole-branch review, and cleanup

**Files:**

- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/99.templates/registry.json`
- Modify: `scripts/validate-active-corpus-residue-closure.py`
- Modify: `tests/test_active_corpus_retention.py`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Remove after final consumer: every artifact under this Plan's ignored SDD
  workspace, by deleting that exact workspace through the SDD finish procedure.

**Interfaces:**

- Consumes: exact branch diff, all task reviews, allocation/baseline/report hashes,
  sanitized remote summary, and current active lifecycle relation.
- Produces: done lifecycle, post-closure authority registration, terminal green
  evidence, whole-branch verdict, clean tracked tree, and absent owned residue.

- [ ] **Step 1: create the exact branch pathset safely**

  ```bash
  WRFR_MERGE_BASE=$(git merge-base main HEAD)
  python3 "$WRFR_SDD/full-corpus-check.py" pathset \
    --root . --base "$WRFR_MERGE_BASE" --lane affected \
    --output "$WRFR_SDD/affected-paths.nul"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_SDD/affected-paths.nul"
  git diff --name-only "$WRFR_MERGE_BASE"
  ```

  Expected: the rendered Git list and guarded NUL pathset name the same approved
  branch paths, with no foreign or ignored SDD artifact.

- [ ] **Step 2: stage the exact terminal proposal**

  Reject any unexpected path before staging. Stage only the paths from the
  guarded affected pathset, then create the staged pathset:

  ```bash
  git add --pathspec-from-file="$WRFR_SDD/affected-paths.nul" \
    --pathspec-file-nul
  python3 "$WRFR_SDD/full-corpus-check.py" pathset \
    --root . --base "$WRFR_MERGE_BASE" --lane staged \
    --output "$WRFR_SDD/staged-paths.nul"
  python3 "$WRFR_SDD/full-corpus-check.py" artifact-register \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json" \
    --path "$WRFR_SDD/staged-paths.nul"
  git diff --cached --check
  ```

- [ ] **Step 3: run affected and staged lanes on the same proposal**

  ```bash
  python3 scripts/run-validation-lane.py --root . --lane affected \
    --paths-file "$WRFR_SDD/affected-paths.nul" --delimiter nul
  python3 scripts/run-validation-lane.py --root . --lane staged \
    --paths-file "$WRFR_SDD/staged-paths.nul" --delimiter nul
  ```

  Expected: both lanes PASS against the same staged active-descriptor proposal;
  no `CLOSURE-WORKTREE-INDEX-DRIFT` is accepted as terminal evidence.

- [ ] **Step 4: run canonical terminal gates sequentially**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-research \
    --baseline "$WRFR_SDD/baseline.json" --report-dir "$WRFR_SDD"
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json"
  python3 "$WRFR_SDD/full-corpus-check.py" remote-validate \
    --summary "$WRFR_SDD/remote-github-summary.json"
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-reference-information-architecture.py --root . --require-settled-baselines
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run
  pre-commit run --all-files
  git diff --check
  git diff --cached --check
  ```

  Run sequentially. If any formatter mutates a file, inspect the exact mutation,
  restage only approved paths, regenerate both pathsets, and replay affected,
  staged, plain pre-commit, all-files, and both diff checks.

- [ ] **Step 5: obtain the pre-closure aggregate review**

  Generate a review package from `WRFR_MERGE_BASE` to `HEAD` using the SDD
  helper. Dispatch the most capable aggregate reviewer with the Spec, Plan, Task,
  review package, ledger rulings, deferred minors, and every workstream review
  result. One fix agent may address the complete findings list, followed by one
  scoped re-review and a committed fix. This gate authorizes the bounded closure
  mutation but is not the terminal whole-branch approval because it does not yet
  contain the closure code/test/lifecycle diff.

- [ ] **Step 6: close the lifecycle with a focused RED/GREEN after review**

  After pre-closure review approval:

  - add Spec 0062 to the exact expected future-Spec list in
    `tests/test_active_corpus_retention.py`, run the command below, and record
    RED because `POST_CLOSURE_SPEC_AUTHORITY_PATHS` still lacks Spec 0062;

    ```bash
    python3 -m unittest tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_frozen_authority_scope_excludes_later_program_authority
    ```

  - set Spec, Plan, and Task status to `done`;
  - mark all WRFR tasks and Plan checkboxes complete;
  - change the Spec 0062 `standaloneExecutions` state to `done`;
  - add Spec 0062 to `POST_CLOSURE_SPEC_AUTHORITY_PATHS` and rerun the same
    focused command GREEN;
  - update Stage 03 index status/currentness and durable progress with commit and
    review evidence;
  - record hosted/provider/live/human evidence as `DEFER`, not failed;
  - record the exact logical commit list and no-push/no-merge boundary.

- [ ] **Step 7: restage and rerun affected, staged, and terminal gates**

  Lifecycle closure changes occur after the first terminal run. Regenerate the
  merge-base-to-worktree affected pathset, verify it, stage only that guarded
  pathset with the exact `git add --pathspec-from-file` command from Step 2,
  regenerate the staged pathset, and repeat Steps 3 and 4 in full. The second
  sequential run is the terminal evidence.

- [ ] **Step 8: commit the terminal closure**

  ```bash
  git add docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/03.specs/README.md \
    docs/99.templates/registry.json \
    scripts/validate-active-corpus-residue-closure.py \
    tests/test_active_corpus_retention.py \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: close full-corpus research reverification"
  ```

- [ ] **Step 9: obtain terminal reviews, verify state, and remove owned residue**

  Generate a fresh `WRFR_MERGE_BASE..HEAD` review package after the closure
  commit. Dispatch the most capable whole-branch reviewer and a
  `python-reviewer` for the residue-closure validator/test diff. Both reviewers
  must inspect the closure commit as well as earlier workstream commits. If a
  Critical or Important finding exists, make one scoped fix commit, regenerate
  affected/staged pathsets, replay Steps 3 and 4 in full, generate a new package,
  and obtain scoped re-review. No cleanup begins until both final verdicts are
  approved.

  Run the focused post-closure test, repository aggregate, and both diff checks
  once more on the approved committed tree. Then run:

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" residue \
    --workspace "$WRFR_SDD" \
    --inventory "$WRFR_SDD/artifact-inventory.json"
  ```

  Record final `HEAD`, status, commit list, counts, artifact inventory, and
  review verdict in the SDD ledger. After the last pre-cleanup consumer, freeze
  the complete approval manifest defined by the Task 8 cleanup-recovery
  addendum. For this exact incident only, the proven manifest state containing
  the known empty `plan` sibling and known successor `.gitignore` supersedes the
  legacy branch that would stop on any foreign sibling. Any identity, entry,
  manifest, lock, executable, review, or content mismatch still takes that
  legacy fail-closed stop branch and authorizes no generic removal.

  Obtain fresh independent security and task/spec approval for the exact source,
  tests, planned guarded creation, complete manifest contract, and commands.
  Then obtain separate human approval to create exact executable
  `/tmp/wrfr-009-sdd-incident-recovery.py`; freeze and independently verify its
  complete executable identity against the approved source before separately
  approving `--check` or `--execute`. This Plan text grants none of those
  actions. The approved incident sequence is `--check`, descriptor-relative
  `rmdir(plan)`, parent `fsync`, proof, descriptor-relative
  `unlink(.gitignore)`, parent `fsync`, and final absence/canonical-child/
  protected-content/residue proof. Any failure after the first removal is
  `RECOVERY_PARTIAL`, stops completion, and cannot be retried without a new
  manifest, review, and approval.

  Only after incident recovery returns `PASS` or a fully proved
  `RECOVERY_ALREADY_COMPLETE` may Step 9 continue to the legacy helper/marker
  branch:

  ```bash
  test ! -e "$WRFR_HELPER_PLAN"
  test ! -L "$WRFR_HELPER_PLAN"
  ```

  Alias absence is the terminal desired state, so the two passing tests skip
  `remove-owned-helper-plan`. If either test fails, stop; do not delete the
  reappeared, unproved path. Do not call `restore-shared-marker`: incident
  recovery has proved the exact successor `.gitignore` absent, while the old
  restoration command was inapplicable to its mode-`0644` incident identity.

  The existing subagent-driven development finish procedure may then run as the
  separate later operation that removes this Plan's canonical SDD workspace.
  Prove that exact workspace absent, the marker's recorded initial state remains
  absent, and every sibling/primary-checkout change remains untouched. Creation,
  execution, and later deletion of the temporary recovery executable each
  require their own recorded authority; no such action occurs in this
  correction.

## Verification Plan

| Spec criterion | Work package | Deterministic evidence |
| --- | --- | --- |
| VAL-WRFR-001 | WRFR-001 | Exact request union `001..036`, no duplicate or extra row |
| VAL-WRFR-002 | WRFR-001, 002..006 | Dual external/workspace record for every row |
| VAL-WRFR-003 | WRFR-001 | Human-request-to-owner coverage matrix exact |
| VAL-WRFR-004 | WRFR-001, 002..007 | Source-fidelity reviews and source-row schema |
| VAL-WRFR-005 | WRFR-001, 002..006 | Selector existence and evidence-depth checks |
| VAL-WRFR-006 | WRFR-001, 007 | Closed outcome vocabulary and mutation fixtures |
| VAL-WRFR-007 | WRFR-001, 007 | Blocking-class and safe-follow-up completeness |
| VAL-WRFR-008 | WRFR-002..008 | Pack inventory unchanged at fourteen files; no duplicate owner |
| VAL-WRFR-009 | WRFR-001, 007 | Source sequence from 091 and claim block 013 exact |
| VAL-WRFR-010 | WRFR-007..009 | Pack, ledger, scopes, indexes, lifecycle, and progress agree |
| VAL-WRFR-011 | WRFR-006, 009 | Nine-class sanitized remote summary and security reviews |
| VAL-WRFR-012 | WRFR-000, 009 | Foreign state untouched; exact SDD workspace absent after finish |
| VAL-WRFR-013 | WRFR-000..009 | Per-task commit and clean task review |
| VAL-WRFR-014 | WRFR-009 | Whole-branch review with no open Critical/Important finding |
| VAL-WRFR-015 | WRFR-009 | Terminal affected/staged/pre-commit/all-files/aggregate/diff sequence |

Every work package runs its focused checks before commit and committed-diff
review. WRFR-009
runs the entire canonical lane twice: once before closure mutation and once after
the lifecycle evidence is final. The second complete run is authoritative.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Repeating a no-op static cycle | Record concise unchanged evidence and cite the existing blocking-class closure |
| Duplicate owner or identifier collision | Closed 36-row corpus, five disjoint reports, one immutable allocation map, one shared-ledger writer |
| External source relocation mistaken for disappearance | Classify redirects/replacements as `superseded`; retain both identities |
| Temporary source outage recorded as unchanged | Bounded fallback and explicit `unreachable` outcome |
| Search snippet treated as evidence | Require original official page or exact official repository revision before adoption |
| Paid standard overclaim | Limit catalog evidence to edition, status, and public scope |
| Runtime effect inferred from static configuration | Evidence-depth field and retained blocking class are mandatory |
| Remote GitHub output leaks sensitive data | Pre-review, exact argv allowlist, checker-owned projection, mode 0600 guarded summary, no raw log/body/token |
| Remote query failure causes retries or fallback drift | One request per class; local fixed unavailable record only; no query retry |
| Shared ledger formatting rewrites historical rows | Append-only region check and explicit old-byte preservation probe |
| Workstream agents collide on files or IDs | Read-only evidence agents; sequential integration; immutable allocation slices |
| Primary checkout's RIA staging is captured | Isolated worktree, merge-base scope, explicit foreign-state prohibition |
| Cleanup removes foreign evidence | Exact Plan-owned SDD workspace only; sibling and `/tmp` artifacts excluded |
| Closure changes escape affected coverage | Regenerate and replay affected/staged lanes after lifecycle mutation |

## Completion Criteria

- Exact thirty-six-row external and workspace observation union, with zero
  missing, duplicate, or extra owner.
- Every user-requested category and sub-area maps to a current canonical owner.
- Every adopted technical claim has reviewed primary-source support, exact
  workspace selectors, evidence depth, rejected inference, and refresh trigger.
- Changed, unchanged, unreachable, superseded, and contradicted evidence is
  distinguishable and historically additive.
- Existing pack remains fourteen Markdown files; no new research folder, topic
  report, parallel ledger, or request owner exists.
- New sources begin at `SRC-WERPC-091`; new claims form contiguous block
  `CLM-WERPC-013-NN`; every ID is referenced exactly as designed.
- Pack, source/claim ledger, ten scopes, collection index, lifecycle records,
  and durable progress agree on terminal counts and status.
- All task-scoped reviews and the whole-branch review have no unresolved
  Critical or Important finding.
- Terminal affected, staged, pre-commit, all-files, aggregate, formatter-review,
  and diff-check sequence passes on the final committed tree.
- Task-owned SDD workspace is removed after final review; foreign workspaces,
  primary-checkout staged RIA changes, and external systems remain untouched.
- No secret, live cluster, provider runtime, hosted execution, deployment,
  publication, push, or merge result is claimed.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WRFR-001](spec.md) | WRFR-001 | [WRFR-001](tasks.md) records exact 36-row union |
| [VAL-WRFR-002](spec.md) | WRFR-001..007 | [WRFR-001..007](tasks.md) record dual evidence |
| [VAL-WRFR-003](spec.md) | WRFR-001 | [WRFR-001](tasks.md) records request coverage |
| [VAL-WRFR-004](spec.md) | WRFR-001..007 | [WRFR-001..007](tasks.md) record source reviews |
| [VAL-WRFR-005](spec.md) | WRFR-001..006 | [WRFR-001..006](tasks.md) record selector checks |
| [VAL-WRFR-006](spec.md) | WRFR-001, 007 | [WRFR-001](tasks.md) records vocabulary mutation tests |
| [VAL-WRFR-007](spec.md) | WRFR-001, 007 | [WRFR-007](tasks.md) records every retained boundary |
| [VAL-WRFR-008](spec.md) | WRFR-002..008 | [WRFR-008](tasks.md) records terminal pack inventory |
| [VAL-WRFR-009](spec.md) | WRFR-001, 007 | [WRFR-007](tasks.md) records ID continuity |
| [VAL-WRFR-010](spec.md) | WRFR-007..009 | [WRFR-009](tasks.md) records projection agreement |
| [VAL-WRFR-011](spec.md) | WRFR-006, 009 | [WRFR-006](tasks.md) records remote/security evidence |
| [VAL-WRFR-012](spec.md) | WRFR-000, 009 | [WRFR-009](tasks.md) records owned residue absence |
| [VAL-WRFR-013](spec.md) | WRFR-000..009 | [WRFR-000..009](tasks.md) record commits/reviews |
| [VAL-WRFR-014](spec.md) | WRFR-009 | [WRFR-009](tasks.md) records whole-branch verdict |
| [VAL-WRFR-015](spec.md) | WRFR-009 | [WRFR-009](tasks.md) records terminal lanes |

### Related Documents

- [Spec 0062](spec.md)
- [Reciprocal Task](tasks.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
