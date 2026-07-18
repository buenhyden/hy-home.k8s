---
title: "Archive Record: Protected Surface and Supply Chain Hardening Implementation Plan"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-07-18"
original_type: "plan"
original_path: "docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md"
archived_on: "2026-07-18"
archive_reason: "completed-lineage"
replacement: null
source_commit: "a12aedfb71ccabd329dabc83bd2863474d1126b0"
source_blob: "7aa4c02b8d08a534a26c83c1d0c76194c548cdd0"
content_sha256: "df5a5f4569fa33996700514ec50364b358d89a1d45f1d7de86da19fb386aa4e8"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'Protected Surface and Supply Chain Hardening Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-14
---

# Protected Surface and Supply Chain Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden repository-static GitHub Action identity and permissions,
GitOps change visibility, and Vault/ESO bootstrap boundaries without reading
secrets, mutating live systems, or weakening the selector contract established
by Spec 031.

**Architecture:** Focused validators own immutable Action references,
identity-only GitOps change sets, and Vault/ESO static safety. The CI workflow
consumes those validators while preserving Spec 031 job selection; GitOps
output contains only object identity and deletion candidates; Vault bootstrap
uses verified TLS and interactive secret input rather than secret-bearing argv
or environment variables. Repository-static evidence remains separate from
remote and live readiness.

**Tech Stack:** Python 3, PyYAML, Bash, GitHub Actions YAML, Dependabot,
zizmor, Kustomize resource graphs, Kubernetes and ESO manifests, Vault HCL,
pre-commit, and repository quality gates.

## Overview

This Plan converts Spec 032 into six independently reviewable implementation
tasks. PSH-001 establishes execution evidence, PSH-002 adds a fixture-tested
Action validator, PSH-003 applies the eight reviewed Action identities and
least-privilege workflow permissions, PSH-004 adds value-free GitOps object and
deletion review, PSH-005 hardens the local Vault/ESO and bootstrap boundary,
and PSH-006 closes repository-static evidence while retaining live lanes as
DEFER.

## Context

At the pre-PSH baseline, the workflows contained fourteen `uses:` occurrences
covering eight unique tag references, and `.github/zizmor.yml` deliberately
disabled `unpinned-uses`. GitOps validation checked structure and manifests but
did not emit a reviewable before/after object-identity deletion set. The tracked
ESO store used HTTP to a local external Vault boundary without declaring the
token audience in `serviceAccountRef`; the bootstrap defaulted
`VAULT_SKIP_VERIFY=true` and placed the Vault token in curl argv and the Valkey
password in kubectl argv. PSH-001 through PSH-006 closed these repository-static
gaps. No live Vault, Kubernetes, ESO, Argo CD, or GitHub settings were inspected.

## Goals & In-Scope

- Pin all eight current remote Actions at reviewed forty-character commit SHAs
  while retaining human-readable version comments.
- Require a read-only workflow default and allow write permissions only in the
  three named issue/PR automation jobs.
- Remove the `unpinned-uses` suppression and keep Dependabot's reviewed
  `github-actions` proposal route.
- Produce a deterministic GitOps before/after identity set with explicit
  deletion candidates and no manifest values.
- Preserve the current local-only Vault HTTP service boundary while rejecting
  an unlabeled insecure transport or any production-readiness claim.
- Add the ESO Kubernetes token audience and retain the exact ServiceAccount,
  namespace, TokenReview binding, and least-privilege Vault paths.
- Make bootstrap Vault TLS verification mandatory and move the Vault token and
  Valkey password out of process argv and exported environment variables.
- Integrate the validators into Spec 031's affected-surface, local harness, and
  CI contracts without changing selector output or job names.

## Non-Goals & Out-of-Scope

- Live Kubernetes, Vault, ESO, Argo CD, NetworkPolicy, or GitHub execution.
- Remote branch protection, repository setting, Dependabot proposal, pull
  request, workflow dispatch, push, release, or merge.
- Reading secret values, ignored certificates, kubeconfigs, local settings,
  shell history, auth files, token caches, or `_workspace/**` scratch.
- Manufacturing a production Vault certificate, changing the external Vault
  runtime, applying the Vault policy, or claiming TLS readiness for the
  in-cluster local-only HTTP endpoint.
- SLSA, OpenSSF, SBOM, provenance, admission-control, or runtime compliance
  claims.
- Changing the path filters, selector outputs, or job-routing semantics owned
  by Spec 031.

### Global Constraints

- Work only in `.worktrees/workspace-document-assurance-modernization` on
  branch `codex/workspace-document-assurance-modernization`.
- Use Spec 032 as the implementation-contract owner and Spec 031 as the
  unchanged affected-surface and CI selection owner.
- Do not inspect, echo, log, serialize, or fixture any real secret value.
- Fixtures use non-secret sentinels and must prove that output excludes all
  non-identity manifest fields.
- Keep remote/live evidence `DEFER`; repository-static PASS must not be called
  live readiness.
- Keep local Action paths unchanged; require `docker://` references to use
  `sha256:` digests if they are introduced.
- Every remote `owner/repository@ref` and external reusable workflow uses a
  reviewed forty-character SHA plus a version comment on the same YAML line.
- Preserve workflow names, job IDs, `needs`, selector outputs, and `if`
  expressions established by Spec 031.
- Keep `permissions: contents: read` as the workflow default; default-deny every
  permission value equal to `write` unless the complete workflow/job/write-key
  tuple exactly matches one of the three named consumers.
- Preserve `github-actions` Dependabot updates as proposals that still require
  review, release-note inspection, and all repository checks.
- GitOps change output contains only change class, apiVersion, kind, namespace,
  name, and repository path; it never prints `data`, `stringData`, `spec`,
  annotations, labels, or decoded content.
- Preserve ClusterSecretStore only because current consumers cross namespaces;
  bind it to ServiceAccount `external-secrets` in namespace
  `external-secrets`, audience `vault`, and role `eso-read-platform`.
- Keep tracked HTTP Vault service/EndpointSlice and store transport explicitly
  `local-only`; production claims require a separately approved TLS design.
- Bootstrap requires an HTTPS `VAULT_ADDR`, an explicit CA file, and an
  interactive `/dev/tty` token prompt. There is no insecure-skip or environment
  token fallback.
