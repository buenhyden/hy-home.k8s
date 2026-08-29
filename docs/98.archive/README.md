# 98.archive

> 현재 구현 권한에서 제거된 `docs/01-05` 문서의 전체 원문과 provenance를 보존하는 비현재 archive stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`98.archive/`는 typed `tombstones/<stage>/` 아래 17개의 `content/archive` record를 보관한다. ADR-0030에 따라 Git history가 기본 full-content archive이며, Stage 98은 README, Migration, 필요한 Tombstone만 두는 minimal lookup layer다. [`migrations/mig-0001-sdlc-taxonomy-convergence.md`](./migrations/mig-0001-sdlc-taxonomy-convergence.md)는 legacy path와 stable path를 잇는 exact 14-field, 93-to-93 `moved` ledger로 남으며, 그 stable path 76개의 body는 각 row의 `source_commit`과 `source_blob`으로 Git에서 복원한다. 각 record의 ArchiveEnvelope payload와 source provenance는 보존되며, 현재 문서는 개별 record가 아니라 이 index만 참조한다.

<!-- archive-manifest:v1 records=17 historical-links=133 -->

[MIG-0005: Codex/Claude 거버넌스 수렴](./migrations/0005-codex-claude-agent-governance-convergence.md)은
제거된 권한 소스의 Git 복구 tuple과 현재 후속 소유자, 변경하지 않은 역사 링크
소비자의 유한 집합을 기록한다. 일반 행마다 full-body snapshot이나 tombstone을
추가하지 않으며, 후속 소유자 없는 삭제는 이 Archive 조회 경계로 해석한다.

## Stage Contract

### In Scope

- `docs/01.requirements`부터 `docs/05.operations`까지에서 제거된 원문의 mirrored full-body record
- `original_path`, `original_type`, archive decision, source commit/blob, SHA-256 provenance
- source commit과 original path를 기준으로 해석하는 historical rendered links
- index-only current navigation과 immutable payload 검증

### Out of Scope

- 현재 SDLC 또는 operations authority
- historical link를 현재 경로로 다시 쓰는 작업
- secret-bearing history의 일반 보존
- metadata 또는 payload를 조용히 수정하는 provenance repair

ArchiveEnvelope.v1 marker 다음 byte부터 EOF까지가 payload다. Closing delimiter는 없으며 validator는 Git blob identity, payload byte count, final newline, SHA-256, mirror path, replacement dependency를 함께 확인한다.

## Document Index

아래 manifest는 17개 record의 source ownership과 digest를 모두 열거한다. `Historical Links`는 payload를 current tree가 아니라 각 `source_commit`과 `original_path` 문맥에서 해석한 local rendered link 수다. `` `null` `` replacement는 `completed-lineage` 또는 별도 current successor가 없는 `retired` record에 허용되며, 현재 closure owner와 archive navigation boundary는 migration-result ledger와 namespace registry가 별도로 기록한다.

