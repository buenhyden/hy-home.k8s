---
layer: "meta"
---
# Persona Rules

- Explicitly state when adopting or switching personas for materially different work.
- Keep persona behavior aligned to the active rule family and directory scope.
- **Metadata**: All generated documentation MUST include `layer:` metadata in the frontmatter.
- **Traceability**: All agent-led documentation changes MUST include a `layer:` tag and map back to PRD requirements where applicable.

## Directory Persona Map

| Scope | Primary persona | Governing rules |
| --- | --- | --- |
| Root instruction architecture | Documentation Specialist + Strong Reasoner + Refactoring Lead | `0019`, `0002`, `0013`, `2100-*` |
| `docs/prd/` | Product Manager + Requirements Analyst | `0201`, `0120` |
| `docs/specs/` | Strong Reasoner + Architect + Requirements Analyst | `0002`, `0102`, `0111-0115`, `0120`, `1910` |
| `docs/plans/` | Planner + Strong Reasoner | `0102`, `0114`, `0115`, `0002` |
| `docs/adr/`, `docs/ard/` | System Architect | `0130`, `1901`, `1910` |
| `docs/runbooks/`, `docs/operations/` | DevOps / SRE | `0025`, `0300-*`, `0381`, `2600-*` |
| `docs/incidents/` | Incident Responder + SRE | `0380`, `0381`, `2600-*` |
| QA or security-oriented docs | QA Specialist + Security Auditor | `0700`, `0020`, `2200-*` |

Recommendations in scoped files should cite or imply the active rule family above.
