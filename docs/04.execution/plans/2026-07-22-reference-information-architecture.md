---
title: 'Reference Information Architecture Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-22
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

**Architecture:** Keep `referenceCurrentPacks` in
`docs/99.templates/support/document-profiles.json` as the sole owner of Current
pack identity, membership, lifecycle, and pointer mirrors. Add a separate
closed-schema Stage 90 contract that references those pack IDs and owns only
immutable observation baselines, overlay mutability, data evidence/freshness,
generator relations, and duplicate-owner rules. A focused Python validator
loads tracked regular files without following symlinks, emits stable rule IDs,
and is integrated into the repository aggregate after hostile fixtures pass.

**Tech Stack:** Python 3 standard library, the repository's installed
`jsonschema` package with `Draft202012Validator`, `unittest`, Git object reads,
Bash generator checks, Markdown contract tables, pre-commit, and the repository
document lifecycle/registry validators.

This reciprocal Plan executes
[Spec 038](../../03.specs/038-reference-information-architecture/spec.md) on
reviewed prerequisite head `fdc86ee9156a35f48d57916be4ecb3505e483a50`,
the activation commit and rollback parent. The Plan-only RED and 49-Plan /
51-Task evidence baseline was
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; prerequisite commits `5ed6de6`
and `fdc86ee` changed no Stage 04 document, so the active pair still raises the
proposed corpus to 50 Plans and 52 Tasks. The activation changes lifecycle
lineage only; RIA-001 through RIA-007 remain unexecuted until their own
test-first evidence, review verdicts, and logical commits exist.

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

### Global Constraints

- Preserve `docs/99.templates/support/document-profiles.json#referenceCurrentPacks`
  as the only Current-pack pointer and member authority.
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
| `docs/90.references/data/reference-information-architecture.schema.json` | Closed JSON Schema for derived immutable guards, section/cell projection rules, source/freshness records, generator relations, and pair-scoped duplicate exceptions. |
| `docs/90.references/data/reference-information-architecture.json` | Repo-local Spec 038 contract instance; references Current pack IDs and pinned commits without repeating their members, paths, digests, or pointers. |
| `scripts/reference_information_architecture.py` | Pure parsing, normalization, digest, Git-object, and finding functions shared by CLI and tests. |
| `scripts/validate-reference-information-architecture.py` | Thin CLI with `--root`, `--contract`, and `--self-test`; prints stable rule IDs and returns 0/1/2. |
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
| RIA-000 | Atomic reciprocal planning activation | None | Plan-only lifecycle RED observed at evidence baseline `8fb9821`; reviewed prerequisite head `fdc86ee` exists | Exact seven-file staged lifecycle GREEN, complete commit-level QA, independent planning re-reviews, rollback parent `fdc86ee`, and activation commit |
| RIA-001 | Closed reference contract, safe loader, and diagnostic interface | RIA-000 | Reviewed activation commit exists | Draft 2020-12 schema/instance validation, contract negative fixtures, focused CLI self-test, complete commit gate, and reviewed logical commit |
| RIA-002 | Audit/research immutability and projection-bounded Current overlay guard | RIA-001 | Pinned source contract loads without findings | Historical/Resolved/Current mutation fixtures fail; exact overlay and navigation projections pass; complete commit gate and review pass |
| RIA-003 | Data source, adopted/rejected scope, and freshness validation | RIA-002 | Observation guards are GREEN | Missing/invalid evidence, scope, date, and trigger fixtures fail; production data inventory passes the complete commit gate and review |
| RIA-004 | Generated ownership and zero-drift validation | RIA-003 | Source/freshness relation is GREEN | Generator collision, command, input/output, stale byte, and owner-link fixtures fail; production generator relation passes the complete commit gate and review |
| RIA-005 | Duplicate Current/generated/manual/policy-owner validation | RIA-004 | Generated relation is GREEN | Duplicate claims/copies and exception-reuse fixtures fail; production Stage 90 has zero findings after the complete commit gate and review |
| RIA-006 | Aggregate integration and command inventories | RIA-005 | All focused production validation is clean | Aggregate invocation RED/GREEN, repository QA, complete commit gate, independent review, and logical integration commit |
| RIA-007 | Independent whole-tranche review and atomic lifecycle closure | RIA-006 | Aggregate integration commit is reviewed | Full/all-files QA, terminal requirements and quality approval, logical closure/evidence commits, and clean-tree postflight |

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
  two new 14-column ledger rows, and the updated Spec row. Keep RIA-001 through
  RIA-007 Queued and the existing registry relation unchanged.

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

