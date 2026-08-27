---
title: "MIG-0004: Document Authority Convergence"
type: "content/archive-migration"
status: "sealed"
owner: "platform"
updated: "2026-08-21"
artifact_id: "MIG-0004"
migration_id: "MIG-0004"
---

# MIG-0004: Document Authority Convergence

## Overview

This atomic ledger seals the WP-004B Requirement Package, prefix-free
Architecture Description, and Spec-package Task authority cutover at source
commit `211e167f9ef0268c937303faa82d7ed297b33e38`. Its approved finite WP-004C
completion additionally pins the terminal Stage99 authority/form cutover at
source commit `7a770c3c0eabaeda554c4030fc08fb17de164fe5`: 33 deleted or moved
support, contract, and form objects, plus the one final Spec0054 `tasks.md`
replacement. It does not add per-Task migration rows.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "434b03a8580a9ee84c89a017555bda46c94c0f1a",
    "content_sha256": "80bdd30592b9c1a0e0efbdf74e89dc025e8308c3d6e1985d5ef9c224e94a03cc",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0002-argo-notifications-slack.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0002-argo-notifications-slack.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "4bdcecfa00a2c27da5e0cf071705b54d55c2ec5b",
    "content_sha256": "fa8dc197e563b9439acefdad2a6073cde51193e485dd289a280c0a208124a192",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0003-workspace-agent-governance-platform.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0003-workspace-agent-governance-platform.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "e5b028e6569a72412b02d28baccead33876cfc36",
    "content_sha256": "f1b0d04f3aa7730298ecd2cd0de158904af7753fd663394b2cfc6e2c2845bb21",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0004-current-local-gitops-platform.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0004-current-local-gitops-platform.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "ab46bc553d8933ff2d76f9a13c971f9a503ecb14",
    "content_sha256": "746bb0ea6761da3804949ec77f3775f9d52e0ed52f2c47187cf64762da3fa702",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0005-workspace-document-assurance-modernization.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0005-workspace-document-assurance-modernization.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "643bf3634aa6cade75980b5d7abee02c98ee1813",
    "content_sha256": "c687ed0330fd3f28606b529834a45823100665cb738507bd288e58faa8eb2e8b",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "5ca81b4ab928f70b0371cec294508b15b708e28e",
    "content_sha256": "6083185b8b4850254e715b72818ac70f89cc25021f415631fea7e6ea40b82823",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0007-repository-delivery-and-platform-assurance.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0007-repository-delivery-and-platform-assurance.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "334ffd406573e6a1e9bb55dd94982df6ca6a999c",
    "content_sha256": "97f2cd8c74f44e588b4f944d6c1e02465bca912ae9b0107a80665e9099d6e2bf",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "7594f93d0f563be2fb39a414248b699baf4f835e",
    "content_sha256": "f68376a25d2af2cc5d0db8bf8233880c6811a66ff2a12cbee94c12d88622f63c",
    "reason": "Replace same-path PRD authority with the unified Requirement Package contract and package-scoped member identities."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0004-argo-rollouts-progressive-delivery.md",
    "stable_path": "docs/02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md",
    "artifact_id": "AD-0004",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "2eb863de8e2cb77d70e2d767a97050395ea4984c",
    "content_sha256": "66a3073e4c0e40bda67044cc1a260dccda8f6695abe48fbf5fc5e774c2ce7cf0",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0005-argo-notifications-slack.md",
    "stable_path": "docs/02.architecture/descriptions/0005-argo-notifications-slack.md",
    "artifact_id": "AD-0005",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "2001eb2049d686749b14e819a402a9866c03683d",
    "content_sha256": "dd662c20cf00cbb853c8e7348f4872b3ec0d0575616e7d5fcd7b1d26f2f52286",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0006-workspace-agent-governance-platform.md",
    "stable_path": "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
    "artifact_id": "AD-0006",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "6d82959d2b69a0840e7c7331307580139ed3419c",
    "content_sha256": "1fa030d23c570a16e9ff99d2bcea24967725ecab0f3041c1e35cfc0632d68aad",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0007-current-local-gitops-platform.md",
    "stable_path": "docs/02.architecture/descriptions/0007-current-local-gitops-platform.md",
    "artifact_id": "AD-0007",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "cf06ec74fb083954cf23e7b38bca3ba86e6d4ede",
    "content_sha256": "07c5f76d17987f16e7cb2ad5b4c9d4f28b1268bb658892958afdf41180628949",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0008-workspace-document-assurance-operating-model.md",
    "stable_path": "docs/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md",
    "artifact_id": "AD-0008",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "5589f994e62e4a955b3f6e92632027c30518d6e9",
    "content_sha256": "eb4f4d37ba5ae9661003c769f5281eb9ae2888d566ceacab93a03040e8c6faaf",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0009-document-lifecycle-evidence-operating-model.md",
    "stable_path": "docs/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md",
    "artifact_id": "AD-0009",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "b903a51e265708ce73c9bb32897c98fe2c270989",
    "content_sha256": "f18360d8adac90b90cc15e4e2383a23c579aa113c4ccb4c2d99fc4001b4dd703",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md",
    "stable_path": "docs/02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md",
    "artifact_id": "AD-0010",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "7bfda6c52f475f6f1d742b472b0627857e9b6fb1",
    "content_sha256": "b1f1dafeb09aa0b519073c0eb3377beb031683dbaf52855fcdf972d0320612a3",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md",
    "stable_path": "docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md",
    "artifact_id": "AD-0011",
    "action": "moved",
    "replacement": null,
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "3b3e5fbdd90f2352d269be6f5ce1f45c3dc4042e",
    "content_sha256": "344e9286c8ee7440b6442677289b4c883d51947c36a6b663143139f93deff3c6",
    "reason": "Remove the redundant filename type prefix while preserving the stable AD identity."
  },
  {
    "legacy_path": "docs/03.specs/0004-argo-rollouts-progressive-delivery/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0004-argo-rollouts-progressive-delivery/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "2c4ed7e802c1d36c8aac4a96f374bb18f45a3fd4",
    "content_sha256": "c3814c96cf33ff9f61bf5b8ee95c4095001cf2de69147fcd3b4961558fbf282f",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0005-argo-notifications-slack/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0005-argo-notifications-slack/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "c6ecf95b4c9f49765d3df4681e840da3715a000b",
    "content_sha256": "876649428aef9a7eadc1fbfca09d730a52a659ff8bd1c8e84aa71ba7fee80edb",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0009-workspace-harness-research-pack/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "1bc22750347e2f4a5a64f1ec07ccc2678b92506e",
    "content_sha256": "bb4ce8c3a5b424108f36e2ca3826f4f784bbdd8ec80e9518c9976a36da4ad46c",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "64ff7ead29add71a28d202a635ac863faafe502f",
    "content_sha256": "be792f6a8c08a1ad18b07c1b6bded74c40bafc45ef3e337b1c58e0b6095ea68f",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0011-template-contract-governance-migration/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "7676d6f3fa76d9ff211a95498acc3a143f0682c6",
    "content_sha256": "5428d291666817b5e7f8f048d7f4982ba8e206f6d4695c5652eac7d6c9ea30ba",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0012-template-governance-audit-enhancement/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "d36582cb46e3393f73685b93e8882f8bd46ba6ab",
    "content_sha256": "853e742abda8a28651a4e92841b852704d7032fcca0a467c12d327559ad7c130",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0013-workspace-document-governance-hardening/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "0b5da61efd463647d3b0e638e5e8fcde48d8be09",
    "content_sha256": "b0a3971acedf971077b07c91e68d51ed809189143fd66facf84a21720dd6427d",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0014-workspace-document-contract-normalization/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "695daa7f8cbd30bd0fe099efe68ce4534f4ee9c5",
    "content_sha256": "06b83a43db15e6dc927291acb53efd52dead9fa3bd859d27bcf499dd999434d3",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0015-agent-governance-contract-normalization/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "9270be2a1d13d9685c5617fc2de5c064723e94d4",
    "content_sha256": "7c915f1ad35c5741b839e4d78c90f71f70c405b414f65a0b18e943220b005967",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0016-active-control-surface-governance-hardening/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "8970dc3c614084e2109cf9bcc308d296fd73538a",
    "content_sha256": "f49ec016ba95850d317cfb3db23a33eee9fbd99b28e0294acb8bbde0b0ed93f7",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0017-workspace-engineering-research-pack/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "888806ef3435dc089e35a20274f4073537ec80ca",
    "content_sha256": "3069c450be9dfca9e1f8964ecaca7e580253ae6b4025e85a1b8b886d95af0122",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "5668b1364b53042481b647092427588057df79c1",
    "content_sha256": "0a4f7c06f2fc5c939217c5c7161828d0536a3eea5b8fdfa9c0486f579a39b064",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0019-template-path-numbering-contract/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "6d6400bdce5c6637ae0f381985c3773d266a24c3",
    "content_sha256": "c51c6807300cb5580e2151cc1e98624c63964d587048946e81452fa937fc2194",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0020-workspace-contract-governance-normalization/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "89543eef0400f056d6ee048108aad5c4fd458a66",
    "content_sha256": "bb90582c72bbb694c10d8a8e6ca6bcb59e7ee61dc2c6db2e5b818df5fe10ab94",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0021-sdlc-lifecycle-contract/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "782be7dce2d20d080ec48d5248d527109406bd31",
    "content_sha256": "8e662945e18ddb7ba374aacf6bd1b223760a481047cf518d17436a3ce400154b",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0022-control-cloud-doc-normalization/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "521e6963457a00be55af477d344481e64d3d6f54",
    "content_sha256": "a97d5f3ed82579fed8c566089f28512c3ee7d6b4c1986375348c1ab37644b82c",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "86a8b49f9a2dbc1bde477e8f5977390b19ed907d",
    "content_sha256": "c0a65721788147d7d158d43079d3c145fb3c7cadfc934f0229d4178292f1f3b9",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/agent-design.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0024-observability-and-network-review-agents/spec.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "0fa26839457f1abae7c81592295df08d1aa3ddca",
    "content_sha256": "6ead8efefae63fc04fefb6238a09dbd31217cad592aa6bb6bc49a55fe9ca4be1",
    "reason": "Fold valid change-local role boundaries into the owning Spec/Plan without retaining a permanent agent-design family."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0024-observability-and-network-review-agents/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "f0d1d4301438d01c35ffc464cfa851a7011884e9",
    "content_sha256": "f76bb7e41406239a9ae606ab6e4aee7fd3ea0499f84274f4b006236595b453fa",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0025-governance-owner-and-roster-currentness/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "9fced7ada812b646f0f525cb23cfcbf5b8c2be66",
    "content_sha256": "3a81de066ac1cfacf54d3d17c905fec0ecf76247c0b7099437864da4ff3d7023",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0026-document-contract-registry/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "e9643b3161de9a3253cfd0015c931e800c27e386",
    "content_sha256": "392eef48c479a42ca3d0b0e56ac833ed7d796914531ed895ef1ed744fc7da6e7",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0027-template-contract-consolidation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "a83986fd1fb39cfe9a001d259ca9d5287d7e9da5",
    "content_sha256": "38a53c3797eb40268ab45fb0f0a6800e40b71345e47bbed499aa9590104f440e",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0028-readme-workspace-profiles/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "2e148f883a517629cc9b6d80a756577862f941bf",
    "content_sha256": "589549286b96ed511a9bd23048d40aa39b6874a8eeb2623c68ac3ce34483e590",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0029-semantic-document-validation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "e43708fc25cdc4c0f0f2881785ceb02b6a3d30c7",
    "content_sha256": "c872727fbbe540c535404ef45084f2da5102513512d1e7a47b8e547454b0380b",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0030-authored-document-migration/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "628cbdd36cda458aaa2738e05929b7138d5d5483",
    "content_sha256": "bb22554efe54420cd7efd746f2d2ed977fb1e8584cb1ce62eb3341fa44ae238d",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0037-active-corpus-and-execution-retention/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "b06228d35372dda0d7e5bf4045579e15a421d771",
    "content_sha256": "1ebfb2a45bedf50159c6e81695f71caeb3d5a9b44e60206e1d4f5517250dbdac",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0038-reference-information-architecture/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "142966c4c988d0e1521d398c942abc09720b6695",
    "content_sha256": "4ad65f140bf484b5db1643316e61911d2b61c28c17429957dd34ce7878deb6dc",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0039-github-ci-qa-evidence/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "9865bf4c116648a19cff5563f3b6a4a3270a5cbc",
    "content_sha256": "9cf058b8c67182f2c3720319c65f1324f28b60edf31110274243c977f5587eb4",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0040-contract-cutover-and-program-closure/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "88345aeb2cfa3900b92423773bb83b8882c35004",
    "content_sha256": "2594591621e51099bf1136c77cffd92313a8a6071fc296395b636483546a6412",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/agent-design.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0041-stage-00-agent-governance-contract/spec.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "a1fdd8e677885ac6e6607188764f8dcd4a49dd25",
    "content_sha256": "a6a6359b01a005877e600ef84ff3a7941c8f1d723e4c7b2e4780a1b53d878d51",
    "reason": "Fold valid change-local role boundaries into the owning Spec/Plan without retaining a permanent agent-design family."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0041-stage-00-agent-governance-contract/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "99b33be36fdd2a7aec5d1a9130816e6061be3c39",
    "content_sha256": "351e44ae722b50fa791870a2bc5384f8c2688000aa8768fe597232ec083fe183",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "b7a882ee29dd436895d618eea6483cc4a07681e6",
    "content_sha256": "6d11891b08ebaca76bf2a1c56fb3e4d47905a3580895c0608ed3d227ddf660e6",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0043-agent-harness-loop-lifecycle/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "2d416ded2a4b175516352ec63f28b95f5db431bc",
    "content_sha256": "3b5bb186cb25c554405d5c0e0b6a95d38620ec80ea6b7995020097870ab8de18",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0044-agent-roster-evaluation-and-admission/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "c48ddde87b1e9829348b369e884fb43eccad1e44",
    "content_sha256": "ed0a1b4cdf72a6d3c066478cb0faf78a2f838609052f1931c6e5b51f0f0693be",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0045-agent-governance-ci-qa-cutover/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "b130066b825e6e98df70e1269ba79247f912d12f",
    "content_sha256": "c5bf52a332965de7c2514d9415341d6dcaf871484553469c1dd81958e94a56cc",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0046-agent-governance-program-closure/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "e7aaf0fb115ce88703348830fadb2a017b22e254",
    "content_sha256": "23225289ab1cf7440cf38c685171da4708214fdf907062885e4d757b884f7ec5",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0047-current-surface-and-stash-reconciliation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "ee1e3dda608a3d1018226755da6f20ef5d0abbb8",
    "content_sha256": "7a3ef41dfa8110641c3928076474331bb6347f4ec8adcd6a32cc70ba2a744dfb",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0048-github-routing-and-ci-evidence/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0048-github-routing-and-ci-evidence/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "799718abc79d5ed20ca1e9d46f7c98156f259da7",
    "content_sha256": "902df479fdbf62d2a12f020cd83ad26f4a21024c72cb3117b485fa49d7686686",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0049-platform-validation-and-security-evidence/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0049-platform-validation-and-security-evidence/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "a9deff02a78d3328060609d93f57d03f8b0824c8",
    "content_sha256": "4c89088d724f480499284535c4c864614114278a54466dabd675d117c2ef67e3",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0050-example-iac-and-validator-qa/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0050-example-iac-and-validator-qa/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "d5844fddcb248930dd33ce6fb536f42f0893025f",
    "content_sha256": "59e7e6cf7faf4dd80113c99e860e6050b848b911c010aa57d42a3e8b492404b5",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0051-repository-assurance-integration-and-closure/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0051-repository-assurance-integration-and-closure/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "244352856d66a0d365bbafbd1e6444f4a17f60ef",
    "content_sha256": "6857abfea1a025abeebaadb6a22321edb02579af5d58258cd076afc2b225fc7a",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0052-document-taxonomy-consolidation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "6de3eafb0e16624a569723557bf6bb0472d708a1",
    "content_sha256": "366e161acafc0e8d3619b6e3085a70ff9e82f372a82f1fd678f2caeec06c5eea",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "b920f1d490152f6353911f0fba556f49b18a05e1",
    "content_sha256": "91d5c21923247e9a6f2c3383ce1ea5bb5ef134a5aa6ebc87fe476a436672f6f9",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "465f24340b99c03a38b5150d517627b69fa7c717",
    "content_sha256": "3fd4925824ad0b92748ff0f27e3a252dee3619c415caff02cc59a385e4c8fc08",
    "reason": "Replace the final transitional Spec 0054 ledger with its package README router and append-only Task records."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0055-workspace-governance-audit-and-remediation/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "977c227a84cb683e59e1898d4b1dda0afdc9163a",
    "content_sha256": "397885782724854276ced6ce13c8e8a99beb948f4c02dea681ba73b834908d25",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "4b506f33423325c0ebf7876388ff8edb4151b77c",
    "content_sha256": "30d484c77de429cb855e5519dc61863d3fe348a1e68f0e8ad9ae79b875e42453",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "24327ea1c8e60712c97c7ad92e76355d5217005e",
    "content_sha256": "c0c8cc6765eb121715bf39120fda43f7781d3ccc05cfb8fad63781de6d66aa28",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "7230cd5f5a92f3b59d0d6f4d6b19076c3d939644",
    "content_sha256": "8819b8ed8166ccc0ae58226730e17cd420e4bebbc50849d58695716558eebe5f",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0059-workspace-research-full-corpus-refresh/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "ff585a5535136da721ead0ea0bf99a034a3bce30",
    "content_sha256": "5124f9e3f1c710c29f656c99e7056b58a0423765865455714557f5abf86cf5b2",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0060-platform-currency-defect-closure/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "080e5606eae9ac03f78c766bf4e789b7e043c7e0",
    "content_sha256": "38f44a008744de162968915bb9c2885c6fd60e9a50232f5a40dba23611cee0a0",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/tasks.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/03.specs/0061-workload-security-context-baseline/README.md",
    "source_commit": "211e167f9ef0268c937303faa82d7ed297b33e38",
    "source_blob": "ab7622a359f68b724d186d232649544dbc2bcfa4",
    "content_sha256": "8ecbd34a901f24a5884f137bb90dde9b33e820a3756884c0587448d2f7afa7c1",
    "reason": "Monolithic ledger decomposed into package-local append-only Task records enumerated by the package router."
  },
  {
    "legacy_path": "docs/99.templates/contracts/registry-form.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/contracts/document-profile.schema.json",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "8a7428c78af244ed74912a09eb312ac1a964b875",
    "content_sha256": "046b40d8771841324e07f295a290f9787f00f8673524faa02d8e0f19868a6fb2",
    "reason": "Merge the registry-form constraint into the terminal document-profile schema."
  },
  {
    "legacy_path": "docs/99.templates/contracts/route-contract.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/registry.json",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "c956b1571349efc60fb370d6d4bb8c2a63078ab8",
    "content_sha256": "850459a15042575819ad6888713d61ddabd3fbb9726aefcfa4669ba60e7ccc48",
    "reason": "Retire the route projection in favour of the root registry."
  },
  {
    "legacy_path": "docs/99.templates/contracts/route-contract.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/registry.json",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "1912c0fc757af1f71a0dccc688c8573a57566361",
    "content_sha256": "8268892e23e47b5c644d829b40a031b929fd4154a0dc399cc9cec4a5acd1d756",
    "reason": "Retire the route projection schema in favour of the root registry."
  },
  {
    "legacy_path": "docs/99.templates/support/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "76a0fa42a697c52563e2bf7d21fb9148507c2876",
    "content_sha256": "fb4bed2bab027161f7425226f4c3b9b61f25413ccd31a89654b49a25c45901a1",
    "reason": "Merge support routing into the terminal Stage99 README."
  },
  {
    "legacy_path": "docs/99.templates/support/document-contract.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "1ee845da3aa42262586de2eac2da753b5e63e8cf",
    "content_sha256": "b181ed92176bf359f580e76872214c2252050d2022a95d82296da32d78febce5",
    "reason": "Merge support guidance into the terminal Stage99 README."
  },
  {
    "legacy_path": "docs/99.templates/support/document-lifecycle.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "5877d1989a45248918354f43d53e5ad71577fa76",
    "content_sha256": "dab00c4c3f07f4ec5336413f3fb15b461b5fb0439ff60b77d23eb67e3e2e41b1",
    "reason": "Merge lifecycle guidance into the terminal Stage99 README."
  },
  {
    "legacy_path": "docs/99.templates/support/document-profiles.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/registry.json",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "2d6fd0d40ec4e2d8d8b0d621b4c5d286f1952da2",
    "content_sha256": "ae873c96a1ace5069b891095abb5887271b5d53d523cfcd4ea2fa47499f94d42",
    "reason": "Replace the flat profile projection with the root registry."
  },
  {
    "legacy_path": "docs/99.templates/templates/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "f1081128f8271140166c2b92aa039cb8e987f8ed",
    "content_sha256": "568c84c88ab19c876aa4416660853005130631b088061b81b713cc71a6e5d097",
    "reason": "Use the terminal Stage99 README router."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/archive-migration.template.md",
    "stable_path": "docs/99.templates/templates/archive/archive-migration.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "dc3164eafd322e8139164cc16342de43fc3a72e8",
    "content_sha256": "1cbf119fbdd0340f35a002c9e12232e7d5986bf80968e23e6bc1e3ad4edc295f",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/archive-record.template.md",
    "stable_path": "docs/99.templates/templates/archive/archive-record.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "e4c080ec323f87d9745ac988d52561efe4ab1547",
    "content_sha256": "6ee6974911b215217b4a59e377e144f6eff1aa28efbfd647dd2897cc087b6b24",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/governance-reference.template.md",
    "stable_path": "docs/99.templates/templates/governance/governance-reference.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "a5209bd57c3edbc36cf5c0c980b04691f63c889c",
    "content_sha256": "8877925295c0b6a2a6162146b97d2a9a51d29fb4a06f72f3ee9a3abc6f7e89db",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/memory.template.md",
    "stable_path": "docs/99.templates/templates/governance/memory.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "b7f80ea24323e6e4b956dea9531a64827d488e48",
    "content_sha256": "eaf93f9007ef3019b690d4f86431367c2dfc422c850bf4964f6425fa49848572",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/progress.template.md",
    "stable_path": "docs/99.templates/templates/governance/progress.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "41eb12709d2a75ba137df87143774985d2401247",
    "content_sha256": "b8261f60bf201d7bf8be0f7d8a7978dc02c070f6ea695bccb40e85b99ed7f5bb",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/reference.template.md",
    "stable_path": "docs/99.templates/templates/references/reference.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "314ab057919f482a08879b05985981d8913ff426",
    "content_sha256": "6257ad1286c3ef8bb1ae5933f22f841271e8eecfc88028b45b741830ffa20d63",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/common/template-support.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/README.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "f24007775ce134141244625931238a14b9890a3e",
    "content_sha256": "e94d2571bf27236bbbadd2c443f4608479a59e852ebaeb511b18b9da77550bea",
    "reason": "Retire the template-support form in favour of the Stage99 router."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/architecture/ad.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/architecture/ad.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "1ed3a4ebf63989046aba2ecced312faba50b64ec",
    "content_sha256": "a355f439a3de2c7d90932ad0dd2193b993140870a6b34034adf2e31d873690f2",
    "reason": "Replace the predecessor form with the terminal Stage99 architecture form and its normalized requirement traceability example."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/architecture/adr.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/architecture/adr.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "85b16084042825695ac198837cfb773ad89d0acc",
    "content_sha256": "62fbd0ac93025392032facedf6c4a8717c10634248d36d250544aad82395107e",
    "reason": "Replace the retained form with the terminal Stage99 profile-bound form."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/execution/plan.template.md",
    "stable_path": "docs/99.templates/templates/specs/plan.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "85868ea88dd80ffd5a2b1f00a39972ebe64ee000",
    "content_sha256": "f5074f79bc1d55f3158f20b351ca966958add88d8edd5c3aa6576fc924509aa9",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/execution/task.template.md",
    "stable_path": "docs/99.templates/templates/specs/task.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "962d31d707d8e46e3e2b1b0c10cc48c1c87d48b5",
    "content_sha256": "54a1e896195d55d1eded63aeb8ab1d3b5c7464b2f2af9d954285754805935e5d",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/operations/guide.template.md",
    "stable_path": "docs/99.templates/templates/operations/guide.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "f3a531cfa3434292a0d75a85a37030fa11871014",
    "content_sha256": "c42537bdde247fda2eaf90660c76304240bc612e4be01bc3817b892253e7b9df",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/operations/incident.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/operations/incident.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "207fd1f6a5c35623e6386ff11a3fad17e9343efd",
    "content_sha256": "f9c10d1fc04c02d69dbcfaccb6927ac99902fac12c62510f988c3bd83789f4bf",
    "reason": "Replace the retained form with the terminal Stage99 profile-bound form."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/operations/policy.template.md",
    "stable_path": "docs/99.templates/templates/operations/policy.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "bdaf39f2df8b37cf124f2491cb3a6396cbd459a7",
    "content_sha256": "61f5a1d7b2b2b5debcf2122672a632c5a13aabe16b64a214f5b6c2496acd1deb",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/operations/postmortem.template.md",
    "stable_path": "docs/99.templates/templates/operations/postmortem.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "03fe6d22e43a71f391e734f2291d98cf77623a2a",
    "content_sha256": "269f3040cc2e15080b60187e357cd96a499efd199f0fa84a9fe5c4f371693b7b",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/operations/runbook.template.md",
    "stable_path": "docs/99.templates/templates/operations/runbook.template.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "7f040add638431b5f906702d80bce22e2d5c0bf2",
    "content_sha256": "3d272e6ed14996c3d29a87cbf750410d2a5e96dbdaa98bdbfc6b8101f449e381",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/requirements/interface.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/requirements/requirement-package.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "6fc69b5ce76fb2566e1a77801cab396b4410e203",
    "content_sha256": "446146d22d19c9382131eb9918717e61f897c38d2ba06d5339c9f5af36be801d",
    "reason": "Unify interface requirements under the Requirement Package form."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/requirements/prd.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/requirements/requirement-package.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "a0b01020dffc8ddd8fdbd0b3b3fb1a5ac7bdab48",
    "content_sha256": "5b1f8a4698efa381d31eeb60ba7ec24a43ac54cfc895573c7cc46b3e723fc967",
    "reason": "Replace the predecessor PRD form with the consolidated Requirement Package form and package-scoped member identities."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/requirements/srs.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/requirements/requirement-package.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "f8d8d8296d5621f3a1062af962198cbae3856711",
    "content_sha256": "fe2d4e29404df7419183e01f1a0ea73fe198a97a70237dc46445321b1a9b6ed1",
    "reason": "Unify SRS requirements under the Requirement Package form."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/agent-design.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/specs/spec.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "6311798fa9a90e1eeef988c59d7f1c53b6e428d4",
    "content_sha256": "b40f068f2406f07dabef823ff67bb9061534756bf10c9dcf80bd4a8cb7f0438a",
    "reason": "Retire agent-design as a permanent document form in favour of Spec."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/data-model.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/specs/data-model.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "d06a2716a20a514ec7bc308fbe2a9201b8b5b8f7",
    "content_sha256": "f45c2b064c9e8e02837e78557cd09d38ded95d12f67dad2d046ec91d7c02403a",
    "reason": "Replace the predecessor form with the terminal Stage99 data-model form and normalized requirement traceability contract."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/openapi.template.yaml",
    "stable_path": "docs/99.templates/templates/specs/openapi.template.yaml",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "7492ec59f553b1ecc7fedb945aace243d28a9149",
    "content_sha256": "aba7ee08fd3c45e63edbc0557911c86ea8b31a47f9afbc3016d2439c65ed1176",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/schema.template.graphql",
    "stable_path": "docs/99.templates/templates/specs/schema.template.graphql",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "f39499ce00d55b88e520400194a5eaad4c263386",
    "content_sha256": "cd6d8b531799d3fd617fe404b441f80c5ab7dc2893bd8519c5ad053c3037dd4a",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/service.template.proto",
    "stable_path": "docs/99.templates/templates/specs/service.template.proto",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "2d9288896bb3c83e7a2ef08f049662cd6e290df1",
    "content_sha256": "b601274f4a078e14350e0d3694ad846544b266293d04764f68ac8decc7bca4b8",
    "reason": "Move retained form to the terminal Stage99 group."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/spec.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/specs/spec.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "37933bc3f5a84546c72eb7450c3915cf4d62e70b",
    "content_sha256": "c390b1fa7a6c9a6bab5ed47ef882581d6ec071d23d0714b8dd86221d4b6fa1f5",
    "reason": "Replace the predecessor form with the terminal Stage99 Spec form and normalized requirement traceability contract."
  },
  {
    "legacy_path": "docs/99.templates/templates/sdlc/specs/tests.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/99.templates/templates/specs/spec.template.md",
    "source_commit": "7a770c3c0eabaeda554c4030fc08fb17de164fe5",
    "source_blob": "3688976891260e7d49c890ee6b0162eff1670a26",
    "content_sha256": "9d8662cd3aafc415e7b99f04b9d865178db43c5ca07ee44f3701165c11b266ff",
    "reason": "Retire permanent tests as a document form in favour of Spec."
  }
]

```

## Recovery

Recovery fails closed unless `source_commit` is a full commit OID reachable
from the durable current ref, `legacy_path` resolves to the recorded regular
blob, the bounded blob read matches `source_blob`, and its SHA-256 matches
`content_sha256`. Recover bytes with `git show <source_commit>:<legacy_path>`.
Replaced and merged rows follow `replacement`; moved rows follow `stable_path`.
