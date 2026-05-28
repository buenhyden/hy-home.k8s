# Postflight Checklist (March 2026)

Run this checklist before finalizing a response.

## 1. Policy Consistency

- [ ] JIT order is still consistent: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- [ ] No contradictory statements were introduced across rules/scopes/providers.
- [ ] Gateway files remain thin and non-duplicative.

## 2. Language and Audience

- [ ] All `docs/00.agent-governance/*` changes are English.
- [ ] Human-facing README files remain Korean.
- [ ] Final user response is Korean.

## 3. Reference Integrity

- [ ] All newly added links resolve correctly.
- [ ] Relative paths in templates resolve from template location.
- [ ] Optional placeholder paths are not emitted as broken Markdown links.
- [ ] README files keep `## Link Basis` and `## Related Documents`; no new `## Related References` heading remains.

## 4. Stage Compliance

- [ ] Any stage-specific guidance is consistent with `stage-authoring-matrix.md`.
- [ ] Inputs/outputs/templates/DoD are aligned for affected stages.

## 5. Verification Evidence

- [ ] Validation commands were executed (or limitations were stated).
- [ ] Relevant outputs were reviewed.
- [ ] Lifecycle hook guard ran or equivalent validation commands were executed; PreCompact advisory output is not treated as completion evidence.
- [ ] Unresolved risks are explicitly documented.
- [ ] No direct cluster mutation or plaintext Kubernetes secret was introduced.
- [ ] `.claude/*.local.md` files remain ignored and untracked; Hookify local rules keep required frontmatter when present.
- [ ] Staged and unstaged changes were reviewed for scope.
- [ ] Unavailable tools, skipped live validation, or CI-only checks were stated.
- [ ] `memory/progress.md` was updated with progress, reusable memory, evidence, and handoff for repo-changing work.
- [ ] Standalone memory files, if any, used `docs/99.templates/memory.template.md` and link back to a related `progress.md` entry.

## 6. Docs 3 Rules Compliance

- [ ] R1: Template read before document creation; `status: draft` set; k8s triggers respected (namespace→ARD, RBAC→ADR, prod→OPER first).
- [ ] R2: Folder-level changes **and content modifications to existing documents** include a README review and update (if stale) in the same PR, with `## Link Basis` and `## Related Documents` intact.
- [ ] R3: Every new authored document includes `## Related Documents` section.
- [ ] R4: Memory ledger coupling is satisfied for repo-changing work and standalone memory files.
- [ ] No HALT condition is unresolved before PR submission.