- [ ] **Step 6: Commit and verify the activation.** Commit exactly the seven
  files with `docs(execution): activate reference information architecture`,
  run explicit-ref lifecycle from `fdc86ee` to the new commit, rerun focused
  document gates, and require clean status before dispatching RIA-001.

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

- [ ] **Step 1: Write the closed-schema RED fixtures.** Add tests that reject
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

- [ ] **Step 2: Run the focused RED.** Run
  `python3 -m unittest tests/test_reference_information_architecture.py -v`.
  Expect import or target-existence failures because the module, CLI, schema,
  and contract do not exist; record only the observed diagnostic in the Task.

- [ ] **Step 3: Implement the minimum safe loader and closed schema.** Use a
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

- [ ] **Step 4: Implement CLI self-test and the production contract skeleton.**
  `--self-test` runs the fixture matrix without reading the production corpus;
  normal mode validates the contract instance. The instance references the two
  registry pack IDs but does not copy their member lists, report paths,
  per-member digests, or Current pointers. Current paths and comparison digests
  are derived at validation time and must equal the registry membership
  exactly. CLI self-test must exercise the accepted encoded commit and every
  malformed-prefix case through the same production parser.

- [ ] **Step 5: Run GREEN and contract checks.** Run:

  ```bash
  python3 -m unittest tests/test_reference_information_architecture.py -v
  python3 scripts/validate-reference-information-architecture.py --self-test
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 -c 'import json; from jsonschema import Draft202012Validator as V; s=json.load(open("docs/90.references/data/reference-information-architecture.schema.json")); i=json.load(open("docs/90.references/data/reference-information-architecture.json")); V.check_schema(s); V(s).validate(i)'
  ```

  Expect all focused tests and self-test to pass. Production may still report
  only the RIA-002/RIA-003 entries intentionally not populated; it must not
  traceback, traverse ignored paths, or claim those criteria PASS.

- [ ] **Step 6: Run the RIA-001 commit gate, review, and commit.** Run pre-commit
  for the seven RIA-001 files, full all-files pre-commit, formatter-diff
  inspection, affected-hook rerun, and both diff checks exactly as required by
  Global Constraints. Obtain requirements compliance and code-quality approval,
  remediate findings, rerun the gate, then commit with
  `feat(references): add reference architecture contract`.

### Task 2: RIA-002 — Immutable observation and overlay guard

**Files:**

- Modify: `docs/90.references/data/reference-information-architecture.json`
- Modify: `scripts/reference_information_architecture.py`
- Modify: `tests/test_reference_information_architecture.py`
- Create: `tests/fixtures/reference-information-architecture/snapshot-mutation.json`
- Create: `tests/fixtures/reference-information-architecture/overlay-mutation.json`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`

**Interfaces:**

- Consumes: validated RIA-001 contract plus exact Git commit and blob reads.
- Produces: `validate_snapshot_guards(...)` and
  `validate_overlay_guards(...)`; each returns ordered `Finding` values and
  compares tracked regular-file bytes or exact parsed table/link projections
  only to declared committed baselines. Current members and comparison digests
  are derived from the registry and may not be supplied by the contract.

- [ ] **Step 1: Add RED tests for immutable observation bodies.** Create fixture
  repositories where a Historical/Resolved audit report, Historical research
  report, or fact-bearing pack README differs by one protected byte from its
  source blob; a protected file is missing; the source ref is not a commit; or
  runtime-derived SHA-256 differs. Expect `RIA-SNAPSHOT` in deterministic path
  order. Reject contract-supplied Current member paths or per-member digests.
  Exercise the RIA-001 encoded-commit parser and reject a bare/invalid/repeated
  prefix before any Git subprocess call. Add closed-runner fixtures for a
  missing executable result, non-zero exit, timeout, malformed or multiple
  `ls-tree` records, mismatched path, non-blob/symlink mode, oversized blob,
  short/extra blob bytes, inherited hostile Git environment, shell use, and
  argv outside the exact allowlist.

- [ ] **Step 2: Add RED tests for overlay-only and navigation projections.** Pin
  Current pack observation commits; derive their members from the registry;
  mutate a protected report, snapshot SHA, score, scope, arithmetic cell, or
  fact-bearing README prose and expect `RIA-OVERLAY`. Accept only the complete
  remediation-roadmap body; `Audit Pack Registry` `Pack role` and
  `Successor / resolution` cells; `Research Pack Index` `Status` cells;
  Current audit `Report Index` `Lifecycle` and `Actionable disposition` cells;
  Current research `Report Index` `Lifecycle` cells; and an exact
  `navigationReplacement` record that changes one declared link destination
  without changing visible text. Reject whole-file README mutability, globs,
  undeclared columns/sections, and reusable navigation exceptions.

- [ ] **Step 3: Run RED.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_snapshot_mutation tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_current_overlay_boundary -v`.
  Expect failures because the guard functions are absent.

