---
title: "98.archive"
version: "0.5.0"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "archive"
---

# 98.archive

> 활성 stage가 더 이상 싣지 않는 것을 retention class 네 가지와 route disposition 두 가지로 보존하는 비현재 archive stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../.agents/README.md).

## Overview

`98.archive/`는 활성 stage가 더 이상 싣지 않는 것을 여섯 가지 disposition으로 보존하는 비현재 stage다. 모델의 결정 기록은 [ADR-0038](../02.architecture/decisions/0038-six-disposition-archive-stage.md)이며 `accepted` 상태다. [SPEC-0079](../03.specs/0079-six-disposition-archive-stage/spec.md)가 registry route, archive form, 검증기를 이 모델로 전환했다. [ADR-0032](./superseded/02.architecture/decisions/0032-completed-and-terminal-document-retention.md) 형식의 봉인 record 25개와 원장 23개는 registry가 정확한 경로로만 분류하므로, 새 봉인 record나 path ledger는 만들 수 없다.

각 disposition은 자신을 처음 사용하는 변경이 만드는 디렉터리를 소유하므로, record가 아직 없는 disposition에는 디렉터리가 없다. family는 두 종류이며, 종류가 디렉터리에 무엇을 담는지와 현재 문서가 그것을 인용할 수 있는지를 결정한다.

### Retention Class

**Retention class**는 한때 현재였던 본문 전체를 당시 적용된 profile 그대로 보관한다. 더 이상 현재가 아닌 governed 문서는 Stage 01, 02, 03, 05, 90, 99를 떠나 실제로 일어난 일에 맞는 class에 보관되며, superseded ADR도 예외가 아니다. 보존은 profile을 따른다. 동결된 본문은 immutable로 남고, Git-history-only disposition은 호환 복제본 없이 복구 가능한 provenance만 남긴다. disposition마다 별도 승인이 필요하다.

- `completed/`: 끝나서 반영된 작업을 보관한다. 무엇을 promote했는지 명명하며, 활성 stage에서 인용할 수 있다.
- `superseded/`: 더 새로운 현재 authority가 대체한 내용을 보관한다. 대체한 문서를 명명하며, 인용할 수 없으므로 후속 문서를 인용한다.
- `retired/`: 후속 없이 철회된 rule 또는 scope를 보관한다. 철회 이유를 명명하며, 인용할 수 없다.
- `resolved/`: 종결된 Incident bundle과 발행된 Postmortem을 보관한다. 종결 증거와 현재 corrective-work owner를 명명하며, 역사 증거로서 인용할 수 있다.

### Route Disposition

**Route disposition**은 본문을 담지 않는다. 이 저장소 밖 consumer를 위한 route를 명명하므로, 현재 문서는 그 route를 명명한 record가 아니라 현재 route를 인용한다.

- `tombstones/`: 본문을 담지 않는다. 퇴역한 route, 그 후속 또는 부재, 이유를 명명하며, 인용할 수 없다.
- `migrations/`: 본문을 담지 않는다. 이동한 scope와 현재 owner를 `MIG-####`로 명명하며, 인용할 수 없다.

인용 가능성은 명명 방식에서 따라 나오며, 명명과 별도로 규정하지 않는다. retention class는 자신의 본문이 여전히 독자를 현재 authority로 이끌 때만 인용할 수 있다. `completed`는 Promotion 선언을 통해, `resolved`는 corrective-work owner를 통해 독자를 이끈다. `superseded` 본문은 대체 문서를 명명하므로 인용은 그 후속 문서에 둔다. 대체된 rule을 인용하는 것이 곧 그 rule이 되살아나는 경로이기 때문이다. `retired`에는 가리키는 대상이 없으므로, 인용하면 독자가 철회된 rule에 머문다.

### One Recovery Reference

어떤 family의 Stage 98 record도 두 번째 복구 원장을 갖지 않는다. redirect, path ledger, 자체 설계한 본문 digest, branch SHA, recovery commit이 없다. 새 disposition은 Document Index의 Retention Catalog 표에 행 하나를 두어 source Git object를 `<commit>:<original path>` 형식으로 한 번만 명명하고, 복구는 일반 Git history가 맡는다. 표의 머리글은 `Disposition Record`와 `Retention Envelope` 두 열이며, 첫 disposition이 표를 만든다. 동결 행의 `Source Commit`, `Source Blob`, `Payload SHA-256` 열은 동결 generation의 형식이며 새 disposition의 형식이 아니다.

