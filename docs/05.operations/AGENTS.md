# AGENTS.md

Agent instructions for `docs/05.operations/` and its `guides/`, `policies/`,
`runbooks/` and `incidents/` collections. The parent
[`docs/AGENTS.md`](../AGENTS.md) still applies.

## Scope

### Allowed Surface

Stage 05 holds the operating documents of the platform: stable guides, shared
policies, executable runbooks, and incident records with their postmortems.
They describe how operators act; they are not permission for an agent to act.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Incident record, RCA and postmortem | [incident-responder](../../.agents/roles/incident-responder.md) | `incident-postmortem`, `rca-methodology` | `.claude/agents/incident-responder.md` | `.codex/agents/incident-responder.toml` |
| Guide, policy or runbook text | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| GitOps and reconciliation procedures | [gitops-reviewer](../../.agents/roles/gitops-reviewer.md) | `gitops-workflow`, `k8s-validate`, `external-service-contract-audit` | `.claude/agents/gitops-reviewer.md` | `.codex/agents/gitops-reviewer.toml` |
| Secret, Vault and access procedures | [security-auditor](../../.agents/roles/security-auditor.md) | `k8s-security-audit`, `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |
| Alerting and observability procedures | [observability-reviewer](../../.agents/roles/observability-reviewer.md) | `risk-report` | `.claude/agents/observability-reviewer.md` | `.codex/agents/observability-reviewer.toml` |

### Non-goals

Non-goals are stated at the end of the Purpose text under Allowed Surface: operating documents are not permission for an agent to act.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Profiles: `operation/guide`, `operation/policy`, `operation/runbook`,
   `operation/incident` and `operation/postmortem`, started from
   `docs/99.templates/templates/operations/`.
2. By default limit agent work here to Git file edits, review, ArgoCD
   reconciliation planning and evidence organization. A command or a command
   boundary marker in an operations document never grants execution
   authority; live cluster, Vault and DNS actions need the operator's
   explicit approval under
   [approval and safety](../../.agents/governance/approval-and-safety.md).
3. Mark every mutating command with its boundary (operator-approved,
   break-glass, bootstrap-only) so the repository quality gate can tell an
   example from an instruction.
4. Incidents use `inc-<NNNN>-<NNNN>` and move `detected` → `investigating` →
   `mitigated` → `resolved`; postmortems use `inc-<NNNN>-<NNNN>-PM` and move
   `draft` → `in-review` → `published`. Do not declare completion without
   action-closure evidence.
5. Record secrets only by path, key, property and mount, with redacted
   evidence. Never paste a value, token or private key.
6. Write `AI Agent Requirements` and `Agent Execution Notes` sections in
   English.
7. Update the collection README in the same change that adds, retitles or
   removes a document.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

Run the strict document checks listed in the parent `AGENTS.md` and
`python3 scripts/validation/repository/quality.py --root .`, which checks
command boundary markers.

### Evidence and Limits

Evidence rules are stated in rules 4 and 5 under Local Obligations.

## Safety

### Protected Actions

Protected actions are stated in rules 2, 3 and 5 under Local Obligations.

### Stop and Escalate

Stop and escalation conditions are stated in rules 2 and 4 under Local Obligations.
