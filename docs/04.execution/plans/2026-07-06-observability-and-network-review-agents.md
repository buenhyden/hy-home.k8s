---
title: 'Observability and Network Review Agents Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-14
---

# Observability and Network Review Agents Implementation Plan

## Overview

This plan sequences adding two worker-tier review agents,
`observability-reviewer` and `network-reviewer`, to the `hy-home.k8s` runtime
roster across Claude-native, Codex-native, and local/Antigravity tracked
adapter surfaces and the harness catalog.

**2026-07-14 terminology correction:** The six completed adapter-file changes,
historical commands, and validation results below remain point-in-time evidence.
Current terminology distinguishes `.claude/agents/*.md` and
`.codex/agents/*.toml` native role files from repository-local
`.agents/agents/*.md`; Gemini CLI native `.gemini/**` was not implemented.

## Context

The workspace already carries observability and network manifests with no
dedicated review owner, as recorded in the AI agents roster and gap-analysis
reference and confirmed against `gitops/`, `traefik/`, and `infrastructure/`.

## Goals & In-Scope

- Two new worker roles, each projected across Claude-native `.claude/agents`,
  Codex-native `.codex/agents`, and local/Antigravity `.agents/agents`.
- Harness catalog roster and adapter-table additions.
- Stage 03/04 governance chain and progress ledger evidence.

## Non-Goals & Out-of-Scope

- Live cluster scraping, querying, or probing.
- Manifest authoring or model-policy tier changes.
- Changes to existing agents beyond adding handoff targets where relevant.

## Work Breakdown

1. Author the Stage 03 spec and agent-design documents.
2. Create this plan and the Stage 04 task record.
3. Create six tracked role-adapter files (three surfaces per role).
4. Add harness catalog roster rows and adapter-table rows.
5. Update spec/plan/task index READMEs and the progress ledger.
6. Run repo-static validation and record evidence.

## Verification Plan

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

## Risks & Mitigations

- **Role overlap** with `security-auditor`/`gitops-reviewer`: mitigated by
  explicit non-goals and handoff rules in the spec and adapters.
- **Adapter drift** across tracked adapter surfaces: mitigated by mirroring the
  existing
  `gitops-reviewer` body and validating parity.

### Agent Rollout & Evaluation Gates

- Gate 1: Claude/Codex/local tracked-adapter parity for each role.
- Gate 2: catalog roster and adapter-table rows present.
- Gate 3: `bash scripts/validate-repo-quality-gates.sh .` PASS.

## Completion Criteria

- All work-breakdown items done, validation green, and evidence recorded in
  the Stage 04 task and progress ledger.

## Traceability

- **Spec**: [../../03.specs/024-observability-and-network-review-agents/spec.md](../../03.specs/024-observability-and-network-review-agents/spec.md)
- **Agent Design**: [../../03.specs/024-observability-and-network-review-agents/agent-design.md](../../03.specs/024-observability-and-network-review-agents/agent-design.md)
- **Task**: [../tasks/2026-07-06-observability-and-network-review-agents.md](../tasks/2026-07-06-observability-and-network-review-agents.md)
- **Harness catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
