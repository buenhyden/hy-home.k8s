# Runbook: Documentation Management

- **Status**: Active
- **layer:** meta

**Overview (KR):** 리포지토리의 문서 분류 체계(Taxonomy)를 유지관리하고 일원화된 구조를 점검하기 위한 지침입니다.

## 1. Responsibility

The **Planner Agent** and **DevOps Agent** are responsible for maintaining the documentation taxonomy.

## Canonical References

- [docs/ard/documentation-system-ard.md](../ard/documentation-system-ard.md)
- [docs/specs/2026-03-16-documentation-system-spec.md](../specs/2026-03-16-documentation-system-spec.md)

## 2. Integrity Checks

Run the following commands to verify system health:

### Check Metadata Coverage

```bash
find docs/ -name "*.md" -print0 | xargs -0 grep -L "layer:"
```

### Check Taxonomy Alignment

```bash
ls docs/
# Expected: adr, ard, agentic, operations, plans, prd, runbooks, specs
```

## 3. Scaling the Taxonomy

When adding a new documentation type:

1. Create the directory in `docs/`.
2. Add a new `LOAD RULE` and scope file in `docs/agentic/scopes/`.
3. Update the trigger map in `AGENTS.md`.
4. Update the root `index.md` index.
