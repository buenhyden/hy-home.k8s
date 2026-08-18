---
title: 'Agent Quality Standards (March 2026)'
type: governance/reference
status: active
owner: platform
updated: 2026-07-30
---

# Agent Quality Standards (March 2026)

## Overview

Quality gates for governance and execution alignment.

### Required Quality Dimensions

- Accuracy: policy text matches actual workspace behavior.
- Concision: avoid repetitive or generic instructions.
- Actionability: every rule implies a concrete action.
- Consistency: no conflicts across bootstrap, persona, scope, and provider docs.

## Authority Boundary

### Coverage Applicability

- Future testable application code should target at least 90% line and branch coverage where a language-specific test framework and coverage tool exist.
- Current Bash/YAML/Markdown infrastructure work uses validation-matrix coverage instead of fake numeric code coverage.
- The validation matrix for this repository includes repository quality gates, GitOps structure checks, Kubernetes manifest syntax, static infrastructure contracts, secret handling scans, shell syntax, CI workflow checks, README/template checks, and explicit live-check limitations.
- Repo-static, CI/toolchain, and live runtime readiness are separate evidence lanes. Do not present repository or CI validation as proof of live k3d, ArgoCD, Vault, ESO, deployment, or external-service health unless the matching live check was approved and run.
- CI/static validation and QA evidence must distinguish optional-tool skips from successful
  full coverage. A fallback path or skipped optional tool is not the same as
  complete tool coverage.
- GitHub Actions is the provider-agnostic remote QA gate for this repository; it
  is not live deployment CD and must not be used as evidence of live runtime
  readiness without an approved live check.
- Adapter parity is validated as role parity plus evidence, not identical
  metadata keys. Native Claude/Codex/Gemini adapters and local/Antigravity
  adapters must preserve role, scope, guardrails, handoff, and postflight
  while using their surface-specific metadata. This static result is not
  provider discovery, policy loading, model resolution, permission, or
  execution evidence.
- PR verification must state which coverage lane applies: 90% code coverage for future testable application code, or validation-matrix coverage for current infrastructure artifacts.

## Governance Context

The affected-surface contract selects repository validators. This document is
the sole canonical owner of the local completion order, step IDs, lane and
result meanings, formatter completion rule, and handoff vocabulary. Preflight
defines expected lanes; workflows, checklists, inventories, and provider
adapters route here and must not redefine those semantics. CI,
provider-runtime, and live evidence remain separate authorities.

## Current Contract

### Validation Lane Contract

`docs/00.agent-governance/contracts/validation-surfaces.json` owns path-to-
validator and local/CI selection. Its affected lane passes every existing
Markdown edit, including untracked files, to the exact document validators;
CI and lifecycle Git ranges disable rename detection so both old and new paths
retain their gates. This document owns how agents name and report the resulting
lanes:

- **affected**: validators selected for normalized changed paths during work
  through `scripts/run-validation-lane.py --lane affected`. Evidence names the
  input path set and every selected validator. An empty path set or a validator
  with no applicable files is `SKIP`, not `PASS`.
- **staged**: contract-selected validators run through
  `scripts/run-validation-lane.py --lane staged` for the exact staged path set,
  followed separately by plain `pre-commit run` against the exact Git index.
  Evidence records both results and identifies the index scope. An affected or
  all-files runner invocation, a working-tree check, or either staged command
  alone cannot substitute for this lane.
- **all-files**: completion requires `pre-commit run --all-files`, which runs
  all applicable file hooks plus the repository quality gate. A
  `scripts/run-validation-lane.py --lane all-files` result is supplemental
  repository-static validator evidence, not a substitute for this command or
  for staged evidence. This lane does not execute or prove `commit-msg` or
  explicit `manual` stages.
- **message/manual**: commit-message and explicit manual-stage checks. Report
  each applicable check separately; do not infer it from `--all-files`.
- **ci**: jobs deterministically selected from the affected-surface contract.
  Local selector, workflow syntax, and static Action checks are repo-static
  evidence only; a remote GitHub run needs its own check URL or run identity.
- **remote/live**: provider discovery/consumption, remote execution, and
  operator-approved Kubernetes, Argo CD, Vault, ESO, cloud, or deployment
  verification. Without direct authorized evidence this lane is `DEFER`.

### Result Vocabulary

- `PASS`: the named command or check ran over the stated scope and satisfied
  its acceptance condition.
- `SKIP`: the lane was selected but had no applicable files, or an explicitly
  optional tool was unavailable; record the reason and any independent
  fallback result.
- `FAIL`: the command ran or input validation stopped execution and the stated
  acceptance condition was not met.
- `DEFER`: the lane requires unavailable authority, environment, provider, or
  remote/live evidence. `DEFER` is a visible limitation, never a pass.

### Local Validator Resource Limits

Every repository-static child selected by the validation-surface contract runs
through `scripts/run-validation-lane.py` with one reviewed finite envelope:

- 1,200 seconds maximum execution time per child;
- 4 MiB maximum retained stdout and 1 MiB maximum retained stderr per child;
- 2 seconds total cleanup time under one monotonic deadline; and
- 64 KiB maximum read chunks with concurrent stdout/stderr draining.

