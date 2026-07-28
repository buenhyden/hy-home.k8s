---
title: 'Reference: Harness Implementation Map'
type: governance/reference
status: active
owner: platform
updated: 2026-07-28
---

# Reference: Harness Implementation Map

## Overview

This document is a navigation map for where harness engineering is implemented in
`hy-home.k8s`. It is **not** a policy source. Each row points to an existing
canonical owner (governance doc, manifest, script, workflow, or runbook). When a
control and this map disagree, the canonical owner wins and this map is updated.

Use it to answer one question quickly: _for a given harness surface, what is the
source of truth, what role does it play, how is it validated statically, and
where is the evidence recorded?_

- `Required Validation` lists repo-static commands or gates, not live-cluster checks.
- `Evidence` points to where results are recorded, not to live runtime health.
- Repo-static `Ready` never means live ArgoCD, Vault, ESO, or deployment readiness.

## Authority Boundary

### Control / Governance

| Surface             | Source                                                          | Role                              | Required Validation                        | Evidence             |
| ------------------- | --------------------------------------------------------------- | --------------------------------- | ------------------------------------------ | -------------------- |
| Thin gateways       | `AGENTS.md`, root `CLAUDE.md`, `GEMINI.md`                      | Route to governance; stay shims   | `scripts/validate-repo-quality-gates.sh .` | `memory/progress.md` |
| Bootstrap + JIT     | `rules/bootstrap.md`                                            | Universal entry, loading sequence | repo-quality-static                        | PR / task evidence   |
| Pre/Postflight      | `rules/preflight-checklist.md`, `rules/postflight-checklist.md` | Before/after edit gates           | manual checklist                           | task / PR            |
| Agentic contract    | `rules/agentic.md`                                              | Agent-first execution rules       | repo-quality-static                        | `memory/progress.md` |
| Approval boundaries | [`rules/approval-boundaries.md`](rules/approval-boundaries.md)  | Single approval matrix            | repo-quality-static                        | task / PR            |

## Governance Context

### Harness Catalog / Runtime Roster

| Surface             | Source                                                               | Role                               | Required Validation                          | Evidence             |
| ------------------- | -------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------- | -------------------- |
| Runtime machine contract | [`contracts/harness-contract.json`](contracts/harness-contract.json) | Role semantics, permissions, evidence, memory, current/target inventory, and consumers | harness, role-semantic, roster-currentness, and affected-surface checks | owning Task and `memory/progress.md` |
| Runtime catalog view | [`harness-catalog.md`](harness-catalog.md)                           | Human-readable agents, skills, adapters, and matrices derived from the machine contract | repo-quality-static (adapter + matrix checks) | `memory/progress.md` |
| Model tier policy   | `model-policy.md`                                                    | Supervisor/worker model tiers      | repo-quality-static                          | catalog              |
| Adapter parity      | `.claude/agents/*.md`, `.codex/agents/*.toml`, `.agents/agents/*.md` | Native Claude/Codex plus local/Antigravity adapters; static parity only | agent adapter checks in repo-quality-static  | catalog              |
| Shared assets       | `.agents/{skills,workflows,output-styles}`                           | Provider-neutral SSoT via symlinks | repo-quality-static                          | catalog              |

## Current Contract

### GitOps Runtime

| Surface              | Source                                                               | Role                              | Required Validation                                                        | Evidence           |
| -------------------- | -------------------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------- | ------------------ |
| App-of-Apps          | `gitops/clusters/local/root-application.yaml`, `gitops/apps/root/**` | Root Application + ApplicationSet | `scripts/validate-gitops-structure.sh`                                     | manifest-static CI |
| AppProjects          | `gitops/clusters/local/appproject-*.yaml`                            | Project boundaries, allow-lists   | `scripts/validate-gitops-structure.sh`, `scripts/validate-policy-gates.sh` | manifest-static CI |
| Platform / workloads | `gitops/platform/**`, `gitops/workloads/**`                          | Desired-state manifests           | `scripts/validate-k8s-manifests.sh .`                                      | manifest-static CI |

