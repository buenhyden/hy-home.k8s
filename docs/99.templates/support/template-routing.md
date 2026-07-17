---
title: 'Template Routing Contract'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-15
---

# Template Routing Contract

## Overview

This document explains how an authored target selects one canonical form.
Template forms live under `docs/99.templates/templates/**`; support contracts
live under `docs/99.templates/support/**`.

## Purpose

Every governed path must match exactly one registry profile. Zero matches leave
the document outside its contract; multiple matches make ownership ambiguous.
Declaration order is never precedence.

## Owned Contract

The closed v7 [Document Profile Registry](./document-profiles.json) is the sole owner
of exact and anchored-regex routes, profile identities, headings, metadata,
canonical forms, exceptions, and body contracts. This support document owns
only the selection procedure, rationale, examples, and change boundary. It does
not publish a route or template inventory.

An authored, native, or append-entry profile is the canonical form owner. A
derived template-mode profile classifies the physical form and inherits its
source contract; it is not a second form owner.

### Exact-One-Profile Procedure

1. Normalize the repository-relative POSIX target path. Do not traverse ignored
   scratch paths or resolve provider views into a different tracked path.
2. Load the registry and evaluate every declared exact or anchored-regex route.
3. Stop when the result is zero or more than one profile; do not infer a form
   from a neighboring file or declaration order.
4. Use the selected profile's canonical form, frontmatter, headings, lifecycle,
   and body contract. Use support prose only to understand why and how.
5. Recalculate relative links from the final authored location and validate the
   authored document, not just the copied form.

### Selection Examples

- A feature requirement is classified from its final Stage 01 path; its matched
  profile supplies the PRD form and requirement traceability contract.
- A README is classified independently from adjacent authored documents; its
  matched README profile keeps it frontmatter-free and defines its H2 contract.
- A native API contract selects its native profile and form. It does not inherit
  Markdown frontmatter or comments from a helper Spec.
- A provider snapshot selects a Stage 90 reference profile. Historical
  provider-local documentation routes are not inferred from executable example
  directories.

The registry is the query surface for the exact answer. README family summaries
and these examples are explanatory views and must never be used as an
exhaustive fallback.

## Authoring Rules

### Route Change Boundary

- Add, change, or retire the registry route and its canonical form in one
  logical change.
- Prove that every physical form has exactly one owning profile and that every
  registry-owned form exists.
- Update only support rationale, Stage 00 procedure, or README navigation that
  is materially affected; do not copy the new route set into those documents.
- Migrate current consumers whose selected contract changes. Preserve completed
  evidence and accepted decisions according to SDLC governance.
- Keep GitHub-native controls, ignored workspace scratch, generated artifacts,
  and native contracts within their registry-declared exception boundaries.
- A cloud snapshot refresh requires approved lifecycle evidence and updates the
  Stage 90 Current reference pack rather than creating a parallel active owner.

## Validation Contract

Run the registry, Markdown, link/owner, and aggregate repository gates after a
route change:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

Passing evidence must show zero uncovered or ambiguous governed paths, an
existing canonical form for every form-owning profile, and exactly one profile
owner for every physical form. Repository-static validation does not prove
provider runtime discovery, remote CI, or live cluster state.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Profile Registry Schema](./document-profiles.schema.json)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
