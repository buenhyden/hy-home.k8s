---
title: 'Workspace Research Full-Corpus Reverification Task'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-22
artifact_id: "TASK-0062"
---

# Workspace Research Full-Corpus Reverification Task (Task)

## Overview

This Task is the execution ledger for `WRFR-000` through `WRFR-009` in the
reciprocal [Plan](plan.md), implementing [Spec 0062](spec.md). Direct human
approval on 2026-08-20 activates the standalone execution relation. The
activation commit is `docs: activate full-corpus research reverification`.
`WRFR-001` completed closed-corpus evidence intake, allocation, three disjoint
registered review packages, and independent task review. The first helper-loss
Package B used a checker-rejected basename; its bounded cleanup and evidence
limitations remain recorded below. Regenerated Packages B/C passed registration
and residue validation, and the reviewer approved Task 2 with no findings.
The first WRFR-002 integration probe then exposed an allocation-order checker
defect before any owner edit. The reviewed checker-only recovery completed,
the accepted fail-fast RED became `ERROR INTEGRATION_SECTION`, and WRFR-002
integrated all nine agent-engineering rows. Its tracked commit and post-commit
task review are complete; the sole stale-evidence Minor is corrected in this
closure unit. WRFR-003 has integrated all four provider/common rows, resolved
one source-boundary review finding, and passed its focused repository-static
validators and both independent pre-commit reviews. Its exact five-file commit,
registered report/package, and post-commit review are complete; the sole stale-
evidence Minor is corrected in this closure unit. WRFR-004 has integrated all
sixteen SDLC/documentation rows into the three existing owners. Its exact
six-file commit, registered report/package, and post-commit review are complete;
the sole stale-evidence Minor is corrected in this closure unit. WRFR-005 has
integrated its exact three-row platform/security slice into the existing owner;
focused static validators and three independent pre-commit reviews approve the
content. Its exact implementation commit, guarded report/package, and
post-commit task review are complete; the sole stale lifecycle Minor is
corrected in this closure unit. WRFR-006 passed its pre-remote review, both
fixed local recoveries, and the one-shot remote sequence. Its nine-class
sanitized summary passed remote validation; seven classes are observed while
`workflows` and `oidc` retain their fixed checker-compatibility unavailable
reasons. The existing delivery/quality owner now contains the single dated
four-row increment and all focused GREEN checks pass. Its exact implementation
commit, registered report/package, and post-commit review are complete; the
sole intentional pre-closure lifecycle Minor is corrected in this closure.
WRFR-006 is complete. WRFR-007 preserves the reviewed checker-only recovery,
the Stage 90 transition-guard recovery, the semantic shared-ledger RED, and the
exact six-file shared projection commit. Its ledger/source content review
remains approved, but task/spec re-review found one Important pre-dispatch
provenance gap, so WRFR-007 is blocked pending explicit human direction.
WRFR-008 remains queued and blocked behind that decision. No remote retry is
permitted.

The target is a 2026-08-20 external-source and workspace reverification of all
thirty-six existing `REQ-WERPC-*` owners, integrated into the existing
`2026-08-08-wer` pack. The WRFR-001 implementation and evidence commit are
complete: guarded checker construction and direct review, artifact-inventory
initialization and recovery, immutable baseline capture, five reviewed
closed-corpus reports, exact-union validation, and final ID allocation all
completed in the ignored SDD workspace. Its independent task-level
spec-compliance and quality review is approved. During WRFR-001, no remote
GitHub query, provider runtime, hosted CI, live infrastructure, or human
validation occurred.
WRFR-002 changed only its four topical owners and three lifecycle records.
WRFR-003 is limited to its two topical owners and the same three lifecycle
records. WRFR-004 is limited to its three topical owners and those lifecycle
records. WRFR-005 is limited to its one topical owner and those lifecycle
records. WRFR-006 has executed its approved pre-remote review, two RED probes,
two preflights, summary initialization/registration, both reviewed local
recoveries, and exactly one approved query budget per class. The final summary,
owner edit, focused GREEN evidence, exact commit, registered report/package,
and post-commit review are complete. WRFR-007 preserves its checker recovery and
shared ledger/scope/pack integration, but its prior task/spec approval is
withdrawn for the recorded Important provenance finding. WRFR-008 and later
work packages have not executed and remain blocked behind human direction.

## Inputs

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Research collection contract](../../90.references/research/README.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)

### Approved design baseline

| Field | Baseline |
| --- | --- |
| Canonical research pack | `docs/90.references/research/2026-08-08-wer/` |
| Pack Markdown files | 14 |
| Request owners | 36, exact IDs `001..036` |
| Source IDs | 90, terminal `SRC-WERPC-090` |
| Claim IDs | 135, terminal `CLM-WERPC-012-04` |
| New source start | `SRC-WERPC-091` |
| New claim block | `CLM-WERPC-013-NN`, starting `01` |
| Matrix states | 23 `Verified`, 1 `Verified gap`, 12 `Partial` |
| Evidence date | 2026-08-20 |
| Execution branch | `codex/2026-08-20-full-corpus-reverification` |
| Design commit | `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` |

### Closed workstream assignment

| Workstream | Exact request IDs | Topical owners |
| --- | --- | --- |
| Agent engineering | 001, 002, 026–032 | harness/loop, agents, model, memory |
| Provider/common | 003–006 | workspace governance, provider status |
| SDLC/documentation | 007, 010–021, 034–036 | SDLC/contracts, Diataxis, LLM-WIKI |
| Platform/security | 008, 009, 025 | Kubernetes/infrastructure/security |
| Delivery/quality | 022–024, 033 | CI/CD, Actions, QA, V&V |

The union is exact and disjoint. Research agents may write only their ignored
structured report. They may not edit repository files, allocate final IDs,
stage, or commit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WRFR-000 | VAL-WRFR-012, 013 | Activate standalone lifecycle and SDD workspace | platform | Done | Activated by direct approval on 2026-08-20 in `docs: activate full-corpus research reverification` | Active standalone Spec/Plan/Task relation; next owner `WRFR-001` |
| WRFR-001 | VAL-WRFR-001..007, 009 | Freeze baseline, collect five read-only reports, allocate IDs | platform + research agents | Done | Exact 36-row union validated; all report and task reviews approved; one source and six claims allocated; tracked evidence committed | Packages A/B/C registered; final residue passed; task review `APPROVED` with Critical/Important/Minor `0/0/0` |
| WRFR-002 | VAL-WRFR-002..005, 008, 013 | Integrate agent engineering findings | agent integrator | Done | Nine allocated rows appended and committed as `06b3d681`; registered post-commit review approved | Report/package registered; task review `APPROVED WITH MINOR`, Critical/Important/Minor `0/0/1`; sole stale-evidence Minor addressed |
| WRFR-003 | VAL-WRFR-002..005, 008, 013 | Integrate provider/common findings | provider integrator | Done | Four allocated rows appended and committed as `a41def9e`; registered post-commit review approved | Report/package registered; task review `APPROVED WITH MINOR`, Critical/Important/Minor `0/0/1`; sole stale-evidence Minor addressed |
| WRFR-004 | VAL-WRFR-002..005, 008, 013 | Integrate SDLC/documentation findings | documentation integrator | Done | Sixteen allocated rows appended and committed as `7bbe6517`; registered post-commit review approved | Report/package registered; task review `APPROVED WITH MINOR`, Critical/Important/Minor `0/0/1`; sole stale-evidence Minor addressed |
| WRFR-005 | VAL-WRFR-002..005, 008, 013 | Integrate platform/security findings | platform/security integrator | Done | Three allocated rows appended and committed as `63efc8de`; registered post-commit review approved | Report/package registered; task review `APPROVED WITH MINOR`, Critical/Important/Minor `0/0/1`; sole stale-evidence Minor addressed |
| WRFR-006 | VAL-WRFR-002..005, 008, 011, 013 | Integrate delivery/quality and read-only GitHub evidence | delivery/security integrator | Done | Nine-class summary and four-row owner integration committed as `ae7a2262`; registered post-commit review approved | Report/package registered; task review `APPROVED WITH MINOR`, Critical/Important/Minor `0/0/1`; sole lifecycle Minor addressed |
| WRFR-007 | VAL-WRFR-006..010, 013 | Integrate source, claim, scope, and pack projections | explicit human decision | Blocked | Integration commit `fef53976` and content evidence preserved; late brief cannot prove pre-dispatch consumption | Task/spec re-review withdrawn with Critical/Important/Minor `0/1/0`; ledger/source content review remains `APPROVED` `0/0/0` |
| WRFR-008 | VAL-WRFR-008, 010, 013 | Reconcile indexes, links, lifecycle, and progress | documentation integrator | Queued (Blocked) | Not executed | No reconciliation preprobe before the WRFR-007 provenance decision |
| WRFR-009 | VAL-WRFR-010, 012..015 | Run terminal lanes, whole-branch review, closure, cleanup | platform + QA | Queued (Blocked) | Not executed | Awaiting WRFR-008 and a separately approved SDD cleanup-recovery gate for the foreign sibling and invalidated marker FileVersion |