### Frozen Generation

현재 보관된 내용은 모두 ADR-0038 이전 generation이며 immutable이다. `completed/`는 record가 아니라 문서 자체를 보관한다. ArchiveEnvelope가 없고, 자신의 profile과 종단 상태를 유지하며, 상대 링크 접두어만 보존 트리 기준으로 재기준된다. `superseded/`의 25개 record는 ArchiveEnvelope payload와 `source_commit`·`source_blob`·`content_sha256` provenance를 가진 봉인 record이고, `migrations/`의 원장은 행마다 commit·blob·digest를 고정한다. 이 generation은 새 형식에 맞추어 다시 쓰지 않으며 검증기는 이를 역사 증거로 분류한다. `completed/`의 기존 보존본 376개는 이를 봉인한 원장 행이 증명하므로 catalog 행이 필요 없다. 이 generation을 인용하는 기존 활성 문서는 SPEC-0079가 consumer로 열거하고 그대로 둔다.

<!-- archive-manifest:v1 records=25 historical-links=198 -->

[MIG-0005: Codex/Claude 거버넌스 수렴](./migrations/0005-codex-claude-agent-governance-convergence.md)은
제거된 권한 소스의 Git 복구 tuple과 현재 후속 소유자, 변경하지 않은 역사 링크
소비자의 유한 집합을 기록한다. 일반 행마다 full-body snapshot이나 tombstone을
추가하지 않으며, 후속 소유자 없는 삭제는 이 Archive 조회 경계로 해석한다.

## Stage Contract

### In Scope

- retention class `completed/`, `superseded/`, `retired/`, `resolved/`에 보관한 본문 전체
- route disposition `tombstones/`, `migrations/`가 명명하는 route와 현재 owner
- 새 disposition마다 Retention Catalog의 Retention Envelope `<commit>:<original path>` 한 개
- ADR-0038 이전 generation의 봉인 record, 원장, completed 보존본과 그 provenance
- index-only current navigation과 동결 payload 검증

### Out of Scope

- 현재 SDLC 또는 operations authority. 보존본을 인용해도 그것이 현재가 되지는 않는다
- 두 번째 복구 원장: redirect, path ledger, 자체 설계 본문 digest, branch SHA, recovery commit
- 동결 generation을 새 형식으로 다시 쓰거나 historical link를 현재 경로로 다시 쓰는 작업
- `mutable` 또는 `current` 상태 문서의 보관. 진행 중인 문서는 아무리 오래되어도 제자리에 남는다
- secret-bearing history의 일반 보존
- metadata 또는 payload를 조용히 수정하는 provenance repair

동결 generation에서는 ArchiveEnvelope.v1 marker 다음 byte부터 EOF까지가 payload다. Closing delimiter는 없으며 validator는 Git blob identity, payload byte count, final newline, SHA-256, mirror path, replacement dependency를 함께 확인한다.

## Document Index

아래 manifest는 25개 record의 source ownership과 digest를 모두 열거한다. `Historical Links`는 payload를 current tree가 아니라 각 `source_commit`과 `original_path` 문맥에서 해석한 local rendered link 수다. 모든 record는 후속 소유자를 명명하며, 현재 closure owner와 archive navigation boundary는 migration-result ledger와 namespace registry가 별도로 기록한다.

