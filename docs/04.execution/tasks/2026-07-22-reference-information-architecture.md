---
title: 'Task: Reference Information Architecture'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-26
---

# Task: Reference Information Architecture

## Overview

This Task is the execution, verification, review, and rollback evidence owner
for RIA-000 through RIA-007. It records the reciprocal Spec 038 execution pair
from reviewed activation and rollback parent
`fdc86ee9156a35f48d57916be4ecb3505e483a50`. Plan-only RED and the 49-Plan /
51-Task inventory were captured at evidence baseline
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; prerequisite commits changed no
Stage 04 document, so this pair raised the corpus to 50 Plans and 52 Tasks.
RIA-000 through RIA-006 are Completed from observed commits, package tests,
repository gates, and clean final package reviews. RIA-007 C1 exact-seven
commit `8c0dcea558212e11ac93a0fe626cddb31315859b` closed the six lifecycle
paths and registry state after final `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` reviews. The activation-to-C1 explicit-ref lifecycle and
repository-static clean-tree postflight passed. The current C2 exact-nine
staged proposal records that evidence in the six lifecycle paths and 446-row
ledger, opens the bounded contract transition, and adds only the final target
digest's exact false-positive adjudication to `.secrets.baseline`. It has no
known C2 identity or postcommit result, C3 identity, settlement, terminal
explicit-ref result, or remote/live, CI-hosted, or provider claim.

The activation preserves the existing registry as the sole Current audit and
research pack owner. It authorizes a separate reference-information contract
only for observation immutability, Current overlay mutability, source and
freshness evidence, generator relations, and duplicate-owner rules. It does
not authorize observation rewriting, CI/FIFO work, live checks, ignored
scratch inspection, or Specs 039-046 activation.

RIA-002 design preflight at reviewed RIA-001 head
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe` found that the original
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47` Current baseline could not pass:
activation commit `cb0c1f6` changed the protected research migration ledger's
inventory boundary from 444 to 446 outside all allowed projections. Work
stopped before the initial RIA-002 RED. Design correction commits `08cf17d` and
`f0c019a` then established schema version 2, separate Historical and Current
baselines, stage-zero authority, the root/open/settled FSM, and the one-shot
transition/durable-settlement chain with approved requirements and quality
reviews. Implementation commits `13835e9`, `e29c6fb`, `27a63b3`, and
`c278173` completed those guards with 37/37 focused tests and repository gates
passing. The later package rows record the exact RIA-003 through RIA-006
results.

## Inputs