| Archive Record | Original Path | Original Type | Source Commit | Source Blob | Payload SHA-256 | Historical Links | Current Replacement | Reason |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| [`tombstones/01.requirements/tmb-prd-legacy-513540c3ab7c8c7ec2d848170c3c6df85b1780a2126ad41cb61d550456cefcac.md`](./tombstones/01.requirements/tmb-prd-legacy-513540c3ab7c8c7ec2d848170c3c6df85b1780a2126ad41cb61d550456cefcac.md) | `docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `9b453b87ae9a6a005c019a61da4924f3e91622ef` | `b5a0300136b39fd1d712586b3b25699f07becfb0c98e58166f8b852d0faf6b81` | 7 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/01.requirements/tmb-prd-legacy-54087d753dd7edf618b1cd5a0ffad654f6511e117ff7eac1ac289792c20c1e4d.md`](./tombstones/01.requirements/tmb-prd-legacy-54087d753dd7edf618b1cd5a0ffad654f6511e117ff7eac1ac289792c20c1e4d.md) | `docs/01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `e0c5d1be8946798106f3e65ffd380096e2329fb2` | `50c643fd33eb0f1761c70eb1a1249e2493273f4533131927e85f37b5a993d343` | 4 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/01.requirements/tmb-prd-legacy-8b107a1a83eb2e477de7f3c7b1d63050cff935af0dcfbdeb1e2636dc4ee5de06.md`](./tombstones/01.requirements/tmb-prd-legacy-8b107a1a83eb2e477de7f3c7b1d63050cff935af0dcfbdeb1e2636dc4ee5de06.md) | `docs/01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md` | `prd` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `a84a9e9938ede202a2e83b9deea51edc059f03b8` | `8e05ad6d3a4b45fc098ad159008b48764144cb412bd37686596660844b74bb34` | 10 | [`docs/01.requirements/0004-current-local-gitops-platform.md`](../01.requirements/0004-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/02.architecture/tmb-adr-legacy-a19264e8c774c9843b1bd489e4ea13b089f9493ddcfe5716a88764e1b41e68ad.md`](./tombstones/02.architecture/tmb-adr-legacy-a19264e8c774c9843b1bd489e4ea13b089f9493ddcfe5716a88764e1b41e68ad.md) | `docs/02.architecture/decisions/0001-k3d-topology-and-network.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `1a18548c491852b8e18b4466fffd50a05f5360a9` | `532c0e570c33fd0931f6573ffb63f3f65d733499808488b5c69983488002628f` | 8 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`tombstones/02.architecture/tmb-adr-legacy-1cf8aa49bbb6bdca7c69c6f94881c636d25dc68b9aa298ecb854790d17f26548.md`](./tombstones/02.architecture/tmb-adr-legacy-1cf8aa49bbb6bdca7c69c6f94881c636d25dc68b9aa298ecb854790d17f26548.md) | `docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `894105d51d7d031ce38c8016b7708b4750600adf` | `01e4ad60363dc2d5bf73bf0e9c16b5d2f682f11698ac2f8966bc7fe30bfbdd84` | 5 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`tombstones/02.architecture/tmb-adr-legacy-78452949112de698bd6fa9205770c51f516c900f4e42f372912612de528eac9f.md`](./tombstones/02.architecture/tmb-adr-legacy-78452949112de698bd6fa9205770c51f516c900f4e42f372912612de528eac9f.md) | `docs/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `d35eaa0000d43cb887742a7d6173aafc4683a699` | `0226cbc4888c2f3dc6897739ba4d9b2e1c2b88c7f918ac72a7adfdb8bc1f19ab` | 6 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`tombstones/02.architecture/tmb-adr-legacy-6ec9a5d55b91e0e59d9b73f4c11ced53d7a3a290c5a88e704b4d6d7f733cfb34.md`](./tombstones/02.architecture/tmb-adr-legacy-6ec9a5d55b91e0e59d9b73f4c11ced53d7a3a290c5a88e704b4d6d7f733cfb34.md) | `docs/02.architecture/decisions/0007-kubernetes-dashboard-v3.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `7c7b4acb5bd68a08b415ca35683392acd701f9b5` | `a62c757f7566a601d0a948c4ecf17aa96b980346724436cba8d5eedd58835964` | 7 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`tombstones/02.architecture/tmb-adr-legacy-59ec4c1d612f19572a59abb443a1279f998584488a41f1adb3bece1081fe774e.md`](./tombstones/02.architecture/tmb-adr-legacy-59ec4c1d612f19572a59abb443a1279f998584488a41f1adb3bece1081fe774e.md) | `docs/02.architecture/decisions/0010-headlamp-replaces-dashboard.md` | `adr` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `97ed0e3ea6a200942fc11d97d67da133069ed048` | `b08ec274a09d2134208b3594482f5a4f197ce7afe5bde5e4289c363b063177ee` | 6 | [`docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | `superseded` |
| [`tombstones/02.architecture/tmb-ad-legacy-a9933ec86fcda902cce202655eaef15ff4131e1b8bf40a74a316368f2b80fe57.md`](./tombstones/02.architecture/tmb-ad-legacy-a9933ec86fcda902cce202655eaef15ff4131e1b8bf40a74a316368f2b80fe57.md) | `docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `9001b10b9657396fe85d6d7b98112dcc6b310e4f` | `cbf08950c2da952a6ca7feaa122085700c5984c5b177a97d90277f3fcca4b44b` | 7 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/02.architecture/tmb-ad-legacy-daf190279d9ffd8a110eee548317c0a8ae58b86ba21220f00427c0dcace9f7b1.md`](./tombstones/02.architecture/tmb-ad-legacy-daf190279d9ffd8a110eee548317c0a8ae58b86ba21220f00427c0dcace9f7b1.md) | `docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `37857c69bd334b3acc59705a701233a303c2bcb2` | `4a0902cee5048f2192e16c3688e9bf1e992e60fde4fe3865abb1fcd45767f59f` | 4 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/02.architecture/tmb-ad-legacy-61d107a63b02dcdfa33f43fbb8418afb7e4bcd4a3d83da0693b71b830da22bb8.md`](./tombstones/02.architecture/tmb-ad-legacy-61d107a63b02dcdfa33f43fbb8418afb7e4bcd4a3d83da0693b71b830da22bb8.md) | `docs/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md` | `ard` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `4d38947d216e84dfc9430f4f632966292b602017` | `dfc0cd13ede805828a19909b2e525648c892dea9fc25d505d7becf8c27acd6b2` | 9 | [`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`](../02.architecture/descriptions/0007-current-local-gitops-platform.md) | `superseded` |
| [`tombstones/03.specs/tmb-spec-legacy-013c5c6ed9d3a810044f6ce50eb9aa043472b2e3528bbdfa1810192682be76ac.md`](./tombstones/03.specs/tmb-spec-legacy-013c5c6ed9d3a810044f6ce50eb9aa043472b2e3528bbdfa1810192682be76ac.md) | `docs/03.specs/001-wsl-k3d-argocd-platform/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `814a42d68c3fe7f78cd6bf274ef08dfe662bb159` | `eb482d1d5ebb3815746815f3dc868ff1669d79b9a1effca53fd7347f55447298` | 15 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`tombstones/03.specs/tmb-spec-legacy-063f6e166f3ebfc9dbcce93b3ea6aa53438f58b75935fbda294e79d87c6b52f4.md`](./tombstones/03.specs/tmb-spec-legacy-063f6e166f3ebfc9dbcce93b3ea6aa53438f58b75935fbda294e79d87c6b52f4.md) | `docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `fc790ba116e35498a0527032c4c060600e087ac9` | `14eefadf9959c8f9d57167cdcffe41c02ac648c9389fa3a24ce50ad399f7b72d` | 10 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`tombstones/03.specs/tmb-spec-legacy-250a2ac6df411e9506f888dd0a0db7493990b3544b20cdfdbb086fa7233034cc.md`](./tombstones/03.specs/tmb-spec-legacy-250a2ac6df411e9506f888dd0a0db7493990b3544b20cdfdbb086fa7233034cc.md) | `docs/03.specs/003-platform-expansion/spec.md` | `spec` | `5e0221525450dbdacb585e6c98ade3f060ddc827` | `6d92ef1b7606fd20aeedd20cb5bb99c6a40d1dda` | `3363c2f0db122199ddf518fa144fbfdac036a1921df0042c2852055a55179d3b` | 21 | [`docs/03.specs/0008-current-local-gitops-platform/spec.md`](../03.specs/0008-current-local-gitops-platform/spec.md) | `superseded` |
| [`tombstones/03.specs/tmb-spec-legacy-aa76c31eb19898c6270484148791abad4d8b07b4323eaf949bddafb0b8e7097c.md`](./tombstones/03.specs/tmb-spec-legacy-aa76c31eb19898c6270484148791abad4d8b07b4323eaf949bddafb0b8e7097c.md) | `docs/03.specs/007-docs-governance-consistency/spec.md` | `spec` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `cc803905127970c28fbb343ee69d71c27e0184f4` | `2143740f6a4c670976992e99e7ca8b35cc49e252912916991840b4a862dcfcbb` | 2 | `null` | `superseded` |
| [`tombstones/05.operations/tmb-guide-legacy-292f0f96da3102684734a62842ee5c4d1e663f731921040911fa288a16163305.md`](./tombstones/05.operations/tmb-guide-legacy-292f0f96da3102684734a62842ee5c4d1e663f731921040911fa288a16163305.md) | `docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md` | `guide` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `5786ac6cb75eb9c86b34bd7d61c1866ec1f693bc` | `a114a4c6632776de96eff8630fd5e672cccb31ffe425332198e7d5a96a427e65` | 4 | [`docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | `superseded` |
| [`tombstones/05.operations/tmb-runbook-legacy-3c3f615242a98268abeac20385372ef3eafe9dd9680454d749d7ffb853cdbf4a.md`](./tombstones/05.operations/tmb-runbook-legacy-3c3f615242a98268abeac20385372ef3eafe9dd9680454d749d7ffb853cdbf4a.md) | `docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md` | `runbook` | `82f0e1922d9748a88b1487a32a59629ba523f408` | `53f410d549871d7b952c7f3fc0d3d745ac3fcebb` | `6befadcc168a6f3bef3c414ab27b6be88f93f7e9f26f8b3ee747f9993d3ad535` | 8 | [`docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | `superseded` |

검증 합계: repository aggregate archive records `17/17`, historical links `133/133`. immutable ARWB base corpus는 pinned `CUTOVER_BASE_COMMIT`에 대해 `ARCHIVE-FINITE-ADMISSION`이 증명하며, 삭제된 body는 digest-pinned WORK-107 ledger의 sealed row로 증명한다.

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
- 이 index만 개별 record를 inventory link로 열거할 수 있다.

## Related Documents

- [Docs README](../README.md)
- [Document Stage Routing](../00.agent-governance/policies/document-authoring.md)
- [Archive Record Decision](../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive Record Template](../99.templates/templates/archive/archive-record.template.md)
- [Template Routing Contract](../99.templates/README.md)
