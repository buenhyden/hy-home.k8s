---
title: "Stage 99 Form Naming and Profile Identity Convergence"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-02"
artifact_id: "MIG-0010"
---

# MIG-0010: Stage 99 Form Naming and Profile Identity Convergence

## Overview

This reviewed ledger records the twelve Stage 99 forms that changed path when
the document contract moved to `family/kind` profile identities. Every form
kept its authoring responsibility; only its name, its directory, or its
frontmatter identity changed.

Nine rows are `replaced` because the form's bytes changed with its name: the
frontmatter now carries the renamed profile identity, the stage-free `layer`
slug, and the three-component `version` grammar. Three rows are `moved`: the
OpenAPI, GraphQL, and protobuf forms were relocated under
`templates/specs/contracts/` so the form tree mirrors the authored destination
`docs/03.specs/####-<slug>/contracts/`, and their bytes are unchanged.

The Codex row is the one substantive form change. Its predecessor was Markdown
while the Codex runtime reads TOML, so no author could copy it into
`.codex/agents/` without rewriting it by hand. The replacement is the TOML form
the runtime accepts.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/99.templates/templates/architecture/ad.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/architecture/description.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "cbbf497299350669664ef05ebd29131d569cfd9b",
    "content_sha256": "8369c8e12338c0f80fadf39c4ae2042ceae568c4e178dacea6baec04e7d4bf55",
    "reason": "The architecture form is named for the document it produces rather than for its acronym, and its frontmatter moved to the sdlc/architecture-description profile identity."
  },
  {
    "legacy_path": "docs/99.templates/templates/architecture/adr.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/architecture/decision.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "6458077bb45f9e239f2cc37222bd6853ead4e10d",
    "content_sha256": "239088282022ff04c4f991b2c0c26589059189f56a2bf49c163c349a568a8073",
    "reason": "The decision form is named for the document it produces rather than for its acronym, and its frontmatter moved to the sdlc/architecture-decision profile identity."
  },
  {
    "legacy_path": "docs/99.templates/templates/archive/archive-migration.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/archive/migration.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "71b92a5e2fce2723752cc372e42d81dfcfc4f4ed",
    "content_sha256": "9b4736789882a6285a974974523fd0fbc2cc96e4957ebd04f3041ee9634248e6",
    "reason": "The form no longer repeats its own directory in its file name, and its frontmatter moved to the archive/migration profile identity with the shared version and layer keys."
  },
  {
    "legacy_path": "docs/99.templates/templates/archive/archive-record.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/archive/tombstone.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "e4c080ec323f87d9745ac988d52561efe4ab1547",
    "content_sha256": "6ee6974911b215217b4a59e377e144f6eff1aa28efbfd647dd2897cc087b6b24",
    "reason": "The form is named for the record it produces, and its frontmatter moved to the archive/tombstone profile identity with the shared version, layer, and artifact_id keys."
  },
  {
    "legacy_path": "docs/99.templates/templates/governance/governance-reference.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/governance/rule.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "7c91cb9532756e82022c55189cc2c29d8e5f6468",
    "content_sha256": "48290d70e65fbc7b0744dbb53d45ecb454c840af20137b920b1463f30d45915d",
    "reason": "One governance form covered six different Stage 00 owners; it becomes the rule form and five sibling forms carry the contract, control, provider, role, and skill kinds."
  },
  {
    "legacy_path": "docs/99.templates/templates/references/reference.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/references/research-reference.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "c4904f88d6a1a68ad77f770bfb54de7340f803e8",
    "content_sha256": "e075186067b08c106848f1f88e5b0be807951d976c821ff93ed60aba1b2e6565",
    "reason": "The generic reference form served only the research family while audit and data already had their own; it is named for the family it serves."
  },
  {
    "legacy_path": "docs/99.templates/templates/runtime/claude-agent-projection.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/runtime/claude-agent.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "a04b1e579c1c530a4ade7d5bd27205ccc6ce75f6",
    "content_sha256": "33da3a3a48e6f1bb3bcc2b5cfd85f0f4991a10171e4dbf97291e8501b6fb651e",
    "reason": "The Claude binding form drops the projection suffix and states its provider-owned keys as placeholders."
  },
  {
    "legacy_path": "docs/99.templates/templates/runtime/codex-agent-projection.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/runtime/codex-agent.template.toml",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "f54b713103cc9df905c311c4d3ba551d2b31bfb3",
    "content_sha256": "beff106ef2396d3cb9f0ce84aa62054a01c382804433da08df7d059a3b9274b2",
    "reason": "The Codex runtime reads TOML, so the Markdown form could never be copied into .codex/agents/; the replacement is the TOML form the runtime actually accepts."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/data-model.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/specs/contracts/data-model.template.md",
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "b85586e2d4030f278b0d7c3c74e11f4eb05b114d",
    "content_sha256": "a01cccd7cf36bfa009db4464094abeb4fe00e740da52c76a2ca573207cf6c236",
    "reason": "Spec-owned contract forms are grouped under one contracts directory, and the frontmatter gained the shared semantic version grammar and stage-free layer."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/openapi.template.yaml",
    "stable_path": "docs/99.templates/templates/specs/contracts/openapi.template.yaml",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "7492ec59f553b1ecc7fedb945aace243d28a9149",
    "content_sha256": "aba7ee08fd3c45e63edbc0557911c86ea8b31a47f9afbc3016d2439c65ed1176",
    "reason": "Spec-owned contract forms are grouped under one contracts directory that mirrors the authored destination; the bytes are unchanged."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/schema.template.graphql",
    "stable_path": "docs/99.templates/templates/specs/contracts/schema.template.graphql",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "f39499ce00d55b88e520400194a5eaad4c263386",
    "content_sha256": "cd6d8b531799d3fd617fe404b441f80c5ab7dc2893bd8519c5ad053c3037dd4a",
    "reason": "Spec-owned contract forms are grouped under one contracts directory that mirrors the authored destination; the bytes are unchanged."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/service.template.proto",
    "stable_path": "docs/99.templates/templates/specs/contracts/service.template.proto",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "3fc50ef1e565e71427e446eae3f6b5e4f76b3497",
    "source_blob": "2d9288896bb3c83e7a2ef08f049662cd6e290df1",
    "content_sha256": "b601274f4a078e14350e0d3694ad846544b266293d04764f68ac8decc7bca4b8",
    "reason": "Spec-owned contract forms are grouped under one contracts directory that mirrors the authored destination; the bytes are unchanged."
  }
]
```

## Recovery

For every row, recover the legacy bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. `moved` rows resolve through `stable_path` and `replaced`
rows through `replacement`; in both cases the legacy bytes remain recoverable
from Git history at the pinned commit.

### Historical consumers

Every routed citation of a retired form path was repointed at its successor in
the same change, so no consumer needs a pinned historical declaration and this
block admits no path. Unrouted prose inside closed records still names the path
that existed when the record was written; those mentions are history, not
references, and are left as written.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
