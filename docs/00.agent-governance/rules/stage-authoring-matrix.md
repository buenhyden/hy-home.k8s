# Stage Authoring Matrix

Canonical authoring matrix for the current docs taxonomy.

| Taxonomy Path | Purpose | Authoring Timing | Persona (Primary) | Input Documents | Output Documents | Template | Completion Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `00.agent-governance` | Agent governance and execution control | Before work starts and when governance changes | Governance Steward | Repository structure, policy context | Rules/scopes/providers/memory entries | `memory.template.md` | JIT loading, language boundary, and checklist consistency are enforced |
| `01.requirements` | Product intent and requirements | Before feature implementation | Product Manager | Problem statement, business goals | PRD | `prd.template.md` | Acceptance criteria, scope, and success metrics are testable |
| `02.architecture/requirements` | Architecture requirements and reference design | After PRD baseline | System Architect | PRD | ARD | `ard.template.md` | Boundaries, quality attributes, and data flow are explicit |
| `02.architecture/decisions` | Architecture decision records | When major decisions are made | System Architect | ARD, alternatives | ADR | `adr.template.md` | Decision rationale, alternatives, and consequences are traceable |
| `03.specs` | Detailed technical specification | Before implementation | Backend/Frontend/Security Engineer | PRD, ARD, ADR | Spec/API/Agent/Data/Test design docs | `spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `tests.template.md` | Contracts and verification-ready design are complete |
| `04.execution/plans` | Execution planning | Immediately after spec baseline | Product/QA/Tech Lead | PRD, Spec, ADR | Plan | `plan.template.md` | Phases, risks, gates, and rollback are defined |
| `04.execution/tasks` | Task execution tracking | During implementation and validation | Engineer/QA Engineer | Plan, Spec | Task records with evidence | `task.template.md` | Status, validation, and evidence are continuously updated |
| `05.operations/guides` | User and operator guides | After feature stabilization | Technical Writer | Spec, operations context | Guides | `guide.template.md` | Target audience can follow and reproduce procedures |
| `05.operations/policies` | Operational policy | Before release and when policy changes | Operations Engineer | Spec, security/compliance requirements | Operation policy docs | `operation.template.md` | Control, retention, and promotion criteria are explicit |
| `05.operations/runbooks` | Executable run procedures | When operations tasks are standardized | Operations Engineer | Operation policy | Runbooks | `runbook.template.md` | Steps are executable with validation and recovery paths |
| `05.operations/incidents` | Incident fact records and post-incident learning | During incident handling and after incident closure | Operations/Security Engineer | Runtime evidence, runbooks | Incident records and `postmortems/` entries | `incident.template.md`, `postmortem.template.md` | Timeline, impact, mitigations, RCA, and prevention actions are linked back to the system |
| `90.references` | Durable reference material | When knowledge should be reused across features or operations | Technical Writer/Governance Steward | Stable facts, inventories, learning material | Reference documents | `reference.template.md` | Reference material is factual, slow-moving, and linked from relevant stages |
| `99.templates` | Reusable document templates | Before authoring or restructuring docs | Technical Writer/Governance Steward | Taxonomy requirements | Templates | n/a | Templates match canonical paths and stay referenced by README files |
