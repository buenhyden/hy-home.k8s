---
title: 'Reference Information Architecture Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-26
---

# Reference Information Architecture Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this Plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close Spec 038 with one fail-closed Reference Information
Architecture contract that protects dated observations, permits only declared
Current remediation overlays, proves source/freshness and generated ownership,
and rejects duplicate Current or policy owners under `docs/90.references/`.

**Architecture:** Require schema version 2 and keep `referenceCurrentPacks` in
`docs/99.templates/support/document-profiles.json` as the sole owner of Current
pack identity, membership, lifecycle, and pointer mirrors. Add a separate
closed-schema Stage 90 contract whose exact `currentPackBaselines` keys mirror
those pack IDs and whose values pin committed comparison authority without
copying members, paths, digests, states, or pointers. Historical snapshot
authority remains separate. One-shot transition and durable settlement records
advance a Current baseline only through an exact protected-member candidate
commit and a following contract-only settlement. A focused Python validator
loads tracked regular files and fixed Git objects without following symlinks,
emits stable rule IDs, and is integrated into the repository aggregate after
hostile fixtures pass.

**Tech Stack:** Python 3 standard library, the repository's installed
`jsonschema` package with `Draft202012Validator`, `unittest`, Git object reads,
Bash generator checks, Markdown contract tables, pre-commit, and the repository
document lifecycle/registry validators.

This reciprocal Plan records
[Spec 038](spec.md) on
reviewed prerequisite head `fdc86ee9156a35f48d57916be4ecb3505e483a50`,
the activation commit and rollback parent. The Plan-only RED and 49-Plan /
51-Task evidence baseline was
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; prerequisite commits `5ed6de6`
and `fdc86ee` changed no Stage 04 document, so the active pair still raises the
proposed corpus to 50 Plans and 52 Tasks. The activation changes lifecycle
lineage only. Activation commit `cb0c1f6` completed RIA-000. RIA-001 completed
through reviewed commits `68e46fc`, `566c74f`, and `15bba3d`. RIA-002 through
RIA-006 subsequently completed through the exact reviewed commits and package
evidence recorded below. RIA-007 C1 exact-seven commit
`8c0dcea558212e11ac93a0fe626cddb31315859b` changed the reciprocal
Spec/Plan/Task, three indexes, and registry Spec 038 program-lineage state from
`active` to `done`. Final whole-tranche reviews returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, and the activation-to-C1
explicit-ref lifecycle and repository-static clean-tree postflight passed.
The current C2 exact-nine staged proposal records that evidence, opens the
bounded ledger transition, and adds only the final target digest's exact
false-positive adjudication to `.secrets.baseline`; it has no known C2
identity or postcommit result, C3 identity, settlement, terminal explicit-ref
result, or remote/live, CI-hosted, or provider claim.

## Context

Spec 037 is done and its terminal repository-static evidence is retained. The
PRD-006 registry therefore admits Spec 038 as the first dependency-ready
tranche. Specs 039 and 040 remain active and unplanned while this Plan runs;
Spec 039 owns the known all-files `os.mkfifo` portability boundary, and Spec
040 owns final compatibility removal and PRD-006 program closure.

The current registry already enforces exactly one Current audit pack and one
Current research pack, including direct members, allowed lifecycle values,
collection rows, and index mirrors. The LLM Wiki generator also has a working
no-diff check. Those controls are inputs, not reasons to duplicate their
authority. Missing controls are historical/Resolved observation-byte guards,
Current overlay-only mutation, data source/freshness evidence, an explicit
generator/input/output/check relation, and normalized duplicate-owner checks.

RIA-002 design preflight originally stopped before RED because the proposed
contract would have compared every Current member to evidence baseline
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`, but activation commit `cb0c1f6`
changed the Current research migration ledger's inventory boundary from 444 to
446 outside every declared projection. The reviewed RIA-001 head
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe` is therefore the initial Current
audit and research baseline; `8fb9821` remains exclusively Historical snapshot
authority. Design commits `08cf17d` and `f0c019a` corrected that model, and
implementation commits `13835e9`, `e29c6fb`, `27a63b3`, and `c278173`
completed the schema-v2/index/FSM/lineage guard with 37/37 focused tests,
repository gates, and approved requirements and quality reviews. RIA-003
through RIA-006 then completed in dependency order with the exact evidence in
the Work Breakdown and reciprocal Task.

### Global Constraints

- Preserve `docs/99.templates/support/document-profiles.json#referenceCurrentPacks`
  as the only Current-pack pointer and member authority.
- Require schema version 2. Keep `snapshotGuard.sourceCommit` exclusive to the
  five Historical/Resolved audit packs and `research/2026-07-04-wer`; require
  `currentPackBaselines` keys to equal the live Current registry IDs exactly
  and initialize both values to `git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`.
- Forbid contract-supplied Current paths, member lists, per-member digests,
  lifecycle states, and pointers. Before deriving paths or digests, require
  baseline/proposed equality for registry `profileId`, pack IDs, members, and
  `allowedStates`, plus tracked regular-file availability for every derived
  pack README and member.
- Permit at most one open `baselineTransitions` record and require terminal
  `--require-settled-baselines` validation to reject it. A transition and its
  durable `baselineSettlements` proof never become registry, baseline, member,
  or general digest authority.
- Define immutable code-owned Current root
  `git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`. Audit remains permanently
  at root with no transition/settlement. Research permits only root, the exact
  one-shot open transition from root, or one settled C2 proof; reject every
  other pin, record cardinality, forged root, or reused ID.
- Treat the exact constant registry path and every derived Current path as
  proposed tracked authority only after a fixed bounded stage-zero index read
  and byte-equal no-follow worktree read. Reject deletes/untracked replacements,
  unmerged entries, symlink/submodule modes, and index/worktree drift.
- Keep CLI evidence modes distinct: normal mode proves verified proposed bytes
  and state only; `--staged` proves proposed C3 against the fixed internal
  current-HEAD resolution of C2; `--commit git-sha1:<C3>` proves the immutable
  post-C3 single-parent chain. Contract/caller revision expressions remain
  forbidden.
- Do not rewrite dated Historical, Resolved, or Current observation facts to
  make later implementation appear complete.
- Permit Current closure changes only in the declared remediation overlay and
  required navigation/index evidence.
- Keep Stage 90 descriptive; active governance stays in Stage 00, delivery
  contracts stay in Stages 01-04, and procedures stay in Stage 05.
- Do not read, traverse, hash, copy, or report ignored `_workspace` children,
  credentials, tokens, kubeconfigs, auth files, shell history, or secret values.
- Use repository-static evidence only. Provider, GitHub-hosted, Kubernetes,
  Vault, ESO, Argo CD, and other live results remain `DEFER` unless separately
  authorized and directly observed.
- Begin every behavior-changing package with a focused failing test, observe
  the expected RED, implement the minimum GREEN, review, and commit logically.
- Before every logical commit—including activation, RIA-001 through RIA-007,
  closure, and postflight evidence—run the package's focused/affected checks,
  `env TMPDIR=/tmp pre-commit run --all-files`, inspect `git status --short`
  and `git diff` for formatter changes, stage only intended output, rerun every
  affected hook, and require both `git diff --check` and
  `git diff --cached --check` to pass. Record observed PASS/SKIP/FAIL/DEFER
  exactly; never pre-claim a result.