## Approval and Safety Boundaries

- **Allowed Paths**: the exact files listed under each Plan work package and
  this Plan's existing unique ignored SDD workspace. The historical temporary
  alias `/tmp/0062-workspace-research-full-corpus-reverification-plan.md` is no
  longer an allowed mutation surface and must remain absent/non-symlink.
- **Forbidden Paths**: any new research directory or topic report; policy,
  manifest, workflow, application, runtime, credential, secret, primary-checkout
  staged RIA, sibling worktree, sibling SDD workspace, and unlisted `/tmp` path.
- **Shared helper marker**: `.superpowers/sdd/.gitignore` was initially absent.
  The current marker is the exact recorded current-user regular non-symlink with
  bytes `*\n` and the recorded FileVersion, but mode `0644`; do not chmod it,
  update provenance, or call `restore-shared-marker`. After every consumer and
  SDD finish precondition completes, only a separately reviewed fd-bound cleanup
  may remove that exact identity, and only with no foreign sibling. Any mismatch
  stops fail-closed without generic deletion or a completion claim.
- **Approval Required**: written Plan approval before WRFR-000; pre-remote
  security approval before any GitHub query; human finishing choice before push,
  merge, publication, branch deletion, or worktree cleanup.
- **External Research**: read-only official/primary-source retrieval; search is a
  locator and never substitutes for reading the source.
- **Remote GitHub**: exactly the nine Plan allowlisted metadata classes, at most
  once each, through the guarded checker. The `workflows` and `oidc` budgets are
  consumed and may be recovered only through their respective fixed local-only
  interfaces. The six intervening classes are complete and immutable;
  `artifacts` alone retains one query budget. No preflight or class rerun,
  dispatch, approval, merge, settings mutation, raw logs, tokens, or
  secret-bearing data.
- **Static Validation**: task-local closed-corpus checker, domain validators,
  document registry, Markdown profiles, links/owners, RIA, affected/staged lanes,
  aggregate quality, pre-commit, all-files, formatter review, and diff checks.
- **Live Validation**: `DEFER`; no live cluster, infrastructure, provider runtime,
  deployment, user, operator, or stakeholder activity is authorized.
- **Secret / Vault Handling**: no secret value, token, credential, raw workflow
  log, Vault payload, or recovery material may be read, printed, or stored.
- **Rollback Plan**: revert the exact logical commit for a tracked work package;
  no remote or live state exists to roll back. Guarded ignored artifacts remain
  available until their final consumer and are then removed with exact-path
  absence proof.
- **Evidence Location**: durable results in this Task, pack owners, source/claim
  ledger, scope index, Stage 03 index, ADR 0022, and durable progress; transient
  reports/review packages in this Plan's ignored SDD workspace only.

### WRFR-001 one-time inventory recovery amendment

Direct review changed the registered checker and appended its evidence to the
registered Task 2 report. Because the inventory binds immutable files through
device, inode, size, `mtime_ns`, `ctime_ns`, and SHA-256, truncating the report
back to its bound 32217-byte prefix cannot restore its former `ctime_ns` and is
forbidden. The sole recovery is the Plan-defined
`artifact-rebind-checker-review` command. It has no target argument and may
replace only the existing `full-corpus-check.py` and `task-2-report.md` records,
at the same two indices, in one inventory CAS.

Before fresh direct review, the controller must complete steps 1–3 below. Step
4 then obtains the required approvals. All four steps must complete before any
stateful recovery; after the report is frozen in step 2, direct-review approval
evidence goes only to mutable `progress.md`:

1. summarize all post-registration Task 2 review evidence in mutable
   `progress.md`;
2. append this amendment and final recovery-review evidence to
   `task-2-report.md`, capture its approved SHA-256, and freeze that report
   permanently;
3. record the exact inventory SHA-256, old checker SHA-256, approved new checker
   SHA-256, old report SHA-256
   `75f08066115632b145d7f210f6de4ab91029b180a5923c9337272c35893afa0b`,
   and approved frozen-report SHA-256;
4. obtain fresh Python and security direct approval for the amended tracked
   contract, exact checker bytes, full normal/optimized self-test output, and
   frozen report identity.

The stateful command is authorized only after those approvals. It validates
the exact inventory path/digest/schema, both old records, both guarded new
targets, every other immutable artifact's complete registered FileVersion, and
both mutable entries. It replaces exactly two same-index records, uses the old
complete inventory FileVersion for CAS, re-reads both targets before and after
CAS, postvalidates the exact new inventory, and rolls back exact old inventory
bytes only against the exact CAS-returned new FileVersion. Concurrent update or
rollback failure is preserved and fails closed. `artifact-register` remains
unchanged, duplicate registration remains rejected, no generic report rebind
exists, and all later WRFR-001 evidence goes only to mutable `progress.md`.

### WRFR-001 helper workflow after alias loss

On 2026-08-21 the exact helper Plan alias
`/tmp/0062-workspace-research-full-corpus-reverification-plan.md` was observed
absent and non-symlink after its created FileVersion had been recorded. No cause
is proved. The alias must remain absent, must not be recreated or synchronized,
and is not an input to any remaining helper call. The existing exact SDD
workspace remains current-user-owned, non-symlink, and mode `0700`.

