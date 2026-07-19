---
title: "Archive Record: Task: Archive Record and Workspace Boundary"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-07-18"
original_type: "task"
original_path: "docs/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md"
archived_on: "2026-07-18"
archive_reason: "completed-lineage"
replacement: null
source_commit: "a12aedfb71ccabd329dabc83bd2863474d1126b0"
source_blob: "e40edd14c8bef4983907a75d7cc7b823412163e6"
content_sha256: "f3badfc88f43281138d82ace386316e0d3f69bbc5a31ea9ea210f9b6597524fb"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'Task: Archive Record and Workspace Boundary'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-18
---

# Task: Archive Record and Workspace Boundary

## Overview

This Task is the terminal staged execution, verification, review, and rollback
ledger for ARWB-001 through ARWB-005. It records the completed implementation
packages, the exact eight-file ARWB-005 closure proposal, and fresh independent
whole-tranche verdicts `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no
findings. Closure commit `855fa78` and post-commit repository-static checks are
recorded. It does not claim remote/live readiness or any inspection of ignored
scratch.

Planning commit `04a4d32` activated the reciprocal Spec 036 Plan/Task pair.
ARWB-001 was committed as `6b9b9cd` from parent `04a4d32`, ARWB-002 as
`f8a54dd` from parent `6b9b9cd`, ARWB-003 as `787b28f` from parent `f8a54dd`,
and ARWB-004 as `87ff444` from parent `787b28f`. The bounded pre-closure range
extends through prerequisite remediation commit `4ccc616` from parent
`87ff444`. That remediation binds the historical ARWB-003 registry proof to
committed cutover `787b28f` through closed Git-object resolution and received
`REQUIREMENTS COMPLIANT` plus `QUALITY APPROVED`. The range is
`04a4d32^..4ccc616`, rollback parent is `4ccc616`, and closure commit is
`855fa78`.

## Inputs

- [Archive Record and Workspace Boundary Implementation Plan](../plans/2026-07-17-archive-record-and-workspace-boundary.md)
- [Spec 036](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive index](../../98.archive/README.md)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [`_workspace` tracked boundary](../../../_workspace/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ARWB-001 | VAL-ARWB-001, VAL-ARWB-002, VAL-ARWB-004, VAL-ARWB-007 | Define exact Git-object recovery and ArchiveEnvelope.v1 parser/schema capability without activating production archive authority. | platform | Done | Focused implementation, independent reviews, and logical commit complete. | Initial RED: missing private module. Requirements RED: ten tests with five expected failures. Quality RED: fifteen tests with two failures and three errors. GREEN: 15/15 plus Ruff/compile and strict document gates. Independent verdicts: `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`. Logical commit: `6b9b9cd`; commit parent: `04a4d32`; no production authority or workspace guard changed. |
| ARWB-002 | VAL-ARWB-002, VAL-ARWB-003, VAL-ARWB-005, VAL-ARWB-007 | Implement fail-closed archive, provenance, integrity, historical-link, current-authority, and immutability validation. | platform | Done | Focused implementation, independent reviews, and logical commit complete. | Initial RED: missing module, then 14 cases with nine failures. Quality RED: 22 cases with 17 failures and 13 errors. GREEN: 22/22 focused and 37/37 ARWB regression, canonical link self-test, Ruff/compile, strict document gates, Markdownlint, and diff check. Verdicts: `REQUIREMENTS COMPLIANT`, initial `QUALITY CHANGES REQUIRED`, final `QUALITY APPROVED`. Logical commit: `f8a54dd`; parent: `6b9b9cd`. |
| ARWB-003 | VAL-ARWB-001 through VAL-ARWB-005 | Atomically activate production archive authority, migrate 31 records, prove 202 links, cut index/current authority, and retire the duplicate archive role. | platform | Done | Focused implementation, independent reviews, and logical commit complete. | Named RED: `ARCHIVE-CUTOVER-INCOMPLETE`. GREEN: manual cutover `records=31 historical_links=202 secret_clean=31`; combined archive suite 57/57; exact finite-admission regression 11/11; dedicated runner/hook/provider result 15/15; registry v8, Markdown, cross-document, lifecycle 666-case self-test, Ruff, and cutover-excluding aggregate evidence recorded below. Secret classification used exit 17, integer timeout 10, suppressed stdout/stderr, and returned source=31 pass=31 detected=0 error=0. Final verdicts: `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`. Logical commit: `787b28f`; parent: `f8a54dd`. |
| ARWB-004 | VAL-ARWB-006 | Enforce `_workspace` as one tracked README plus unread ignored scratch using Git metadata only. | platform | Done | Focused implementation, independent reviews, and logical commit complete. | Initial RED: focused unittest failed because the production validator was absent. Initial GREEN: 10/10. Quality review: `QUALITY CHANGES REQUIRED` because actual-worktree `check-ignore` admitted ignored-child authority. Remediation RED: one failure and one error across the two hostile-child cases. Remediation GREEN: 16/16 focused methods, isolated self-test, production metadata/object proof, repository aggregate, Ruff check/format, Python compile, Bash syntax, strict Markdown/link, and diff check pass. Final verdicts: `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`. Logical commit: `87ff444`; parent: `787b28f`. |
| ARWB-005 | VAL-ARWB-001 through VAL-ARWB-007 | Reproduce incomplete closure, run full local QA, prepare Spec 036's atomic lifecycle closure for independent review, then record the committed repository-static postflight. | platform | Done | Exact eight-file closure proposal, local repository-static QA, independent whole-tranche requirements/quality reviews, closure commit, and post-commit static checks complete. | Spec-only staged RED exited 2 with `LIFECYCLE-BASE` observing `REGISTRY_PROGRAM_STATE`. Prerequisite remediation `4ccc616` received `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, after which the complete proposal passes staged lifecycle, focused 87/87, and the direct aggregate. Fresh whole-tranche closure reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings. All-files pre-commit records `strict-repository-quality` as `SKIP` because the separately run aggregate is PASS and the hook's Spec 039 FIFO boundary remains isolated. Package commits: `6b9b9cd`, `f8a54dd`, `787b28f`, `87ff444`; planning commit: `04a4d32`; rollback parent: `4ccc616`; pre-closure range: `04a4d32^..4ccc616`; closure commit: `855fa78`. Post-commit explicit-ref lifecycle `4ccc616..855fa78`, strict registry 434 paths, snapshot-DEFER, and clean-tree checks passed. |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/036-archive-record-and-workspace-boundary/**`
  and its Stage 03 index; this reciprocal Plan/Task and Stage 04 indexes;
  `docs/98.archive/**`; archive-specific `docs/99.templates/support/**` and
  `docs/99.templates/templates/**`; `_workspace/README.md` only; archive,
  lifecycle, Markdown, link/owner, and workspace metadata validators in
  `scripts/**`; their exact fixtures and script/test indexes; directly
  implicated Stage 00/.github descriptions; the three migration-ledger rows
  owned by Spec 036 and this pair.