- Run a focused RED-GREEN test and an independent reviewer gate before every
  logical commit.
- Run `pre-commit run --all-files` and the complete repo-static bundle before
  closure.
- Do not commit, push, merge, publish, dispatch, or apply from this planning
  task; implementation commits occur only while executing this Plan.

---

### File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Execution evidence | Spec 032, this Plan, same-topic Task, Spec/Plan/Task indexes | Own PSH-001 through PSH-006 state, validation evidence, reviewer, limitations, and rollback SHAs. |
| Action identity | `scripts/validate-github-actions-security.py`, its fixture, five workflows, Action inventory | Classify local, docker, and remote `uses`; enforce SHA/version and permission contracts. |
| GitOps change review | `scripts/validate-gitops-change-set.py`, its fixture, GitOps/CI/harness consumers | Render the repository-local resource graph to identities and report added/deleted identities only. |
| Vault/ESO static safety | `scripts/validate-vault-eso-contracts.py`, fixture, ESO/Vault manifests, HCL, bootstrap, static contracts | Enforce local-only transport, exact identity/audience/RBAC/policy, verified TLS, and secret-safe process boundaries. |
| Selector integration | Spec 031 validation-surface registry and `.github/workflows/ci.yml` | Add domain validators without changing path selection, outputs, job IDs, or job-routing behavior. |
| Closure | Task, roadmap, progress ledger, current indexes | Record repository-static PASS, optional SKIP/fallback, live DEFER, reviewer, rollback, and residual risk. |

## Work Breakdown

| Task | Description | Primary validation | Commit | Status |
| --- | --- | --- | --- | --- |
| PSH-001 | Start reciprocal Spec/Plan/Task execution evidence | Focused lineage assertion | `docs(execution): start protected surface hardening` | Done |
| PSH-002 | Add the fixture-tested Action identity and permission validator | Validator self-test | `test(security): add GitHub Actions security validator` | Done |
| PSH-003 | Pin all eight remote Actions and harden workflow permissions | Validator repository check, actionlint, zizmor | `fix(ci): pin Actions and minimize workflow permissions` | Done |
| PSH-004 | Add identity-only GitOps render and deletion review | Positive/negative change-set fixtures | `feat(gitops): validate identity-only change sets` | Done |
| PSH-005 | Harden local Vault/ESO and bootstrap secret handling | Vault self-test, static contracts, shell/secret checks | `fix(security): harden local Vault and ESO contracts` | Done |
| PSH-006 | Close lifecycle and repository-static evidence | Full QA bundle and independent review | `docs(security): close protected surface hardening evidence` | Done |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Lineage | Focused Python assertion in PSH-001 | Spec, Plan, Task, and indexes link reciprocally. |
| VAL-PLN-002 | Action fixtures | `python3 scripts/validate-github-actions-security.py --self-test` | Remote tag, missing version comment, mutable docker reference, broad write, and suppression cases fail exactly; local path passes. |
| VAL-PLN-003 | Action repository | `python3 scripts/validate-github-actions-security.py --root .` | Fourteen occurrences resolve to eight reviewed SHAs, version comments exist, permissions are minimal, and suppression is absent. |
| VAL-PLN-004 | GitOps change set | `python3 scripts/validate-gitops-change-set.py --self-test` | Added/deleted identities are exact and the sentinel manifest value never appears in output. |
| VAL-PLN-005 | Vault/ESO | `python3 scripts/validate-vault-eso-contracts.py --self-test` and `--root .` | HTTP needs local-only labels, audience/RBAC/policy are exact, insecure TLS and secret argv/env patterns fail. |
| VAL-PLN-006 | Repository | Static bundle and `pre-commit run --all-files` | Required gates pass, optional tool SKIP is separate, and live lanes are DEFER. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| A tag SHA is copied incorrectly | Remote code identity differs from the reviewed release | Use the eight upstream `git ls-remote` results frozen in PSH-003 and validate exact forty-character values. |
| Workflow permission hardening breaks automation | Greeting, labeling, or stale management fails remotely | Keep only the permissions each documented Action consumes; do not dispatch; record remote CI as DEFER. |
| GitOps review leaks manifest values | Secret or configuration content appears in logs | Build equality from the four-field immutable `ObjectIdentity`, carry path only in `RenderedObject` evidence, and reject the sentinel value in fixtures. |
| A deletion is hidden by a modified multi-document YAML | Argo CD prune impact is missed | Diff identity sets rather than filenames; a changed identity becomes one DELETE plus one ADD. |
| TLS hardening breaks local bootstrap | Vault cannot be reached with the configured local CA | Require `VAULT_CA_FILE`, fail before mutation, keep rollback to the prior commit, and do not add an insecure fallback. |
| ESO audience does not match the external Vault role | Desired state would fail live authentication | Document `bound_audiences=vault` as an operator prerequisite and keep apply/live verification DEFER. |
| ClusterSecretStore remains broader than a namespaced store | Cross-namespace identity has larger scope | Retain one exact SA/namespace/audience, narrow TokenReview subject and HCL paths, and require a separate migration decision before changing store kind. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Every production validator must call the same
  validation function used by its fixture self-test.
- **Protected Review Gate**: A fresh reviewer checks Action SHAs/permissions,
  GitOps output redaction/deletions, and Vault/ESO secret/TLS behavior before
  each protected-surface commit.
- **Sandbox / Canary Gate**: Fixtures and repository-static commands only; no
  workflow dispatch, manifest apply, Vault request, or cluster access.
- **Human Approval Gate**: Required for push, merge, remote workflow execution,
  certificate or credential change, GitOps reconciliation, or live operator
  action.
- **Rollback Trigger**: Any validator false negative, secret sentinel in output,
  selector/job-routing change, unresolved permission consumer, or static gate
  failure blocks the task and reverts its logical commit.
- **Live Evidence Boundary**: GitHub remote behavior, Argo CD prune/reconcile,
  ESO authentication, Vault TLS/runtime, and Kubernetes authorization remain
  DEFER even after repository-static PASS.

---

### Task 1: Start the Canonical Execution Chain (PSH-001)

**Files:**

