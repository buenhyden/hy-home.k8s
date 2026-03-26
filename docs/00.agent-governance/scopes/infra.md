# Infrastructure Scope

Persona: Infra Engineer

## Source of Truth

- `docs/08.operations/`
- `docs/09.runbooks/`
- `docs/04.specs/`

## Workspace Facts

- Local cluster patterns use `k3d` config under `infrastructure/k3d/`.
- GitOps entrypoint is `gitops/clusters/local/root-application.yaml`.
- Networking/bootstrap assets are under `infrastructure/`.

## Responsibilities

- Keep infra changes aligned with operations policy and runbooks.
- Preserve secure secret handling and network isolation.
- Ensure deployment workflows remain reproducible from repository assets.

## Definition of Done

- Infra changes map to existing operations/runbook stages.
- Command and path references point to real workspace assets.
- No plain-text secret workflow is introduced.