- **Forbidden Paths**: ignored `_workspace` children; secrets, credentials,
  tokens, auth files, shell history, kubeconfigs, Vault data, local diagnostics;
  Kubernetes/GitOps desired state, infrastructure, provider runtime adapters,
  unrelated current documents, completed Plan/Task movement, Spec 037-040
  bodies except read-only boundary checks, and bulk non-archive rewrites.
- **Approval Required**: Any remote GitHub change, live system action, secret
  handling, dependency installation, protected-surface expansion, publication,
  push, or merge requires separate explicit human approval.
- **Static Validation**: Named archive/recovery/workspace self-tests, exact
  31/202 proofs, strict registry/Markdown/link/lifecycle checks, repository
  aggregate, changed-file Markdownlint, diff check, and all-files pre-commit.
- **Live Validation**: `DEFER`. This tranche authorizes repository-static Git
  object and document evidence only; it has no provider or cluster lane.
- **Secret / Vault Handling**: Automated archive validation may stream tracked
  Git blob bytes in memory only into the repository secret classifier. It must
  emit redacted path/code diagnostics and never payloads, matches, or values;
  a detection marks the record `BLOCKED` and stops envelope creation. Agents
  and logs must not display secret-bearing history. Never inspect ignored
  scratch to search for secrets or evidence.