- Modify: `docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: active Spec 032 and completed Spec 031 evidence.
- Produces: one active Task whose exact IDs are `PSH-001` through `PSH-006`.
- Produces: reciprocal Spec/Plan/Task lineage for every later evidence update.
- Produces: one exact fourteen-column durable-ledger row for the new Task.

- [x] **Step 1: Run the failing reciprocal-lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path

spec = Path('docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md')
task = Path('docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md')
assert task.exists(), task
assert '../../04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md' in spec.read_text()
assert '../../04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md' in spec.read_text()
assert '../../03.specs/032-protected-surface-supply-chain-hardening/spec.md' in plan.read_text()
assert '../tasks/2026-07-12-protected-surface-supply-chain-hardening.md' in plan.read_text()
assert '../../03.specs/032-protected-surface-supply-chain-hardening/spec.md' in task.read_text()
assert '../plans/2026-07-12-protected-surface-supply-chain-hardening.md' in task.read_text()
PY
```

Expected: FAIL because the Task and reciprocal links do not exist yet.

- [x] **Step 2: Create the active execution record**

At Task 1 execution, set the Spec, Plan, and Task to `status: active`. The
embedded lifecycle snapshot below is normalized at closure to the final Done
states; commit `a2aa49f200b0b6bd36fe67ee469d17a971297430` preserves the initial
Active/Pending transition evidence.

```markdown
| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| PSH-001 | Start reciprocal execution evidence | doc | Reciprocal-link assertion | platform | Done |
| PSH-002 | Add Action identity and permission validator | guardrail | Action fixture self-test | platform | Done |
| PSH-003 | Pin eight Action identities and minimize workflow permissions | ci | Action validator, actionlint, zizmor | platform | Done |
| PSH-004 | Add GitOps identity and deletion change-set review | guardrail | GitOps fixture self-test | platform | Done |
| PSH-005 | Harden local Vault/ESO and bootstrap secret handling | security | Vault fixture, static contracts, secret scan | platform | Done |
| PSH-006 | Close repository-static evidence and lifecycle | doc | Full QA bundle and independent review | platform | Done |
```

Add exact reciprocal links, add Active index rows dated `2026-07-12`, and add
the new Task's exact fourteen-column durable-ledger row.

- [x] **Step 3: Re-run the lineage assertion**

Run the Step 1 command again.

Expected: PASS with no output.

- [x] **Step 4: Run focused conformance**

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
```

Expected: all applicable checks PASS.

- [ ] **Step 5: Commit**

```bash
git add \
  docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
python3 - <<'PY'
import subprocess