- Use `apply_patch` for tracked edits and preserve unrelated user changes.
- Remote push, merge, publication, live mutation, dependency installation, and
  credential changes require separate explicit human approval.

### File Responsibility Map

| Path | Responsibility |
| --- | --- |
| `docs/90.references/data/reference-information-architecture.schema.json` | Closed schema-v2 contract for separate Historical guards, exact Current baseline map, one-shot transitions, durable settlements, section/cell projection rules, source/freshness records, generator relations, and pair-scoped duplicate exceptions. |
| `docs/90.references/data/reference-information-architecture.json` | Repo-local Spec 038 contract instance; pins exact Current pack IDs by map key and commits by value without repeating members, paths, digests, states, or pointers. |
| `scripts/reference_information_architecture.py` | Pure parsing, normalization, stage-zero index/worktree authority, root-FSM, digest, Git-object, and finding functions shared by CLI and tests. |
| `scripts/validate-reference-information-architecture.py` | Thin CLI with normal mode, `--staged`, anchored `--commit git-sha1:<oid>`, `--require-settled-baselines`, `--root`, `--contract`, and `--self-test`; prints stable rule IDs and returns 0/1/2. |
| `tests/test_reference_information_architecture.py` | Focused positive, hostile, and regression tests for all six Spec criteria and input boundaries. |
| `tests/fixtures/reference-information-architecture/` | Minimal fixture contract/corpus trees for deterministic negative cases; no copied production corpus. |
| `scripts/validate-repo-quality-gates.sh` | Aggregate invocation of self-test and production validation. |
| `docs/90.references/{README.md,audits/README.md,data/README.md,llm-wiki/README.md,research/README.md}` | Category routing, contract discovery, and exact authority/freshness wording only when a focused finding requires it. |
| `scripts/README.md`, `tests/README.md` | Command contract and focused-test inventory. |
| Spec/Plan/Task/index/ledger files | Activation and terminal lifecycle evidence; never implementation authority. |

## Goals & In-Scope

- Protect every Historical and Resolved audit observation body and every
  Historical research observation body against drift using pinned committed
  source objects and derived exact SHA-256 evidence.
- Protect Current audit/research members derived at runtime from
  `referenceCurrentPacks`; permit only the remediation overlay and exact
  declared section/cell navigation projections while preserving fact-bearing
  README prose, snapshot SHA, scores, scope, and observation fields.
- Advance the Current research baseline for RIA-007 ledger evidence only through
  one exact open transition commit followed by a contract-only durable
  settlement; keep every non-target Current member and the registry equal to
  the prior baseline.
- Require repo-backed data assets to name evidence, an observed/check date,
  non-empty adopted and rejected scope, and a non-empty refresh trigger without
  expanding universal frontmatter.
- Declare exactly one generator, its input roots, output, and check command for
  each generated Stage 90 artifact, and require zero generated drift.
- Detect duplicate Current claims, generated/manual output collisions, and
  copied active-policy/runbook paragraphs in Stage 90 with deterministic
  thresholds and closed source/destination/role-scoped structural exceptions.
- Integrate focused checks into repository-static QA, document their command
  contracts, and close Spec/Plan/Task atomically after independent review.

## Non-Goals & Out-of-Scope

- Changing the Current audit or research pack selection, member list, or
  lifecycle vocabulary merely to simplify this validator.
- Consolidating dated snapshots solely because topics overlap, or deleting
  historical evidence that remains a valid observation record.
- Promoting reference analysis into policy, runbook, release, incident, or
  runtime authority.
- Adding vector storage, embeddings, retrieval services, static wiki sites, or
  a second generated navigation owner.
- Modifying GitHub Actions, the GitOps FIFO self-test, provider adapters,
  Kubernetes manifests, infrastructure, secrets, or live environments.
- Activating Specs 039-046 or changing PRD-003 provider-program lineage.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| RIA-000 | Atomic reciprocal planning activation | None | Completed: Plan-only lifecycle RED and reviewed prerequisite head `fdc86ee` | Activation commit `cb0c1f6`, exact seven-file scope, lifecycle/QA/review evidence |
| RIA-001 | Closed reference contract, safe loader, and diagnostic interface | RIA-000 | Completed from activation commit `cb0c1f6` | Reviewed commits `68e46fc`, `566c74f`, `15bba3d`; focused/schema/CLI PASS and clean final requirements/quality verdicts |
| RIA-002 | Audit/research immutability, Current baseline FSM, transition, settlement, and projection-bounded overlay guard | RIA-001 | Completed: design correction commits `08cf17d`, `f0c019a` | Implementation commits `13835e9`, `e29c6fb`, `27a63b3`, `c278173`; 37/37 focused and repository gates PASS; requirements compliant and quality approved |
| RIA-003 | Data source, adopted/rejected scope, and freshness validation | RIA-002 | Completed from reviewed RIA-002 implementation | Commits `7083909`, `77e081d`; nine-asset ledger and exact inventory; 43/43 focused and repository gates PASS; requirements compliant and quality approved |
| RIA-004 | Generated ownership and zero-drift validation | RIA-003 | Completed from reviewed RIA-003 implementation | Commits `5d15c1c`, `0cb1789`; fixed-argv generator relation and zero drift; 46/46 focused and repository gates PASS; requirements compliant and quality approved |
| RIA-005 | Duplicate Current/generated/manual/policy-owner validation | RIA-004 | Completed from reviewed RIA-004 implementation | Commits `671e722`, `000cf858`; owner/collision/exception/policy-copy proof; 81/81 focused and repository gates PASS; requirements, parser, and quality review approved |
| RIA-006 | Aggregate integration and command inventories | RIA-005 | Completed from reviewed RIA-005 implementation | Commit `76c1d4b`; self-test-before-production integration; 82/82 focused and aggregate gates PASS; requirements compliant and quality approved |
| RIA-007 | Independent whole-tranche review, atomic lifecycle closure, postflight transition, and settlement | RIA-006 | C1 exact-seven commit `8c0dcea558212e11ac93a0fe626cddb31315859b` and clean-tree postflight observed | Final C1 reviews approved and activation-to-C1 explicit-ref lifecycle plus repository-static postflight passed; C2 is an exact-nine staged open-transition and exact-value `.secrets.baseline` adjudication proposal with no C2 identity/postcommit, C3, settlement, terminal explicit-ref, or remote/live claim |

### Task 0: RIA-000 — Atomic reciprocal planning activation

**Files:**