- **Rollback Plan**: Before the uncreated closure commit, discard or replace
  the exact eight-file staged proposal, leaving parent `4ccc616` unchanged. For
  full-tranche rollback, revert newest ARWB commit first and remove consumers
  before the archive contract. After terminal closure, stage one
  complete ARWB-005-through-ARWB-001 reverse patch, validate the restored
  compatible state only after the full patch is assembled, and create one
  atomic rollback commit. Planning commit is `04a4d32`, current rollback parent
  is `4ccc616`, and the pre-closure range is `04a4d32^..4ccc616`.
- **Evidence Location**: This Task, logical Git commits, exact archive/index
  records, focused fixtures, and durable tracked migration evidence. Ignored
  scratch and dry-run logs are never closure evidence.

The `_workspace` no-read boundary is absolute for automated validation. An
agent or script must not list the directory, expand a child glob, recurse,
open, stat by discovery, hash, copy, move, or delete ignored children. It may
query the Git index and ignore rules for an explicit non-created probe path.

## Verification Summary

Planning activation began from repository baseline `04cb3a6`, after Spec 035
closed and made Spec 036 the first unfinished PRD-006 tranche. The approved
Spec and ADR record a 31-record recovery inventory and 202 historical links,
but that activation package had not rerun or claimed those results. No archive
payload, registry route, form, validator, index, current link, or workspace
guard was changed by the activation package.

The reciprocal active Plan/Task pair was the only current execution component
for Spec 036 at activation. Spec 037 remained active as a design contract with
no Plan/Task. Focused activation checks covered exact route admission, five-key frontmatter,
canonical body contracts, reciprocal rendered links, stage-index membership,
three 14-column ledger records, and whitespace integrity. Long repository
aggregate and all-files lanes are deferred until implementation or closure and
are not represented as planning PASS evidence.

The focused activation run passed with both then-untracked execution files
supplied as explicit candidates: strict registry classified 434 paths across two
programs (`baseline=433`, `new=62`, uncovered 0, ambiguous 0), strict Markdown
reports zero violations, strict cross-document validation accepts the sole
Spec 036 reciprocal pair, changed-file Markdownlint passes, and
`git diff --check` reports no whitespace error.

ARWB-001 then added an import-only private recovery module and one focused
unit-test surface. The intentional RED command
`python3 -m unittest tests/test_archive_recovery.py` exited 1 because
`scripts.archive_recovery` did not exist. After the minimal implementation,
the same command first ran seven cases and passed. Requirements review then
identified missing duplicate-key, canonical-serialization, and raw-path
normalization negatives. The expanded ten-test RED ran with five expected
failures: one duplicate key was accepted, CRLF returned the wrong diagnostic,
extra spacing was accepted, and both `./` and repeated-separator paths were
accepted. The remediation now rejects duplicate mappings, requires loaded
metadata to serialize byte-identically as canonical UTF-8/LF frontmatter, and
requires raw repository paths to equal their `PurePosixPath` rendering.
Requirements re-review returned `REQUIREMENTS COMPLIANT`. Quality review then
required Ruff conformance, payload-free dataclass representations, literal Git
pathspecs, real SHA-256 repository evidence, deterministic bounded Git
execution with stable errors, DEL rejection, and a non-authoritative name for
the bounded inline-link count. The expanded fifteen-test RED ran with two
failures and three errors before those changes. The cases use temporary Git
repositories to prove SHA-1 and SHA-256 commit/blob identity, raw `cat-file`
bytes, byte count, payload SHA-256, non-authoritative inline-link candidate
count, mirrored archive-path proposal, UTF-8
admission, the closed reason/replacement dependency, exact marker placement,
payload-to-EOF collision safety, final-newline preservation, and rejection of
worktree-byte substitution. It also proves literal metacharacter paths,
global/system/graft/replace/lazy-fetch isolation, bounded Git subprocesses,
payload-free representations, and stable non-disclosing process/root/object-
format failures. Quality re-review returned `QUALITY APPROVED`. ARWB-001 was
committed as `6b9b9cd` from parent `04a4d32`. The 31-record/202-link corpus
proof and ARWB-002 through ARWB-005 remained pending at that package boundary,
so the Task and Spec stayed active.

