---
title: "Agent Responsibilities"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# Agent Responsibilities

## Overview

Select the responsibility needed for the task, then resolve the concrete role
and provider projection from the [agent registry](../roles/registry.json).
This router is not a duplicate roster or permission inventory.

## Scope

Responsibility explains the domain boundary; registry permission and explicit
task ownership determine permitted actions. A review lens is not write access.

## Item Index

- [Architecture](architecture.md): structure, system boundaries, and decisions.
- [Documentation](documentation.md): authored content and navigation quality.
- [Infrastructure](infrastructure.md): Kubernetes/GitOps desired-state work.
- [Supervision](supervision.md): bounded delegation, dependencies, and escalation.
- [Operations](operations.md): operating knowledge, recovery, and incidents.
- [Quality](quality.md): reproducible validation and result evidence.
- [Security](security.md): exposure, privilege, isolation, and unsafe execution.

Canonical role bodies:

- [supervisor](supervisor.md)
- [code-reviewer](code-reviewer.md)
- [doc-writer](doc-writer.md)
- [gitops-reviewer](gitops-reviewer.md)
- [incident-responder](incident-responder.md)
- [k8s-implementer](k8s-implementer.md)
- [network-reviewer](network-reviewer.md)
- [observability-reviewer](observability-reviewer.md)
- [security-auditor](security-auditor.md)
- [wiki-curator](wiki-curator.md)
- [docs-researcher](docs-researcher.md)
- [quality-engineer](quality-engineer.md)

## Add and Find

Load only the relevant responsibility owners. Product intent belongs in the
Requirement Package; backend/API and UI behavior belong in the Spec and its
implementation task. UI work additionally follows root `DESIGN.md` and checks
accessibility/responsiveness. These general duties do not need unused
standalone agent scopes in this infrastructure workspace.

Add a role or skill only for an approved concrete gap, through the neutral
registry and reviewed projections. Declare ownership transitions when a task
crosses domains; escalate unclear or conflicting boundaries.

## Related Documents

- [Governance Hub](../README.md)
- [SDLC Flow](../sdlc.md)
- [Delegated Development](../skills/delegated-development.md)
