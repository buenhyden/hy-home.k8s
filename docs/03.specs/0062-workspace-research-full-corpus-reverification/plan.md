---
title: 'Workspace Research Full-Corpus Reverification Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-20
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

The canonical Plan remains the registry-routed `plan.md`, so SDD helpers use
one exact Plan-owned alias,
`/tmp/0062-workspace-research-full-corpus-reverification-plan.md`. The alias is
a byte-identical current-user mode-`0600` regular file, never a symlink. Its
unique basename makes the helper workspace
`.superpowers/sdd/0062-workspace-research-full-corpus-reverification-plan/`.
Before every `task-brief` call, synchronize the alias from canonical `plan.md`.
Task 1 and Task 2 use the exact bootstrap sequence in WRFR-000; after the
checker exists, its guarded `helper-sync` subcommand owns every refresh. All
helper calls receive explicit output paths under the unique workspace and run
with `umask 077`.

Before the checker exists, WRFR-000 records every helper-returned artifact path
in `progress.md` after resolving it under the exact SDD root, rejecting a
symlink or non-regular file, confirming current-user ownership, and setting
mode `0600`. WRFR-001 initializes `artifact-inventory.json` from that exact
record and then registers the checker and inventory itself. Thereafter, every
`task-brief` and `review-package` result and every named output is registered
immediately through the checker before another consumer runs. Registration is
version-bound and fails on an outside-root path, duplicate, missing file,
symlink, wrong owner, wrong mode, or unapproved artifact class.

The terminal residue check requires directory contents and inventory to be
equal. The SDD finish procedure runs only after the final consumer, removes
only the exact resolved Plan workspace, and proves that exact path absent. The
checker removes the exact helper Plan alias after its final helper consumer and
proves it absent. The shared parent `.superpowers/sdd/.gitignore` is
helper-owned, not Plan-owned: before the first helper call it must be absent or
a current-user regular non-symlink containing exactly `*\n`; its prior state is
recorded. After the final helper call, an initially existing marker must remain
byte-identical. An initially absent marker is removed only after verifying it is
still current-user, regular, non-symlink, exact `*\n`, and the Plan workspace is
the only remaining SDD child; a foreign sibling makes cleanup fail closed. The
terminal state must equal the recorded initial state.

For every Task, the controller records `WRFR_TASK_BASE=$(git rev-parse HEAD)`
before dispatch. The implementer completes focused validation and commits the
logical unit before returning its report. Only then does the controller run
`review-package` over `WRFR_TASK_BASE..HEAD` with an explicit, absent output
path in the SDD workspace and dispatch the task reviewer. A required fix is a
new scoped commit followed by a new review package from the same original base
through the new `HEAD` and one scoped re-review. The successor Task is not
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

The predecessor [Spec 0059](../0059-workspace-research-full-corpus-refresh/spec.md)
completed a full-corpus observation on 2026-08-17 and corrected one Kubernetes
claim on 2026-08-18. The current pack contains fourteen Markdown files,
thirty-six owners, ninety source IDs, and one hundred thirty-five claim IDs. Its
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
- Modify: `docs/99.templates/support/document-profiles.json`
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
    docs/99.templates/support/document-profiles.json \
    scripts/validate-links-and-owners.py \
    tests/test_document_strict_cutover.py \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: activate full-corpus research reverification"
  ```

- [ ] **Step 6: review the committed activation and prepare Task 2**

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

- [ ] **Step 1: write the checker self-test before implementation**

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

- [ ] **Step 2: implement and verify the guarded checker**

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

- [ ] **Step 3: capture the exact baseline**

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

- [ ] **Step 4: dispatch five read-only research agents**

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

- [ ] **Step 5: independently review each research report**

  Dispatch one source-fidelity reviewer per workstream and one cross-workstream
  quality reviewer after all five reports exist. Reviews check source identity,
  checked-on date, claim support, selector existence, evidence depth, exact row
  membership, duplicate research, and DEFER boundaries. Resolve every Critical
  or Important finding in the report and re-review before allocation.

- [ ] **Step 6: validate the union and allocate IDs**

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

- [ ] **Step 7: update execution evidence and run focused checks**

  Mark `WRFR-001` Done in the Task only after the reviews and allocation pass.
  Record the exact observed counts, hashes, review verdicts, source-access
  failures, and out-of-ledger observations. Update Plan checkboxes for completed
  steps and durable progress with next owner `WRFR-002`.

  ```bash
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