- Modify: `docs/03.specs/038-reference-information-architecture/spec.md`
- Modify: `docs/03.specs/README.md`
- Create: `docs/04.execution/plans/2026-07-22-reference-information-architecture.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-22-reference-information-architecture.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: evidence baseline
  `8fb9821497aaa93d9ed5fc1a69b60c628b047b47`, reviewed prerequisite head
  `fdc86ee9156a35f48d57916be4ecb3505e483a50`, active Spec 038, the PRD-006
  program relation, and exact Plan/Task body contracts.
- Produces: one reviewed active reciprocal pair, rollback parent `fdc86ee`,
  exact seven-path activation commit, and no implementation result.

- [x] **Step 1: Observe the Plan-only lifecycle RED.** Stage only the new Plan
  and run `python3 scripts/validate-document-lifecycle.py --root . --mode staged`.
  Observed exit `1`, rule `LIFECYCLE-CREATE`, and `Plan count 1, Task count 0`.

- [x] **Step 2: Build the exact seven-file reciprocal proposal.** Add the Task,
  direct Spec identity, Spec/Plan/Task index rows, 446-path migration inventory,
  two new 14-column ledger rows, and the updated Spec row. At activation, keep
  RIA-001 through RIA-007 Queued and the existing registry relation unchanged.

- [x] **Step 3: Run focused activation GREEN.** Run staged lifecycle, registry
  self-test, strict registry, strict Markdown profiles, strict cross-document
  validation, changed-file Markdownlint, and cached diff check. Require the
  observed results `PASS`, registry self-test 119, strict inventory 446,
  Markdown violations 0, and cross-document valid.

- [x] **Step 4: Run the activation commit gate.** Run pre-commit with the exact
  seven paths, then `env TMPDIR=/tmp pre-commit run --all-files`; inspect
  `git status --short` and both staged/unstaged diffs for formatter changes,
  stage only intentional output, rerun affected hooks, and require
  `git diff --check` plus `git diff --cached --check` to pass. Record any
  non-PASS result with its owning limitation; do not substitute a skipped hook.
  The first run exposed the pre-existing Spec 037
  `CLOSURE-CURRENT-RESIDUE` post-closure admission defect and a Git-SHA secret
  false positive. Reviewed prerequisite commits `5ed6de6` and `fdc86ee`
  preserved the frozen 100-row closure ledger while admitting only complete
  active Plan/Task controls; the contract example now uses `git-sha1:`. The
  staged pair then passed residue validation with `active_controls=2/1`, exact
  changed-file pre-commit, all-files pre-commit, formatter/status inspection,
  and both diff checks without skipped hooks or formatter changes.

- [x] **Step 5: Close both planning-review findings and obtain re-review.** The
  initial requirements verdict was `REQUIREMENTS CHANGES REQUIRED` for missing
  RIA-000 and per-commit all-files gates. The initial quality verdict was
  `QUALITY CHANGES REQUIRED` for duplicated member projection, incomplete
  research/README protection, broad digest exceptions, missing source scope,
  unsplit packages/schema validation, and stale ledger count. Apply this exact
  remediation and require fresh `REQUIREMENTS COMPLIANT` and
  `QUALITY APPROVED` verdicts with no blocking findings. The first re-review
  returned `REQUIREMENTS COMPLIANT` and `QUALITY CHANGES REQUIRED`; quality
  required the anchored `git-sha1:` schema/parser contract, immediate
  activation parent `fdc86ee`, and a closed fixed-argv Git object reader.
  Those corrections are now in the proposal. The final focused re-reviews
  returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no Critical,
  Important, or Minor findings.

- [x] **Step 6: Commit and verify the activation.** Commit exactly the seven
  files with `docs(execution): activate reference information architecture`,
  run explicit-ref lifecycle from `fdc86ee` to the new commit, rerun focused
  document gates, and require clean status before dispatching RIA-001.
  Activation commit `cb0c1f6` is observed with the exact seven-file scope.

### Task 1: RIA-001 — Closed contract and validator interface

**Files:**

- Create: `docs/90.references/data/reference-information-architecture.schema.json`
- Create: `docs/90.references/data/reference-information-architecture.json`
- Create: `scripts/reference_information_architecture.py`
- Create: `scripts/validate-reference-information-architecture.py`
- Create: `tests/test_reference_information_architecture.py`
- Create: `tests/fixtures/reference-information-architecture/minimal-valid.json`
- Modify: `docs/90.references/data/README.md`

**Interfaces:**

- Consumes: `referenceCurrentPacks.packs[].id` from
  `docs/99.templates/support/document-profiles.json`; repository root and an
  optional contract path from the CLI.
- Produces: `Finding(rule_id: str, path: str, message: str)`,
  `load_contract(root: Path, contract_path: Path) -> dict[str, object]`,
  `validate_reference_architecture(root: Path, contract: Mapping[str, object]) -> list[Finding]`,
  and CLI exits `0` clean, `1` findings, `2` configuration/input failure.

- [x] **Step 1: Write the closed-schema RED fixtures.** Add tests that reject
  duplicate JSON keys, unknown top-level keys, schema versions other than `1`,
  absolute/parent/dot/empty path segments, paths outside declared roots,
  duplicate pack IDs, output paths, and mutable paths, symlinks, non-regular
  files, and missing registry pack references. The minimal valid shape is:

  ```json
  {
    "$schema": "./reference-information-architecture.schema.json",
    "schemaVersion": 1,
    "evidenceCutoff": "2026-07-22",
    "currentPackRegistry": "docs/99.templates/support/document-profiles.json",
    "snapshotGuard": {
      "sourceCommit": "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47",
      "historicalPackIds": [],
      "currentPackIds": []
    },
    "mutableIndexProjections": [],
    "dataAssets": [],
    "generatedAssets": [],
    "duplicateRules": {
      "canonicalOwnerRoots": ["docs/00.agent-governance", "docs/05.operations/policies", "docs/05.operations/runbooks"],
      "minimumParagraphCharacters": 160,
      "structuralExceptions": []
    }
  }
  ```

  Define `snapshotGuard.sourceCommit` with the anchored schema pattern
  `^git-sha1:[0-9a-f]{40}$`. Add negative fixtures for a bare OID, an empty or
  repeated prefix, uppercase hex, non-hex text, SHA-256 length, trailing text,
  and whitespace. The encoded string is contract data; Git receives only the
  exact 40 lowercase hexadecimal characters after one validated prefix.

- [x] **Step 2: Run the focused RED.** Run
  `python3 -m unittest tests/test_reference_information_architecture.py -v`.
  Expect import or target-existence failures because the module, CLI, schema,
  and contract do not exist; record only the observed diagnostic in the Task.

- [x] **Step 3: Implement the minimum safe loader and closed schema.** Use a
  duplicate-key-rejecting `json.loads(..., object_pairs_hook=...)`, `Path.lstat`,
  an allowlisted repository-relative POSIX path parser, and no-follow regular
  file reads. Implement
  `parse_git_sha1(value: object) -> str`: require a full anchored match of
  `git-sha1:<40 lowercase hex>`, remove exactly one `git-sha1:` prefix, assert
  the result matches `^[0-9a-f]{40}$`, and otherwise emit `RIA-SNAPSHOT`
  without returning an argv value. Define stable diagnostic IDs
  `RIA-CONTRACT`, `RIA-BOUNDARY`, `RIA-SNAPSHOT`, `RIA-OVERLAY`, `RIA-SOURCE`,
  `RIA-GENERATOR`, and `RIA-DUPLICATE`; diagnostics contain paths and rule
  facts, never file bodies.

- [x] **Step 4: Implement CLI self-test and the production contract skeleton.**
  `--self-test` runs the fixture matrix without reading the production corpus;
  normal mode validates the contract instance. The v1 bootstrap references the
  two registry pack IDs but does not copy their member lists, report paths,
  per-member digests, or Current pointers. Current paths and comparison digests
  are derived at validation time and must equal the registry membership
  exactly. CLI self-test must exercise the accepted encoded commit and every
  malformed-prefix case through the same production parser. RIA-002 replaces
  this bootstrap Current shape with required schema version 2.

- [x] **Step 5: Run GREEN and contract checks.** Run:

  ```bash
  python3 -m unittest tests/test_reference_information_architecture.py -v
  python3 scripts/validate-reference-information-architecture.py --self-test
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 -c 'import json; from jsonschema import Draft202012Validator as V; s=json.load(open("docs/90.references/data/reference-information-architecture.schema.json")); i=json.load(open("docs/90.references/data/reference-information-architecture.json")); V.check_schema(s); V(s).validate(i)'
  ```

  Expect all focused tests and self-test to pass. Production may still report
  only the RIA-002/RIA-003 entries intentionally not populated; it must not
  traceback, traverse ignored paths, or claim those criteria PASS.

- [x] **Step 6: Run the RIA-001 commit gate, review, and commit.** Run pre-commit
  for the seven RIA-001 files, full all-files pre-commit, formatter-diff
  inspection, affected-hook rerun, and both diff checks exactly as required by
  Global Constraints. Obtain requirements compliance and code-quality approval,
  remediate findings, rerun the gate, then commit with
  `feat(references): add reference architecture contract`.

  RIA-001 completed through `68e46fc`, `566c74f`, and `15bba3d`. Final reviews
  returned exact verdicts `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`,
  findings none. Focused unit, CLI self-test/production, and canonical Draft
  2020-12 schema/instance validation passed. Raw historical hook output is not
  reconstructed here, and CI/remote/live PASS is not claimed.

### Task 2: RIA-002 — Immutable observation and overlay guard

**Files:**

- Modify: `docs/90.references/data/reference-information-architecture.schema.json`
- Modify: `docs/90.references/data/reference-information-architecture.json`
- Modify: `scripts/reference_information_architecture.py`
- Modify: `tests/test_reference_information_architecture.py`
- Modify: `tests/fixtures/reference-information-architecture/minimal-valid.json`
- Create: `tests/fixtures/reference-information-architecture/snapshot-mutation.json`
- Create: `tests/fixtures/reference-information-architecture/overlay-mutation.json`
- Modify: `docs/90.references/data/README.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`

**Interfaces:**

- Consumes: validated RIA-001 contract, schema version 2, live
  `referenceCurrentPacks`, and exact Git commit/blob reads.
- Produces: `validate_snapshot_guards(...)` and
  `validate_overlay_guards(...)`, and `validate_baseline_transitions(...)`;
  each returns ordered `Finding` values and compares tracked regular-file bytes
  or exact parsed table/link projections only to declared committed authority.
  Current members, README paths, states, and comparison digests are derived
  from an exactly equal baseline/proposed registry and may not be supplied by
  the contract.

- [x] **Step 1: Add schema-v2 and exact-baseline RED tests.** Require
  `schemaVersion: 2`; reject the v1 `snapshotGuard.currentPackIds` shape and any
  Current path, member list, digest map/list, state, or pointer duplication.
  Require `currentPackBaselines` keys to equal the live registry Current IDs
  exactly, with anchored commit values and no missing, extra, or stale key. For
  each distinct baseline, require exact proposed/baseline equality of registry
  `profileId`, ordered pack IDs, `members`, and `allowedStates`, then require the
  registry-derived pack README and every member to be an available tracked
  regular file before deriving paths or SHA-256 values. Prove the original
  `8fb9821` Current research baseline fails on the ledger's 444-to-446 protected
  change and that `15bba3d` passes. Add stable `RIA-TRANSITION` diagnostics and
  require value-free path/rule facts without contract or blob bodies.

  Encode the code-owned immutable root
  `git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe` and a closed schema/code FSM.
  Audit must remain at root with no transition or settlement. Research permits
  only: root with no records; open with root pin, exactly one
  `ria-007-postflight-ledger` transition from root, and no settlement; or
  settled with no open transition, map value equal to literal C2, and exactly
  one matching durable settlement. Reject every other map value/cardinality,
  arbitrary pin, forged root, audit transition, or reused transition ID.

- [x] **Step 2: Add immutable-body and projection RED tests.** Create fixture
  repositories where a Historical/Resolved audit report, Historical research
  report, Current member, or fact-bearing pack README differs by one protected
  byte; a protected file is missing; the source ref is not a commit; or a
  runtime-derived SHA-256 differs. Expect deterministic `RIA-SNAPSHOT` or
  `RIA-OVERLAY`. Keep `snapshotGuard.sourceCommit` exclusively for audit packs
  `audits/2026-05-24-whga`, `audits/2026-07-02-whia`,
  `audits/2026-07-03-wdgh`, `audits/2026-07-04-wdcn`,
  `audits/2026-07-05-wea`, and research pack `research/2026-07-04-wer`.
  Accept only the complete remediation-roadmap body; `Audit Pack Registry`
  `Pack role` and `Successor / resolution` cells; `Research Pack Index`
  `Status` cells; Current audit `Report Index` `Lifecycle` and
  `Actionable disposition` cells; Current research `Report Index` `Lifecycle`
  cells; and one exact `navigationReplacement` destination with unchanged
  visible text. Reject whole-file README mutability, globs, undeclared cells,
  and reusable exceptions.

- [x] **Step 3: Add transition and settlement RED tests.** Define an open
  transition as this exact closed record shape:

  ```json
  {
    "id": "ria-007-postflight-ledger",
    "packId": "research/2026-07-07-wer",
    "fromCommit": "git-sha1:<active-map-pin>",
    "subject": "document-migration-evidence-ledger",
    "targetSha256": "<64-lowercase-hex>",
    "targetByteLength": 1,
    "reason": "<non-empty bounded reason>"
  }
  ```

  The schema permits zero or one record, requires `fromCommit` to equal that
  pack's active map pin, derives the exact member path from registry membership
  and the constant subject, caps the target at `2_000_000` bytes, and gives the
  record no baseline, member, path, pointer, revision, or general digest-list
  authority. Reject Historical targets, `HEAD`/revision expressions,
  self-reference, an arbitrary subject/path, wrong digest/size/bytes, missing or
  non-member target, registry drift, any non-target Current change, multiple or
  stale transitions, and reuse of a settled transition ID. Require
  `--require-settled-baselines` to fail with `RIA-TRANSITION` while open.

  A durable settlement record repeats the exact transition `id`, `packId`,
  `fromCommit`, constant `subject`, target digest, target length, and reason,
  and adds literal anchored `transitionCommit`. Reject direct baseline changes,
  a cleared transition without proof, missing/mismatched proof, a settlement
  whose map value is not that literal transition commit, or a proof naming a
  commit whose exact contract did not contain the matching open transition.
  Through fixed Git reads, prove the named transition commit retained the prior
  baseline and equal registry, contained the exact target bytes, and left all
  non-targets unchanged. Settlement records remain append-only and durable.

- [x] **Step 4: Run the named RED selectors.** Run focused tests for schema-v2
  map equality, `8fb9821` failure versus `15bba3d` success, snapshot mutation,
  Current overlay bounds, the open-transition matrix, direct baseline jump, and
  settlement proof chain. Include the production fixed-runner hostile matrix:
  malformed/repeated commit prefixes before subprocess, missing executable,
  non-zero exit, timeout, output caps, malformed/multiple `ls-tree` records,
  path/mode/type/OID mismatch, oversized/non-canonical size, short/extra blob,
  inherited hostile Git environment, shell use, and argv outside the allowlist.
  Add proposed-authority cases for staged delete plus untracked replacement,
  unmerged stages, symlink and submodule modes, and index/worktree byte drift.
  Add staged-settlement and explicit-ref cases for internal-HEAD/C2 mismatch,
  proposed index drift outside the contract, detached/non-parent C3, zero-parent
  C3, and merge-parent C3. Expect failures because v2 index/FSM/lineage
  validation is absent. Record no implementation result from the earlier
  preflight blocker.

- [x] **Step 5: Implement the fixed Git runner and baseline comparison.** Pass
  every contract commit through `parse_git_sha1()` and give Git only the
  returned 40-hex OID. Set `GIT_EXECUTABLE = "/usr/bin/git"`, `shell=False`, a
  10-second timeout, and a newly constructed closed environment with
  `HOME=/nonexistent`, `PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
  `GIT_LITERAL_PATHSPECS=1`, `GIT_NO_LAZY_FETCH=1`,
  `GIT_NO_REPLACE_OBJECTS=1`, `GIT_OPTIONAL_LOCKS=0`, and
  `GIT_TERMINAL_PROMPT=0`; do not inherit arbitrary `GIT_*` variables. Permit
  only these literal argv shapes:

  ```text
  /usr/bin/git ls-files -z --stage -- <safe-path>
  /usr/bin/git cat-file -t <commit-oid>
  /usr/bin/git cat-file commit <commit-oid>
  /usr/bin/git ls-tree -z --full-tree <commit-oid> -- <safe-path>
  /usr/bin/git cat-file -t <blob-oid>
  /usr/bin/git cat-file -s <blob-oid>
  /usr/bin/git cat-file blob <blob-oid>
  /usr/bin/git rev-parse --verify HEAD
  /usr/bin/git diff-index --cached --name-status -z --no-renames <commit-oid> --
  ```

  The `rev-parse` argv is an internal staged-settlement constant only; `HEAD`
  never comes from contract/CLI data and never becomes a baseline or transition
  authority. All other commit arguments are parsed literal OIDs. Require
  `commit\n`; parse exactly one NUL-terminated regular-blob tree record
  whose returned path equals the requested safe path; validate the blob OID as
  40 lowercase hex; require `blob\n`; parse a canonical decimal size no larger
  than `2_000_000`; cap metadata stdout at 65,536 bytes and every stderr at
  16,384 bytes; read no blob until its size passes; cap blob stdout at the
  declared size; kill the process on timeout or cap overflow; and require
  returned blob length to equal the declared size. Treat missing executable,
  timeout, non-zero exit, output overflow, malformed/multiple tree records,
  mismatched path, non-blob/symlink mode, malformed OID, non-canonical or
  oversized size, and short/extra bytes as value-free findings; never accept a
  caller/contract revision expression, shell, inherited hostile Git variables,
  or lazy/network fetch.

  Read the exact constant registry path first with `ls-files`. Require exactly
  one stage-0 record, returned path equality, mode `100644` or `100755`, and no
  stage 1/2/3, symlink `120000`, submodule `160000`, missing, or duplicate
  record. Read its fixed blob, then require bounded `O_NOFOLLOW` regular
  worktree bytes to equal it. Apply the same boundary to every registry-derived
  exact safe path. Compare registries first, derive Current paths/digests second,
  then compare proposed index authority; never infer authority from an
  untracked or worktree-only file. Mask only declared cells or one destination.