Post-implementation focused evidence is repository-static: the same unit-test
command passes `15/15`; `ruff check`, `ruff format --check`, and
`python3 -m py_compile` pass for the module and test;
strict registry reports 434 classified paths with `baseline=433`, `new=62`,
two programs, and zero uncovered or ambiguous paths; strict Markdown reports
zero violations; strict cross-document validation reports valid; changed-file
Markdownlint and whitespace/final-newline checks pass. This is focused
repository-static evidence, not the canonical affected runner. Affected,
staged, all-files, message/manual, CI, and remote/live lanes are not claimed by
the ARWB-001 package. Its logical commit is `6b9b9cd` from parent `04a4d32`;
rollback before later-package consumption is the bounded revert of that commit.

ARWB-002 began with `python3 -m unittest tests/test_archive_validation.py`
failing because the import-only validator module did not exist. After the
immutable interfaces were introduced as empty skeletons, the named 14-case RED
ran with nine expected failures covering metadata order/type, blob/digest and
payload mutation, wrong mirror, source-tree miss despite current-tree
existence, archive reactivation, active direct individual-archive navigation,
duplicate `original_path` authority, and archive mutation/deletion. The minimal
implementation now parses the ARWB-001 envelope, recovers provenance from full
Git objects, checks sanitized literal source-tree paths, and imports the
filesystem-free canonical CommonMark adapter from
`validate-links-and-owners.py` by fixed script path. Current authority consumes
only passed frozen Markdown/profile inputs; immutability consumes passed base
and proposed byte mappings. Payload, Markdown, and resolved target values are
excluded from representations and diagnostics.

Independent requirements review returned `REQUIREMENTS COMPLIANT`. Initial
quality review returned `QUALITY CHANGES REQUIRED` because current authority
did not close its inventory/status/profile inputs, the predictable dynamic
module cache and adapter return were trusted, malformed public containers could
raise or fail open, and the completed requirements verdict was not recorded.
The expanded 22-case quality RED ran with 17 failures and 13 errors, including
raw `KeyError`, `TypeError`, and `AttributeError` paths. Remediation now
materializes exact record/document sequences and archive mappings before sort
or dereference; validates every inventory member, mapping key/value, canonical
path, and finite current status/profile; and treats every active/accepted path
below `docs/98.archive` except the exact index as reactivated independently of
caller inventory. The fixed canonical adapter path is loaded under a private
unique verified module identity rather than a predictable cache entry. Import,
call, sequence, link-kind, and target-shape failures collapse to one stable
payload-free diagnostic.

A residual quality pass caught the empty-parts `.` path and invalid repository-
root boundary. The final patch rejects those values before adapter or Git use,
prevalidates mixed record fields before sorting, and fixes the same empty-path
rule in the public rendered-link adapter. The final quality re-review returned
`QUALITY APPROVED`.

The focused ARWB-002 suite passes 22/22 and the combined ARWB-001/002 suite
passes 37/37. The canonical cross-document self-test passes; Ruff check and
format, Python compile, strict registry (`434` paths, `baseline=433`, `new=62`,
two programs, zero uncovered/ambiguous), strict Markdown (zero violations),
strict cross-document validation, changed-document Markdownlint, and
`git diff --check` pass. This is import-only repository-static evidence; it
does not activate a production archive route/form/predicate, inspect or migrate
the 31-record corpus, claim the 202-link proof, retire Tombstones, or inspect
ignored `_workspace` children. The logical commit is `f8a54dd` from parent
`6b9b9cd`.

ARWB-003 began with the named production RED
`ARCHIVE-CUTOVER-INCOMPLETE`. The atomic cutover then replaced the exact 31
mirrored records with canonical ArchiveEnvelope.v1 frontmatter, marker, and
payload-to-EOF bytes. Twenty-six records recover from source commit
`5e0221525450dbdacb585e6c98ade3f060ddc827`; five recover from
`82f0e1922d9748a88b1487a32a59629ba523f408`. The production validator proves
31 unique original paths, exact full commit/blob identities, payload SHA-256,
31 replacements, 202 source-commit historical links, a complete 31-row index
manifest, zero direct current links to individual records, and the single
`content/archive`/`template/content/archive` authority in registry v8.

