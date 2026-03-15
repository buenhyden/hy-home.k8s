---
title: 'Runbook: Documentation Quality and Metadata Validation'
status: 'Active'
date: '2026-03-15'
owner: 'Platform Team'
tags:
  - runbook
  - document
layer: 'meta'
---
# Runbook: Documentation Quality and Metadata Validation

- **Status**: Active
- **Owner**: Platform Team
- **Last Reviewed**: 2026-03-15
- **layer**: meta

**Overview (KR):** 리포지토리의 모든 문서가 layer 메타데이터를 포함하고 올바른 경로에 위치하는지 검증하기 위한 절차입니다.

## Purpose

Ensure all documentation follows the March 2026 standards for metadata and pathing.

## Canonical References

- [AGENTS.md](file:///home/hy/projects/hy-home.k8s/AGENTS.md)
- [docs/adr/0005-documentation-normalization.md](file:///home/hy/projects/hy-home.k8s/docs/adr/0005-documentation-normalization.md)

## Review Checklist

- [ ] Every markdown file has `layer:` in the yaml frontmatter.
- [ ] Documentation is stored in the correct pluralized directory (e.g., `plans/` instead of `plan/`).
- [ ] Cross-references use relative markdown links.
- [ ] No placeholders remain in active documents.

## Investigation Procedure

1. **Verify Metadata**:

   ```bash
   grep -r "layer:" docs/
   ```

2. **Check for Outdated Paths**:

   ```bash
   ls -d docs/incident docs/plan docs/spec 2>/dev/null
   ```

## Verification Steps

- [ ] `pre-commit run --all-files` passes.
- [ ] No warnings from agent about missing context.
