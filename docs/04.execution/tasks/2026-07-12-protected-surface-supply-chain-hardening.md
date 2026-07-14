---
title: 'Task: Protected Surface and Supply Chain Hardening'
type: sdlc/task
status: active
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
| PSH-005 | Harden local Vault/ESO and bootstrap secret handling | security | Vault fixture, static contracts, secret scan | platform | Pending |
| PSH-006 | Close repository-static evidence and lifecycle | doc | Full QA bundle and independent review | platform | Pending |

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
GREEN requires the Spec, Plan, and Task to name one another, one Active index
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
self-test passes,
while repository mode intentionally remains RED for PSH-003 with fourteen
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
pre-commit, and diff checks pass. The final handoff is the exact sixteen-path
staged set with no unstaged tracked changes and unchanged HEAD. Reviewer
disposition is worker self-review PASS and controller review pending; rollback
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
exact three fixture rows and all 91 repository identities. Fresh correction
verification and independent re-review are required before commit; remote CI
and live Argo CD evidence remain DEFER.

## Traceability

- [Protected Surface and Supply Chain Hardening Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Protected Surface and Supply Chain Hardening Plan](../plans/2026-07-12-protected-surface-supply-chain-hardening.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Workspace Document Assurance PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Workspace Document Assurance ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Current Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