Secret classification streamed each exact recovered Git-blob payload to
`gitleaks` with detection exit 17 and integer timeout 10 while suppressing
stdout and stderr. The redacted aggregate is `source=31 pass=31 detected=0
error=0`; no payload, match, or secret value was printed or retained in
diagnostics. The canonical template is now `archive-record.template.md`; the
old form/profile and metadata-only production gate are absent. Current
navigation routes through `docs/98.archive/README.md`, including all 31 Current
research-ledger destinations.

Local GREEN evidence is: explicit local/manual production cutover
`records=31 historical_links=202 secret_clean=31`; combined ARWB suite 57/57;
registry self-test 119 cases and strict 434-path classification; Markdown
self-test and strict zero violations; cross-document self-test and strict
PASS; lifecycle self-test 666 cases; Ruff check and format PASS. The default
repository-quality aggregate completed within its 600-second bound with exit 0
and `[PASS] repository quality gates passed`; that aggregate intentionally does
not invoke the full-history/`gitleaks` cutover proof. Production post-validate
always runs the real affected lane and has no self-test or required-validator
skip. Dedicated pure selector/runner tests execute all 7 manifest and 4 docs
validators without recursively invoking the production hook. Validator
subprocesses use a closed startup environment, absolute trusted tool resolution,
and exact repository-quality body marker proof; the production hook uses
`/usr/bin/python3 -I` and independently requires one PASS result line.
The archive index parser rejects missing, duplicate, extra, column-swapped, and
cross-row digest-swapped evidence, while the finite base admission proves the
exact 31 legacy-record conversions without restoring their retired authority.
ARWB-003 executes from parent `f8a54dd`; CI integration remains a Spec 039
follow-up and is not changed by this package.

After the initial independent verdicts, the required staged lifecycle command
exposed 33 failures: 31 legacy-to-current archive profile changes and the
retired/new template delete-create pair. A focused eight-case RED proved the
finite admission was absent. A later exact-identity review added three expected
RED failures showing that version/profile identifiers alone still admitted a
different registry. The remediation classifies base and proposed documents with
their own immutable registry Git blobs and admits only the exact `f8a54dd`
registry-v7-to-v8 staged/CI cutover manifest. It pins base registry blob
`0d9347c8ffa84ba313d0d70b42efb331d6e468c1` and proposed registry blob
`ed62f1792ba60e9be95d0d93b75d43654df3456f`. Exact GREEN evidence is 11/11
focused cases, staged lifecycle exit 0, and the 666-case lifecycle self-test;
partial, extra, wrong-base, wrong-registry-OID, missing-pair, registry drift,
unrelated-profile, snapshot, and explicit-ref variants remain denied. The
lifecycle adapter does not invoke the archive payload or secret-classification
path.

The initial independent review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`. After exact registry-identity remediation, repeat
requirements review again returned `REQUIREMENTS COMPLIANT` and final quality
re-review returned `QUALITY APPROVED`. Logical commit `787b28f` from parent
`f8a54dd` makes the ARWB-003 row Done. No ignored `_workspace` child was opened
or traversed.

The final staged pre-commit exposed two generic-tool false positives rather
than archive-content defects: entropy scanning treated canonical Git/SHA
integrity fields as secrets, and Markdownlint treated immutable recovered
payload headings as current document style. The remediation excludes only the
exact-length `source_commit`, `source_blob`, and `content_sha256` metadata lines
from detect-secrets, marks the five source-code Git object constants with the
tool's inline false-positive pragma, and excludes only archive record
subdirectories from Markdownlint while retaining lint on the archive index.
Gitleaks still scans the staged corpus, and `archive_cutover.py` still classifies
all 31 exact recovered payloads and proves their provenance and digest. Focused
detect-secrets and Markdownlint hooks pass with no payload mutation. Independent
boundary re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`.