- [x] **Step 6: Implement one-shot transition and durable settlement checks.**
  Validate exact candidate bytes while the active map remains at its old pin.
  Keep the registry and every non-target Current member old-baseline exact.
  Normal validation may accept the one open transition; terminal
  `--require-settled-baselines` may not. For settlement, require the current
  contract to change no protected content, set only the affected map value to
  literal `transitionCommit`, remove the open record, and append its matching
  proof. Read that commit's contract, registry, target, and non-target blobs
  through the fixed runner. No hidden or detached candidate commit is allowed.

  Keep evidence modes mutually exclusive. Normal mode has no mode flag and
  validates verified index/worktree bytes and FSM state without claiming commit
  lineage. `--staged` is the only C3 preflight: resolve current branch HEAD with
  the one fixed internal argv, require its OID equals settlement
  `transitionCommit` C2, and require bounded `diff-index` output to contain only
  one modified exact contract path relative to C2. `--commit git-sha1:<C3>` is
  the only post-C3 explicit-ref mode: parse the literal C3 commit object, require
  exactly one parent equal to C2, and validate the C3 contract/tree/blob. Reject
  detached/non-parent, zero-parent, and merge-parent C3. Only this explicit mode
  supplies durable terminal post-commit lineage evidence.

- [x] **Step 7: Populate production guards without member duplication.** Keep
  Historical source commit
  `git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47` only for the five named
  audit packs and `research/2026-07-04-wer`. Set the exact two-key Current map
  to `git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`, leave production
  `baselineTransitions` and `baselineSettlements` empty, and declare only the
  Step 2 projections. Derive all Current READMEs, members, paths, states, and
  digests; declare no mutable README path. Production therefore begins in the
  exact FSM root state, with audit permanently rooted.

