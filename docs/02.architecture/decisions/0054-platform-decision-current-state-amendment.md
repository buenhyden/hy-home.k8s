---
title: "Platform Decision Current-State Amendment"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "ADR-0054"
---

# ADR-0054: Platform Decision Current-State Amendment

## Overview

The operator approved on 2026-11-05 a scoped amendment that brings the
accepted clauses of six platform and delivery ADRs in line with the
implemented repository. It replaces only the clauses named below.
[ADR-0011](./0011-argo-rollouts-progressive-delivery.md),
[ADR-0012](./0012-argo-notifications-slack.md),
[ADR-0014](./0014-current-local-gitops-platform-contract.md),
[ADR-0026](./0026-argo-cd-source-integrity-non-adoption.md),
[ADR-0041](./0041-openbao-secret-backend.md) and
[ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md) stay accepted for
every other clause, and their bodies stay as dated decision history. Apart from
the Rollouts delivery clause, which SPEC-0141 implements, this decision
changes no manifest, and it claims no observed cluster state.

## Context

The 2026-11-05 Stage 02 review recorded, in each ADR's Traceability, accepted
Decision or Non-goal clauses that no longer describe the repository. Rule 3 of
the Stage 02 instructions forbids rewriting them in place. Earlier scoped
amendments ([ADR-0047](./0047-agent-contract-and-resource-ownership.md),
[ADR-0049](./0049-external-data-service-contract-alignment.md)) set the
pattern of one accepted record that replaces named clauses. The current
sources are:

- [`gitops/workloads/adminer/rollout.yaml`](../../../gitops/workloads/adminer/rollout.yaml):
  the reference Rollout advances by an AnalysisTemplate step and timed pauses,
  with no manual pause gate.
- [`gitops/platform/argocd/argocd-notifications-cm.yaml`](../../../gitops/platform/argocd/argocd-notifications-cm.yaml):
  `service.slack` uses an app token, and the default `subscriptions` send
  `on-health-degraded`, `on-sync-failed` and `on-deployed` to
  `slack:hy-home-alerts`.
- [`gitops/apps/root/platform-rollouts-app.yaml`](../../../gitops/apps/root/platform-rollouts-app.yaml):
  the Rollouts chart keeps `notifications.enabled: false`.
- [`gitops/platform/eso/vault-secret-store.yaml`](../../../gitops/platform/eso/vault-secret-store.yaml):
  the `vault-backend` store reaches OpenBao over HTTPS with the `openbao-ca` CA
  and requests the `vault` and API-server audiences, without a reviewer JWT.
- [`gitops/apps/root/platform-traefik-app.yaml`](../../../gitops/apps/root/platform-traefik-app.yaml):
  besides `kubernetesIngressNGINX`, a static `file` provider holds one `hsts`
  middleware attached to the `websecure` entry point, which keeps the HSTS
  header that ingress-nginx sent on every TLS response.

## Decision

The operator, as request owner, approved these replacements on 2026-11-05.
Compliance is confirmed by the strict document checks and by comparing each
clause with the source named in Context.

1. **ADR-0011 Non-goal.** "Forcing automatic promotion (manual promotion is
   the default)" is replaced by: the platform imposes no promotion mode; each
   application chooses manual promotion or timed steps gated by an approved
   safety check in its own Rollout, and a failing check aborts the rollout.
2. **ADR-0012 Decision and Non-goal.** The Slack integration authenticates
   with a Slack app token, not a webhook; the credential lives in the OpenBao
   backend through the `vault-backend` ClusterSecretStore
   ([ADR-0041](./0041-openbao-secret-backend.md)). The default subscription
   sends health degradation, sync failure and deployment completion to the
   shared channel; a per-app subscription may add another channel. Rollouts
   completion and abort events are delivered by the Argo Rollouts
   controller's own notification engine, not by ArgoCD Notifications, which
   evaluates Applications only. That engine uses the same app token from the
   OpenBao `platform/notifications` entry through its own ExternalSecret in
   `argo-rollouts`, the built-in `on-rollout-completed` and
   `on-rollout-aborted` triggers, and a default subscription to the shared
   channel. The unused `rollout-*` templates and triggers leave
   `argocd-notifications-cm`. SPEC-0141 implements this clause.