The latest ARWB-003 requirements review returned `NOT COMPLIANT` for archive
creation without same-diff source removal, an unstructured index-membership
check, ARWB-003 CI workflow coupling, and a fast hook self-test that did not
execute all affected validators. Six remediation tests produced eight expected
RED outcomes (five failures and three errors). GREEN now binds archive creation
to its removed source in the same proposed diff, validates every field of the
31-row archive index with fail-closed cardinality and row identity, admits only
the exact finite 31-record legacy conversion at parent `f8a54dd`, leaves
`.github/workflows/ci.yml` unchanged, and executes every affected validator
in production. Recursive aggregate testing is isolated in the dedicated pure
runner entrypoint. Repeat requirements review returned
`REQUIREMENTS COMPLIANT`.

A repeat review then isolated a bounded-runner context defect, and the quality
review required complete removal rather than a stronger caller-provided token.
The final RED was six failures and six errors across production isolation,
aggregate boundary, external index tables, hostile Git state, and stable
failure diagnostics. GREEN removes all production self-test/skip variables,
keeps the unchanged CI workflow free of the manual cutover dependency, rejects
every table outside the canonical 31-row manifest, applies recovery-grade Git
isolation to inventory and finite-base calls, and converts invalid root,
registry, startup, timeout, and Git failures to fixed payload-free diagnostics.
Repeat review confirmed those boundaries before the later runner and provider
entry hardening findings were remediated.

The final quality follow-up produced five focused RED failures: a caller PATH
could shadow `bash`, `BASH_ENV` could suppress the real aggregate body, a zero
exit without the body marker or with duplicate markers passed, validator tools
remained relative, and the production hook lacked an isolated runner/result
gate. GREEN is 12/12 dedicated runner and hook-result tests. Validators now use
a closed startup environment and fixed absolute tool resolution; repository
quality requires exactly one body success marker. Production post-validate uses
`/usr/bin/python3 -I` in an empty environment and independently requires one
PASS result. Actual manifest and docs hook runs returned exact 7/7 and 4/4 PASS
status maps. Repeat review confirmed the child-runner boundary and then required
the provider entry hardening recorded next.

The provider-entry P1 follow-up produced fourteen RED failures across three
test methods: all three provider commands retained ambient shell startup state,
six valid docs/manifest executions returned forged empty success, three
malformed payloads returned zero, the hostile fake shell ran, and production
Python/project-root entries were not closed. GREEN is 15/15 combined
runner/result/provider tests. Claude, Codex, and Gemini PostToolUse commands now
use exact `/usr/bin/env -i` entries, fixed `/usr/bin:/bin`, provider-owned project
variables, and `/usr/bin/bash --noprofile --norc`; every direct production
Python entry uses `/usr/bin/python3 -I` in an explicit environment. Bounded
hostile integration preserves the 4/4 docs and 7/7 manifest selections for all
providers and rejects malformed JSON with exit 2. Actual-worktree Claude docs
and Codex manifest commands exited zero with one repository-quality marker;
the Gemini malformed command exited 2 with `HOOK-PAYLOAD-JSON`.
Final independent quality review returned `QUALITY APPROVED` with no blocking
finding.

Independent requirements review first returned `NOT COMPLIANT` for split
cutover commits, stale successor projections, and missing ARWB-003/005 RED
evidence. After remediation it returned `REQUIREMENTS COMPLIANT`. Independent
quality review then required fixture-only ARWB-001 authority, redacted
in-memory secret classification, and detailed criterion/package navigation;
after remediation it returned `QUALITY APPROVED`.

ARWB-004 began with `python3 -m unittest tests/test_workspace_boundary.py`
failing because `scripts/validate-workspace-boundary.py` did not exist. The
initial 10/10 GREEN required exactly one stage-zero `100644` README and rejected
extra or force-added children, conflicts, executable mode, symlink, gitlink,
nonregular, and malformed index records. The initial quality review returned
`QUALITY CHANGES REQUIRED`: running `check-ignore` in the actual worktree let an
ignored `_workspace/.gitignore` become unread scratch authority. The two-case
remediation RED returned one failure and one error. A wrong root policy passed
when the ignored child made the probe ignored, while a correct root policy
failed when that child unignored the probe and ignored the README.