The pre-amendment Task 2 commit sequence after base
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c` is
`ab1dcbae4b0b85a20e6b8c2236249ffa6559ca1f`,
`ce74dc29c3be4fd5a4198bafd01998881ffdd969`,
`19c270b17f8b8e303516eea8da68bf852d229e6f`, and
`802193d33a08423f055615b621fb2667b0a99a1e`. The evidence implementation and
commit are complete, the helper-loss amendment is commit `2716ce9f`, and the
artifact-class correction is commit `4f25be8b`. The checker-admitted replacement
packages and independent task review are complete. That review originally
unblocked dispatch, but `WRFR-002` is now blocked by the later allocation-order
checker defect and has not edited a tracked owner.

The shared branch then received two separately owned remediation commits:
`a8fffa6100b3178337cb72deaf56e24c7f14d008` modifies only the Spec 0059 Task,
and `09f7cf1d70f7f533f7323343bad8de02c1ace3f4` modifies only
`.secrets.baseline`. They are outside WRFR-001 implementation evidence and
retain their separate owners and reviews. The three disjoint package ranges
below exclude both remediation commits from WRFR-001 evidence.

Package A is already registered as `task-2-review-package.md`, SHA-256
`5ab1b0da2e51f8c2ece16a43265e2e3c02633bb969f4fc65d20b6799991867ec`,
for range `8d8c8e56..802193d3`; its registration produced inventory SHA-256
`255628ef76ca95e3dd1b41797bd58089c12fa06fc0a4a764672c683ff3cc46b5`.
Neither identity may be regenerated or rebound.

The first Package B generation used basename
`task-2-helper-loss-fix-review-package.md` for range
`09f7cf1d..2716ce9f`. It created one current-user mode-`0600` 50,861-byte
regular non-symlink with SHA-256
`84776c9a4343572cb0bb0ef8c6cb634f7d30abbadf42ede1b3ee9799b71795bb`,
but registration failed exactly with `ERROR ARTIFACT_CLASS`. No reviewer
consumed it, the inventory remained at the Package A hash above, and no retry
occurred. Before regeneration, the controller used `stat` to verify regular
type, mode `0600`, owner `hy`, and size `50861`, confirmed the SHA-256 above,
ran `test ! -L`, and proved the exact basename absent from inventory. It then
ran `rm -f` against the exact absolute path and proved that path absent and
`residue` PASS. Package A and inventory hashes remained unchanged.

The cleanup did not record device, inode, `mtime_ns`, or `ctime_ns`, retain a
complete FileVersion, or unlink through a bound directory descriptor. It does
not prove same-file continuity between the checks and `rm -f`; that residual
limitation remains explicit. This exception authorizes no further deletion or
retry.

After the correction was committed directly on `2716ce9f`, the controller
created regenerated Package B for the earlier helper-loss amendment and a
separate Package C for this correction. Before each call it independently
guarded-reads and freezes the canonical Plan and applies every explicit-output
precondition in Plan Task 2 Step 9, then runs exactly:

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

The canonical Plan and each generated output are postvalidated before reviewer
dispatch. Neither call may invoke `sdd-workspace`, use a default output,
recreate the alias, or invoke `helper-sync`. Registered Package A, regenerated
Package B, and Package C go together to the same task reviewer. Package B is
exactly `09f7cf1d..2716ce9f`; Package C is exactly
`2716ce9f..WRFR_CORRECTION_HEAD`. Neither range may be widened or conflated, and
the separately owned `a8fffa61` and `09f7cf1d` baseline fixes remain outside
Task 2 evidence. Terminal alias cleanup skips
`remove-owned-helper-plan` only while the alias remains absent/non-symlink; a
reappearance stops execution without deletion. The initially absent shared
marker remains the exact recorded helper-created identity with bytes `*\n` and
mode `0644`. It is not repaired now. Its only authorized terminal removal is
the separately reviewed fd-bound, exact-identity, no-foreign-sibling procedure
in the Plan.

The final registered review identities are:

| Package | Exact range | SHA-256 |
| --- | --- | --- |
| `task-2-review-package.md` | `8d8c8e56..802193d3` | `5ab1b0da2e51f8c2ece16a43265e2e3c02633bb969f4fc65d20b6799991867ec` |
| `task-2-fix-1-review-package.md` | `09f7cf1d..2716ce9f` | `84776c9a4343572cb0bb0ef8c6cb634f7d30abbadf42ede1b3ee9799b71795bb` |
| `task-2-fix-2-review-package.md` | `2716ce9f..4f25be8b` | `81700dd345b9940c433cd8fb7d6e84a5506109c71547353753f5bec4e8dcfd11` |

The final registered inventory SHA-256 is
`021421d7341679884fed0976060465a5022c4ba72acc38e19c95cbf52d7038a4`,
and final `residue` returned `PASS`. The same independent Task 2 reviewer
consumed all three registered packages and returned `APPROVED` with
Critical/Important/Minor `0/0/0`, explicitly unblocking `WRFR-002`. The final
`pre-commit run --all-files` rerun exited `0`; every hook passed and reported no
mutation.

### WRFR-002 allocation-order checker recovery

The Task 3 base is
`e8edd3fddb4171aad634ee31a278d136fd3e4529`. Its registered brief is
`task-3-brief.md`, SHA-256
`0a04b10fadaa25f798e5b8648bc818c026d9c417dfe0f1d54a90370b82bb2de3`;
registration produced inventory SHA-256
`79bd0803f575a594a7f7b9ee3dc59a9100c09790668c6cf438866c91ade49f63`.
The first actual integration RED on 2026-08-21 returned exactly
`ERROR ALLOCATION_REFERENCE`. The implementer was paused and touched no
tracked file.

The defect is limited to the checker's final row-reference comparison. The
registered allocation's global claims are `013-01..06`, while request-row
traversal sees the same unique complete membership in order
`013-04,05,01,02,03,06`. The correction compares exact cardinality,
uniqueness, and sorted membership and preserves per-row owner checks. A new
real self-test accepts non-global row insertion order and rejects missing,
duplicate, and wrong-owner references.

The Plan's fixed `artifact-rebind-checker-only` command is the sole authorized
recovery. It may update only the same-index `full-corpus-check.py` inventory
record from registered SHA-256
`425b2eac6616cbf986960070b38061d76a6584fa4c139748a97d2c6da3d3fc7d`
to freshly reviewed SHA-256
`584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d`.
It has no generic target/report argument and validates all non-target records,
full inventory identity, CAS continuity, post-state, and exact rollback
continuity. The frozen Task 2 report stays
`bb5e198e7c99a7c510296d12cf9c7f94eb8af4eed4ea9a6eedec91e085379598`.

The first Python review found one Important race in the generic CAS helper's
post-lock FileVersion read. A new TDD case mutates the inventory immediately
after lock release. The revised helper captures its own replacement version
under the lock, so rollback cannot overwrite those concurrent bytes. The old
reviewed SHA is superseded and its approvals do not apply to the revised bytes.

The revised candidate checker is current-user mode `0600`, 196902 bytes. All 89 named
self-tests pass in normal and optimized mode; `py_compile`, Ruff check, and
Ruff format check pass. The stateful command remains forbidden until fresh
independent Python and security reviewers approve these exact checker bytes and
the tracked Plan/Task/progress contract with no Critical or Important finding.
After the three-document amendment is committed, the controller may execute
the exact Plan tuple once, with no retry. Only a same-index sole-checker delta,
`residue` and both self-test passes, and a post-recovery
`ERROR INTEGRATION_SECTION` from the unchanged Task 3 probe may unblock the
paused implementer. Allocation, baseline, reports, review packages, Task 3
brief, and topical owners remain immutable throughout recovery.

Fresh Python and security reviews approved the final checker and tracked
recovery contract with no Critical or Important finding. The controller ran
the exact checker-only command once; it exited `0` with no output and was not
retried. Only the checker record changed. The resulting checker SHA-256 is
`584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d`,
inventory SHA-256 is
`befe28f3abe095ac359ff187850e84cdaf5fe2016fa27e0334653ef3e52dbc8f`,
and the frozen report/allocation identities are unchanged. `residue` and all
89 normal/optimized self-tests passed. The unchanged integration probe then
exited `1` with the expected fail-fast `ERROR INTEGRATION_SECTION`, unblocking
owner integration without claiming four simultaneous diagnostics.

### WRFR-006 remote incident and recovery contract

The required pre-remote security review completed `Approved With Minor`,
Critical/Important/Minor `0/0/1`; its sole Minor concerned broad bounded
403/404 recognition. Authentication and repository-identity preflights each ran
once and succeeded. The repository projection was exactly
`buenhyden/hy-home.k8s`, its GitHub HTTPS URL, and default branch `main`; auth
output was discarded. The local and missing-summary RED results were
`ERROR INTEGRATION_SECTION` and `ERROR PATH_INVALID` respectively.

After guarded initialization and registration, the `workflows` class ran exactly
once and stopped at `ERROR REMOTE_COMMAND`. Only sanitized state `failed`, reason
`non-allowlisted-failure`, and empty data were retained. The bounded checker
captured and classified stdout/stderr in memory, but raw output was not exposed
to the controller or a human, copied into evidence, or persisted. Neither
preflight nor `workflows` may be retried, and the other eight classes have not
run. The incident tuple is checker
`584086b297a7446e0a6dea932f0693831a3748813cae6f281bee41eb889c765d`,
summary
`cc77a8ae007b71f32328ce159dd03f60d3a32390131710cb6eee675bdbee4b56`,
and inventory
`1dc24b116bbd09cb8e36f96a0bfb6c332dac8793f15b3cf33cc858efd8c9c22b`.

The child received no GitHub configuration/state locations and created the
repository-local regular file `.local/state/gh/device-id`. Its contents were
not directly inspected by the controller or checker. The exact fixed cleanup
identity uses device `2096`, UID `1000`, common
`mtime_ns`/`ctime_ns` `1787287593754570540`, and these path-specific values:

| Path | Inode | Size | Mode | Exact entry |
| --- | ---: | ---: | ---: | --- |
| `.local` | 1747675 | 4096 | `0755` | `state` |
| `.local/state` | 2221665 | 4096 | `0755` | `gh` |
| `.local/state/gh` | 3263846 | 4096 | `0755` | `device-id` |
| `.local/state/gh/device-id` | 3276459 | 36 | `0600` | regular file; not directly inspected by controller/checker |

The fixed [Plan recovery gate](plan.md#wrfr-006-remote-incident-and-fixed-recovery-gate)
is now authoritative. Its order is: commit this contract; implement the checker
test-first and obtain fresh exact-byte Python/security approvals; run
`artifact-rebind-checker-only` once; run the exact dirfd-bound
`remove-owned-gh-state-residue` once; run the no-network
`remote-recover-auth-context` once; then run only `runs`,
`actions-permissions`, `workflow-permissions`, `rulesets`,
`branch-protection`, `environments`, `oidc`, and `artifacts`, once each in that
order. Recovery preserves the original `observedAt` and converts only the
existing `workflows` record to `unavailable` with reason
`checker-auth-context-incompatible` and empty data.

Every summary mutation uses a registered-summary/inventory compensating CAS.
Summary-only rollback is allowed only when inventory CAS did not commit. After
an inventory commit, later failure compensates inventory first against its
exact returned FileVersion, then summary against its exact returned
FileVersion, and postvalidates the old pair; any drift or compensation failure
is a distinct fail-closed inconsistency because two-file atomic replacement is
unavailable. Cleanup uses literal dirfd traversal,
`O_NOFOLLOW`, complete metadata identity, exact entry sets, `fstat` rechecks,
empty-directory removal, and post-absence proof. The same-UID race window is an
explicit limitation, not an atomicity claim.

Each remaining-query child receives only minimal `PATH`/locale, the fixed
`GH_CONFIG_DIR=/home/hy/.config/gh` and
`XDG_STATE_HOME=/home/hy/.local/state`, plus fixed non-secret prompt, pager,
update-notifier, color, and terminal-prompt controls enumerated by the Plan.
`HOME`, tokens, `GH_HOST`, `GH_REPO`, `GH_DEBUG`, `LD_*`, proxy, `PAGER`,
`XDG_CONFIG_HOME`, and other configuration variables are forbidden. The
controller and checker must not directly read, hash, copy, print, or persist
configuration/state contents. Only the approved `/usr/bin/gh` child may consume
the standard-path bytes for authentication/state operation, without exposing
them through raw output or evidence. The Plan pins the current
metadata-only identities for `/home/hy/.config/gh`, `config.yml`, `hosts.yml`,
and `/home/hy/.local/state/gh/device-id`, including exact directory entries and
pre/post stability. Literal `/home/hy/...` dirfd traversal is required; path
resolution alone is insufficient. `/` and `/home` use the trusted-system-dir
snapshot rule, including user-namespace UID `65534`, no group/world or
current-process write access, and retained-dirfd stability. `/home/hy` onward
requires current UID, no group/world write access, and retained-dirfd stability.
A `config.yml` absence snapshot is valid only as `ENOENT`
both before and after; symlink, appearance, disappearance, metadata change, or
repository `.local` presence fails closed.

At this first incident checkpoint, WRFR-006 was `In Progress`/blocked. No
delivery owner edit, retry, fallback, alternate endpoint, raw-output inspection,
remaining remote query, push, merge, publication, or live action was authorized
before the recovery gate completed.

### WRFR-006 OIDC schema incident and recovery contract

The first recovery gate above completed without a network retry: the approved
checker was rebound, `remove-owned-gh-state-residue` removed the repository
`.local` tree exactly once, `remote-recover-auth-context` converted only the
existing `workflows` record to its fixed local `unavailable` disposition, and
`residue` passed with `.local` absent. The controller then invoked `runs`,
`actions-permissions`, `workflow-permissions`, `rulesets`,
`branch-protection`, and `environments` exactly once each in the approved order,
and each observation was retained through the registered-summary transaction.

The `oidc` class ran exactly once and stopped with `ERROR REMOTE_SCHEMA`. Its
only persisted projection is state `failed`, reason `schema-invalid`, and empty
data. The checker captured and classified the raw response in process memory,
but did not expose it to the controller or a human, copy it, or persist it; the
raw response is no longer available for diagnosis. No retry, fallback,
alternate endpoint, preflight, or `artifacts` query occurred. The second
incident tuple is:

- checker SHA-256
  `31a14c46f18bdaa690360f67d263ad78aa440a8345d76c9160c150ba1b4f56a3`;
- summary SHA-256
  `6255a3734325aab127e81b5730a121c9bf97c38b0611d91c21b9c6f1f7dc9ee2`;
- inventory SHA-256
  `008be406a418348269cf5c58c3becf9cac024ba1db6adf1f430e0d9ae5fd927e`.

GitHub's primary
[OIDC REST documentation](https://docs.github.com/en/rest/actions/oidc)
defines `use_default` as a boolean and `include_claim_keys` as optional and
ignored when `use_default` is true. That contract makes an absent or nullable
claim-key projection plausible, but it does not establish what the lost raw
response contained. The exact cause of this incident therefore remains
unproven. Recovery addresses only the checker's documented compatibility gap;
it does not assert a remote OIDC configuration value.
The fixed jq object always emits `include_claim_keys`, so a missing raw field is
represented as post-projection `null`; a post-projection object without the key
is still rejected.

The sole recovery interface is fixed and accepts no class or reason input:

```text
remote-recover-oidc-schema --workspace DIR --inventory FILE --summary FILE \
  --expected-inventory-sha256 OLD --expected-summary-sha256 OLD
