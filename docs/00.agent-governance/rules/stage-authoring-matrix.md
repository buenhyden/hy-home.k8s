# Stage Authoring Matrix

Canonical authoring matrix for the current docs taxonomy.

All authored stage documents must use the matching template from
`docs/99.templates/README.md` before writing. New authored documents start with
`status: draft`, keep the required template headings, and include
`## Related Documents`. README entrypoints use `readme.template.md`.

Human-facing README and overview prose should prefer Korean. Agent governance,
provider adapters, hook contracts, prompt/tool contracts, technical specs,
execution plans, task evidence, and explicit AI-agent-facing sections such as
`AI Agent Requirements` should prefer English. `docs/03.specs/**/spec.md`,
`docs/04.execution/plans/*.md`, and `docs/04.execution/tasks/*.md` are
English-first execution artifacts. When a stage document mixes human and agent
audiences, keep the reader-facing context in Korean and keep the AI-agent
execution requirements in English.

| Taxonomy Path | Purpose | Authoring Timing | Persona (Primary) | Input Documents | Output Documents | Template | Completion Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `00.agent-governance` | Agent governance and execution control | Before work starts and when governance changes | Governance Steward | Repository structure, policy context | Rules/scopes/providers/memory entries | `memory.template.md`, `progress.template.md` | JIT loading, language boundary, progress ledger, and checklist consistency are enforced |
| `01.requirements` | Product intent and requirements | Before feature implementation | Product Manager | Problem statement, business goals | PRD | `prd.template.md` | Acceptance criteria, scope, and success metrics are testable |
| `02.architecture/requirements` | Architecture requirements and reference design | After PRD baseline | System Architect | PRD | ARD | `ard.template.md` | Boundaries, quality attributes, and data flow are explicit |
| `02.architecture/decisions` | Architecture decision records | When major decisions are made | System Architect | ARD, alternatives | ADR | `adr.template.md` | Decision rationale, alternatives, and consequences are traceable |
| `03.specs` | Detailed technical specification | Before implementation | Backend/Frontend/Security Engineer | PRD, ARD, ADR | Spec/API/Agent/Data/Test design docs | `spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `tests.template.md` | Contracts and verification-ready design are complete |
| `04.execution/plans` | Execution planning | Immediately after spec baseline | Product/QA/Tech Lead | PRD, Spec, ADR | Plan | `plan.template.md` | Phases, risks, gates, and rollback are defined |
| `04.execution/tasks` | Task execution tracking | During implementation and validation | Engineer/QA Engineer | Plan, Spec | Task records with evidence | `task.template.md` | Status, validation, and evidence are continuously updated |
| `05.operations/guides` | User and operator guides | After feature stabilization | Technical Writer | Spec, operations context | Guides | `guide.template.md` | Target audience can follow and reproduce procedures |
| `05.operations/policies` | Operational policy | Before release and when policy changes | Operations Engineer | Spec, security/compliance requirements | Operation policy docs | `policy.template.md` | Control, retention, and promotion criteria are explicit |
| `05.operations/runbooks` | Executable run procedures | When operations tasks are standardized | Operations Engineer | Operation policy | Runbooks | `runbook.template.md` | Steps are executable with validation and recovery paths |
| `05.operations/incidents` | Incident fact records and post-incident learning | During incident handling and after incident closure | Operations/Security Engineer | Runtime evidence, runbooks | Incident folders with `INC-###-<title>.md` and optional `postmortem.md` | `incident.template.md`, `postmortem.template.md` | Timeline, impact, mitigations, RCA, and prevention actions are linked back to the system |
| `90.references` | Durable reference material | When knowledge should be reused across features or operations | Technical Writer/Governance Steward | Stable facts, inventories, learning material | Reference documents | `reference.template.md` | Reference material is factual, slow-moving, linked from relevant stages, and keeps authority/source/freshness fields English-first |
| `98.archive` | Metadata-only old document Tombstones | When an old active-stage document conflicts with current implementation or is deprecated-only/superseded-only | Governance Steward | Current replacement docs, implementation evidence | Tombstone documents and archive index rows | `archive-tombstone.template.md` | Original path is mirrored, old body is removed, active docs link only to the archive index |
| `99.templates` | Reusable document templates | Before authoring or restructuring docs | Technical Writer/Governance Steward | Taxonomy requirements | Templates | n/a | Templates match canonical paths and stay referenced by README files |
