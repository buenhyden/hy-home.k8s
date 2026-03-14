---
layer: "meta"
---
# Runbook: Documentation Management

## 1. Responsibility

The **Planner Agent** and **DevOps Agent** are responsible for maintaining the documentation taxonomy.

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
4. Update the root `README.md` index.
