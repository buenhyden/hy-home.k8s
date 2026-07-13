# Cloud Example Reference Destinations

## Overview

This collection is the documentation handoff for dated AWS and Azure reference
snapshots. It separates reference evidence from executable example assets and
does not claim live-cloud, deployed-runtime, or provider-latest readiness.

## Scope

The dated provider indexes and snapshots now exist under `aws/` and `azure/`.
The exact 59 example-local documentation sources are retired. Executable assets
remain under [`examples/aws`](../../../examples/aws/) and
[`examples/azure`](../../../examples/azure/) as implementation references; the
dated provider snapshots are their durable documentation destinations.
[Spec 030](../../03.specs/030-authored-document-migration/spec.md) completed that
relocation and authored-document consolidation.

## Item Index

| Destination | Purpose | Current executable owner |
| --- | --- | --- |
| [AWS dated snapshot](aws/2026-07-12-aws-example-snapshot.md) | Consolidated AWS reference and source-coverage index | [`examples/aws`](../../../examples/aws/) |
| [Azure dated snapshot](azure/2026-07-12-azure-example-snapshot.md) | Consolidated Azure reference and source-coverage index | [`examples/azure`](../../../examples/azure/) |

## Add and Find

Use the provider child index when looking for dated reference reports. Use the
corresponding `examples/<provider>/` tree for executable manifests, Terraform,
and validation assets. Add or relocate durable material only through the Spec
030 plan so links, provenance, and successor records move together.

## Related Documents

- [References stage](../README.md)
- [Authored Document Migration Spec](../../03.specs/030-authored-document-migration/spec.md)
- [AWS executable examples](../../../examples/aws/)
- [Azure executable examples](../../../examples/azure/)