expected = {
    'docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md',
    'docs/04.execution/tasks/README.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
}
staged = {
    path.decode()
    for path in subprocess.check_output(
        ['git', 'diff', '--cached', '--name-only', '-z']
    ).split(b'\0')
    if path
}
unstaged = subprocess.check_output(['git', 'diff', '--name-only', '-z'])
assert staged == expected, (sorted(staged), sorted(expected))
assert unstaged == b'', unstaged
PY
git commit -m "docs(execution): start protected surface hardening"
```

---

### Task 2: Add the Action Security Validator (PSH-002)

**Files:**

- Create: `scripts/validate-github-actions-security.py`
- Create: `tests/fixtures/github-actions-security.json`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md`
- Modify: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`

**Interfaces:**

- Produces: `classify_uses(value: str) -> Literal['local', 'docker', 'remote']`.
- Produces: `validate_workflow(path: Path, data: dict, lines: list[str]) -> list[str]`.
- Produces: `validate_repository(root: Path) -> list[str]`.
- Produces CLI: `python3 scripts/validate-github-actions-security.py --self-test`.
- Produces CLI: `python3 scripts/validate-github-actions-security.py --root .`.
- The self-test and repository mode call the same three production functions.

- [x] **Step 1: Create the failing fixture**

Create `tests/fixtures/github-actions-security.json` with these exact case
names and expected outcomes:

```json
{
  "cases": [
    {"name": "valid-remote-sha", "uses": "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", "comment": "v7.0.0", "expected": []},
    {"name": "remote-tag", "uses": "actions/checkout@v7.0.0", "comment": "v7.0.0", "expected": ["remote uses must use a forty-character commit SHA"]},
    {"name": "missing-version-comment", "uses": "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", "comment": "", "expected": ["remote uses must retain a version comment"]},
    {"name": "valid-local", "uses": "./.github/actions/local-check", "comment": "", "expected": []},
    {"name": "valid-docker-digest", "uses": "docker://alpine@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "comment": "3.22.1", "expected": []},
    {"name": "mutable-docker", "uses": "docker://alpine:3.22.1", "comment": "3.22.1", "expected": ["docker uses must use a sha256 digest"]},
    {"name": "broad-write", "permissions": {"contents": "write"}, "expected": ["workflow default permissions must be read-only"]},
    {"name": "valid-allowlisted-job", "workflow": "greetings.yml", "job": "greeting", "permissions": {"issues": "write", "pull-requests": "write"}, "expected": []},
    {"name": "unlisted-write", "workflow": "ci.yml", "job": "build", "permissions": {"pages": "write"}, "expected": ["write permission is not allowlisted"]},
    {"name": "write-all", "permissions": "write-all", "expected": ["write-all is forbidden"]},
    {"name": "unpinned-suppression", "zizmor": {"rules": {"unpinned-uses": {"disable": true}}}, "expected": ["unpinned-uses suppression is forbidden"]}
  ]
}
```

Keep `cases` as the exact eleven-case primary contract. Add a separately named
`repositoryBoundaryCases` array with exactly ten missing-root,
missing-directory, empty-directory, root/directory/file-symlink,
non-regular-workflow, and zizmor symlink cases. Add `requiredWriteCases` with
exactly twenty-one cases: exact writes, extra reads, missing job, missing
permissions, all-read, missing write, and extra write for each of
`greetings/greeting`, `labeler/label`, and `stale/stale`. The supplemental
cases do not alter the primary eleven-case cardinality.
Keep numeric, null, mapping, and list `uses:` values as four internal
self-test mutations rather than JSON fixture cases; retain one internal quoted
local-path positive so quoted and plain same-line strings remain accepted.

- [x] **Step 2: Run the fixture and confirm RED**

```bash
python3 scripts/validate-github-actions-security.py --self-test
```

Expected: FAIL because the validator does not exist.

- [x] **Step 3: Implement the minimal validator**

Use these exact reference classes and permission rules:

```python
REMOTE_REF = re.compile(r"^[^\s/@]+/[^\s@]+(?:/[^\s@]+)*@([0-9a-f]{40})$")
DOCKER_REF = re.compile(r"^docker://[^\s@]+@sha256:([0-9a-f]{64})$")
VERSION_COMMENT = re.compile(r"#\s*(v?[0-9]+(?:\.[0-9]+){0,2})\s*$")
ALLOWED_JOB_WRITES = {
    ("greetings.yml", "greeting"): {"issues", "pull-requests"},
    ("labeler.yml", "label"): {"pull-requests"},
    ("stale.yml", "stale"): {"issues", "pull-requests"},
}
```

Require top-level `contents: read` and default-deny every permission entry whose
value is `write`, regardless of whether its key is known today. Reject
`write-all`. A write is valid only when the workflow filename, job ID, and the
complete set of write-valued keys exactly matches one of the three
`ALLOWED_JOB_WRITES` entries; additional keys such as `pages: write` fail.
Read-valued keys do not expand the write allowlist. Reject any `unpinned-uses`
disable. Parse YAML with a duplicate-key rejecting loader and locate the
same-line version comment from the source line rather than from parsed YAML.
Preserve every parsed and source `uses` occurrence regardless of its YAML type,
then require both views to contain strings before comparing them. Numeric,
null, mapping, list, multiline, or otherwise non-plain shapes fail with
`uses entries must be plain same-line scalar values`; parsed and source
collectors must never jointly erase a malformed occurrence.
Repository mode must fail closed before reading YAML: the caller-provided root,
`.github`, and `.github/workflows` must be existing non-symlink directories;
the workflow directory must contain at least one real regular workflow YAML;
and every workflow or optional zizmor YAML input must be a non-symlink regular
file. Inspect these boundaries with `lstat()` and preserve the caller path in
CLI mode rather than resolving away symlink identity. When an allowlisted
workflow exists, its named job and exact required write set are mandatory;
removing the job/permissions or reducing required writes is a contract failure,
while extra read-valued keys remain valid.

- [x] **Step 4: Run GREEN and prove current repository RED**

```bash
python3 scripts/validate-github-actions-security.py --self-test
python3 scripts/validate-github-actions-security.py --root .
```

Expected: the exact eleven primary cases plus ten boundary, twenty-one
required-write, and five internal uses-shape cases PASS. Repository mode FAILS with fourteen
mutable remote occurrences, missing workflow defaults in `greetings.yml`,
`labeler.yml`, and `stale.yml`, and the `unpinned-uses` suppression. This
repository failure is the RED input for PSH-003 and is not integrated into the
aggregate quality gate until PSH-003 turns it green.

- [x] **Step 5a: Run focused checks and stage the exact scope**

```bash
python3 -m py_compile scripts/validate-github-actions-security.py
pre-commit run --files \
  scripts/validate-github-actions-security.py \
  tests/fixtures/github-actions-security.json \
  scripts/README.md \
  tests/README.md \
  docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md
git diff --check
git add \
  scripts/validate-github-actions-security.py \
  tests/fixtures/github-actions-security.json \
  scripts/README.md \
  tests/README.md \
  docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md
test "$(git diff --cached --name-only | wc -l)" -eq 6
test -z "$(git diff --name-only)"
```

- [ ] **Step 5b: Controller review and commit**

```bash
git commit -m "test(security): add GitHub Actions security validator"
```

---

### Task 3: Pin Actions and Minimize Workflow Permissions (PSH-003)

**Files:**

- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/generate-changelog.yml`
- Modify: `.github/workflows/greetings.yml`
- Modify: `.github/workflows/labeler.yml`
- Modify: `.github/workflows/stale.yml`
- Delete: `.github/zizmor.yml`
- Verify only: `.github/dependabot.yml`
- Modify: `.github/ABOUT.md`
- Modify: `docs/90.references/data/tech-stack-version-inventory.md`
- Modify: `docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md`
- Modify: `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md`
- Modify: `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md`
- Modify: `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`

The exact Task 3 implementation mutable/deleted set is 15 paths. The
verify-only `.github/dependabot.yml` path is not part of that set.

**Interfaces:**

- Consumes: `validate_repository(root: Path) -> list[str]` from PSH-002.
- Produces: `GitHubActionIdentityContract.v1` with eight exact SHA/version pairs.
- Produces: `WorkflowPermissionContract.v1` with read-only workflow defaults
  and three exact job-write consumers.
- Preserves: Spec 031 `changes` outputs, job IDs, `needs`, and `if` expressions.

- [ ] **Step 1: Capture RED from the real repository**

```bash
python3 scripts/validate-github-actions-security.py --root .
```

Expected: FAIL with the PSH-002 mutable-reference, permission-default, and
suppression findings.

- [ ] **Step 2: Replace all fourteen occurrences using the reviewed map**

Use exactly these upstream tag resolutions, observed with `git ls-remote` on
2026-07-12:

| Action | Version comment | Commit SHA |
| --- | --- | --- |
| `actions/checkout` | `v7.0.0` | `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0` |
| `actions/setup-python` | `v6.3.0` | `ece7cb06caefa5fff74198d8649806c4678c61a1` |
| `pre-commit/action` | `v3.0.1` | `2c7b3805fd2a0fd8c1884dcaebf91fc102a13ecd` |
| `actions/first-interaction` | `v3` | `1c4688942c71f71d4f5502a26ea67c331730fa4d` |
| `actions/labeler` | `v6.1.0` | `f27b608878404679385c85cfa523b85ccb86e213` |
| `orhun/git-cliff-action` | `v4` | `f50e11560dce63f7c33227798f90b924471a88b5` |
| `actions/upload-artifact` | `v7` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |
| `actions/stale` | `v10.3.0` | `eb5cf3af3ac0a1aa4c9c45633dd1ae542a27a899` |

Each YAML line uses this exact shape:

```yaml
- uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0
```

Apply the mapping to all five checkout, three setup-python, and the six
remaining occurrences. Store the SHA, not the tag, as each corresponding
`github_actions` value in the version inventory; the workflow comment remains
the human version boundary.

- [ ] **Step 3: Apply the exact permission contract and suppression removal**

Add this top-level default after each workflow trigger when it is absent:

```yaml
permissions:
  contents: read
```

Keep these exact job overrides:

```yaml
# greetings.yml / greeting
permissions:
  issues: write
  pull-requests: write

# labeler.yml / label
permissions:
  contents: read
  pull-requests: write

# stale.yml / stale
permissions:
  issues: write
  pull-requests: write
```

Delete `.github/zizmor.yml`; it contains only the obsolete suppression. Keep
the existing weekly grouped `github-actions` Dependabot proposal route and
record in `.github/ABOUT.md` that no zizmor suppression file is required.
Preserve the historical findings, link labels, dates, conclusions, and
surrounding prose in the five declared Stage 90 documents. Replace only the six
Markdown link targets that would otherwise point to the deleted
`.github/zizmor.yml`: select the active GitHub Actions security validator, the
PSH Task, or `.github/ABOUT.md` as the replacement evidence target according to
the local context of each link. Do not rewrite or suppress the historical
finding that the link documents.

- [ ] **Step 4: Integrate the validator into repository quality**

Replace the current quality-gate block that requires `unpinned-uses` to be
disabled with this subprocess contract:

```python
action_security = subprocess.run(
    [sys.executable, str(root / "scripts/validate-github-actions-security.py"), "--root", str(root)],
    cwd=root,
    text=True,
    capture_output=True,
)
if action_security.returncode != 0:
    fail("GitHub Actions security validation failed: " + action_security.stdout.strip())
```

- [ ] **Step 5: Run GREEN verification**

```bash
python3 scripts/validate-github-actions-security.py --self-test
python3 scripts/validate-github-actions-security.py --root .
bash scripts/validate-repo-quality-gates.sh .
pre-commit run actionlint --all-files
pre-commit run zizmor --all-files
git diff --check
```

Expected: all commands PASS; there are fourteen remote occurrences, eight unique
SHA/version identities, no suppression, and no unauthorized write permission.

- [ ] **Step 6: Independent review and commit**

Reviewer checks each SHA against the frozen table, confirms comments and
permission consumers, and confirms no selector/job-routing line changed.

```bash
git add \
  .github/workflows/ci.yml \
  .github/workflows/generate-changelog.yml \
  .github/workflows/greetings.yml \
  .github/workflows/labeler.yml \
  .github/workflows/stale.yml \
  .github/zizmor.yml \
  .github/ABOUT.md \
  docs/90.references/data/tech-stack-version-inventory.md \
  docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md \
  docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md \
  docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md \
  docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md \
  docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md \
  scripts/validate-repo-quality-gates.sh \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md
git commit -m "fix(ci): pin Actions and minimize workflow permissions"
```

---

### Task 4: Add Identity-Only GitOps Change Review (PSH-004)

**Files:**

- Create: `scripts/validate-gitops-change-set.py`
- Create: `tests/fixtures/gitops-change-set/cases.json`
- Create: `tests/fixtures/gitops-change-set/base/kustomization.yaml`
- Create: `tests/fixtures/gitops-change-set/base/retained-configmap.yaml`
- Create: `tests/fixtures/gitops-change-set/base/removed-service.yaml`
- Create: `tests/fixtures/gitops-change-set/head/kustomization.yaml`
- Create: `tests/fixtures/gitops-change-set/head/moved-retained-configmap.yaml`
- Create: `tests/fixtures/gitops-change-set/head/added-service.yaml`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `scripts/validate-harness.sh`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `gitops/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`

**Interfaces:**

- Produces immutable `ObjectIdentity(api_version, kind, namespace, name)`; path
  is evidence and is never part of identity equality.
- Produces `RenderedObject(identity: ObjectIdentity, path: str)` and
  `render_identity_graph(root: Path, revision: str) -> dict[ObjectIdentity, RenderedObject]`.
- Produces `diff_identities(base: dict[ObjectIdentity, RenderedObject], head: dict[ObjectIdentity, RenderedObject]) -> ChangeSet`.
- Produces CLI: `python3 scripts/validate-gitops-change-set.py --self-test`.
- Produces CLI: `python3 scripts/validate-gitops-change-set.py --root . --base-ref REF`.
- Output rows are exactly `ADD|DELETE|RETAIN apiVersion kind namespace/name path`.
- Consumes Spec 031 validator ID `gitops-change-set`; it does not change the
  route or CI job selected for `gitops/**`.

- [ ] **Step 1: Write the failing identity fixture**

The base graph contains ConfigMap `platform/retained` at
`retained-configmap.yaml` and Service `platform/removed`. The head graph
contains the same ConfigMap identity at `moved-retained-configmap.yaml` and
Service `platform/added`. Put `DO_NOT_EMIT_SENTINEL` under the ConfigMap `data`
in both graphs. This path-only move must remain `RETAIN`, not an ADD/DELETE
pair. Set `cases.json` to this exact result:

```json
{
  "expected": [
    "ADD v1 Service platform/added added-service.yaml",
    "DELETE v1 Service platform/removed removed-service.yaml",
    "RETAIN v1 ConfigMap platform/retained moved-retained-configmap.yaml"
  ],
  "forbidden_output": ["DO_NOT_EMIT_SENTINEL", "data:", "spec:", "stringData:"]
}
```

- [ ] **Step 2: Run RED**

```bash
python3 scripts/validate-gitops-change-set.py --self-test
```

Expected: FAIL because the script does not exist.

- [ ] **Step 3: Implement the minimal identity renderer**

Use PyYAML only to locate `apiVersion`, `kind`, `metadata.namespace`, and
`metadata.name`. Recursively follow local `resources` in `kustomization.yaml`.
Reject absolute paths, `..`, remote URLs, generators, Helm inflators, and
patches instead of pretending they were rendered. For a Git revision, read
files with `git show <revision>:<path>`; use the working tree for the head. If
`BASE_REF` is forty zeroes, use `HEAD^`; if the repository has no parent,
compare with the empty tree. Sort identities lexically before output.

Build `ObjectIdentity` from exactly `apiVersion`, `kind`, namespace, and name.
Store the source path only in `RenderedObject`. Diff dictionary keys and use the
head `RenderedObject.path` for ADD/RETAIN output and the base path for DELETE;
therefore a path-only move retains the same identity. The serializer must use
only this shape:

```python
def format_identity(change: str, rendered: RenderedObject) -> str:
    identity = rendered.identity
    namespace = identity.namespace or "_cluster"
    return f"{change} {identity.api_version} {identity.kind} {namespace}/{identity.name} {rendered.path}"
```

- [ ] **Step 4: Integrate the domain consumer without changing selection**

Add `gitops-change-set` to the existing `gitops/**` validator list in
`validation-surfaces.json`. In the existing `manifest-static` run block add:

```yaml
- name: Review GitOps object identity and deletion set
  env:
    BASE_REF: ${{ github.event.pull_request.base.sha || github.event.before }}
  run: |
    python3 scripts/validate-gitops-change-set.py --root . --base-ref "$BASE_REF"
```

Add the same command with `--base-ref HEAD` to `validate-harness.sh`. Register
the script and its identity-only evidence semantics in script/test/GitOps
READMEs and the repository quality gate.

- [ ] **Step 5: Run GREEN verification**

```bash
python3 scripts/validate-gitops-change-set.py --self-test
python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD
python3 scripts/validate-affected-surfaces.py --root .
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/validate-repo-quality-gates.sh .
pre-commit run actionlint --all-files
git diff --check
```

Expected: fixture output matches exactly; real worktree output contains only
identities; affected-surface and CI selection remain unchanged.

- [ ] **Step 6: Independent review and commit**

Reviewer verifies the fixture detects the DELETE, reports the path-only move as
one RETAIN with no ADD/DELETE for that identity, the sentinel never appears,
and the CI diff contains no changed filter/output/job-routing line.

```bash
git add \
  scripts/validate-gitops-change-set.py \
  tests/fixtures/gitops-change-set \
  docs/00.agent-governance/contracts/validation-surfaces.json \
  .github/workflows/ci.yml \
  scripts/validate-harness.sh \
  scripts/validate-repo-quality-gates.sh \
  scripts/README.md \
  tests/README.md \
  gitops/README.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md
git commit -m "feat(gitops): validate identity-only change sets"
```

---

### Task 5: Harden Local Vault/ESO and Bootstrap Boundaries (PSH-005)

**Files:**

- Create: `scripts/validate-vault-eso-contracts.py`
- Create: `tests/fixtures/vault-eso-contracts.json`
- Modify: `gitops/platform/eso/vault-secret-store.yaml`
- Modify: `gitops/platform/eso/vault-token-reviewer-binding.yaml`
- Modify: `gitops/platform/external-services/vault-external.yaml`
- Verify only: `infrastructure/vault/policies/eso-read.hcl`
- Modify: `infrastructure/bootstrap-local.sh`
- Modify: `infrastructure/tests/verify-contracts-static.sh`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `scripts/validate-harness.sh`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `gitops/README.md`
- Modify: `infrastructure/README.md`
- Modify: `docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md`
- Modify: `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`
- Modify: `docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md`
- Modify: `docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`
- Modify: `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`
- Modify: `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`
- Modify: `docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`
- Modify: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`

**Interfaces:**

- Produces `validate_vault_store(data: dict) -> list[str]`.
- Produces `validate_token_reviewer(data: dict) -> list[str]`.
- Produces `validate_vault_policy(text: str) -> list[str]`.
- Produces `validate_bootstrap(text: str) -> list[str]`.
- Produces CLI: `python3 scripts/validate-vault-eso-contracts.py --self-test`.
- Produces CLI: `python3 scripts/validate-vault-eso-contracts.py --root .`.
- Produces bootstrap contract: HTTPS plus CA, token from `/dev/tty`, curl
  header from stdin, Kubernetes Secret value from stdin, and no insecure mode.
- Preserves local-only ClusterSecretStore because current ExternalSecrets span
  `argocd` and `apps`; changing the store kind is outside this Plan.

- [ ] **Step 1: Write the failing positive/negative fixture**

Create these exact cases in `vault-eso-contracts.json`:

```json
{
  "cases": [
    {"name": "valid-local-http", "mutation": "none", "expected": []},
    {"name": "http-without-local-boundary", "mutation": "remove-local-only-annotations", "expected": ["HTTP Vault transport requires local-only annotations"]},
    {"name": "missing-audience", "mutation": "remove-vault-audience", "expected": ["Vault serviceAccountRef audiences must equal ['vault']"]},
    {"name": "wrong-service-account", "mutation": "change-service-account", "expected": ["Vault identity must be external-secrets/external-secrets"]},
    {"name": "broad-token-reviewer", "mutation": "add-token-reviewer-subject", "expected": ["TokenReview binding must contain exactly one subject"]},
    {"name": "wildcard-policy", "mutation": "add-platform-wildcard", "expected": ["Vault policy must not contain wildcard platform paths"]},
    {"name": "insecure-bootstrap", "mutation": "add-curl-insecure", "expected": ["bootstrap must not disable Vault TLS verification"]},
    {"name": "token-in-argv", "mutation": "add-token-header-argument", "expected": ["bootstrap must not place Vault token in argv"]},
    {"name": "secret-in-env", "mutation": "add-exported-token", "expected": ["bootstrap must not accept or export Vault token environment input"]},
    {"name": "secret-in-kubectl-argv", "mutation": "add-from-literal-password", "expected": ["bootstrap must not place generated secret values in kubectl argv"]}
  ]
}
```

- [ ] **Step 2: Implement the validator and prove repository RED**

```bash
python3 scripts/validate-vault-eso-contracts.py --self-test
```

Expected before implementation: FAIL because the script does not exist. After
minimal implementation, self-test PASS and this command must fail on the
current repository:

```bash
python3 scripts/validate-vault-eso-contracts.py --root .
```

Expected repository findings: missing local-only annotations, missing
`audiences: [vault]`, `VAULT_SKIP_VERIFY`, curl `-k`, token header argv, token
environment input, and kubectl `--from-literal` secret argv.

- [ ] **Step 3: Mark the local-only HTTP boundary**

As one 2–5 minute checkpoint, add these annotations to the ClusterSecretStore
and the external Vault Service/EndpointSlice documents, then run repository mode
and confirm that only the remaining audience/bootstrap findings remain:

```yaml
annotations:
  platform.hyhome.io/environment-scope: local-only
  platform.hyhome.io/transport-boundary: local-only-http
```

- [ ] **Step 4: Add the exact ESO audience and service-account identity**

As a separate 2–5 minute checkpoint, keep the current HTTP server and add the
audience:

```yaml
serviceAccountRef:
  name: external-secrets
  namespace: external-secrets
  audiences:
    - vault
```

Keep role `eso-read-platform`. Run repository mode again and confirm the
audience/identity findings are gone before continuing.

- [ ] **Step 5: Verify the TokenReview binding and least-privilege HCL**

In one read/verification checkpoint, keep exactly one TokenReview subject,
ServiceAccount `external-secrets` in namespace `external-secrets`; verify the
following literal `VaultHclReadAllowlist.v1` and reject any missing path,
additional path, wildcard, or write capability:

```text
secret/data/platform/argocd
secret/metadata/platform/argocd
secret/data/platform/postgres-app
secret/metadata/platform/postgres-app
secret/data/platform/notifications
secret/metadata/platform/notifications
```

Every listed stanza permits exactly `read` and `list`; no other capability is
accepted. The validator fixture and repository check consume this literal
allowlist rather than inferring paths from prose.
Document the external operator prerequisite `bound_audiences=vault`. State
that the HTTP endpoint is acceptable only for the current local k3d network
boundary and is not a production TLS claim. Do not modify
`infrastructure/vault/policies/eso-read.hcl`; if verification fails, stop this
checkpoint and record a separately reviewed follow-up rather than expanding the
Plan's verify-only scope.

- [ ] **Step 6: Replace insecure Vault transport and token input**

Remove `VAULT_SKIP_VERIFY` and environment-token input. Add this exact secure
input and curl shape before the first Vault request:

```bash
VAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"

case "$VAULT_ADDR" in
  https://*) ;;
  *) fail "VAULT_ADDR must use https:// for secret-bearing bootstrap" ;;
