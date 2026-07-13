---
title: 'Task: Authored Document Migration'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-13
---

# Task: Authored Document Migration

## Overview

This Task tracks seven bounded migration waves that move the approved authored
document corpus from measured compatibility debt to strict profile validation.
ADM-001 establishes reciprocal execution lineage. ADM-002 through ADM-007 then
publish the durable evidence ledger, normalize each owned document family,
consolidate duplicate AWS/Azure prose, and close the compatibility boundary.

## Inputs

- **Lifecycle Promotion**: The operator's direct program approvals promote this
  Task from the canonical `draft` starting state to `active` for execution.
- **Parent Spec**: `docs/03.specs/030-authored-document-migration/spec.md`
- **Parent Plan**: `docs/04.execution/plans/2026-07-12-authored-document-migration.md`
- **Validation Baseline**: Completed Specs 026 through 029 provide the registry,
  templates, README profiles, semantic validators, and the exact 468-path
  post-ADM-001/pre-ledger inventory (`baseline=433`, `new=37`).
- **Migration Baseline**: The approved baseline identity is
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`; program-created targets are
  accounted for separately by the validator inventory.

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| ADM-001 | Start reciprocal Spec, Plan, Task, and index lineage | platform | Done | `python3` reciprocal-lineage assertion in Plan Task 1 Step 4; logical commit `docs(execution): start authored document migration` |
| ADM-002 | Publish the baseline disposition and durable research ledger | platform | Done | Pre-ledger RED was sole `LEDGER-MISSING`; final inventory/ledger equality is exactly 469 paths (`baseline=433`, `new=38`) with 14 columns, a pinned self-row, `preserve=183`, `transform=227`, `merge=59`, zero ledger Markdown/cross-document diagnostics, and empty semantic items; logical commit `docs(migration): inventory authored document dispositions` |
| ADM-003 | Normalize Stage 01–03 active design documents | platform | Done | Exact 34-path manifest SHA-256 `3cd63fa57b386f8036f14a8a59638318b5686fe4b618422b8577ad106f54e29f`; seven atomic batches `5/5/5/5/5/5/4` each returned zero exact-path diagnostics; all 34 ledger rows record official-primary or explicit repository-only source applicability and `shape-normalized`; compatibility debt moved from `266/1299` paths/occurrences to `232/1127`; logical commit `docs(migration): normalize active sdlc design documents` |
| ADM-004 | Normalize Stage 04–05 execution and operations documents | platform | Done | Exact 120-path allowed manifest SHA-256 `ac9ca4985d0f8945ae342294bcb059fb00d5f343c5167d3c71378e3b0e6c2a8e`; corrected debt-removal manifest SHA-256 `947e7a5e37ace8e0da7099fad2a7891d371308a52ec214d52b734419988fd565`; 24 atomic five-path checkpoints each returned zero exact-path diagnostics; independent correction reconstructed 47 Task safety boundaries, restored seven Plan fence interiors from `851007d`, canonicalized nine Runbooks, and added semantic-review evidence to the same 63 ledger rows; final Task re-review corrected nine Task-table range endpoints and the two affected validation-command/live-lane records across exactly ten Task and ledger rows; remaining debt is `112` paths, `626` occurrences, and `602` token obligations; final exact set is `120` documents plus six evidence/validation owners; zero-cap correction dependency `851007d`; logical commit target `docs(migration): normalize execution and operations documents` |
| ADM-005 | Normalize governance, Current references, Archive links, and six support documents | platform | Done | Exact 73-path allowed manifest SHA-256 `c9788e8f27a3497ab459aae2d0b001d98323672cefb0e1228ef328331749fe95`; debt-removal manifest SHA-256 `5d8b9fc200e0029011b1c8469492ee99a555e6e979979851ffb5d77284b1a9d1`; 15 atomic batches returned zero exact-path diagnostics; final debt is `39` paths, `102` occurrences, and `102` obligations, solely the frozen ADM-006 cloud set; exact rollback unit is 73 documents plus six evidence/validation owners; logical commit `docs(migration): normalize governance references and archive links` |
| ADM-006 | Consolidate AWS and Azure example documentation | platform | Done | Immutable source59 SHA-256 `2ed87a48e9b62da9e16f904f0bbe2ebdf3f1ebaef5be55fdcf06b1608c3a315b`; allowed70 SHA-256 `3c297fa6f0feedbd813b3e3de467a1cb6f0d01da44253951a737b15e756877b9`; approved AWS/Azure snapshot SHA-256 values `650c3cd13bc8fc555db11cd9ee42de0831b910b20780418f8ba37e1bcf69c1fc` / `c16bdd939e998775c0c18d251226a1e2cc301503e1127a69360c540f080d9081`; post-delete graph SHA-256 `d5f345ab514f1359518dac709c62842ef46c09aac41094fbb76a52656331615e` proves zero source-target, external, consumer, and unresolved deletion edges; current ledger equality is 412 rows and source-deleted history is exactly source59 with provider-correct `26/33` destinations; README schema 2 proves active `52`, retired `20`, immutable baseline `47+20=67`, and new active `5`, with provider-correct durable destinations; exact-six lifecycle guards pin completed Stage 90 indexes/snapshots, retired source59, retained executable assets, and durable provider destinations while exact-three Azure subentrypoint non-link text remains frozen; the focused registry summary is `README baseline=67 active_current=52 retired=20 declared_total=72 schema=2 exact_set=yes uncovered=0 ambiguous=0`; 22 executable assets remain; debt moved from exact `39/102/102` paths/occurrences/obligations to `0/0/0`, fixture digest `9bc4cbc4eb6a3a53e0ffdaa7465a3085092cf03ec8273881a6d3584fe26218fc`; README text, registry statement-level, and Markdown AST guards, both validator self-tests, compatibility validation, focused hooks, and the repository quality gate pass; exact staged set is 79 paths (`70+9`), with no commit created under the operator boundary; logical commit target `docs(migration): consolidate cloud example documentation` |
| ADM-006C | Retire residual relationship aliases before strict cutover | platform | Ready for review | Exact 17-document set is the reviewed ADM-003C exact-16 plus ADM-004C exact-1 split; canonical sorted-NUL SHA-256 `345cbbfa545bb2850b57155ce6f65aab79e624f0fd14c4c915748072b2802e86`; RED was exactly `43` diagnostics (`17` required, `26` unsupported) over those paths; implementation preserves unique link targets, fenced blocks, document facts, and lifecycle state while producing one `Traceability` H2 and zero legacy relationship H2s per document; no-container diagnostics are zero; exact staged target is 21 modified paths; independent review and commit remain required |
| ADM-007 | Enable strict validation and close Spec 030 | platform | Queued | `python3 scripts/validate-document-contract-registry.py --root . --mode strict`, both semantic validators in strict mode, and `bash scripts/validate-repo-quality-gates.sh .`; logical commit `chore(docs): cut over document profiles to strict validation` |

## Approval and Safety Boundaries

- **Allowed Paths**: Only the exact path set declared by the active ADM Plan
  Task may change. ADM-001 is limited to its seven Spec, Plan, Task, index, and
  canonical progress-ledger paths. ADM-003 through ADM-006 use the reviewed
  disjoint fixture allocation `34/120/73/39`; ADM-005's thirteen handoff paths
  are structural-only and retain Spec 027/031 semantic ownership. ADM-006's
  document manifest is exactly 70 paths: 59 deletions, two snapshots, and nine
  relocation-only README paths. The three added Azure `gitops`,
  `infrastructure`, and `kubernetes` READMEs may change only the eight relative
  links that resolve into the deletion set; all nine paths retain Spec 028
  profile/body ownership.
- **Forbidden Paths**: Credentials, secrets, ignored `_workspace` children,
  local diagnostics, provider or cluster state, generated outputs, and paths
  outside the current ADM wave are excluded.
- **Approval Required**: Human approval is required before accepted-ADR
  supersession, cloud-document deletion, strict cutover, remote push or merge,
  publication, credential access, or live mutation.
- **Static Validation**: Run each Plan Task's RED/GREEN assertions, exact
  inventory or manifest checks, applicable semantic validators, repository
  quality gate, `git diff --check`, exact staged-path proof, and pre-commit.
- **Live Validation**: DEFER. Spec 030 changes authored repository content and
  does not establish Kubernetes, Argo CD, Vault, ESO, or cloud-provider runtime
  readiness.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  tokens, keys, certificates, kubeconfigs, secret values, Vault data, auth
  files, shell history, or ignored local state.
- **Rollback Plan**: Revert ADM commits newest-first. Each wave keeps content,
  ledger rows, finite-debt removal, validator proof, and execution evidence in
  one logical rollback unit.
- **Evidence Location**: This Task, its parent Plan, the durable migration
  ledger after ADM-002, the canonical progress ledger, logical commits, and
  ignored `.superpowers/sdd/adm-*-report.md` review packages.
- **GitOps Impact**: None; desired-state behavior is outside Spec 030.
- **Kubernetes Impact**: None; no live cluster command is authorized.
- **Operations / Runbook Impact**: Authored operational documents may be
  normalized in ADM-004 without changing live system behavior.

## Verification Summary

ADM-001 started from the expected RED state: the Task path was absent, so the
three-document lineage assertion exited 1 before reading any reciprocal links.
GREEN requires the Spec, Plan, and Task to name each other, unique active rows
in all three Stage indexes, exactly seven ADM rows, an append-only progress
entry, `git diff --check`, focused pre-commit, and an exact seven-path change
set. These checks are repository-static and do not access ignored local state,
secrets, live systems, remote CI, publication, push, merge, or deployment. Its
committed Task adds one normal authored target, so ADM-002 now consumes exactly
468/current and 37/new before ledger creation and must produce 469/current and
38/new with the ledger self-row.

ADM-002 published the sole durable migration evidence owner after proving the
fixture-derived `34/120/73/39` wave partition. The ordered 469-row table equals
the final inventory exactly, its cloud source rows merge to the two ADM-006
snapshot destinations, all remaining registered debt rows transform in their
own wave, and all other paths preserve themselves. The compatibility debt
container remains schema-v1 and growth-closed with `items: []`; strict and
compatibility cross-document checks now have zero ledger diagnostics.

Post-commit quality review corrected two orchestration boundaries without
changing the ledger rows: the Markdown self-test now evaluates the production
corpus against the current Asia/Seoul date while retaining fixed dates for
parser fixtures, and the active-currentness stale-contract scan excludes only
the exact migration ledger because its required inventory rows name archived
paths as evidence rather than current authority. Exact-path negative proof
prevents the exception from widening to other Stage 90 documents.

The first ADM-003 batch rehearsal changed only five documents while leaving
their compatibility records in place. The semantic validator correctly
returned nonzero `DEBT-UNUSED` failures, proving that a document-only batch
cannot satisfy the advertised checkpoint. Those edits were fully reverted.
The corrected ADM-003 through ADM-005 sequence now makes each batch atomic
across its exact documents, ledger rows, fixture records, and cumulative
fixture/validator caps; the next batch remains blocked until compatibility
mode reports zero diagnostics for the exact current NUL batch. The repository
quality gate's complete-fixture digest and mutation proof are refreshed once
after the wave's final batch, not at every intermediate checkpoint.
ADM-006 performs the final permitted cap/self-test synchronization after its
39 records are removed. Every ADM-003 through ADM-006 commit runs a staged
line guard that rejects validator changes outside the frozen numeric cap and
self-test comparisons.

ADM-004 batch 07 consumed the sole `BODY-H2-DUPLICATE` record and legitimately
reduced that rule cap to zero. Python's `Counter` omits zero-valued keys, so the
old self-test's raw `dict(Counter)` comparison failed even though fixture and
production diagnostics agreed. The bounded correction projects actual counts
over the existing `EXPECTED_DEBT_CAPS` keys; it changes no parser, diagnostic,
outcome, route, rule ID, or CLI behavior. The staged-line guard permits only
that exact expression in addition to the previously allowed numeric updates.

ADM-003 completed the exact approved Stage 01–03 wave: five PRDs, five ARDs,
four accepted ADRs, and twenty Specs now use their canonical H2 shapes while
preserving every non-heading fact. The frozen manifest contains 34 paths with
SHA-256 `3cd63fa57b386f8036f14a8a59638318b5686fe4b618422b8577ad106f54e29f`
and was applied in seven atomic batches of `5/5/5/5/5/5/4`; every batch
finished with zero compatibility diagnostics for its exact NUL manifest.
Each corresponding durable-ledger row records whether the normalization used
an official primary source or an explicit repository-only contract review,
and all 34 results are `shape-normalized`.

The completed wave removed exactly its 34 fixture records. Affected-path and
semantic-occurrence debt moved from `266/1299` to `232/1127`; the remaining
required-heading/residue union is 196 paths with 51 overlaps. The complete
fixture semantic digest and mutation proofs now pin those after-values, while
the staged validator guard proves that only frozen numeric cap and self-test
expectations changed. The wave does not touch README profiles, ADM-004 paths,
live rules, templates, CI, agents, scripts beyond the two validation owners,
secrets, remote state, or cluster state.

ADM-004 completed the exact approved Stage 04–05 wave: forty-nine Plans,
forty-seven Tasks, eight Guides, seven Policies, and nine Runbooks now use
their canonical H2 boundaries while preserving commands, historical results,
dates, limitations, and operational meaning. The frozen allowed manifest
contains 120 paths with SHA-256
`ac9ca4985d0f8945ae342294bcb059fb00d5f343c5167d3c71378e3b0e6c2a8e`;
the corrected debt-removal manifest has SHA-256
`947e7a5e37ace8e0da7099fad2a7891d371308a52ec214d52b734419988fd565`.
Twenty-four atomic five-path checkpoints each finished with zero
compatibility diagnostics for its exact NUL manifest, and all 120 durable
ledger rows are `shape-normalized` with exact-source review evidence.

The completed wave removed exactly its 120 fixture records. Remaining debt is
112 affected paths, 626 occurrences, and 602 token obligations: required
`42/200/200`, residue `52/56/56`, delimiter `24/24/0`, unsupported
`90/346/346` with 228 distinct tokens, and duplicate `0/0/0`; the
required/residue overlap is 4 and union is 90. The complete fixture semantic
digest is
`e95542b4fc35b19fe4ab408088561110b968a57234345029193d3f45766102b1`,
and the refreshed mutation proof covers affected paths and rules plus path,
occurrence, obligation, distinct-token, overlap, and union caps. The bounded
zero-cap self-test correction is the reviewed dependency commit `851007d`.

The final wave change set is exactly 126 tracked paths: the 120 frozen
documents plus the durable ledger, compatibility fixture, Markdown validator,
quality-gate consumer, this Task, and the canonical progress ledger. Rollback
reverts the eventual ADM-004 logical commit as one unit while retaining
`851007d`. The final R2 reconciliation restored only the prior frontmatter
`updated` values on the 24 indexed Stage 05 documents; body normalization,
ledger outcomes, and the exact 126-path set remain unchanged, no README became
stale, and the full repository quality gate passed. ADM-005 remains blocked
until the ADM-004 commit and its independent review are accepted. Reverting
`851007d` is only safe after removing every dependent ADM-004 validator change.

Independent semantic review then identified three bounded authoring defects in
the committed ADM-004 document subset. The correction removes generic Working
Rules and provider-type catalogs from exactly 47 Tasks and reconstructs each
Task's eight safety fields from its own Inputs, executable rows, recorded
verification, and parent authorities. It restores every fence interior in the
exact seven affected Plans byte-for-byte from dependency `851007d`, while
retaining their outer canonical heading normalization. It also puts the exact
nine affected Runbooks in canonical H2 order and consolidates unique Canonical
References links under the sole Traceability owner without changing procedures
or recovery evidence. The same 63 durable-ledger rows now record this
independent semantic decision.

Final Task re-review found that nine generated ranges had continued into a
later evidence table rather than stopping at the first Task Table, and that two
research Tasks retained bare command fragments while one invented a live
`argocd` lane contrary to its preserved limitation. The exact ten Tasks now
derive range endpoints only from the bounded Task Table, retain only complete
recorded static commands, and mark the Current research live lane `DEFER`.
Exactly ten ledger rows record the additional correction. Final closure proves
the exact `13`-path correction above `acdb8e6` and the unchanged `126`-path
combined wave from `851007d`, with `626 DEFER / 0 FAIL`, zero diagnostics on
all 120 wave documents, and a clean index.

ADM-005 completed the exact 73-path governance, Current-reference, and support
wave. The allowed manifest SHA-256 is
`c9788e8f27a3497ab459aae2d0b001d98323672cefb0e1228ef328331749fe95`, and the
reviewed debt-removal manifest SHA-256 is
`5d8b9fc200e0029011b1c8469492ee99a555e6e979979851ffb5d77284b1a9d1`.
Fifteen atomic batches (`5` paths for batches 01–14 and `3` for batch 15)
finished with zero diagnostics for each exact manifest. The 73 durable-ledger
rows are `shape-normalized`, and the complete fixture digest and mutation
proof now pin the ADM-006-only remainder.

All thirteen Spec 027/031 handoff paths received only canonical frontmatter or
section-shape/order changes, duplicate-residue removal, and applicable link
repair. Exact semantic, fence, table, provider, route, schema, form, and
authority preservation checks passed. The frozen ADM-005 manifest contains no
Stage 98 path, so the Stage 98/Tombstone mutation count is exactly zero.

Remaining compatibility debt is exactly `39` paths, `102` occurrences, and
`102` token obligations: required `4/4/4`, residue `17/21/21`, delimiter
`0/0/0`, unsupported `39/77/77` with `37` distinct tokens, duplicate `0/0/0`,
required/residue overlap `4`, required/residue union `17`, and total union
`39`. Its path set equals the frozen ADM-006 AWS/Azure cloud set. The exact
ADM-005 working and rollback unit is `79` tracked paths: 73 documents plus the
durable ledger, fixture, Markdown validator, quality-gate consumer, this Task,
and canonical progress ledger. Revert the eventual ADM-005 logical commit as
one unit; ADM-006 consumes the exact 39-path cloud remainder without reopening
any ADM-005 document or evidence row.

ADM-006 pre-mutation review reproduced the source, debt, ledger, executable
asset, and official-primary evidence but rejected the 67-path boundary because
literal `rg` matching omitted eighteen relative Markdown links. Ten were in
already named README paths; eight were in
`examples/azure/{gitops,infrastructure,kubernetes}/README.md`. The corrected
Plan resolves tracked Markdown destinations with the existing link-validator
parser and freezes every edge into the immutable 59-source set. Its RED graph
contains 265 source-target links: 225 internal deletion-tree links and 40
external links from exactly eight consumers to 23 targets. Those eight
consumers plus the snapshot-pack root index equal the exact nine Spec 028
relocation-only README paths.

The correction preserves the source identity
`2ed87a48e9b62da9e16f904f0bbe2ebdf3f1ebaef5be55fdcf06b1608c3a315b`,
the 39-path debt identity
`35ad28eee5da9f73bb5878f18a05c2282785b43187e5657424c563fd03f96034`,
and all `102` tuples. It replaces only the unsafe allowed/inbound boundaries:
the exact 70-path allowed identity is
`3c297fa6f0feedbd813b3e3de467a1cb6f0d01da44253951a737b15e756877b9`,
and the resolved graph identity is
`2ecf54da33dd7f2163db470ae447e79be7693b079f341a8e69d57fc20561fcdc`.
The regenerated debt manifest that binds those immutable source/debt identities
to the 70-path allowed set and resolved graph has SHA-256
`b3590d397620f6e45280073140eacb08b07034b1f24b82d54f6fc987e42b36f1`.
After README rerouting, ADM-006 must prove zero external deletion-target edge
and zero unresolved local link before deleting any source. This four-owner Plan
correction creates no snapshot, changes no README/source/fixture, and does not
authorize mutation until a fresh preparation review approves the new hashes.

ADM-006 completed only after independent pre-deletion approval bound both
immutable snapshots, source59, allowed70, debt39/102, the resolved link graph,
the exact nine relocation-only README paths, and 22 executable assets. The AWS
and Azure snapshot SHA-256 values remain
`650c3cd13bc8fc555db11cd9ee42de0831b910b20780418f8ba37e1bcf69c1fc` and
`c16bdd939e998775c0c18d251226a1e2cc301503e1127a69360c540f080d9081`.
The 59 deleted paths are absent from both the tracked inventory and filesystem;
all 22 non-Markdown provider assets remain outside the deletion set.

The durable ledger now separates current authority from retained history. Its
first table equals the 412-path current corpus, including two current snapshot
rows. Its second table retains all fourteen fields for exactly the source59
set: 26 AWS rows target only the AWS snapshot, 33 Azure rows target only the
Azure snapshot, and every result is `merge-complete; source-deleted` under the
independent ADM-006 reviewer. The post-delete resolved graph contains zero
source-target, internal, external, consumer, and target edges and has SHA-256
`d5f345ab514f1359518dac709c62842ef46c09aac41094fbb76a52656331615e`.

The approved 39 paths and 102 diagnostic/token tuples were removed exactly,
leaving the schema-v1, Spec 030-owned, growth-closed compatibility container
empty for ADM-007. Every semantic cap is zero; the complete fixture digest is
`9bc4cbc4eb6a3a53e0ffdaa7465a3085092cf03ec8273881a6d3584fe26218fc`,
and the quality gate protects owner, growth, profile/baseline, empty
affected-path, rule-cap, occurrence/obligation/distinct-token, overlap, and
union mutations. The Markdown validator diff guard permits only the final
numeric caps and reviewed zero-safe self-test. The README text guard permits
only the exact-six pinned lifecycle/status replacements and freezes the three
Azure subentrypoint whole-file link-only states. The registry statement-level
AST guard permits only the two README retirement functions and one pinned
schema-2 summary expression; all other production and self-test AST remains
identical to its approved baseline.

The exact staged unit is 79 paths: allowed70 plus the durable ledger, empty
compatibility fixture, registry validator, Markdown validator, quality-gate
consumer, README schema-2 fixture, fixture handoff documentation, this Task,
and canonical progress ledger. No commit was created. Before commit, rollback
is the exact 79-path inverse/unstage operation; after a future logical commit, use
`git revert <ADM-006-commit>` so both snapshots, all 59 deletions, nine README
routes, ledger history, fixture, validators, and execution evidence return
atomically. ADM-007 owns only removal of the now-empty compatibility containers,
strict-mode cutover, and Spec 030 closure; it must not reopen ADM-006 content.

ADM-006C removes the last residual relationship-heading aliases before that
cutover. Its hardcoded exact-17 set is split between the ADM-003C exact-16 and
ADM-004C exact-1 escape owners, and its atomic review boundary is those
documents plus this Task, the Plan, durable ledger, and progress memory. The
pre-edit no-container result was exactly `43` diagnostics; after
canonicalization it is zero. Unique link-target sets and fenced-block counts
are unchanged, and no fixture, registry, validator, provider, CI, protected
surface, or live behavior is changed. The implementation is ready for an
independent review before the logical commit
`docs(migration): retire residual relationship aliases`.

## Traceability

- **Spec**: [Authored Document Migration Technical Specification](../../03.specs/030-authored-document-migration/spec.md)
- **Plan**: [Authored Document Migration Implementation Plan](../plans/2026-07-12-authored-document-migration.md)
- **Previous Tranche**: Semantic Document Validation, Spec 029
- **Next Tranche**: Affected Surface and Agent QA, Spec 031
