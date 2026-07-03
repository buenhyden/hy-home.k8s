---
title: 'Reference: Workspace Document Governance Hardening Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-03
---

# Reference: Workspace Document Governance Hardening Audit

## Overview

This audit records the Task 1 repo-static baseline for workspace document
governance hardening. It preserves the current inventory, summarizes durable
drift classes, and routes remediation to later tasks without changing the
active contracts during the audit pass.

## Purpose

Provide a durable, dated lookup for the baseline audit findings that should
inform Task 2 through Task 5 without making those remediation changes in
Task 1.

## Reference Type

- audit

## Authority Boundary

This document owns observed audit evidence and remediation routing from the
2026-07-03 baseline scans. Active execution policy remains in Stage 00
governance, template support contracts, provider runtime overlays, and
repository validators. Repo-static validation does not prove live k3d, Argo CD,
Vault, ESO, Kubernetes, cloud, provider runtime, or external-service readiness.

## Scope

- Captures repo-static inventory, frontmatter and README scan classes,
  provider surface traceability, and CI/QA documentation evidence.
- Excludes live runtime validation, secret inspection, provider account
  mutation, Kubernetes mutation, and remediation work owned by later tasks.

## Definitions / Facts

- Tracked Markdown/YAML/YML/GraphQL/proto files at baseline: 480.
- Tracked Markdown files at baseline: 358.
- README files remained frontmatter-free in the focused README metadata scan.
- The active docs top-level taxonomy contained only the canonical stage
  folders; no `docs/superpowers` tree was present.
- The stale provider-local hook path literal is intentionally not repeated in
  this active reference because the repository quality gate rejects that
  literal in active authored documents.

## Findings

| Finding ID | Surface | Evidence | Decision | Routed Task |
| --- | --- | --- | --- | --- |
| WDGH-AUD-001 | README section contract | `docs/00.agent-governance/README.md:99` uses `## Related Folders`; the deprecated-heading scan returned only this active match. | Durable README heading drift. Normalize during workspace document application, then decide whether the validator should enforce this heading family. | T-004, T-005 |
| WDGH-AUD-002 | README frontmatter scan | README-only metadata scan returned `examples/aws/docs/README.md:72`, a body `---` after `## Related Documents`; no README frontmatter was found. | Not YAML frontmatter, but it is durable README structure evidence for the workspace application pass. | T-004 |
| WDGH-AUD-003 | CI/QA documentation | `tests/README.md:58` still names the legacy Claude provider-local hook directory in the shell syntax command, while `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md:92` and `scripts/README.md` point to `docs/00.agent-governance/hooks`. | Active CI/QA documentation drift. Align the current shell syntax surface and add deterministic coverage if practical. | T-004, T-005 |
| WDGH-AUD-004 | Provider and CI owner traceability | Root shims route to Stage 00 provider notes and runtime baselines; `.github/ABOUT.md` and `.github/workflows/ci.yml` own the CI job contract. | No Task 1 fix. Use these owners as the traceability baseline for provider and CI/QA hardening. | T-003, T-005 |

## Implementation Checklist

| Item | Owner Surface | Action | Status |
| --- | --- | --- | --- |
| Record baseline command evidence and tracked inventory. | Stage 04 task record | Capture required command outputs and summarized scan classes. | Done |
| Register durable audit report. | `docs/90.references/audits/README.md` | Add the dated audit report to the audit index. | Done |
| Normalize README heading drift. | Workspace README surfaces | Replace or merge active deprecated related-document headings during the document application pass. | Pending T-004 |
| Review README body delimiter evidence. | Workspace README surfaces | Decide whether the post-`Related Documents` horizontal rule should be removed or preserved as intentional content. | Pending T-004 |
| Align CI/QA hook syntax documentation. | CI/QA documentation and validator | Update active shell syntax guidance and evaluate deterministic validator coverage. | Pending T-004/T-005 |
| Verify provider wording boundaries. | Provider entrypoints and runtime overlays | Ensure provider claims do not overstate hook or permission parity. | Pending T-003 |

## Review and Freshness

- Review date: 2026-07-03.
- Refresh trigger: rerun when template routing, provider entrypoints, CI/QA
  workflows, README contracts, or validator contracts change.

## Sources

- `git status --short --branch`
- `git diff --check`
- `bash scripts/validate-repo-quality-gates.sh .`
- `git ls-files '*.md' '*.yaml' '*.yml' '*.graphql' '*.proto' | wc -l`
- `git ls-files '*.md' | wc -l`
- `find docs/99.templates/templates -maxdepth 5 -type f | sort`
- `find docs/99.templates/support -maxdepth 2 -type f | sort`
- `find docs/00.agent-governance -maxdepth 3 -type f | sort`
- Frontmatter, README heading, provider, and CI/QA scans recorded in the
  linked Task evidence.

## Related Documents

- [Parent Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Parent Plan](../../04.execution/plans/2026-07-03-workspace-document-governance-hardening.md)
- [Task Evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md)
- [Audit Index](./README.md)