esac

require_file "$VAULT_CA_FILE"
if [[ ! -r /dev/tty ]]; then
  fail "interactive /dev/tty is required for Vault token input"
fi
IFS= read -r -s -p "Vault token: " vault_token </dev/tty
printf '\n' >/dev/tty
[[ -n "$vault_token" ]] || fail "Vault token input is empty"

cleanup_sensitive() {
  unset vault_token VALKEY_PASSWORD
}
trap cleanup_sensitive EXIT HUP INT TERM

vault_curl() {
  printf 'X-Vault-Token: %s\n' "$vault_token" |
    curl --fail-with-body --silent --show-error \
      --cacert "$VAULT_CA_FILE" --header @- "$@"
}
```

Call `vault_curl` without `-H`. Run `bash -n infrastructure/bootstrap-local.sh`
and the validator repository mode; confirm only the Kubernetes Secret argv and
documentation findings remain before continuing.

- [ ] **Step 7: Move the generated Kubernetes Secret value to stdin**

As a separate 2–5 minute checkpoint, extract only `valkey_password` into the
non-exported shell variable and replace `--from-literal` with stdin:

```bash
VALKEY_PASSWORD="$(vault_curl \
  "$VAULT_ADDR/v1/secret/data/platform/argocd" |
  jq -er '.data.data.valkey_password')"