- [x] **Step 8: Run focused and production GREEN.** Run the full unit module,
  CLI self-test, normal production CLI, production CLI with
  `--require-settled-baselines`, Draft 2020-12 schema/instance validation,
  strict document registry, strict Markdown, and strict cross-links. Expect
  zero snapshot/overlay/transition findings, exact production map equality,
  empty production transitions/settlements, root-state equality, and no
  protected observation changes. Staged and explicit-ref modes are exercised
  in isolated fixtures; they are not inferred from normal-mode PASS.

- [x] **Step 9: Run the RIA-002 commit gate, review, and commit.** Run pre-commit
  for the RIA-002 files, full all-files pre-commit, formatter-diff inspection,
  affected-hook rerun, and both diff checks. After fresh requirements and
  quality approval and any required rerun, commit with
  `feat(references): protect reference observations and overlays`.

### Task 3: RIA-003 — Data source, scope, and freshness validation

**Files:**

- Modify: `docs/90.references/data/reference-information-architecture.json`
- Modify: `scripts/reference_information_architecture.py`
- Modify: `tests/test_reference_information_architecture.py`
- Create: `tests/fixtures/reference-information-architecture/source-freshness.json`
- Modify: `docs/90.references/data/README.md`
- Modify: `docs/99.templates/templates/common/reference.template.md` only if a
  production finding proves its existing source/scope/freshness prompts incomplete.

**Interfaces:**

- Consumes: RIA-002 safe reads, ordered findings, and contract
  `evidenceCutoff: YYYY-MM-DD`.
- Produces: `validate_data_assets(root, contract) -> list[Finding]`; every asset
  has tracked `repositoryEvidence`, non-empty `refreshTrigger`, and one or more
  closed source records with `url`, `checkedOn`, `adoptedScope`, and
  `rejectedScope`.

- [x] **Step 1: Write exact source-ledger RED tests.** Add
  `test_data_asset_requires_source_scope_date_and_trigger`,
  `test_data_asset_rejects_after_cutoff_and_untracked_evidence`, and
  `test_data_asset_accepts_closed_source_ledger`. Reject missing/non-HTTPS URL,
  invalid date, date after `evidenceCutoff`, empty adopted or rejected scope,
  empty trigger, missing asset, missing tracked repo evidence, unknown fields,
  and duplicate source records.