The runner starts each child in its own session/process group. Timeout, either
pipe overflow, pipe failure, or pipes held by descendants after the direct
leader exits is `FAIL`: the runner kills the process group and direct leader,
closes both read ends, and reaps the leader within the single cleanup deadline.
Result lines expose only observed byte counts, SHA-256 digests, completion
flags, the stable boundary status, and the return code; child payload is never
copied into evidence. Repository quality still requires return code zero and
exactly one complete `[PASS] repository quality gates passed` stdout line
within the bounded stdout envelope. These limits govern local child execution
only and are not hosted CI, provider-runtime, remote, or live evidence.

### Canonical Completion Sequence

Every repo-changing task follows this ordered completion sequence. Consumers
must link here for the shared order and result meanings rather than redefining
them.

1. **targeted**: Run the smallest focused checks while implementing and record
   their command, scope, and result.
2. **affected**: Run the affected runner for every normalized changed path and
   record the selected validators and their results.
3. **staged**: Stage the exact logical file set, run the staged runner for the
   exact staged path set, then run plain `pre-commit run` against that exact Git
   index; record both results.
4. **tests**: Run the relevant direct test suites and repository aggregate,
   preserving each command's separate result.
5. **all-files**: Run `pre-commit run --all-files`; only that command qualifies
   as all-files completion evidence.
6. **formatter-review**: Review `git status --short`, `git diff`, and
   `git diff --cached` for every formatter mutation, including files outside
   the initial target set.
7. **rerun**: If any formatter changes any file, treat the mutating invocation
   and earlier affected, staged, and all-files results as non-completion
   evidence; review the change, restage the exact logical set, and rerun
   affected, staged, and all-files validation until the final results are
   clean.
8. **diff-checks**: Run `git diff --check` and
   `git diff --cached --check`, confirm the final staged and unstaged scope, and
   record all eight ordered step results in the handoff.

Prettier remains dormant and decision-gated. Its configuration files are
routed validation inputs, but no current hook, runner, aggregate, or CI
contract enforces Prettier; do not report Prettier coverage without a separate
approved activation.

### CI Validation Supply-Chain Contract

The Linux/CPython 3.12 validation lane separates dependency intent from its
resolved artifact:

- `.github/requirements/ci-validation.in` owns only the exact direct pins.
- `.github/requirements/ci-validation.txt` is generated with Python 3.12,
  contains every direct and transitive dependency as an exact `==` pin, and
  carries one or more SHA-256 hashes for every package.
- Every validation job uses exactly
  `python -m pip install --disable-pip-version-check --only-binary :all: --require-hashes --requirement .github/requirements/ci-validation.txt`.
  Hash checking is all-or-nothing and source distributions are excluded,
  following [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/).
- The inventory mirrors the lock digest, resolved package count, generation lane,
  and direct-input/lock paths; the CI validator's reviewed runtime digest is the
  independent authority. Refresh both only through the reviewed lock-refresh
  change that updates the resolved lock and inventory atomically. This artifact is evidence for the Linux/CPython
  3.12 CI lane only; it must not be represented as a portable lock for another
  operating system or Python version.

Every non-local repository in `.pre-commit-config.yaml` uses a unique full
40-character commit. Update hooks with `pre-commit autoupdate --freeze`, retain
the emitted `# frozen: <tag>` provenance, reconcile the exact commit and source
tag maps in the technology inventory, and rerun the CI Python contract before
accepting the change. This follows the official
[pre-commit autoupdate options](https://pre-commit.com/#pre-commit-autoupdate-options).
The `local` repository is the only rev-exempt entry.

Frozen remote-hook repository commits and source tags are PASS provenance
evidence. Their transitive hook environments and cold offline replay are DEFER:
they require a separately owned immutable hook-artifact program and are not
claimed closed by the base CI Python lock.

### Handoff Evidence Contract

Every repo-changing agent handoff records the following fields in the owning
Task or approved evidence record. A field may say `none` or `DEFER` with a
reason, but it must not be silently omitted:

- scope and changed paths;
- acceptance IDs;
- commands and tool/version;
- the ordered `targeted`, `affected`, `staged`, `tests`, `all-files`,
  `formatter-review`, `rerun`, and `diff-checks` result for each step;
- per-lane `PASS`, `SKIP`, `FAIL`, or `DEFER` results;
- limitations;
- reviewer identity and review disposition;
- rollback commit(s) or bounded rollback procedure;
- residual risk; and
- next owner.

Static gateway, hook, or role-adapter presence proves only tracked repository
configuration. It does not prove that Claude, Codex, Gemini, or another native
runtime discovered, loaded, or enforced that adapter.

## Validation and Refresh

### Minimum Verification for Governance Updates

- Structure parity with expected governance tree.
- English-only check under `docs/00.agent-governance/`.
- Root shim link checks for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Affected-surface and provider-neutral role-semantic validators pass alongside
  native/local adapter metadata and roster-currentness checks.
- Checklist references remain valid (`preflight`, `postflight`, and the consolidated `document-authoring` contract).
- Diff check confirms no unintended edits outside the approved change scope.

## Related Documents

- [Validation Surface Contract](../contracts/validation-surfaces.json)
- [Harness Approval Boundaries](approval-boundaries.md)
- [Postflight Checklist](postflight-checklist.md)
- [Local Harness Catalog](../harness-catalog.md)
