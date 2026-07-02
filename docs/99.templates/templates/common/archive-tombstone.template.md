---
title: 'Archive Tombstone: {Original Document Title}'
type: content/archive-tombstone
status: archived
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/98.archive/<original-docs-subpath>.md -->

# Archive Tombstone: [Original Document Title]

> Use this template for `docs/98.archive/<original-docs-subpath>.md`.
>
> Rules:
>
> - Do not preserve the old document body in the tombstone.
> - Keep only routing, reason, replacement, and evidence metadata.
> - Link active documents to the archive index only.
> - Use relative links only, calculated from the final tombstone location.

---

## Overview

이 문서는 현재 구현과 맞지 않는 old 문서를 `98.archive`로 이동했음을 기록하는 Tombstone이다.

## Original Document

- Original path: `docs/<original-path>.md`
- Original title: [Title]
- Original type: [prd | ard | adr | spec | plan | task]

## Archive Decision

- Archived on: YYYY-MM-DD
- Reason: [Why the active document was removed from current stages.]
- Currentness rule: The old body is intentionally not retained because active stages must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [Replacement document]
- Current active index: [Stage README]

## Current Implementation Evidence

- [Evidence path or command]

## Archive Index

- Archive index: `docs/98.archive/README.md`

## Related Documents

- [Current replacement]