printf '%s' "$VALKEY_PASSWORD" |
  kubectl -n argocd create secret generic argocd-external-valkey \
    --from-file=redis-password=/dev/stdin \
    --dry-run=client -o yaml |
  kubectl apply -f -
unset VALKEY_PASSWORD
```

- [ ] **Step 8: Correct unsafe operational examples in exact small batches**

Use these four exact 2–5 minute checkpoints; validate each pair before opening
the next pair:

1. `docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md` and
   `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`.
2. `docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md` and
   `docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`.
3. `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md` and
   `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`.
4. `docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`,
   `infrastructure/README.md`, and `gitops/README.md`.

Remove active examples that export or inline `VAULT_TOKEN`, use `curl -k` for
secret-bearing requests, or put credentials in command argv. Document that
`./infrastructure/bootstrap-local.sh` prompts on `/dev/tty`, uses
`VAULT_CA_FILE`, and has no non-interactive or insecure fallback.

- [ ] **Step 9: Extend static enforcement and CI consumption**

Make `verify-contracts-static.sh` assert the exact annotations, audience,
identity, and no-wildcard HCL contract. Add validator ID
`vault-eso-contracts` to the existing bootstrap/Vault HCL/ESO routes in
`validation-surfaces.json`. Add this command to the existing
`manifest-static` block without changing its selector:

```yaml
bash scripts/check-secret-handling.sh .
python3 scripts/validate-vault-eso-contracts.py --root .
```

Add the same validator to `validate-harness.sh`, the repository quality gate,
and script/test inventories.

- [ ] **Step 10: Run GREEN verification**

```bash
python3 scripts/validate-vault-eso-contracts.py --self-test
python3 scripts/validate-vault-eso-contracts.py --root .
bash -n infrastructure/bootstrap-local.sh
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
bash scripts/validate-k8s-manifests.sh .
python3 scripts/validate-affected-surfaces.py --root .
bash scripts/validate-repo-quality-gates.sh .
rg -n 'VAULT_SKIP_VERIFY|curl .*-[A-Za-z]*k|VAULT_TOKEN=.*bootstrap-local|--from-literal=redis-password' \
  infrastructure/bootstrap-local.sh \
  docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md \
  docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md \
  docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md \
  docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md \
  docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md \
  docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md \
  docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md