- [x] **Step 2: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_requires_source_scope_date_and_trigger tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_rejects_after_cutoff_and_untracked_evidence tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_accepts_closed_source_ledger -v`.
  Expect failures because `validate_data_assets` is absent.

- [x] **Step 3: Implement the minimal closed source ledger.** Parse dates
  strictly, compare them only to the contract cutoff for deterministic results,
  require non-empty adopted/rejected arrays, validate HTTPS URLs without network
  access, and validate repo evidence through the RIA-001 tracked no-follow read
  boundary. Do not invent a universal expiry date.

- [x] **Step 4: Populate every current data asset.** Add all current
  `docs/90.references/data/` assets, including the RIA schema/contract, with
  exact tracked evidence, checked official-source URL, adopted scope, rejected
  scope, and refresh trigger. Preserve data authority boundaries and do not
  convert repo-backed evidence into live PASS.

- [x] **Step 5: Run focused and production GREEN.** Run the full unit module,
  CLI self-test, production CLI, Draft 2020-12 schema/instance validation, and
  strict Markdown/link checks. Expect zero `RIA-SOURCE` findings.

- [x] **Step 6: Run the RIA-003 commit gate, review, and commit.** Run pre-commit
  for exact RIA-003 files, full all-files pre-commit, formatter-diff inspection,
  affected-hook rerun, and both diff checks. Obtain fresh requirements and
  quality approval, rerun after fixes, then commit with
  `feat(references): enforce source scope and freshness`.

### Task 4: RIA-004 — Generated ownership and zero-drift validation

**Files:**

- Modify: `docs/90.references/data/reference-information-architecture.json`
- Modify: `scripts/reference_information_architecture.py`
- Modify: `tests/test_reference_information_architecture.py`
- Create: `tests/fixtures/reference-information-architecture/generator-collision.json`
- Modify: `docs/90.references/llm-wiki/README.md`

**Interfaces:**

- Consumes: RIA-003 safe reads and ordered finding interface.
- Produces: `validate_generated_assets(root, contract) -> list[Finding]`; the
  only executable mapping is the exact contract string
  `bash scripts/generate-llm-wiki-index.sh --check` to a fixed argv tuple.

- [x] **Step 1: Write exact generator RED tests.** Add
  `test_generator_requires_unique_owner_relation`,
  `test_generator_rejects_unmapped_command_and_stale_output`, and
  `test_generator_accepts_llm_wiki_relation`. Reject duplicate output owners,
  generator/output identity, missing tracked generator/input/output, directory
  or symlink output, unknown command, stale generated bytes, and stale
  canonical-owner links.

- [x] **Step 2: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_requires_unique_owner_relation tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_rejects_unmapped_command_and_stale_output tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_accepts_llm_wiki_relation -v`.
  Expect failures because `validate_generated_assets` is absent.

- [x] **Step 3: Implement fixed-argv validation.** Validate relation shape and
  tracked paths, map the one exact check string to a literal argv tuple, execute
  it without a shell in a sanitized environment, and return path-only
  `RIA-GENERATOR` diagnostics. Contract data may not introduce another command.

- [x] **Step 4: Populate one production relation.** Register
  `scripts/generate-llm-wiki-index.sh`, its declared input roots,
  `docs/90.references/llm-wiki/wiki-index.md`, and the exact check command.
  Run `bash scripts/generate-llm-wiki-index.sh --check` and require zero drift.

- [x] **Step 5: Run focused and production GREEN.** Run the full unit module,
  CLI self-test/production, direct generator no-diff, and strict links. Expect
  zero `RIA-GENERATOR` findings.

- [x] **Step 6: Run the RIA-004 commit gate, review, and commit.** Run pre-commit
  for exact RIA-004 files, full all-files pre-commit, formatter-diff inspection,
  affected-hook rerun, and both diff checks. Obtain fresh requirements and
  quality approval, rerun after fixes, then commit with
  `feat(references): enforce generated ownership`.

### Task 5: RIA-005 — Duplicate Current, generated, and policy ownership

**Files:**

- Modify: `docs/90.references/data/reference-information-architecture.json`
- Modify: `scripts/reference_information_architecture.py`
- Modify: `tests/test_reference_information_architecture.py`
- Create: `tests/fixtures/reference-information-architecture/current-owner.json`
- Create: `tests/fixtures/reference-information-architecture/policy-copy.json`
- Modify: `docs/90.references/README.md`
- Modify: `docs/90.references/audits/README.md` only when a production finding
  proves an exact bounded owner/copy remediation.
- Modify: `docs/90.references/data/README.md` only under the same finding gate.
- Modify: `docs/90.references/llm-wiki/README.md` only under the same finding gate.
- Modify: `docs/90.references/research/README.md` only under the same finding gate.

**Interfaces:**

- Consumes: RIA-004 safe reads, registry Current packs, and generated relations.
- Produces: `validate_duplicate_rules(root, contract) -> list[Finding]`;
  paragraph normalization removes Markdown destinations/formatting while
  preserving visible text. Each exception is a closed record containing exact
  `canonicalOwnerPath`, `referencePath`, `paragraphSha256`, `structuralRole`,
  and non-empty `reason`.

- [x] **Step 1: Write exact duplicate-owner RED tests.** Add
  `test_duplicate_current_and_generated_manual_owners_fail`,
  `test_policy_paragraph_copy_fails`, and
  `test_structural_exception_is_pair_scoped`. Reject a second Current claim,
  generated/manual collision, and any normalized paragraph of at least 160
  visible characters copied from Stage 00 policy, Stage 05 Policy, or Stage 05
  Runbook into Stage 90.

- [x] **Step 2: Prove exception non-reuse in RED.** Accept an exception only
  when the digest occurs in the exact canonical/reference path pair and matches
  its declared structural role; reject use at any other source, destination,
  digest, or role, stale records, unknown roles, and blanket digest lists.

- [x] **Step 3: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_duplicate_current_and_generated_manual_owners_fail tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_policy_paragraph_copy_fails tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_structural_exception_is_pair_scoped -v`.
  Expect failures because `validate_duplicate_rules` is absent.

- [x] **Step 4: Implement minimal normalized comparison.** Derive Current claims
  from registry/index mirrors, compare generated outputs to manual owners, hash
  normalized visible paragraphs, and validate closed pair-scoped structural
  exceptions. Headings, pure link lists, table headers, and generated notices
  are ignored by parser classification, not by a global digest allowlist.

- [x] **Step 5: Run production scan and remediate only proven gaps.** Replace a
  prohibited current policy/procedure copy with concise analysis and a
  canonical link while preserving dated facts, sources, and interpretation.
  Add a structural exception only when its exact two-path role is verified.

- [x] **Step 6: Run focused and production GREEN.** Run the full unit module,
  CLI self-test/production, generator no-diff, and strict links. Expect zero
  duplicate Current, generated/manual, or active-policy copy findings.

- [x] **Step 7: Run the RIA-005 commit gate, review, and commit.** Run pre-commit
  for exact RIA-005 files, full all-files pre-commit, formatter-diff inspection,
  affected-hook rerun, and both diff checks. Obtain fresh requirements and
  quality approval, rerun after fixes, then commit with
  `feat(references): reject duplicate reference owners`.

### Task 6: RIA-006 — Aggregate integration and command inventories

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `tests/test_reference_information_architecture.py`

**Interfaces:**

- Consumes: RIA-001 through RIA-005 reviewed commits and focused commands.
- Produces: aggregate self-test-before-production invocation and durable command
  inventories; it does not change CI topology or lifecycle state.

- [x] **Step 1: Add the exact aggregate-integration RED.** Add
  `ReferenceInformationArchitectureTests.test_aggregate_runs_self_test_before_production`
  to `tests/test_reference_information_architecture.py`. It reads the aggregate
  script and asserts one self-test invocation precedes one production `--root`
  invocation.

- [x] **Step 2: Run the named RED selector.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_aggregate_runs_self_test_before_production -v`.
  Expect failure because the aggregate has neither invocation.

