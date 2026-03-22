---
layer: "meta"
---
# Development Workflows

Detailed workflows for building and maintaining the `hy-home.k8s` platform.

## 1. Spec-First Development

1. **Understand Intent**: Clarify requirements before design.
2. **Draft Spec**: Create a new specification in `docs/specs/` using the template.
3. **Approval**: Get user approval on the spec.
4. **Implementation Plan**: Draft an execution plan in `docs/plans/`.
5. **Execute**: Proceed with implementation once the plan is approved.

## 2. Validation & Deployment

- **Pre-commit**: Always run `pre-commit run --all-files` before committing.
- **GitOps Flow**: Commits to main trigger ArgoCD synchronization.
- **Manual kubectl**: Avoid manual `kubectl apply` for infrastructure. Use it only for debugging.

## 3. Rollback Procedure

Every deployment MUST have a corresponding rollback plan documented in `docs/runbooks/`.