| Archive Record | Original Path | Original Type | Source Commit | Source Blob | Payload SHA-256 | Historical Links | Current Replacement | Reason |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| [`superseded/01.requirements/0001-wsl-k3d-argocd-platform.md`](./superseded/01.requirements/0001-wsl-k3d-argocd-platform.md) | `docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `9b453b87ae9a6a005c019a61da4924f3e91622ef` | `b5a0300136b39fd1d712586b3b25699f07becfb0c98e58166f8b852d0faf6b81` | 7 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`superseded/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md`](./superseded/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md) | `docs/01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `e0c5d1be8946798106f3e65ffd380096e2329fb2` | `50c643fd33eb0f1761c70eb1a1249e2493273f4533131927e85f37b5a993d343` | 4 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`superseded/01.requirements/0003-platform-expansion-dashboard-mesh.md`](./superseded/01.requirements/0003-platform-expansion-dashboard-mesh.md) | `docs/01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `a84a9e9938ede202a2e83b9deea51edc059f03b8` | `8e05ad6d3a4b45fc098ad159008b48764144cb412bd37686596660844b74bb34` | 10 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`superseded/02.architecture/0001-k3d-topology-and-network.md`](./superseded/02.architecture/0001-k3d-topology-and-network.md) | `docs/02.architecture/decisions/0001-k3d-topology-and-network.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `1a18548c491852b8e18b4466fffd50a05f5360a9` | `532c0e570c33fd0931f6573ffb63f3f65d733499808488b5c69983488002628f` | 8 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`superseded/02.architecture/0004-external-services-endpoints-and-valkey-backend.md`](./superseded/02.architecture/0004-external-services-endpoints-and-valkey-backend.md) | `docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `894105d51d7d031ce38c8016b7708b4750600adf` | `01e4ad60363dc2d5bf73bf0e9c16b5d2f682f11698ac2f8966bc7fe30bfbdd84` | 5 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`superseded/02.architecture/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./superseded/02.architecture/0005-wsl2-ha-baseline-and-external-endpoint-contract.md) | `docs/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `d35eaa0000d43cb887742a7d6173aafc4683a699` | `0226cbc4888c2f3dc6897739ba4d9b2e1c2b88c7f918ac72a7adfdb8bc1f19ab` | 6 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`superseded/02.architecture/0007-kubernetes-dashboard-v3.md`](./superseded/02.architecture/0007-kubernetes-dashboard-v3.md) | `docs/02.architecture/decisions/0007-kubernetes-dashboard-v3.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `7c7b4acb5bd68a08b415ca35683392acd701f9b5` | `a62c757f7566a601d0a948c4ecf17aa96b980346724436cba8d5eedd58835964` | 7 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`superseded/02.architecture/0010-headlamp-replaces-dashboard.md`](./superseded/02.architecture/0010-headlamp-replaces-dashboard.md) | `docs/02.architecture/decisions/0010-headlamp-replaces-dashboard.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `97ed0e3ea6a200942fc11d97d67da133069ed048` | `b08ec274a09d2134208b3594482f5a4f197ce7afe5bde5e4289c363b063177ee` | 6 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`superseded/02.architecture/0001-wsl-k3d-argocd-platform.md`](./superseded/02.architecture/0001-wsl-k3d-argocd-platform.md) | `docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `9001b10b9657396fe85d6d7b98112dcc6b310e4f` | `cbf08950c2da952a6ca7feaa122085700c5984c5b177a97d90277f3fcca4b44b` | 7 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`superseded/02.architecture/0002-wsl2-k3d-argocd-ha-platform.md`](./superseded/02.architecture/0002-wsl2-k3d-argocd-ha-platform.md) | `docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `37857c69bd334b3acc59705a701233a303c2bcb2` | `4a0902cee5048f2192e16c3688e9bf1e992e60fde4fe3865abb1fcd45767f59f` | 4 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`superseded/02.architecture/0003-platform-expansion-mesh-dashboard.md`](./superseded/02.architecture/0003-platform-expansion-mesh-dashboard.md) | `docs/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `4d38947d216e84dfc9430f4f632966292b602017` | `dfc0cd13ede805828a19909b2e525648c892dea9fc25d505d7becf8c27acd6b2` | 9 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`superseded/03.specs/0001-wsl-k3d-argocd-platform.md`](./superseded/03.specs/0001-wsl-k3d-argocd-platform.md) | `docs/03.specs/001-wsl-k3d-argocd-platform/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `814a42d68c3fe7f78cd6bf274ef08dfe662bb159` | `eb482d1d5ebb3815746815f3dc868ff1669d79b9a1effca53fd7347f55447298` | 15 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`superseded/03.specs/0002-wsl2-k3d-argocd-ha-platform.md`](./superseded/03.specs/0002-wsl2-k3d-argocd-ha-platform.md) | `docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `fc790ba116e35498a0527032c4c060600e087ac9` | `14eefadf9959c8f9d57167cdcffe41c02ac648c9389fa3a24ce50ad399f7b72d` | 10 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`superseded/03.specs/0003-platform-expansion.md`](./superseded/03.specs/0003-platform-expansion.md) | `docs/03.specs/003-platform-expansion/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `6d92ef1b7606fd20aeedd20cb5bb99c6a40d1dda` | `3363c2f0db122199ddf518fa144fbfdac036a1921df0042c2852055a55179d3b` | 21 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`superseded/03.specs/0007-docs-governance-consistency.md`](./superseded/03.specs/0007-docs-governance-consistency.md) | `docs/03.specs/007-docs-governance-consistency/spec.md` | `spec` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `cc803905127970c28fbb343ee69d71c27e0184f4` | `2143740f6a4c670976992e99e7ca8b35cc49e252912916991840b4a862dcfcbb` | 2 | `null` | `superseded` |
| [`superseded/05.operations/0004-headlamp-auth-oidc-guide.md`](./superseded/05.operations/0004-headlamp-auth-oidc-guide.md) | `docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md` | `guide` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `5786ac6cb75eb9c86b34bd7d61c1866ec1f693bc` | `a114a4c6632776de96eff8630fd5e672cccb31ffe425332198e7d5a96a427e65` | 4 | [`docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | `superseded` |
| [`superseded/05.operations/0005-headlamp-keycloak-runbook.md`](./superseded/05.operations/0005-headlamp-keycloak-runbook.md) | `docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md` | `runbook` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `53f410d549871d7b952c7f3fc0d3d745ac3fcebb` | `6befadcc168a6f3bef3c414ab27b6be88f93f7e9f26f8b3ee747f9993d3ad535` | 8 | [`docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | `superseded` |
| [`superseded/01.requirements/0005-workspace-document-assurance-modernization.md`](./superseded/01.requirements/0005-workspace-document-assurance-modernization.md) | `docs/01.requirements/0005-workspace-document-assurance-modernization.md` | `sdlc/requirement` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `5f47c5104c0195d9237c9353260b272c008a48ed` | `f719388aaa5eab9d4cdd4e26402e0a33f1463e6cb889f56537866ffae307ff9f` | 6 | [`docs/01.requirements/0003-workspace-agent-governance-platform.md`](../01.requirements/0003-workspace-agent-governance-platform.md) | `superseded` |
| [`superseded/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md`](./superseded/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md) | `docs/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md` | `sdlc/requirement` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `03dfeaf1e9771348e09071a92ae290234a165f2d` | `5a5658b59d93e91ab12bbdd687ec9128a32cf7fcf71630d7371ba114fc7f15e2` | 8 | [`docs/01.requirements/0003-workspace-agent-governance-platform.md`](../01.requirements/0003-workspace-agent-governance-platform.md) | `superseded` |
| [`superseded/01.requirements/0007-repository-delivery-and-platform-assurance.md`](./superseded/01.requirements/0007-repository-delivery-and-platform-assurance.md) | `docs/01.requirements/0007-repository-delivery-and-platform-assurance.md` | `sdlc/requirement` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `eeee654e76e8fdc67dc5425e2f7514ce19f0784f` | `0ae1a7c664784230e4dbfb220cc06819df7580a80f7041d72f78ac37238cd185` | 9 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`superseded/01.requirements/0008-workspace-document-taxonomy-consolidation.md`](./superseded/01.requirements/0008-workspace-document-taxonomy-consolidation.md) | `docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md` | `sdlc/requirement` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `39873ca978afad84d1cb10129c66b6c1f3424098` | `28ae25c1608db13f51c586c3b568d4d3c97356e9fce34125e685463da9ee77f7` | 8 | [`docs/01.requirements/0003-workspace-agent-governance-platform.md`](../01.requirements/0003-workspace-agent-governance-platform.md) | `superseded` |
| [`superseded/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md`](./superseded/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md) | `docs/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md` | `sdlc/architecture-description` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `09b6966e4915afd7c6e90c131ab095707ef6f97b` | `2c694a9adfa3192917505ec3fb8b3fdd9944545a1851bf6508c74c0d17049f3a` | 9 | [`docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | `superseded` |
| [`superseded/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md`](./superseded/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md) | `docs/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md` | `sdlc/architecture-description` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `02f09b51676305bae082cf8c685b462c85adf6fc` | `240aee6adaa9915d03070ebbecfe8c392947243623e335eeb4894401cae757a0` | 10 | [`docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | `superseded` |
| [`superseded/02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md`](./superseded/02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md) | `docs/02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md` | `sdlc/architecture-description` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `dd1d54ca4112c915753cee313aeec4f92a745cd2` | `2ca26c452cbc75bd5f7d1c5bdfee4cfe6f8f1c10d3555e8a7e5d3edea77a6b70` | 7 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`superseded/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md`](./superseded/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md) | `docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md` | `sdlc/architecture-description` | `89dc12df213849e3e591c3f52bde2b1d288f033b` | `9c03158b129e5b1f4e885af94d3129f87eb84052` | `a73c32d18bec1102b8103adc73e637cda073ef7b262d724a6115e3d8e93821ac` | 8 | [`docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | `superseded` |

검증 합계: repository aggregate archive records `25/25`, historical links `198/198`. immutable ARWB base corpus는 pinned `CUTOVER_BASE_COMMIT`에 대해 `ARCHIVE-FINITE-ADMISSION`이 증명하며, 삭제된 body는 digest-pinned WORK-107 ledger의 sealed row로 증명한다.

[MIG-0019](./migrations/0019-requirement-and-architecture-authority-transfer.md)는 이 추가 8개 source의
현재 의미 승계와 독립 봉인 provenance를 기록한다. 기존 WORK-107 payload와 목록은 수정하지 않는다.

[MIG-0020](./migrations/0020-stage00-agent-registry-authority-transfer.md)는
당시 retired `.agents/` registry와 schema의 Stage 00 successor 및 Git recovery provenance를 기록한다.

[MIG-0021](./migrations/0021-common-agent-authority-routing.md)는 공통 authority의 현재 소유자와
기존 전이의 퇴역한 중간 목적지를 연결한다. MIG-0009와 MIG-0020을 포함한 이전 봉인 원문과
archive-time replacement는 유지하고, 현재 목적지만 이 후속 전이로 합성한다.

현재 문서는 봉인 원장을 현재 owner처럼 라우팅하지 않고 이 index를 경유한다. 이 index는
아래 원장을 직접 연결하며, 현재 문서가 계보로 인용하는 나머지 원장은 `migrations/`에서
 artifact ID로 찾는다.
[MIG-0004](./migrations/0004-document-authority-convergence.md)는 document authority
수렴 시점의 경로 전이와 Git 복구 정보를,
[MIG-0009](./migrations/0009-governance-memory-retirement.md)는 거버넌스 memory
구조의 퇴역과 그 후속 소유자를 기록한다.

[Spec 0052 완료 패키지](./completed/03.specs/0052-document-taxonomy-consolidation/spec.md)는
Spec·Plan과 17개 Task를 원래 문서 타입과 완료 상태로 보존한다.
[MIG-0022](./migrations/0022-document-taxonomy-package-retention.md)는 이 패키지의
이전 경로와 Git 원문 복구 정보를 기록한다. 위 record manifest의 수치와는 별개다.

### Retention Catalog

첫 ADR-0038 disposition은 대체된 ADR-0032를 `superseded/`에 보존한다. 각 행은 record 하나와 Retention Envelope 하나를 명명한다.

| Disposition Record | Retention Envelope |
| --- | --- |
| [`superseded/02.architecture/decisions/0032-completed-and-terminal-document-retention.md`](./superseded/02.architecture/decisions/0032-completed-and-terminal-document-retention.md) | `223b773f7ac15b755906cc485a9700f23194a16e:docs/02.architecture/decisions/0032-completed-and-terminal-document-retention.md` |

## Authoring Workflow

### ADR-0038 Disposition

새 disposition은 다음 순서를 따른다.

1. 문서에 실제로 일어난 일(완료, 대체, 후속 없는 철회, 사고 종결, route 퇴역, scope 이동)과 현재 authority를 확정하고 family를 하나 고른다. disposition 승인을 해당 Task에 기록한다.
2. Retention class면 문서를 `docs/98.archive/<class>/<원래 stage 경로>`로 옮기고 원래 profile, identity, 종단 상태를 유지한다. 본문이 class가 요구하는 명명(promote 대상, 대체 문서, 철회 이유, 종결 증거와 corrective-work owner)을 갖는지 확인한다.
3. Route disposition이면 본문 없이 기록한다. `tombstones/`의 `archive/route-tombstone`(`TOMB-####`)은 `retired_route`, `successor`, `reason`을, `migrations/`의 `archive/scope-migration`(`MIG-####`)은 `moved_scope`와 `current_owner`를 명명한다.
4. Retention Catalog에 Retention Envelope `<commit>:<original path>` 한 개를 기록한다. blob, digest, branch SHA, redirect를 추가하지 않는다. lifecycle gate는 보존 본문의 envelope가 비교 base의 source object와 같은지, route disposition의 envelope가 비교 base의 그 route object와 같은지, scope migration이 옮긴 문서가 현재 상태와 identity를 유지하는지 확인한다. 보존 본문과 scope migration이 옮긴 문서는 상대 링크 재기준 외에 원본과 달라질 수 없으며, 같은 변경에서 함께 옮긴 문서 사이의 링크는 새 경로를 따른다. Stage 98에 들어간 보존 본문과 route record는 이후 어떤 변경도 수정하거나 제거할 수 없다.
5. 현재 consumer를 인용 규칙에 맞춘다. `superseded/` 인용은 후속 문서로, `retired/`·`tombstones/`·`migrations/` 인용은 현재 route로 바꾼다.
6. 디렉터리가 없으면 첫 구성원과 같은 변경에서 만든다.

### ADR-0032 Generation Procedure

아래 절차는 동결 generation의 record가 만들어진 방식을 기록한다. registry가 동결 record와 원장을 정확한 경로로만 분류하므로, 이 절차로 새 record를 만들 수 없다.

1. 현재 authority와 replacement를 먼저 확정하고 원본 경로 제거와 mirrored archive record 생성을 하나의 proposed snapshot으로 준비한다.
2. 원본은 working-tree text가 아니라 full source commit의 Git blob bytes로 복구한다.
3. 복구 blob을 stdout/stderr 비공개, 완전 redaction, 전용 detection exit code로 secret classifier에 통과시킨다. 탐지 또는 도구 오류는 fail-closed다.
4. Canonical archive form의 metadata를 채우고 marker 직후 exact blob bytes를 append한다. Payload의 줄바꿈과 final newline은 변경하지 않는다.
5. Production cutover validator로 immutable base 31/202를 그대로 확인하고, migration validator로 eligible-prefix pair, exact envelope/source/digest, unique original owner, reason-dependent replacement, additive historical links, aggregate index membership/count, source removal, current direct-link 부재를 확인한다.
6. 생성 후 record mutation·deletion·reactivation은 거부한다. 필요한 metadata repair는 별도 provenance repair 결정과 증거를 요구한다.

### Relative Link Rules

- Payload link는 archive 위치 기준으로 재계산하거나 수정하지 않는다.
- Historical validation은 `source_commit` tree에서 `original_path`를 base로 사용한다.
- 현재 문서가 archive로 링크할 수 있는 곳은 이 index, `completed/`, 역사 증거로서의 `resolved/`뿐이다. 그 밖의 family는 후속 문서나 현재 route를 인용하며, 동결 record는 identifier로 명명하고 이 index를 경유한다. 계보·출처 인용은 [Docs README](../README.md)의 Archive 참조 규칙을 따른다.
- 이 index가 동결 record inventory와 새 disposition의 Retention Catalog를 소유한다. 동결 generation의 Terminal ADR/문서에 있는 명시적 역사 인용은 원래 source를 가리킬 수 있지만 current authority를 부여하지 않는다.

## Related Documents

- [Docs README](../README.md)
- [Document Stage Routing](../../.agents/governance/document-authoring.md)
- [Archive Retention Decision](./superseded/02.architecture/decisions/0032-completed-and-terminal-document-retention.md)
- [Six-Disposition Archive Decision](../02.architecture/decisions/0038-six-disposition-archive-stage.md)
- [Tombstone Template](../99.templates/templates/archive/tombstone.template.md)
- [Route Tombstone Template](../99.templates/templates/archive/route-tombstone.template.md)
- [Scope Migration Template](../99.templates/templates/archive/scope-migration.template.md)
- [Template Routing Contract](../99.templates/README.md)