- [ ] **Step 8: commit and review evidence intake**

  ```bash
  git add docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: record full-corpus research evidence intake"
  ```

  Generate the committed `WRFR_TASK_BASE..HEAD` package and dispatch the task
  reviewer. Resolve Critical or Important findings with a scoped fix commit and
  re-review before Task 3.

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

- [ ] **Step 1: reproduce the missing-section RED**

  Use a read-only probe that requires the exact dated H3 in all four owner files
  and the exact nine request IDs in the report. Expected before edits: four
  missing-section diagnostics and exit 1.

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . \
    --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" \
    --workstream agent-engineering
  ```

- [ ] **Step 2: append the agent-engineering findings**

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

- [ ] **Step 3: run agent-focused GREEN checks**

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

- [ ] **Step 4: commit and review agent findings**

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

- [ ] **Step 1: reproduce the two-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream provider-common
  ```

  Expected before edits: two missing-section diagnostics and exit 1.

- [ ] **Step 2: append the provider/common findings**

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

- [ ] **Step 3: run provider-focused GREEN checks**

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

- [ ] **Step 4: commit and review provider findings**

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

- [ ] **Step 1: reproduce the three-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream sdlc-documentation
  ```

  Expected before edits: three missing-section diagnostics and exit 1.

- [ ] **Step 2: append the SDLC and document-family findings**

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

- [ ] **Step 3: run documentation-focused GREEN checks**

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

- [ ] **Step 4: commit and review SDLC findings**

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

- [ ] **Step 1: reproduce the platform-owner RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream platform-security
  ```

  Expected before edits: one missing-section diagnostic and exit 1.

- [ ] **Step 2: append the platform and security findings**

  The dated H3 must distinguish Kubernetes desired state, infrastructure
  scripts/contracts, and security controls. Reverify RBAC least privilege,
  Secret API exposure, service-account tokens, workload hardening, NetworkPolicy,
  admission, GitOps revision identity, Helm provenance, image digests, signatures,
  attestations, SLSA provenance, Vault/ESO identity, and recovery evidence.

  Compare official sources with exact repository selectors. Do not run `kubectl`,
  `k3d`, `helm`, `argocd`, `vault`, `docker`, a registry client, or any live
  infrastructure command. Never inspect a Secret value.

- [ ] **Step 3: run platform-focused GREEN checks**

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

- [ ] **Step 4: commit platform findings**

  ```bash
  git add docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md \
    docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md \
    docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git commit -m "docs: reverify platform and security research"
  ```

- [ ] **Step 5: review the committed platform findings**

  Generate the committed package and dispatch source-fidelity, task, and
  `security-reviewer` reviews. The security review must verify no secret payload,
  live command, identity mutation, unbounded permission claim, or supply-chain
  equivalence entered the report. Resolve every Critical or Important finding
  in a scoped fix commit and re-review before Task 7.

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

- [ ] **Step 1: obtain pre-remote security approval**

  Before any `gh` or GitHub API command, dispatch `security-reviewer` with the
  exact repository, branch, the two preflight argv vectors from Step 3, the nine
  evidence-query argv vectors from Step 4, every projected field, stdout/stderr
  treatment, timeout, one-query-per-class budget, guarded output contract, and
  no-retry rule. The reviewer must approve both preflight output minimization and
  the checker's per-class documented-unavailable path. Stop remote evidence
  collection if that review reports an unresolved Critical or Important issue.

