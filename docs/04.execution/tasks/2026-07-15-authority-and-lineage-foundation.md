---
title: 'Task: Authority and Lineage Foundation'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-15
---

# Task: Authority and Lineage Foundation

## Overview

This Task is the durable execution and review record for Spec 034. It tracks
registry v6 lineage, cross-document admission, Stage 00 authority cleanup,
Current audit dispositions, and tranche closure without claiming remote or live
evidence.

## Inputs

- **Plan**: [Authority and Lineage Foundation Implementation Plan](../plans/2026-07-15-authority-and-lineage-foundation.md)
- **Spec**: [Spec 034](../../03.specs/034-authority-and-lineage-foundation/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Decision**: [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- **Current audit**: [2026-07-11 WEIA remediation roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ALF-001 | VAL-ALF-001 through VAL-ALF-004 | Introduce typed registry v6 program relations. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | Initial RED: the v6 `valid-minimal` fixture failed with `REGISTRY_SCHEMA` against the v5 loader. Review RED: duplicate `status` was accepted with no diagnostic. GREEN: registry self-test passes 78 cases, including 19 lineage mutations and the isolated legacy migration proof; strict mode loads two programs with 430 classified paths, baseline 433, new 58, uncovered 0, and ambiguous 0. |
| ALF-002 | VAL-ALF-002, VAL-ALF-004, VAL-ALF-006, VAL-ALF-007 | Enforce cross-document lineage and predecessor-gated execution; retire duplicate Stage 00 lifecycle tables. | platform | Done | Implemented; independent requirements and quality review approved the current contract and root fallback review closed the final URI-classification crash. | Initial RED: six cases reported the missing production rule set. Review RED: seven mutations reproduced rendered-evidence, pair-admission, and table-wrapper bypasses. Rounds two through four closed rendered, graph, table, and scanner gaps. Round five closed six cross-container label/destination joins; round six closed five full-reference identifier joins. Round seven closed twelve outer-opacity, destination-remainder, and code-span recovery gaps. Round eight closed five angle-destination and quoted-title delimiter gaps. Round nine closed eleven block, escape, token-state, and reference-definition gaps plus the failed-candidate quadratic scan. Round ten closed four image-subtree, unresolved-adjacency, and code-wrapped authority gaps. Round eleven closed four display-label and resolved-image token-state gaps. Round twelve closed five follow-up execution, definition-validity, and consumed-source-span gaps. Round thirteen closed three definition-source-span and nested-parenthesized-title gaps. Round fourteen closed four whitespace-only destination-remainder continuation gaps. Round fifteen closed paragraph-interruption and failed-inline shortcut-fallback gaps. Round sixteen closed ordered/unordered list-container opacity gaps. Round seventeen closed empty-marker trailing-whitespace padding gaps. Round eighteen closed tab-stop indentation and lazy container-paragraph gaps. Round nineteen closed whitespace-only reference-label resolution gaps. Round twenty closed Setext/thematic leaf-block indented-code opacity gaps. Round twenty-one closed standalone Setext-delimiter false positives while preserving thematic-break disambiguation. Round twenty-two closed definition/container ownership before indented/Setext block-state ordering. Round twenty-three closed quoted-definition paragraph-state false positives. Round twenty-four closed lazy-completed multiline-definition state gaps. Round twenty-five closed explicit quote-marker Setext provenance gaps. Round twenty-six closed leaf-boundary reference-definition admission gaps. Round twenty-seven closed CommonMark reference-label length gaps. Round twenty-eight closed escape-aware reference-definition labels, zero-through-four-column/tab destination and title continuations, blank-free multiline-title source spans, and complete-definition/indented-code disambiguation. Round twenty-nine separated same-line invalid-title rejection from next-line invalid-title fallback after a complete destination. Round thirty made synthetic Setext/thematic join boundaries definition-aware while preserving real post-definition delimiters. Round thirty-one preserved open-paragraph Setext ownership and added escape-aware CommonMark character-reference decoding before percent/path or rendered-cell normalization. Round thirty-two preserved lazy quote/list provenance through joined definition re-parsing and masked valid inline HTML tag tokens without hiding visible Markdown between them. Round thirty-three made inline HTML opaque without changing Markdown grammar or reference-label identity, made comments and type-7 blocks escape/quote/grammar aware, and restored visible wrapper text in lifecycle cells. Round thirty-four replaced the repeated sentinel with collision-free reversible raw-token identities across shortcut, collapsed, and full labels while preserving raw length. Round thirty-five separated comment block/inline state, bounded inline HTML to one paragraph, added multiline definition labels, and accepted one-plus-hyphen GFM delimiters. Round thirty-six separated code-raw grammar from rendered-code suppression, closed container paragraphs on HTML block types 2–5, handled the overlapping comment closer, and rejected lazy pseudo-tables. Round thirty-seven excluded code-span brackets before link pairing and namespaced arbitrary raw BMP private-use input away from opaque HTML identities. Round thirty-eight established code/destination versus HTML precedence and restored CommonMark label case folding from structured token-source provenance. Round thirty-nine corrected backslash handling to CommonMark run-length semantics and assigned valid destination/title and quote-aware HTML ownership before code pairing. Round forty limited inline suffix ownership to complete candidates with paired raw non-code bracket openers. Round forty-one added context-sensitive backslash parity and provisional raw/raw-code-aware suffix ownership. Round forty-two limited dependency-ready execution to the first unfinished original tranche and prohibited every follow-up component. Round forty-three corrected CommonMark code-span precedence and replaced quadratic link/HTML containment with sorted interval sweeps. Round forty-four replaced quadratic code-span/HTML overlap checks with a source-order-preserving two-pointer sweep. Round forty-five established monotonic source-order suffix ownership and linear bracket-tree suppression. Round forty-six closed escaped-adjacent-run opener parity, nested bare-destination whitespace, paragraph-reset ownership rescans, and quadratic execution-component closure with monotonic ownership work and cached adjacency components. Round forty-seven separated CommonMark ASCII-control, Unicode-space, separator, and line-ending predicates and replaced all-token-per-label opaque provenance scans with a one-time token-start index. Round forty-eight stopped local-path classification from trimming parser-preserved Unicode spaces or controls into canonical lineage owners. Round forty-nine made URI-scheme detection non-throwing for malformed external destinations and restored explicit Windows drive-path rejection. GREEN: 336 isolated cases cover all five stable diagnostics, CommonMark/GFM inline-block and container boundaries, raw 999-code-point reference-label admission and 1000-character fail-closed rejection, ordered/unordered list indentation including tab stops and empty-marker normalization, list/blockquote lazy continuation with real block boundaries and explicit/lazy provenance, context-sensitive ATX/Setext/thematic leaf-block code opacity, root/container valid-definition nonparagraph state including leaf-boundary admission and lazy-completed multiline definitions, invalid/incomplete-definition paragraph retention, ownership-before-opacity ordering, standalone delimiter-like paragraph continuation, nested opacity, nonempty normalized reference labels, punctuation-only escapes, resolved link/image/reference token state, block-aware exact valid-definition source masking, escape-aware definition-label closure, zero-through-four-column/tab continuation, validated blank-free multiline definitions and titles, definition-aware container joining with real post-definition boundaries and open-paragraph preservation, escape-aware numeric/named character-reference decoding with entity-before-percent/path/NFKC ordering, joined lazy-line provenance, ownership-first CommonMark inline-HTML and code-span scanning with collision-free same-length token identity, injectively namespaced raw BMP private-use input, and token-source label case folding, grammar/label preservation, escape-aware comments, quote-aware type-7 blocks, rendered-cell wrapper text, comment block/strict-inline state, paragraph-bounded tags, multiline definition labels, one-plus-hyphen GFM delimiters, ownership-first link/definition and HTML grammar with CommonMark backtick-run bracket exclusion and rendered-code suppression, HTML type-2–5 leaf boundaries, overlapping comment closer, lazy-table exclusion, and escaped/invalid-opener controls, same-line invalid-title rejection with next-line invalid-title fallback, failed-inline shortcut fallback, offset-stable lifecycle-cell normalization, closed execution components across tranches and follow-ups, table variants, and stable diagnostic tuples; strict current-corpus validation passes. Stage 00 points to Stage 99 owners instead of copying their lifecycle table. |
| ALF-003 | VAL-ALF-005 | Add the evidence-backed Current audit disposition overlay. | platform | Queued | Not executed | Observation-row preservation, overlay links, validators, and logical commit will be recorded here. |
| ALF-004 | VAL-ALF-001 through VAL-ALF-007 | Run full QA, independent review, and atomic lifecycle closure. | platform | Queued | Not executed | Command matrix, review verdicts, rollback parent, and closure commit will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/00.agent-governance/**`, `docs/03.specs/034-authority-and-lineage-foundation/**`, `docs/03.specs/README.md`, this Plan/Task and Stage 04 indexes, `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`, `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`, `docs/99.templates/support/document-profiles.{json,schema.json}`, `scripts/document_contracts.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-links-and-owners.py`, `scripts/README.md`, and the two named fixture files.
- **Forbidden Paths**: Kubernetes/GitOps desired state, infrastructure, policies, secrets, provider runtime adapters, unrelated audit observations, completed/accepted PRD-005/ARD-0008/ADR-0016/Specs 026-033/Plan/Task bodies, and Specs 035-040 bodies except read-only verification.
- **Approval Required**: Any live system, secret, remote GitHub setting, push, publication, or scope expansion requires separate explicit approval.
- **Static Validation**: Registry, Markdown-profile, cross-document, repository-quality, Markdown lint, staged diff, and all-files pre-commit commands from the Plan.
- **Live Validation**: DEFER. This tranche has no authorized live lane.
- **Secret / Vault Handling**: Do not read, print, move, or infer secret values, tokens, auth files, or Vault data.
- **Rollback Plan**: Revert the newest logical ALF commit first; if the v6 cutover must be removed, revert ALF-002 before ALF-001 so no validator consumes the removed typed interface.
- **Evidence Location**: This Task, the logical Git commits, registry/cross-document fixtures, and the dated Current audit overlay.

## Verification Summary

ALF-001 is implemented and independently approved. Its test-first RED run
failed because schema/loader v5 rejected the new closed-v6 fixture. After the
implementation, `python3 scripts/validate-document-contract-registry.py --root
. --self-test` passes 78 cases and the strict command passes 430 classified
paths while exposing two typed programs. Production loading rejects v5; its
only converter is private to the self-test migration fixture. Quality review
then added fail-closed duplicate-key parsing, explicit ADR timestamp rejection,
and consecutive follow-up approval-order validation. The approved design
baseline remains `daf0636` plus review correction `0f67e9c`. The current
environment has one known all-files limitation: `validate-gitops-change-set.py
--self-test` calls `os.mkfifo`, which returns `Errno 95` in this filesystem and
is independently reproducible on unchanged main. Spec 039 owns its portability
remediation. Requirements re-review returned `REQUIREMENTS COMPLIANT`; quality
re-review returned `QUALITY APPROVED` after the three fail-closed fixes.

ALF-002 passes the typed registry through the raw cross-document interface and
validates relation-state parity, rendered reciprocal evidence, the exact
PRD-005/ARD-0008/Spec-033/ADR-0017 successor record, and predecessor-gated
Plan/Task admission. Plain or inline-code path text is not link evidence;
paragraph breaks, raw HTML blocks, indented code, fenced blocks, and comments
are also excluded while a valid soft-break link remains evidence. From each
relation Spec, rendered local links seed a closed current Plan/Task component.
The first original tranche whose state is neither `done` nor `archived`
requires exactly one reciprocal pair whose two members link directly to that
Spec; connected extra or orphan nodes fail even without their own Spec link.
Every remaining original tranche and every follow-up has no current component,
regardless of mutable follow-up state. A disconnected other-program component
remains outside the relation scope. Root
and blockquote content now share one block-rendering view, so raw HTML, tilde or
backtick fences, indented code, and headings inside raw HTML cannot become link
or section evidence. Each rendered line retains its container segment and
depth; a transition creates a hard inline-token boundary for link labels,
destinations, and full-reference identifiers while soft breaks in one container
remain valid. Outer fences, raw HTML, and indented code propagate their opaque
state before deeper quote parsing. Ordered and unordered list items are
likewise entered outside-in: marker width
and one-to-four-space padding determine the continuation indent, each item has
its own container identity, and stripped content is rendered again so nested
lists, fences, raw HTML, indented code, and tables preserve their semantics.
An empty marker line always uses marker width plus one as its content indent,
regardless of two, three, four, or more trailing spaces; same-line content keeps
the one-to-four versus five-or-more padding distinction.
Tabs advance to four-column stops for marker padding and continuation stripping;
when a tab crosses the required indent, its remaining columns stay in content.
An active list or blockquote paragraph may carry an unmarked lazy continuation
in the same container. Blank lines, fences, raw HTML, indented code, headings,
thematic/setext lines, blockquotes, and list siblings remain real boundaries.
Normal list paragraph links remain rendered evidence. The single-pass inline
scanner resolves
balanced, escaped, and angle-bracket destinations, rejects an unescaped `<`
inside angle brackets, validates the complete optional single-, double-, or
parenthesized-title remainder, and supports full, collapsed, and shortcut
references. Inline parsing consumes the destination, optional title, and actual
outer closer in context, so parentheses inside an angle destination or quoted
title cannot terminate the link early. An unescaped nested `(` invalidates a
parenthesized inline or definition title; an escaped `\(` remains content.
If an inline candidate fails completely, its opener label may still resolve as
a shortcut reference; the failed `(...)` suffix remains literal and is not
recorded as a consumed source span.
Reference-label normalization collapses internal whitespace and case-folds, but
the result must contain at least one non-whitespace character. Whitespace-only
space, tab, or soft-break labels neither register definitions nor resolve as
shortcut, full, collapsed, or failed-inline fallback references.
Backslashes unescape only CommonMark's
ASCII punctuation set; sequences such as `00\09` retain the backslash. List
items, ATX and setext headings, thematic breaks, and GFM table rows/cells start
hard inline boundaries, while a normal same-paragraph soft break remains valid.
ATX headings and thematic breaks close a leaf block. A Setext delimiter closes
one only when it follows an eligible paragraph line in the same container;
standalone `=+` or one/two-hyphen lookalikes instead open or continue a normal
paragraph, while standalone `---` remains a thematic break. An immediately
following four-space/tab-indented block is code only after a real leaf boundary;
the same indentation after an open normal paragraph remains continuation.
A fully valid reference definition is a nonparagraph block: it cannot qualify a
following delimiter as Setext content, and an immediately following indented
line is code. Container ownership is resolved before indented/Setext opacity.
Thus a blank-separated four-space continuation after `- paragraph` is the same
list item's second paragraph, while unmarked `===`, `--`, and indentation after
an active blockquote paragraph retain lazy-continuation provenance. These
fixtures were cross-checked with the installed `markdown-it-py` CommonMark
renderer; genuine root and sufficiently indented list code remain opaque.
Container-local quote/list paragraph state uses the same complete valid-definition
spans: `> [r]: /u` closes quote paragraph state, so a following root-indented
line is root code, while an invalid definition-looking quote line stays ordinary
paragraph content and can retain an unmarked lazy continuation.
After each quote/list lazy append, the accumulated container-local lines are
re-evaluated against complete definition spans. A newly completed multiline
definition closes the paragraph; an invalid or incomplete candidate remains
open. Lazy provenance still prevents unmarked `===` or `--` from being
reclassified as an explicitly owned Setext delimiter.
Only the unmarked branch carries lazy provenance. An explicitly marked
`> ===` or `> --` is evaluated with explicit ownership, can close an eligible
quote paragraph as Setext, and prevents a following root-indented line from
being admitted as lazy quote evidence. Explicit normal quote lines keep the
paragraph open.
Reference-definition admission uses the same leaf boundaries: ATX and thematic
blocks close paragraph state, and a Setext delimiter does so only when it closes
an eligible preceding paragraph. A valid definition after that boundary is a
nonparagraph block and makes an immediate four-space continuation code; an
ordinary paragraph still cannot be interrupted by a definition-looking line.
The [CommonMark 0.31.2 link-label contract](https://spec.commonmark.org/0.31.2/#links)
limits raw content inside the brackets to 999 Unicode code points before
normalization. A soft line ending therefore counts once and a two-code-point
escape such as `\*` counts twice. Definition registration and shortcut, full,
collapsed, and failed-inline fallback resolution all reject 1000 or more
source characters through the same normalization entry point.
Closing-token-order bracket state forbids a nested link's outer target, does not
count an image target as link evidence, preserves an outer link containing an
image, suppresses link candidates only inside a successfully resolved image-alt
subtree, and treats links inside an unresolved image opener as ordinary links.
An independent inline/full/collapsed/shortcut link remains eligible after an
unresolved or escaped literal bracket; only an actually consumed reference
suffix is suppressed. Reference definitions use an escape-aware label closer,
so an escaped `\]` remains label content. They may continue their destination
or move a complete single-, double-, or parenthesized title to the next
immediate line at zero through four visual columns or one tab. A
destination-line remainder containing only spaces or tabs still delegates
title validation to that immediate continuation. A title may span multiple
nonblank lines. Only a definition whose destination and optional title parse
completely contributes a resolved label, and its exact source span—including
the continuation destination and title—is masked from shortcut scanning. An
invalid definition, including a title interrupted by a blank line, remains
ordinary rendered text. Four-space content is absorbed only while a definition
still needs a destination or begins a title; ordinary four-space content after
a complete definition remains indented code. When the destination is already
complete, an invalid title-looking next line does not invalidate the definition:
the definition span ends on the destination and the candidate line remains
rendered. A malformed title on the destination line still invalidates the
whole definition. These rules follow the
[CommonMark 0.31.2 link reference definition grammar](https://spec.commonmark.org/0.31.2/#link-reference-definitions).
Reference-definition labels may likewise cross nonblank soft line endings.
Their escape-aware closing-bracket scan retains each line ending in the raw
999-code-point count, normalizes whitespace for full/collapsed/shortcut lookup,
and keeps the complete multiline label inside the definition source span.
Before container lines are joined with synthetic inline hard boundaries, the
joiner now maps complete definition spans within each root, quote, or list
container. Setext/thematic-looking destination or title continuation lines stay
inside that definition. A real delimiter after the completed definition remains
a boundary, and real Setext/thematic blocks outside definitions are unchanged.
The joiner also retains open-paragraph provenance, so a definition-looking line
inside multiline Setext content cannot be promoted by a synthetic blank. Link
extraction carries unmarked quote/list lazy-line provenance through the joined
rendered view as line metadata. Re-parsing definition spans therefore cannot
reinterpret a lazy `===` as an explicitly owned Setext delimiter and admit a
following definition. Inline tokenization assigns source ownership to complete
valid inline and reference-definition destinations/titles and quote-aware HTML
tokens. Nested link/HTML candidates resolve through two sorted interval sweeps:
an HTML token inside a destination/title remains link syntax, while a link-like
suffix inside an HTML token remains HTML attribute content. Equal endpoints
count as containment; partial overlap does not. Inline suffix ownership is one
monotonic left-to-right commit pass rather than a global fixed point. Completed
definition and HTML tokens are consumed when reached, a code opener consumes
through its next equal-length closer, and only the bracket stack that remains
outside those tokens can propose a suffix. A complete destination/title suffix
is committed atomically only after its opener is already visible. A candidate's
own title backtick therefore cannot retroactively erase a code span that hid
that candidate. An unmatched outer `[` followed by a backtick similarly lets
that backtick open code, and a title-like suffix inside the span cannot
resurrect the hidden link. An orphan `](` owns nothing, while an earlier valid
suffix still protects its internal title backtick by being consumed before the
scanner reaches it. The same bracket rules serve links and images. Backticks
inside committed spans cannot participate in later code pairing. Outside code,
an odd number
of preceding backslashes escapes an opening run while even parity leaves it
active. Once code is open, the next equal-length run closes it regardless of a
backslash inside that code. One sorted two-pointer overlap sweep excludes every
HTML candidate intersecting the resulting non-overlapping code spans; touching
endpoints remain disjoint, and retained HTML tokens preserve source order. An
HTML candidate overlapped by code therefore remains literal code, while owned
angle destinations remain link grammar. Only the remaining valid
HTML opening/closing tag source spans, including quoted, unquoted, and multiline
attributes, become non-whitespace opaque identities before link scanning. A
reversible side-channel intern
registry assigns each distinct token a unique base-6399 unprefixed BMP
private-use sequence of exactly the same source length, retaining CR/LF
positions. Every raw BMP private-use character is injectively escaped under a
reserved `E000` prefix before comparison, so arbitrary source text cannot equal
an HTML identity. Encoded-to-source offsets restore lifecycle-cell labels from
the original text, and each escaped pair counts as one source code point for the
999-character reference-label limit. Identical markup therefore matches across
shortcut, collapsed, and full reference paths, while different same-length tags,
ASCII/Unicode attributes, and raw private-use input remain distinct. Reference
label normalization rehydrates each opaque token's original source only for
CommonMark whitespace normalization and Unicode case folding, so case-equivalent
tag and attribute spelling matches without weakening token opacity or collapsing
distinct canonical markup. Visible
Markdown between tags remains eligible; escaped or invalid openers remain
Markdown text. A valid line-start comment opens a block through the first
`-->`, with its entire closing line opaque even when Markdown follows. Inline
comments instead use strict CommonMark comment grammar: an internal `--`
remains text, and an escaped opener is never a comment. Inline tags and comments
cannot span a blank paragraph boundary. The type-7 HTML-block scanner shares
the same quote-aware valid-tag grammar, so quoted `>` is content while invalid
attributes cannot open an opaque block. The `&lt;!--&gt;` overlap form terminates on
its first line because the closing scan may overlap the opener. HTML block types
2 through 5—comment, processing instruction, declaration, and CDATA—also close
root, quote, and list paragraph state before lazy or indented-code admission. Link
destinations decode only unescaped CommonMark numeric or named character
references with `html.unescape` before percent decoding and POSIX path
normalization; an escaped ampersand remains literal. Lifecycle table cells
collapse rendered link syntax, remove valid inline markup and attributes while
retaining visible child text, decode character references outside code and
backslash escapes, and only then apply NFKC/case and authority normalization.
Definition collection
tracks paragraph state: a definition-looking line cannot interrupt an ordinary
paragraph, while a blank or rendered block boundary reopens definition
admission. A successfully consumed
inline link/image destination and title is one
non-candidate source span, so bracket-looking text inside it cannot become a
shortcut reference; a genuinely adjacent outer reference remains eligible.
Nested link suppression uses the paired-bracket parent tree instead of walking
every ancestor for every candidate. One source-order propagation marks resolved
image ancestors and source-consumed candidates; one reverse propagation marks
candidate-bearing subtrees and suppresses candidate ancestors. Final link order
remains source order, and labels are materialized only for survivors. Hard-inline
boundary positions are indexed once, so nested labels and suffixes do not copy
or rescan their full ancestor text.
CommonMark equal-length backtick runs are paired per hard-bounded
paragraph/container segment in near-linear time regardless of a preceding
backslash. Before that pairing, complete valid inline and reference-definition
destination/title spans and quote-aware inline HTML tokens claim their source;
backticks inside those owned spans cannot open or close code. Brackets inside a
resulting code span never enter link-label pairing, an unmatched opener cannot
mask a later paragraph, and a same-container soft-break code span remains
opaque. Invalid destination/title or HTML-looking text owns no source, so its
backticks retain normal code-span semantics. Code inside a valid link label
remains compatible. Lifecycle-table
detection finds family and transition
columns by header name, accepts GFM delimiter cells with one or more hyphens and
optional colons/pipes, preserves multiple transitions per family, permits
wrapper columns, and excludes non-rendered copies. Table admission rejects any
header, delimiter, or row carrying lazy-continuation provenance; explicit quote
tables and root tables remain eligible. The two Stage 00 lifecycle
tables were replaced by concise pointers to the registry, frontmatter schema,
SDLC governance, and template-routing owners. This is repository-static
evidence only and does not change the ALF-001 live/remote boundary.

| ALF-001 command | Result |
| --- | --- |
| `python3 scripts/validate-document-contract-registry.py --root . --self-test` before implementation | RED: exit 1; `valid-minimal` expected no diagnostics and received `REGISTRY_SCHEMA`. |
| Quality-review RED fixture run | RED: duplicate `status` expected `REGISTRY_PROGRAM_STATE` and received no diagnostic because the last YAML value was accepted. |
| `python3 scripts/validate-document-contract-registry.py --root . --self-test` after review remediation | PASS: 78 cases, 64 profiles, 30 templates, duplicate `status`/`updated`, timestamp rejection, follow-up approval order, legacy-v5 migration fixture, and mutation probes. |
| `python3 scripts/validate-document-contract-registry.py --root . --mode strict` | PASS: baseline 433, new 58, programs 2, uncovered 0, ambiguous 0, and 430 classified paths. |
| Markdown-profile and cross-document self-test plus strict commands | PASS: both self-tests and both current-corpus strict integrations. |
| `ruff check` for the two Python owners; Python AST parse; JSON parse; `git diff --check` | PASS. The optional repository-wide Ruff formatter baseline remains outside this work package; no Ruff lint or syntax issue exists in the changed Python. |
| Changed-file pre-commit with `strict-repository-quality` skipped | PASS for affected-surface validation, JSON, EOF, line endings, whitespace, gitleaks, detect-secrets, and Markdown lint. The skipped aggregate is the already bounded FIFO limitation owned by Spec 039, not an ALF-001 PASS claim. |

| ALF-002 command | Result |
| --- | --- |
| `python3 scripts/validate-links-and-owners.py --root . --self-test` before implementation | RED: exit 1; all six initial program-lineage cases reported `PROGRAM-LINEAGE rules are unimplemented`. |
| Quality-review RED fixture run | RED: seven mutations were accepted incorrectly—paragraph-break, raw-HTML, and indented-code links; a missing ready pair; and three optional-pipe/link-emphasis authority tables. |
| Round-two quality-review RED fixture run | RED: a section-internal heading-adjacent indented-code link was accepted as historical evidence; shortcut-reference and balanced-destination cells plus a nested blockquote table returned no duplicate-authority diagnostic. |
| Round-three quality-review RED fixture run | RED: direct-Spec counting accepted both one Plan/two Tasks and two Plans/one Task when the one-sided extra node linked only into the admitted execution pair. |
| Round-four quality-review RED fixture run | RED: nine gaps reproduced—balanced/escaped reciprocal and execution links, three non-rendered blockquote forms, a raw-HTML-contained heading, extra-family-row and wrapper-column tables, and a 20k unmatched-bracket scan that took 14.457 seconds against a two-second cap. |
| Round-five quality-review RED fixture run | RED: five cross-container labels were accepted incorrectly—reciprocal and execution root-to-quote links plus historical root-to-quote, quote-to-root, and quote-depth transitions. Follow-up RED showed that an execution destination could still close across the boundary. Sibling quote segments were already rejected and a same-container quote soft break remained valid. |
| Round-six quality-review RED fixture run | RED: five full-reference identifiers crossed hard container boundaries—reciprocal and execution root-to-quote references plus historical root-to-quote, quote-to-root, and quote-depth references. A same-container full-reference soft break remained valid. |
| Round-seven quality-review RED fixture run | RED: twelve gaps reproduced—outer quote fences exposed reciprocal and execution links, outer raw HTML exposed historical links, invalid destination remainders were accepted in inline/reference/table links, outer fence/raw blocks exposed lifecycle tables, and unmatched backticks masked valid links in later paragraphs or containers. Valid angle destinations and single/double/parenthesized titles, nested indented code masking, and same-container soft-break code spans already passed. |
| Round-eight quality-review RED fixture run | RED: five gaps reproduced—inline and reference angle destinations admitted an unescaped `<`, quoted-title `)` characters terminated reciprocal and execution links early, and angle-destination `)(` characters terminated historical evidence early. Escaped `\<` already passed; an explicit unmatched-angle case and the prior garbage cases remain rejected. |
| Round-nine quality-review RED fixture run | RED: eleven semantic gaps reproduced—list, setext, thematic, and GFM table boundaries were crossed; non-punctuation escapes were erased in bare, angle, and reference destinations; a nested link exposed its outer target; an adjacent shortcut reference was skipped; and a continued reference destination was ignored. The 4k failed-inline-candidate fixture took 6.790 seconds against a two-second cap. ATX separation and image-only/image-in-link semantics already passed. |
| Round-ten quality-review RED fixture run | RED: four gaps reproduced—an image-alt subtree link counted as reciprocal evidence, unresolved preceding brackets suppressed a following inline link and full reference, and a code-wrapped PRD link normalized into a lifecycle family. Collapsed/shortcut combinations, normal link/emphasis/reference authority cells, nested-link protection, image-only exclusion, and image-inside-link outer evidence already passed. |
| Round-eleven quality-review RED fixture run | RED: four gaps reproduced—a shortcut after an escaped literal bracket was suppressed, inline and full-reference links inside unresolved image openers were suppressed, and a code-formatted label inside a real PRD link lost its rendered family text. The resolved-image subtree negative, image-inside-link outer positive, nested-link guard, and whole-link code lookalike negative remained green. |
| Round-twelve quality-review RED fixture run | RED: five gaps reproduced—link destination/title and image title spans exposed shortcut-looking ARD tokens, a current pair connected to completed follow-up Spec 033 escaped the execution gate, and an invalid garbage reference definition made a PRD reference cell look authoritative. Genuinely adjacent references remain accepted; Round forty-two supersedes this round's provisional active-follow-up execution admission. |
| Round-thirteen quality-review RED fixture run | RED: three gaps reproduced—a valid definition title exposed a shortcut-looking ARD token, and an unescaped nested `(` was accepted in both reference-definition and inline parenthesized titles. Valid next-line single/double/parenthesized titles, an escaped `\(`, and invalid blank-continuation or unclosed-title boundaries already behaved as required. |
| Round-fourteen quality-review RED fixture run | RED: four gaps reproduced—spaces-only and tabs-only destination remainders skipped valid next-line definition titles and exposed shortcut-looking ARD tokens, while nested-parenthesized and unclosed title candidates did not reject their definitions. |
| Round-fifteen quality-review RED fixture run | RED: two gaps reproduced—a definition-looking line interrupted an ordinary paragraph and supplied reciprocal evidence, while `[ARD](not a link)` did not fall back to a valid `[ARD]` shortcut reference after inline parsing failed. Blank and heading block boundaries already admitted definitions correctly. |
| Round-sixteen quality-review RED fixture run | RED: five gaps reproduced—an ordered `123.` item exposed a five-space-indented tilde-fence reciprocal link; an unordered item exposed indented-code reciprocal evidence; nested ordered/unordered raw HTML exposed a historical link; an ordered `12.` item exposed an indented-code execution link; and an ordered `123.` item exposed an indented-code lifecycle table as duplicate authority. An ordered `1.` normal list paragraph link already remained valid evidence. |
| Round-seventeen quality-review RED fixture run | RED: four gaps reproduced—empty unordered or ordered marker lines with two, three, or four trailing spaces used that whitespace as padding, exposing reciprocal, historical, and execution code links plus a lifecycle code table. Empty-marker five-space and same-line four-space/five-space controls already preserved their distinct semantics. |
| Round-eighteen quality-review RED fixture run | RED: six gaps reproduced—unordered and ordered marker-following tab padding plus a tab continuation exposed reciprocal or execution code links, while list reciprocal, list execution, and blockquote historical lazy continuations were split by false container boundaries. Normal unordered/ordered tab content and a list sibling boundary already behaved correctly. Three older plain quote-return fixtures were re-anchored on actual ATX/list block openers because their former unmarked lines are valid lazy continuation under this round. |
| Round-nineteen quality-review RED fixture run | RED: four gaps reproduced—space-only shortcut, tab-only full, soft-break whitespace full, and whitespace collapsed labels normalized to the empty key and resolved through an empty-key definition. Normal spaced and tab-spaced nonempty labels already resolved correctly. |
| Round-twenty quality-review RED fixture run | RED: five gaps reproduced—Setext-following reciprocal, historical, and execution indented links; a thematic-following historical indented link; and a thematic-following indented lifecycle table were treated as rendered evidence. Existing ATX-following indented-code negatives, Setext/thematic boundary cases, and normal-paragraph indented continuation remained correct. |
| Round-twenty-one quality-review RED fixture run | RED: three gaps reproduced—standalone `===` before reciprocal and execution indented links plus standalone `--` before a historical indented link were treated as Setext leaf boundaries. A valid preceding paragraph plus Setext delimiter remained opaque, standalone `---` remained a thematic break, and all earlier ATX/thematic controls passed. |
| Round-twenty-two quality-review RED fixture run | RED: five block-state ordering gaps reproduced. A valid reference definition incorrectly qualified following `===` as Setext and incorrectly let an immediate indented historical link render; root masking hid a list item's blank-separated second paragraph; and active blockquote paragraphs lost unmarked `===`/`--` plus indented-link lazy continuations. `markdown-it-py` in CommonMark mode rendered the definition/standalone-delimiter link, list second paragraph, and both quote continuations, while rendering the definition/immediate-indent control as code. Existing genuine root code and list code-indentation controls remained green. |
| Round-twenty-three quality-review RED fixture run | RED: three gaps reproduced—fully valid quoted definitions incorrectly kept quote paragraph state open and admitted following root-indented reciprocal, historical, and execution links as lazy evidence. A normal quoted paragraph plus unmarked indentation and an invalid definition-looking quote line plus indentation already remained rendered lazy continuations. The valid/invalid distinction and root-code outcome were cross-checked with `markdown-it-py` in CommonMark mode. |
| Round-twenty-four quality-review RED fixture run | RED: three quoted multiline-definition gaps reproduced—an unmarked 1-space destination completed a valid definition, but paragraph state stayed open and admitted root-indented reciprocal, historical, and execution links as lazy evidence. Invalid quoted multiline and valid/invalid list counterparts already preserved paragraph/code behavior. The list controls use a destination below marker content indent to exercise the lazy branch and content-indent-plus-four for code. During remediation, lazy `===`/`--` controls caught and prevented an explicit-Setext regression. |
| Round-twenty-five quality-review RED fixture run | RED: three explicit-marker provenance gaps reproduced—`> paragraph` followed by `> ===` was passed through the lazy branch and admitted root-indented reciprocal, historical, and execution links as quote evidence. An explicit normal quote continuation, plus existing unmarked lazy `===`/`--` controls, already behaved correctly. `markdown-it-py` CommonMark output confirmed explicit Setext closes the quote heading before root code while explicit normal content retains lazy admission. |
| Round-twenty-six quality-review RED fixture run | RED: four leaf-boundary definition-admission gaps reproduced—root thematic and valid Setext plus quote/list ATX boundaries did not admit a following valid definition, exposing immediate indented reciprocal, historical, or execution links. Root ATX already behaved correctly through its rendered hard boundary. An ordinary paragraph definition-lookalike plus indented-link control remained rendered and the earlier paragraph-interruption reference control remained unresolved, confirming definitions still cannot interrupt paragraphs. All six shapes were cross-checked with `markdown-it-py` CommonMark output. |
| Round-twenty-seven quality-review RED fixture run | RED: six 1000-character reference labels resolved through shortcut, full, collapsed, failed-inline fallback, soft-line, and escaped-source paths across reciprocal, historical, and execution surfaces. Their paired 999-character cases already resolved. Official CommonMark confirms the limit applies to raw bracket content before normalization and defines characters as Unicode code points; the soft-line fixtures count LF once, while escaped fixtures count each backslash and punctuation source code point. |
| Round-twenty-eight quality-review RED fixture run | RED: six reference-definition grammar gaps reproduced—an escaped `\]` closed the definition label early; destination continuations at zero, four, and tab columns were ignored; and zero-column plus multiline title source spans exposed fake reciprocal links. Four-column/tab title-span controls, a blank-line-invalid title that must remain rendered, and a complete-definition/four-space-code contrast were already green and remain locked as reviewer controls. Official CommonMark supplies the escape-aware label close, next-line destination/title, multiline-title, blank-line rejection, and complete-source-span basis; the accepted four-column/tab continuation boundary follows this program's explicit round constraint. |
| Round-twenty-nine quality-review RED fixture run | RED: three complete definitions were discarded when their next line looked like an unclosed double title, an invalid nested-parenthesized title, or a closed title followed by garbage. CommonMark keeps the already complete destination definition and renders the failed optional-title candidate as ordinary paragraph content. GREEN separates same-line failure from next-line fallback, covers a continued destination, and proves both real reference resolution and rendered phantom-link behavior. |
| Round-thirty quality-review RED fixture run | RED: all six definition-aware join fixtures failed. A complete continued destination followed by a real `---` delimiter was split before its destination, losing reciprocal, historical, and execution evidence in root, quote, and list containers. A valid `===` destination was also split, so a later duplicate definition incorrectly won instead of preserving CommonMark first-definition semantics. GREEN maps definition ownership before adding synthetic Setext/thematic boundaries; actual post-definition delimiters and true external Setext/thematic blocks remain boundaries. |
| Round-thirty-one quality-review RED fixture run | RED: three open-paragraph definition lookalikes were promoted after the joiner inserted a blank before their Setext delimiter in root, quote, and list containers. Numeric and named character references plus entity-produced percent escapes were not decoded in reciprocal, historical, or execution destinations, and numeric/named rendered table labels were not recognized as lifecycle authority. GREEN retains paragraph continuation provenance, decodes unescaped entities before percent/path normalization, and decodes rendered cell text before NFKC. Invalid named references and escaped ampersands remain literal; code spans remain entity-literal. |
| Round-thirty-two quality-review RED fixture run | RED: three unmarked quote/list `===` continuations lost lazy provenance after the rendered container was joined, so a following reference definition was admitted as reciprocal, historical, or execution evidence. Three valid inline HTML attribute spans likewise exposed bracket-looking links from a span, anchor, or multiline opening tag. GREEN carries lazy-line metadata through definition re-parsing and masks only valid inline HTML token spans. Markdown between tags, escaped/invalid openers, comments, explicit Setext, and real definition boundaries remain reviewer controls. |
| Round-thirty-three quality-review RED fixture run | RED: space-masked inline tags promoted `<b>[owner]: ...` into a reference definition and collapsed markup-bearing reference labels; an escaped comment opener hid a real execution link; the type-7 block matcher rejected a valid quoted `>` but accepted invalid `!!!` attributes; and inline wrappers hid visible lifecycle header, family, and transition text. GREEN uses non-whitespace opaque sentinels for syntax scanning, escape-aware comments, shared quote-aware tag grammar, and a separate markup-stripped rendered-cell view. Actual comments, attributes, escaped/invalid openers, and all Round 32 controls remain locked. |
| Round-thirty-four quality-review RED fixture run | RED: one repeated opaque sentinel made different same-length inline HTML tokens normalize to the same reference label, so `<i>`/`<b>` shortcut labels, ASCII-attribute collapsed labels, and Unicode-attribute full labels resolved across markup that CommonMark keeps distinct. GREEN interns raw tokens into collision-free reversible same-length private-use identities. Identical markup still resolves through shortcut/collapsed/full paths, markup-bearing raw labels preserve the 999/1000 boundary, and link syntax inside attributes remains opaque. |
| Round-thirty-five quality-review RED fixture run | RED: line-start comment blocks exposed Markdown on their closing line; invalid inline comments hid real links; inline tags crossed blank paragraph boundaries; multiline definition labels failed basic, escaped, and raw-999 resolution; and one/two-hyphen GFM delimiter cells were not recognized as tables or authority. GREEN separates line-start block from strict inline comment state, bounds inline tokens to one paragraph, scans escape-aware multiline labels into complete source spans, and accepts optional-colon/pipe delimiters with one or more hyphens. Next-line comment-block evidence, valid inline trailing links, and raw-1000 rejection remain controls. |
| Round-thirty-six quality-review RED fixture run | RED: code-span masking erased invalid backtick suffixes before inline and definition grammar ran; quote-owned comment/processing blocks left paragraph state open; `&lt;!--&gt;` missed its overlapping closer and swallowed the next line; and a lazy quote paragraph was promoted to lifecycle-table authority. GREEN parses HTML-opaque/code-raw syntax before filtering link openers by rendered code spans, treats HTML block types 2–5 as container leaf boundaries, permits the overlapping closer, and excludes lazy-provenance table lines. Code-only links, list CDATA, root declarations, explicit quote tables, and root tables remain controls. |
| Round-thirty-seven quality-review RED fixture run | RED: a `]` rendered inside a code span closed the surrounding reciprocal link label, a backslash-adjacent backtick case opened a false execution code span under the then-current tokenizer, a different-length inner backtick run exposed the same bracket-pairing error, and raw BMP private-use text reproduced an opaque HTML identity. GREEN excluded span-internal brackets while retaining surrounding links and separated raw BMP private-use text from HTML identities with an injective prefix namespace and source-offset side channel. Round forty-one owns the final context-sensitive backslash interpretation. Code-only links, identical raw labels, and raw 999/1000 limits remain controls. |
| Round-thirty-eight quality-review RED fixture run | RED: an HTML candidate consumed a code-span closer and hid a following execution link; inline and reference `<foo>` destinations returned opaque PUA instead of `foo`; code-rendered `<i>` was removed and promoted adjacent `PRD` to false lifecycle authority; and case-equivalent tag or Unicode-attribute reference labels did not resolve. GREEN tokenizes code first, reserves link-grammar angle destinations before masking only non-code HTML, and rehydrates structured token source solely for reference-label whitespace normalization and Unicode case folding. Distinct tags remain distinct and collision-free. |
| Round-thirty-nine quality-review RED fixture run | RED: four ownership-order gaps remained, and backticks inside a valid angle destination, valid inline title, or valid HTML attribute incorrectly participated in code-span pairing and hid a following execution link. GREEN gave complete valid inline/reference destination-title suffixes and quote-aware HTML tokens source ownership before matching the remaining equal-length runs. Nested ownership resolves by containment, preserving both destination-contained angle tokens and existing HTML-attribute-embedded link negatives. Round forty-one supersedes this round's provisional treatment of a preceding backslash. |
| Round-forty quality-review RED fixture run | RED: orphan `](` suffixes claimed their complete backtick-bearing remainder without a matching label opener, exposing reciprocal and execution links that CommonMark renders inside code; the historical counterpart was already fail-closed. GREEN derives provisional raw code spans, reuses bracket token state to require a paired non-code/unescaped opener, and grants ownership only when the paired close is immediately followed by a fully parsed inline destination/title. Existing nested/adjacent links, image/link containment, label code spans, and failed-candidate performance remain controls. |
| Round-forty-one quality-review RED fixture run | RED: an odd-backslash escaped opening run hid a rendered execution link, and the then-provisional unmatched-outer-bracket expectation treated `/t` as rendered. GREEN established context-sensitive odd/even opener parity and inside-code closer behavior, but retained a raw/raw-code-aware candidate union. Round forty-three supersedes that union and corrects the exact case against the CommonMark oracle. Actual code-wrapped links, orphan suffixes, nested/adjacent links, image/link containment, and code-bearing labels remain controls. |
| Round-forty-two requirements-review RED fixture run | RED: after the base fixture removed the active follow-up Plan/Task pair, every lineage case gained an execution diagnostic because dependency-ready selection incorrectly considered `followUps`. GREEN selects only the first original tranche whose state is not `done` or `archived`; active direct and draft indirect follow-up components now fail, while explicit follow-up absence, the exact first-original pair, completed/blocked absence, and disconnected other-program components remain controls. The stable diagnostic expected/actual tuple now names original-tranche readiness. |
| Round-forty-three quality-review RED fixture run | RED: CommonMark renders `` [`[x](/t "`") `` as literal `[` plus a code span and trailing text, but direct extraction returned `/t` and lineage admitted the hidden execution link. Three scale fixtures also reported that the interval sweep was absent. GREEN removes the raw-pair union, admits only code-aware active brackets for ordered atomic suffix parsing, and replaces both link/HTML nested `any(...)` checks with stable sorted sweeps. Ordinary valid title-backtick links, odd escaped openers, inside-code backslash-prefixed closers, even-parity openers, actual code wrappers, orphan/nested/adjacent/image/reference controls, and equal-endpoint/nesting/partial-overlap semantics remain covered. Independent valid link plus opening/closing HTML-token sets at 2k, 4k, and 8k retain exact counts with each containment scan bounded by the total interval count. |
| Round-forty-four quality-review RED fixture run | RED: three 2k/4k/8k code-wrapped HTML fixtures reported that the interval overlap sweep was absent; the old token-by-code-span `any(...)` path measured 0.121/0.469/1.766 seconds. GREEN reuses the ordered interval result and source-order index helper in a two-pointer overlap sweep. The same inputs retain 4k/8k/16k raw HTML tokens, 2k/4k/8k code spans, and zero visible HTML with deterministic work `5999/11999/23999`, each below the `3n` bound; observed times were 0.0171/0.0339/0.0603 seconds. Before, inside, covering, after, and touching-boundary intervals; mixed visible/hidden HTML; odd/even opener parity; inside-code backslash-prefixed closer behavior; and actual code wrappers remain controls. |
| Round-forty-five quality-review RED fixture run | RED: `` [y](/u "`")`[y](/u "`") `` returned two `/u` links because each candidate provisionally claimed its own title backtick before opener visibility was final. Three 2k/4k/8k nested-link fixtures separately reported that bracket-tree suppression was absent. GREEN replaces the circular provisional set with a monotonic source-order token/stack pass and replaces two per-candidate ancestor walks with top-down image/source eligibility plus bottom-up candidate-subtree propagation. The nested generator keeps only the deepest `/t`, suppresses 1999/3999/7999 ancestors, and performs exactly 4000/8000/16000 tree steps (`2n`, below `3n`); observed full extraction times were 0.0268/0.0556/0.1036 seconds. Adjacent links, first-hidden/second-visible variants, ordinary title backticks, unmatched outer code, odd/even openers, malformed nested links, resolved/unresolved image ancestors, outer links containing images, references, orphan suffixes, and output order remain controls. |
| Round-forty-six quality-review RED fixture run | RED: an escaped first backtick followed by an adjacent raw run exposed `/t` instead of letting the unescaped tail open code; whitespace inside nested parentheses was accepted in both inline and reference bare destinations, and an invalid outer link consumed its valid inner Task link; three 2k/4k/8k blank-separated owned-backtick fixtures reported the ownership work helper absent; and four 500/1k/2k/4k execution chains reported the adjacency index absent. GREEN preserves raw-run closer semantics while treating only the unescaped tail as an outside-code opener, fails nested bare-destination whitespace closed without suppressing an inner valid candidate, advances one ownership cursor across all paragraph segments, and builds incoming/undirected execution adjacency plus connected-component and Spec-seed caches once. Backtick ownership work was `9999/19999/39999` steps in `0.0173/0.0344/0.0694` seconds; execution closure was `3499/6999/13999/27999` steps in `0.0009/0.0018/0.0062/0.0111` seconds, with second-query zero-step identity reuse. |
| Round-forty-seven quality-review RED fixture run | RED: U+001C in inline and reference bare destinations was stripped into a valid shorter target, while NBSP, EM SPACE, and IDEOGRAPHIC SPACE were misclassified as separators; NUL, VT, FF, US, and DEL controls were likewise accepted or truncated. Three 2k/4k/8k HTML-token plus shortcut-label fixtures separately reported that the opaque-label interval index was absent. The [CommonMark 0.31.2 link grammar](https://spec.commonmark.org/0.31.2/#links) is the character oracle: bare destinations exclude ASCII controls and U+0020, component separators are space/tab plus at most one line ending, and non-ASCII spaces remain characters. `markdown-it-py` agreed on inline controls and Unicode destinations but normalized the U+001C reference-definition case differently, so the normative grammar governs that exact negative. GREEN uses CR/LF-only source splitting, explicit ASCII-control/bare-destination predicates, and a space/tab plus single-CR/LF/CRLF separator scanner; title-internal controls and Unicode spaces remain content, including a multiline NBSP-only title line. Opaque token starts are indexed once, each label uses a measured binary interval lookup, and full-containment semantics survive adjacent, covering, and touching controls. Indexed work was `29964/63917/135822` steps within bounds `34015/72016/152017`; complete probes resolved `2000/4000/8000` links in `0.0926/0.2097/0.4395` seconds. |
| Round-forty-eight requirements-review RED fixture run | RED: `_local_destination` used generic Unicode `strip()`, so canonical owner paths with leading or trailing NBSP, EM SPACE, or IDEOGRAPHIC SPACE—and a direct trailing U+001C control—collapsed onto the canonical document. The same defect let an inline NBSP target satisfy Spec-to-ARD reciprocity and a reference-form EM SPACE target satisfy current execution direct-Spec admission. Exact canonical, percent-decoded, character-reference-decoded, and backslash-escaped punctuation controls already resolved correctly. GREEN consumes the parser-owned destination verbatim before scheme, percent, and POSIX path handling; all six Unicode-space edge forms remain distinct local paths, rendered inline/reference extraction retains the character, both lineage false-evidence cases produce their stable diagnostics, and the canonical normalization controls remain green. |
| Round-forty-nine root quality-review RED fixture run | RED: the rendered angle destination `http://[` raised `ValueError` in `urlsplit()` and stopped validation; a Windows drive path was classified as an external URI before the explicit absolute-path rule could run. GREEN uses a non-throwing RFC-style ASCII scheme predicate after network and drive-absolute checks. The malformed URI remains external, drive paths remain rejected as absolute, and canonical local, anchor, network, and ordinary external controls pass. |
| `python3 scripts/validate-links-and-owners.py --root . --self-test` after quality-review remediation | PASS: 336 isolated lineage cases cover the valid tree, five stable diagnostics, outer-first raw/fence opacity, ownership-before-indented/Setext block masking, root and container-local valid-definition nonparagraph state including leaf-boundary admission and lazy-completed multiline definitions, definition-aware container joining with true post-definition delimiters, open ordinary paragraphs, and joined lazy-line provenance preserved, invalid/incomplete-definition paragraph retention, explicit-versus-lazy continuation provenance, CommonMark/GFM hard block/container boundaries with valid soft breaks, raw 999-code-point reference-label admission with 1000-character fail-closed rejection before normalization, escape-aware definition-label closure, zero-through-four-column and tab destination/title continuations, blank-free multiline-title masking, complete-definition versus following-indented-code disambiguation, ordered code-aware paired-opener inline suffix ownership without raw-pair resurrection, odd/even outside-code backslash parity, inside-code closer matching, ownership-first inline/reference destination-title and quote-aware HTML token spans, code-span bracket exclusion, and rendered-code opener suppression, same-line invalid-title rejection with next-line invalid-title fallback, collision-free reversible same-length HTML identities, token-source Unicode case folding across shortcut/collapsed/full and ASCII/Unicode attributes, plus injectively namespaced raw BMP private-use input, block/definition grammar and raw 999/1000 reference-label identity preserved including escape-aware multiline definition labels and complete source spans, HTML type-2–5 container leaf boundaries, line-start comment-block closing-line opacity with overlapping-closer termination, strict escape-aware inline comments, paragraph-bounded inline HTML, quote-aware valid type-7 HTML blocks, rendered wrapper text with attributes ignored, and visible Markdown plus escaped/invalid-opener controls, CommonMark numeric/named destination and rendered-cell character references with escape/code protection and entity-before-percent/path/NFKC ordering, context-sensitive Setext leaf termination, standalone delimiter-like paragraph continuation, thematic-break disambiguation, ATX/Setext/thematic leaf-block termination followed by definition and indented-code opacity with normal-paragraph continuation preserved, ordered/unordered marker-width, four-column tab stops with overshoot preservation, empty-marker normalization, same-line five-or-more padding fallback, active list/blockquote lazy continuation with actual fence/raw/indent/heading/list-sibling boundaries, nested list/fence/raw/indented-code/table opacity with normal list paragraph evidence, nonempty normalized reference-label admission across definitions and shortcut/full/collapsed/fallback usage, punctuation-only destination escapes, resolved link/image/reference token state with consumed destination/title spans, block-aware exact valid-definition source-span masking, multiline and fully validated definitions/titles including whitespace-only destination remainders, failed-inline shortcut fallback with a literal unconsumed suffix, code-masked offset-stable lifecycle-cell normalization with original display-label recovery, paragraph/container code-span recovery, preserved adjacent/collapsed/shortcut references, first-original-tranche execution cardinality/reciprocity plus remaining-tranche and follow-up component absence, one-plus-hyphen optional-colon/pipe GFM delimiter, lazy-provenance table exclusion with explicit quote/root positives, table header/transition variants, exact diagnostic tuple/count/path/text/owner/order, deterministic sub-two-second unmatched-bracket, unmatched-backtick-run, and failed-inline-candidate caps, plus 2k/4k/8k independent valid-link/HTML containment, code-wrapped HTML/code overlap, nested bracket-tree suppression, and blank-separated backtick-ownership sweeps together with 500/1k/2k/4k execution-component chains and 2k/4k/8k opaque-label/token index sweeps with exact counts, monotonic source-order ownership, survivor-only label materialization, malformed/image controls, endpoint/source-order retention, cached execution-result identity, ASCII-control versus Unicode-space destination/title controls, CR/LF/CRLF separator controls, opaque-token adjacent/covering/touching retention, exact Unicode-space local-path retention with reciprocal/execution false-evidence rejection, indexed label work bounds, and linear work bounds. The isolated 4k failed-candidate probe fell from 6.790 seconds to 0.025 seconds. |
| `python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry` | PASS: zero current-corpus cross-document diagnostics. |
| Markdown-profile self-test and strict registry-body mode; document-contract registry strict mode | PASS: zero Markdown-profile diagnostics; 430 classified paths, two programs, zero uncovered paths, and zero ambiguous paths. |
| Ruff, Python compile, JSON parse, `git diff --check`, and changed-file Markdownlint | PASS: no Python lint/syntax error, malformed fixture JSON, whitespace error, or Markdown violation. |

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ALF-001](../plans/2026-07-15-authority-and-lineage-foundation.md#task-1-introduce-typed-registry-v6-program-relations) | Done. | Closed-v6 schema/data, `Registry.program_lineage`, duplicate-key/timestamp/approval-order review remediation, 78-case self-test, strict 430-path PASS, and independent requirements/quality approval provide repository-static evidence. |
| [ALF-002](../plans/2026-07-15-authority-and-lineage-foundation.md#task-2-enforce-cross-document-lineage-and-execution-admission) | Done. | Typed cross-document lineage diagnostics, 336 isolated cases, forty-nine review-remediation rounds, Stage 00 authority-table retirement, independent requirements/quality approval, root fallback review, and strict current-corpus PASS are included in the logical ALF-002 commit. |
| [ALF-003](../plans/2026-07-15-authority-and-lineage-foundation.md#task-3-normalize-the-current-audit-remediation-overlay) | Queued. | This Task will record observation-preservation, overlay, review, and commit evidence. |
| [ALF-004](../plans/2026-07-15-authority-and-lineage-foundation.md#task-4-validate-and-close-the-authority-foundation) | Queued. | This Task will record full QA, review verdicts, rollback, and closure evidence. |
