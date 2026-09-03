---
title: "Reference Form Family Naming"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-03"
artifact_id: "MIG-0012"
---

# MIG-0012: Reference Form Family Naming

## Overview

This reviewed ledger records the three Stage 90 reference forms that take the
name of the family they serve. Each form already lives in `references/` and
already declares its family in `type`, so the `-reference` suffix repeated the
directory and the frontmatter without distinguishing anything: the sibling that
`audit-reference.template.md` had to be told apart from is
`audit-pack.template.md`, and `pack` is what separates them.

Every row is `moved`. The bytes are unchanged, so each form keeps its profile,
its required sections and its `artifact_id` grammar; only the path is new. The
registry route for each `template/reference/*` profile names the new path in
the same change, and every citation was repointed with it.

MIG-0010 replaced the generic `reference.template.md` with
`research-reference.template.md`. That sealed row keeps its own bytes and
resolves through this ledger, which names the endpoint it now has.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/99.templates/templates/references/audit-reference.template.md",
    "stable_path": "docs/99.templates/templates/references/audit.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e3c3f5b3bb7903c09bad4931a4e587b7a21dc15",
    "source_blob": "5b4d1fc6807d55501de1f24fd57717c2ad50f0a1",
    "content_sha256": "e17fdf2e14bc3adcfa295f23a4d92901ec51b376a138e22834a6a1d054b7744b",
    "reason": "The form serves the audit family and sits in references/, so the -reference suffix repeated its directory; audit-pack.template.md is the sibling it is told apart from."
  },
  {
    "legacy_path": "docs/99.templates/templates/references/data-reference.template.md",
    "stable_path": "docs/99.templates/templates/references/data.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e3c3f5b3bb7903c09bad4931a4e587b7a21dc15",
    "source_blob": "5add25a90aea8c67a4a270cf64087d621afadde9",
    "content_sha256": "4f049b196f8fd486ff33cba10cf82336f9648b2059fe366b996659b1bd4f5cf4",
    "reason": "The form serves the data family and sits in references/, so the -reference suffix repeated its directory; data-pack.template.md is the sibling it is told apart from."
  },
  {
    "legacy_path": "docs/99.templates/templates/references/research-reference.template.md",
    "stable_path": "docs/99.templates/templates/references/research.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e3c3f5b3bb7903c09bad4931a4e587b7a21dc15",
    "source_blob": "c97f237283724733f6e10f547095336f1936ee98",
    "content_sha256": "0a86680a2e08f7d29e96dcfd1082c389fec12d322d75a8885889835c00708184",
    "reason": "The form serves the research family and sits in references/, so the -reference suffix repeated its directory; research-pack.template.md is the sibling it is told apart from."
  }
]
```

## Recovery

For every row, recover the legacy bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Each `moved` row is byte-identical to its `stable_path`, so
the form at the new path is the recovered form.

### Historical consumers

Every citation of a renamed form was repointed at its new path in the same
change, so no consumer needs a pinned historical declaration here and this
block admits no path.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
