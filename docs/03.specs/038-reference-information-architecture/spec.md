---
title: 'Reference Information Architecture Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-22
---

# Reference Information Architecture Technical Specification (Spec)

## Overview

This Spec consolidates the authority, currentness, generation, freshness, and
duplicate rules for docs/90.references. It keeps audits, research, data,
generated LLM navigation, learning material, and historical archive records
distinct while preventing any of them from becoming an accidental policy,
plan, runbook, or runtime owner.

The reciprocal implementation
[Plan](../../04.execution/plans/2026-07-22-reference-information-architecture.md)
and [Task](../../04.execution/tasks/2026-07-22-reference-information-architecture.md)
activate eight dependency-ordered work packages, RIA-000 through RIA-007,
from reviewed activation and rollback parent
`fdc86ee9156a35f48d57916be4ecb3505e483a50`. Plan-only RED and the 49-Plan /
51-Task inventory were captured at evidence baseline
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; prerequisite commits changed no
Stage 04 document, so the proposed pair raises that corpus to 50 Plans and 52
Tasks. Activation commit `cb0c1f6` completed RIA-000. RIA-001 completed through
reviewed commits `68e46fc`, `566c74f`, and
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`; its final requirements and quality
reviews were clean. RIA-002 is In Progress at reviewed design correction only:
its implementation RED has not begun, and no remote or live result is claimed.

## Strategic Boundaries & Non-goals

- **In scope**: docs/90.references and subdirectories, Current-pack pointers,
  remediation overlays, source/freshness metadata, generated-output ownership,
  category indexes, duplicate detection, cross-links, and directly affected
  templates/support rules.
- **Non-goals**: Rewriting dated observation facts, merging snapshots solely
  because topics overlap, defining active governance in references, or
  creating a retrieval/vector runtime.

## Contracts

- Audits own dated implementation observations and a separately maintained
  remediation overlay; exactly one pack is Current.
- Research owns dated external-source synthesis and source ledgers; exactly one
  current research pack may be selected for a program.
- Data owns repo-backed facts, source checks, and refresh triggers.
- llm-wiki owns only deterministic generated canonical-owner navigation.
- Learning owns non-authoritative study roadmaps.
- Archive owns immutable non-current records and is not a reference-policy
  substitute.
- A dated snapshot is not a duplicate merely because a later snapshot exists.

## Core Design

Registry current-pack entries, folder indexes, and generated-output checks
provide one discoverable currentness path. Historical and Resolved packs keep
their bodies and observation SHAs. Current closure changes only remediation
overlays. Schema version 2 keeps `snapshotGuard.sourceCommit` exclusively for
the five Historical/Resolved audit packs and Historical research pack
`research/2026-07-04-wer`. A required top-level `currentPackBaselines` map is
keyed exactly by the live registry's Current pack IDs and pins each pack to an
anchored `git-sha1:` commit. The initial audit and research pins are the
reviewed RIA-001 head
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`.

The contract never supplies Current member paths, per-member digests, or
pointers. The validator first reads the exact constant registry path
`docs/99.templates/support/document-profiles.json` through a bounded stage-zero
index reader. For that path and every later registry-derived exact safe path it
runs only `/usr/bin/git ls-files -z --stage -- <safe-path>`, requires exactly one
stage-0 entry in regular mode `100644` or `100755`, reads that fixed blob, and
requires a bounded `O_NOFOLLOW` regular worktree read to equal the index bytes.
Missing, deleted-plus-untracked, unmerged stage 1/2/3, symlink `120000`,
submodule `160000`, duplicate, unsafe-path, or index/worktree-drift inputs fail
before semantic comparison. Proposed authority is therefore the verified
stage-zero blob, never an untracked or worktree-only replacement.

Only after the registry itself passes that boundary may validation derive pack
README and member paths or digests. The baseline commit's registry `profileId`,
pack IDs, member lists, and `allowedStates` must equal the proposed registry
exactly, and every derived README/member must exist as a regular blob at the
baseline and as the equal verified proposed index/worktree object. Fact-bearing
pack READMEs remain protected outside exact table-cell or link-destination
navigation projections.

The code-owned immutable Current root is
`git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`. The exact two-key map always
pins the audit pack to that root. Audit admits no transition or settlement.
Research has only three valid states: root (root pin, no records), open (root
pin, exactly one `ria-007-postflight-ledger` transition from root and no
settlement), or settled (no open transition, map pin equal to literal C2, and
exactly one matching durable settlement whose prior open-C2 proof validates).
Every other map value, record cardinality, arbitrary or forged root, audit
transition, and reused ID fails the schema and code-owned state machine.