- [ ] **Step 4: Implement committed-baseline and projection comparison.** Pass
  `snapshotGuard.sourceCommit` through `parse_git_sha1()` and give Git only its
  returned 40-hex OID. Set `GIT_EXECUTABLE = "/usr/bin/git"`, `shell=False`, a
  10-second timeout, and a newly constructed closed environment with
  `HOME=/nonexistent`, `PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
  `GIT_LITERAL_PATHSPECS=1`, `GIT_NO_LAZY_FETCH=1`,
  `GIT_NO_REPLACE_OBJECTS=1`, `GIT_OPTIONAL_LOCKS=0`, and
  `GIT_TERMINAL_PROMPT=0`; do not inherit arbitrary `GIT_*` variables. Permit
  only these literal argv shapes:

  ```text
  /usr/bin/git cat-file -t <commit-oid>
  /usr/bin/git ls-tree -z --full-tree <commit-oid> -- <safe-path>
  /usr/bin/git cat-file -t <blob-oid>
  /usr/bin/git cat-file -s <blob-oid>
  /usr/bin/git cat-file blob <blob-oid>
  ```

  Require `commit\n`; parse exactly one NUL-terminated regular-blob tree record
  whose returned path equals the requested safe path; validate the blob OID as
  40 lowercase hex; require `blob\n`; parse a canonical decimal size no larger
  than `2_000_000`; cap metadata stdout at 65,536 bytes and every stderr at
  16,384 bytes; read no blob until its size passes; cap blob stdout at the
  declared size; kill the process on timeout or cap overflow; and require
  returned blob length to equal the declared size. Treat timeout, non-zero
  exit, overflow, malformed/extra output, type,
  mode, path, size, or length mismatch as value-free `RIA-SNAPSHOT`; never use
  `HEAD`, revision expressions, a shell, or lazy/network fetch. Derive Current
  paths from exact registry membership, derive every comparison digest, and
  compare proposed tracked regular files. For README projections, mask only the
  exact declared table cells or one link destination before byte comparison;
  all remaining bytes stay protected. Do not infer a baseline from worktree
  bytes and do not exempt a whole README.

- [ ] **Step 5: Populate production guards without member duplication.** Pin
  snapshot evidence baseline
  `git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; reference the five Historical/Resolved audit
  pack IDs and Historical research pack `research/2026-07-04-wer`, and reference
  Current audit/research pack IDs only. Derive all direct tracked Markdown
  members and SHA-256 values from the pinned commit and Current registry at
  validation time. Declare the exact overlay/table/link projections from Step 2
  and no mutable README path.

- [ ] **Step 6: Run focused and production GREEN.** Run the full unit module,
  CLI self-test, production CLI, strict document registry, strict Markdown,
  and strict cross-link validation. Expect zero snapshot/overlay findings and
  no changes to protected observation files.

- [ ] **Step 7: Run the RIA-002 commit gate, review, and commit.** Run pre-commit
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

- [ ] **Step 1: Write exact source-ledger RED tests.** Add
  `test_data_asset_requires_source_scope_date_and_trigger`,
  `test_data_asset_rejects_after_cutoff_and_untracked_evidence`, and
  `test_data_asset_accepts_closed_source_ledger`. Reject missing/non-HTTPS URL,
  invalid date, date after `evidenceCutoff`, empty adopted or rejected scope,
  empty trigger, missing asset, missing tracked repo evidence, unknown fields,
  and duplicate source records.

