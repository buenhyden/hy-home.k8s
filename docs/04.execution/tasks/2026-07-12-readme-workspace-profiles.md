---
title: 'Task: README and Workspace Profiles'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-12
---

# Task: README and Workspace Profiles

## Overview

This Task tracks six bounded implementation units for replacing the monolithic
README form with path-derived profiles, migrating the complete README corpus,
and preserving `_workspace` as temporary non-secret repository-support staging.
RWP-001 through RWP-006 are complete: all 67 baseline README files and five
cloud handoffs resolve to one of six profiles, and the retired common form and
its compatibility exceptions have been removed.

## Inputs

- **Parent Spec**: [README and Workspace Profiles Technical Specification](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Parent Plan**: [README and Workspace Profiles Implementation Plan](../plans/2026-07-12-readme-workspace-profiles.md)
- **Completed Registry Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Completed Template Spec**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Semantic Validator Consumer**: [Semantic Document Validation](../../03.specs/029-semantic-document-validation/spec.md)
- **Authored Corpus and Handoff Migration Owner**: [Authored Document Migration](../../03.specs/030-authored-document-migration/spec.md)

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| RWP-001 | Start reciprocal execution lineage | platform | Done | Six links and index rows |
| RWP-002 | Create six forms, routes, and complete fixture | platform | Done | 67 baseline and 72 final dispositions; 8 executable cases |
| RWP-003 | Migrate repository, stage, and collection entrypoints | platform | Done | 27 baseline plus cloud collection handoff |
| RWP-004 | Migrate snapshot packs and create provider snapshot handoffs | platform | Done | 28 baseline plus two provider indexes |
| RWP-005 | Migrate implementation/workspace entrypoints and create example handoffs | platform | Done | 12 baseline plus two provider entrypoints |
| RWP-006 | Delete monolith, verify handoff fixtures, and close | platform | Done | 72 exact routes; 60 profiles, 27 templates, 466 targets; zero universal markers |

## Approval and Safety Boundaries

- **Allowed Paths**: Each RWP unit used the exact path set declared in its Plan
  task. RWP-006 changed exactly the 25 active consumer and lifecycle paths
  listed in Plan Task 6: 24 modified paths and one deleted form. Historical
  non-README evidence remained outside the closure scope.
- **Forbidden Paths**: Ignored `_workspace` children, secrets, credentials,
  local diagnostics, live/provider/cluster state, remote resources, and every
  path outside the applicable RWP task scope remained untouched.
- **Approval Required**: Human approval is required before adding a seventh
  profile, accessing secrets or local state, publishing, pushing, or performing
  any remote or live mutation. The operator approved this tranche's protected
  Stage 00, Stage 99, provider, hook, script, and validator changes.
- **Static Validation**: Registry self-test and compatibility modes, the
  focused fence-aware 72-path assertion, semantic digest and fixture SHA pins,
  repository quality gate, active residue searches, `git diff --check`, exact
  cached scope proof, and all-files pre-commit checks form the closure bundle.
- **Live Validation**: DEFER. This tranche is repository-static and does not
  establish Kubernetes, Argo CD, Vault, ESO, or provider-runtime readiness.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  credentials, secret values, Vault data, tokens, keys, certificates,
  kubeconfigs, local settings, diagnostics, or ignored workspace content.
- **Rollback Plan**: Revert newest-first: the closure commit containing this
  Task, then `60fd310`, `3dfa3c1`, `f20f563`, `147b27b`, `771eecb`,
  `495c792`, `01fdfd6`, `a6c3b91`, `6fe2a83`, `4e85c55`, `30468a9`,
  `983bba9`, and `44b8e37`. Do not partially restore the retired common form
  without its registry, fixture, and validator state.
- **Evidence Location**: This Task, the commits above, and ignored
  `.superpowers/sdd/rwp-task-{1..6}-report.md` implementation reports. The
  exact closure SHA and independent RWP-006 review belong in the Task 6 report
  because a commit cannot contain its own SHA.
- **GitOps Impact**: None; no manifests or desired-state configuration change.
- **Kubernetes Impact**: None; no live cluster command is authorized or run.
- **Operations / Runbook Impact**: None; no operational procedure changes.

`_workspace` validation is limited to tracked-file and ignore-rule metadata.
It must never enumerate or open ignored children. Spec 029 must run the same
eight cases in `readme-profile-cases.json` through its production CommonMark-
aware parser and then remove the temporary finite fixture reader from the
repository quality gate. Spec 030 owns broader authored-corpus migration and
cloud-document handoff consolidation.

## Verification Summary

- RWP-001 through RWP-005 were independently reviewed clean after their recorded
  compatibility, proof-hardening, fixture, hidden-anchor, and implementation-
  table fixes. The logical chain is `44b8e37` through `3dfa3c1`; `60fd310`
  corrected the atomic RWP-006 closure proof before implementation.
- Registry validation passes with 60 profiles, 27 template forms, 466 classified
  targets (`baseline=433`, `new=35`), and no uncovered or ambiguous paths.
  README validation passes for all 67 baseline and 72 final paths, with all 72
  in canonical profile mode.
- The byte-identical fixture SHA is
  `50f8c8ab05267a9ddf059d72ca6950d4f05b14ad82010c0d9576eb7a9f1f68d0`;
  its five added handoffs are `docs/90.references/cloud-examples/README.md`,
  `docs/90.references/cloud-examples/aws/README.md`,
  `docs/90.references/cloud-examples/azure/README.md`,
  `examples/aws/README.md`, and `examples/azure/README.md`.
- The document-profile projection SHA is
  `54ab9344bc7c718da6bb8ad95cdd5a9e3ab66728052263afbe9f2c107a04a7a8`;
  the template-compatibility fixture SHA is
  `d53a36f8849fdb8131f79c23ad2bd66c267a1594f12c0b03f353dfe5c88b46a2`.
- Active residue searches, focused parser and handoff proofs, registry modes,
  repository quality, diff checks, link/index/hook/mutation probes, exact
  25-path cached scope, and every applicable all-files pre-commit hook pass.
  Dockerfile lint is a non-applicable SKIP because no Dockerfile was selected,
  not a pass.
- Evidence is repository-static only. No live, secret-value, credential,
  remote CI, publication, push, merge, deployment, or third-party mutation was
  performed or inferred.

## Traceability

- **Spec**: [README and Workspace Profiles](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Plan**: [README and Workspace Profiles Implementation Plan](../plans/2026-07-12-readme-workspace-profiles.md)
- **Previous Registry Tranche**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Previous Template Tranche**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Semantic Validation Consumer**: [Semantic Document Validation](../../03.specs/029-semantic-document-validation/spec.md)
- **Authored Migration Owner**: [Authored Document Migration](../../03.specs/030-authored-document-migration/spec.md)