rg -n 'X-Vault-Token:.*\$' \
  docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md \
  docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md \
  docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md \
  docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md \
  docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md \
  docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md \
  docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md
git diff --check
```

Expected: all validators PASS and both `rg` commands exit `1` with no output.
The production `validate-vault-eso-contracts.py --root .` validator owns the
safe stdin-header semantics, including the required `printf` producer piped to
`curl --header @-`. Unrelated non-secret local UI status and smoke probes are
outside this secret-bearing checkpoint. No live endpoint is contacted.

- [ ] **Step 11: Independent review and commit**

Reviewer verifies no real secret was read, no secret appears in diff/output,
the local-only exception cannot be read as production-ready, the external Vault
audience prerequisite is explicit, and CI selectors/job routing are unchanged.

```bash
git add \
  scripts/validate-vault-eso-contracts.py \
  tests/fixtures/vault-eso-contracts.json \
  gitops/platform/eso/vault-secret-store.yaml \
  gitops/platform/eso/vault-token-reviewer-binding.yaml \
  gitops/platform/external-services/vault-external.yaml \
  infrastructure/bootstrap-local.sh \
  infrastructure/tests/verify-contracts-static.sh \
  docs/00.agent-governance/contracts/validation-surfaces.json \
  .github/workflows/ci.yml \
  scripts/validate-harness.sh \
  scripts/validate-repo-quality-gates.sh \
  scripts/README.md \
  tests/README.md \
  gitops/README.md \
  infrastructure/README.md \
  docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md \
  docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md \
  docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md \
  docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md \
  docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md \
  docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md \
  docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md
