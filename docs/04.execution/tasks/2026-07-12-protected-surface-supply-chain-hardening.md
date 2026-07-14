---
title: 'Task: Protected Surface and Supply Chain Hardening'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-14
---

# Task: Protected Surface and Supply Chain Hardening

## Overview

This Task tracks six bounded changes that harden protected repository surfaces
without claiming remote or live-system readiness. PSH-001 establishes the
reciprocal Spec, Plan, Task, and Stage-index chain. PSH-002 through PSH-006 add
fixture-tested Action, GitOps, Vault/ESO, bootstrap, secret-handling, and
repository-static closure evidence in dependency order.

## Inputs

- **Parent Spec**: [Protected Surface and Supply Chain Hardening Technical Specification](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- **Parent Plan**: [Protected Surface and Supply Chain Hardening Implementation Plan](../plans/2026-07-12-protected-surface-supply-chain-hardening.md)
- **QA Baseline**: Completed Spec 031 owns affected-surface selection, local/CI
  parity, cross-provider role semantics, and the Stage 00 QA handoff.
- **Security Baseline**: Official GitHub Actions, OpenGitOps, External Secrets,
  Vault, and Kubernetes guidance referenced by the parent Spec defines the
  reviewed repository-static boundaries.

## Task Table

| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| PSH-001 | Start reciprocal execution evidence | doc | Reciprocal-link assertion | platform | Done |
| PSH-002 | Add Action identity and permission validator | guardrail | Action fixture self-test | platform | Done |
| PSH-003 | Pin eight Action identities and minimize workflow permissions | ci | Action validator, actionlint, zizmor | platform | Done |
| PSH-004 | Add GitOps identity and deletion change-set review | guardrail | GitOps fixture self-test | platform | Done |
| PSH-005 | Harden local Vault/ESO and bootstrap secret handling | security | Vault fixture, static contracts, secret scan | platform | Done |
| PSH-006 | Close repository-static evidence and lifecycle | doc | Full QA bundle and independent review | platform | Done |

## Approval and Safety Boundaries

- **Allowed Paths**: Each logical unit is limited to the exact `Files` list in
  the parent Plan. PSH-001 changes only this Task, its parent Spec and Plan, and
  their three Stage indexes plus the Task's one durable-ledger row.
- **Forbidden Paths**: Provider credentials, authentication state, ignored
  certificates or local settings, secret values, kubeconfigs, generated local
  output, and paths outside the active Plan unit are excluded.
- **Approval Required**: Human approval is required before push, merge, remote
  workflow execution, certificate or credential change, GitOps reconciliation,
  Kubernetes apply, Vault request, or other live operator action.
- **Static Validation**: Run the exact RED/GREEN fixture or assertion for the
  active PSH row, its focused validator commands, repository quality gates,
  pre-commit, diff checks, exact staged-path proof, and independent review where
  required by the parent Plan.
- **Live Validation**: DEFER. Repository-static checks do not prove GitHub
  remote behavior, Argo CD prune or reconciliation, ESO authentication, Vault
  TLS/runtime behavior, or Kubernetes authorization.
- **Secret / Vault Handling**: Do not read, print, decode, enumerate, move, or
  modify secret values, tokens, certificates, Vault data, provider auth files,
  shell history, or ignored local state.
- **Rollback Plan**: Revert completed PSH logical commits newest-first. Keep
  validators and their consumers in the same owning unit or revert consumers
  before their contracts.
- **Evidence Location**: This Task, its parent Spec and Plan, logical commits,
  repository-static validator output, and ignored `.superpowers/sdd/psh*-report.md`
  review packages.
- **GitOps Impact**: PSH-004 reviews rendered identity and deletion candidates
  only; it does not apply, prune, or reconcile desired state.
- **Kubernetes Impact**: No live cluster mutation is authorized.
- **Operations / Runbook Impact**: PSH-005 may align tracked local-only security
  contracts and runbook evidence only within its exact Plan boundary.

## Verification Summary

PSH-001 began from the expected RED state: the canonical Task path did not
exist, so the reciprocal-lineage assertion exited 1 before inspecting links.
Its GREEN gate required the Spec, Plan, and Task to name one another, one Active index
row dated 2026-07-12 for each document, the exact PSH-001 through PSH-006 table,
one exact fourteen-column durable-ledger row, strict document conformance, the
full repository quality gate, focused pre-commit, and exactly seven staged
paths with no unstaged tracked changes. This evidence is repository-static;
remote and live lanes remain DEFER.

PSH-002 added the duplicate-key-rejecting Action identity and permission
validator plus its exact eleven-case primary fixture. Ten supplemental
repository-boundary cases reject missing/empty roots and directories,
root/directory/file symlinks, non-regular workflow inputs, and a symlinked
zizmor file before external content can be read. Twenty-one supplemental
required-write cases cover two positive shapes and five mutations for each of
the three named workflow/job consumers, so removing a job, permissions map, or
required write cannot pass. Four internal non-string `uses` mutations prove
numeric, null, mapping, and list values cannot disappear from both parser
views; an internal quoted-local positive preserves valid quoted same-line
behavior without changing the 11/10/21 JSON cardinalities. The fixture
self-test passed. At that tranche boundary, repository mode intentionally
remained RED for PSH-003 with fourteen
mutable remote occurrences, missing top-level `contents: read` defaults in
`greetings.yml`, `labeler.yml`, and `stale.yml`, and the tracked
`unpinned-uses` suppression: eighteen bounded findings in total. ASQA-004 had
already removed `dorny/paths-filter`, so the parent Plan's stale fifteen/nine
cardinalities were corrected to fourteen/eight, with five checkout, three
setup-python, and six remaining occurrences. The Action validator is not part
of the aggregate repository quality gate until PSH-003 turns this evidence
green; no workflow, suppression, remote dispatch, or live state changed here.

PSH-003 pinned all fourteen remote `uses:` occurrences to the eight reviewed
forty-character SHAs with same-line version comments, synchronized the Action
inventory to those immutable identities, and preserved Dependabot's weekly
grouped `github-actions` proposal route. All five workflows now default to
`contents: read`; only the exact greeting, label, and stale jobs retain their
required issue or pull-request writes. The obsolete zizmor suppression file was
deleted, and the fail-closed Action validator now runs inside the aggregate
repository quality gate. A pre/post structural comparison preserved the exact
Spec 031 `changes` outputs, job IDs, `needs`, and `if` expressions. Repository-
static Action validation, actionlint, zizmor, aggregate quality, and diff checks
pass; official upstream tag/SHA resolution was independently reconfirmed on
2026-07-14. No secret, remote workflow, push, merge, or live state was accessed
or changed; remote/live evidence remains DEFER.

PSH-004 added an identity-only GitOps resource graph and wired it into only the
existing `gitops/**` validator surface, `manifest-static`, the local harness,
and the aggregate repository quality gate. The exact fixture output is one
ADD, one DELETE, and one path-only RETAIN; the sentinel and all forbidden
manifest body keys are absent. Local `--base-ref HEAD` comparison emitted 91
RETAIN rows matching only the exact identity-row grammar, with empty stderr and
no `data`, `spec`, `metadata`, or `stringData` body output. A normalized
pre/post workflow comparison proved the name, three triggers, changes outputs,
ordered six job IDs, every `needs` and `if`, and the complete selector step are
unchanged; removing the one new manifest step makes the workflow equivalent as
parsed YAML. Acceptance `PSH-004` and `VAL-PLN-004` are PASS: focused boundary
probes, exact fixture/forbidden checks, affected-surface self-test and repository
coverage, GitOps structure, 104-manifest YAML and kube-linter validation,
aggregate quality, actionlint, strict document checks, focused exact-path
pre-commit, and diff checks pass. The initial handoff was the exact sixteen-path
staged set with no unstaged tracked changes and unchanged HEAD. Reviewer
disposition at that checkpoint was worker self-review PASS with controller
review pending; rollback
before commit is to unstage and remove only the exact staged unit, while
rollback after a future commit is one commit revert. No commit, remote
workflow, secret, credential, cluster, Argo CD, Vault, ESO, publish, push,
merge, or third-party mutation ran; CI remote and all live lanes remain DEFER.
Residual risk is limited to remote GitHub and live Argo CD behavior, and the
next owner is the controller/protected reviewer.

The independent pre-commit review then blocked the first PSH-004 handoff on
history checkout/base selection, serialized-token grammar, Kustomization
dialect, and durable negative coverage. The correction keeps the exact sixteen
paths and Spec 031 routing invariant: `manifest-static` now uses
`fetch-depth: 0` with credentials disabled, and its base expression covers PR,
push (including forty-zero), and workflow dispatch. Forty-zero distinguishes a
true root from an unavailable shallow parent by inspecting the HEAD commit
object and verifying its first parent. All identity/path fields are validated
before serialization, only the current `kustomize.config.k8s.io/v1beta1`
Kustomization pair is accepted, and the tracked `--self-test` now executes the
full negative renderer and temporary Git-history matrix while preserving the
exact three fixture rows and all 91 repository identities. The corrected unit
then passed focused verification and independent re-review before commit;
remote CI and live Argo CD evidence remain DEFER.

PSH-005 adds an exact ten-case Vault/ESO validator and repository loader,
marks the in-cluster HTTP store/Service/EndpointSlice boundary as local-only,
sets the ESO identity and audience to `external-secrets/external-secrets` and
`vault`, and hardens bootstrap secret transport. The bootstrap now requires an
HTTPS Vault address and readable `VAULT_CA_FILE`, prompts silently through
`/dev/tty`, sends the token header and generated Kubernetes Secret value
through stdin, and has no noninteractive or insecure fallback. The external
Vault operator must separately configure `bound_audiences=vault`; local-only
HTTP is not production TLS. The exact one-subject TokenReview binding and
six-block read/list HCL remained byte-identical.

The four exact documentation batches removed active token export/inlining,
secret-bearing insecure curl, credential argv, and password-literal examples.
The affected-surface registry adds `vault-eso-contracts` only to the five
bootstrap, HCL, and ESO/Vault manifest consumers while preserving every other
path selection and all CI job outputs. `manifest-static` adds only
`python3 scripts/validate-vault-eso-contracts.py --root .` adjacent to the
existing secret-handling command; the workflow name, three triggers, six job
IDs, every `needs`/`if`, and the three `changes` outputs are unchanged. The
local harness and repository quality gate run both self-test and repository
mode, and the script/test/GitOps/infrastructure inventories own the command and
operator boundaries.

Acceptance `PSH-005` and `VAL-PLN-005` are repo-static PASS for the ten-case
self-test, repository mode, bootstrap/static shell syntax, exact static
contracts, secret handling, policy fallback, 104-manifest validation,
affected-surface self-test/repository coverage, strict Markdown/link checks,
repository quality, actionlint, shellcheck, focused pre-commit, harness, and
diff hygiene. Plan correction `0a3cf2f` replaced the overbroad unsafe-example
probe with two bounded acceptance searches: the exact bootstrap plus seven
authorized operational documents for insecure transport, environment, and
literal-secret forms, and the seven operational documents for token-header
argv forms. Both corrected searches return exit `1` with no output; the three
unrelated, unauthenticated local UI probes remain outside PSH-005 scope. The
actual working scope is the exact twenty-two authorized paths because the
TokenReview binding and verify-only HCL remain byte-identical. The first
independent review reported C0/H0/M4/L0 and two bounded re-reviews exposed
remaining structural-validator bypasses. The v4 correction closes the curl
configuration, dependency-discovery, xtrace, and sensitive-use boundaries
with durable negative regressions; final independent re-review approved the
staged unit at C0/H0/M0/L0. Remote CI, live Kubernetes, Argo CD, Vault, ESO,
production TLS, and external operator evidence remain DEFER. No secret,
credential, ignored certificate, runtime setting, shell history, live system,
remote workflow, push, merge, or third-party state was accessed or changed.

### PSH-006 Repository-Static Closure Evidence

The following table is the rerunnable evidence record for the completed
PSH-001 through PSH-006 tranche. Results were captured on 2026-07-14 KST at
PSH-005 head `2b1e56775883a596be3f13fca1cabe1cb2680133`; the PSH-006 closing commit
cannot embed its own content-addressed SHA.

| Evidence | Result | Command or boundary |
| --- | --- | --- |
| Affected-surface fixture | PASS | `python3 scripts/validate-affected-surfaces.py --self-test` |
| Affected-surface repository | PASS | `python3 scripts/validate-affected-surfaces.py --root .` |
| Action-security fixture | PASS | `python3 scripts/validate-github-actions-security.py --self-test` |
| Action-security repository | PASS | `python3 scripts/validate-github-actions-security.py --root .` |
| GitOps change-set fixture | PASS | `python3 scripts/validate-gitops-change-set.py --self-test`; exact one ADD, one DELETE, and one path-only RETAIN, no manifest values |
| GitOps repository review | PASS | `python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD`; 91 RETAIN identity-only rows, no manifest values |
| Vault/ESO fixture | PASS | `python3 scripts/validate-vault-eso-contracts.py --self-test`; exact 10 cases |
| Vault/ESO repository | PASS | `python3 scripts/validate-vault-eso-contracts.py --root .` |
| Infrastructure static contracts | PASS | `bash infrastructure/tests/verify-contracts-static.sh` |
| GitOps structure | PASS | `bash scripts/validate-gitops-structure.sh` |
| Kubernetes manifests | PASS | `bash scripts/validate-k8s-manifests.sh .`; YAML plus installed kube-linter across 104 files |
| kube-linter | PASS | Installed at `/home/hy/.local/bin/kube-linter`; full 104-file lint ran, version output `development` |
| Secret handling | PASS | `bash scripts/check-secret-handling.sh .`; 100 files, no plaintext secret pattern |
| Policy gates | PASS | `bash scripts/validate-policy-gates.sh .` |
| Conftest | SKIP | `command -v conftest` exited 1; Conftest was unavailable and is not represented as PASS |
| Built-in policy fallback | PASS | Ran separately inside `bash scripts/validate-policy-gates.sh .` after the Conftest SKIP |
| Shell syntax | PASS | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` |
| Repository quality | PASS | `bash scripts/validate-repo-quality-gates.sh .` |
| All-files pre-commit | PASS | `pre-commit run --all-files`; applicable hooks passed and Dockerfile lint was a no-file SKIP |
| Diff hygiene | PASS | `git diff --check` |
| Independent review | PASS | Whole-tranche reviewer disposition C0/H0/M0/L0 for PSH-001 through PSH-005 |
| Secret-value access | none | No secret, credential, ignored certificate, auth state, kubeconfig, shell history, token cache, or secret value was read or emitted |
| Rollback | PASS | First-parent commit before PSH-001: `05e2b7050b8d150ec46eddf731bf28283bd11c04`; revert PSH commits newest-first |
| Remote/live | DEFER | Remote GitHub execution, live Argo CD prune/reconcile, Vault/ESO authentication and TLS runtime, and Kubernetes authorization were not run |
| External Vault role | DEFER | Apply `bound_audiences=vault` through a separately approved operator change |
| Credential rotation | DEFER | No credential was read, written, or rotated |
| Rollback rehearsal | DEFER | No live rollback or recovery rehearsal was executed |

The seven first-parent implementation commits before closure are PSH-001
`a2aa49f200b0b6bd36fe67ee469d17a971297430`, PSH-002
`1a3f94cab4d9bba07b73db612e083e78fe0b4630`, PSH-003 Plan correction
`b26893670024b6f8e57ad7923783e573ad391d8c`, PSH-003
`2bce69fd6ddb850a94f886ef8906ce436a937cea`, PSH-004
`82679a4c977716dbb968fd37b8a901cd86e036af`, PSH-005 Plan correction
`0a3cf2faffb039b6c26f22b657ecd36577c47e67`, and PSH-005
`2b1e56775883a596be3f13fca1cabe1cb2680133`.

## Traceability

- [Protected Surface and Supply Chain Hardening Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Protected Surface and Supply Chain Hardening Plan](../plans/2026-07-12-protected-surface-supply-chain-hardening.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Workspace Document Assurance PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Workspace Document Assurance ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Current Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