```

At this second incident checkpoint, WRFR-006 remained `In Progress` and
blocked. The next permitted operations were closed and ordered:

1. Commit this three-document amendment before changing ignored checker or
   registered artifact bytes.
2. Extend the checker test-first so the OIDC validator accepts
   `include_claim_keys: null` only when `use_default` is exactly `true`, and add
   the fixed no-network recovery interface above. Compile, run normal and
   optimized self-tests and Ruff, then obtain fresh independent Python and
   security approvals over the exact checker bytes. Any Critical or Important
   finding or later byte change closes the gate.
3. Run `artifact-rebind-checker-only` exactly once against checker
   `31a14c46f18bdaa690360f67d263ad78aa440a8345d76c9160c150ba1b4f56a3`
   and inventory
   `008be406a418348269cf5c58c3becf9cac024ba1db6adf1f430e0d9ae5fd927e`,
   binding only the newly approved checker identity. Do not retry.
4. Invoke `remote-recover-oidc-schema` exactly once against summary
   `6255a3734325aab127e81b5730a121c9bf97c38b0611d91c21b9c6f1f7dc9ee2`
   and the then-current exact inventory identity. It launches no child and
   performs no network access. The query-budget order is the Plan command
   sequence; the persisted class-map order is separately the canonical
   lexicographic `tuple(sorted(REMOTE_CLASSES[:8]))` emitted by
   `_json_bytes(sort_keys=True)` and is not invocation evidence. It preserves
   the summary repository identity, canonical persisted class-map order, all
   seven preceding class records at the parsed data level, the `oidc`
   `observedAt`, and the absence of `artifacts`; it changes
   only `oidc` from `failed` / `schema-invalid` / `{}` to `unavailable` /
   `checker-oidc-schema-incompatible` / `{}`. The existing compensating
   registered-summary/inventory CAS and rollback contract remains mandatory.
5. Prove `.local` absent and run `residue`; then invoke only the untouched
   `artifacts` query exactly once. Prove `.local` absent again, run `residue`,
   and execute `remote-validate`. Neither preflight nor any of the first eight
   classes may be invoked again.

The registered summary and inventory remain untouched until this tracked
contract is committed and the new checker passes exact-byte review. No delivery
owner edit, OIDC conclusion, retry, raw-output inspection, push, merge,
publication, or live mutation is authorized by this amendment.

### WRFR-001 evidence intake completion

This section records completed intake implementation evidence and the approved
task-level post-commit review recorded above.

The exact final registered artifact identities are:

| Artifact | SHA-256 |
| --- | --- |
| `research-agent-engineering.json` | `f0dd1038b056d3f2bdc5e6c5e457e4f3c6cd93cdd5ab75375780101da9eca5b1` |
| `research-provider-common.json` | `bf5728c6d4f69dce90cff533058372e243ffed28ed5b5ee8949444212250ce86` |
| `research-sdlc-documentation.json` | `be273b3dad1b6b4f50d12285cf9114406ba5c3af94ded7646a71ceda5b47ae85` |
| `research-platform-security.json` | `edff89e3b29fdcaa658044ffc768b7c297e39a02936bd39657c90bb759a7fbce` |
| `research-delivery-quality.json` | `f55cc2285577530544c48f26fb497184b43bb9822236e46a736294ed8695d993` |
| `allocation.json` | `04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b` |
| `artifact-inventory.json` | `39ef8f41848340daf9a0756a80611bcb549960080fc4bb5c8007a4ce625c8567` |

All five final source-fidelity reviews returned `Approved`. The final
cross-workstream quality review returned `Approved` with
Critical/Important/Minor `0/0/0`. The reports contain exactly 36 disjoint rows:
external results are 3 `changed`, 32 `unchanged`, and 1 `unreachable`; workspace
results are 29 `confirmed`, 6 `drifted`, and 1 `absent`; dispositions are 20
`Verified`, 4 `Verified gap`, and 12 `Partial`.

The allocation contains the sole new source `SRC-WERPC-091` for
`REQ-WERPC-009`; claims `CLM-WERPC-013-01..03` belong to
`REQ-WERPC-011..013`, and claims `CLM-WERPC-013-04..06` belong respectively to
`REQ-WERPC-008`, `009`, and `025`. The exact workstream slices remain those in
the closed assignment above. There is no duplicate, gap, reservation, or new
request owner.

The registered NASA SWE-047 traceability URL was unavailable for
`REQ-WERPC-033`; that row remains `Partial`/`human-judgement` and adopts no new
traceability claim from the failed retrieval. The official GitHub Environments
URL was unavailable for `REQ-WERPC-022` and `023`; neither row adopts an
environment claim from it. The sole out-of-ledger source observation accepted
for allocation is the official K3s v1.35 release-family page for
`REQ-WERPC-009`, with live-cluster and patch-suitability inferences rejected.

The immutable baseline retains row 020's originally observed legacy selector.
Validation normalizes only that observation to the real `#ditaxis-baseline`
anchor. Every report row must include its normalized baseline selector;
additional exact owner selectors remain permitted. `validate-research` and
`residue` both passed after allocation registration. The frozen Task 2 report
remains SHA-256
`bb5e198e7c99a7c510296d12cf9c7f94eb8af4eed4ea9a6eedec91e085379598`
and was not appended.