git commit -m "fix(security): harden local Vault and ESO contracts"
```

---

### Task 6: Close Repository-Static Evidence and Lifecycle (PSH-006)

**Files:**

- Modify: `docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: PSH-001 through PSH-005 commits and independent review results.
- Produces: completed Spec/Plan/Task lifecycle and one rerunnable evidence table.
- Produces: RMD-014 closure evidence.
- Produces: repository-static remediation evidence for RMD-001 through RMD-003
  while retaining external-role, rotation, rollback rehearsal, and live checks
  as open/DEFER where they were not executed.

- [x] **Step 1: Run the failing closure assertion**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md'),
    Path('docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md'),
    Path('docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md'),
]
for path in paths:
    assert 'status: done' in path.read_text(), path
task = paths[2].read_text()
for task_id in ('PSH-001', 'PSH-002', 'PSH-003', 'PSH-004', 'PSH-005', 'PSH-006'):
    assert task_id in task and f'| {task_id} |' in task
assert 'Remote/live | DEFER' in task
assert 'RMD-014 closure evidence' in Path('docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md').read_text()
PY
```

Expected: FAIL while lifecycle and evidence are still active.

- [x] **Step 2: Run the complete repository-static bundle**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-github-actions-security.py --self-test
python3 scripts/validate-github-actions-security.py --root .
python3 scripts/validate-gitops-change-set.py --self-test
python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD
python3 scripts/validate-vault-eso-contracts.py --self-test
python3 scripts/validate-vault-eso-contracts.py --root .
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

Expected: required checks PASS. If kube-linter or Conftest is unavailable,
record its tool result as SKIP and the built-in fallback separately. Remote
GitHub execution, live Argo CD prune/reconcile, Vault/ESO authentication, TLS
runtime, and Kubernetes authorization are recorded as DEFER.

- [x] **Step 3: Obtain one whole-tranche independent review**

The reviewer records:

```text
Scope: PSH-001..PSH-005 commit range
Action identity/permissions: PASS or blocking finding
GitOps identity/deletion/redaction: PASS or blocking finding
Vault/ESO TLS/identity/secret handling: PASS or blocking finding
Selector/job-routing preservation: PASS or blocking finding
Secret-value access: none
Remote/live evidence: DEFER
Rollback: first-parent commit before PSH-001
```

Resolve every Critical or Important finding and rerun the relevant focused
commands before proceeding.

- [x] **Step 4: Close lifecycle and roadmap evidence**

Set Spec, Plan, and Task to `status: done`; mark all six Task rows Done; update
the three indexes. Add a roadmap subsection titled
`### RMD-014 closure evidence` that links Spec, Plan, Task, validator, and five
workflows. Record RMD-001 through RMD-003 repository-static remediation without
rewriting the dated source finding and explicitly retain unexecuted external
Vault role application, credential rotation, live TLS/ESO authentication, and
rollback rehearsal as follow-up/DEFER. Append one progress entry with commands,
results, reviewer, limitations, and rollback commit.

- [x] **Step 5: Re-run closure and final quality checks**

Run the Step 1 assertion again, then:

```bash
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
git status --short
```

Expected: assertion and required gates PASS. Status shows only the intended
closure files before commit.

- [ ] **Step 6: Commit**

```bash
git add \
  docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md \
  docs/04.execution/tasks/README.md \
  docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "docs(security): close protected surface hardening evidence"
```

## Completion Criteria

- All fourteen current remote `uses:` occurrences resolve to the eight exact
  reviewed SHAs and retain same-line version comments.
- Local Actions remain local; introduced docker Actions, if any, require an
  immutable digest and version comment.
- All workflows have read-only defaults; only greeting, label, and stale jobs
  have their exact issues/pull-request writes.
- `.github/zizmor.yml` and every `unpinned-uses` suppression are absent.
- Dependabot retains the weekly reviewed `github-actions` proposal route.
- GitOps fixtures prove one ADD, one DELETE, and one RETAIN while excluding all
  manifest values from output.
- Real GitOps review emits identity-only change rows and does not claim Argo CD
  prune or reconciliation evidence.
- ClusterSecretStore declares the exact SA, namespace, audience, role, and
  local-only HTTP boundary; TokenReview and HCL remain least privilege.
- Bootstrap requires HTTPS and a CA, reads the token from `/dev/tty`, places no
  token or password in argv/exported env, and has no insecure fallback.
- Affected-surface selection and CI job routing remain those approved in Spec
  031; only domain validator commands are added.
- Required repo-static gates pass, optional SKIP/fallback are separate, and all
  remote/live lanes remain DEFER.
- Independent review and rollback commit are recorded without secret values.

## Traceability

- [Protected Surface and Supply Chain Hardening Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Protected Surface and Supply Chain Hardening Task](../tasks/2026-07-12-protected-surface-supply-chain-hardening.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Workspace Document Assurance PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Workspace Document Assurance ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Current Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
- [Kubernetes Infrastructure and Security Audit](../../90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md)
- [GitHub Actions Secure Use](https://docs.github.com/en/actions/reference/security/secure-use)
- [OpenGitOps Principles](https://opengitops.dev/)
- [External Secrets Security Best Practices](https://external-secrets.io/v2.0.0/guides/security-best-practices/)
- [Vault Production Hardening](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)
