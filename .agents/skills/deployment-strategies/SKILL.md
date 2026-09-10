---
name: "deployment-strategies"
description: "Use when comparing or designing Kubernetes and ArgoCD deployment strategies, including Blue-Green, Canary, Rolling update, rollback, zero-downtime deployment, progressive delivery, probes, and DORA metrics. Monitoring tool setup and actual CI pipeline configuration are outside this skill's scope."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# Deployment Strategies — Choosing and Verifying a Rollout

Select a rollout strategy for a Kubernetes workload reconciled by Argo CD, then
design the verification and reversal that make the choice safe to review.

## Workflow Steps

1. State what the change is risking: whether it can be served side by side with
   the current version, whether it is reversible by reverting desired state
   alone, and what a failure would cost. The answer decides the strategy, not
   the strategy's popularity.
2. Read `references/strategies.md` and choose one. The comparison table
   separates them by exactly the properties step 1 established.
3. Read `references/verification.md` and design the verification half: which
   probes prove readiness, which conditions abort the rollout, and what reverses
   it. A strategy without a stated abort condition is a strategy that cannot
   fail visibly.
4. Express both halves as desired state in the repository. This procedure
   produces a reviewable change, never a cluster action.
5. Observe the branch and approval boundary below before proposing the change.

## Reference Material

`references/strategies.md` holds the catalog and `references/verification.md`
holds probe, abort, and measurement detail. Both are read when a decision needs
them rather than carried through every use of this skill, because a rollout
question is usually about one strategy and not about all five.

## Branch and Promotion Model

This workspace has one integration branch and no environment promotion chain,
so the generic multi-branch models a deployment guide usually lists do not
describe it. `main` is the integration base, a change reaches it through a
prefixed branch and review, and Argo CD reconciles the merged desired state
under operator control. [Git policy](../../governance/git.md) owns the branch,
merge and finish rules, `.github/workflows/ci.yml` owns the executable branch
shape, and [approval and safety](../../governance/approval-and-safety.md) owns
which actions need explicit authorization.

No promotion path shortens an approval. A passing check is evidence, never
permission, and an emergency still needs the same authorization boundary.