### WRFR-002 agent-engineering integration

WRFR-002 consumed registered report SHA-256
`f0dd1038b056d3f2bdc5e6c5e457e4f3c6cd93cdd5ab75375780101da9eca5b1`
and allocation SHA-256
`04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`.
Its exact slice is `REQ-WERPC-001`, `002`, and `026..032`; every row has an
empty new-source and new-claim allocation. The four existing topical owners
each now contain exactly one `### 2026-08-20 full-corpus reverification`
section, with existing source identities, baseline workspace selectors,
As-Is/Gap/Target, evidence depth, rejected inference, blocking class,
retained `DEFER`, owner, safe follow-up, and refresh trigger.

The pre-recovery probe failed at `ERROR ALLOCATION_REFERENCE`; no owner file
had been edited. Following the reviewed checker-only recovery, the accepted
fail-fast RED was `ERROR INTEGRATION_SECTION`. After integration, the same
probe passed all nine rows. Harness, loop, roster-currentness, agent
evaluations, model fitness, and checkpoint validators passed. Strict Markdown
reported zero violations, strict links/owners passed, and `git diff --check`
passed. These results establish repository-static integration only. Provider
runtime, model fitness/promotion, checkpoint use, connected resources, cost,
latency, hosted CI, live infrastructure, and human validation remain `DEFER`
where their evidence class is absent.

The tracked unit is limited to the four topical owners plus this Task, its
Plan, and durable progress. Commit
`06b3d681b11e0a373afcbe6bc86031dba615f590` contains exactly those seven
paths. Registered report SHA-256 is
`9f589540cadf2893133d5a04b8fa8ee5b34747980117e4889fe98eaf9f1843ce`;
registered package SHA-256 is
`3fb6e7af4e5073e9ddde872c152a5332366763398654ca0eee15a1bf9e61f535`
for range `e8edd3fddb4171aad634ee31a278d136fd3e4529..06b3d681b11e0a373afcbe6bc86031dba615f590`;
final inventory SHA-256 is
`ec9863801083b29107e438a92998b40d121eca2183d6834cbfa3a5621b76fcfa`.

Independent pre-commit source-fidelity/content and spec-compliance/quality
reviews both returned `APPROVED` with Critical/Important/Minor `0/0/0`. The
initial affected lane passed every selected agent and document validator and
then failed only at the expected `CLOSURE-WORKTREE-INDEX-DRIFT` because this
logical unit had not yet been staged. This is not completion evidence; the
affected and staged lanes must pass against the exact index before commit.

The exact-index affected and staged lanes, plain pre-commit, all-files,
formatter review, and both diff checks subsequently passed without mutation.
The post-commit reviewer returned `APPROVED WITH MINOR`,
Critical/Important/Minor `0/0/1`, and allowed WRFR-003 to unblock. Its sole
Minor identified this Task table's stale pre-commit evidence; the Done row
above addresses it. WRFR-003 is queued and ready, not executed.

### WRFR-003 provider/common integration

