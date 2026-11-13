# AGENTS.md

Agent instructions for `examples/azure/` and its `infrastructure/`, `gitops/`
and `kubernetes/` subfolders, which have no `AGENTS.md` of their own. The READMEs are
for human readers; these rules are for AI agents. Read
[`../AGENTS.md`](../AGENTS.md) first; the repository root gateway and
`.agents/governance/` still apply.

## Scope

### Allowed Surface

These are executable Azure reference implementations: Bicep for AKS, AGC and
data services (`infrastructure/`), managed platform GitOps resources
(`gitops/`), and workload manifests (`kubernetes/`). They are not the active
local desired state; no local Argo CD tree reconciles them, and they prove no
current Azure support, subscription readiness or cost.

| Work in `examples/azure/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change Bicep or manifests | [k8s-implementer](../../.agents/roles/k8s-implementer.md) | `deployment-strategies`, `gitops-workflow`, `k8s-validate`, `external-service-contract-audit` | `.claude/agents/k8s-implementer.md` | `.codex/agents/k8s-implementer.toml` |
| Review GitOps structure | [gitops-reviewer](../../.agents/roles/gitops-reviewer.md) | `gitops-workflow`, `k8s-validate` | `.claude/agents/gitops-reviewer.md` | `.codex/agents/gitops-reviewer.toml` |
| Review identity and secret handling | [security-auditor](../../.agents/roles/security-auditor.md) | `k8s-security-audit`, `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |

Native loading and permission limits are in
[`.claude/provider.md`](../../.claude/provider.md) and
[`.codex/provider.md`](../../.codex/provider.md). Approval boundaries are in
[approval and safety](../../.agents/governance/approval-and-safety.md).

### Non-goals

Non-goals are stated in the opening text of Allowed Surface: these files are not the active local desired state.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Never commit Azure credentials, subscription state, deployment outputs,
   kubeconfigs, tokens, keys, certificates or secret values.
2. Do not run `az`, `kubectl` or deployment commands against a live
   subscription or cluster; these files are reference assets.
3. Keep version constraints in each file and inject parameters through the
   reviewed interface. Recheck the official Azure support range before an
   approved use.
4. The platform contract is owned by REQ-0004 and AD-0007; do not treat an
   example as current authority.
5. After a change, run `bash scripts/validate-k8s-manifests.sh .` and
   `bash scripts/validate-policy-gates.sh .` for manifests, and record what
   was not validated (Bicep build, live AKS) as a limitation.

#### `infrastructure/`

Bicep definitions for AKS, Application Gateway for Containers, networking,
Azure Database for PostgreSQL and Azure Cache for Redis.

1. When a resource definition changes, confirm it still matches the related
   ADR and Spec.
2. Prefer the modular deployment structure and keep dependencies between
   modules explicit.
3. Inject deployment parameters through variables or parameters; do not
   hardcode them.
4. Do not run `az deployment` or other provider commands; Bicep build and
   what-if results are external evidence.

#### `gitops/`

Managed platform resources for AKS: Azure Managed Identity and federated
credentials, Gateway API definitions for Application Gateway for Containers,
and platform controller and Helm settings.

1. When editing a manifest, confirm the Azure resources it references (IDs,
   resource IDs) are still valid.
2. Never commit a secret value in a manifest; use the Secret Store CSI driver
   configuration.
3. Follow the resource naming and labeling rules exactly.
4. Keep application resources out of this folder; they belong in
   `kubernetes/`.

#### `kubernetes/`

Application manifests for the AKS target: Workload Identity service
accounts, Secret Store CSI volumes, external service references and sample
workloads.

1. When generating a manifest, check that the
   `azure.workload.identity/use: "true"` label is present.
2. Mount every secret as a file through a `secrets-store.csi.k8s.io` volume.
3. Follow the resource tag and labeling rules.
4. Promote a manifest into the active `gitops/` tree only through an owned
   change with its own Spec.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This folder hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here.

## Verification

### Required Checks

Required checks are stated in rule 5 under Local Obligations.

### Evidence and Limits

Evidence limits are stated in rule 5 under Local Obligations.

## Safety

### Protected Actions

Protected actions are stated in rules 1 and 2 under Local Obligations.

### Stop and Escalate

This folder adds no stop condition beyond the work lifecycle's stop rule and the approval and safety policy; if work here needs its own, state it here.
