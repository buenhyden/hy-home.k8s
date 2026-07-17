---
title: 'Task: Document Schema and Lifecycle Contract'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-17
---

# Task: Document Schema and Lifecycle Contract

## Overview

This Task is the mutable execution and review ledger for DSLC-001 through
DSLC-006 under [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md).
It records test-first results, logical commits, rollback parents, independent
reviews, and explicit static/live evidence boundaries.

## Inputs

- [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Document type, format, and evidence research](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Current implementation audit pack](../../90.references/audits/2026-07-11-weia/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| DSLC-001 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-003, VAL-DSLC-007, VAL-DSLC-008 | Add closed registry v7 value, role, lifecycle, evidence, and compatibility schema plus typed projection. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | RED archive-specific semantics and policy-ID/path-alias bypasses reproduced; GREEN 117-case registry self-test, complete literal typed projection, duplicate-key rejection, strict registry/Markdown/cross PASS; logical commit `5781ea3`. |
| DSLC-002 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-005 | Enforce metadata values, template/source parity, and baseline-only Tombstone admission. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | RED seven value-contract cases returned `metadata value rules are unimplemented`; expanded 18-case GREEN covers string/integer/number/boolean/date kinds, profile/literal constants, status/literal enums, scalar patterns, denied/allowed null, equals/not-equals, required/forbidden, and absent-versus-explicit-null references without private archive semantics. Exact 31-path Tombstone compatibility plus explicit untracked include rejection, 11/11 template/source parity mutations including typed value-contract parity, and strict current-corpus/registry/cross PASS are recorded. |
| DSLC-003 | VAL-DSLC-003, VAL-DSLC-004, VAL-DSLC-008 | Implement exact staged, CI, explicit-ref, and snapshot comparison modes and transition graph validation. | platform | Done | Implemented; final independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | Named RED failed on both missing public entrypoints and every declared fixture group. Expanded GREEN is 124 cases: 42 literal forward edges, 9 comparison priorities, 12 admission events, 35 isolated Git/ref/environment/root bases, 7 argument boundaries, 5 additive include failures, one current snapshot DEFER, and 13 fixture-closure mutations. |
| DSLC-004 | VAL-DSLC-004, VAL-DSLC-008 | Enforce edge-specific rendered-link, state, same-diff, and body-contract evidence. | platform | Done | Remediated after independent rejection; final re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | GREEN is 651 cases: 42 forward edges, exact 504 edge scenarios with a full-diagnostic assertion hash, 9 comparisons, 12 admissions, 43 Git/ref/provenance bases, 7 arguments, 5 includes, one snapshot DEFER, 23 fixture mutations, and 5 review regressions. Remediation closes context-forgery, reciprocal backlink, ready-Spec state, allowed-H2, Task placeholder, and Result-column bypasses while retaining canonical CommonMark evidence and staged/index, explicit-ref, and CI provenance. |
| DSLC-005 | VAL-DSLC-005, VAL-DSLC-006, VAL-DSLC-007 | Close native, role/source, Stage 00/99, and directly implicated consumer drift without bulk corpus rewrite. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | RED accepted four cross-row role-label copies and exact leading SDLC blocks on native surfaces. GREEN is 121 registry cases with 64 profiles, 30 templates, parity 11/11, plus native 10/10 and a five-family Git-index integration proof. Stage 00 relationship wording, four Stage 99 v7 residues, Runbook/Incident roles, 64-row tests inventory, and six-form research pointer are corrected. Operations census is Guide 8 + Policy 7 + Runbook 9 = 24; Incident/Postmortem bodies = 0, recorded only as Spec 037 input. OpenAPI/GraphQL/protobuf syntax tooling remains Spec 039 `DEFER`. The aggregate quality script passed its registry/Markdown/cross/GitOps/Vault/affected-surface/agent-role/roster prefix, then produced no output for more than three minutes and was stopped (exit 130); it is not reported as PASS. Focused static and native-tool lanes passed. |
| DSLC-006 | VAL-DSLC-001 through VAL-DSLC-008 | Run full QA, whole-tranche review, and atomic lifecycle closure. | platform | Queued | Not executed | Done lineage, command matrix, review verdicts, rollback parent, closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**:
  `docs/00.agent-governance/rules/stage-authoring-matrix.md`,
  `docs/00.agent-governance/rules/postflight-checklist.md`, and
  `docs/00.agent-governance/hooks/k8s-pre-edit.sh`;
  `docs/03.specs/035-document-schema-and-lifecycle-contract/**` and its Stage 03
  index; this Plan/Task and Stage 04 indexes;
  `docs/05.operations/incidents/README.md`; the directly implicated Stage 90
  research ledger/pointer; `docs/99.templates/support/**` and canonical forms
  implicated by v7; `scripts/document_contracts.py`, document/lifecycle/link
  validators and `scripts/README.md`; focused fixtures; program relation and
  migration-ledger closure rows.
- **Forbidden Paths**: Kubernetes/GitOps desired state, infrastructure,
  policies, secrets, provider runtime adapters, generated outputs, accepted or
  completed historical bodies, archive corpus conversion, bulk Stage 05/helper
  body normalization, completed Plan/Task movement, and Spec 036-040 bodies
  except read-only boundary verification.
- **Approval Required**: Any live system, secret, remote GitHub setting, push,
  publication, dependency installation, or scope expansion requires separate
  explicit approval.
- **Static Validation**: Registry, Markdown-profile, lifecycle,
  cross-document, native available-linter, repository-quality, Markdown lint,
  staged diff, and all-files pre-commit commands from the Plan.
- **Live Validation**: DEFER. Spec 035 authorizes no remote/provider/live lane.
- **Secret / Vault Handling**: Do not read, print, move, or infer ignored
  secrets, credentials, tokens, auth files, shell history, kubeconfigs, or
  Vault values.
- **Rollback Plan**: Before closure, revert the newest open DSLC package first
  and remove v7 consumers before v7 schema/data. After DSLC-006, do not reopen
  terminal evidence in isolation: apply DSLC-006 through DSLC-001 newest-first
  with `git revert --no-commit`, validate only the complete staged v6/active
  state, and create one atomic rollback commit. Record every commit parent in
  this Task.
- **Evidence Location**: This Task, logical Git commits, focused fixtures,
  validator outputs summarized here, and the durable migration ledger.

## Verification Summary

Planning baseline: registry v6 classifies 430 paths through 64 profiles and 30
templates with zero uncovered or ambiguous routes. Registry self-test has 78
cases; cross-document self-test has 344 cases. Current frontmatter/profile
validation passes. No Spec 035 implementation work has run yet. The isolated
filesystem reproduces one known `os.mkfifo` `Errno 95` in the all-files
repository-quality hook; Spec 039 owns that portability fix, and it may be
recorded as DEFER only when every other hook passes.

Planning review first rejected underspecified creation/movement admission,
edge evidence, Git comparison interfaces, native syntax claims, closure order,
null-body profile handling, and post-closure rollback. The remediated Plan now
owns exact admission defaults, an edge/predicate matrix, the lifecycle
module/CLI/fixture and exit contract, staged closure review, explicit native
syntax DEFER, heading-set predicates for null-body profiles, and one atomic
post-closure rollback. Independent re-review returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. The staged planning set passes
strict registry, Markdown-profile, cross-document, diff-check, and changed-file
Markdown lint validation.

DSLC-001 RED failed on the first newly declared v7 mutation because the v6
self-test had no mutation implementation. GREEN upgrades production to closed
registry v7, exposes immutable value/role/admission/lifecycle/evidence
projections, checks every production edge against exactly one predicate case,
and pins the 31 tracked Tombstones to baseline-only admission. The registry
rejects duplicate JSON keys at root or nested depth, noncanonical Tombstone
baseline spellings, and archive-specific value semantics before Spec 036.
Registry self-test passes 117 cases with the complete literal
64-profile/30-template projection, every admission/lifecycle/evidence field,
generic private-fixture conditional semantics, and private v5/v6 migration
proof. Strict registry validates 432 paths; strict
Markdown reports zero violations and strict cross-document validation passes.
No lifecycle Git comparison, metadata enforcement, evidence resolution, corpus
rewrite, archive route, or CI change is claimed by this package.

Independent review first rejected archive-specific value ownership, partial
predicate projection, duplicate-key JSON parsing, and noncanonical Tombstone
path aliases. Remediation removed production archive literal/conditional
semantics, added a complete independent literal projection and schema-valid
semantic-drift mutations, centralized duplicate-key-rejecting JSON loading,
and checked raw Tombstone paths by exact profile membership. A second review
found the combined policy-ID rename plus `//` alias bypass; the 117th mutation
reproduces and closes it. Final re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`.

DSLC-002 RED added production-derived value-contract cases; all seven initial
cases failed because metadata value rules were unimplemented. Review
remediation expanded GREEN to an exact 18-case value matrix. Generic
literal-constant, literal-enum, and conditional capabilities use only the
ordinary five-key `sdlc/spec` profile and introduce no private Tombstone reason,
replacement, or archived-state semantics. The matrix evaluates string,
integer, number, boolean, and date kinds; profile/literal constants;
status/literal enums; patterns over canonical scalar text; denied and allowed
nulls; both conditional operators and effects; and the intentional distinction
between an absent reference (no match) and an explicit null reference (eligible
to match). Established title, type, status, owner, and date rule IDs remain
stable. Ordinary authored documents still have the five ordered keys,
templates alone retain starter/date placeholders, and the strict current
corpus has zero violations. A baseline-only admission check
keeps the exact 31 tracked Tombstones readable and rejects copied, renamed, or
explicitly included untracked Tombstone paths. The registry self-test adds a
11/11 independent template/source parity matrix for frontmatter, order,
status, headings, class, body contract, typed value contract, source
cardinality, missing source, duplicate source, and unknown source. Focused
self-tests, strict registry, strict Markdown, and strict cross-document
validation pass. Independent re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`; the logical DSLC-002 commit records this evidence.

DSLC-003 RED named both absent public entrypoints and every literal forward,
comparison, admission, Git, argument, include, and snapshot case before the
engine existed. GREEN adds an immutable pure comparison interface plus a
public CLI for staged HEAD/index, explicit CI merge-base, explicit refs, and
filesystem snapshot modes. Event priority is exact rename, same-path profile
change, invalid state, then edge; exact renames emit one event, while a
content-changing rename stays delete plus create. Plan/Task creation requires
exactly one of each in the same allowed state and proposal; rendered reciprocal
links and direct-Spec identity remain DSLC-004 evidence scope.

The first independent review returned `NOT COMPLIANT` and `QUALITY REJECTED`
for unclassified add/delete/modified gaps, inherited Git-environment steering,
fixture closure, and peeled non-commit refs. The second requirements review
returned `COMPLIANT`, while its paired quality review rejected submodule-ignore
steering and unchecked nested fixture shapes. The remediated 124-case self-test
expands all 42 literal profile edges and uses isolated temp Git repositories
for HEAD/index/worktree divergence; governed and unclassified add/delete,
same-path modification, exact rename, and content-changing rename; real
same-path type-claim change; unknown type claim; additive include
non-filtering; unique, disconnected, and criss-cross CI bases; and explicit
refs. Exact `R100` remains one rename event before profile selection, while
modified governed-to-unclassified, unclassified-to-governed, and
unclassified-to-unclassified paths remain deterministic delete/create events.

Every inherited `GIT_*` variable is removed for subprocesses and imported
registry/inventory calls, then fixed noninteractive identity/config variables
are installed only for the validation scope and the caller environment is
restored. Git commands disable replacements, graft steering, external diff,
text conversion, hooks, and fsmonitor; exact rename detection has an unlimited
limit and `--ignore-submodules=none` overrides local and tracked
submodule-ignore policy. Staged and explicit-ref fixtures replace a governed
Markdown blob with a gitlink under `ignore=all` and prove exit `2` with
`LIFECYCLE-BASE`, never a clean result. Repository identity must resolve to the
requested non-bare worktree.
Direct refs must resolve to commits without implicit peeling: raw trees, blobs,
and annotated tags fail with exit `2`, while a lightweight tag pointing
directly to a commit passes. Fixture schema, ordered cases, stable rule IDs,
and the exact unique production-edge projection are closed. Every nested
profiles/edges/document/status/rule/argv/exit/base-mode/include/snapshot shape
is validated before execution; thirteen private mutations cover removed
families/cases, duplicates, unknown names, null base/documents, malformed
status/exit/member values, unhashable base-mode/operation values, and a
non-object list member. All argument/provenance failures return exit `2` with
the complete stable diagnostic envelope; lifecycle violations return `1`.
Current repository snapshot returns exit `0` with exactly one
`LIFECYCLE-BASE-DEFER` and never claims transition PASS. Both ref snapshots are
classified with the current v7 registry; the pure interface independently
accepts base/proposed profile IDs, while historical registry reloading remains
an explicit non-claim. Final independent re-review returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` after the submodule-ignore,
nested-shape, and unhashable-enum reproductions were closed.

DSLC-004 RED added a closed evidence fixture contract and failed before the
public resolver and fixture root existed. GREEN expands the lifecycle self-test
to 651 cases. Every one of the 42 production edges owns the same ordered 12
scenarios: positive, missing, wrong profile, wrong state, wrong relationship
section, unchanged, ambiguous base, body-contract mismatch, plain-text path,
opaque Markdown, orphan, and multiple evidence. Twenty-three fixture mutations
close missing, duplicated, reordered, null, non-string, unknown-predicate, and
edge-projection drift.

The lifecycle CLI builds complete immutable base and proposed Markdown maps
from Git objects or the stage-zero index before it resolves evidence. It calls
the public CommonMark-aware adapter in `validate-links-and-owners.py`; no second
Markdown parser and no worktree fallback are introduced. Body-contract
relationships count only rendered links from the declared source or target
columns, heading-set relationships count only links under the exact selected
heading, and unresolved, orphan, or multiply matching candidates produce one
stable aggregated `LIFECYCLE-EVIDENCE` result per target. Task Evidence cells
may directly identify an operated or referenced target without requiring an
invented reciprocal relationship from Incident or Postmortem documents.

Plan and Task evidence must be reciprocal, changed atomically where the edge
requires it, direct to the same generic Spec, and attached to the first
dependency-ready nonterminal original-program tranche. Isolated Git cases prove
blocked and split-Spec rejection, base-only relationship removal, proposed-only
relationship admission, CI proposed-tree resolution, and both directions of
index/worktree divergence. Snapshot mode remains an explicit transition-history
DEFER, and historical registry reloading remains outside this package.

The first independent requirements and quality reviews rejected the initial
implementation. Remediation retains every outer subject transition. Git-shaped
variants mutate rendered evidence only; the logically impossible `$self`
wrong-profile and wrong-state combinations mutate only the isolated pure
interface evidence projection and are rejected by context-integrity checks.
Every ambiguous-base variant runs through an edge-shaped CI graph, and the full
ordered 504-case diagnostic envelope—including every `evidence_gap`—is fixed to
one literal assertion hash. Five focused regressions close forged
`created_paths`, missing reciprocal body evidence, unsupported root H2, the
canonical Task evidence placeholder, and Result-column target links. A 43rd
Git base rejects an otherwise reciprocal active Plan/Task pair when the
proposed dependency-ready Spec status differs from the registry relation state.
Final independent re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` for the exact six-file package.

DSLC-005 RED proved that the registry accepted each of the four audited
cross-row role-label copies and that the Markdown entrypoint accepted an exact
leading five-key SDLC envelope on a native OpenAPI path. GREEN makes canonical
role labels unique across decision rows, forbids direct template role
assignment, and keeps legitimate same-row multi-profile roles plus sole-source
template inheritance. Registry self-test now passes 121 cases for 64 profiles
and 30 templates; template/source parity remains 11/11 and includes the typed
role/source comparison.

The native fixture closes exactly five families: GitHub issue form, GitHub
workflow, OpenAPI, GraphQL, and protobuf. Five positive payloads and five
otherwise-identical leading-SDLC-envelope negatives pass `10/10`; an isolated
Git-index integration executes the same five positive and five negative paths
through the production scan. GitHub YAML remains native-owned and must stay
uncovered by the document registry. Machine-contract ownership is derived from
the typed native role and route-selected profile. A legal YAML `---` marker,
a non-SDLC multi-document mapping, and GraphQL/protobuf delimiter comments are
not rejected. This package does not claim OpenAPI, GraphQL, or protobuf syntax
validation; unavailable syntax tooling remains a Spec 039 `DEFER`.

Direct drift remediation replaces four Stage 00 universal relationship
requirements with registry-selected wording, updates the four active Stage 99
v5 residues to closed v7 wording, makes the Runbook author prompt role-based,
and keeps hypothesis/root-cause analysis out of the Incident Record role. The
tests inventory now states the exact 64-row breakdown (55 validate-document,
7 classification-only, 1 append-fragment, 1 excluded), with native `10/10`
reported separately, and the research ledger points to all six current README
forms. The read-only Spec 037 census is Guide 8 + Policy 7 + Runbook 9 = 24 and
Incident/Postmortem bodies = 0; no operations corpus body was rewritten.
Independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`.
DSLC-005 is complete; DSLC-006 has not started.

Focused registry, Markdown, lifecycle, cross-document, Ruff, Python compile,
JSON, diff, YAML, GitHub workflow, security, Markdown, secret, and shell gates
pass. The repository-quality aggregate passed its registry, Markdown,
cross-document, GitOps identity, Vault/ESO, affected-surface, agent-role, and
roster prefix, then emitted nothing for more than three minutes. It was stopped
with exit 130 and is not claimed as a full PASS; no FIFO diagnostic was emitted.

## Traceability

- **Spec**: [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- **Plan**: [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- **Predecessor Task**: [Spec 034 execution evidence](./2026-07-15-authority-and-lineage-foundation.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [DSLC-001](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-001-registry-v7-contract) | Done; requirements compliant and quality approved. | RED review reproductions; GREEN 117 registry cases, complete literal v7 typed projection, strict 432-path registry, Markdown zero violations, cross-document PASS, and duplicate/canonical-path guards. |
| [DSLC-002](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-002-metadata-template-and-compatibility-enforcement) | Done; requirements compliant and quality approved. | Initial seven-case RED; exact 18-case selected v7 value matrix without private archive semantics, 31-path baseline-only admission plus explicit untracked include proof, 11/11 template/source parity mutations including typed value parity, strict current-corpus PASS, and independent review closure. |
| [DSLC-003](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-003-base-and-transition-engine) | Done; requirements compliant and quality approved. | Named entrypoint/case RED; 124-case engine/Git/CLI/fixture-closure GREEN and current snapshot exact DEFER; submodule-ignore and nested/unhashable-shape review reproductions closed by final independent re-review. |
| [DSLC-004](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-004-transition-evidence) | Done; requirements compliant and quality approved. | Closed 504-scenario exact diagnostic projection, canonical CommonMark evidence adapter, context integrity, reciprocal/allowed-H2/Task-column rules, dependency-ready same-Spec-state proof, 43 Git provenance bases, 23 fixture mutations, and 5 review regressions. |
| [DSLC-005](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-005-native-role-and-support-drift) | Done; requirements compliant and quality approved. | RED role/native acceptance; GREEN 121 registry cases, parity 11/11, native 10/10 plus Git-index integration, direct Stage 00/99/Incident/Runbook/tests/research drift remediation, the Spec 037 operations census, and independent review closure. |
| [DSLC-006](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-006-closure) | Queued. | Full QA, independent reviews, and atomic closure evidence will be recorded here. |
