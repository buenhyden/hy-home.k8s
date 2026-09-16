---
title: "Reference: Git Provenance and Superseded Record Citation"
version: "0.1.1"
type: "reference/research"
status: "draft"
owner: "platform"
updated: "2026-09-15"
layer: "references"
artifact_id: "RES-0002-m0001"
---

# Reference: Git Provenance and Superseded Record Citation

## Overview

This dated reference records what primary sources say about naming and keeping
Git objects, keeping superseded decisions and incident records, signalling moved
or removed public URLs, removing sensitive data, validating conditional schema
fields, and parsing Markdown links. It bounds the Stage 98 choices in ADR-0039.

## Reference Type

Research reference with source-backed claims and stated limits.

## Authority Boundary

A claim here states what an external source documents. Whether this repository
retains, cites, or validates something is decided by
[common governance](../../../../.agents/README.md), the Stage 99 registry, and
[ADR-0039](../../../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md)
once accepted.

## Scope

Included: Git revision syntax, object inspection, garbage collection, clone
depth and filters; the original ADR article; SRE postmortem practice; HTTP
redirect and gone semantics; GitHub sensitive-data removal; JSON Schema
conditionals, annotations, and `format`; CommonMark links and code; Diátaxis.
Excluded: hosting-provider garbage collection policy, digital preservation
certification, and any runtime behavior.

## Definitions / Facts

### Git object naming and availability

- `<rev>:<path>` "names the blob or tree at the given path in the tree-ish
  object named by the part before the colon" (gitrevisions, Specifying
  Revisions). One envelope form can therefore name a document's blob or a
  package's tree. The syntax does not assert the type; the object at the path
  decides it.
- `git cat-file -t` shows "the object type identified by `<object>`", and `-e`
  exits zero "if `<object>` exists and is a valid object" (git-cat-file). Existence
  is local and says nothing about reachability or persistence.
- `git gc` "tries very hard not to delete objects that are referenced anywhere in
  your repository", while unreachable objects are pruned after a grace period
  that defaults to two weeks (git-gc, Notes and `gc.pruneExpire`). An object
  name alone is not a durable reference; reachability from a kept ref is.
- `--depth` creates "a shallow clone with a history truncated", and `--filter`
  requests "a subset of reachable objects" (git-clone). A shallow or partial
  clone may lack the object an envelope names.

### Superseded decisions and incident records

- The original ADR article states: "If a decision is reversed, we will keep the
  old one around, but mark it as superseded", with a reference to its
  replacement (Nygard, 2011). The source keeps superseded decisions and does not
  restrict citing them; this repository's restriction on current citations is a
  local policy choice.
- A postmortem is "a written record of an incident, its impact, the actions
  taken to mitigate or resolve it, the root cause(s), and the follow-up actions"
  (SRE Book, Postmortem Culture). Well-written postmortems have action items
  with "both an owner and a tracking number" (SRE Workbook, Postmortem Culture).
  Neither chapter sets a retention period or a citation policy.

### Public URLs and sensitive data

- HTTP 301 and 308 mean the resource "has been assigned a new permanent URI",
  and 410 means it is "no longer available at any location" and likely
  permanently (RFC 9110, 15.4.2, 15.4.9, 15.5.11). These are server response
  semantics for a live site, not version-control provenance.
- For a leaked secret, GitHub's first step is to "revoke and/or rotate that
  secret"; rewriting history "will change the hashes" of affected commits
  (GitHub Docs, Removing sensitive data). This is hosting-product guidance, and
  it is why a history rewrite cannot be a routine retention step.

### Schema conditionals and annotations

- `if`/`then`/`else` applies `then` only when `if` is valid, and
  `dependentRequired` requires properties when a given property is present
  (Understanding JSON Schema, Conditionals).
- Annotation keywords such as `default`, `deprecated`, and `readOnly` "aren't
  strictly used for validation", and "by default, `format` is just an annotation"
  (Understanding JSON Schema, Annotations and Type). A declared format is not
  proof that a validator enforces it. These guide pages are explanatory, not the
  normative specification.

### Markdown links and code

- A link reference definition "does not correspond to a structural element of a
  document", and code fence content "is treated as literal text, not parsed as
  inlines" (CommonMark 0.31.2, 4.7 and 4.5). Link-like text in code is not a
  link, so a comparison that rewrites it changes bytes a renderer never treats
  as links.

### Documentation purpose

- Diátaxis "identifies four distinct needs, and four corresponding forms of
  documentation" (diataxis.fr). A retained body keeps the purpose it had; the
  archive index is navigation, not a fifth form.

## Sources

| Source                                  | URL                                                                                                                      | Checked    | Result                                                                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| gitrevisions                            | https://git-scm.com/docs/gitrevisions                                                                                    | 2026-09-15 | Fetched                                                                                                                 |
| git-cat-file                            | https://git-scm.com/docs/git-cat-file                                                                                    | 2026-09-15 | Fetched                                                                                                                 |
| git-gc                                  | https://git-scm.com/docs/git-gc                                                                                          | 2026-09-15 | Fetched                                                                                                                 |
| git-clone                               | https://git-scm.com/docs/git-clone                                                                                       | 2026-09-15 | Fetched                                                                                                                 |
| Documenting Architecture Decisions      | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions                                                 | 2026-09-15 | Fetched                                                                                                                 |
| SRE Book, Postmortem Culture            | https://sre.google/sre-book/postmortem-culture/                                                                          | 2026-09-15 | Fetched after one HTTP 403 retry                                                                                        |
| SRE Workbook, Postmortem Culture        | https://sre.google/workbook/postmortem-culture/                                                                          | 2026-09-15 | Fetched                                                                                                                 |
| RFC 9110                                | https://www.rfc-editor.org/rfc/rfc9110.html                                                                              | 2026-09-15 | Fetched                                                                                                                 |
| GitHub, Removing sensitive data         | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | 2026-09-15 | Fetched                                                                                                                 |
| Understanding JSON Schema, Conditionals | https://json-schema.org/understanding-json-schema/reference/conditionals                                                 | 2026-09-15 | Fetched                                                                                                                 |
| Understanding JSON Schema, Annotations  | https://json-schema.org/understanding-json-schema/reference/annotations                                                  | 2026-09-15 | Fetched                                                                                                                 |
| Understanding JSON Schema, Type         | https://json-schema.org/understanding-json-schema/reference/type                                                         | 2026-09-15 | Fetched                                                                                                                 |
| CommonMark Spec 0.31.2                  | https://spec.commonmark.org/0.31.2/                                                                                      | 2026-09-15 | Fetched                                                                                                                 |
| Diátaxis                                | https://diataxis.fr/                                                                                                     | 2026-09-15 | Fetched                                                                                                                 |
| PREMIS Ontology                         | https://www.loc.gov/standards/premis/ontology/index.html                                                                 | 2026-09-15 | `unreachable`: HTTP 403 twice, and `https://www.loc.gov/standards/premis/v3/` also returned HTTP 403; no claim recorded |

## Review and Freshness

Refresh when a cited Git, HTTP, JSON Schema, or CommonMark section changes, when
PREMIS becomes reachable and an object, event, agent, or rights distinction is
needed, or when ADR-0039 or its successor revises retention or citation. Current
truth stays with the governance and registry owners named above.

## Related Documents

- [Research pack](README.md)
- [Spec 0082](../../../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md)