- [x] **Step 3: Add minimal aggregate wiring and inventories.** Invoke focused
  self-test then production validation without changing CI topology or the
  generator owner. Document CLI arguments, exits, rule IDs, safe boundaries,
  the focused test selector, and production command in the two inventories.

- [x] **Step 4: Run focused and repository GREEN.** Run the named selector,
  full focused module, CLI self-test/production, generator no-diff, registry
  self-test/strict, strict Markdown/links, and
  `bash scripts/validate-repo-quality-gates.sh .`. Expect PASS and no lifecycle,
  CI, provider, remote, or live claim.

- [x] **Step 5: Run the RIA-006 commit gate, review, and commit.** Run pre-commit
  for the exact four files, full all-files pre-commit, formatter-diff
  inspection, affected-hook rerun, and both diff checks. Obtain fresh
  requirements and quality approval, rerun after fixes, then commit with
  `chore(qa): integrate reference architecture validation`.

### Task 7: RIA-007 — Independent review and atomic lifecycle closure

**Files:**

- C1 lifecycle closure modifies exactly: Spec 038 and its index, this Plan and
  its index, the reciprocal Task and its index, and the document-profile
  registry's Spec 038 program-lineage state. The ledger and reference contract
  are untouched.
- C2 postflight evidence modifies exactly the same six lifecycle paths plus
  `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`
  `docs/90.references/data/reference-information-architecture.json`, and
  `.secrets.baseline`.
- C3 settlement modifies exactly
  `docs/90.references/data/reference-information-architecture.json`.

**Interfaces:**

- Consumes: reviewed activation and RIA-001 through RIA-006 commits.
- Produces: exact Task results, atomic `active -> done` Spec/Plan/Task and
  registry-state proposal, seven-file closure commit C1, explicit-ref
  postflight, nine-file evidence/open-transition/exact scanner-adjudication
  commit C2, and
  contract-only settlement commit C3. No commit claims its own content-addressed
  identity.

- [x] **Step 1: Prepare terminal evidence without pre-claiming commits.** Mark
  each RIA row Done only with exact observed test/review/commit evidence; update
  Spec/Plan/Task, all three indexes, and the registry's Spec 038 program-lineage
  state in one staged lifecycle proposal. Do not change the migration ledger or
  contract in C1. Keep C1, C2, and C3 identities explicitly unidentified until
  each preceding commit is observed.

- [x] **Step 2: Run terminal repository QA.** Run focused tests, production
  reference validation, generator no-diff, registry self-test/strict, staged
  lifecycle, strict Markdown/links, aggregate QA, exact seven-file pre-commit,
  `env TMPDIR=/tmp pre-commit run --all-files`, formatter-diff inspection,
  affected-hook reruns, and both diff checks. Require observed PASS; a skipped
  strict hook cannot substitute for closure evidence.