- [ ] **Step 2: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_requires_source_scope_date_and_trigger tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_rejects_after_cutoff_and_untracked_evidence tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_data_asset_accepts_closed_source_ledger -v`.
  Expect failures because `validate_data_assets` is absent.

- [ ] **Step 3: Implement the minimal closed source ledger.** Parse dates
  strictly, compare them only to the contract cutoff for deterministic results,
  require non-empty adopted/rejected arrays, validate HTTPS URLs without network
  access, and validate repo evidence through the RIA-001 tracked no-follow read
  boundary. Do not invent a universal expiry date.

- [ ] **Step 4: Populate every current data asset.** Add all current
  `docs/90.references/data/` assets, including the RIA schema/contract, with
  exact tracked evidence, checked official-source URL, adopted scope, rejected
  scope, and refresh trigger. Preserve data authority boundaries and do not
  convert repo-backed evidence into live PASS.

- [ ] **Step 5: Run focused and production GREEN.** Run the full unit module,
  CLI self-test, production CLI, Draft 2020-12 schema/instance validation, and
  strict Markdown/link checks. Expect zero `RIA-SOURCE` findings.

- [ ] **Step 6: Run the RIA-003 commit gate, review, and commit.** Run pre-commit
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

- [ ] **Step 1: Write exact generator RED tests.** Add
  `test_generator_requires_unique_owner_relation`,
  `test_generator_rejects_unmapped_command_and_stale_output`, and
  `test_generator_accepts_llm_wiki_relation`. Reject duplicate output owners,
  generator/output identity, missing tracked generator/input/output, directory
  or symlink output, unknown command, stale generated bytes, and stale
  canonical-owner links.

- [ ] **Step 2: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_requires_unique_owner_relation tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_rejects_unmapped_command_and_stale_output tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_generator_accepts_llm_wiki_relation -v`.
  Expect failures because `validate_generated_assets` is absent.

- [ ] **Step 3: Implement fixed-argv validation.** Validate relation shape and
  tracked paths, map the one exact check string to a literal argv tuple, execute
  it without a shell in a sanitized environment, and return path-only
  `RIA-GENERATOR` diagnostics. Contract data may not introduce another command.

- [ ] **Step 4: Populate one production relation.** Register
  `scripts/generate-llm-wiki-index.sh`, its declared input roots,
  `docs/90.references/llm-wiki/wiki-index.md`, and the exact check command.
  Run `bash scripts/generate-llm-wiki-index.sh --check` and require zero drift.

- [ ] **Step 5: Run focused and production GREEN.** Run the full unit module,
  CLI self-test/production, direct generator no-diff, and strict links. Expect
  zero `RIA-GENERATOR` findings.

- [ ] **Step 6: Run the RIA-004 commit gate, review, and commit.** Run pre-commit
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

- [ ] **Step 1: Write exact duplicate-owner RED tests.** Add
  `test_duplicate_current_and_generated_manual_owners_fail`,
  `test_policy_paragraph_copy_fails`, and
  `test_structural_exception_is_pair_scoped`. Reject a second Current claim,
  generated/manual collision, and any normalized paragraph of at least 160
  visible characters copied from Stage 00 policy, Stage 05 Policy, or Stage 05
  Runbook into Stage 90.

- [ ] **Step 2: Prove exception non-reuse in RED.** Accept an exception only
  when the digest occurs in the exact canonical/reference path pair and matches
  its declared structural role; reject use at any other source, destination,
  digest, or role, stale records, unknown roles, and blanket digest lists.