WRFR-003 consumes registered provider/common report SHA-256
`bf5728c6d4f69dce90cff533058372e243ffed28ed5b5ee8949444212250ce86`
and allocation SHA-256
`04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`.
Its exact slice is `REQ-WERPC-003..006`, with no allocated source or claim ID.
Exactly one dated 2026-08-20 H3 was appended to each existing provider/common
owner. The accepted pre-edit RED was the checker's fail-fast
`ERROR INTEGRATION_SECTION`; the four-row probe is now GREEN.

The first source-fidelity review found one Important source-boundary omission:
REQ-WERPC-005 relied on the existing Codex memory observation without naming
`SRC-WERPC-068`. The provider owner now lists `SRC-WERPC-009..013` and
`SRC-WERPC-068`. The covering integration, strict Markdown, strict links, and
diff checks passed after the correction. Independent source-fidelity and
spec/quality/security re-reviews then both returned `APPROVED` with
Critical/Important/Minor `0/0/0`.

Provider config/evidence, roster admission/currentness, strict Markdown, strict
links/owners, and the diff check all pass. These results establish only the
published-product and repository-static boundaries. Native discovery,
installation, authentication, entitlement, effective permissions, hook
delivery, model resolution, MCP connectivity, memory behavior, and provider
execution remain `DEFER`.

Commit `a41def9e570ed798c87d6a17adb766df394f4768` contains the exact five-file
logical unit. Registered report SHA-256 is
`39c9bdcd9710d66ea57c06e5404da326f07d8424423e85900d559fba60ddc996`;
registered review-package SHA-256 is
`889801d930e7e25e5beb828fea743e6a9ccb652ecc6ae0f979c474dc924d74d7`
for exact range
`8cd4721f06943f16302ada0c993187c9328d503b..a41def9e570ed798c87d6a17adb766df394f4768`;
final inventory SHA-256 is
`e949e9f191b8153486e1f2d43c9f903f65df583cb5f436ef91dd0a60a3bb3cce`.
The post-commit reviewer returned `APPROVED WITH MINOR`,
Critical/Important/Minor `0/0/1`; this closure corrects its sole stale-evidence
Minor. That closure unblocked WRFR-004; its current state follows.

### WRFR-004 SDLC/documentation integration

WRFR-004 consumes registered SDLC/documentation report SHA-256
`be273b3dad1b6b4f50d12285cf9114406ba5c3af94ded7646a71ceda5b47ae85`
and allocation SHA-256
`04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`.
Its exact slice is `REQ-WERPC-007`, `010..021`, and `034..036`. The only
allocated identities are claims `CLM-WERPC-013-01..03` for current-form AD
terminology corrections. Each existing owner contains exactly one dated H3
immediately before its terminal Related Documents section.

The pre-edit probe exited `1` with fail-fast `ERROR INTEGRATION_SECTION`;
after integration it passed all sixteen rows. Strict registry, strict Markdown,
active-corpus, RIA self-test, LLM-WIKI generated-index check, and diff check
passed. The first strict-links run found a real authority conflict: two required
append targets were complete-blob-pinned historical alias sources. Separate
reviewed commits `bdd36f09` and `42222c33` admitted only the approved terminal
insertion slice and the existing Spec 0062 approval expectation. They are not
part of this six-file work unit. Python and security reviews approved those
exact changes with no finding, their full focused class passed 25/25, and the
production strict-links rerun passed.

Independent source-fidelity and spec/quality/security reviewers returned
`APPROVED` with Critical/Important/Minor `0/0/0`. They confirmed exact
row/source/claim mapping, append-only history, ISO catalog limits, the Release
`Verified gap`, the Diataxis no-empty-family and reader-evidence boundary, and
the LLM-WIKI generator/publication/MCP/runtime separation. No provider, hosted,
live, secret, remote, or user-effectiveness evidence was collected or promoted.
Commit `7bbe6517a014cbc3e79c896d5097a3ae8b99a283` contains the exact six-file
logical unit and follows separately reviewed prerequisites `bdd36f09` and
`42222c33`. Registered report SHA-256 is
`c7749874d884d0cd4af617537cd583eb11432ff0ffd537b68212248a84845918`;
registered review-package SHA-256 is
`b996e1022dd709d3a0b70d21df9c58ef9d29c1122810041b377d90aca9cb709e`
for exact range `615c3a87..7bbe6517`; final inventory SHA-256 is
`0d60d1d3602fc357bbabe382dd4ede0bfedaba640e2742d367de021fed5936c0`.
The post-commit reviewer returned `APPROVED WITH MINOR`,
Critical/Important/Minor `0/0/1`; this closure corrects its sole stale-evidence
Minor. That closure unblocked WRFR-005; its current state follows.

### WRFR-005 platform/security integration

WRFR-005 consumes registered platform/security report SHA-256
`edff89e3b29fdcaa658044ffc768b7c297e39a02936bd39657c90bb759a7fbce`
and allocation SHA-256
`04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b`.
Its exact slice is `REQ-WERPC-008`, `009`, and `025`; the only allocated
identities are `SRC-WERPC-091` and `CLM-WERPC-013-04..06`. Exactly one dated
H3 was appended immediately before terminal Related Documents in the existing
Kubernetes/infrastructure/security owner. No research folder, duplicate report,
request owner, or shared-ledger row was created.

The pre-edit integration probe exited `1` with fail-fast
`ERROR INTEGRATION_SECTION`; after the append it returned
`PASS validate-integration` for all three rows. GitOps structure, static
infrastructure contracts, 106-manifest syntax and kube-linter validation,
Vault/ESO contracts, secret handling, strict Markdown, strict links/owners, and
the diff check all passed at their named canonical paths.

Independent source-fidelity, spec/quality, and security reviewers each returned
`APPROVED` with Critical/Important/Minor `0/0/0`. They confirmed the exact
source/claim mapping, current selectors, append-only integration, and separation
among Git revision, Helm provenance, image digest, signature, attestation, and
SLSA provenance. No Secret payload, credential, token, live command/result,
identity mutation, effective-RBAC/admission/CNI claim, or recovery claim entered
the owner.

All three rows remain `Partial` with blocking class `live-cluster`.
Kubernetes authorization/admission/CNI, Argo reconciliation, Vault/ESO backend
and readiness, registry/artifact trust, and recovery effectiveness remain
`DEFER`. Commit `63efc8de90227e1d3c32e2c4388876d4b850a94b` contains the exact
four-file logical unit. Registered report SHA-256 is
`dfe45681c38ec2312936315a465f8069b6f6d1474afda5f6a86d7e34f5804e78`;
registered review-package SHA-256 is
`88111b614c7bda7305cf0d2686d57bda598106c2e66a4bce38333ba32c5682c0`
for exact range `8ed7fae3..63efc8de`; final inventory SHA-256 is
`d844156bdfe0dab8ab90009e89ad7807aab6987571955aa8a2783f4784047f24`.
The post-commit reviewer returned `APPROVED WITH MINOR`,
Critical/Important/Minor `0/0/1`; this closure corrects its sole intentional
pre-closure lifecycle Minor. WRFR-005 is complete. WRFR-006 passed its
pre-remote gate and its first fixed recovery. At that checkpoint, the sole
`oidc` query had failed schema validation and the second fixed recovery gate
preceded the untouched `artifacts` query.

### WRFR-006 delivery and quality integration

WRFR-006 consumes delivery/quality report SHA-256
`f55cc2285577530544c48f26fb497184b43bb9822236e46a736294ed8695d993`
and the allocation slice `REQ-WERPC-022`, `023`, `024`, and `033`, with no new
source or claim identity. Both fixed incident recoveries completed under their
tracked contracts. The untouched `artifacts` query then ran once, and the final
remote summary SHA-256
`da137936a4ec5cbb10c06303b96e22cc933188fec7042b8aa0dd774e627d4d21`
passed nine-class remote validation.