3. **ADR-0014 Decision.** The 2026-11-03 wording of the Decision (Traefik in
   active scope, replaced decisions recovered only from Git history, no
   deleted or archived document as design input) is accepted as the current
   text. "ESO/Vault integration" and the Non-goal's "Vault runtime state"
   read "ESO/OpenBao integration" and "OpenBao runtime state", and "the
   active PRD/ARD/Spec chain" reads "the active Requirement, Architecture
   Description and Spec chain".
4. **ADR-0026 preferred control.** The clause recording commit-SHA pinning as
   the preferred future control is replaced by
   [ADR-0029](./0029-mutable-target-revision-retention.md), which retains the
   mutable `main` revision. ADR-0026's non-adoption of source integrity
   stands; the identity gap stays recorded and open.
5. **ADR-0041 Decision and Non-goal.** ESO authenticates to OpenBao over HTTPS
   (`https://openbao.hy.home.arpa`, `openbao-ca`), so the HTTP local-only
   transport and the Non-goal deferring TLS no longer apply. The ServiceAccount
   token requests the `vault` and API-server audiences, not `vault` alone.
6. **ADR-0050 provider clause.** "Enable only the `kubernetesIngressNGINX`
   provider" is replaced by: `kubernetesIngressNGINX` is the only provider
   that discovers routes; a static `file` provider may hold middleware
   definitions only, currently the one `hsts` middleware applied to
   `websecure`. The plain `kubernetesIngress` and `kubernetesCRD` providers
   stay disabled.

## Explicit Non-goals

- Changing any manifest, chart value or validator other than the Rollouts
  notification delivery that SPEC-0141 implements.
- Custom Rollouts notification templates or per-Rollout routing.
- Adopting commit-SHA pinning or Argo CD source integrity.
- Replacing any of the amended ADRs as a whole.

## Consequences

- **Positive**: every accepted platform decision now reads true against the
  repository, and the dated clarifications in the amended ADRs point to one
  approving record.
- **Negative**: a reader must combine each amended ADR with this record.
- **Operational**: live Slack receipt, OpenBao authentication and Traefik
  responses remain operator observations; this record proves none of them.
  The OpenBao entry must hold `slack_token` before the Rollouts ExternalSecret
  can become ready.

## Alternatives

- **Successor ADRs that supersede each document**: rejected; it would delete
  six records whose other clauses stay current and churn every inbound link.
- **Reverting the manifests to the old clauses**: rejected; the current
  behaviour (check-gated promotion, app token, HTTPS to OpenBao, HSTS parity)
  is the reviewed and wanted state.
- **Editing the accepted clauses in place**: rejected by Stage 02 rule 3.

## Traceability

The amendment applies only to the clauses named in the Decision. The amended
ADRs keep their original bodies, and their 2026-11-05 clarifications refer to
this record.

- **Requirement**: [REQ-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)
  IF-0002; [REQ-0002](../../01.requirements/0002-argo-notifications-slack.md)
  FR-0002, FR-0003, NFR-0001 and IF-0001;
  [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)
  FR-0003, FR-0010, FR-0013 and NFR-0002.
- **Architecture**: [AD-0004](../descriptions/0004-argo-rollouts-progressive-delivery.md),
  [AD-0005](../descriptions/0005-argo-notifications-slack.md),
  [AD-0007](../descriptions/0007-current-local-gitops-platform.md).
- **Specification**: SPEC-0141 implements the Rollouts delivery clause; the other clauses need no Spec because their implementation already exists.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0011](./0011-argo-rollouts-progressive-delivery.md) | Replaces only the promotion-default Non-goal | N/A — no Spec package; documentation amendment |
| [ADR-0012](./0012-argo-notifications-slack.md) | Replaces the webhook, Vault and default-subscription clauses and assigns Rollouts delivery to the Rollouts notification engine | N/A — SPEC-0141 implements the Rollouts delivery clause in a later change |
| [ADR-0014](./0014-current-local-gitops-platform-contract.md) | Accepts the 2026-11-03 Decision wording and replaces the Vault and PRD/ARD names in its Decision and Non-goals | N/A — no Spec package; documentation amendment |
| [ADR-0026](./0026-argo-cd-source-integrity-non-adoption.md) | Replaces only the preferred-control clause, by ADR-0029 | N/A — no Spec package; documentation amendment |
| [ADR-0041](./0041-openbao-secret-backend.md) | Replaces the HTTP transport, TLS Non-goal and audience clauses | N/A — no Spec package; documentation amendment |
| [ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md) | Replaces only the single-provider clause | N/A — no Spec package; documentation amendment |