### Kubernetes Static Validation

| Surface          | Source                                            | Role                               | Required Validation | Evidence           |
| ---------------- | ------------------------------------------------- | ---------------------------------- | ------------------- | ------------------ |
| Manifest syntax  | `scripts/validate-k8s-manifests.sh`               | YAML syntax + optional kube-linter | run script          | manifest-static CI |
| Static contracts | `infrastructure/tests/verify-contracts-static.sh` | Repo-static infra contract checks  | run script          | manifest-static CI |

### Policy Gates

| Surface     | Source                                                                | Role                                                                                | Required Validation               | Evidence           |
| ----------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------- | ------------------ |
| Policy gate | `scripts/validate-policy-gates.sh`, `policy/conftest/kubernetes.rego` | Block plaintext Secret, `CreateNamespace=true`, AppProject wildcard, `latest` image | run script (Conftest or fallback) | manifest-static CI |

### Secret / Vault / External Secrets

| Surface           | Source                                                                     | Role                                   | Required Validation                   | Evidence           |
| ----------------- | -------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------- | ------------------ |
| Plaintext scan    | `scripts/check-secret-handling.sh`                                         | Reject plaintext Secret manifests      | run script (redacted findings)        | manifest-static CI |
| ESO / SecretStore | `gitops/platform/eso/**`, `gitops/platform/external-services/vault-*.yaml` | ExternalSecret / SecretStore contracts | `scripts/validate-k8s-manifests.sh .` | manifest-static CI |
| Example contract  | `examples/sample-app/external-secret.yaml`                                 | App onboarding secret path contract    | repo-quality-static                   | manifest-static CI |

### Bootstrap Boundary

| Surface           | Source                                                                  | Role                             | Required Validation                               | Evidence         |
| ----------------- | ----------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------- | ---------------- |
| Local bootstrap   | `infrastructure/bootstrap-local.sh`, `infrastructure/k3d/**`            | Operator-bound cluster bootstrap | static review only; live run is operator-approved | runbook evidence |
| Bootstrap runbook | `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md` | Approved bootstrap procedure     | n/a (human/operator path)                         | runbook record   |

### CI

| Surface     | Source                             | Role                                                            | Required Validation | Evidence      |
| ----------- | ---------------------------------- | --------------------------------------------------------------- | ------------------- | ------------- |
| CI gates    | `.github/workflows/ci.yml`         | Collect push/PR paths as NUL records with rename detection disabled so old/new protection domains are retained, select pre-commit, repo-quality-static, and manifest-static from the affected-surface contract, then aggregate unchanged job results in ci-summary | affected-surface rename proof plus actionlint; remote execution remains separate evidence | GitHub checks |
| PR contract | `.github/PULL_REQUEST_TEMPLATE.md` | Harness Impact + static/live evidence split                     | repo-quality-static | PR body       |

### Affected-Surface Selection

| Surface | Source | Role | Required Validation | Evidence |
| --- | --- | --- | --- | --- |
| Path contract | `contracts/validation-surfaces.json`, adjacent schema | Map one normalized tracked path to exactly one surface, argv validators, lanes, CI jobs, protection, fallback, evidence class, and exact affected-Markdown path-input consumers | `python3 scripts/validate-affected-surfaces.py --root .` | Spec 031 Task |
| Selector and fixture | `scripts/select-affected-surfaces.py`, `tests/fixtures/validation-surfaces.json` | Preserve NUL path records, compare push/PR and rename range cases to exact CI job booleans, and emit deterministic JSON or GitHub output without shell evaluation or first-match precedence | `python3 scripts/validate-affected-surfaces.py --self-test` | Spec 031 Task |

### Agent Role and QA Evidence

