---
title: "MIG-0006: Unroutable Reference Profile Retirement"
type: "content/archive-migration"
status: "sealed"
owner: "platform"
updated: "2026-08-30"
artifact_id: "MIG-0006"
---

# MIG-0006: Unroutable Reference Profile Retirement

## Overview

This reviewed ledger records the retirement of three Stage 99 templates whose
profiles never routed a document. `content/audit`, `content/research` and
`content/data` each required a dated directory of the form `YYYY-<letter>`,
while every real directory under `docs/90.references/` is `YYYY-MM-DD-<slug>`,
so none of the three ever classified a file. The 43 documents that do live in
those directories — 26 audits, 13 research notes, 4 data references — all
classify as `content/reference`, whose eight required sections are identical to
the three retired profiles'.

`reference.template.md` already names the distinction as a section rather than a
profile: its `Reference Type` prompt reads "classify this as research, snapshot,
glossary, or evidence reference". The retired templates duplicated its purpose.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/99.templates/templates/references/audit.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/99.templates/templates/references/reference.template.md",
    "source_commit": "d885cba511a7628d2aabbd0d3e8774367ee52260",
    "source_blob": "6ec03d05b53b21d81fdd07ee97d6c63cd37b2452",
    "content_sha256": "0875192a5f4d2d5bfd493a44cf1d1cf359b144b00fa71168ec10604374d2a081",
    "reason": "The content/audit profile never routed a document because its dated-directory pattern cannot match a YYYY-MM-DD directory; audit documents already author from the reference template, whose Reference Type section carries the distinction."
  },
  {
    "legacy_path": "docs/99.templates/templates/references/research.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/99.templates/templates/references/reference.template.md",
    "source_commit": "d885cba511a7628d2aabbd0d3e8774367ee52260",
    "source_blob": "2b57624f02696eac2b900d3b264d1c8931df9d3f",
    "content_sha256": "5ff2735c7656e8f37bacafae06b68e0bfe0d17802b56526ea8ba4f7a81e12751",
    "reason": "The content/research profile never routed a document and its only instance was this template; its eight required sections are identical to content/reference's, which the research corpus already uses."
  },
  {
    "legacy_path": "docs/99.templates/templates/references/data.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/99.templates/templates/references/reference.template.md",
    "source_commit": "d885cba511a7628d2aabbd0d3e8774367ee52260",
    "source_blob": "60a8ca60a9d9b0fee87a17269d810b805b41efdc",
    "content_sha256": "0bf8b253ee923fb121ba9f882514471100bc06530aad378fa070fa8df8460d9d",
    "reason": "The content/data profile never routed a document and docs/90.references/data/ holds no dated directory at all; its data references author from the reference template."
  }
]
```

## Recovery

For every row, recover the legacy bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Merged rows resolve through `replacement`; their legacy bytes
remain recoverable from Git history.

### Historical consumers

No current document cites the three retired templates. Their only references
were the six registry entries retired with them, so this block admits no path.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
