---
layer: "ops"
---
# Observability Manual (OBSERVABILITY.md)

_Target Location: `docs/manuals/observability-manual.md`_
_Description: Defines the project's strategy for monitoring, logging, and tracing to ensure system reliability and rapid debugging._

## Overview (KR)
이 문서는 시스템의 안정성과 디버깅 효율성을 높이기 위한 모니터링, 로깅, 그리고 트레이싱 전략을 정의합니다. RED 메트릭 수집 및 SLO 기반의 알람 정책을 포함합니다.

---

## 1. Metrics & SLIs (RED Pattern)

Essential metrics MUST be collected using Prometheus/OpenTelemetry:

- **Rate**: Number of requests per second.
- **Errors**: Number of failed requests (4xx/5xx).
- **Duration**: Latency distributions (p50, p95, p99).

## 2. Structured Logging

All services MUST follow the logging standards in `.agent/rules/2620-logging-std.md`:

- **Format**: JSON structured logging.
- **Mandatory Fields**: `timestamp`, `level`, `service_name`, `trace_id`, `message`.
- **Retention**: 7 days (Development), 30 days (Production).

## 3. Distributed Tracing

Critical inter-service pipelines MUST propagate headers for tracing:

- **Standard**: W3C Trace Context (`traceparent`).
- **Implementation**: OpenTelemetry SDKs integrated into all backend services.
- **Visualization**: Grafana Tempo / Jaeger.

## 4. Reliability (SLOs/SLIs)

| Indicator | Metric | Target (SLO) |
| :--- | :--- | :--- |
| **Availability** | Uptime % (Success/Total) | 99.9% |
| **Performance** | Latency p95 | < 500ms |
| **Quality** | Error Rate | < 0.1% |

## 5. Continuity & Disaster Recovery
- **Data Backups**: Automated snapshots for persistent volumes (MinIO, Qdrant).
- **Verification**: Monthly backup restoration tests.
- **Targets**: RTO < 4h, RPO < 1h.
