---
title: 'GitHub CI and QA Evidence Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-27
artifact_id: "PLAN-0039"
---

# GitHub CI and QA Evidence Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this Plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close
[Spec 039](spec.md) with a
portable GitOps boundary self-test, one exact-version CI Python dependency
contract, explicit all-files pre-commit execution, seven-day transient artifact
retention, preserved affected/full-document selection, and unambiguous
PASS/SKIP/FAIL/DEFER completion evidence.

**Architecture:** Keep
`docs/00.agent-governance/contracts/validation-surfaces.json` as the path,
validator, and CI-selection owner. Add one narrow CI Python contract validator
that reconciles `.github/requirements/ci-validation.txt`,
`.github/workflows/ci.yml`, and the technology inventory without duplicating
general Action security. Extend the existing GitHub Actions security validator
only for artifact retention. Make the GitOps self-test capability-aware while
preserving the same non-regular-file rejection. Keep result semantics in
`quality-standards.md`; provider shims, PR guidance, and checklists consume that
authority instead of redefining it.

**Tech Stack:** GitHub Actions YAML, Python 3.12, `pre-commit==4.6.1`,
`PyYAML==6.0.3`, `jsonschema==4.26.0`, Python standard-library `unittest`,
repository shell validators, JSON fixtures, Markdown governance, and Git
explicit-ref lifecycle validation.

The approved activation and rollback parent is
`cd726e05fdb9d33727314d316aadb5ebbec0942d`. The latest observed remote
GitHub Actions result remains run `29982910320`, an observed FAIL for commit
`bd93374d7f531317c3bd061eb1ef567c1e2e0084`; it is not evidence for the
current local branch. This Plan authorizes repository-local implementation
only. A push, workflow dispatch, branch-protection mutation, or post-change
hosted result requires separate approval.

GCQE-000 through GCQE-005 are complete from observed commits, focused and
repository-static gates, and their recorded reviews. GCQE-006 now prepares the
exact eight-file terminal lifecycle proposal at base HEAD
`39e6150a6f7a79b710d0e2cd7bc2dee8349f871a`. Test-only commits `096c5c4`,
`b5c3eea`, and `39e6150` respectively close final-tranche lifecycle fixtures,
advance the exact active-corpus terminal frontier, and bind current/advanced
test assertions to index object identities. Their scoped reviews returned
`REQUIREMENTS COMPLIANT` / `QUALITY APPROVED`; they do not approve the
whole-tranche terminal proposal. The proposal passes the 46-test residue
class, 84-test module, 22-case self-test, exact advanced production frontier,
repository aggregate, 668-case lifecycle self-test, staged lifecycle, and
strict document gates. Earlier terminal review attempts found rollback
omissions and the old-frontier aggregate failure; later staged testing found
three old-state assertions and a first test-compat index-OID P1. Those findings
are remediated. The sole later invalid explicit-ref finding is also closed;
fresh whole-tranche reviewers `/root/gcqe006_final_requirements` and
`/root/gcqe006_final_quality` returned `REQUIREMENTS COMPLIANT` and `QUALITY
APPROVED`, with no findings against corrected patch digest
`58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
The terminal commit gate is observed complete. Closure commit
`e1d1e910840337327a557ab4b84e86f8fced11d6` contains the exact eight-file
lifecycle package, and the activation-to-closure explicit-ref lifecycle plus
clean-tree postflight passed on 2026-07-27. Hosted run `29982910320` remains
historical FAIL evidence for its older SHA; current hosted, provider, and live
evidence remains `DEFER`. This later evidence update does not identify or
claim its own commit.

### Global Constraints

- Work only in the repository-local isolated worktree for
  `feat/agent-governance-platform`.
- Preserve Spec 039 as the sole owner of this tranche. Do not absorb Spec 040
  closure compatibility or Specs 041-046 provider-harness work.
- Begin every behavior-changing package with a focused failing test or fixture,
  observe the expected RED, implement the minimum GREEN, review, and commit as
  one logical unit.
- Use `apply_patch` for tracked edits. Preserve unrelated user work and stage
  only the files named by the active package.
- Run affected and staged checks during work. Before every logical commit, run
  `pre-commit run --all-files`, inspect formatter mutations with
  `git status --short`, `git diff`, and `git diff --cached`, rerun affected
  hooks after any mutation, and require both diff checks to pass.
- Do not use the POSIX `/tmp` environment override as Spec 039 closure evidence.
  The unqualified all-files command must pass after the FIFO portability fix.
- Keep the CI workflow entry present for every supported event and retain
  `ci-summary` with `if: always()` as the sole aggregate hosted verdict.
- Keep affected selection conservative. Contract, registry, schema, template,
  governance, validator, archive, and migration-ledger paths must continue to
  select pre-commit and repository-quality document validation.
- Keep GitHub Actions at immutable full commit SHAs and default
  `contents: read`; do not broaden write permissions.
- Install CI-owned Python packages only from
  `.github/requirements/ci-validation.txt`. Do not add a second requirements
  owner, loose inline package installs, mutable version ranges, or
  `pre-commit/action`.
- Treat the changelog artifact as transient review evidence with exactly seven
  retention days. It is not a release publication or canonical tracked
  changelog.
- Report PASS, SKIP, FAIL, and DEFER literally. A historical remote FAIL,
  unavailable hosted rerun, optional-tool SKIP, and local repository PASS are
  different evidence records.
- Do not read or print credentials, tokens, kubeconfigs, auth files, ignored
  `_workspace` contents, shell history, or secret values.
- Do not install dependencies, push, dispatch workflows, modify GitHub
  settings, merge, publish, deploy, or mutate live Kubernetes/Vault resources
  without separate explicit approval.

### File Responsibility Map

| Path | Responsibility |
| --- | --- |
| `scripts/validate-gitops-change-set.py` | GitOps identity/deletion validation and portable non-regular-file self-test boundary. |
| `tests/test_validate_gitops_change_set.py` | Focused FIFO-supported, unsupported, and unexpected-error regressions. |
| `.github/requirements/ci-validation.txt` | Sole exact-version CI Python dependency owner. |
| `.github/workflows/ci.yml` | Always-entered CI topology, affected internal jobs, explicit dependency setup, all-files pre-commit, and aggregate verdict. |
| `scripts/validate-ci-python-contract.py` | Reconciles the requirements file, CI workflow, and technology inventory with stable rule IDs. |
| `tests/test_validate_ci_python_contract.py` | Positive and hostile unit cases for the CI Python contract. |
| `tests/fixtures/validation-surfaces.json` | Contract/bulk-document selection regression. |
| `scripts/validate-affected-surfaces.py` | Existing fixture runner and CI range/selector owner; changes only if a new required fixture name or assertion is necessary. |
| `.github/workflows/generate-changelog.yml` | Seven-day changelog preview artifact producer. |
| `scripts/validate-github-actions-security.py` | Immutable Action identity, least privilege, and artifact-retention enforcement. |
| `tests/fixtures/github-actions-security.json` | Exact artifact-retention positive and negative self-test cases. |
| `scripts/validate-repo-quality-gates.sh` | Aggregate ordering, workflow topology, guidance invariants, and self-test-before-production invocation. |
| `docs/90.references/data/tech-stack-version-inventory.md` | Human-readable mirror of exact CI Python and Action identities. |
| `docs/00.agent-governance/rules/quality-standards.md` | Canonical lane, result, all-files, formatter-review, and handoff semantics. |
| `docs/00.agent-governance/rules/postflight-checklist.md` | Completion checklist consuming the canonical QA semantics. |
| `docs/00.agent-governance/rules/git-workflow.md` | Logical-commit and branch-finish QA obligations. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Reviewer-facing all-files and evidence-class checklist. |
| `.github/ABOUT.md` | GitHub surface routing and current workflow responsibility claims. |
| `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` | Operator-facing CI/QA command and evidence guidance. |
| `scripts/README.md`, `tests/README.md` | Command and test inventory updates. |
| Spec/Plan/Task/index/progress files | Reciprocal activation, implementation evidence, review, rollback, and terminal lifecycle records. The settled 446-row migration snapshot is a protected input, not an activation output. |

## Context

The local worktree passes the repository aggregate and passes all-files
pre-commit only when `TEMP`, `TMP`, and `TMPDIR` are redirected to POSIX
`/tmp`. The unqualified invocation inherits a Windows-mounted temporary
directory and `scripts/validate-gitops-change-set.py --self-test` aborts when
`os.mkfifo` returns error 95. The self-test intends to prove rejection of a
non-regular manifest resource; its purpose does not require a FIFO when the
filesystem cannot create one.

The remote `main` evidence is older than the local branch. Run `29982910320`
failed `pre-commit`, `repo-quality-static`, and `ci-summary` because the
`language: system` hooks imported `jsonschema` before the pre-commit job had
installed it. The job delegates to `pre-commit/action`, while the other CI jobs
install loose, different Python package sets. The Action also brought a
transitive Node.js 20 warning. The fix is one explicit Python version, one
exact-version file, and one explicit `pre-commit run --all-files` command.

The affected-surface contract and `ci-summary` topology already implement most
of VAL-GCQE-001 and VAL-GCQE-002. This tranche protects those behaviors with
focused fixtures instead of replacing them. The only artifact upload,
`generate-changelog.yml`, currently omits `retention-days`. The existing
Actions security validator is the narrow owner for the new seven-day rule.

The version choices use the official package records observed on 2026-07-26:

- [pre-commit 4.6.1](https://pypi.org/project/pre-commit/4.6.1/) is the current
  release and the official pre-commit documentation recommends
  `pre-commit run --all-files` for CI.
- [PyYAML 6.0.3](https://pypi.org/project/PyYAML/) is the current exact YAML
  dependency used by repository validators.
- [jsonschema 4.26.0](https://pypi.org/project/jsonschema/) is the current exact
  schema dependency used by affected-surface and document checks.
- GitHub's
  [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use)
  supports immutable Action identity and least-privilege permissions.
- GitHub's
  [artifact retention guidance](https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization)
  distinguishes explicit workflow retention from repository defaults.

### Legacy Task ledger inputs

This Task is the execution, verification, review, rollback, and handoff evidence
owner for GCQE-000 through GCQE-006. It records
[Spec 039](spec.md) from approved
design, activation, and rollback parent
`cd726e05fdb9d33727314d316aadb5ebbec0942d`.

The Plan-only staged lifecycle probe is directly observed. It exited `1` with
`LIFECYCLE-CREATE`, expected exactly one active Plan and one active Task, and
observed Plan count `1` and Task count `0`. This reciprocal Task closes that
intentional creation RED. No implementation package, hosted CI rerun, review
approval, closure commit, or live result is claimed at activation.

The latest hosted evidence remains GitHub Actions run `29982910320`, an
observed FAIL for commit
`bd93374d7f531317c3bd061eb1ef567c1e2e0084`. It exposed missing Python
dependencies in the pre-commit job and a transitive Node.js warning from
`pre-commit/action`. A post-change hosted result remains DEFER until a
separately approved push or workflow dispatch is directly observed.

GCQE-001 through GCQE-005 are complete through reviewed implementation and
integration evidence at `aaee364`. Test-only final-tranche lifecycle-fixture
commit `096c5c48e364663c616a1984089c11a1fe5b3b61` received `REQUIREMENTS
COMPLIANT` / `QUALITY APPROVED` from
`/root/gcqe006_selftest_rapid_review`. Active-corpus frontier commit
`b5c3eea128b8b3be7c858f70803f83994be1fc77` received `REQUIREMENTS
COMPLIANT` from `/root/gcqe006_frontier_requirements_review` and `QUALITY
APPROVED` from `/root/gcqe006_frontier_quality_review`. Test-only
index-bound current/advanced assertion commit
`39e6150a6f7a79b710d0e2cd7bc2dee8349f871a` received fresh `REQUIREMENTS
COMPLIANT` from `/root/gcqe006_test_compat_requirements_review` and `QUALITY
APPROVED` from `/root/gcqe006_test_compat_fresh_quality`. These approvals are
scoped to their compatibility changes, not the whole terminal tranche.

GCQE-006 closed on 2026-07-27 in
`e1d1e910840337327a557ab4b84e86f8fced11d6`. That commit contains exactly the
Spec, Plan, Task, their three indexes, the document-profile registry, and
shared progress paths listed by Plan Task 6; the registry-owned PRD-0006
program-lineage state for Spec 039 is terminal while Spec 040 remains
`active`. The 46-test residue class, 84-test module, 22-case residue self-test,
exact advanced production frontier, repository aggregate, 668-case lifecycle
self-test, and Step 2 staged/strict gates passed; the settled migration
snapshot remains byte-identical. After the sole invalid explicit-ref finding
was closed, `/root/gcqe006_final_requirements` returned `REQUIREMENTS
COMPLIANT` and `/root/gcqe006_final_quality` returned `QUALITY APPROVED`, with
no findings against corrected patch digest
`58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
Step 6 then passed explicit-ref lifecycle using the raw activation and closure
OIDs, CI Python production at `3` jobs / `3` pins, GitHub Actions security,
GitOps self-test, clean-tree repository aggregate, and all applicable
all-files hooks. Dockerfile lint was a no-file `SKIP`; status, diff, and
diff-check inspection were clean. Hosted run `29982910320` remains historical
FAIL evidence for its older SHA, while current hosted, provider, and live
evidence remains `DEFER`. This later evidence update does not identify or
claim its own commit.

