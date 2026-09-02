---
title: "Stage 03 Package Router Retirement"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-02"
artifact_id: "MIG-0011"
---

# MIG-0011: Stage 03 Package Router Retirement

## Overview

This reviewed ledger records the sixty-three Stage 03 package routers that
retire because the package already proves its own navigation. `spec.md` owns
the change contract, `plan.md` owns implementation order and risk, and
`tasks/` is the Task inventory. The router restated all three and was the only
document that had to be edited whenever a Task was added, so it was a
duplicate index rather than an owner.

Every row is `merged`: the router's routing responsibility moves to the
package Plan, or to the package Spec for the ten packages that have no Plan.
Three packages already carried no router, so the retired shape was not
universal even before this change.

The one router that owned unique content was Spec 0054's shared execution
contract. That text moved into `plan.md` under Global Constraints, where the
Plan already owns the package's execution boundary, and every citation was
repointed in the same change.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/03.specs/0004-argo-rollouts-progressive-delivery/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0004-argo-rollouts-progressive-delivery/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "3847115229db69f60e63dceaf1120bd77b4e2174",
    "content_sha256": "31cabd0ab9502a98d0d26086253b22329521ed0e63b3f5d948595163024c08d6",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0005-argo-notifications-slack/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0005-argo-notifications-slack/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "cd274a8b63259a3ab7205a7ba0b2983fc1af6f2b",
    "content_sha256": "0517eb4762353cce35be35a13fb45238d1254b6bd05d56ce43a044e216fefb62",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0006-workspace-harness-gap-analysis/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0006-workspace-harness-gap-analysis/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "933b7346ebfef0c6dc42ae3b2835171e36cdb2d3",
    "content_sha256": "c866f90acdc83d4de399ff53279e187b59f59220e5e7fc35a50d6e3b8b2ffc5f",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0008-current-local-gitops-platform/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0008-current-local-gitops-platform/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "6655537ab1bd8c35445449519f0e9a471278cddd",
    "content_sha256": "67f43c9f00db62e7a1ab3a565fc056d2a2a9ce69ab686ecc5dcefbac0311008d",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0009-workspace-harness-research-pack/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "10555fa8858b7ed52646ab0c3b6acb072fcbce1c",
    "content_sha256": "156fef11b1e44e3f6ea45ea771f3223aa1664cf46a89bee59a51aaf27309de2a",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "19b6a5c556dd4f23c02faa2259d63255e43c5089",
    "content_sha256": "9bdff9d1a3a7f51cace48fa47875c35e7518177391fe491d3f3d3848c09bc79c",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0011-template-contract-governance-migration/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "dcd24be7e6f3a7c6d527181bdb7d16449d6044f8",
    "content_sha256": "0aa783a709e74a29a0f2faacb78926672851a07ac73f172637b5534b78cb7361",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0012-template-governance-audit-enhancement/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "bb3867894b4332815ed84a3db8ba7ca78b3dde10",
    "content_sha256": "38b19d57ee3f4821982d892340de86ba2edf1ad3080703e91f40d26c7c41dcdd",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "39bd5e5cea8a49b3e09c4733623f2cc90bcbdca1",
    "content_sha256": "6cc6f8f25675650477811f688b21d025c6860c56f16ccf524df0b952d9cdda64",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0014-workspace-document-contract-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "c3a7df7192a98e32cff321f9fb0e4891d3041518",
    "content_sha256": "2f33c5c8f0d8fa0dab7c389c0b14ca61003f6dbaceb9cfa2bc451faddd6bbc0f",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0015-agent-governance-contract-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "43a72d993204e5c7bfddfd563b8c8e42eca40a26",
    "content_sha256": "7f626171bacd3331072bfa3ab2c0844bdbd90c7497582d2cbda9e954018906ad",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0016-active-control-surface-governance-hardening/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "cfe8b9cc47439f401aa0dcdc375ea2f030dfbba4",
    "content_sha256": "aa04150553e07b17558d98a913f01f942f6311bbd1873f3c6923e6cc2f06d9e8",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0017-workspace-engineering-research-pack/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "69def8797cc31c1fa7b011e3d4a86731a22fa04f",
    "content_sha256": "f7ce30f6353dd857772ed9f38faa7e55224553b2bbc7649b2fc899f4a2bd82d6",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "1edbbffe3844ac60b852ed9f1c8f56b879f02ff7",
    "content_sha256": "57c4a52b319f5769d7f71487c61ea382e086a0956f5d33ff63e52709f66004c7",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0019-template-path-numbering-contract/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "98982d5771ca7f3bf02f91f7509d2175fd3437da",
    "content_sha256": "4515f2a164957ff6a8b34331ee722153e10c165da9cac63e66fbcc746cda0b25",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0020-workspace-contract-governance-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "00b5b3a6903c7fb0ef8e40feeb968c24515c1f0e",
    "content_sha256": "1dea228dacaf170c0e1eb4c1412a7e7a55c699f69b20bca08b02bd85d1494008",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0021-sdlc-lifecycle-contract/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "49d445bd05eae3192304d8ad89ea9e5134f78369",
    "content_sha256": "d5a563820f45e96314cce8ab89248b934bca2ce3544273c629c4cf6839e8f69d",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0022-control-cloud-doc-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "e6b69ab76988fb51708200e4d3055cdc7f8318d1",
    "content_sha256": "d2f62218f0204c57599c3324fea582aec7d6cbfb06d150f128e8ff7566de3763",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "4ae247c851c30778a54d375686b03c5a8e27e93f",
    "content_sha256": "e660605a5078a8c104acf16cdf3cc83ef47b24de334849901db5babd8004c961",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0024-observability-and-network-review-agents/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "1fd269094d8977f19236b616930b2d95842b9c80",
    "content_sha256": "7b550ee02a905e8f4ae7ada33f913112e174650fc9a7bbd9f247d58b2121ce88",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0025-governance-owner-and-roster-currentness/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "2172ccfb88891a1ef4ae48991f470a74c4036379",
    "content_sha256": "87a3e20a073bd409b3d323ea5b4fdf55f13f116c20d8d0135ec4912996a3ac57",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0026-document-contract-registry/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "a50594adec171aec8e02ceb6ebef1df33d4e90e7",
    "content_sha256": "74c452aa2aadc07b6932d9e820e1e6607d382c54a3ad23a13a55a7aba848f1da",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0027-template-contract-consolidation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "faca05afb565674bd888dce08f65a8fdb740a835",
    "content_sha256": "1b00eb562a8f3aa99d1c5cb4b461a1ac0b5bd184a6df620d4759332fc8e1c757",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0028-readme-workspace-profiles/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "079a1cc4b2eea77065ddfc1b2f9c3cf57a3c9141",
    "content_sha256": "3cf157acc5f62ef20f3b3e73a38e486132737966c5f093aaa1359ad0338fbd46",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0029-semantic-document-validation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "9a9d1f3504cac6fae136d13a7fd00f8d25dc25f5",
    "content_sha256": "b341fea1b3cc72e9b59b3bf8d9f20a93c24bafd7a7bdf6a02f13eab6ac2fc9c7",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0030-authored-document-migration/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "744a0c0520a55ffda42a7bdcd67fbfda057bd2c6",
    "content_sha256": "1e68aa4140c20b547c44f8b5c4663f7e20ce3fc770f538b692a155a2e69fe904",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0031-affected-surface-agent-qa/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0031-affected-surface-agent-qa/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "e750673eab0122fbd7c031e1ff255860e357326e",
    "content_sha256": "3e314beffbb187974744eaea60a2d74e50f1590f6b1c34a074280092c3fa0a5c",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0032-protected-surface-supply-chain-hardening/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0032-protected-surface-supply-chain-hardening/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "4adca02708dc54402910a5ba78048d1c723a35ec",
    "content_sha256": "1a66cfae8b23f5f8e0636e8b438ad5625607fd71bbd5c5dd6fb71452e25a1942",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0033-template-lifecycle-contract-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0033-template-lifecycle-contract-normalization/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "9dd7ef0d136751d5e8d603d8d5938132cce2ba48",
    "content_sha256": "ba4995269bba231bb92d9f9dddb46c0ce15c4302cdbb7ff288dc6cd030ba7fa0",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0034-authority-and-lineage-foundation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0034-authority-and-lineage-foundation/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "11873df0ec7b59372c7030c8cb286e2db4767bce",
    "content_sha256": "ad2aefa41c76898ddab0922587ebd8e85ee2f94e8dd0921d6720ece9f8b94a7c",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0035-document-schema-and-lifecycle-contract/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0035-document-schema-and-lifecycle-contract/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "17dd33588f3fc3b74ee5788d27c2916df86cd926",
    "content_sha256": "989498d7bf18359d998da12d5d4e3577497002f7b1608764abbf4f2ede04b588",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0036-archive-record-and-workspace-boundary/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "3f2a97a25f26adb8542dcb6986f622975db29d23",
    "content_sha256": "e31cd5edf813264a8c0adf0ac85b041cda068a7fc6ec9e9b899b81b2cabae103",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0037-active-corpus-and-execution-retention/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "cca9eda8d518afddb63b55163456cfe3cc2fec7c",
    "content_sha256": "e063cc69098a2972dd0eeb9cb2d9f4c89940094d08484109ccee0d04b7cb9674",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0038-reference-information-architecture/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "42b810c031d643fe20f99bef2b0237e63b992f6b",
    "content_sha256": "c3aa1aa4c4e4b48c6139fe08ca154ffd9c7b58dd09e6ccb3a5f701ed4cce8a69",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0039-github-ci-qa-evidence/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "723173e96a2b13f8db085ce9260c3b63e83a6048",
    "content_sha256": "5c08961d04ce202c07bcec6a974a568bec0272f2f3026f9839889ddfb569fea4",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0040-contract-cutover-and-program-closure/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "41e22b10687255d62aaa30c230b497e946874a35",
    "content_sha256": "160b0534461f04aedd646d2681f6c5c1069bab5432466bc46fc832b675a7ef23",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0041-stage-00-agent-governance-contract/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "b52c8f228ea548a46d61d20949cad25f557b4a29",
    "content_sha256": "3f0165f524af702cb78bc5ed1ff1e1f05ef1cd16e90ffcd7745c8aed05d4b840",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "ffab20e5fa64e37dc08084a3257812caefbe6c44",
    "content_sha256": "db413a5ec12cad1374dba4d26816aeb198abfb2a096851ec8ac57708b65ee282",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0043-agent-harness-loop-lifecycle/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "2a9972a2692f352d80ebc682b148c7dd6af7bbbf",
    "content_sha256": "9bac48e3446580617f3f38c07e5ef470dda74dab4bd3553816e98558394edc6d",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0044-agent-roster-evaluation-and-admission/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "8d84fa1550dcf0b4f8416d5facbd6a4c2798e94b",
    "content_sha256": "c45840a64a38573c68603e9441a37bef3142d15c58565fde668093a6b498f1ab",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0045-agent-governance-ci-qa-cutover/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "cfb052e2b9e047e9f05fc8be34bff52f32d37d33",
    "content_sha256": "d27caaf9b519742799a72455cf2db16f96a9735e7152beaab40da0a0f6faffb0",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0046-agent-governance-program-closure/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "74d90397890d6e1bd9f88eddd6e7172f31b1ff7d",
    "content_sha256": "5b3e20ddcdd1859fe1a66ef00017fb48d159bb3f3633f51a5cb73c0680ede969",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "3ffba1857608f19c586cf12fbfd822f7a4546733",
    "content_sha256": "b4dffe2d8ce4fa99ba62e362f46deeb8cf07b7ce1b83bdd0c47afb523ea0d965",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0048-github-routing-and-ci-evidence/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0048-github-routing-and-ci-evidence/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "f33a6a7b35543188147c953ea6a439160f1ae354",
    "content_sha256": "4102f5021e61f730e47cc6280790745b40fd4a91e87c4197376f2614eb0ad3ba",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0049-platform-validation-and-security-evidence/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0049-platform-validation-and-security-evidence/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "6ad309c77590cd326a741382f9db4dbe627ebde8",
    "content_sha256": "98e3efd51e5a36644bbd705edc2aea09463e9dd712a9b8476aa1804b1fb6a005",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0050-example-iac-and-validator-qa/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0050-example-iac-and-validator-qa/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "edccee9c986523ef4c0905d9a4edec435c6dba9d",
    "content_sha256": "c6a2710ebf2145a1603f560c5488da656b067a65eda7923dbb73e83d02873cd2",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0051-repository-assurance-integration-and-closure/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0051-repository-assurance-integration-and-closure/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "f47a3f106aff0be25fadcf816fd8191156ad4391",
    "content_sha256": "9a1c0c9538bd8fe58a0a064195aac4268fb88da5e537738f0eedffd7a7c8eb81",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0052-document-taxonomy-consolidation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "e5d352c281b1aac994be36041b8ea0f0cfd897bb",
    "content_sha256": "b65a0bc7255e9ef43b4b1286a4ae2e7735f413ac988e6bc3fed5e54c2e4568e3",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "af0f2747d51ae1468453893843162f3350d94fe7",
    "content_sha256": "e40bb6485766d958b97edbef44ce8ca4fb3fd0e5bd85d6f68b33a66748fde302",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "250e710d567ecf8544159682552fc01e5876b40b",
    "content_sha256": "b3ba801dc61308d742b6d9eaa901505fcf9e1fc8addf6e180eee2b2cdc2d0a82",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0055-workspace-governance-audit-and-remediation/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "679f1886636bb57d048479196e874b698acaeee4",
    "content_sha256": "596a994bc03dfe815811e5b1806ca6b33acbdda98157c5c7d7116b7b67477dda",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "38e946d8083cf8e7e948fd4f98772dca1a5b1b17",
    "content_sha256": "49f917aa0227a5dd67d4522e303a9048fba0ca197f3cf111c0313a351aaa9ac0",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "d109c51e35decf261f87d210962711b59605a075",
    "content_sha256": "8463be943e48d6c5f07a6659ebf3523df37d87fe9557b14f0416b68a76591d36",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "ba2400a5de862fe236681e022cabe551768f8af7",
    "content_sha256": "a03fb56009ebc0c146dc7ecc91e0231bfe63843b7ab7d494e1843ec3f4c31f51",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0059-workspace-research-full-corpus-refresh/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "1f82a5f68b6c3e0f26d9e712fec3c062add72cad",
    "content_sha256": "f82a27f2f34e688fb24992970279fd8fd08f253055965c07a68031f771ffaa5f",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0060-platform-currency-defect-closure/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "c4ca18f81687312df9497222cd4091efe2dc0e4e",
    "content_sha256": "d00d1d934f17d7e4c9731251c1e622894f88ee52af219a7839f932666aad44a4",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0061-workload-security-context-baseline/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "745a15e769e4e80abe7bc2d9c5e7995a5bdc693c",
    "content_sha256": "d204f8e25511c0ff3853afde2e884d8810ce61237c52f7652d478d6eb3c5babc",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0062-workspace-research-full-corpus-reverification/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "97fdd005247d4b4a77a9cde1c77adc4785aececc",
    "content_sha256": "fd9f2669f8551c59437f8e946ce1044d99c23bbd491c4c6964a52f6d0df1e6d8",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0066-validation-tooling-ownership/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0066-validation-tooling-ownership/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "90db685c2f80c73b4be83fca7a994140b3bda42e",
    "content_sha256": "95705fcea0a6512d4ceb107f44aa648ee28e1fbf8995b8a329747fa0174ead3c",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0067-artifact-identity-and-filename-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0067-artifact-identity-and-filename-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "86d8a43f01133054041b78f391e96115204d4cbe",
    "content_sha256": "1c70271625c9f0118fc109cf18920ae3d6842ecfe45593ea4a920202192552aa",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  },
  {
    "legacy_path": "docs/03.specs/0068-agent-projection-rendering-and-gate-reduction/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0068-agent-projection-rendering-and-gate-reduction/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "98c5cc9b8715dbaf9c1de152ec412f08ed7d822b",
    "content_sha256": "c1d868311c5ce53ef7b0aa3f55d6e8d53ef974a81c347cd9a79b2df94fea79d7",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0070-retired-provider-residue-disposition/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0070-retired-provider-residue-disposition/spec.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "7f1adfb74702ae4b5857775c5d1679799df197f8",
    "content_sha256": "a5d427360777877f257be0dfb2e4446e2fd7f0405f93a7f65a28f6f2eec16d9b",
    "reason": "The package router duplicated navigation the package already proves. This package has no Plan, so its routing responsibility merges into the package Spec."
  },
  {
    "legacy_path": "docs/03.specs/0071-document-taxonomy-and-form-identity-normalization/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/03.specs/0071-document-taxonomy-and-form-identity-normalization/plan.md",
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "251b383879b005b1f3d0faf4f019e86d91e6e4a7",
    "content_sha256": "2f7b1334a40fffe07c04635bf4d4411340aaece61a1f60a0f49d0cdd78971abd",
    "reason": "The package router duplicated navigation the package already proves: spec.md owns the contract, plan.md owns execution order, and tasks/ is the Task inventory. Its routing responsibility merges into the package Plan."
  }
]
```

## Recovery

For every row, recover the legacy bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Each `merged` row resolves through `replacement`, and the
legacy bytes remain recoverable from Git history at the pinned commit.

### Historical consumers

Every routed citation of a retired router was repointed at its successor in the
same change, so no consumer needs a pinned historical declaration here and this
block admits no path. The nine documents whose retired-surface coverage MIG-0005
pins are re-pinned in that record against the bytes they now carry, because a
consumer identity belongs to exactly one sealed record.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
