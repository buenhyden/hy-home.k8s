# Cloud Example Reference Destinations

## Overview

This collection is the documentation handoff for dated AWS and Azure reference
snapshots. It separates reference evidence from executable example assets and
does not claim live-cloud, deployed-runtime, or provider-latest readiness.

## Scope

The dated provider indexes will live at `aws/README.md` and
`azure/README.md`. Executable assets remain under
[`examples/aws`](../../../examples/aws/) and
[`examples/azure`](../../../examples/azure/) until the approved migration
changes their canonical location. [Spec 030](../../03.specs/030-authored-document-migration/spec.md)
owns that relocation and authored-document consolidation.

## Item Index

| Destination | Purpose | Current executable owner |
| --- | --- | --- |
| `aws/README.md` | Dated AWS reference snapshot index; created in the snapshot-pack migration | [`examples/aws`](../../../examples/aws/) |
| `azure/README.md` | Dated Azure reference snapshot index; created in the snapshot-pack migration | [`examples/azure`](../../../examples/azure/) |

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