- [x] **Step 3: Obtain independent whole-tranche reviews.** Generate a review
  package from activation parent `fdc86ee` through proposed HEAD. Require exact
  verdicts `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; remediate all
  blocking findings, rerun affected/full gates, and repeat both reviews. Final
  C1 verdicts were exactly `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`.

- [x] **Step 4: Run the closure commit gate and commit.** Re-run the exact
  changed-file and all-files gates after the final review, inspect formatter
  diffs, rerun affected hooks, require both diff checks, then commit the exact
  seven C1 paths with
  `docs(sdlc): close reference information architecture tranche`.
  The ledger remained byte-identical in C1. The exact-seven commit is
  `8c0dcea558212e11ac93a0fe626cddb31315859b`.

- [x] **Step 5: Verify clean-tree postflight.** Run explicit-ref lifecycle from
  the activation commit to C1, focused/production/generator,
  strict document, aggregate, all-files pre-commit, `git diff --check`, and
  clean status. Record only directly observed outcomes. The successful
  postflight used activation commit
  `cb0c1f6131ad6a8cf3f2f2ca18a369b5cd31d77b` through literal C1 and passed
  explicit-ref lifecycle, RIA 85/85, self-test, normal production,
  settled-baseline root validation, generator no-diff, registry
  self-test/strict, strict Markdown/cross-document, terminal residue, role
  audit, aggregate, all-files pre-commit, both diff checks, and clean status.
  An earlier invocation from `fdc86ee9156a35f48d57916be4ecb3505e483a50`
  failed closed because the reciprocal pair was absent at that ref; it was an
  operator ref-selection check, not repository-defect or PASS evidence.

- [x] **Step 6: Prepare the exact C2 postflight transition.** Add the observed
  C1 identity and postflight results to the six lifecycle docs/indexes, update
  the migration ledger and its inventory/freshness evidence, and add exactly one
  `ria-007-postflight-ledger` transition to the contract. The transition keeps
  the research baseline at its active pin, names the registry-derived ledger
  subject, and commits the exact proposed ledger SHA-256 and byte length. All
  other Current members and registry bytes remain old-baseline exact. Add the
  final target digest's exact path/value detect-secrets false-positive result
  to `.secrets.baseline` without changing scanner filters or behavior. C2
  changes exactly nine files; it contains no C2 SHA and makes no self-claim.
  This staged proposal likewise has no C2 postcommit result, C3 identity,
  settlement, terminal explicit-ref result, or
  CI-hosted/provider/remote/live claim.

- [ ] **Step 7: Gate and commit C2.** Run focused transition tests, normal
  production validation, and prove terminal `--require-settled-baselines`
  intentionally fails only for the open transition. Run staged lifecycle,
  strict documents, aggregate, exact nine-file pre-commit, all-files
  pre-commit, formatter/status inspection, affected-hook reruns, and both diff
  checks. Obtain task-scoped requirements/quality approval, then commit with
  `docs(sdlc): record reference architecture postflight`. Re-run normal
  production validation and require clean status; do not claim remote/live PASS.

- [ ] **Step 8: Prepare and commit C3 baseline settlement.** Modify only the
  contract: set the research `currentPackBaselines` value to literal C2, remove
  the open transition, and append its durable settlement proof with literal
  `transitionCommit` C2. Change no registry, ledger, lifecycle, README,
  `.secrets.baseline`, or other protected content. The validator must read C2's contract and blobs through the
  fixed runner and prove the matching transition, prior baseline/registry
  equality, exact target bytes, and unchanged non-targets. Run `--staged` with
  `--require-settled-baselines`: its fixed internal HEAD resolution must equal
  literal C2, and the proposed stage-zero index must differ from C2 only by the
  contract. Run focused direct-jump/settlement/reuse, HEAD/C2 mismatch,
  out-of-contract index drift, and index/worktree authority tests, plus exact
  contract-only pre-commit, all-files pre-commit, formatter/status inspection,
  affected-hook reruns, and both diff checks. Normal mode may additionally
  prove current bytes/FSM but cannot substitute for staged parent evidence.
  Then commit the reviewed settlement and require clean status.

- [ ] **Step 9: Verify terminal settlement postflight.** Run explicit-ref
  lifecycle and reference validation with exact
  `--commit git-sha1:<literal-C3> --require-settled-baselines`, then all
  focused/production/generator/strict/aggregate/all-files gates. Explicit-ref
  mode must parse the C3 commit object/tree/contract, require exactly one parent
  equal literal C2, and reject detached/non-parent/zero-parent/merge-parent
  fixtures. Require empty open transitions, one durable settlement, terminal
  explicit-ref PASS, and clean status. A normal clean-tree PASS remains current
  byte/state evidence only. Rollback is C3, then C2, then C1; never roll C2 back
  while retaining C3's baseline proof.

## Verification Plan

| Spec criterion | Deterministic evidence | Required result |
| --- | --- | --- |
| VAL-RIA-001 | Schema-v2 exact map/root-FSM, stage-zero registry equality, Current-pack registry/link, and pack-reference fixtures | Audit is permanent root; research is exactly root/open/settled; map keys equal registry IDs; no duplicated pack authority |
| VAL-RIA-002 | Historical source plus fixed index/worktree and per-Current-pack Git/blob/digest fixtures | Historical/Resolved bodies equal `8fb9821`; proposed registry/member authority is one stage-zero regular blob equal to no-follow worktree bytes; `8fb9821` fails and `15bba3d` passes the ledger case |
| VAL-RIA-003 | Current projection, root/open/settled FSM, staged C3, explicit-ref parent, direct-jump, and hostile index/commit fixtures | Only declared projections or exact one-shot ledger bytes change; staged C3 differs from C2 only at contract; literal C3 has exactly parent C2 and terminal explicit-ref passes |
| VAL-RIA-004 | Data asset URL/date/adopted/rejected-scope/trigger fixtures and production contract | Every governed data asset has repo evidence, checked source, adopted and rejected scope, and refresh trigger |
| VAL-RIA-005 | Generator ownership fixtures and `generate-llm-wiki-index.sh --check` | One generator relation and zero output drift |
| VAL-RIA-006 | Current-claim, generated/manual, and normalized policy-copy fixtures | Zero duplicate owners or copied active policy/procedure paragraphs |
| Repository closure | Strict registry/Markdown/links/lifecycle, aggregate, all-files pre-commit, diff, independent review, and `--require-settled-baselines` | C1/C2/C3 chain is durable, production transitions are empty at terminal state, all repository-static lanes PASS, and live/remote lanes remain accurately bounded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| New contract duplicates Current-pack authority | Two sources disagree about members, states, paths, digests, or pointers | Require exact map-key/registry equality, pin commits only, derive Current members/digests after baseline/proposed registry equality, and forbid duplicated fields |
| Worktree bytes become their own baseline | Existing drift is blessed silently | Pin a committed source, verify object type and declared digest, and read exact Git objects |
| Baseline advances without durable evidence | Protected Current bytes can be silently blessed | Allow one exact member transition, require C2 candidate bytes plus unchanged non-targets, and settle only through a C3 proof that reads literal C2 |
| Overlay rule permits broad mutation | Observation facts can be rewritten as closure evidence | Permit the exact remediation body and table-cell/link-destination projections only; reject whole README paths, globs, undeclared sections, and fact-cell changes |
| Paragraph-copy scan produces noise | Valid analysis is blocked or broad allowlists appear | Normalize visible paragraphs, use a 160-character minimum, classify structural/link-only text, and bind every exception to one canonical/reference path pair, digest, role, and reason |
| Generator check becomes arbitrary execution | Contract data can run commands | Map one exact check string to a fixed argv; never invoke through a shell |
| Stage 90 remediation changes historical meaning | Audit/research evidence loses integrity | Preserve observation bodies and only replace proven current policy copies with canonical links |
| Spec 039 portability debt contaminates closure | SKIP/DEFER is mislabeled PASS | Use `TMPDIR=/tmp` for the approved local all-files lane and retain explicit ownership/limitation text |

Rollback is newest-first by reviewed logical commit. Before RIA-007 terminal
closure, revert only the failing package and its exact contract/index changes.
After closure, revert C3, then C2, then C1, then RIA-006 through RIA-001, and
the seven-file activation commit last. Preserve
reviewed prerequisite commits `5ed6de6` and `fdc86ee` unless their own active
control contract is separately shown to regress. Never remove a guard before
restoring the observation, generator, or owner relation it protects.

## Completion Criteria

- RIA-000 through RIA-007 have observed RED/GREEN or document-lifecycle
  evidence, complete per-commit all-files/formatter/diff gates, fresh
  requirements and quality approval, and one logical commit per independently
  reviewable package.
- All six Spec 038 criteria pass in focused production validation, with stable
  diagnostics and hostile fixtures covering negative boundaries.
- Current audit/research identity remains owned only by the existing registry;
  the exact baseline-map keys mirror it and no parallel member, state, path,
  digest, or pointer source exists.
- Historical/Resolved audit, Historical research, and protected Current
  observation bytes match pinned committed baselines; only declared
  overlay/navigation projections or the one-shot RIA-007 ledger transition are
  mutable.
- Every governed data asset has repo evidence, source URL, checked date,
  adopted/rejected scope, and refresh trigger; the generated wiki has one owner
  and zero drift.
- Duplicate Current owners, generated/manual outputs, and copied active-policy
  paragraphs are zero or represented only by verified pair-scoped structural
  exceptions.
- Strict document, reference, aggregate, all-files pre-commit, diff, and
  independent whole-tranche reviews pass; the C1/C2/C3 chain is proven,
  terminal settled-baseline validation passes, and worktree status is clean.
- Spec 038, this Plan, its Task, indexes, registry relation, and migration
  ledger agree on terminal state without activating Spec 039 or PRD-003.

## Traceability

- **Spec**: [Reference Information Architecture](spec.md)
- **Task**: [Reference Information Architecture Task](tasks.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **AD**: [AD-0009](../../02.architecture/descriptions/ad-0009-document-lifecycle-evidence-operating-model.md)
- **Current audit**: [2026-07-11 WEIA](../../90.references/audits/2026-07-11-weia/README.md)
- **Current research**: `docs/90.references/research/2026-07-07-wer/README.md`; [current lookup](../../90.references/research/2026-08-08-wer/README.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-RIA-001](spec.md#success-criteria--verification-plan) | RIA-001, RIA-005, RIA-007 | [Contract and Current-pack evidence](tasks.md#task-table) |
| N/A — VAL-RIA-002 shares the Spec 038 source linked in VAL-RIA-001 | RIA-002, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-003 shares the Spec 038 source linked in VAL-RIA-001 | RIA-002, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-004 shares the Spec 038 source linked in VAL-RIA-001 | RIA-003, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-005 shares the Spec 038 source linked in VAL-RIA-001 | RIA-004, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-006 shares the Spec 038 source linked in VAL-RIA-001 | RIA-005, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
