# Stage Authoring Matrix (00-10, 90, 99)

Canonical authoring matrix for the docs lifecycle stages.

| Stage | Purpose | Authoring Timing | Persona (Primary) | Input Documents | Output Documents | Template | Completion Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | Agent governance and execution control | Before work starts and when governance changes | Governance Steward | Repository structure, policy context | Rules/scopes/providers/memory entries | `memory.template.md` | JIT loading, language boundary, and checklist consistency are enforced |
| 01 | Product intent and requirements | Before feature implementation | Product Manager | Problem statement, business goals | PRD | `prd.template.md` | Acceptance criteria, scope, and success metrics are testable |
| 02 | Architecture reference design | After PRD baseline | System Architect | PRD | ARD | `ard.template.md` | Boundaries, quality attributes, and data flow are explicit |
| 03 | Architecture decision records | When major decisions are made | System Architect | ARD, alternatives | ADR | `adr.template.md` | Decision rationale, alternatives, and consequences are traceable |
| 04 | Detailed technical specification | Before implementation | Backend/Frontend/Security Engineer | PRD, ARD, ADR | Spec/API/Agent/Data/Test design docs | `spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `tests.template.md` | Contracts and verification-ready design are complete |
| 05 | Execution planning | Immediately after spec baseline | Product/QA/Tech Lead | PRD, Spec, ADR | Plan | `plan.template.md` | Phases, risks, gates, and rollback are defined |
| 06 | Task execution tracking | During implementation and validation | Engineer/QA Engineer | Plan, Spec | Task records with evidence | `task.template.md` | Status, validation, and evidence are continuously updated |
| 07 | User and operator guides | After feature stabilization | Technical Writer | Spec, Operations context | Guides | `guide.template.md` | Target audience can follow and reproduce procedures |
| 08 | Operational policy | Before release and when policy changes | Operations Engineer | Spec, security/compliance requirements | Operation policy docs | `operation.template.md` | Control, retention, and promotion criteria are explicit |
| 09 | Executable run procedures | When operations tasks are standardized | Operations Engineer | Operation policy | Runbooks | `runbook.template.md` | Steps are executable with validation and recovery paths |
| 10 | Incident fact records and post-incident learning | During incident handling and after incident closure | Operations/Security Engineer | Runtime evidence, runbooks | Incident records and `postmortems/` entries | `incident.template.md`, `postmortem.template.md` | Timeline, impact, mitigations, RCA, and prevention actions are linked back to the system |
| 90 | Durable reference material | When knowledge should be reused across features or operations | Technical Writer/Governance Steward | Stable facts, inventories, learning material | Reference documents | `reference.template.md` | Reference material is factual, slow-moving, and linked from relevant stages |
| 99 | Reusable document templates | Before authoring or restructuring docs | Technical Writer/Governance Steward | Stage requirements | Templates | n/a | Templates match canonical stage paths and stay referenced by README files |
