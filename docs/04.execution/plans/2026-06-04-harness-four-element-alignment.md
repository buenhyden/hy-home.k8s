---
title: 'Harness Four-Element Alignment Plan'
type: plan
status: done
owner: platform
updated: 2026-06-04
---

# Harness Four-Element Alignment Plan

## Overview (KR)

이 문서는 `hy-home.k8s` AI Agent 하네스를 네 요소인 지시 문서, 아키텍처
제약, 피드백 루프, 지식 저장소 관점으로 재감사하고 Codex/Claude provider
surface에 같은 관계 모델을 고정하는 실행 계획이다.

## Context

The current Stage 00 governance already has thin provider gateways, shared hook
scripts, Codex/Claude runtime baselines, provider-specific agent surfaces, repo
validators, and a project memory ledger. The remaining gap is not a missing
directory; it is that the four harness elements are distributed across several
files and are not described as one causal control model:

```text
instructions -> constraints -> feedback -> knowledge -> next instructions
```

This plan keeps the existing canonical adapter model and improves traceability
without creating a parallel governance hierarchy.

## Goals & In-Scope

- **Goals**:
  - Record the current workspace audit against the four harness elements.
  - Make `docs/00.agent-governance/harness-catalog.md` the canonical
    four-element control model.
  - Make `.claude/CLAUDE.md` and `.codex/CODEX.md` state how each provider
    implements the four elements.
  - Make the docs folder responsibility, language boundary, and template
    routing contract explicit in common governance.
  - Make drift garbage collection explicit for code drift, document drift, and
    structure drift, including the feedback loop from repeated errors to
    harness changes.
  - Update the repo-local `workspace-harness-audit` skill so future audits must
    preserve the relationship model, not only file inventories.
  - Extend repository validation so the four-element contract, language
    boundary, and drift cleanup contract cannot be removed silently.
- **In Scope**:
  - `docs/00.agent-governance/harness-catalog.md`
  - `docs/00.agent-governance/rules/documentation-protocol.md`
  - `docs/00.agent-governance/rules/stage-authoring-matrix.md`
  - `docs/00.agent-governance/rules/agentic.md`
  - `docs/00.agent-governance/README.md`
  - `.claude/CLAUDE.md`
  - `.codex/CODEX.md`
  - `.agents/skills/workspace-harness-audit/skill.md`
  - `docs/README.md`
  - Existing `AI Agent Requirements` sections in authored PRDs
  - `scripts/validate-repo-quality-gates.sh`
  - Plan/Task indexes and progress memory

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Add new runtime agents or replace the Stage 00 canonical adapter model.
  - Treat Codex hook wiring as a Claude-style permission gate.
  - Change model policy, CI topology, Kubernetes manifests, Vault, ESO, ArgoCD,
    or live cluster state.
- **Out of Scope**:
  - Direct `kubectl`, `argocd`, or `vault` mutation.
  - Secret value inspection or credential modification.
  - Installing external skills or plugins.

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- |
| PLN-001 | Audit current four-element surfaces | `docs/00.agent-governance/**`, `.claude/**`, `.codex/**`, `.agents/**`, `scripts/**` | REQ-H4-001 | Evidence recorded in paired task |
| PLN-002 | Add common four-element control model | `docs/00.agent-governance/harness-catalog.md` | REQ-H4-002 | Catalog includes instruction, constraint, feedback, and knowledge rows for common, Claude, and Codex surfaces |
| PLN-003 | Add provider runtime contracts | `.claude/CLAUDE.md`, `.codex/CODEX.md` | REQ-H4-003 | Both baselines explain provider-specific enforcement and feedback paths |
| PLN-004 | Update audit workflow skill | `.agents/skills/workspace-harness-audit/skill.md` | REQ-H4-004 | Skill requires relationship mapping and named-skill boundary evidence |
| PLN-005 | Add regression checks | `scripts/validate-repo-quality-gates.sh` | REQ-H4-005 | Repo quality gate checks the new contract phrases |
| PLN-006 | Add docs language/template and drift GC contracts | `documentation-protocol.md`, `stage-authoring-matrix.md`, `agentic.md`, `docs/README.md` | REQ-H4-006 | Governance states folder responsibilities, template routing owners, AI-agent English sections, and drift cleanup loop |
| PLN-007 | Record execution evidence | paired task, README indexes, `memory/progress.md` | REQ-H4-007 | Task and progress ledger include validation results and RTK limitation |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-H4-001 | Structural | Plan/Task and README indexes are complete | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-H4-002 | Runtime JSON | Runtime hook JSON remains parseable | `python3 -m json.tool .claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json` | PASS |
| VAL-H4-003 | Shell | Hook and validation scripts remain syntactically valid | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-H4-004 | Wiki | Generated LLM Wiki index stays current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-H4-005 | Hygiene | Whitespace and patch sanity | `git diff --check` | PASS |
| VAL-H4-006 | Language contract | AI-agent-specific requirement sections are English | `bash scripts/validate-repo-quality-gates.sh .` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Duplicating policy across provider files | Medium | Keep durable policy in Stage 00 and provider baselines as pointers plus provider-specific execution contracts only |
| Overstating Codex hooks as enforcement | High | State Codex hook wiring is context/validation and relies on Codex sandbox/approval plus autonomous governance compliance |
| Treating repo-static checks as live readiness | High | Keep readiness evidence lanes separate and retain opt-in live probe wording |
| Reintroducing Korean prose into AI-agent requirement sections | Medium | Keep the language contract in governance and enforce `AI Agent Requirements` sections through the repo quality gate |
| Drift cleanup becoming blame-oriented instead of harness-oriented | Medium | Route recurring errors to rules, skills, hooks, validators, templates, indexes, archive Tombstones, or memory entries |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Run repo quality, JSON parsing, shell syntax,
  generated-index freshness, and diff hygiene checks.
- **Sandbox / Canary Rollout**: Not applicable; this is repository governance
  and validation wiring.
- **Human Approval Gate**: Live runtime validation, CI topology, provider model
  policy, GitOps manifests, secret material, and external systems are out of
  scope.
- **Rollback Trigger**: Revert this Plan/Task/catalog/baseline/skill/validator
  change set if repository quality validation fails and cannot be fixed in
  scope.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Four-element audit and implementation plan recorded.
- [x] Common harness catalog states the four-element control model.
- [x] Codex and Claude runtime baselines state provider-specific four-element
      contracts.
- [x] Common governance states documentation folder responsibilities, template
      routing ownership, language boundary, and drift garbage collection.
- [x] Workspace harness audit skill routes future audits through the same model.
- [x] Repository quality gate protects the new contract.
- [x] Progress memory records evidence and limitations.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Tasks**: [../tasks/2026-06-04-harness-four-element-alignment.md](../tasks/2026-06-04-harness-four-element-alignment.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Claude Runtime Baseline**: [../../../.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
