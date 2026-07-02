# Reference: Harness Implementation Map

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

## Control / Governance

| Surface             | Source                                                          | Role                              | Required Validation                        | Evidence             |
| ------------------- | --------------------------------------------------------------- | --------------------------------- | ------------------------------------------ | -------------------- |
| Thin gateways       | `AGENTS.md`, root `CLAUDE.md`, `GEMINI.md`                      | Route to governance; stay shims   | `scripts/validate-repo-quality-gates.sh .` | `memory/progress.md` |
| Bootstrap + JIT     | `rules/bootstrap.md`                                            | Universal entry, loading sequence | repo-quality-static                        | PR / task evidence   |
| Pre/Postflight      | `rules/preflight-checklist.md`, `rules/postflight-checklist.md` | Before/after edit gates           | manual checklist                           | task / PR            |
| Agentic contract    | `rules/agentic.md`                                              | Agent-first execution rules       | repo-quality-static                        | `memory/progress.md` |
| Approval boundaries | [`rules/approval-boundaries.md`](rules/approval-boundaries.md)  | Single approval matrix            | repo-quality-static                        | task / PR            |

## Harness Catalog / Runtime Roster

| Surface             | Source                                                               | Role                               | Required Validation                          | Evidence             |
| ------------------- | -------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------- | -------------------- |
| Runtime roster SSOT | [`harness-catalog.md`](harness-catalog.md)                           | Agents, skills, mirrors, matrices  | repo-quality-static (mirror + matrix checks) | `memory/progress.md` |
| Model tier policy   | `model-policy.md`                                                    | Supervisor/worker model tiers      | repo-quality-static                          | catalog              |
| Adapter parity      | `.claude/agents/*.md`, `.codex/agents/*.toml`, `.agents/agents/*.md` | Provider-native agents + mirrors   | agent mirror checks in repo-quality-static   | catalog              |
| Shared assets       | `.agents/{skills,workflows,output-styles}`                           | Provider-neutral SSoT via symlinks | repo-quality-static                          | catalog              |

## GitOps Runtime

| Surface              | Source                                                               | Role                              | Required Validation                                                        | Evidence           |
| -------------------- | -------------------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------- | ------------------ |
| App-of-Apps          | `gitops/clusters/local/root-application.yaml`, `gitops/apps/root/**` | Root Application + ApplicationSet | `scripts/validate-gitops-structure.sh`                                     | manifest-static CI |
| AppProjects          | `gitops/clusters/local/appproject-*.yaml`                            | Project boundaries, allow-lists   | `scripts/validate-gitops-structure.sh`, `scripts/validate-policy-gates.sh` | manifest-static CI |
| Platform / workloads | `gitops/platform/**`, `gitops/workloads/**`                          | Desired-state manifests           | `scripts/validate-k8s-manifests.sh .`                                      | manifest-static CI |

## Kubernetes Static Validation

| Surface          | Source                                            | Role                               | Required Validation | Evidence           |
| ---------------- | ------------------------------------------------- | ---------------------------------- | ------------------- | ------------------ |
| Manifest syntax  | `scripts/validate-k8s-manifests.sh`               | YAML syntax + optional kube-linter | run script          | manifest-static CI |
| Static contracts | `infrastructure/tests/verify-contracts-static.sh` | Repo-static infra contract checks  | run script          | manifest-static CI |

## Policy Gates

| Surface     | Source                                                                | Role                                                                                | Required Validation               | Evidence           |
| ----------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------- | ------------------ |
| Policy gate | `scripts/validate-policy-gates.sh`, `policy/conftest/kubernetes.rego` | Block plaintext Secret, `CreateNamespace=true`, AppProject wildcard, `latest` image | run script (Conftest or fallback) | manifest-static CI |

## Secret / Vault / External Secrets

| Surface           | Source                                                                     | Role                                   | Required Validation                   | Evidence           |
| ----------------- | -------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------- | ------------------ |
| Plaintext scan    | `scripts/check-secret-handling.sh`                                         | Reject plaintext Secret manifests      | run script (redacted findings)        | manifest-static CI |
| ESO / SecretStore | `gitops/platform/eso/**`, `gitops/platform/external-services/vault-*.yaml` | ExternalSecret / SecretStore contracts | `scripts/validate-k8s-manifests.sh .` | manifest-static CI |
| Example contract  | `examples/sample-app/external-secret.yaml`                                 | App onboarding secret path contract    | repo-quality-static                   | manifest-static CI |

## Bootstrap Boundary

| Surface           | Source                                                                  | Role                             | Required Validation                               | Evidence         |
| ----------------- | ----------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------- | ---------------- |
| Local bootstrap   | `infrastructure/bootstrap-local.sh`, `infrastructure/k3d/**`            | Operator-bound cluster bootstrap | static review only; live run is operator-approved | runbook evidence |
| Bootstrap runbook | `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md` | Approved bootstrap procedure     | n/a (human/operator path)                         | runbook record   |

## CI

| Surface     | Source                             | Role                                                            | Required Validation | Evidence      |
| ----------- | ---------------------------------- | --------------------------------------------------------------- | ------------------- | ------------- |
| CI gates    | `.github/workflows/ci.yml`         | branch-policy, repo-quality-static, manifest-static, ci-summary | CI run on PR        | GitHub checks |
| PR contract | `.github/PULL_REQUEST_TEMPLATE.md` | Harness Impact + static/live evidence split                     | repo-quality-static | PR body       |

## Evidence / Progress

| Surface         | Source                                                     | Role                                 | Required Validation | Evidence   |
| --------------- | ---------------------------------------------------------- | ------------------------------------ | ------------------- | ---------- |
| Progress ledger | `docs/00.agent-governance/memory/progress.md`              | Repo-changing work + reusable memory | repo-quality-static | itself     |
| Plans / tasks   | `docs/04.execution/plans/**`, `docs/04.execution/tasks/**` | Execution + validation evidence      | repo-quality-static | stage docs |

## Operations / Runbooks

| Surface  | Source                           | Role                                     | Required Validation | Evidence        |
| -------- | -------------------------------- | ---------------------------------------- | ------------------- | --------------- |
| Policies | `docs/05.operations/policies/**` | Operational controls and boundaries      | repo-quality-static | policy docs     |
| Runbooks | `docs/05.operations/runbooks/**` | Bootstrap, recovery, rollback procedures | repo-quality-static | runbook records |

## Live Runtime Evidence

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
- [Harness Task Contract Template](../99.templates/templates/sdlc/specs/harness-task-contract.template.md)
- [Operations Hub](../05.operations/README.md)
