---
title: "Affected Pull Request GitOps Validation"
version: "1.1.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-20"
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

This decision amends the hosted-validation clause of ADR-0048. It covers
selection, execution and reporting of static GitOps identity validation on
main-targeting PRs. The existing local render, schema and operational checks
keep their respective input and authority boundaries.

## Options

### Considered Options

Keep local GitOps validation alone, add one hosted job per leaf, or share the
existing PR candidate job and environment.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Local only | Avoids hosted work. | Leaves hosted GitOps assurance absent. | Not selected: the Problem states a PR can change desired Kubernetes state while passing the hosted metadata and style checks. |
| Separate leaf jobs | Isolates failure displays. | Duplicates checkout or setup for selected leaves. | not stated in this document |
| Shared PR job | Shares setup and preserves the required job name. The aggregate distinguishes what each leaf observed. | The workflow definition itself remains editable by a PR. | Chosen: the Decision reports style, CI lock and GitOps identity checks under the existing `style-pr` status. |

## Decision

### Chosen Option

Use the existing `style-pr` status to report selected style, CI lock and
GitOps identity checks. Bind the reviewed base, head and merge identities and
compare both parents. Select checks from the cumulative base-to-merge diff.
The GitOps leaf calls the reviewed base's existing validator against candidate
data. The final step requires success for each selected leaf and a skipped
outcome for each unselected leaf.

### Authority and Effect

P01 clarification, 2026-11-20: the current scoped user request extends the
existing selected PR job to affected purpose checks under D01. It retains
this decision's exact merge binding, stable required name and fail-closed
aggregation. The earlier base-tool-only execution method is replaced for
purpose checks by candidate validators and their regressions under the
read-only, no-secret job; style configuration and the Python dependency lock
remain reviewed-base inputs. This is the new requested implementation scope,
not retrospective acceptance or a new claim about the runs below. Current
selection and evidence rules are owned by QUAL-R006 in the
[quality policy](../../04.quality/quality.md#requirements); the SPEC-0223 Task
records P01 implementation, review, hosted results and pending acceptance.


The operator accepted this decision on 2026-11-18, on the basis of the
implemented workflow and the observed aggregate runs. The workflow is
implemented in `.github/workflows/ci.yml` on `main` (EVD-166) with read-only
repository permission and without persistent checkout credentials. The hosted
aggregate was observed on PR runs with the CI lock and GitOps leaves skipped
for absent affected paths; EVD-166 records the run on `c2243ef9`. A hosted run
in which the CI lock or GitOps leaf is selected and executes remains
unobserved, and the first PR that changes `gitops/` or the CI lock owns that
observation. The workflow definition itself remains editable by a PR.

#### Sources

[ADR-0048](./0048-local-qa-and-semver-release-ownership.md),
[REQ-0003 FR-0017](../../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements)
and [AD-0006](../01.descriptions/0006-workspace-agent-governance-platform.md).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0048 hosted validation clause](./0048-local-qa-and-semver-release-ownership.md#one-local-validation-graph) | Amends only the hosted validation clause; every other clause stays | [SPEC-0161](../../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage) |

## Consequences

### Impacts

Implemented in `.github/workflows/ci.yml` (EVD-166) and accepted by the
operator on 2026-11-18. The changed GitOps scope gets an additional static
identity result on the exact PR merge input. A metadata edit still verifies
applicable candidate checks when same-input hosted evidence cannot be
authenticated.

### Follow-up

The topology update reached `main` through PR #290 before any change to the
CI dependency lock. The owning Spec package's Task records the hosted
aggregate, and required-check read-back in EVD-166.
The GitOps leaf was inapplicable on that candidate. A hosted run in which the
CI lock or GitOps leaf is selected and executes remains unobserved; the first
PR that changes `gitops/` or the CI lock owns that observation.