| Surface | Source | Role | Required Validation | Evidence |
| --- | --- | --- | --- | --- |
| Harness contract | `contracts/harness-contract.json`, adjacent schema | Own the closed role, permission, evidence, consumer, and four-class memory contract; current inventory is exactly `10/3/30`, while `12/4/48` remains target-only | `python3 scripts/validate-agent-harness-contract.py --self-test` and `--root .` | Spec 041 Task |
| Role semantics | `contracts/harness-contract.json` `adapterSemantics`, thirty tracked role adapters | Own shared responsibility, output, prohibition, stop, handoff, capability-tier, and evidence claims across `local`, `claude`, and `codex` without copying surface model/tool/effort metadata | `python3 scripts/validate-agent-role-semantics.py --self-test` and `--root .` | Spec 041 Task |
| Surface metadata and roster | `contracts/harness-contract.json`, native Claude/Codex plus local/Antigravity adapters | Preserve surface-owned model/tool/effort fields, exact ten-role stems, thirty current adapters, and scope imports; Gemini native and the twelve-role/four-surface/forty-eight-adapter inventory remain target-only | harness validator, repository quality gate, and roster-currentness validator | Spec 041 Task |
| Legacy readability | `contracts/agent-role-semantics.json` and adjacent schema | Readable compatibility input with zero semantic consumers; removal remains Spec 045-owned | harness compatibility check | Spec 045 Task |
| Lane, result, and handoff contract | `rules/quality-standards.md`, `rules/postflight-checklist.md` | Define `affected`, `staged`, `all-files`, `message/manual`, `ci`, `remote/live`; require `PASS`/`SKIP`/`FAIL`/`DEFER` and complete handoff fields | postflight review and repository quality gate | owning Task and `memory/progress.md` |

Tracked gateway, hook, and role-adapter files are repository configuration.
They are not evidence that a native provider discovered, loaded, or enforced
those files; provider-runtime evidence remains a separate lane.

### Evidence / Progress

| Surface         | Source                                                     | Role                                 | Required Validation | Evidence   |
| --------------- | ---------------------------------------------------------- | ------------------------------------ | ------------------- | ---------- |
| Progress ledger | `docs/00.agent-governance/memory/progress.md`              | Repo-changing work + reusable memory | repo-quality-static | itself     |
| Memory classes  | `contracts/harness-contract.json`, `memory/README.md`      | Declare working short-term, durable long-term, domain-scoped, and provider-local auxiliary authority | harness contract check; executable lifecycle deferred to Spec 043 | owning Task |
| Plans / tasks   | `docs/04.execution/plans/**`, `docs/04.execution/tasks/**` | Execution + validation evidence      | repo-quality-static | stage docs |

### Operations / Runbooks

| Surface  | Source                           | Role                                     | Required Validation | Evidence        |
| -------- | -------------------------------- | ---------------------------------------- | ------------------- | --------------- |
| Policies | `docs/05.operations/policies/**` | Operational controls and boundaries      | repo-quality-static | policy docs     |
| Runbooks | `docs/05.operations/runbooks/**` | Bootstrap, recovery, rollback procedures | repo-quality-static | runbook records |

## Validation and Refresh

### Live Runtime Evidence

| Surface           | Source                                                                | Role                                 | Required Validation                          | Evidence                  |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------- | ------------------------- |
| Live verification | `infrastructure/tests/run-all.sh`, `infrastructure/tests/verify-*.sh` | k3d / ArgoCD / ESO / TLS live checks | **operator-approved only**, not default path | runbook / incident record |

Live runtime evidence is separated from repo-static validation. Running it
requires an approved operations procedure; skipped live checks are reported
explicitly with their reason.

## Related Documents

- [Local Harness Catalog](harness-catalog.md)
- [Approval Boundaries](rules/approval-boundaries.md)
- [Bootstrap Governance](rules/bootstrap.md)
- [Canonical Task Approval and Safety Boundaries](../99.templates/templates/sdlc/execution/task.template.md#approval-and-safety-boundaries)
- [Operations Hub](../05.operations/README.md)