Seven classes are observed: Actions is enabled with allowed-actions mode `all`;
default workflow permission is `read`; rulesets are empty; `main` protection
projects required `ci-summary` with strict mode and administrator enforcement
disabled and zero required approvals; environments and artifacts each total
zero; and the retained run sample contains 20 completed results, 13 success and
7 failure, over 8 unique head SHAs. `workflows` remains unavailable with reason
`checker-auth-context-incompatible`; `oidc` remains unavailable with reason
`checker-oidc-schema-incompatible`. These are sanitized setting and historical
metadata observations, not proof of current-local-HEAD hosted execution,
effective enforcement, cause, approval, actual OIDC setting, promotion,
deployment, intended use, or stakeholder acceptance.

Exactly one `### 2026-08-20 full-corpus reverification` section was appended
immediately before terminal Related Documents in the existing delivery/quality
owner. It covers CI/CD, Actions and supply-chain controls, every named QA lane,
and the full Requirements Validation / Product Verification / Product
Validation boundary with Workspace As-Is, Gap, Target, and Verification. The
pre-edit probe failed exactly with `ERROR INTEGRATION_SECTION`; after the append
it returned `PASS validate-integration`. GitHub Actions security, CI Python
contract, affected surfaces, agent-governance CI, strict Markdown, strict
links/owners, and `git diff --check` also passed.

Commit `ae7a22620ede8bfdb387c4528952f156e82a7aa2` contains the exact
four-file logical unit. Registered report SHA-256 is
`00856efaed17e3d5267e13d1c83399529bab7203201167d873bf83712aaec6a9`;
registered review-package SHA-256 is
`71a09244cce2ddb51bc2f1a1568ed874d1614837423e430fb8d3bbe816b3b876`
for exact range `fcbcd869..ae7a2262`; final inventory SHA-256 is
`68b4173514a287eaff1e9e1c3b50c7ad57d3e6dbce2eb01b6dcd10ba9d08c1bc`.
The post-commit reviewer returned `APPROVED WITH MINOR`,
Critical/Important/Minor `0/0/1`, found no material implementation defect,
and allowed WRFR-007 to unblock after this bounded lifecycle closure. The sole
Minor was the intentional pre-closure state corrected here. WRFR-006 is
complete and WRFR-007 is queued and ready. No new research folder/report,
shared ledger projection, push, merge, publication, workflow dispatch, remote
mutation, or live action is claimed by this closure.

### WRFR-007 pre-integration checker recovery

The first Task 8 shared-ledger probe ran at clean commit `cb494def` before any
owner edit and returned exactly `ERROR ARGUMENTS_INVALID`. The checker SHA-256
was `2308481b8b0ded1647c105a4ab9aad0292db1459e53b8989a49f1fd3bdd7b038` and
the inventory SHA-256 was
`68b4173514a287eaff1e9e1c3b50c7ad57d3e6dbce2eb01b6dcd10ba9d08c1bc`.
The parser has only the five topical workstreams, and no-workstream validation
also checks only those five. WRFR-007 remains blocked with no ledger, scope, or
README edit.

The tracked Plan amendment fixes the repair boundary: retain topical behavior;
add closed `shared-ledger` and `reconciliation` modes; make no-workstream
validation compose all seven validators; define the append-only source/claim
table schemas; derive exact `14/36/91/141` census and report distributions; and
fail closed on ledger legacy drift, allocation projection, identifier
references, ten-scope projection, pack reconciliation, collection census,
lifecycle, Stage 03, ADR/registry reciprocity, and progress. The required order
is TDD RED, minimal checker repair, compile plus normal/optimized self-tests and
Ruff, exact-byte Python/security review, tracked final-hash amendment, one
checker-only rebind with no retry, residue/self-test proof, and the unchanged
Task 8 probe reaching `ERROR INTEGRATION_SOURCE_PROJECTION`. The sole ledger
integrator may resume only after that semantic RED.

The final checker candidate is SHA-256
`3cdaf66628e817663d9306b8e31c95788db0111fb30f1dcdcedc027fbdab338a`,
367108 bytes, mode `0600`, owner `hy:hy`. All 128 normal and optimized
self-tests, compile, Ruff check, and Ruff format-check pass. Fresh Python and
security exact-byte reviews both approved it at Critical/Important/Minor
`0/0/0`. The Plan now fixes the exact ledger insertion boundary and the scope,
pack, collection, and progress table serialization that WRFR-007/008 must
produce.

Before the one-shot checker rebind, remove only the exact unregistered review
cache described in the Plan. Its file identity is device/inode
`2096/1754901`, 404505 bytes, mode `0600`, UID:GID `1000:1000`, mtime/ctime
`1787398444410567416` ns, and SHA-256
`4589e081b801c768b74f855815e0d67f6a9c452dd8e2f1d54c6dabd43815f68e`.
Its sole parent-cache directory is device/inode `2096/1694147`, mode `0755`,
UID:GID `1000:1000`, with the same mtime/ctime. Use the Plan's retained-dirfd,
no-follow, exact-entry, pre-unlink revalidation, `fsync`, empty-directory
`rmdir`, and post-absence procedure. A mismatch stops cleanup. The inventory
and every registered artifact remain unchanged until the already-fixed
checker-only rebind runs exactly once.

No registered artifact, topical/shared owner, remote state, or live system may
change before the tracked recovery contracts and checker review gates allow it.

### WRFR-007 Stage 90 frozen-blob transition-guard recovery

The approved shared projection is present only in the three Task 8 research
owners. The exact shared validator, strict document registry, strict Markdown
profiles, and diff check pass. Strict links validation exits `2` with
`configuration error: reviewed Stage 90 move source differs from its frozen blob`
because
`docs/90.references/research/2026-08-08-wer/README.md` moved from reviewed base
blob `6bfec251d8927dd82f5c12b49c013a598c64d088` to reviewed Task 8 successor blob
`11719d258d0454d68f3e6b6ed0377c3d3b9de6b2`.

The bounded repair retains the Stage 90 move-edge probe at `29` and the immutable
alias source/edge/occurrence probes at `27/93/169`. One closed path-keyed
`(base, target)` transition map must serve both the Stage 90 and immutable-alias
checks. Foreign keys, a mismatched base, non-lowercase-40hex values,
`target == base`, insertion/prefix overlap, and any arbitrary mutation fail
closed. The repair may change only `scripts/validate-links-and-owners.py` and
`tests/test_archive_validation.py`; it cannot weaken edge, redirect,
occurrence, target, path, or archive checks.

The controller must first commit this three-document contract, then run focused
TDD RED/GREEN, compile, Ruff check/format-check, focused and full archive tests,
validator self-test, strict links, and diff check; obtain independent code and
security approval; and commit exactly the two guard files. Only then does the
sole ledger integrator resume the original Task 8 Step 5. WRFR-007 remains
blocked/in progress, with no completion or post-commit review claimed.

### WRFR-007 provenance correction and decision gate

`task-8-brief.md` was generated and registered after exact integration commit
`fef53976b97c560de0a9f020e87be1e7e0e1c3b8`, so it cannot establish registered
brief consumption before implementer dispatch. The late brief, implementer
report, and review package remain immutable and must not be rewritten.
Independent task/spec re-review withdrew the prior `APPROVED` result and records
Critical/Important/Minor `0/1/0`. The separate ledger/source content review
remains `APPROVED`, `0/0/0`, and no integration content or validation evidence
is withdrawn.

