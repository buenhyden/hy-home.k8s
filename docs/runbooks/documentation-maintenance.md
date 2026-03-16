# Documentation Maintenance Runbook

- **Status**: Active
- **layer:** meta

# Documentation Maintenance Runbook

> **Status**: Active
> **Owner**: buenhyden
> **layer:** meta

**Overview (KR):** 프로젝트 문서의 일관성을 유지하고, March 2026 표준을 지속적으로 준수하기 위한 운영 절차서입니다.

## 1. Metadata Compliance Check

All new markdown files MUST include `layer:` metadata.

```bash
# Verify missing layers
grep -L "layer:" docs/**/*.md root/*.md
```

## 2. Plural Path Enforcement

Ensure execution documents reside in the correct plural directories.

- **Check plans**: `ls docs/plans/` (MUST NOT be `docs/plan/`)
- **Check specs**: `ls docs/specs/` (MUST NOT be `docs/spec/`)

## 3. Agent Rule Updates

When a new architectural standard is established:

1. Create an ADR in `docs/adr/`.
2. Update `docs/agentic/agent-instructions.md` if mapping changes.
3. Update model-specific rules in `docs/agentic/rules/`.

## 4. Periodic Audits

Run the following command quarterly to ensure link integrity:

```bash
# Using a link checker or grep for relative links
grep -r "\[.*\](.*\.md)" docs/
```

## Related Documents

- [docs/ard/documentation-system-ard.md](../ard/documentation-system-ard.md)
- [docs/prd/documentation-system-prd.md](../prd/documentation-system-prd.md)
