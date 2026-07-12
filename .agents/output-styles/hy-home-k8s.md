---
name: hy-home-k8s GitOps
description: Evidence-first, GitOps-first output style for the hy-home.k8s WSL2+k3d ArgoCD repository.
---

# hy-home.k8s GitOps Output Style

You are operating in the `hy-home.k8s` repository: a WSL2+k3d home-lab platform
managed through ArgoCD GitOps. Apply this output contract on top of the governance
loaded from `docs/00.agent-governance/**`.

## Response Contract

- Respond to the human in Korean. Keep governance and control documents under
  `docs/00.agent-governance/**` in English (per `rules/documentation-protocol.md`).
- Lead with repo-backed evidence: cite concrete files, current diffs, validators, and
  scoped source paths before proposing changes. Do not assert behavior you have not checked.
- Stay GitOps-first: never mutate the live cluster directly. Treat `kubectl apply/patch`,
  `argocd app sync`, and secret writes as human-approved bootstrap or break-glass paths only.
- Never write plaintext Kubernetes secrets.

## Execution Discipline

- Follow the JIT loading sequence: bootstrap -> preflight -> persona -> scope -> provider
  -> progress -> postflight.
- Author stage documents Template-First using `docs/99.templates/support/template-routing.md`
  and the matching template; use `docs/99.templates/README.md` as the inventory summary
  and route generated docs into the canonical `docs/01`–`docs/05`, `docs/90`, `docs/99`
  tree only.
- Define validation evidence before editing. Report skipped or unavailable local tools
  honestly (for example, when `rtk` is not on PATH).
- Prefer existing skills, agents, and validators over new code; make surgical, in-place changes.

## Completion Reporting

- State validation results plainly: if a gate failed, show the output; if a check was
  skipped, say so. Do not claim done-and-verified without evidence.
- Record repo-changing work in `docs/00.agent-governance/memory/progress.md` and keep the
  related README current and conformant with its registry-selected required/allowed H2 contract.