WRFR-007 is blocked pending explicit human direction between only two paths:
(A) a documented one-time exception accepting the exact full-Plan/scoped-prompt
evidence, with a new scoped closure review; or (B) a closed re-execution that
withdraws and reapplies only the three research projections after a registered
pre-dispatch brief, followed by a new fix package and review. WRFR-008 remains
queued but blocked and must not start before that decision. No exception,
re-execution, completion, or successor authorization is claimed here.

### SDD helper incident and separate WRFR-009 cleanup gate

After this provenance correction, the controller mistakenly invoked the
forbidden canonical `sdd-workspace` helper. The command created the exact empty
directory `.superpowers/sdd/plan` at device/inode `2096/4541614`, mode `0755`,
UID:GID `1000:1000`, mtime/ctime `1787407543766841537` ns. It also rewrote
`.superpowers/sdd/.gitignore` with the same `*\n` bytes and unchanged SHA-256
`cdbcae15105d6b781e620813c79c7e868740d4e9cc53ce6f5fcbbc12387adf4b`.
That marker retains device/inode `2096/4410802`, mode `0644`, UID:GID
`1000:1000`, while mtime/ctime moved from `1787208168057628362` ns to
`1787407543770964835` ns.

The canonical Plan workspace is unchanged at device/inode `2096/4406235`, mode
`0700`; inventory SHA-256 remains
`058cad35454e285dcc4c7b9b2be8ede06e111090ec45f78762cd5a001c14b545`;
and no canonical task-artifact bytes changed. The new sibling and invalidated
marker FileVersion nevertheless block WRFR-009 cleanup preconditions. No
deletion, chmod, restoration, or recovery was attempted.

The Task 8 decision remains exactly A/B above. Separately, the new SDD objects
require explicit human direction and an independently reviewed one-time
cleanup-recovery design before any recovery operation or WRFR-009 cleanup. No
procedure or authorization is invented by this Task record.

### Stop conditions

Execution stops only for a destructive or irreversible action, a
security-sensitive action not already approved, an external side effect such as
push/merge/publication, or a Plan defect that leaves every path forward a guess.
All other conflicts receive a recorded SDD ruling and continue under the Spec.

## Verification Summary

WRFR-000 activation and WRFR-001 intake, tracked evidence, registered review
packages, and task-level post-commit review are complete. The WRFR-002 checker
recovery, nine-row topical integration, exact seven-file commit, registered
report/package, and post-commit task review are complete. WRFR-003 has completed
its four-row owner integration, focused validation, exact five-file commit,
registered report/package, and post-commit task review. WRFR-004 has completed
its sixteen-row topical integration, exact six-file commit, registered
report/package, and post-commit review. WRFR-005 has integrated its exact
three-row owner section and passed focused static validation plus three
independent pre-commit reviews. Its exact four-file implementation commit,
registered report/package, and post-commit review are complete. The sole stale
lifecycle Minor is closed. WRFR-006 passed both fixed recoveries, final remote
validation, four-row owner integration, focused GREEN checks, exact four-file
commit, registered report/package, and post-commit review. Its sole lifecycle
Minor is closed; WRFR-007 is blocked only by the tracked pre-integration checker
recovery gate. Initial design evidence included:

- isolated worktree created from clean tracked `HEAD`;
- primary checkout's unrelated staged RIA files excluded from the branch;
- pre-authoring `bash scripts/validate-repo-quality-gates.sh .` passed;
- strict document registry passed with 538 paths after Spec indexing;
- strict Markdown profiles reported zero violations;
- strict cross-document links and owners passed;
- design commit `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` contains only Spec 0062 and the Stage 03 index entry.

WRFR-001 then validated the immutable `14/36/90/135` baseline, five registered
reports and their exact 36-row union, the final allocation, and whole-workspace
artifact residue. These results prove the closed-corpus public-source and
repository-static intake only. They do not prove remote GitHub state, provider
runtime, hosted CI, live infrastructure, or user validation.

WRFR-002 preserved those evidence limits while appending the accepted delta to
four existing owners. Its task-local integration probe and all six canonical
agent validators passed, as did strict Markdown, strict links/owners, and the
diff check. No new ledger ID or owner was created.

WRFR-003 likewise preserves those limits across the common-environment and
provider-status owners. Its four-row probe and canonical provider validators
pass, the corrected source boundary received independent approval, and no new
ledger ID or owner was created. Its exact five-file implementation commit,
guarded report/package registration, and post-commit review are complete.

WRFR-004 preserves those limits across its three SDLC/documentation owners.
Its sixteen-row probe and documentation validators pass after the separately
reviewed alias-authority prerequisites. Only three allocated current-form AD
claims are cited; Release, reader-effectiveness, publication, retrieval, MCP,
and provider/runtime evidence remain bounded. Its exact six-file implementation
commit, guarded report/package registration, and post-commit review are
complete.

WRFR-005 preserves those boundaries across Kubernetes desired state,
infrastructure execution contracts, and security controls. Its three-row probe
and all canonical platform/security static validators pass, and independent
source-fidelity, spec/quality, and security reviews approve the owner content.
Its exact implementation commit, guarded report/package registration, and
post-commit task review are complete. WRFR-006 completed its pre-remote review,
RED probes, preflights, summary registration, both fixed local recoveries, all
nine query budgets, remote validation, one owner append, and the focused static
checks. Its exact implementation commit, guarded report/package registration,
and post-commit task review are complete. No current-HEAD hosted, enforcement,
OIDC-setting, stakeholder, deployment, or live outcome is promoted.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-WRFR-001](spec.md) | Done | The checker validated the exact `001..036` report union, and the independent Task 2 reviewer approved Packages A/B/C with no findings |
| [VAL-WRFR-002](spec.md) | All five workstream integrations and reviews passed | All 36 rows carry closed evidence fields; WRFR-002..006 integrated their exact disjoint slices without changing the request set |
| [VAL-WRFR-003](spec.md) | Done | The five registered reports retain the exact closed workstream assignment |
| [VAL-WRFR-004](spec.md) | All five workstream integrations and reviews passed | Registered research review is preserved; all integrated workstreams retain exact primary-source identities and limits |
| [VAL-WRFR-005](spec.md) | Five topical integrations passed | WRFR-002 through WRFR-006 record exact baseline selectors and evidence-depth boundaries; all five commits/reviews are complete |
| [VAL-WRFR-006](spec.md) | Intake passed; ledger integration pending | All rows use the closed outcome vocabulary and passed checker validation |
| [VAL-WRFR-007](spec.md) | Intake passed; ledger integration pending | Every row carries a valid blocking-class disposition combination |
| [VAL-WRFR-008](spec.md) | In progress | WRFR-002 through WRFR-006 appended to eleven existing owners without creating a research folder, duplicate topic report, or request owner; WRFR-007..008 remain |
| [VAL-WRFR-009](spec.md) | Allocation passed; ledger integration pending | WRFR-001 allocated source 091 and claims 013-01..06 without gaps or duplicates |
| [VAL-WRFR-010](spec.md) | Not executed | WRFR-007..009 own the shared projection sequence |
| [VAL-WRFR-011](spec.md) | Remote summary and security reviews passed | Nine unique sanitized classes passed; seven are observed and workflows/OIDC retain fixed checker-compatibility unavailable reasons |
| [VAL-WRFR-012](spec.md) | Workspace passed; cleanup pending | WRFR-001 residue validation passed; WRFR-009 still owns exact cleanup |
| [VAL-WRFR-013](spec.md) | In progress | WRFR-001..006 logical commits and task reviews are complete; WRFR-007..009 remain pending |
| [VAL-WRFR-014](spec.md) | Not executed | WRFR-009 owns the whole-branch review gate |
| [VAL-WRFR-015](spec.md) | Not executed | WRFR-009 owns the terminal lane sequence |

### Related Documents

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [ADR 0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../00.agent-governance/memory/progress.md)