- [ ] **Step 2: reproduce local and remote RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream delivery-quality
  python3 "$WRFR_SDD/full-corpus-check.py" remote-validate \
    --summary "$WRFR_SDD/remote-github-summary.json"
  ```

  Expected before edits/initialization: one missing-section diagnostic and one
  missing guarded summary diagnostic.

- [ ] **Step 3: initialize and verify the remote target**

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

- [ ] **Step 4: run each approved remote query once**

  Invoke every query through `remote-query`; the checker verifies the argv,
  applies a bounded timeout, projects only the named fields, and performs a
  version-bound atomic update. The exact evidence classes and argv are:

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

- [ ] **Step 5: validate the remote summary**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" remote-validate \
    --summary "$WRFR_SDD/remote-github-summary.json"
  ```

  Expected: exactly nine unique evidence classes, every class either sanitized
  metadata or explicit unavailable, no raw URLs other than the approved repo
  identity, no token/log/body field, and no evidence tied to a revision other
  than the returned `headSha` values.

- [ ] **Step 6: append the delivery and quality findings**

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

- [ ] **Step 7: run delivery-focused GREEN checks**

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

- [ ] **Step 8: commit and review delivery findings**

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

- [ ] **Step 1: reproduce ledger and projection RED**

  ```bash
  python3 "$WRFR_SDD/full-corpus-check.py" validate-integration \
    --root . --baseline "$WRFR_SDD/baseline.json" \
    --allocation "$WRFR_SDD/allocation.json" --workstream shared-ledger
  ```

  Expected before shared integration: allocated source/claim IDs absent from the
  ledger, scope projection absent, and pack counts still at the baseline.

- [ ] **Step 2: append source and claim records**

  Use `allocation.json` exactly. Append sources in numeric order, then append the
  `CLM-WERPC-013-NN` cycle block in numeric order. Each source row contains owner,
  official URL/revision, source class, checked-on date, adopted scope, rejected
  scope, uncertainty, and trigger. Each claim row contains request owner, claim,
  source IDs, exact workspace selectors, evidence depth, disposition, missing
  evidence, safe boundary, owner, and trigger.

  Preserve every pre-existing row byte-for-byte. If Markdown table formatting
  would rewrite old rows, stop and switch to an append operation that touches
  only the new section; do not accept mechanical whole-ledger reflow.

- [ ] **Step 3: re-project the ten governance scopes**

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

- [ ] **Step 4: reconcile the pack README**

  Append a dated reconciliation section with exact terminal file/request/source/
  claim counts, external outcome distribution, workspace outcome distribution,
  disposition distribution, changed request IDs, corrections, unreachable
  sources, out-of-ledger observations, and retained blocking-class distribution.

  Update only mutable snapshot/count cells that are contractually current. Do
  not rewrite earlier dated reconciliation sections.

- [ ] **Step 5: validate shared integration**

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

- [ ] **Step 6: commit and review shared integration**

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

### Task 9: WRFR-008 — cross-link and lifecycle reconciliation

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`
- Modify: `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Modify: `docs/99.templates/support/document-profiles.json`
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
    docs/99.templates/support/document-profiles.json \
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
- Modify: `docs/99.templates/support/document-profiles.json`
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
    docs/99.templates/support/document-profiles.json \
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
  python3 "$WRFR_SDD/full-corpus-check.py" restore-shared-marker \
    --workspace "$WRFR_SDD" \
    --bootstrap-ledger "$WRFR_SDD/progress.md"
  python3 "$WRFR_SDD/full-corpus-check.py" remove-owned-helper-plan \
    --path "$WRFR_HELPER_PLAN"
  test ! -e "$WRFR_HELPER_PLAN"
  test ! -L "$WRFR_HELPER_PLAN"
  ```

  Record final `HEAD`, status, commit list, counts, artifact inventory, and
  review verdict in the SDD ledger. After the final scoped re-review has no open
  Critical or Important finding, delete only this Plan's SDD workspace via the
  subagent-driven development finish procedure and verify that exact path is
  absent. Verify the shared marker state equals its recorded initial state. If a
  foreign sibling prevents safe restoration, stop with an explicit cleanup
  blocker instead of deleting or claiming completion. Leave every sibling SDD
  workspace and every primary-checkout change untouched.

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