The remediation makes four bounded, closed-environment, `shell=False` Git
queries against the actual repository: stage metadata for `_workspace` and the
root `.gitignore`, then size and exact blob retrieval for the validated full
SHA-1/SHA-256 root-ignore OID. The root ignore entry must be one stage-zero
`100644` regular file and its immutable blob is size-capped before retrieval.
Only that blob is written to an isolated temporary Git context. The two literal
`check-ignore --no-index` queries run there, so an actual ignored child can
neither hide a wrong root policy nor override a correct one. No worktree root
ignore file is opened. Diagnostics remain stable code/path pairs; Git startup,
timeout, malformed size, oversize, and blob-length mismatch fail closed.

The remediation GREEN is 16/16. `--self-test` passes isolated hostile-child Git
states, injected malformed/stage/ignore/blob cases, full SHA-1/SHA-256 IDs, and
actual-path traversal/open/stat sentinels that allow isolated evaluation;
`--root .` passes the production index/object and isolated ignore proof. The
aggregate still runs self-test then production validation and contains no
inline workspace check. No actual ignored `_workspace` child was listed,
walked, globbed, statted, opened, read, or hashed. The repository aggregate
exits zero with its exact PASS marker; Ruff check/format, Python compile, Bash
syntax, strict Markdown/link, and diff check also pass. Repeat requirements
review returned `REQUIREMENTS COMPLIANT` and repeat quality review returned
`QUALITY APPROVED`. Logical commit `87ff444` from parent `787b28f` makes the
ARWB-004 row Done.

ARWB-005 then reproduced the required partial staged lifecycle RED by changing
only Spec 036 from `active` to `done`. The validator exited `2` with the exact
`LIFECYCLE-BASE` diagnostic whose observed value is
`REGISTRY_PROGRAM_STATE`. The completed proposal changes exactly eight files:
the Spec/Plan/Task, their three indexes, the registry program-lineage state,
and the three existing migration-ledger rows. Spec 037 remains active and
dependency-ready with no Plan or Task created or linked.

After converting the six repeated lifecycle-table PRD links to the same
single-link/N/A pattern used by the completed Spec 035 closure, the complete
proposal passes staged lifecycle. Registry self-test passes 119 cases with 64
profiles, 30 templates, parity 11/11, and README fixtures 8/8; strict registry
passes 434 paths with `baseline=433`, `new=63`, and zero uncovered or ambiguous
paths. Lifecycle self-test passes all 666 cases. Strict Markdown reports zero
violations, strict cross-document validation passes, manual cutover reports
`records=31 historical_links=202 secret_clean=31`, and workspace self-test plus
production validation pass without reading ignored children.

The first full focused closure command correctly exposed that the ARWB-003
registry assertion compared its pinned proposed blob with the mutable current
worktree. Prerequisite remediation `4ccc616` instead binds that historical OID
to committed cutover `787b28f` through absolute `/usr/bin/git`, a closed
environment, replacement-object denial, bounded execution, commit-type and
path validation, plus stable fail-closed errors. Its focused RED/GREEN expands
the finite-cutover regression from 11 to 14 methods. Independent remediation
reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; these are
distinct from the later whole-tranche ARWB-005 closure reviews.

Final focused evidence passes 87/87: 14 finite archive-lifecycle cutover, 57
archive recovery/validation/cutover, and 16 workspace-boundary methods. The
direct repository aggregate passes with its exact final PASS marker. All-files
pre-commit runs with `SKIP=strict-repository-quality`: that one hook is
explicitly `SKIP` because the aggregate is proven separately and the hook's
isolated GitOps fixture still encounters the Spec 039-owned `os.mkfifo`
`Errno 95` boundary. Dockerfile lint is a separate no-file `SKIP`; every other
applicable hook, including JSON, Markdownlint, secrets, shell, workflow,
zizmor, and Kubernetes lint, passes. Independent whole-tranche reviews returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings. Closure
commit `855fa78` records the exact eight-file proposal. Post-commit
explicit-ref lifecycle validation for `4ccc616..855fa78` passed, strict registry
passed with 434 paths, snapshot mode returned the expected comparison-history
`DEFER`, and the worktree was clean. Package commits are `6b9b9cd`,
`f8a54dd`, `787b28f`, and `87ff444`; prerequisite remediation is `4ccc616`;
planning commit is `04a4d32`, rollback parent is `4ccc616`, and the bounded
pre-closure range is `04a4d32^..4ccc616`.