Top-level `baselineTransitions` and `baselineSettlements` provide the only
bounded way to advance a Current baseline. Normally the transition array is
empty and it may contain at most one open record. An open transition is not a
baseline, member, path, digest-list, or pointer authority: it is the one-shot
`ria-007-postflight-ledger` authorization for the registry-derived
`document-migration-evidence-ledger` member of one Current pack, from the
active map pin to one exact SHA-256 and byte length no greater than 2 MB. All
other Current members and the registry must still equal the old baseline.
Historical targets, arbitrary paths or digest lists, `HEAD`, revision
expressions, self-references, detached candidates, and reused transitions are
invalid. Terminal validation with `--require-settled-baselines` fails while a
transition remains open.

A settlement-only commit changes no protected content, advances the affected
map value to the literal preceding transition commit, removes the open record,
and appends a durable settlement proof naming that literal C2 commit.

Staged C3 validation is selected only by `--staged`. The validator resolves the
current branch commit through one fixed internal argv,
`/usr/bin/git rev-parse --verify HEAD`, parses exactly one lowercase commit OID,
verifies its type, and requires it to equal settlement `transitionCommit` C2.
`HEAD` is never contract, baseline, transition, or caller-supplied authority;
no caller or contract revision expression is accepted. A bounded fixed
`diff-index --cached --name-status -z --no-renames <C2-oid> --` comparison must
show that the proposed index differs from C2 only at the exact contract path.
The verified contract worktree bytes must equal that index blob.

Post-C3 durable evidence uses mutually exclusive explicit-ref mode
`--commit git-sha1:<C3>`. It parses that literal commit object through the fixed
Git reader, requires exactly one parent equal to literal C2, and validates the
C3 contract/tree/blob rather than current index or worktree bytes. Detached or
non-parent C3, zero-parent, and merge-parent commits fail. Normal mode validates
the current verified index/worktree state but proves no commit lineage; staged
mode proves proposed C3 against current branch parent C2; explicit-ref mode
proves the immutable post-C3 commit chain. Only explicit-ref settled validation
can supply terminal post-commit lineage evidence.

When a settlement is present, each applicable mode uses the same fixed Git
object reader to prove that C2 contained the matching open transition, retained
the root baseline and equal registry, contained the exact target bytes, and left
all non-target members unchanged. Root/open validation does not invent a C2.
Direct baseline jumps, missing or mismatched proof, clearing without proof,
arbitrary pins, and transition-ID reuse fail closed with `RIA-TRANSITION`.

Duplicate analysis compares normalized scope, authority claim, source coverage,
generation owner, and current state. It consolidates only duplicate current
owners, generated/manual pairs, and policy text copied into references.

Generated wiki output is accepted only when its tracked file equals generator
output. Manual edits and stale canonical-owner paths fail.

## Data Modeling & Storage Strategy

Reference profiles record role-specific allowed states and body evidence
without adding a universal frontmatter expansion. Source check, observation
date, adopted/rejected source scope, authority boundary, and refresh trigger
remain semantic body contracts where the profile requires them.

Generated ownership is a registry relation between generator, output, inputs,
and validation command. Data freshness uses explicit triggers rather than an
arbitrary universal expiration date.

## Interfaces & Data Structures

- Current-pack validator: schema-v2 exact baseline map, profile, pack ID,
  registry-derived README/members and digests, states, observation SHA,
  protected README projection, index row, unique Current pointer, and durable
  transition/settlement chain.
- Source-ledger validator: source URL, checked date, adopted/rejected scope, and
  refresh trigger.
- Generated-output validator: generator path, input roots, output path, and
  no-diff result.
- Duplicate-owner validator: normalized role, scope, lineage, current state,
  and canonical replacement.

## Edge Cases & Error Handling

- A Historical pack containing the word Open does not reopen a finding.
- A Current audit can contain DEFER for live evidence without losing Current
  status.
- A research conclusion that becomes policy must be promoted to its owner and
  linked; the reference remains evidence, not the policy source.
- Generated output missing its tool is SKIP or DEFER according to the owning
  contract, never PASS.
- Learning content may overlap a technical topic but cannot own operational
  instructions.
- A Current baseline cannot advance merely because proposed bytes are valid;
  only the one-member open-transition commit followed by its contract-only
  settlement proof can advance it.
- A clean normal-mode result is byte/state evidence, not C3 parent evidence;
  terminal lineage requires literal `--commit git-sha1:<C3>` explicit-ref mode.

## Failure Modes & Fallback / Human Escalation

- If two documents claim the same Current scope, stop consolidation until the
  owner and preservation disposition are approved.
- If source currentness cannot be verified, preserve the dated snapshot and
  mark its currentness limitation.
- If a generator is unavailable, validate the tracked contract statically and
  record the missing execution separately.
- If a baseline transition is open, non-terminal validation may verify its
  exact candidate while terminal validation fails until settlement; no hidden
  or detached candidate commit is accepted.

## Verification Commands

- Run Current-pack, member, index, and observation-SHA checks.
- Run schema-v2 baseline-map, registry-equivalence, transition, settlement,
  and terminal `--require-settled-baselines` checks.
