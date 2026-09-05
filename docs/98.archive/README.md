# 98.archive

> 현재 구현 권한에서 제거된 `docs/01-05` 문서의 전체 원문과 provenance를 보존하는 비현재 archive stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`98.archive/`는 활성 스테이지를 떠난 문서를 보관하는 비현재 stage다. 네 개의 하위 디렉터리는 이름이 아니라 [ADR-0032](../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)가 registry의 종단 상태 분류에서 파생한 역할로 구분된다.

- `migrations/`는 경로 전이 자체를 봉인한 원장이다. `archive/migration` profile의 `sealed` 문서이며, 어떤 문서가 어디로 갔는지에 대한 유일한 기계 증거다.
- `completed/`는 끝까지 진행된 작업을 보관한다. 판정 근거는 replacement를 명명하지 않는 종단 상태이며, `done`과 끝난 패키지 안의 `cancelled`가 여기 해당한다. 보존 단위는 문서가 아니라 패키지이므로, 미종단 문서가 하나라도 있으면 패키지 전체가 활성 스테이지에 남는다.
- `superseded/`는 후속 문서가 대체한 문서의 record를 보관한다. 판정 근거는 종단 `superseded` 상태와 존재하는 replacement다.
- `tombstones/`는 끝난 패키지 없이 단독으로 끝난 문서의 record를 보관한다. 판정 근거는 `withdrawn`·`rejected`·`cancelled`·`retired`·`invalidated` 종단 상태와 replacement의 부재다.

`completed/`만 record가 아니라 문서 자체를 보관한다. ArchiveEnvelope가 없고, 자신의 profile과 종단 상태를 유지하며, 상대 링크 접두어만 보존 트리 기준으로 재기준된다. 바이트 동일성이 아니라 링크 대상 동일성이 보존 불변식이고, 원본 바이트는 각 행이 고정한 `source_commit`과 `source_blob`으로 Git에서 복원한다. 그 링크는 현재 결합이 아니라 역사 증거로 읽는다.

`superseded/`와 `tombstones/`는 봉인 record를 보관한다. 각 record의 ArchiveEnvelope payload와 source provenance는 보존되며, 현재 문서는 개별 record가 아니라 아래 index를 참조한다. 이 stage가 현재 보관한 25개 record는 모두 후속 문서를 명명하므로 전부 `superseded/`에 있고, `tombstones/`는 아직 구성원이 없다. 구성원이 없는 디렉터리도 역할을 유지하며, 이는 방치된 폴더가 아니라 올바른 공집합이다.

<!-- archive-manifest:v1 records=25 historical-links=198 -->

[MIG-0005: Codex/Claude 거버넌스 수렴](./migrations/0005-codex-claude-agent-governance-convergence.md)은
제거된 권한 소스의 Git 복구 tuple과 현재 후속 소유자, 변경하지 않은 역사 링크
소비자의 유한 집합을 기록한다. 일반 행마다 full-body snapshot이나 tombstone을
추가하지 않으며, 후속 소유자 없는 삭제는 이 Archive 조회 경계로 해석한다.

## Stage Contract

### In Scope

- `docs/01.requirements`부터 `docs/05.operations`까지에서 제거된 원문의 mirrored full-body record
- 활성 스테이지를 떠난 종단 문서의 보존본과 그 경로를 은퇴시킨 봉인 원장 행
- `original_path`, `original_type`, archive decision, source commit/blob, SHA-256 provenance
- source commit과 original path를 기준으로 해석하는 historical rendered links
- index-only current navigation과 immutable payload 검증

### Out of Scope

- 현재 SDLC 또는 operations authority. 보존본을 인용해도 그것이 현재가 되지는 않는다
- historical link를 현재 경로로 다시 쓰는 작업
- `mutable` 또는 `current` 상태 문서의 보관. 진행 중인 문서는 아무리 오래되어도 제자리에 남는다
- secret-bearing history의 일반 보존
- metadata 또는 payload를 조용히 수정하는 provenance repair

ArchiveEnvelope.v1 marker 다음 byte부터 EOF까지가 payload다. Closing delimiter는 없으며 validator는 Git blob identity, payload byte count, final newline, SHA-256, mirror path, replacement dependency를 함께 확인한다.

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
retired `.agents/` registry와 schema의 Stage 00 successor 및 Git recovery provenance를 기록한다.

## Authoring Workflow

1. 현재 authority와 replacement를 먼저 확정하고 원본 경로 제거와 mirrored archive record 생성을 하나의 proposed snapshot으로 준비한다.
2. 원본은 working-tree text가 아니라 full source commit의 Git blob bytes로 복구한다.
3. 복구 blob을 stdout/stderr 비공개, 완전 redaction, 전용 detection exit code로 secret classifier에 통과시킨다. 탐지 또는 도구 오류는 fail-closed다.
4. Canonical archive form의 metadata를 채우고 marker 직후 exact blob bytes를 append한다. Payload의 줄바꿈과 final newline은 변경하지 않는다.
5. Production cutover validator로 immutable base 31/202를 그대로 확인하고, migration validator로 eligible-prefix pair, exact envelope/source/digest, unique original owner, reason-dependent replacement, additive historical links, aggregate index membership/count, source removal, current direct-link 부재를 확인한다.
6. 생성 후 record mutation·deletion·reactivation은 거부한다. 필요한 metadata repair는 별도 provenance repair 결정과 증거를 요구한다.

### Relative Link Rules

- Payload link는 archive 위치 기준으로 재계산하거나 수정하지 않는다.
- Historical validation은 `source_commit` tree에서 `original_path`를 base로 사용한다.
- Current 문서는 `docs/98.archive/README.md`만 참조한다.
- 이 index가 record inventory를 소유한다. Terminal ADR/문서의 명시적 역사 인용은 원래 source를 가리킬 수 있지만 current authority를 부여하지 않는다.

## Related Documents

- [Docs README](../README.md)
- [Document Stage Routing](../00.agent-governance/policies/document-authoring.md)
- [Archive Record Decision](../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Tombstone Template](../99.templates/templates/archive/tombstone.template.md)
- [Template Routing Contract](../99.templates/README.md)
