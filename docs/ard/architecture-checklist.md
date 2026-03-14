---
layer: "infra"
---
# Architecture & Tech Stack Checklist

When starting a project or writing an Architecture Reference Document (ARD), the following checklist MUST be addressed and agreed upon by the Human and Planner Agent:

| Category | Check Question | Priority | Notes / Decisions |
| --- | --- | --- | --- |
| **Architecture Style** | Is the architectural style decided (e.g., Monolithic, Modular Monolith, Microservices)? | **Mandatory** | |
| **Service Boundaries** | Are the boundaries and responsibilities of core services/modules expressed in diagrams/docs? | **Mandatory** | |
| **Domain Model** | Are core domain entities (e.g., User, Document) and relations defined (ER/UML)? | **Mandatory** | |
| **Tech Stack (Backend)** | Have the language, framework, and key libraries (e.g., web framework, ORM) been decided? | **Mandatory** | |
| **Tech Stack (Frontend)** | Have the framework (React/Vue/Next), state management, and build tools been decided? | **Mandatory** | |
| **Database** | Have the primary DB engine (e.g., MySQL, PostgreSQL, MongoDB) and schema strategy been decided? | **Mandatory** | |
| **Messaging / Async** | Is a message broker (e.g., Kafka, RabbitMQ) or async processing method defined? | *Optional* | |
| **Infrastructure** | Is the deployment target (Cloud/On-Prem, Kubernetes, Serverless) decided? | **Mandatory** | |
| **Non-Functional Req** | Are NFRs (Availability, Latency, Throughput) defined with quantitative metrics? | **Mandatory** | |
| **Scalability Strategy** | Are Scale-up/out, partitioning, or caching strategies drafted? | *Optional* | |
| **Arch. Principles** | Is there a documented list of architectural principles, including "what NOT to do"? | *Optional* | |
| **ADR Management** | Is there a process established to leave ADRs for key technical decisions? | *Optional* | Yes, use `docs/adr/`. |
| **Pillar Alignment** | Does the architecture align with the 6 Core Pillars (Security `2200`, Performance `2300`, Observability `2600`, Compliance `2400`, Documentation `2100`, Localization `2500`)? | **Mandatory** | See `.agent/rules/`. |
| **Agent Rule Compliance** | Does the tech stack selection comply with language/framework specific laws (e.g., `1200-Nextjs.md`) defined in `.agent/rules/`? | **Mandatory** | |

> **Process Enforcement**: The Planner Agent MUST explicitly answer all items of this checklist when creating an ARD, adhering to `.agent/rules/1910-architecture-documentation.md` and `.agent/rules/1901-architecture-rules.md`. The Reviewer Agent MUST verify that any code changes (e.g., in a PR) do not violate these agreed-upon decisions (such as unauthorized Tech Stack or DB changes) before merging.