- Run proposed index/worktree authority tests and staged/explicit-ref settlement
  lineage tests, including detached, non-parent, and merge-parent commits.
- Run reference profile, source/freshness, and duplicate-owner validation.
- Regenerate llm-wiki and require no diff.
- Run link, repository quality, Markdown, and all-files pre-commit checks.
- Run staged lifecycle admission for the exact reciprocal Spec 038 Plan/Task
  activation before beginning RIA-001.

## Success Criteria & Verification Plan

- **VAL-RIA-001**: Audit and research Current pointers are unique and complete.
- **VAL-RIA-002**: Historical and Resolved observation bodies remain unchanged.
- **VAL-RIA-003**: Current closure updates only the remediation overlay and
  affected indexes, or uses the one-shot ledger transition and durable
  settlement proof without weakening any other Current member.
- **VAL-RIA-004**: Data references name source evidence and refresh triggers.
- **VAL-RIA-005**: Generated wiki output has one generator and zero drift.
- **VAL-RIA-006**: Duplicate Current owners, generated/manual duplicates, and
  active-policy copies under references are zero.

### Execution Evidence

The Plan-only staged RED exited `1` with `LIFECYCLE-CREATE`: the lifecycle
validator expected exactly one active Plan and one active Task and observed
`Plan count 1, Task count 0`. The complete activation proposal adds the
reciprocal Task, links this Spec to both execution records, updates the three
stage indexes, and updates the exact 14-column migration ledger. The
PRD-006 registry relation already marks Spec 038 active and remains unchanged.

Focused activation GREEN is observed: staged lifecycle, registry self-test 119,
strict inventory 446, strict Markdown zero, cross-document valid,
changed-file Markdownlint, and cached diff passed. Initial independent
requirements and quality reviews both required changes; the Plan now includes
RIA-000, per-commit all-files gates, derived membership, Historical research
and README projections, pair-scoped exceptions, adopted/rejected source scope,
Draft 2020-12 instance validation, and split RIA packages. The first all-files
attempt exposed the predecessor Spec 037 active-control admission gap and a
Git-SHA secret false positive. Reviewed prerequisite commits `5ed6de6` and
`fdc86ee` preserve the frozen closure ledger, reject unadmitted Stage 04
artifacts, and admit this exact pair as `active_controls=2/1`; `git-sha1:`
removes the false positive without weakening the pin. Exact changed-file and
all-files pre-commit plus both diff checks now pass with no skipped hook or
formatter change. The first re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY CHANGES REQUIRED`; the proposal now closes the anchored `git-sha1:`
schema/parser, immediate parent `fdc86ee`, and fixed-argv bounded Git object
reader findings. Final focused re-reviews returned `REQUIREMENTS COMPLIANT`
and `QUALITY APPROVED` with no findings. Activation commit `cb0c1f6` completed
RIA-000.

RIA-001 completed through `68e46fc`, `566c74f`, and `15bba3d`. Final focused
reviews returned exact verdicts `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`, findings none. Focused unit, CLI self-test/production, and
Draft 2020-12 schema/instance validation passed. Historical raw hook output,
CI, remote, and live execution are not reconstructed or claimed here.

Before
RIA-002 RED or implementation began, preflight at reviewed RIA-001 head
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe` proved the original single
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47` baseline impossible for Current
research: activation commit `cb0c1f6` changed the protected migration ledger's
inventory boundary from 444 to 446 outside every allowed projection. No
RIA-002 RED or implementation occurred. Design correction commit `08cf17d`
received `QUALITY CHANGES REQUIRED` with four Important findings. This
follow-up proposal closes settlement lineage, proposed tracked authority, the
root state machine, and execution-status truth; follow-up approval is not yet
claimed. RIA-002 is In Progress at design review only. It separates Historical
snapshot evidence from Current baselines and adds the bounded
transition/settlement chain; it does not alter Current pack
membership, observation bodies, CI/FIFO, provider, remote, live, credential,
secret, or ignored-workspace state.

## Traceability

- **Foundation**: [Spec 035](../035-document-schema-and-lifecycle-contract/spec.md)
- **Final integrator**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **Current audit**: [2026-07-11 WEIA](../../90.references/audits/2026-07-11-weia/README.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Plan**: [Reference Information Architecture Implementation Plan](../../04.execution/plans/2026-07-22-reference-information-architecture.md)
- **Task**: [Reference Information Architecture Task](../../04.execution/tasks/2026-07-22-reference-information-architecture.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-001 | Registry and index checks enforce unique Current packs. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-002 | Historical-body guard compares observation snapshots with baseline. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-003 | Overlay fixtures restrict mutable projections; transition/settlement fixtures prove the one-member durable baseline chain. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-004 | Reference body-contract checks verify source and freshness fields. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-005 | Generator no-diff validation protects the wiki index. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-006 | Duplicate and policy-residue fixtures fail. |