- [ ] **Step 3: Run the named RED selectors.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_duplicate_current_and_generated_manual_owners_fail tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_policy_paragraph_copy_fails tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_structural_exception_is_pair_scoped -v`.
  Expect failures because `validate_duplicate_rules` is absent.

- [ ] **Step 4: Implement minimal normalized comparison.** Derive Current claims
  from registry/index mirrors, compare generated outputs to manual owners, hash
  normalized visible paragraphs, and validate closed pair-scoped structural
  exceptions. Headings, pure link lists, table headers, and generated notices
  are ignored by parser classification, not by a global digest allowlist.

- [ ] **Step 5: Run production scan and remediate only proven gaps.** Replace a
  prohibited current policy/procedure copy with concise analysis and a
  canonical link while preserving dated facts, sources, and interpretation.
  Add a structural exception only when its exact two-path role is verified.

- [ ] **Step 6: Run focused and production GREEN.** Run the full unit module,
  CLI self-test/production, generator no-diff, and strict links. Expect zero
  duplicate Current, generated/manual, or active-policy copy findings.

- [ ] **Step 7: Run the RIA-005 commit gate, review, and commit.** Run pre-commit
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

- [ ] **Step 1: Add the exact aggregate-integration RED.** Add
  `ReferenceInformationArchitectureTests.test_aggregate_runs_self_test_before_production`
  to `tests/test_reference_information_architecture.py`. It reads the aggregate
  script and asserts one self-test invocation precedes one production `--root`
  invocation.

- [ ] **Step 2: Run the named RED selector.** Run
  `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_aggregate_runs_self_test_before_production -v`.
  Expect failure because the aggregate has neither invocation.

- [ ] **Step 3: Add minimal aggregate wiring and inventories.** Invoke focused
  self-test then production validation without changing CI topology or the
  generator owner. Document CLI arguments, exits, rule IDs, safe boundaries,
  the focused test selector, and production command in the two inventories.

- [ ] **Step 4: Run focused and repository GREEN.** Run the named selector,
  full focused module, CLI self-test/production, generator no-diff, registry
  self-test/strict, strict Markdown/links, and
  `bash scripts/validate-repo-quality-gates.sh .`. Expect PASS and no lifecycle,
  CI, provider, remote, or live claim.

- [ ] **Step 5: Run the RIA-006 commit gate, review, and commit.** Run pre-commit
  for the exact four files, full all-files pre-commit, formatter-diff
  inspection, affected-hook rerun, and both diff checks. Obtain fresh
  requirements and quality approval, rerun after fixes, then commit with
  `chore(qa): integrate reference architecture validation`.

### Task 7: RIA-007 — Independent review and atomic lifecycle closure

**Files:**

- Modify: `docs/03.specs/038-reference-information-architecture/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-22-reference-information-architecture.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-22-reference-information-architecture.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: reviewed activation and RIA-001 through RIA-006 commits.
- Produces: exact Task results, atomic `active -> done` Spec/Plan/Task proposal,
  closure commit, explicit-ref postflight, and a separately gated evidence-only
  commit whose own identity is never self-claimed.

- [ ] **Step 1: Prepare terminal evidence without pre-claiming commits.** Mark
  each RIA row Done only with exact observed test/review/commit evidence; update
  Spec/Plan/Task and all three indexes in one staged lifecycle proposal; update
  the two migration-ledger rows and inventory/freshness counts. Keep closure
  and evidence-update commit identities explicitly unidentified until observed.

- [ ] **Step 2: Run terminal repository QA.** Run focused tests, production
  reference validation, generator no-diff, registry self-test/strict, staged
  lifecycle, strict Markdown/links, aggregate QA, exact seven-file pre-commit,
  `env TMPDIR=/tmp pre-commit run --all-files`, formatter-diff inspection,
  affected-hook reruns, and both diff checks. Require observed PASS; a skipped
  strict hook cannot substitute for closure evidence.

