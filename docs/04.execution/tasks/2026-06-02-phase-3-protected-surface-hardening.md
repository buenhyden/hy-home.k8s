---
title: 'Task: Phase 3 Protected Surface Hardening'
type: task
status: done
owner: platform
updated: 2026-06-02
---

# Task: Phase 3 Protected Surface Hardening

## Overview (KR)

이 문서는 Phase 3 protected surface hardening의 작업 단위와 검증 증거를 추적한다.
작업 범위는 승인된 policy, runtime hook, CI, template, CI topology, model policy, provider config, GitOps manifest, live validation 범위를 검토·적용하는 것이다.
Concrete drift가 없는 model policy, provider config, GitOps manifest는 no-op으로 기록하며, live cluster mutation이나 secret-value inspection은 포함하지 않는다.

## Inputs

- **Parent Plan**: [Phase 3 Protected Surface Hardening Plan](../plans/2026-06-02-phase-3-protected-surface-hardening.md)
- **Phase 2 Plan**: [Phase 2 Governance Alignment Plan](../plans/2026-06-02-phase-2-governance-alignment.md)
- **Phase 1 Audit Evidence**: [Phase 1 Governance Alignment Audit Task](./2026-06-02-phase-1-governance-alignment-audit.md)
- **Governance Decision**: [ADR-0013: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)

## Working Rules

- Preserve ADR-0013 and the Stage 00 canonical adapter model.
- Treat `.agents/**` as the shared asset SSoT for skills, workflows, output styles, and Gemini hook wiring.
- Policy, runtime hook, CI, template, CI topology, model policy, provider config, GitOps manifest, and live validation are approved for this Phase 3 scope.
- Do not perform cluster mutation, deployment, external Vault mutation, secret-value inspection, private RTK database, publish, or destructive Git actions.
- Documentation-only and guardrail work still needs validation evidence.
- Repo-static validation must not be reported as live runtime readiness unless a separate live check was approved and run.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add `.agents/**` to CI repo-quality path filter | guardrail | N/A | PLN-001 | `bash scripts/validate-repo-quality-gates.sh .`; targeted `.agents/**` scan | platform | Done |
| T-002 | Add `.agents/*` repo-quality matching to post/lifecycle hooks | guardrail | N/A | PLN-002 | `bash -n ...`; targeted hook scan | platform | Done |
| T-003 | Parse `.agents/hooks.json` in runtime JSON validation lanes | guardrail | N/A | PLN-002 | `bash scripts/validate-repo-quality-gates.sh .`; targeted `.agents/hooks.json` scan | platform | Done |
| T-004 | Clarify read-only SessionStart live probe boundary | runtime | N/A | PLN-003 | SessionStart wording scan and approved read-only live probe output | platform | Done |
| T-005 | Add non-structural live-readiness boundary guidance to templates/docs | doc | N/A | PLN-004 | Template heading remains unchanged; repo quality gate passes | platform | Done |
| T-006 | Record Phase 3 artifacts, indexes, links, and progress evidence | doc | N/A | PLN-005 | Phase 3 README/index scan and progress ledger update | platform | Done |
| T-007 | Record protected-surface no-op decisions and approved read-only live validation | eval | N/A | PLN-006 | Live validation command output or limitation; no model/provider/GitOps manifest diff without drift | platform | Done |

## Suggested Types

- `guardrail`
- `runtime`
- `doc`
- `eval`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 3

- [x] T-001 CI shared asset trigger
- [x] T-002 Runtime hook repo-quality trigger
- [x] T-003 Runtime hook JSON parse lane
- [x] T-004 SessionStart readiness boundary
- [x] T-005 Template and governance guidance
- [x] T-006 Execution evidence and index sync
- [x] T-007 Protected-surface no-op decisions and live validation

## Verification Summary

- **Test Commands**:
  - `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh` — PASS.
  - `git diff --check` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS.
  - `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1 bash docs/00.agent-governance/hooks/session-start.sh` — PASS command exit 0; reported k3d `hyhome` present, three Terminating pods, and Degraded ArgoCD apps `adminer`, `platform-argocd-config`, and `platform-eso-config`.
  - `bash infrastructure/tests/run-all.sh` — FAIL at ESO/Vault integration: `vault-backend Ready is not True (actual=False)`.
  - `bash infrastructure/tests/verify-external-services.sh` — PASS.
  - `bash infrastructure/tests/verify-network-policies.sh` — PASS.
  - `bash infrastructure/tests/verify-ingress-tls.sh` — PASS with warning: Kiali ingress TLS secret was not found or mismatched.
- **Eval Commands**:
  - Targeted `.agents/**` and `.agents/hooks.json` trigger scan — PASS.
  - Targeted Phase 3 index/link scan — PASS.
  - Targeted Phase 3 frontmatter and related-documents scan — PASS.
  - Protected-surface no-op diff review for model policy, provider config, and GitOps manifests — PASS; no diff under `docs/00.agent-governance/model-policy.md`, `.codex/agents`, `.claude/agents`, `.agents/agents`, `gitops`, or `infrastructure`.
  - ESO/Vault status probe — `ClusterSecretStore/vault-backend` condition `Ready=False`, reason `InvalidProviderConfig`, message `unable to create client`; `argocd-external-valkey` condition `Ready=False`, reason `SecretSyncedError`, message `could not get secret data from provider`.
- **Logs / Evidence Location**:
  - This task document after final verification.
  - [Progress ledger](../../00.agent-governance/memory/progress.md).

## Related Documents

- [Phase 3 Protected Surface Hardening Plan](../plans/2026-06-02-phase-3-protected-surface-hardening.md)
- [Phase 4 ESO Vault Runtime Diagnosis Plan](../plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- [Phase 4 ESO Vault Runtime Diagnosis Task](./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- [Phase 2 Governance Alignment Plan](../plans/2026-06-02-phase-2-governance-alignment.md)
- [Phase 2 Governance Alignment Task](./2026-06-02-phase-2-governance-alignment.md)
- [Phase 1 Governance Alignment Audit Task](./2026-06-02-phase-1-governance-alignment-audit.md)
- [ADR-0013: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- [Task Template](../../99.templates/task.template.md)