Repository-static evidence cannot establish remote object retention, GitHub
configuration, provider delivery, live Kubernetes/Vault/ESO/Argo CD state, or
the contents or safety of ignored `_workspace` scratch. Those lanes remain
`DEFER`; no ignored child was read to create this Task.

## Traceability

- **Spec**: [Archive Record and Workspace Boundary](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- **Plan**: [Archive Record and Workspace Boundary Implementation Plan](../plans/2026-07-17-archive-record-and-workspace-boundary.md)
- **Predecessor Task**: [Document Schema and Lifecycle Contract Task](./2026-07-16-document-schema-and-lifecycle-contract.md)
- **Decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ARWB-001](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-001-recovery-and-envelope-contract) | Done. | Initial, requirements-remediation, and quality-remediation RED evidence is recorded above; the private recovery/envelope suite passes 15/15 with `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. Logical commit `6b9b9cd`, parent `04a4d32`. |
| [ARWB-002](../../03.specs/036-archive-record-and-workspace-boundary/spec.md) | Done. | Missing-module/nine-failure RED and quality-remediation 17-failure/13-error RED are recorded above; focused 22/22 and combined 37/37 GREEN pass. Verdicts are `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; logical commit `f8a54dd`, parent `6b9b9cd`. |
| N/A — ARWB-003 shares the Plan linked in ARWB-001 | Done. | Named cutover RED and local GREEN are recorded: exact 31/31 payload, 202/202 source links, index-only current navigation, registry v8 archive-movement predicate, secret-clean 31/31, combined 57/57 archive tests, finite-admission regression 11/11, dedicated runner/hook/provider result 15/15, and deterministic validator gates. Final verdicts are `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; logical commit `787b28f`, parent `f8a54dd`. |
| N/A — ARWB-004 shares the Plan linked in ARWB-001 | Done. | Missing-validator RED, initial 10/10 GREEN, `QUALITY CHANGES REQUIRED`, two-case hostile-child RED (one failure, one error), and remediation 16/16 GREEN are recorded. Staged root-ignore object authority, isolated ignore evaluation, actual-path no-read sentinels, aggregate, Ruff/format/compile, Bash syntax, strict Markdown/link, and diff check pass. Final verdicts are `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; logical commit `87ff444`, parent `787b28f`. |
| N/A — ARWB-005 shares the Plan linked in ARWB-001 | Done. | Spec-only staged RED observed `REGISTRY_PROGRAM_STATE`; remediation `4ccc616` received `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; staged lifecycle, self-tests, strict document gates, manual cutover, workspace proof, focused 87/87, and direct aggregate pass. Fresh whole-tranche closure reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings. All-files pre-commit records strict aggregate as `SKIP` for the Spec 039 FIFO boundary while all other applicable hooks pass. Package commits `6b9b9cd`, `f8a54dd`, `787b28f`, and `87ff444`; planning commit `04a4d32`; rollback parent `4ccc616`; pre-closure range `04a4d32^..4ccc616`; closure commit `855fa78`; post-commit explicit-ref lifecycle `4ccc616..855fa78`, strict registry, snapshot-DEFER, and clean-tree checks passed. |

The lifecycle table renders the Plan and Spec relationship targets once to
preserve exact activation cardinality. The package-level anchors below provide
complete navigation without creating duplicate lifecycle evidence targets.

### Detailed Package Map

| Work package | Plan anchor |
| --- | --- |
| ARWB-001 | [Recovery and envelope capability](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-001-recovery-and-envelope-contract) |
| ARWB-002 | [Archive validators](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-002-archive-validators) |
| ARWB-003 | [Atomic corpus and authority cutover](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-003-atomic-corpus-and-authority-cutover) |
| ARWB-004 | [`_workspace` Git-metadata guard](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-004-_workspace-git-metadata-guard) |
| ARWB-005 | [Validation and lifecycle closure](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-005-validation-and-lifecycle-closure) |
