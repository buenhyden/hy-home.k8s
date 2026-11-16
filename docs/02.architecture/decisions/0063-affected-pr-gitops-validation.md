---
title: "Affected Pull Request GitOps Validation"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-16"
artifact_id: "ADR-0063"
---

# ADR-0063: Affected Pull Request GitOps Validation

## Context

### Problem and Drivers

The PR metadata and style checks report evidence for different inputs. A PR
can change the repository's desired Kubernetes state while passing both checks.
The local GitOps identity validator already reads the declared resource graph
and rejects malformed, unsupported, missing or duplicate objects.

### Decision Scope

This proposal amends the hosted-validation clause of ADR-0048. It covers
selection, execution and reporting of static GitOps identity validation on
main-targeting PRs. The existing local render, schema and operational checks
keep their respective input and authority boundaries.

## Decision

### Chosen Option

Use the existing `style-pr` status to report selected style, CI lock and
GitOps identity checks. Bind the reviewed base, head and merge identities and
compare both parents. Select checks from the cumulative base-to-merge diff.
The GitOps leaf calls the reviewed base's existing validator against candidate
data. The final step requires success for each selected leaf and a skipped
outcome for each unselected leaf.

### Authority and Effect

The W06 implementation request authorizes developing and testing the candidate.
The operator's ADR acceptance, the associated policy update and an observed
hosted run establish adoption evidence. The workflow runs with read-only
repository permission and without persistent checkout credentials. The
workflow definition itself remains editable by a PR.

## Alternatives

### Considered Options

Keep local GitOps validation alone, add one hosted job per leaf, or share the
existing PR candidate job and environment.

### Trade-offs

| Alternative | Trade-off |
| --- | --- |
| Local only | Avoids hosted work and leaves hosted GitOps assurance absent. |
| Separate leaf jobs | Isolates failure displays and duplicates checkout or setup for selected leaves. |
| Shared PR job | Shares setup and preserves the required job name. The aggregate distinguishes what each leaf observed. |

## Consequences

### Impacts

The changed GitOps scope gets an additional static identity result on the
exact PR merge input. A metadata edit still verifies applicable candidate
checks when same-input hosted evidence cannot be authenticated.

### Follow-up

Record queue, checkout, setup and leaf timing on the first authorized PR run.
Verify the actual required-check settings separately. During adoption, deliver
the topology update before a change to the CI dependency lock so the reviewed
base's exact topology checker can recognize the successor workflow.

## Traceability

### Sources

[ADR-0048](./0048-local-qa-and-semver-release-ownership.md),
[REQ-0003 FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements)
and [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0048 hosted validation clause](./0048-local-qa-and-semver-release-ownership.md#one-local-validation-graph) | Proposed clause amendment | [SPEC-0161](../../03.specs/0161-w00-v14-7-delta-intake/spec.md) |