- [Reference Information Architecture Implementation Plan](../plans/2026-07-22-reference-information-architecture.md)
- [Spec 038](../../03.specs/038-reference-information-architecture/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [Current audit pack](../../90.references/audits/2026-07-11-weia/README.md)
- [Current research pack](../../90.references/research/2026-07-07-wer/README.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [Predecessor Spec 037 Task](./2026-07-18-active-corpus-and-execution-retention.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| RIA-000 | Activation gate | Commit the exact seven-file reciprocal Plan/Task activation with staged lifecycle, complete per-commit QA, independent planning re-reviews, evidence baseline `8fb9821`, and rollback parent `fdc86ee`. | platform | Done | Activation completed. | Commit `cb0c1f6`; exact seven-file scope; Plan-only `LIFECYCLE-CREATE` RED, focused GREEN, final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. |
| RIA-001 | VAL-RIA-001 | Add the closed Draft 2020-12 reference schema/contract, safe loader, stable diagnostics, CLI self-test, and hostile boundary fixtures without duplicating Current member paths, digests, or pointers. | platform | Done | Contract bootstrap and safe validator completed. | Commits `68e46fc`, `566c74f`, `15bba3d`; focused unit, CLI self-test/production, schema/instance PASS; final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. Historical raw hook output and remote/live PASS are not claimed. |
| RIA-002 | VAL-RIA-002, VAL-RIA-003 | Implement schema-v2 Historical/Current separation, stage-zero proposed authority, exact root FSM, bounded overlay, and one-shot ledger transition/durable settlement lineage. | platform | Done | Historical/Current baseline protection and exact lineage proof completed. | Design commits `08cf17d`, `f0c019a`; implementation commits `13835e9`, `e29c6fb`, `27a63b3`, `c278173`; focused 37/37 and repository gates PASS; requirements compliant and quality approved. |
| RIA-003 | VAL-RIA-004 | Enforce repo evidence, HTTPS source, checked date, adopted/rejected scope, and refresh trigger for every current data asset. | platform | Done | Exact nine-asset source/scope/freshness ledger and inventory proof completed. | Commits `7083909`, `77e081d`; focused 43/43 and repository gates PASS; requirements compliant and quality approved. |
| RIA-004 | VAL-RIA-005 | Enforce one fixed-argv generator/input/output/check relation and zero LLM Wiki drift. | platform | Done | Immutable generator/input/output/owner relation and zero-drift proof completed. | Commits `5d15c1c`, `0cb1789`; focused 46/46 and repository gates PASS; requirements compliant and quality approved. |
| RIA-005 | VAL-RIA-001, VAL-RIA-006 | Reject duplicate Current and generated/manual owners plus normalized active-policy copies, with only exact pair-scoped structural exceptions. | platform | Done | Current-owner, generated/manual, pair-scoped exception, and policy-copy guards completed. | Commits `671e722`, `000cf858`; focused 81/81 and repository gates PASS; requirements, parser, and quality review approved. |
| RIA-006 | VAL-RIA-001 through VAL-RIA-006 | Integrate self-test-before-production validation into repository aggregate QA and command inventories. | platform | Done | Aggregate self-test-before-production integration and inventories completed. | Commit `76c1d4b`; focused 82/82 and aggregate gates PASS; requirements compliant and quality approved. The closed post-validate environment still lacks `gitleaks` on `/usr/bin:/bin`; Spec 039 owns that limitation. |
| RIA-007 | VAL-RIA-001 through VAL-RIA-006 | Preserve the exact C1 closure/postflight, separately gated C2 open-transition proposal, and later contract-only C3 settlement boundaries. | platform | Done | C1 exact-seven commit `8c0dcea558212e11ac93a0fe626cddb31315859b`, final whole-tranche approval, and clean-tree postflight are observed; C2 is staged only. | C1 reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; activation-to-C1 explicit-ref lifecycle and the bounded repository-static postflight passed. The exact-nine C2 proposal includes only the exact-value `.secrets.baseline` adjudication beyond the lifecycle/ledger/contract paths and has no C2 identity/postcommit, C3 identity, settlement, terminal explicit-ref, or remote/live claim. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 038 and its Stage 03 index; this reciprocal Plan and
  Task plus Stage 04 indexes; the migration evidence ledger; a focused Stage
  90 reference IA schema/contract; focused validator, tests, fixtures, and
  script/test inventories; the aggregate quality script; exact Stage 90
  category/pack/reference files only when a validator finding proves the
  bounded correction required by Spec 038.
- **Forbidden Paths**: Historical/Resolved/Current observation rewrites;
  Current pack membership or pointer duplication; CI workflow and FIFO changes
  owned by Spec 039; compatibility removal owned by Spec 040; provider-agent,
  Kubernetes, infrastructure, GitOps, secret, or live-runtime changes; ignored
  `_workspace` children; credentials, tokens, kubeconfigs, auth files, and
  shell history; Specs 039-046 activation.
- **Approval Required**: Push, merge, publication, remote GitHub action, live
  system action, secret handling, dependency installation, or scope expansion
  beyond the approved Spec/Plan requires separate explicit human approval.
- **Static Validation**: Focused unit/self-test/production reference checks,
  generated LLM Wiki no-diff, strict registry/Markdown/cross-document and
  staged lifecycle checks, repository aggregate, all-files pre-commit,
  formatter-diff review, `git diff --check`, and terminal
  `--require-settled-baselines` validation.
- **Live Validation**: `DEFER`. Repository-static results do not prove provider,
  GitHub-hosted, Kubernetes, Vault, ESO, Argo CD, credential, or live state.
- **Secret / Vault Handling**: Do not open or print secret values. Diagnostics
  contain only stable rule IDs, repository-relative paths, and bounded facts;
  ignored scratch is never an evidence source.
- **Rollback Plan**: Reverse newest reviewed logical commit first. Before
  closure, revert the failing RIA package only. After closure, revert the
  contract-only C3 settlement, nine-file C2 transition/postflight/scanner
  adjudication evidence, seven-file C1 closure, then RIA-006 through RIA-001 and activation last; restore
  each protected owner relation before removing its guard.
- **Evidence Location**: This Task, reviewed logical commits, the Stage 90
  reference IA contract, focused tests/fixtures, aggregate results, and terminal
  lifecycle records. Temporary output and subagent scratch are not closure
  evidence.

## Verification Summary

The intentional activation RED staged only the new active Plan and ran
`python3 scripts/validate-document-lifecycle.py --root . --mode staged`.
It exited `1` with `LIFECYCLE-CREATE`, expected exactly one Plan and one Task
creation in state `active`, and observed `Plan count 1, Task count 0`. No
implementation criterion, review verdict, remote/live result, or closure is
claimed from that RED.

The complete activation proposal adds this reciprocal Task, links the active
Spec to the pair, updates the Spec/Plan/Task indexes, and updates the exact
14-column migration ledger. The registry relation was already active and is
not changed. Focused activation GREEN is directly observed: staged lifecycle,
registry self-test 119, strict 446-path inventory, strict Markdown zero,
cross-document valid, changed-file Markdownlint, and cached diff all passed.
The first activation commit-gate run exposed the Spec 037
`CLOSURE-CURRENT-RESIDUE` follow-on admission defect and a Git-SHA
detect-secrets false positive. Separately reviewed prerequisite commits
`5ed6de6` and `fdc86ee` now keep the frozen 100-row terminal ledger unchanged,
reject unadmitted Stage 04 artifacts, and admit only a complete active pair.
The contract example uses `git-sha1:`. With the seven files restaged, the
residue validator passed with `active_controls=2/1`; exact changed-file and
all-files pre-commit, formatter/status inspection, and both diff checks passed
without skipped hooks or formatter changes. Clean planning re-reviews followed,
and activation commit `cb0c1f6` completed RIA-000.

Initial independent requirements review returned
`REQUIREMENTS CHANGES REQUIRED`: it required RIA-000 and complete
all-files/formatter/diff gates before every logical commit. Initial independent
quality review returned `QUALITY CHANGES REQUIRED`: it required runtime-derived
Current membership, Historical research and README projections, pair-scoped
exceptions, adopted/rejected source scope, exact Draft 2020-12 validation,
separate source/generator/duplicate packages, an exact aggregate test, and the
ledger freshness count correction. Those findings are incorporated into the
current proposal. The first re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY CHANGES REQUIRED`; quality required an anchored `git-sha1:`
schema/parser, immediate activation/rollback parent `fdc86ee`, and fixed
`/usr/bin/git` argv, closed environment, timeout, output/size bounds, and strict
tree/blob parsing. Those corrections are incorporated. Final focused
re-reviews returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` with no Critical, Important, or Minor findings. Activation
commit `cb0c1f6` completed RIA-000.

RIA-001 completed through `68e46fc`, `566c74f`, and `15bba3d`. Its final
focused reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with
no findings; focused unit, CLI self-test/production, and Draft 2020-12
schema/instance checks passed. Historical raw hook output, CI, remote, and live
execution are not reconstructed or claimed.

RIA-002 design correction completed in `08cf17d` and `f0c019a`; its final
requirements and quality reviews approved the Historical/Current separation,
stage-zero authority, root/open/settled FSM, and staged/explicit settlement
lineage. Implementation commits `13835e9`, `e29c6fb`, `27a63b3`, and
`c278173` completed schema-v2 baseline protection, bounded overlays, and exact
lineage proof. The package passed 37/37 focused tests and repository gates;
final requirements and quality reviews approved it.

RIA-003 commits `7083909` and `77e081d` added the exact post-closure fixture
admission, nine-asset source/scope/freshness ledger, stage-zero/named-commit
inventory, and control-safe semantic validation. The package passed 43/43
focused tests and repository gates; requirements and quality reviews approved
it. RIA-004 commits `5d15c1c` and `0cb1789` added the exact generator fixture
admission, immutable generator relation, fixed-argv zero-drift check, and
canonical-owner proof. The package passed 46/46 focused tests and repository
gates; requirements and quality reviews approved it.

RIA-005 commits `671e722` and `000cf858` added exact duplicate-owner fixture
admission, single Current-owner cardinality, generated/manual collision
detection, pair-scoped structural exceptions, and bounded visible-Markdown
policy-copy normalization. The package passed 81/81 focused tests and
repository gates; requirements, parser, and quality review dispositions
approved it. RIA-006 commit `76c1d4b` integrated self-test before production
validation and recorded durable script/test command inventories. The package
passed 82/82 focused tests and aggregate gates; requirements and quality
reviews approved it.

RIA-007 C1 exact-seven commit
`8c0dcea558212e11ac93a0fe626cddb31315859b` changed exactly this
Spec/Plan/Task lineage, its three indexes, and the registry's Spec 038
program-lineage state from `active` to `done`. Final whole-tranche reviews
returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. The successful
clean-tree postflight used activation commit
`cb0c1f6131ad6a8cf3f2f2ca18a369b5cd31d77b` through literal C1 and observed
explicit-ref lifecycle PASS; RIA module 85/85; RIA self-test, normal
production, settled-baseline root validation, generator no-diff, registry
self-test/strict, strict Markdown, strict cross-document, terminal residue,
role audit, repository aggregate, all-files pre-commit, both diff checks, and
clean status PASS. An earlier invocation from activation parent
`fdc86ee9156a35f48d57916be4ecb3505e483a50` failed closed because the
reciprocal Plan/Task did not exist at that ref; it was an operator
ref-selection check, not the successful postflight, a repository defect, or
PASS evidence.

The current C2 staged proposal changes exactly the same six lifecycle paths,
the migration ledger, reference contract, and `.secrets.baseline`, for exactly
nine tracked paths. It preserves the 446-row Markdown inventory and
dispositions, keeps both Current baseline pins at the active root, leaves
settlements empty, opens only the ledger-byte-bound transition, and records
only that final digest's exact path/value detect-secrets false-positive
adjudication. The scanner baseline is not a ledger row. C2 has no known SHA or
postcommit result; C3 identity, settlement, terminal explicit-ref, remote,
CI-hosted, provider-runtime, Kubernetes, Vault, ESO, Argo CD, credential,
secret-value, deployment, and live PASS remain unclaimed. The closed
post-validate environment's `/usr/bin:/bin` PATH still lacks `gitleaks`; the
normal PATH repository gates are separate evidence, and this C2 proposal
changes no hook, validator, scanner behavior, or CI topology.

## Traceability

- **Plan**: [Reference Information Architecture Implementation Plan](../plans/2026-07-22-reference-information-architecture.md)
- **Spec**: [Spec 038](../../03.specs/038-reference-information-architecture/spec.md)
- **Predecessor Task**: [Active Corpus and Execution Retention Task](./2026-07-18-active-corpus-and-execution-retention.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [RIA-000](../plans/2026-07-22-reference-information-architecture.md#task-0-ria-000--atomic-reciprocal-planning-activation) | Completed. | Commit `cb0c1f6`; exact seven-file activation, Plan-only lifecycle RED, focused GREEN, final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. |
| [RIA-001](../../03.specs/038-reference-information-architecture/spec.md#success-criteria--verification-plan) | Completed. | Commits `68e46fc`, `566c74f`, and `15bba3d`; focused unit, CLI, schema/instance PASS; final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. Historical raw hook, CI, remote, and live PASS are not claimed. |
| N/A — RIA-002 shares the Plan linked in RIA-000 | Completed. | Design commits `08cf17d`, `f0c019a`; implementation commits `13835e9`, `e29c6fb`, `27a63b3`, `c278173`; focused 37/37 and repository gates PASS; requirements compliant and quality approved. |
| N/A — RIA-003 shares the Plan linked in RIA-000 | Completed. | Commits `7083909`, `77e081d`; exact nine-asset source/scope/freshness and inventory proof; focused 43/43 and repository gates PASS; requirements compliant and quality approved. |
| N/A — RIA-004 shares the Plan linked in RIA-000 | Completed. | Commits `5d15c1c`, `0cb1789`; immutable generator relation and zero drift; focused 46/46 and repository gates PASS; requirements compliant and quality approved. |
| N/A — RIA-005 shares the Plan linked in RIA-000 | Completed. | Commits `671e722`, `000cf858`; owner/collision/exception/policy-copy proof; focused 81/81 and repository gates PASS; requirements, parser, and quality review approved. |
| N/A — RIA-006 shares the Plan linked in RIA-000 | Completed. | Commit `76c1d4b`; self-test-before-production integration; focused 82/82 and aggregate gates PASS; requirements compliant and quality approved; closed-hook `gitleaks` PATH limitation retained for Spec 039. |
| N/A — RIA-007 shares the Plan linked in RIA-000 | C1 closure and clean-tree postflight completed; C2 exact-nine staged proposal prepared. | C1 `8c0dcea558212e11ac93a0fe626cddb31315859b`; final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; activation-to-C1 explicit-ref lifecycle and repository-static postflight PASS. C2 includes the exact-value `.secrets.baseline` adjudication but has no identity/postcommit claim; C3, settlement, terminal explicit-ref, and remote/live evidence remain unclaimed. |