- [ ] **Step 3: Obtain independent whole-tranche reviews.** Generate a review
  package from activation parent `fdc86ee` through proposed HEAD. Require exact
  verdicts `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; remediate all
  blocking findings, rerun affected/full gates, and repeat both reviews.

- [ ] **Step 4: Run the closure commit gate and commit.** Re-run the exact
  changed-file and all-files gates after the final review, inspect formatter
  diffs, rerun affected hooks, require both diff checks, then commit the seven
  lifecycle paths with
  `docs(sdlc): close reference information architecture tranche`.

- [ ] **Step 5: Verify clean-tree postflight.** Run explicit-ref lifecycle from
  the activation commit to the closure commit, focused/production/generator,
  strict document, aggregate, all-files pre-commit, `git diff --check`, and
  clean status. Record only directly observed outcomes.

- [ ] **Step 6: Prepare and gate the postflight evidence update.** Add the
  observed closure commit and postflight results to Spec/Plan/Task/index/ledger
  without identifying the evidence-update commit. Run exact changed-file and
  all-files pre-commit, inspect formatter diffs, rerun affected hooks, require
  both diff checks, and obtain task-scoped requirements/quality approval.

- [ ] **Step 7: Commit the evidence update.** Commit with
  `docs(sdlc): record reference architecture postflight`, rerun strict document
  and aggregate checks, and require clean status. Record no remote/live PASS.

## Verification Plan

| Spec criterion | Deterministic evidence | Required result |
| --- | --- | --- |
| VAL-RIA-001 | Existing Current-pack registry/link self-tests plus focused pack-reference fixtures | Exactly one audit and one research Current pointer; contract references but does not duplicate pack authority |
| VAL-RIA-002 | Pinned source/blob/digest fixtures and production observation guards | Historical/Resolved audit and Historical research observation bodies, including fact-bearing README bytes outside projections, equal committed baseline |
| VAL-RIA-003 | Current protected-body and exact table/link projection fixtures | Only the remediation overlay and declared navigation cells/link destinations can change; snapshot facts remain protected |
| VAL-RIA-004 | Data asset URL/date/adopted/rejected-scope/trigger fixtures and production contract | Every governed data asset has repo evidence, checked source, adopted and rejected scope, and refresh trigger |
| VAL-RIA-005 | Generator ownership fixtures and `generate-llm-wiki-index.sh --check` | One generator relation and zero output drift |
| VAL-RIA-006 | Current-claim, generated/manual, and normalized policy-copy fixtures | Zero duplicate owners or copied active policy/procedure paragraphs |
| Repository closure | Strict registry/Markdown/links/lifecycle, aggregate, all-files pre-commit, diff, independent review | All repository-static lanes PASS and live/remote lanes remain accurately bounded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| New contract duplicates Current-pack authority | Two sources disagree about members, paths, digests, or pointers | Reference registry pack IDs and pinned commits only; derive Current members and digests at validation time and forbid those fields in the schema |
| Worktree bytes become their own baseline | Existing drift is blessed silently | Pin a committed source, verify object type and declared digest, and read exact Git objects |
| Overlay rule permits broad mutation | Observation facts can be rewritten as closure evidence | Permit the exact remediation body and table-cell/link-destination projections only; reject whole README paths, globs, undeclared sections, and fact-cell changes |
| Paragraph-copy scan produces noise | Valid analysis is blocked or broad allowlists appear | Normalize visible paragraphs, use a 160-character minimum, classify structural/link-only text, and bind every exception to one canonical/reference path pair, digest, role, and reason |
| Generator check becomes arbitrary execution | Contract data can run commands | Map one exact check string to a fixed argv; never invoke through a shell |
| Stage 90 remediation changes historical meaning | Audit/research evidence loses integrity | Preserve observation bodies and only replace proven current policy copies with canonical links |
| Spec 039 portability debt contaminates closure | SKIP/DEFER is mislabeled PASS | Use `TMPDIR=/tmp` for the approved local all-files lane and retain explicit ownership/limitation text |

Rollback is newest-first by reviewed logical commit. Before RIA-007 terminal
closure, revert only the failing package and its exact contract/index changes.
After closure, revert the evidence-update commit first, then closure, then
RIA-006 through RIA-001, and the seven-file activation commit last. Preserve
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
  no parallel member or pointer source exists.
- Historical/Resolved audit, Historical research, and protected Current
  observation bytes match pinned committed baselines; only declared
  overlay/navigation projections remain mutable.
- Every governed data asset has repo evidence, source URL, checked date,
  adopted/rejected scope, and refresh trigger; the generated wiki has one owner
  and zero drift.
- Duplicate Current owners, generated/manual outputs, and copied active-policy
  paragraphs are zero or represented only by verified pair-scoped structural
  exceptions.
- Strict document, reference, aggregate, all-files pre-commit, diff, and
  independent whole-tranche reviews pass; worktree status is clean.
- Spec 038, this Plan, its Task, indexes, registry relation, and migration
  ledger agree on terminal state without activating Spec 039 or PRD-003.

## Traceability

- **Spec**: [Reference Information Architecture](../../03.specs/038-reference-information-architecture/spec.md)
- **Task**: [Reference Information Architecture Task](../tasks/2026-07-22-reference-information-architecture.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Current audit**: [2026-07-11 WEIA](../../90.references/audits/2026-07-11-weia/README.md)
- **Current research**: [2026-07-07 WER](../../90.references/research/2026-07-07-wer/README.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-RIA-001](../../03.specs/038-reference-information-architecture/spec.md#success-criteria--verification-plan) | RIA-001, RIA-005, RIA-007 | [Contract and Current-pack evidence](../tasks/2026-07-22-reference-information-architecture.md#task-table) |
| N/A — VAL-RIA-002 shares the Spec 038 source linked in VAL-RIA-001 | RIA-002, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-003 shares the Spec 038 source linked in VAL-RIA-001 | RIA-002, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-004 shares the Spec 038 source linked in VAL-RIA-001 | RIA-003, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-005 shares the Spec 038 source linked in VAL-RIA-001 | RIA-004, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
| N/A — VAL-RIA-006 shares the Spec 038 source linked in VAL-RIA-001 | RIA-005, RIA-007 | N/A — the paired Task is linked in VAL-RIA-001 |
