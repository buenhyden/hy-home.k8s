---
title: "Common Agent Authority Routing"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "platform"
updated: "2026-09-06"
layer: "archive"
artifact_id: "MIG-0021"
---

# MIG-0021: Common Agent Authority Routing

## Overview

This finite recovery record applies ADR-0035 to the former Stage 00 authority
sources. It also closes the already retired intermediate endpoints left by
prior sealed transitions. These are semantic replacements because native
metadata and relative links evolve with their owners. Deleted unused forms
have no current successor and resolve to the Archive lookup boundary.

Earlier migration records, including MIG-0009 and MIG-0020, retain their complete
sealed bytes and archive-time replacement claims. The ordered migration graph
composes their destinations through this record; historical path strings are
source evidence and grant no authority to a retired tree. The current common
owner is `.agents/README.md`, with native provider notes in provider directories.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": ".agents/agents/code-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/code-reviewer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "6e2f9d44b323eab54d695be2c56b6cc9f8146d38",
    "content_sha256": "09e1304fb820036cb2d1948f9f906f0b47cb8e04d07457b60bf173a74f9e14a8",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/doc-writer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/doc-writer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "143644292cd3dc3f63e9abbd41751e689a12cef4",
    "content_sha256": "ac441955e675134e2c3c0cfcef505da76aa53ba4c86e8485d5b6c3541246c3a7",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/docs-researcher.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/docs-researcher.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "d02980295c779eef3224fc706a70db2318afcb0c",
    "content_sha256": "3656f8f16c5d7eb8fa5933ae777b16830560d11da321d58f273e061b1e4da6f5",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/gitops-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/gitops-reviewer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "1818e12d8b2f0d7e2f04b3b5b1f37b9881907612",
    "content_sha256": "60db92b4e43e30bc65a06a6a9a73d37d782974dcfbb0873e7cfd35475bb80e6a",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/incident-responder.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/incident-responder.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "a99c7c3377042a68193d6b8389a16a6f4baa6e08",
    "content_sha256": "f26445484279b91a23e2689d4f2dabb0406686c99382470551e153d8e44c0588",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/k8s-implementer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/k8s-implementer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "12ccae7ae67ce1b97489d7ed425fc22187b932f8",
    "content_sha256": "30a5483b6f08ba0e59c8b7f6e7b8280843316ff6018e9b69e760fadbaaf2ae06",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/network-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/network-reviewer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "2646a7367eb49e09d4b8ceb64d97d8035ee56696",
    "content_sha256": "7d9a12984c982615eaf88e37e79651878a80312b1044871fbcd8eefc891eb983",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/observability-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/observability-reviewer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "9aedb7c39d717be798e0e42180fa400ab924588b",
    "content_sha256": "4a6e5e4043b401af75332ac452445fb5c2d15296cb1868df8b0361c1e97ddff2",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/quality-engineer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/quality-engineer.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "d4a0e9772f4b88d16872c5d26a36ba75973d7ec5",
    "content_sha256": "9b85baa6f9582c4e18fd95efcdf4b4b89ee341f2012529829543520a54097402",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/security-auditor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/security-auditor.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "e3aa7c1fc820f4d6a94bd6f82e5792c85cfbcc9f",
    "content_sha256": "d716effda735b73036504e8d8f1123cca771a26af93c8faadf1cfe478fe8b01c",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/supervisor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/supervisor.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "a82787f67118e50b3492047342208b35d916f49b",
    "content_sha256": "59e2b80a786cd62090f70bb50e4024dbea98d20cd865f1df9c3dbdaea466cefb",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/agents/wiki-curator.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/wiki-curator.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "40e91256eae3167c5f5de2e31e3ad605eeebbbe7",
    "content_sha256": "f86b29351d9fc1e35cc796ac335d73dd614ab26bdd6babeeca7b000411126293",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".agents/skills/knowledge-map/skill.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/knowledge-map/SKILL.md",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "e264a9a5f467ed22bc7762656933c56f126831c8",
    "content_sha256": "250cff670cb3b7bcb9edc015a2867376ec499fb72d8858e44887f0fc9adb8271",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": ".github/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".github/repository-surface.md",
    "source_commit": "f1cb54cdec5e834cb2b4870d2bc9aaa0ccc740a1",
    "source_blob": "24a8f8f2d3ae554219d49b6723830d737a0b65a7",
    "content_sha256": "2628ac4c116c4921d4d2904cbab3886d50eaf267a17d25b28b06534fec70f920",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/README.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "1ff496f9c64fe7589e07d068b0ced7395c933f69",
    "content_sha256": "b2a1f1f8c35d2b1f768aded044ff46d97c6f315def769e2f8926554ef00ada83",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/agent-execution.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/agent-execution.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "428285d02fc1fec7a453a61615270a2de558f983",
    "content_sha256": "df3bbede034613cc8afd0757de0f76e85b0de5472593d48cfaaf56ebdfd9fca1",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/approval-and-safety.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/approval-and-safety.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9d3ee00c0af9442ba9d58c3f4977b940b5140071",
    "content_sha256": "8989021b17e52a2df05ff01493e69435dfcd62161b78419055a34c83ad14d26c",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/context-and-memory.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/context-and-memory.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "40b285669d877ea24719019ccc18b5becee13058",
    "content_sha256": "62bfd78f758e758e48971a1733a274e24c8804775a5b5ba97ef7af3e5665d32f",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/document-authoring.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/document-authoring.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "d752681dde279f45e899bf86feeb0e3f4ab53cbc",
    "content_sha256": "5c70553c3b3fa55b4dc8206db6e4d2cfb16302cd39f60482b8cbdfb14251e8cb",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/document-lifecycle.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/document-lifecycle.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "3432845a2b53f71bb7d8bd10a5ac97a7d047332e",
    "content_sha256": "9b1501d2ee3fd4a6caeb47536d0a8bdbb03251f2a72b07bdf3b572d37669b50f",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/formatting-and-linting.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/formatting-and-linting.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "dcfda25d8f700c61f59344a2700bc4325884e76d",
    "content_sha256": "21d5d302d5a3b423d87b758be6102c15d4c3fc55a12ea11885dae01e0ce94c70",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/git.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/git.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "eafe4798de0070a190191fb562b8e5ccd17cd824",
    "content_sha256": "86f3c1481282e81a46c87ce8db4989c4a41cd6d94d0bd5ccea2950f4b2fd6f70",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/model-selection.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/model-selection.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "4da8700c573c6dcb8be06ae4a8106d4c146933c8",
    "content_sha256": "ca7be00862f63d911074d66f6de61fa5f9c9f6204253cbaa4b00610b4f844cf2",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/policies/quality.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/quality.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "ba128225aa2fa41478246a5a20ae1196bc2ff9e4",
    "content_sha256": "238943cc556c0ba39769adb2913602e075c1d77bba4eaa328ecba528c1f372f5",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/providers/claude.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".claude/provider.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "50760a117f6bd163631e07a1ae0757f3ac702463",
    "content_sha256": "8f9c0860e57338984797edbfe74c05bdfba9392cbd331d09947f040e30a2736f",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/providers/codex.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".codex/provider.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "0bcd751afd22c146cf33c715d915c3f0aed9fa25",
    "content_sha256": "8d6dfa01791dac28bb88e47104230aada2c06c19ea36d988c84fc2521f92ab1a",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "2064f8c55cc5ea657934d016f774295634fbeae5",
    "content_sha256": "0a5fcaf266e12b96e5188ee585d9fc21ccff9189c463d70693caaf5afe41b066",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/architecture.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/architecture.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "fa05d5dc65695e86beb8daba882d7b92ce275aa9",
    "content_sha256": "1e8c4bd336fad9345e03e959ca0a89cb13707fdd2f2e4fd7dbac27393e1ec52e",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/code-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/code-reviewer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9bff7c572d2937057d7684fdf3836945768f9980",
    "content_sha256": "60c27c00f95272b5f67246354c3df3b80eaf1d1a0b8067bcbc8d0cd05cadc56d",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/doc-writer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/doc-writer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9d9062f666b15a35b1e04222a18f7ddde16d57ea",
    "content_sha256": "2ca61ec826825c1df3e048867d8a703bb57eff1e7505a6f2e3147a8db0e1e969",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/docs-researcher.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/docs-researcher.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "a58ef79870ab9b4c02db15d4bc5bf6e2d2f138cb",
    "content_sha256": "aad6fa2fa78b3930d8280c388ece991ecdd6cde629d2812d0378735a30f96ee3",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/documentation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/documentation.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "a273314742636fe9887e00b738788dd2009f537e",
    "content_sha256": "5f9171db33272e28a8ccf9fb6c802071d20bf2c2905bacc0302ffb7be7a6d298",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/gitops-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/gitops-reviewer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "5b2d89594e71adc5a881ed518219cc6bc0f58626",
    "content_sha256": "9c85e6dfe3dd3ca2819c14519bc0d9880bf89feec7e0a6f2b696412e2fd63291",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/incident-responder.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/incident-responder.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "23155c60765c091c6bf2bd50f190e6c6707f4161",
    "content_sha256": "07bd76eff7cac5bb9bb5491b3ad502fa955d3ac7389c35dd5914e6e0112269c7",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/infrastructure.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/infrastructure.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "992e8f3c3e8fc8cdc094fd95ed63526c9ad4c7c0",
    "content_sha256": "55d5259a008e19e943af1da3b20e7ba1a7315c60b5ccf4ec18aecfdbaafc35e5",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/k8s-implementer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/k8s-implementer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "0143369fa169524ee40171ea8083cb52cf6aac2f",
    "content_sha256": "fc4a284ee863a9145bfe3ac69caac121c0ae9affa58ac324f7a436c054c2bb95",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/network-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/network-reviewer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "ef25eb561875f932ff4c151bbddbcea59d9c0f1a",
    "content_sha256": "b36498539ba04b79b3a4d20c79421de7d1e44507e5c888a6d164a9e6c681f74d",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/observability-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/observability-reviewer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "780024c64918bd99e50ef18cb3d8e4b746ff3d33",
    "content_sha256": "d38bfdc006d3069cf86686ce164a37afe65053d1801a94241fcbed2883ca83f2",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/operations.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/operations.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "27aa31126e0b4da91bc02053921b2e4733add4e0",
    "content_sha256": "58e4b3b83b509f365caf270907d794ea90c98d887c2584683ac07bcb21ce4f10",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/quality-engineer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/quality-engineer.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9685cbf63ff818ab638e56337cf2f4415eb53169",
    "content_sha256": "2898fa82793eb89e44cd7927a0c3b827dc259f695dfedf3c8ec34abd0ed7f9d2",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/quality.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/quality.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "07d3f970f3de41cc1967e90b5e94d3cb726fbcd4",
    "content_sha256": "0af83663aa604a61d881c4281f9f1a3dfcbef648120a7639fb6fc7ef50c3f480",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/registry.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/registry.json",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "8f8a0705ebe4af666815d391f580f5e0c9e043c5",
    "content_sha256": "c362baed28845beb7af07b86c81e7536a19301fd53c72f683fce32720cfe6cbf",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/registry.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/registry.schema.json",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "2fdcdc0f69a09bfe8ec8c1a29e1c56e373831e5d",
    "content_sha256": "831999708f9b995d8de7bca15f8d3eabff9cf21ee9a131c7a8396f91b5a4cac6",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/security-auditor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/security-auditor.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "63fe5d2a433dd120fad68817e4ef39622cf06032",
    "content_sha256": "194285a2ada2d74c47dbd1b5140f8f00a1561d24dec6fa61df810be986b790aa",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/security.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/security.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "34f36c06d26f2164ed5e809e8edc31c840c41532",
    "content_sha256": "929f89bc55a817319cf53579e2b8ff6dbc0c6f4eda4e08df2957fb0d24c2f80d",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/supervision.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/supervision.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "764ba214c60ca2f3669685f80f0b302b2cbf23d3",
    "content_sha256": "182b52655730a315d5039b5c8dad389069fe2723edaeda3cc681dde7e7acbf68",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/supervisor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/supervisor.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "eca19319cfda4480dddfd06cd28c750958246417",
    "content_sha256": "2f03e16e5a5558df7d67cfdf5ff1045847d6b18b15d4f114bfc5d4663be00bcb",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/roles/wiki-curator.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/wiki-curator.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "d5f3240c1bb6ce2e48c0e4790fab7f4992d4435b",
    "content_sha256": "bbc6898e619028b2a5eeb238ba70cd2adc620e15c42b6dd87208d3bf29807c9c",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/sdlc.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/governance/sdlc.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "4b5531c8e423f37fd7613b5d77f2c2030c6ff23d",
    "content_sha256": "c32d0fbeff2bd8efd99ec7387c2055e15562f3a42cf0d4ec29baa3c074103660",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/delegated-development.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/workflows/delegated-development.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "207b53cb3938843e9fd2465d27f141a6300c812d",
    "content_sha256": "5f5034db41f3c8c6d0e6e9828028fc2c9a9924110ff61b6341a7514a7f67999e",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/deployment-strategies/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/deployment-strategies/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "f4586e9698dd2573698bfef5ff5635cbc7fece3d",
    "content_sha256": "9138211168c0c364a5c4d406588396d98c3661ef83dc2caaa8f8392cd4c0621d",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/docs-stage-conformance/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/docs-stage-conformance/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "b89abdd16c90ffb1a59fe763df746979c278df76",
    "content_sha256": "cd4e307f8b742f442dfd72f699c9b306a98abac4cd8baf4a057fd86958f5b2a2",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/docs-stage-routing/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/docs-stage-routing/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "ad266035d1330470f7cc87a0b25cf7fb10e29b83",
    "content_sha256": "31393c1fbab8ad964e143db739c605f1e20bb6917e1c9567e365aa6d472e6c79",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/execution-plan/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/execution-plan/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "86fea48d0946d85f3b9eb97a93a90617f3bf44bd",
    "content_sha256": "ba6b62496d5d335875437d795c9cee1fb5b48e35de5e22208eb69c4932185e9e",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/gitops-workflow/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/gitops-workflow/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "a163ab1edd8fe5a275b5fa1ce0641a950bfd6277",
    "content_sha256": "28bd6274b26ce47960673c222ef2fda5577d2d6356b9efb18f706a8161785808",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/incident-postmortem/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/incident-postmortem/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9570d16c8c7162140331a9b562025b5305997330",
    "content_sha256": "caf88342bb5c7df9b4fba16b5a2c7bca5cd7e8ac8ee04c3223cffddf45a268a7",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/k8s-security-audit/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/k8s-security-audit/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "9cb918e31b59fe2cdcacc8d715ab27c256001748",
    "content_sha256": "c74c609b1efc9701d94c46225f77cd5000d8384f1d9d18349c21442b0f38dd98",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/k8s-validate/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/k8s-validate/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "b90154d0a97bd9aa50e5f9b010363c8824f8db7b",
    "content_sha256": "b1c9f2dc91d9207fd7f03f50f13d9993833e3c5ce843a14a4dac5fa1eddc7562",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/knowledge-map/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/knowledge-map/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "5d28c01bcfa6f581dd3d298a1b04433a75b06a87",
    "content_sha256": "0c340437e9968b8579da08cba4e6b6244cfeda0cc295e7f963a370f230e3fdab",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/ops-runbook/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/ops-runbook/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "1d3a46b84c2bb5fc3866e66554953541d985089c",
    "content_sha256": "0adebc8653fa6662a2efa5f789775e3a799710ea93c0c0f164529b2ea9d61739",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/rca-methodology/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/rca-methodology/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "75c6c179eef75cef836a15c72a5787df69ca5d5f",
    "content_sha256": "4dea01e5dcf62beea49cd49b2e58c7fd1f559d80bcaca2dfe1345dab01061762",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/requirements-to-design/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/requirements-to-design/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "e9e371754687c73958cf71d235b715240d9ed25f",
    "content_sha256": "04727818cb4315ce40fe50a0c87e6e2b6c909acc374556d9f4352854412faf9e",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/risk-report/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/risk-report/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "eb8d2e8cfd0d2bf094d46065693c7cae4896d239",
    "content_sha256": "45b31185d2d1fd47f64a2a9f61f7f95fd942f774189ab13c07f332a196e8c8f7",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/task-breakdown/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/task-breakdown/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "583a6720704b1e85fb9b7339a314171ca8c59c38",
    "content_sha256": "c4603ef11f36f069f25ed5f04ec5641061ad15b941277ff86f0fb3ede343aa54",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/vulnerability-patterns/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/vulnerability-patterns/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "7db6a40b0a7faa5283aefc6e1bbdfb4f221fa2f9",
    "content_sha256": "2755c8830c88c79da2c2f14d922a9c51052e6b1053c6b8c65a13bfb35cfb8c61",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/work-lifecycle.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/workflows/work-lifecycle.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "edcf72fa12a6868867a03a119c6f134229233f37",
    "content_sha256": "0735125bd55c438e33b2e02a7b5239e063c6f34c25396a870fef8ae0e72106d3",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/skills/workspace-harness-audit/SKILL.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/skills/workspace-harness-audit/SKILL.md",
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "source_blob": "6ef80e5101b3c8ead4aedeefeda5dc8033cf468c",
    "content_sha256": "97596c92297b840b230cb6264ebb8dc5346d973bf5a837007823b7f0a3c1400e",
    "reason": "ADR-0035 transfers the active responsibility to its common or native provider owner."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/contracts/data-model.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "f4fbb29fe24e3e6f19707a0e37f67e17d5ab750c",
    "content_sha256": "df8e4e183d4e6069b005051ef384b75a2139661ae941ac088fa1c9b28cb3e1ea",
    "reason": "The unused native contract form was retired without a current replacement; preserve Git recovery through Archive lookup."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/contracts/openapi.template.yaml",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "7492ec59f553b1ecc7fedb945aace243d28a9149",
    "content_sha256": "aba7ee08fd3c45e63edbc0557911c86ea8b31a47f9afbc3016d2439c65ed1176",
    "reason": "The unused native contract form was retired without a current replacement; preserve Git recovery through Archive lookup."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/contracts/schema.template.graphql",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "f39499ce00d55b88e520400194a5eaad4c263386",
    "content_sha256": "cd6d8b531799d3fd617fe404b441f80c5ab7dc2893bd8519c5ad053c3037dd4a",
    "reason": "The unused native contract form was retired without a current replacement; preserve Git recovery through Archive lookup."
  },
  {
    "legacy_path": "docs/99.templates/templates/specs/contracts/service.template.proto",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "4596915862db5891dbee1046fc0a758bf49f8948",
    "source_blob": "2d9288896bb3c83e7a2ef08f049662cd6e290df1",
    "content_sha256": "b601274f4a078e14350e0d3694ad846544b266293d04764f68ac8decc7bca4b8",
    "reason": "The unused native contract form was retired without a current replacement; preserve Git recovery through Archive lookup."
  },
  {
    "legacy_path": "scripts/validate-agent-harness-semantics.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "scripts/validate-agent-governance.py",
    "source_commit": "fa3d5a9dcbb2afdc631ee10662dae6f733b080ee",
    "source_blob": "fc3bedebdcecf9372eaf972707383b5a8fe1fbb9",
    "content_sha256": "73b7ad0beaeb971e2dc4cca9df0e7b19898f3eba5ba51b0447db90f86cd51af7",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": "scripts/validate-agent-legacy-cutover.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "scripts/validate-agent-governance.py",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "12e7164511c7802499c1203c381606e56f79053c",
    "content_sha256": "3df451203d2d122620019e2fa4c625ed1960c89b7aa719a5fff0811a1b0b114c",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": "tests/test_validate_agent_governance_closure.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "tests/test_agent_governance.py",
    "source_commit": "e8bb831926b28c90639aed267d0c538857cffafc",
    "source_blob": "31a943001311d0a12d5f66bea9400f100c0a0c8f",
    "content_sha256": "74c46bf3d250e96245c276ae01f9c8a46939d87fbf252d1027842c5b2bf46b4d",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  },
  {
    "legacy_path": "tests/test_validate_agent_legacy_cutover.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "tests/test_agent_governance.py",
    "source_commit": "41f8144e7e791a0563863b0fe993fe6432499a81",
    "source_blob": "ac47ff514a57dfdc9190f5967851671d89357497",
    "content_sha256": "55039f9e834a4cd687899fad25a3d01d0f926e167236445b826f05da61e30bf5",
    "reason": "Close the already retired intermediate endpoint at its current responsibility owner."
  }
]
```

## Recovery

Each row binds a regular source blob in a full immutable commit retained by
the named repository branch history. Verify the record with
`python3 scripts/archive_recovery.py --record docs/98.archive/migrations/0021-common-agent-authority-routing.md --verify`.
The recovery validator checks durable reachability, exact blob and SHA-256,
source retirement, unique successor composition, and proposed index/worktree
parity. The reviewed migration remains a proposed seal until that logical
snapshot passes the existing validation lane; it does not authorize staging,
committing, provider discovery, or live execution.

<!-- archive-historical-consumers:v1 format=json -->

```json
[
  {
    "source_commit": "eb4fcfe3283115388d6eb1f31d56780b3e578f77",
    "paths": [
      "docs/98.archive/migrations/0009-governance-memory-retirement.md"
    ]
  }
]
```