- [GitHub CI and QA Evidence Implementation Plan](plan.md)
- [Spec 039](spec.md)
- [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [Affected-surface contract](../../00.agent-governance/contracts/validation-surfaces.json)
- [Agent quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Git workflow](../../00.agent-governance/rules/git-workflow.md)
- [GitHub configuration hub](../../../.github/README.md)
- [Technology version inventory](../../90.references/data/tech-stack-version-inventory.md)
- `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`; [current lookup](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Predecessor Spec 038 Task](../0038-reference-information-architecture/README.md)
## Goals & In-Scope

- Make the GitOps self-test pass on FIFO-capable and FIFO-unsupported
  filesystems while always exercising `RESOURCE_NOT_REGULAR`.
- Pin Python `3.12` in all three validation jobs and install the same exact
  `pre-commit`, `PyYAML`, and `jsonschema` contract before execution.
- Remove `pre-commit/action` and execute
  `pre-commit run --all-files --show-diff-on-failure` with full checkout
  history.
- Add deterministic validation that rejects loose dependency versions, inline
  package installs, inventory drift, mutable Python selection, missing full
  history, missing all-files execution, or reintroduction of
  `pre-commit/action`.
- Preserve the always-entered CI workflow, conditional internal jobs,
  `ci-summary if: always()`, and conservative full-document selection.
- Require exactly seven retention days on every `actions/upload-artifact`
  step and cover missing, string, and wrong numeric values.
- Require AI agents and human contributors to run all-files pre-commit, inspect
  formatter changes, rerun affected checks, and report every evidence lane
  with the canonical result vocabulary.
- Add focused unit/self-test/production evidence, aggregate integration,
  independent review, logical commits, rollback boundaries, and atomic terminal
  lifecycle closure.

## Non-Goals & Out-of-Scope

- Pushing the branch, dispatching a hosted workflow, changing branch
  protection/rulesets, or claiming a post-change GitHub Actions PASS.
- Adding deploy CD, container publication, changelog commits, release
  publication, direct Kubernetes mutation, or Vault/ESO/Argo CD live work.
- Installing or configuring Claude or Gemini CLIs, changing provider models,
  adding native Gemini surfaces, changing the agent roster, or implementing
  Specs 041-046.
- Replacing the affected-surface registry, changing CI job IDs, or weakening
  conditional internal execution merely to make every job run.
- Introducing a general Python application dependency manager, lockfile, hash
  policy, or runtime dependency contract beyond the three CI validation
  packages.
- Treating artifact retention as archival preservation or changing repository
  default retention settings.
- Rewriting historical run evidence, previous Task outcomes, dated audit
  observations, or Current research facts to make this tranche appear
  complete.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| GCQE-000 | Settled-ledger admission prerequisite and reciprocal Spec 039 planning activation | None | Approved Spec 039 design, prerequisite commit `cd726e0`, and rollback parent `cd726e0` | Plan-only lifecycle RED, unchanged protected ledger, exact six-path active pair, focused GREEN, logical activation commit |
| GCQE-001 | Portable GitOps non-regular fixture | GCQE-000 | Reproduce unqualified FIFO error or focused injected unsupported error | Focused unit tests and unqualified GitOps self-test PASS without weakening `RESOURCE_NOT_REGULAR` |
| GCQE-002 | Exact CI Python and explicit pre-commit contract | GCQE-001 | Observed remote missing-dependency FAIL and existing selector/topology evidence | Exact requirements file, Python 3.12 jobs, explicit all-files command, selector regression, contract validator PASS |
| GCQE-003 | Seven-day artifact evidence contract | GCQE-002 | Existing immutable Action/permission validator PASS and missing-retention RED | Retention fixture and repository validator PASS with `retention-days: 7` |
| GCQE-004 | Result vocabulary and agent completion guidance | GCQE-003 | Canonical quality owner and existing four-state runner behavior | Result tests plus all-files/formatter guidance assertions and consumer docs PASS |
| GCQE-005 | Aggregate integration and independent review | GCQE-004 | GCQE-001 through GCQE-004 logical commits | Focused, affected, staged, aggregate, unqualified all-files, security, requirements, and quality review evidence |
| GCQE-006 | Atomic lifecycle closure and clean-tree postflight | GCQE-005 | Whole-tranche reviews approved with no blocking findings | Exact terminal lifecycle package, explicit-ref lifecycle PASS, clean-tree repository-static postflight, remote lane DEFER |

### Task 0: GCQE-000 — Reciprocal Spec 039 planning activation

**Files:**

- Modify: `docs/03.specs/0039-github-ci-qa-evidence/spec.md`
- Create: `docs/03.specs/0039-github-ci-qa-evidence/plan.md`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/plan.md`
- Create: `docs/03.specs/0039-github-ci-qa-evidence/README.md#task-records`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: active Spec 039, PRD-0006, AD-0009, ADR-0017, program-lineage
  order 6, approved design commits `b69f829` and `56f19c2`, prerequisite
  commit `cd726e0`, the settled RIA ledger digest, and the reviewed
  post-settlement admission prerequisite.
- Produces: one active reciprocal Plan/Task pair, direct Spec backlinks, Stage
  04 index rows, shared progress handoff, and no implementation result. The
  protected 446-row ledger remains byte-identical.

- [x] **Step 1: Observe the Plan-only lifecycle RED.** Stage only this Plan and
  run:

  ```bash
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  ```

  Require exit `1`, rule `LIFECYCLE-CREATE`, Plan count `1`, and Task count
  `0`. Any different failure stops activation for diagnosis.

- [x] **Step 2: Add the reciprocal active Task.** Use the canonical Task
  profile, exact seven-column Task table, exact three-column lifecycle table,
  approval/safety fields, rollback parent `cd726e0`, and rows GCQE-000 through
  GCQE-006 in state `Queued` except GCQE-000 `In Progress`.

- [x] **Step 3: Complete reciprocal links and indexes.** Add Plan and Task
  backlinks to Spec 039 Traceability, add Active rows to both Stage 04
  indexes, and update the shared progress handoff from design review to
  approved planning activation. Do not add Plan/Task rows to the closed
  PRD-0005 migration snapshot.

- [x] **Step 4: Stage exactly the six activation paths and run focused
  GREEN.**

  ```bash
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  git diff --cached --check
  ```

- [x] **Step 5: Run the logical-commit gate.**

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  env TMPDIR=/tmp TMP=/tmp TEMP=/tmp pre-commit run --all-files
  git status --short
  git diff --check
  git diff --cached --check
  ```

  The temporary-directory override is permitted only for this pre-fix
  activation package and must be recorded as the Spec 039-owned limitation. The
  observed activation gate passed the repository aggregate, failed raw
  all-files only at the existing FIFO self-test limitation, and used
  `SKIP=strict-repository-quality pre-commit run --all-files` only after direct
  aggregate proof.

- [x] **Step 6: Commit the activation.**

  ```bash
  git commit -m "docs(execution): activate GitHub CI QA evidence"
  ```

  Activation commit
  `2ddfe4b7697e998b41d3125be94cdc4cee295388` changes only the six named
  paths. Its identity is recorded here only by this later evidence update,
  never predicted or embedded in the commit that created it.

### Task 1: GCQE-001 — Portable GitOps non-regular fixture

**Files:**

- Create: `tests/test_validate_gitops_change_set.py`
- Modify: `scripts/validate-gitops-change-set.py`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Design:**

Add `errno`, `Callable`, and `Literal` imports and one helper. Unsupported FIFO
creation falls back to a directory at the same resource path. A directory is
also non-regular, so `_render_path_root` must still raise
`RESOURCE_NOT_REGULAR`. Unexpected permission or I/O failures remain FAIL.

```python
FIFO_UNSUPPORTED_ERRNOS = frozenset(
    code
    for code in (
        getattr(errno, "ENOSYS", None),
        getattr(errno, "ENOTSUP", None),
        getattr(errno, "EOPNOTSUPP", None),
    )
    if code is not None
)


def _create_non_regular_fixture(
    path: Path,
    make_fifo: Callable[[Path], None] | None = getattr(os, "mkfifo", None),
) -> Literal["fifo", "directory-fallback"]:
    if make_fifo is not None:
        try:
            make_fifo(path)
            return "fifo"
        except OSError as exc:
            if exc.errno not in FIFO_UNSUPPORTED_ERRNOS:
                raise
    path.mkdir()
    return "directory-fallback"
```

- [x] **Step 1: Add focused tests before the helper exists.** Import the
  hyphenated script with `importlib.util` and add these exact behaviors:

  ```python
  def test_unsupported_fifo_uses_directory_fallback(self):
      def unsupported(_path: Path) -> None:
          raise OSError(errno.EOPNOTSUPP, "unsupported")

      with tempfile.TemporaryDirectory() as raw:
          target = Path(raw) / "resource.yaml"
          result = MODULE._create_non_regular_fixture(target, unsupported)
          self.assertEqual(result, "directory-fallback")
          self.assertTrue(target.is_dir())

  def test_unexpected_fifo_error_is_not_downgraded(self):
      def denied(_path: Path) -> None:
          raise OSError(errno.EACCES, "denied")

      with tempfile.TemporaryDirectory() as raw:
          with self.assertRaises(OSError) as raised:
              MODULE._create_non_regular_fixture(Path(raw) / "resource.yaml", denied)
          self.assertEqual(raised.exception.errno, errno.EACCES)
  ```

  Also cover the supported injected creator, explicit `None` fallback, and
  `_self_test_boundaries()` completion.

- [x] **Step 2: Run the focused RED.**

  ```bash
  python3 -m unittest tests/test_validate_gitops_change_set.py
  ```

  Require failure because `_create_non_regular_fixture` does not yet exist.

- [x] **Step 3: Implement the helper and replace the unconditional call.**

  ```python
  fixture_kind = _create_non_regular_fixture(non_regular / "pipe.yaml")
  if fixture_kind not in {"fifo", "directory-fallback"}:
      raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")
  _expect_self_test_error(
      "RESOURCE_NOT_REGULAR", lambda: _render_self_test_case(non_regular)
  )
  ```

- [x] **Step 4: Run focused GREEN and both production modes.**

  ```bash
  python3 -m unittest tests/test_validate_gitops_change_set.py
  python3 scripts/validate-gitops-change-set.py --self-test
  python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD
  ```

- [x] **Step 5: Update command/test inventories and run the package gate.**

  ```bash
  python3 scripts/validate-affected-surfaces.py --root .
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff --check
  git diff --cached --check
  ```

  The all-files command is intentionally unqualified. Require no FIFO error and
  inspect any formatter mutation before staging.

- [x] **Step 6: Commit the portable boundary.**

  ```bash
  git commit -m "fix(qa): make GitOps boundary fixture portable"
  ```

### Task 2: GCQE-002 — Exact CI Python and explicit pre-commit contract

**Files:**

- Create: `.github/requirements/ci-validation.txt`
- Create: `scripts/validate-ci-python-contract.py`
- Create: `tests/test_validate_ci_python_contract.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `tests/fixtures/validation-surfaces.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/90.references/data/tech-stack-version-inventory.md`
- Modify: `.github/ABOUT.md`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Dependency contract:**

```text
jsonschema==4.26.0
pre-commit==4.6.1
PyYAML==6.0.3
```

The technology inventory mirrors, but does not replace, that executable owner:

```yaml
ci_python: '3.12'
ci_python_dependencies:
  jsonschema: '4.26.0'
  pre-commit: '4.6.1'
  PyYAML: '6.0.3'
```

The validator exposes `--root` and `--self-test`, returns `0` only on exact
agreement, and emits these stable rule IDs:

| Rule ID | Rejected drift |
| --- | --- |
| `CI-PYTHON-PIN` | Missing, duplicate, loose, malformed, unexpected, or wrong package pin |
| `CI-PYTHON-INVENTORY` | Technology inventory version/package mismatch |
| `CI-PYTHON-VERSION` | A validation job does not select Python `3.12` |
| `CI-PYTHON-WORKFLOW` | A validation job omits the shared requirements install or uses a loose inline install |
| `CI-PRECOMMIT-ACTION` | `pre-commit/action` is present in workflow or inventory |
| `CI-PRECOMMIT-ALL-FILES` | Explicit all-files/show-diff execution is absent or altered |
| `CI-PRECOMMIT-HISTORY` | Pre-commit checkout does not use `fetch-depth: 0` |

Core parsing remains network-free:

```python
EXPECTED_PINS = {
    "jsonschema": "4.26.0",
    "pre-commit": "4.6.1",
    "pyyaml": "6.0.3",
}
EXPECTED_PYTHON = "3.12"
VALIDATION_JOBS = ("pre-commit", "repo-quality-static", "manifest-static")
INSTALL_COMMAND = (
    "python -m pip install --disable-pip-version-check "
    "--requirement .github/requirements/ci-validation.txt"
)
PRE_COMMIT_COMMAND = "pre-commit run --all-files --show-diff-on-failure"


def canonical_package_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()
```

- [x] **Step 1: Create the focused test module before the validator.** Build a
  temporary minimal repository with the exact requirements, inventory YAML
  fence, and three validation jobs. Add positive and one-mutation cases for
  every rule ID, plus a real-root pass test.

  ```python
  def test_pre_commit_action_is_rejected(self):
      root = self.make_valid_root()
      workflow = root / ".github/workflows/ci.yml"
      workflow.write_text(
          workflow.read_text(encoding="utf-8")
          + "\n# pre-commit/action@2c7b3805fd2a0fd8c1884dcaebf91fc102a13ecd\n",
          encoding="utf-8",
      )
      self.assert_rule(root, "CI-PRECOMMIT-ACTION")

  def test_requirement_must_be_exact(self):
      root = self.make_valid_root()
      requirements = root / ".github/requirements/ci-validation.txt"
      requirements.write_text(
          "jsonschema>=4.26.0\npre-commit==4.6.1\nPyYAML==6.0.3\n",
          encoding="utf-8",
      )
      self.assert_rule(root, "CI-PYTHON-PIN")
  ```

- [x] **Step 2: Run the focused RED.**

  ```bash
  python3 -m unittest tests/test_validate_ci_python_contract.py
  ```

  Require import/file failure because the validator does not yet exist.

- [x] **Step 3: Implement the fail-closed validator.** Require regular
  non-symlink inputs, exact three-line requirements, exact inventory mirror,
  exact Python version in all validation jobs, exactly one shared install step
  per job, no inline package names, no `pre-commit/action`, full pre-commit
  checkout history, and exactly one explicit all-files/show-diff command.

- [x] **Step 4: Run validator unit GREEN and self-test.**

  ```bash
  python3 -m unittest tests/test_validate_ci_python_contract.py
  python3 scripts/validate-ci-python-contract.py --self-test
  ```

- [x] **Step 5: Change the CI workflow and requirements owner.** Set every
  `actions/setup-python` step to:

  ```yaml
  with:
    python-version: '3.12'
  ```

  Set the pre-commit checkout to full history and replace
  `pre-commit/action` with:

  ```yaml
  - name: Install repository validation dependencies
    run: |
      python -m pip install --disable-pip-version-check --requirement .github/requirements/ci-validation.txt
  - name: Run all pre-commit hooks
    run: |
      pre-commit run --all-files --show-diff-on-failure
  ```

  Make `repo-quality-static` and `manifest-static` use the same install
  command. Keep job IDs, `needs`, selector expressions, timeouts, permissions,
  and `ci-summary` unchanged.

- [x] **Step 6: Mirror the exact contract in the technology inventory.** Remove
  the `pre-commit/action` Action row, add `ci_python` and
  `ci_python_dependencies`, and refresh the checked date/source note to
  2026-07-26 without changing unrelated versions.

- [x] **Step 7: Add the full-document selector regression.** Add
  `contract-bulk-document-escalation` to `selectionCases` with:

  ```json
  {
    "name": "contract-bulk-document-escalation",
    "lane": "ci",
    "paths": [
      "docs/99.templates/registry.json",
      "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
      "docs/98.archive/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md"
    ],
    "expected": {
      "validators": [
        "document-contract-registry",
        "links-and-owners",
        "markdown-profiles",
        "repository-quality"
      ],
      "ciJobs": ["pre-commit", "repo-quality-static"],
      "protectedLevel": "protected",
      "unmatchedPaths": []
    }
  }
  ```

  The archived path above exists at the activation baseline. Before locking the
  fixture, record the already observed selector result: the four document
  validators, two CI jobs, protected level, and empty unmatched-path set shown
  in the expected object.

- [x] **Step 8: Integrate self-test before production in the aggregate.**

  ```bash
  python3 "$ROOT_DIR/scripts/validate-ci-python-contract.py" --self-test
  python3 "$ROOT_DIR/scripts/validate-ci-python-contract.py" --root "$ROOT_DIR"
  ```

  Keep the existing workflow topology assertions. Update only assertions made
  stale by explicit setup, the new fixture count, and removal of
  `pre-commit/action`.

- [x] **Step 9: Update current GitHub and command inventories.** Replace
  `.github/ABOUT.md`'s deferred Spec 039 statement with the implemented
  full-history, pinned-dependency, explicit all-files path. Document the new
  validator and tests without duplicating package-version authority.

- [x] **Step 10: Run focused and aggregate GREEN.**

  ```bash
  python3 -m unittest tests/test_validate_ci_python_contract.py
  python3 scripts/validate-ci-python-contract.py --self-test
  python3 scripts/validate-ci-python-contract.py --root .
  python3 scripts/validate-affected-surfaces.py --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  python3 scripts/validate-github-actions-security.py --root .
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff --check
  git diff --cached --check
  ```

- [x] **Step 11: Commit the exact CI validation environment.**

  ```bash
  git commit -m "ci(qa): pin explicit pre-commit validation environment"
  ```

### Task 3: GCQE-003 — Seven-day artifact evidence contract

**Files:**

- Modify: `tests/fixtures/github-actions-security.json`
- Modify: `scripts/validate-github-actions-security.py`
- Modify: `.github/workflows/generate-changelog.yml`
- Modify: `.github/ABOUT.md`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Design:**

Add one exact fixture collection:

```json
"artifactRetentionCases": [
  {"name": "exact-seven", "retention": 7, "expected": []},
  {
    "name": "missing",
    "retention": null,
    "expected": ["upload-artifact retention-days must equal 7"]
  },
  {
    "name": "quoted-seven",
    "retention": "7",
    "expected": ["upload-artifact retention-days must equal 7"]
  },
  {
    "name": "wrong-number",
    "retention": 90,
    "expected": ["upload-artifact retention-days must equal 7"]
  }
]
```

Extend workflow validation with:

```python
ARTIFACT_RETENTION_DAYS = 7
UPLOAD_ARTIFACT_PREFIX = "actions/upload-artifact@"


def _validate_artifact_retention(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    for job_id, job in (data.get("jobs") or {}).items():
        if not isinstance(job, dict):
            continue
        for step_index, step in enumerate(job.get("steps") or [], start=1):
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if not isinstance(uses, str) or not uses.startswith(UPLOAD_ARTIFACT_PREFIX):
                continue
            options = step.get("with")
            retention = options.get("retention-days") if isinstance(options, dict) else None
            if (
                isinstance(retention, bool)
                or not isinstance(retention, int)
                or retention != ARTIFACT_RETENTION_DAYS
            ):
                step_path = Path(
                    f"{path.as_posix()}[job={job_id}][step={step_index}]"
                )
                errors.append(
                    _diagnostic(
                        step_path,
                        "upload-artifact retention-days must equal 7",
                    )
                )
    return errors
```

- [x] **Step 1: Add the four fixture cases before implementation.** Extend the
  JSON fixture only, then run:

  ```bash
  python3 scripts/validate-github-actions-security.py --self-test
  ```

  Require the exact fixture-shape RED.

- [x] **Step 2: Add the expected cases, fixture writer, and retention
  validator.** Compose `_validate_artifact_retention` with the existing
  permission and `uses` validators. Update the self-test fixture equality and
  message so all four cases are mandatory.

- [x] **Step 3: Run self-test GREEN while production still reports missing
  retention.**

  ```bash
  python3 scripts/validate-github-actions-security.py --self-test
  python3 scripts/validate-github-actions-security.py --root .
  ```

  Require self-test PASS and repository FAIL naming only the changelog upload
  step.

- [x] **Step 4: Set the workflow retention.**

  ```yaml
  with:
    name: changelog-${{ github.ref_name }}
    path: CHANGELOG.md
    if-no-files-found: error
    retention-days: 7
  ```

- [x] **Step 5: Update GitHub/script/test descriptions and run GREEN.**

  ```bash
  python3 scripts/validate-github-actions-security.py --self-test
  python3 scripts/validate-github-actions-security.py --root .
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff --check
  git diff --cached --check
  ```

- [x] **Step 6: Commit the retention contract.**

  ```bash
  git commit -m "ci(evidence): enforce seven-day changelog retention"
  ```

### Task 4: GCQE-004 — Result vocabulary and agent completion guidance

**Files:**

- Modify: `tests/test_run_validation_lane.py`
- Modify: `tests/test_post_validate_runner_result.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: `docs/00.agent-governance/rules/postflight-checklist.md`
- Modify: `docs/00.agent-governance/rules/git-workflow.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/ABOUT.md`
- Modify: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Authority split:**

- `quality-standards.md` defines lanes, four result states, command order,
  completion evidence, and formatter-review semantics.
- Postflight, Git workflow, PR template, GitHub hub, and the operations guide
  link to that owner and state only role-specific actions.
- The runner continues to emit all four states. The post-validate result helper
  continues to accept exactly one PASS and reject every competing state.

- [x] **Step 1: Extend focused result tests.** Parse all four states:

  ```python
  r"^\[(PASS|SKIP|FAIL|DEFER)\] ([^ ]+) "
  ```

  Add a remote/live contract case proving `run_selected` emits one DEFER,
  invokes no subprocess, and exits `0`. Add `defer`, `fail`,
  `pass-plus-defer`, and `pass-plus-fail` cases to
  `test_requires_one_exact_pass_and_no_competing_status`.

- [x] **Step 2: Run focused result tests.**

  ```bash
  python3 -m unittest \
    tests/test_run_validation_lane.py \
    tests/test_post_validate_runner_result.py \
    tests/test_provider_post_validate_hook.py
  ```

  Existing behavior may already pass; record that as regression evidence, not
  as a newly implemented result-state claim.

- [x] **Step 3: Add governance assertions before prose.** Extend the aggregate
  to require these exact consumer invariants:

  - `quality-standards.md` contains
    ``pre-commit run --all-files`` and an ordered formatter-review/rerun rule.
  - `postflight-checklist.md` contains checked items for the all-files command,
    formatter/status inspection, and rerun after mutation.
  - `git-workflow.md` requires the all-files command before each logical commit
    and before branch finish.
  - `PULL_REQUEST_TEMPLATE.md` asks for the all-files result and explicit
    PASS/SKIP/FAIL/DEFER lane classification.

  Run `bash scripts/validate-repo-quality-gates.sh .` and require RED naming
  the missing phrases.

- [x] **Step 4: Implement the canonical completion sequence.** In
  `quality-standards.md`, require:

  1. focused tests while implementing;
  2. affected validators for changed paths;
  3. staged hooks for the exact index;
  4. relevant direct tests and repository aggregate;
  5. `pre-commit run --all-files`;
  6. `git status --short`, unstaged diff, and cached diff formatter review;
  7. affected/staged/all-files rerun after any mutation; and
  8. final diff checks and lane-by-lane handoff.

- [x] **Step 5: Update each consumer in its own role.** Keep README-style
  routing concise, replace the PR template's vague “Relevant pre-commit hooks”
  line, remove `.github/ABOUT.md`'s stale future Spec 039 claim, and make the
  operations guide reproduce the exact local commands without redefining the
  result vocabulary.

- [x] **Step 6: Run focused and aggregate GREEN.**

  ```bash
  python3 -m unittest \
    tests/test_run_validation_lane.py \
    tests/test_post_validate_runner_result.py \
    tests/test_provider_post_validate_hook.py
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff --check
  git diff --cached --check
  ```

- [x] **Step 7: Commit the completion evidence contract.**

  ```bash
  git commit -m "docs(qa): enforce all-files completion evidence"
  ```

### Task 5: GCQE-005 — Aggregate integration and independent review

**Files:**

- Modify only files named by concrete review findings within Spec 039 scope.
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Run focused test suites.**

  ```bash
  python3 -m unittest tests/test_validate_gitops_change_set.py
  python3 -m unittest tests/test_validate_ci_python_contract.py
  python3 -m unittest \
    tests/test_run_validation_lane.py \
    tests/test_post_validate_runner_result.py \
    tests/test_provider_post_validate_hook.py
  python3 scripts/validate-github-actions-security.py --self-test
  python3 scripts/validate-github-actions-security.py --root .
  python3 scripts/validate-affected-surfaces.py --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  ```

- [x] **Step 2: Run direct CI/GitOps production checks.**

  ```bash
  python3 scripts/validate-ci-python-contract.py --self-test
  python3 scripts/validate-ci-python-contract.py --root .
  python3 scripts/validate-gitops-change-set.py --self-test
  python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  ```

- [x] **Step 3: Run affected, staged, aggregate, and unqualified all-files
  lanes.** Use NUL-delimited changed paths for the affected runner, stage only
  the current logical evidence update, and then run:

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff
  git diff --cached
  git diff --check
  git diff --cached --check
  ```

  Require no FIFO error, no skipped required hook, no unreviewed formatter
  mutation, and no result-state substitution.

- [x] **Step 4: Dispatch an independent requirements reviewer.** The reviewer
  checks every VAL-GCQE criterion, Plan scope, exact pins, full-history
  behavior, selector escalation, result vocabulary, Task evidence, and remote
  DEFER boundary. A non-compliant verdict blocks closure.

- [x] **Step 5: Dispatch an independent quality/security reviewer.** The
  reviewer checks fail-closed parsing, symlink/regular-file boundaries,
  exception handling, workflow permissions, Action identity, artifact
  retention, shell injection, dependency ownership, tests, and rollback. Any
  Critical or Important finding blocks closure.

- [x] **Step 6: Fix findings test-first and obtain fresh re-review.** Commit
  each bounded remediation as its own logical unit with a Conventional Commit
  message naming the concrete reviewer rule or affected contract. Do not create
  a remediation commit when there is no finding.

- [x] **Step 7: Record observed evidence only.** Update the Task and progress
  ledger with exact commands, results, reviewer identities/dispositions,
  limitations, rollback commits, residual risk, and next owner. Keep hosted CI
  post-change evidence DEFER.

### Task 6: GCQE-006 — Atomic lifecycle closure and clean-tree postflight

**Files:**

- Modify: `docs/03.specs/0039-github-ci-qa-evidence/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/plan.md`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/plan.md`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/README.md#task-records`
- Modify: `docs/03.specs/0039-github-ci-qa-evidence/README.md#task-records`
- Modify: `docs/99.templates/registry.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Prepare the exact terminal lifecycle proposal.** Change Spec,
  Plan, Task, three indexes, and PRD-0006 program-lineage Spec 039 state from
  `active` to `done`; update the reciprocal Task and progress with observed
  evidence while leaving the settled migration snapshot byte-identical. Keep
  Spec 040 `active`.

- [x] **Step 2: Run staged lifecycle and strict document gates.**

  ```bash
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  git diff --cached --check
  ```

- [x] **Step 3: Obtain final whole-tranche requirements and quality approval.**
  Reviewers `/root/gcqe006_final_requirements` and
  `/root/gcqe006_final_quality` returned `REQUIREMENTS COMPLIANT` and `QUALITY
  APPROVED`, with no findings against corrected staged patch digest
  `58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`
  after the sole invalid explicit-ref finding was closed.

- [x] **Step 4: Run the terminal commit gate.**

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git status --short
  git diff
  git diff --cached
  git diff --check
  git diff --cached --check
  ```

- [x] **Step 5: Commit the lifecycle closure.**

  ```bash
  git commit -m "docs(sdlc): close GitHub CI and QA evidence tranche"
  ```

  Observed closure commit:
  `e1d1e910840337327a557ab4b84e86f8fced11d6`. Its diff contains exactly the
  eight paths listed for Task 6. No hosted rerun is claimed.

- [x] **Step 6: Run clean-tree postflight from the activation commit to the
  closure commit.** The executor recorded both exact identities and invoked
  `validate-document-lifecycle.py --mode explicit-ref` with raw 40-hex OIDs
  through `--from-ref` and `--to-ref`. The `git-sha1:<oid>` evidence-label
  form was not passed to the CLI.

  ```bash
  python3 scripts/validate-document-lifecycle.py \
    --root . \
    --mode explicit-ref \
    --from-ref 2ddfe4b7697e998b41d3125be94cdc4cee295388 \
    --to-ref e1d1e910840337327a557ab4b84e86f8fced11d6
  ```

  Run the remaining clean-tree commands:

  ```bash
  python3 scripts/validate-ci-python-contract.py --root .
  python3 scripts/validate-github-actions-security.py --root .
  python3 scripts/validate-gitops-change-set.py --self-test
  bash scripts/validate-repo-quality-gates.sh .
  pre-commit run --all-files
  git diff --check
  git status --short
  ```

  The explicit-ref lifecycle command passed. CI Python production reported
  `3` jobs / `3` pins; GitHub Actions security, the GitOps self-test, and the
  repository aggregate passed. `pre-commit run --all-files` passed every
  applicable hook, with Dockerfile lint recorded as a no-file `SKIP`.
  `git status`, diff inspection, and diff-check inspection were clean. Remote
  hosted CI remains `DEFER`, with run `29982910320` retained only as
  historical FAIL evidence for its older SHA.

## Verification Plan

| Lane | Command or evidence | Required outcome |
| --- | --- | --- |
| FIFO unit | `python3 -m unittest tests/test_validate_gitops_change_set.py` | Supported, unsupported, absent, and unexpected FIFO branches are covered. |
| GitOps self-test | `python3 scripts/validate-gitops-change-set.py --self-test` | PASS without temporary-directory override or uncaught FIFO error. |
| CI contract unit | `python3 -m unittest tests/test_validate_ci_python_contract.py` | Every stable rule ID has a hostile case and the valid fixture passes. |
| CI contract self-test | `python3 scripts/validate-ci-python-contract.py --self-test` | PASS from an isolated exact fixture. |
| CI contract production | `python3 scripts/validate-ci-python-contract.py --root .` | Requirements, workflow, and inventory agree exactly. |
| Selector | `python3 scripts/validate-affected-surfaces.py --self-test` and `--root .` | Contract/bulk document paths select document validators, pre-commit, and repo-quality. |
| Actions security | `python3 scripts/validate-github-actions-security.py --self-test` and `--root .` | Full-SHA identity, least privilege, and exact seven-day retention PASS. |
| Result semantics | Runner/result/provider-hook unittests | PASS/SKIP/FAIL/DEFER remain distinct; one required PASS cannot be forged. |
| Document lifecycle | staged activation/closure and explicit-ref postflight | Reciprocal active creation and atomic terminal closure PASS. |
| Strict docs | registry, Markdown-profile, and link/owner strict commands | No uncovered route, profile drift, broken owner/link, or reciprocal-lineage error. |
| Repository aggregate | `bash scripts/validate-repo-quality-gates.sh .` | Exact repository PASS marker and zero failure. |
| All files | `pre-commit run --all-files` | Every applicable hook passes without `/tmp` override or unreviewed formatter mutation. |
| Hosted CI | Existing run `29982910320`; no post-change dispatch | Historical SHA remains FAIL; current branch remains DEFER until separately approved. |
| Live runtime | No command authorized | DEFER; no Kubernetes, Vault, ESO, Argo CD, provider, credential, or deployment claim. |

Per logical commit, the owning Task records the focused RED, focused GREEN,
affected/staged scope, aggregate, all-files, formatter review, both diff checks,
review disposition, rollback commit, and residual risk. A later command cannot
retroactively convert an earlier failure or skipped lane into PASS.

### Legacy Task verification evidence

Activation evidence contains the intentional creation RED:

```text
FAIL LIFECYCLE-CREATE
docs/03.specs/0039-github-ci-qa-evidence/plan.md
expected="exactly one Plan and one Task creation in the same proposal state 'active'"
observed="Plan count 1, Task count 0"
base_mode="staged"
```

The exact six-path reciprocal proposal passes staged lifecycle, registry
self-test and strict mode, strict Markdown profiles, strict cross-document
validation, settled RIA validation, cached diff check, and repository
aggregate. Activation commit
`2ddfe4b7697e998b41d3125be94cdc4cee295388` contains exactly those six paths,
and the post-commit repository aggregate passes at that HEAD. GCQE-001 through
GCQE-004 are complete in `d0d788d`, `b2bf4a8`, `bca57ae`, and `8621e88`.
GCQE-005 first reproduced the closed-runner classifier failure rather than
substituting an ambient aggregate PASS. Remediation `b329016` made Gitleaks
available without broadening the closed PATH, and reviewer
`/root/gcqe_005_remediation_reviewer` then returned CHANGES REQUESTED for an
Important effective-execute-class gap. Follow-up `7b536d1` corrected that gap;
fresh remediation re-review is APPROVED. The current staged integration passed
focused, direct, strict, 30-path cumulative affected, staged, aggregate, and
unqualified all-files lanes with no formatter mutation. Requirements reviewer
`/root/gcqe_005_requirements_review` returned REQUIREMENTS COMPLIANT with no
finding; quality/security reviewer `/root/gcqe_005_quality_security_review`
returned QUALITY APPROVED with no finding. Both matched review package SHA-256
`f4d50ec45e7d977b22c55cd18f6d8e56bc6cf7436713980d1b1f09f38632cb38`.
GCQE-005 is Done. GCQE-006 has prepared the refreshed exact eight-file terminal
proposal at base HEAD `39e6150a6f7a79b710d0e2cd7bc2dee8349f871a`.
The review history remains explicit:

- First-pass requirements reviewer
  `/root/gcqe006_terminal_requirements_review` returned `NOT COMPLIANT`, and
  rapid quality reviewer `/root/gcqe006_terminal_quality_rapid` returned
  `CHANGES REQUESTED`, because the rollback chain omitted reviewed commits.
- Original quality reviewer `/root/gcqe006_terminal_quality_review` returned
  `QUALITY NOT APPROVED` because the old active-corpus frontier made the
  aggregate fail against the staged advanced proposal.
- Commit `b5c3eea` remediated that frontier and received scoped frontier
  requirements/quality approval. Its first staged full-class run then exposed
  three old-state production assertions. The first test-compat review also
  raised a P1 because current/advanced expectations were not bound to exact
  index object identities.
- Commit `39e6150` remediated the three assertions and index-OID P1. Fresh
  test-compat reviewers returned `REQUIREMENTS COMPLIANT` and `QUALITY
  APPROVED`; these are scoped compatibility verdicts, not terminal approval.
- Final whole-tranche reviewer `/root/gcqe006_final_requirements` returned
  `REQUIREMENTS NOT COMPLIANT`, and reviewer
  `/root/gcqe006_final_quality` returned `QUALITY NOT APPROVED`, solely because
  Plan Task 6 Step 6 used invalid explicit-ref flag names and passed
  `git-sha1:` evidence labels where the CLI requires raw refs or OIDs. Step 6
  now uses `--from-ref` and `--to-ref`, fixes the activation side to the exact
  raw 40-hex OID, and requires replacement of the closure placeholder with its
  observed raw 40-hex OID before execution.
- Fresh whole-tranche reviewer `/root/gcqe006_final_requirements` returned
  `REQUIREMENTS COMPLIANT`, and reviewer `/root/gcqe006_final_quality`
  returned `QUALITY APPROVED`, with no findings against corrected staged patch
  digest
  `58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
  The sole invalid explicit-ref finding is closed and Step 3 is complete.

The refreshed proposal passed the residue class `46/46`, full module `84/84`,
residue self-test `22`, exact advanced production counts, repository aggregate
with `[PASS] repository quality gates passed`, lifecycle self-test `668`,
staged lifecycle, registry self-test/strict, strict Markdown, strict
links/owners, and both diff checks. Fresh whole-tranche terminal reviews are
approved. The terminal repository quality gate and unqualified all-files
pre-commit passed with every applicable hook green, Dockerfile lint skipped
for no files, no formatter mutation, exactly eight staged paths, no unstaged
changes, and both diff checks green. Step 5 produced exact eight-path closure
commit `e1d1e910840337327a557ab4b84e86f8fced11d6`. Step 6 passed explicit-ref
lifecycle from raw activation OID
`2ddfe4b7697e998b41d3125be94cdc4cee295388` to that raw closure OID, CI Python
production at `3` jobs / `3` pins, GitHub Actions security, GitOps self-test,
the clean-tree repository aggregate, and every applicable all-files hook.
Dockerfile lint remained a no-file `SKIP`; status, diff, and diff-check
inspection were clean. Hosted run `29982910320` remains historical FAIL for
its exact older SHA, while the current branch hosted, provider, and live lanes
remain `DEFER`. This evidence update does not identify or claim its own commit.
## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Directory fallback accidentally weakens non-regular coverage | Assert `RESOURCE_NOT_REGULAR` for both FIFO and directory fixture branches; re-raise unexpected errors. | GCQE-001 |
| Python version or package pin becomes duplicated | Requirements file is executable SSoT; technology inventory is validated mirror; inline installs are rejected. | GCQE-002 |
| Removing `pre-commit/action` changes cache behavior | Accept loss of transitive Action cache as a deliberate simplification; explicit command correctness and dependency availability take priority. | GCQE-002 |
| Full-history checkout increases CI time | Limit `fetch-depth: 0` to jobs that require history; retain job timeouts and affected internal selection. | GCQE-002 |
| Exact package pins age | Inventory records observation date; Dependabot/manual refresh opens a later bounded change with the same validator. | platform |
| New selector fixture misstates current path ownership | Verify the chosen archived path exists and inspect actual selector output before locking expected values. | GCQE-002 |
| Artifact retention rule affects future unrelated uploads | Apply the exact seven-day rule to every upload-artifact step; a different consumer duration requires a named decision and validator update. | GCQE-003 |
| Guidance is duplicated across consumers | Keep definitions in quality standards and enforce links/action-only wording elsewhere. | GCQE-004 |
| Formatter mutates files after tests | Inspect status and both diffs, restage intentionally, and rerun affected/staged/all-files checks. | every package |
| Local PASS is mistaken for hosted PASS | Keep run identity/SHA in Task; hosted post-change lane stays DEFER without separately approved push. | GCQE-005/006 |
| Terminal files claim their own unknown commit SHA | Keep only pre-commit evidence in the closure commit; add its observed SHA in a later evidence update, whose own commit remains unidentified and unclaimed. | GCQE-006 |
| Rollback removes enforcement before consumers | Revert newest consumer/guidance package first, then retention, CI contract, FIFO helper, and activation last; rerun aggregate after each rollback. | platform |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: Spec 039 and its reciprocal Stage 04 Plan/Task/index
  lineage; the settled migration snapshot is read-only validation input;
  `.github/workflows/ci.yml`,
  `.github/workflows/generate-changelog.yml`,
  `.github/requirements/ci-validation.txt`, `.github/ABOUT.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`; the focused CI, GitOps, Actions,
  affected-surface, aggregate, runner, hook-result, unit-test, fixture,
  governance, operations-guide, script/test inventory, technology-inventory,
  and shared progress paths named in the Plan.
- **Forbidden Paths**: Provider gateways/adapters/models/roster; `.gemini/**`;
  Specs 040-046 implementation; Kubernetes/GitOps desired-state changes;
  infrastructure, Vault, ESO, Argo CD, deployment, release publication,
  branch-protection, credentials, secret values, ignored `_workspace`
  children, auth files, kubeconfigs, tokens, and shell history.
- **Approval Required**: Dependency installation, push, workflow dispatch,
  GitHub setting mutation, merge, publication, live command, credential access,
  secret handling, or expansion outside the exact Spec 039 paths requires
  separate explicit human approval.
- **Static Validation**: Focused unit tests; GitOps, CI-contract,
  affected-surface, Actions-security self-test and production modes; staged and
  explicit-ref lifecycle; strict registry/Markdown/link checks; repository
  aggregate; unqualified all-files pre-commit; formatter/status review; both
  diff checks.
- **Live Validation**: DEFER. No post-change hosted GitHub Actions, provider,
  Kubernetes, Vault, ESO, Argo CD, cloud, deployment, or credential result is
  authorized by this Task.
- **Secret / Vault Handling**: Do not open, print, copy, hash, or report secret
  values. Diagnostics and evidence contain only stable rule IDs,
  repository-relative paths, bounded metadata, commit identities, and public
  run identifiers.
- **Rollback Plan**: Revert closure commit
  `e1d1e910840337327a557ab4b84e86f8fced11d6` first, then
  `39e6150`, `b5c3eea`, `096c5c4`, `aaee364`, `7b536d1`, `b329016`,
  `8621e88`, `bca57ae`, `b2bf4a8`, `d0d788d`, `4aaaa4b`, `50d04e4`,
  `9bb74ce`, and activation `2ddfe4b` last. This is the complete exact
  newest-first chain. Rerun focused and aggregate checks after every revert.
  Do not rewrite shared history or use destructive reset/clean operations.
- **Evidence Location**: This Task, the reciprocal Plan, reviewed logical
  commits, exact test/fixture files, repository-static command output,
  the byte-verified settled migration snapshot, and shared progress ledger.
  Temporary logs, subagent scratch, and hosted results for other SHAs are not
  current closure evidence.
## Completion Criteria

- The reciprocal Spec 039 Plan/Task pair is active before implementation and
  terminally done only after all work packages and independent reviews finish.
- The unqualified GitOps self-test and unqualified all-files pre-commit pass on
  the current filesystem without an uncaught FIFO error.
- `.github/requirements/ci-validation.txt` contains exactly the three approved
  exact pins; all validation jobs use Python 3.12 and that file.
- `pre-commit/action` is absent from workflows and technology inventory;
  pre-commit runs explicitly with all-files/show-diff and full checkout history.
- Existing CI job IDs, supported-event entry, affected selection,
  `ci-summary if: always()`, permissions, and full-SHA Action identities remain
  valid.
- Contract/bulk document paths have deterministic fixture evidence selecting
  the full repository-quality document gate.
- Every upload-artifact step declares integer `retention-days: 7`, with
  positive and hostile self-test evidence.
- Result tests and guidance preserve distinct PASS, SKIP, FAIL, and DEFER
  semantics and require all-files plus formatter review before commit/finish.
- Focused, affected, staged, direct production, strict document, aggregate,
  all-files, diff, review, terminal lifecycle, and clean-tree postflight
  evidence are recorded in the Task.
- No credentials or secret values were accessed, no live mutation occurred,
  and current hosted CI remains DEFER unless separately authorized and
  observed.
- Logical commits are independently reversible and the worktree is clean at
  handoff.

## Traceability

- **Spec**:
  [GitHub CI and QA Evidence](spec.md)
- **Task**:
  [Task: GitHub CI and QA Evidence](README.md#task-records)
- **PRD**:
  [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **AD**:
  [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-GCQE-001](spec.md#success-criteria--verification-plan) | GCQE-002, GCQE-005, GCQE-006 | [Workflow entry and aggregate evidence](tasks/tsk-0003-gcqe-002.md) |
| N/A — VAL-GCQE-002 shares the Spec 039 source linked in VAL-GCQE-001 | GCQE-002, GCQE-005 | N/A — the paired Task is linked in VAL-GCQE-001 |
| N/A — VAL-GCQE-003 shares the Spec 039 source linked in VAL-GCQE-001 | GCQE-002, GCQE-003, GCQE-005 | N/A — the paired Task is linked in VAL-GCQE-001 |
| N/A — VAL-GCQE-004 shares the Spec 039 source linked in VAL-GCQE-001 | GCQE-001, GCQE-005 | N/A — the paired Task is linked in VAL-GCQE-001 |
| N/A — VAL-GCQE-005 shares the Spec 039 source linked in VAL-GCQE-001 | GCQE-004, GCQE-005 | N/A — the paired Task is linked in VAL-GCQE-001 |
| N/A — VAL-GCQE-006 shares the Spec 039 source linked in VAL-GCQE-001 | GCQE-004, GCQE-005, GCQE-006 | N/A — the paired Task is linked in VAL-GCQE-001 |

### Legacy Task traceability

- **Plan**:
  [GitHub CI and QA Evidence Implementation Plan](plan.md)
- **Spec**:
  [Spec 039](spec.md)
- **Predecessor Task**:
  [Reference Information Architecture Task](../0038-reference-information-architecture/README.md)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [GCQE-000](plan.md#task-0-gcqe-000--reciprocal-spec-039-planning-activation) | Done — Plan-only lifecycle RED, prerequisite `cd726e0`, exact-six reciprocal GREEN, activation `2ddfe4b`, and post-commit aggregate PASS observed. | Rule `LIFECYCLE-CREATE`, Plan 1/Task 0, rollback parent `cd726e0`, staged lifecycle/registry/profile/link/RIA PASS, exact-six commit `2ddfe4b`, and HEAD aggregate PASS. |
| [VAL-GCQE-004](spec.md#success-criteria--verification-plan) | Done in `d0d788d`. | Portable non-regular fixture, exact diagnostic, focused six-test GREEN, and fresh review approval observed. |
| N/A — GCQE-002 shares the Plan linked in GCQE-000 | Done in `b2bf4a8`. | Exact CI Python owner/workflow/selector contract, final 12-test GREEN, aggregate/all-files PASS, and fresh review approval observed. |
| N/A — GCQE-003 shares the Plan linked in GCQE-000 | Done in `bca57ae`. | Exact seven-day retention, hostile-shape/case regressions, aggregate/all-files PASS, and final fresh review approval observed. |
| N/A — GCQE-004 shares the Plan linked in GCQE-000 | Done in `8621e88`. | Four-state and eight-step completion evidence, strict/aggregate/all-files PASS, and independent approval observed. |
| N/A — GCQE-005 shares the Plan linked in GCQE-000 | Done through `7b536d1` plus the reviewed staged evidence proposal. | Initial classifier and index-boundary failures, remediation `b329016`, reviewer CHANGES REQUESTED, follow-up `7b536d1`, fresh remediation APPROVED, final cumulative repository-static PASS, REQUIREMENTS COMPLIANT, and QUALITY APPROVED are observed. |
| N/A — GCQE-006 shares the Plan linked in GCQE-000 | Done through Step 6. | Exact eight-file closure `e1d1e910840337327a557ab4b84e86f8fced11d6` retains advanced residue `46/84/22`, exact `0/0` active and `4/2` terminal controls, aggregate, lifecycle `668`, staged/strict document gates, terminal repository quality/all-files gates, and diff checks. Rollback, old-frontier, three old-state assertion, index-OID P1, and sole invalid explicit-ref findings remain recorded and remediated. Reviewers `/root/gcqe006_final_requirements` and `/root/gcqe006_final_quality` returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings against digest `58640a0d…`. Explicit-ref lifecycle passed from activation `2ddfe4b7697e998b41d3125be94cdc4cee295388`; CI Python `3` jobs / `3` pins, Actions security, GitOps self-test, clean-tree aggregate, and applicable all-files hooks passed; Dockerfile lint was a no-file `SKIP`; status/diff/diff-check inspection was clean. Spec 040 remains active, the settled snapshot is unchanged, and current hosted/provider/live remains `DEFER`. |
