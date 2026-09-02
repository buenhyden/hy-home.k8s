---
title: "Codex and Claude agent governance convergence"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-08-28"
artifact_id: "MIG-0005"
---

# MIG-0005: Codex and Claude Agent Governance Convergence

## Overview

This finite record preserves the reviewed authority removals for Spec0054 WP-003A.
Its source commit is recovery provenance, not a branch-current policy pin.
Changed prose and projections are merged, never claimed to be identical moves.
No original bodies or per-row tombstones are duplicated. MIG-0004 retains its
original source, target, document digest and mapping without modification.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": ".agents/GEMINI.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "4587b3fb0a585a70b5cda52013e5267b762da682",
    "content_sha256": "c24b8e3c0e345b01df94172a57d3270a1b058e345fb4129239dd6a7edf349ef5",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": ".agents/hooks.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "f5bcc2fa72cb3281bf5b1e4fa3911b7fd14f1344",
    "content_sha256": "1a8180c60868bb74de1a9223da2fd3ef2dc3297eeec2564282e188de1af2f922",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": ".agents/output-styles/hy-home-k8s.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/agent-execution.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "fbaea7e7892980a44ea8e80efe1efb6161e4abe5",
    "content_sha256": "967b256af043e8d9aba8e038e6b3c4245e85b6e5497b19d897835cb2ca0f4186",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": ".agents/rules/graphify.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/skills/knowledge-map/skill.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "4ab343cdb38d0c0e2da1f8a33dca3c1923acb7c5",
    "content_sha256": "d5a456956c17c05bce443cff9cab5969d7e45b922cc5735e953fca2bd464a008",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": ".agents/rules/workspace-rules.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/agent-execution.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "8ba3ae04c9c0ba8396ceed022206f70a549d123c",
    "content_sha256": "8a56daafa4d2efa38da045ae51478db1ee3acb8e2be0c3b5483f4a65755e7f90",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": ".agents/workflows/graphify.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/skills/knowledge-map/skill.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5eebd46120526ef97c12fe9d9a62980fc447d9c4",
    "content_sha256": "ea825fb542c00a2f21acf4f9caf1341eb7b8c41ea48a23f3f869d1216aba0899",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": ".agents/workflows/qa-cicd-workflow.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/quality.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "b60f713f204b9c571f09fe74e5e60a544fd2ebd7",
    "content_sha256": "77748cab744a032cc00c97eebdeb3e6c21184311d7ff0180b4d814c5f5cecf99",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": ".codex/hooks.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "e798e1c4ac89b3d2e91e2f6c3db8bf85857a4cae",
    "content_sha256": "8385873b3f0b5bfe017e2e5bfe3d87a5f334d464ff7fbc315ce5c27fc0ba76e6",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": ".gemini/agents/code-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/code-reviewer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "0f64ecf4a4477909eae8c3713d15dd99fd251f25",
    "content_sha256": "e238f4350416051b7301d98e07d4c3063e2fb966012dd7133e4cdfad6bc7e3cc",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/doc-writer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/doc-writer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "eb54af955a43493fc004a77b84814f08ab37b57d",
    "content_sha256": "f30e46f3557b1128f2ed9573b8622e990275fa7086e7ba1628906c4dfe30caeb",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/docs-researcher.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/docs-researcher.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "8b298c2902bd4465ba93c80d5e43e621cbbe163e",
    "content_sha256": "8fd21593771ba59d0e7a8b7467255a1f8a2b96d8cb831effd10283dea1740dbd",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/gitops-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/gitops-reviewer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "01e102cf2b260622de4e5fd271bf50623055d615",
    "content_sha256": "37d56071dd907bb8b86b41edefc00edc48911eb57c62a74c97376a97840b0ee4",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/incident-responder.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/incident-responder.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "9536e34789db7dbabee72b8cc2963326419a8c15",
    "content_sha256": "316a5707cf5dbde697b4444c12a584b2b747761c1e8eaa5021e4a8e9d25737e0",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/k8s-implementer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/k8s-implementer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "578a88affc4291cf1ccfe79a3ea94705f04228f8",
    "content_sha256": "2c0846562bb7aba3f3ed169602fb24fdde6851f24d3f5b7bcc13223eee5479ad",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/network-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/network-reviewer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "6d4260523e2d96cc6c494285a1f9fb55423fd7e9",
    "content_sha256": "a876db59e649c209ff119bd17585bfb201c8c21642ebdf77ff5956f03b7d3b48",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/observability-reviewer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/observability-reviewer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "f55444f062dc847c0fab9ea34cc739731984b901",
    "content_sha256": "6f0ba2dab44324bf9b76e896e515dac69c40dea834d68fe875ccc386ae9fb759",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/quality-engineer.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/quality-engineer.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "88aef2d5b3af400cf4b9008471f69c828f3d53de",
    "content_sha256": "7517e2119fd7c202b78f663ea72be21f2eeda83a7587f82a1e987b23ab2be663",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/security-auditor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/security-auditor.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "10b6d49cfd6f27ffa067bba2c084e802ec86a592",
    "content_sha256": "454f4ce055f5a7d4b01be10ddcb485ed28761e4a6fda549f6b4bc35782556200",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/supervisor.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/supervisor.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "6cea486faab92e6e3d6a1d5a35cd21a31771bf0d",
    "content_sha256": "9bbda521f819ace9a3b6a33c07918d92615d52fe2c0d2470d66998e3419a5ecc",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/agents/wiki-curator.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/agents/wiki-curator.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5aa22939a219aa248059042088dcc137c3696c36",
    "content_sha256": "e507f6555b6aefc334627e93e0c9ca3e7734561161118f4286e186af88c97dbb",
    "reason": "Retire unsupported projection; neutral role remains canonical."
  },
  {
    "legacy_path": ".gemini/settings.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "d99f92e7b8e3cce17d46d003831348399e3f159d",
    "content_sha256": "3e9aae6a65832de9dbed7fc878e3ac7d10593c6cd7786c408a6c1a6f7e53344e",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": "GEMINI.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "df1d5732b54bffe85f5deb5d2c1fcec1ea40a9e3",
    "content_sha256": "89ce3a90a59420058b987f298422c5f31c0e560985eafac15f0fd32a22d5f062",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-evaluations.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5c57b84756afb7c8e573664feaf56c53401139d7",
    "content_sha256": "d4b2f1369da80037d4e8a7d976c780c5c35a70a5ad42569d802e044d873a8ca8",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-evaluations.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/contracts/agent-registry.schema.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "6e32aa1dfb6f2f08927c69a2162634752f0a0857",
    "content_sha256": "d42907063a19c54969e0d7d37c7a24f4f3419c6f0d4640fd019bd0d442f19198",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-governance-closure.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "2f9709cca568d29218a045ae9526393d9865cc50",
    "content_sha256": "fb963446c423f4b8641a8d5bb95affb3dadfa40d7576b189d18691ba5c038fe4",
    "reason": "Retire duplicate current closure snapshot authority; the neutral registry owns the supported agent set."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-governance-closure.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/contracts/agent-registry.schema.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "2f3ae0d6fc63f6be18ee39d8ca95dc41e7829396",
    "content_sha256": "43f14a3d9d6203feaa72a07c220f793110e83d28b55c9467acf3ca276bbfa769",
    "reason": "Retire duplicate closure snapshot format; the registry schema owns the current agent contract."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-legacy-cutover.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "scripts/validate-agent-legacy-cutover.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "450f46c78e1ba530542e39c444393af987b36fdf",
    "content_sha256": "5d78bc4bde363769cd949824b5c39b044044ecb333e0dd6a82bc9cf28da53aa7",
    "reason": "Retire the duplicate legacy snapshot contract; the legacy validator retains unique current-consumer checks and RIA reads historical projections from validated recovery bytes."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "scripts/validate-agent-legacy-cutover.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "7c0173017734634766d4e7da9114b7baae6e38c6",
    "content_sha256": "a317502d95cf55642863bd8750f12ae88f88c14ce262c82baf509204b16f203b",
    "reason": "Retire the legacy snapshot schema as current authority; historical RIA interpretation retains its validated source schema through this recovery record."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-model-fitness.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "4ccffcf52ec85ab35330ddd74d8c2d0af39fc32a",
    "content_sha256": "d384f71ca268297261a63fc3b716afe4eaa5cc57b8031fc0d0e28a7e9985c398",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-model-fitness.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/contracts/agent-registry.schema.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "37f335b837a4ac0d91fbf8eca7e9c47bfafee37e",
    "content_sha256": "74169258e7f9b77c117d5884bd39f80877f508d6bceb0878b7f3da7745fa5047",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-roster-admission.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "d37f8d8fb781eecf1e222d2e84cb56751751964d",
    "content_sha256": "ab7c8ab3e496780822efcf8cc8377cba0ccea43bd1c29c478d91b5b4f9dc6347",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-roster-admission.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/contracts/agent-registry.schema.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "894e004714ef4b9ab9cf34ed69aaba90ef4b8fe2",
    "content_sha256": "365d1e4c64ba76a048dbfe567bcc8389904fab86240b4310a8ab1c7e8cf0afb3",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/harness-contract.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5d5dced672dd123a4a3a364792bfafde2c910fd4",
    "content_sha256": "45f28d7b322594ba40682e63e87967f5ce50907a64ec1b57742db4de8f07899c",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/harness-contract.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/contracts/agent-registry.schema.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "d1ab8c2adc32f3294928d11ffe7ef9c7a45a92a8",
    "content_sha256": "47045eee914eb30d4297951b61e79746a3accc19d51b02d9d54067f3ce0718e5",
    "reason": "Replace retired finite census contract with neutral registry authority."
  },
  {
    "legacy_path": "docs/00.agent-governance/harness-catalog.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "2a57aafc0c3b56a558291c0216a55c5eb4c65238",
    "content_sha256": "6673a7e7445b8ffdc69c547ac52e72e063595679c8b4bb6833c88362cbb32f98",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source. Human roles/README navigation is secondary, not an alternate machine successor."
  },
  {
    "legacy_path": "docs/00.agent-governance/model-policy.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/model-selection.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "7a8a6344d06fda45368e10adfa8e27634b0d521c",
    "content_sha256": "da4362a87ec7aa06b83c20a80cb651e5fd2ec51b4ac794df525d846afc3b30e8",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/providers/gemini.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "4881e23ad505d18d77cb7cb99b8eb40d8f9d0560",
    "content_sha256": "c20909baa7a4020d42cfdb42f0efaae3e6f9c35dc2e9658b1e12e4edb84f996e",
    "reason": "Retire unsupported provider or custom hook authority without a live successor; Archive lookup retains evidence."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/agentic.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/agent-execution.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "ec1bce0e59a1ff37e340458448eddcf0fcc1f2db",
    "content_sha256": "80535114c744abfae49797b09c0004221e3eb673173e01cce124c594f0643ac2",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/approval-boundaries.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/approval-and-safety.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "bcb517983160d603c635c73b03564c913b474109",
    "content_sha256": "90e067b5217bf10a035d9d4c88dee22e7dbb707735d245271f8a88eaf8476dc3",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/bootstrap.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/agent-execution.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "c1b8c04ce82a889819f50bfd4f6f4f45ff63c365",
    "content_sha256": "c8e996ca43c6c896fb88cd2922a5b28027610cdaaa9902ec3295d468b85ad2f8",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source. skills/work-lifecycle.md owns procedure, not an alternate machine successor."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/document-authoring.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/document-authoring.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5b7c1912af0463bb70b61958603e3f7a5b43bd8c",
    "content_sha256": "a19193452ae90a7718a202e8a294065e149ee76ac9a946444cba112b74228bb8",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/git-workflow.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/git.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "2bce3fa91063be4b4452ed76e0328e38abf12bde",
    "content_sha256": "e753bf880ee7ea88a6235a6b6449602fa2eae6bf3baad4355d320340f5c09ef2",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/persona.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/README.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "144116b343dda2dc4d331c98931df8171bc952ac",
    "content_sha256": "9cf5e7d485e5e9ffa8d96363161f3f86d7a6c13c85e711ed8072d068d7b64045",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/postflight-checklist.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/skills/work-lifecycle.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "96713bf77b994e28f3f88ffb2388bfb0f0bc6d10",
    "content_sha256": "42a9497059cfec48abd118f5c7bdd536b180c2e65e98a03ba5c32f2f7409c644",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/preflight-checklist.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/skills/work-lifecycle.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "5178f75f9b7a6ae89c8251995bd6b95327561b39",
    "content_sha256": "09743cdf1cebc4866526ebc3eed32a48975f92728be8f16e79f78b80f2822dd2",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/quality-standards.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/quality.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "9ed9d7951b6c003c5073466d9f2de7b160f53f3e",
    "content_sha256": "fd922d0b07fc25676b8f0eb6cf48bfc02357d2cd6b2efb02ea5ba0ad31fa520a",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/rules/standards.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/policies/agent-execution.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "6894e433e3287a2d46253ff2e5b210a291eaa38f",
    "content_sha256": "a4fd9b4871054d5748bc0d6ba6944d818e0dcac31d866d75fc4557f04afd3489",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/architecture.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/architecture.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "2ddd52d03249aaea7a2226b44948f2124dd89e42",
    "content_sha256": "d50c91942dca02042e879583f08f87fe9c7f66a1809e25ed1a6cc5df945b4352",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/backend.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/README.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "d9d5497836e37fb5acf8f7c09db547596e637c79",
    "content_sha256": "93824722e637d7695144b17fa6848b48cded0ace98651db727a5f2c7f72bdf07",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/docs.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/documentation.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "48b5e5b666de4ab84a05ee74d88f27feeb87b485",
    "content_sha256": "82c1f1ccbad1ce7b49e6158c69c17ba1b37c5b60f85805f8ff57efc2a75cf482",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/frontend.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/README.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "aacfad6846f3a118a94d54c708d766708bd896f4",
    "content_sha256": "833b27180a7642b17a7d585e468737429dd4b3964534841b7787af3c63e77db9",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/infra.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/infrastructure.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "4aa078c4bde16eec8fc1fd266d6bc08e05394139",
    "content_sha256": "7c07e72f283e9605c519fd9dbb26b4340f3e2a16c026d3516604eb1f037ee2d6",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/meta.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/supervision.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "a5b8694a10204cbdf34eac745d825fd96fd806a5",
    "content_sha256": "e7c3e5e1a5e4ec78ff1afccb12e861e37a1dfb6ea7c94704be6063e56ca59568",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/ops.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/operations.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "ec55818cd2fc17cc123bb34db4592138d08a0fe9",
    "content_sha256": "f903495dc137f40eb420816a70d0f3716bf166d75ba4b5dc1cc5bc68a5a2086a",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/product.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/README.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "7e929a610c9695c6b5b758a17361a840386fcded",
    "content_sha256": "a704c37c24fd926f4687b5461c2274c368bfa57f531efba5731d69fac6eb1be9",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/qa.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/quality.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "e13380b7e92d53ba17fe6a46ca3b0344a7edb6a0",
    "content_sha256": "6e9e9d2e3e2187bd24ad8644177ddaf74547cd610fde2b7bc44b91b30e6e45e3",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/scopes/security.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/roles/security.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "c137ddeb8069dadd47eff98d61a7078ac2a41131",
    "content_sha256": "0b80c48e9be036d235401b9b601fc435cf04cf64436a9e492c5429a28db9ea15",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "docs/00.agent-governance/subagent-protocol.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/skills/delegated-development.md",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "0e02eedc33ed33934c6c3750036e93fd92f365db",
    "content_sha256": "72545dbc7ed929e2f6d56690f8dc898869df39ac43f18ded579f06c2b15c9a6d",
    "reason": "Merge retired authority into its canonical successor; Git retains the exact prior source."
  },
  {
    "legacy_path": "tests/fixtures/agent-evaluations.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "58f536446868f557e69b5b45442cfa91191c1c4d",
    "content_sha256": "f092b000c713d0d1f7f00a59bd0733d4c31258197729e6d15645ba78f8d81b1b",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/fixtures/agent-governance-closure.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "tests/test_validate_agent_governance_closure.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "021c0d62be623323ef270e25c14589e2222d4fd2",
    "content_sha256": "65bf91f9970ff3583d3c70eceb74d21f3243f8eade89864a6f6a9354ba20cbdc",
    "reason": "Replace the finite closure snapshot fixture with focused behavioral coverage of the compatibility CLI and terminal registry owner."
  },
  {
    "legacy_path": "tests/fixtures/agent-harness-contract.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "38520fc936262570f00eeb25ab85023307df48ef",
    "content_sha256": "9263c011d494ad0e32ca7485fc4493e56ab027c9719adbcaebbc69220e93a5cf",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/fixtures/agent-harness-semantics.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "d11d407df47e0694eea467c6e5a425ce83b1b98b",
    "content_sha256": "66d472561a28c70336fb10e331e286f463cfe27cce3854f7eb6f39ced8519883",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/fixtures/agent-legacy-cutover.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "tests/test_validate_agent_legacy_cutover.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "c9e6aca21926aa69a6ed2a476992336ae3f904be",
    "content_sha256": "3f208c26840ab3755b2a73a6300c514792093d393e13e47e20abc876a9d4306d",
    "reason": "Replace the finite legacy occurrence fixture with behavioral tests for retired-file absence, current consumers, safe successors and proved historical dispositions."
  },
  {
    "legacy_path": "tests/fixtures/agent-model-fitness.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "7ac184e0535a463d5f737adbbfd9932752c94ae8",
    "content_sha256": "2299ed92a4c91f254e5677cc46beb7237fb1504c7809f689bc07854dd031e0fa",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/fixtures/agent-roster-admission.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "701808eaf1452eaaf43dd7fc682c70b483144887",
    "content_sha256": "d043d8ade8a284a7a4541d53b80705cf75f6eb9731c454a1e743f5fd2bad76d3",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/fixtures/agent-roster-currentness.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/registry.json",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "3137d7ea0e03475beb6165875c9b0d65252fea15",
    "content_sha256": "42885ab6e9e6f9103022115b31fd2de63e7bdb10b3ba8d2dd93f694f64f0cedb",
    "reason": "Retire duplicate snapshot fixture; registry owns current data."
  },
  {
    "legacy_path": "tests/test_validate_agent_evaluations.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "tests/test_validate_agent_registry.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "be5e3aeed66bcec3de233077703fa1e95154e756",
    "content_sha256": "755e79f87a0263acb6e4204d616c317eaff3450642a9d52c02718432025bb384",
    "reason": "Replace snapshot tests with registry-driven behavioral tests."
  },
  {
    "legacy_path": "tests/test_validate_agent_model_fitness.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "tests/test_validate_agent_registry.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "1f9e310b573e37301ae7748408845b01bd34df04",
    "content_sha256": "6ee94b60a6cd4664b5bd60760c66343797b8ebeccbecca087674ed1c57c859dd",
    "reason": "Replace snapshot tests with registry-driven behavioral tests."
  },
  {
    "legacy_path": "tests/test_validate_agent_roster_admission.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "tests/test_validate_agent_registry.py",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "3a5d561f778e036a1f0db6ed5732e792e4ed1cb7",
    "content_sha256": "5c602bc0dd9242f590dd98b543dedc27323f05e99ad2159541c01f99d9527f1f",
    "reason": "Replace snapshot tests with registry-driven behavioral tests."
  },
  {
    "legacy_path": ".github/ABOUT.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".github/README.md",
    "source_commit": "a3cf5836e46cb2e53f9ec5ddf4150559d2643d39",
    "source_blob": "3c220c744cc9b26c9c5536e1307fca8c40abfe11",
    "content_sha256": "5e42f947379a82552197a2c488a5a6daa872579bcb2474cff6f67ff7531af375",
    "reason": "Replace the retired GitHub repository description with the current README owner."
  },
  {
    "legacy_path": "docs/00.agent-governance/contracts/agent-role-semantics.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/registry.json",
    "source_commit": "a3cf5836e46cb2e53f9ec5ddf4150559d2643d39",
    "source_blob": "ede5dbde26fa6994dd3877ad995893be8736e2a4",
    "content_sha256": "6339793aa5078f9277e158280b326b65762f71d5201ae71079445f002322d206",
    "reason": "Replace the retired role-semantics contract with the registry terminal owner."
  },
  {
    "legacy_path": "scripts/validate-agent-role-semantics.py",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "scripts/validate-agent-harness-semantics.py",
    "source_commit": "a3cf5836e46cb2e53f9ec5ddf4150559d2643d39",
    "source_blob": "aa08e9505bef2679766025ca54bd3833f34131ec",
    "content_sha256": "3d6bff86733eb7ee8b1fc3ece7aa1c945740e5761b7e19c4b2799bd91e0d611f",
    "reason": "Replace the retired role-semantics validator with the current harness-semantics validator."
  },
  {
    "legacy_path": "tests/fixtures/agent-role-semantics.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/registry.json",
    "source_commit": "a3cf5836e46cb2e53f9ec5ddf4150559d2643d39",
    "source_blob": "ffb4098b05453fc6f523589ce2cd7ae8be6d3ae1",
    "content_sha256": "258cac3c86b58bc5fbcc0ecf1d642a985f0bc623573a1907e16b66dec63a07c4",
    "reason": "Replace the obsolete role-semantics fixture with the registry terminal owner."
  },
  {
    "legacy_path": "graphify-out/GRAPH_REPORT.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "870c2f2b0952282ebe165ff1e2fddc95e6d48222",
    "content_sha256": "a8e0a9fd32b810f2d8e510395eaf82686ad776abcff24615b5f40e027c3c4056",
    "reason": "Unmaintained generated output, no repository-owned reproduction procedure, removal with consumer-zero and Git recovery (not regeneration)."
  },
  {
    "legacy_path": "graphify-out/GRAPH_TREE.html",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "b97533670acef9469480bc45e43fffaee5cac470",
    "content_sha256": "aa27a81ee852215f3687790d89061c845944495dada53c44d3f9ca4ef3066539",
    "reason": "Unmaintained generated output, no repository-owned reproduction procedure, removal with consumer-zero and Git recovery (not regeneration)."
  },
  {
    "legacy_path": "graphify-out/graph.html",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "222ce556d1b236e22c81d2cfb4c32d793783b81e",
    "content_sha256": "7510de52ae1b72a7b9b430e387f06a8fa20dbac0a7783a9c16722d72ee285f0c",
    "reason": "Unmaintained generated output, no repository-owned reproduction procedure, removal with consumer-zero and Git recovery (not regeneration)."
  },
  {
    "legacy_path": "graphify-out/graph.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_blob": "300b4753e00998d56cff7c17a301f99af5bbf33c",
    "content_sha256": "69d6674c68beda78ac3337f38c702ec6e0eb41044ded54827574676e36161a66",
    "reason": "Unmaintained generated output, no repository-owned reproduction procedure, removal with consumer-zero and Git recovery (not regeneration)."
  }
]
```

## Recovery

Source commits must remain reachable from the current named durable branch ref;
at authoring this was `refs/heads/codex/spec-0054-authority-convergence`.
Run the root CLI with the record above:

```bash
python3 scripts/archive_recovery.py --record docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md --verify
```

Verification requires regular Git mode, exact commit/blob/digest, strict UTF-8,
bounded reads, unique cycle-free targets, and synchronized index/worktree bytes.
A deleted row without a successor resolves to Archive lookup, not an absent live
owner. Recover original bodies through each recorded Git commit and source path.

### Partial-content disposition

`docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
remains at its current path, with every section except the first 14-column
`Historical authored-document migration inventory` preserved. That table is
retired as an obsolete duplicated historical inventory with an obsolete
terminal-shape obligation. Its latest full source identity is:

```yaml
source_commit: "bb55a1ae93c9fc3017f64b5f2246af11442265d3"
source_blob: "57b25b3eb312107abe1f6dfc18d9222ee4145682"
content_sha256: "291a6f191e5ff9c84993599bed99def57389ee065d8cfe0f8d4aa5ac1af227e5"
```

This manual prose uses existing identity field names; it is not a new parsed
record schema. Git can replay the full historical source, but cannot certify
this prose-level partial-content disposition. The public generic `--record
--verify` command does not certify this human recovery note.

Only the following finite historical consumers are admitted. Their complete
bytes must equal the immutable source, including progress.md until WP012. An
ordinary rendered Migration disposition or the explicit source-backed typed
reference evidence below may admit a consumer. A done status, directory,
repeated token or future append grants no admission. Existing Stage90 snapshot
and retirement sources retain their independent pre-existing source protections.

<!-- archive-historical-consumers:v1 format=json -->

```json
[
  {
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "paths": [
      "docs/03.specs/0009-workspace-harness-research-pack/plan.md",
      "docs/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
      "docs/03.specs/0011-template-contract-governance-migration/plan.md",
      "docs/03.specs/0011-template-contract-governance-migration/spec.md",
      "docs/03.specs/0012-template-governance-audit-enhancement/plan.md",
      "docs/03.specs/0012-template-governance-audit-enhancement/spec.md",
      "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
      "docs/03.specs/0014-workspace-document-contract-normalization/plan.md",
      "docs/03.specs/0017-workspace-engineering-research-pack/spec.md",
      "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
      "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md",
      "docs/03.specs/0019-template-path-numbering-contract/plan.md",
      "docs/03.specs/0019-template-path-numbering-contract/spec.md",
      "docs/03.specs/0020-workspace-contract-governance-normalization/spec.md",
      "docs/03.specs/0024-observability-and-network-review-agents/plan.md",
      "docs/03.specs/0024-observability-and-network-review-agents/spec.md",
      "docs/03.specs/0025-governance-owner-and-roster-currentness/plan.md",
      "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md",
      "docs/03.specs/0031-affected-surface-agent-qa/spec.md",
      "docs/03.specs/0039-github-ci-qa-evidence/plan.md",
      "docs/03.specs/0040-contract-cutover-and-program-closure/plan.md",
      "docs/03.specs/0041-stage-00-agent-governance-contract/plan.md",
      "docs/03.specs/0042-provider-native-runtime-and-model-evidence/plan.md",
      "docs/03.specs/0043-agent-harness-loop-lifecycle/plan.md",
      "docs/03.specs/0044-agent-roster-evaluation-and-admission/plan.md",
      "docs/03.specs/0045-agent-governance-ci-qa-cutover/plan.md",
      "docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md",
      "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/plan.md",
      "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md",
      "docs/03.specs/0059-workspace-research-full-corpus-refresh/plan.md",
      "docs/03.specs/0059-workspace-research-full-corpus-refresh/spec.md",
      "docs/03.specs/0060-platform-currency-defect-closure/spec.md",
      "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md",
      "docs/90.references/audits/2026-08-09-wgia/ai-agents-integrated-and-role-specific-agents.md",
      "docs/90.references/audits/2026-08-09-wgia/ci-cd-github-actions-qa-and-validation.md",
      "docs/90.references/audits/2026-08-09-wgia/harness-loop-fixtures-scripts-and-blockers.md",
      "docs/90.references/audits/2026-08-09-wgia/security-and-approval-boundaries.md",
      "docs/90.references/audits/2026-08-09-wgia/workspace-purpose-governance-and-operating-contracts.md"
    ]
  },
  {
    "source_commit": "15b11453bf2ec4f8081d6588088dbce5c6e863b9",
    "paths": [
      "docs/00.agent-governance/memory/progress.md"
    ]
  },
  {
    "source_commit": "4932a8158ffbbc926093aee76322f0402ce465b6",
    "paths": [
      "docs/03.specs/0014-workspace-document-contract-normalization/spec.md",
      "docs/03.specs/0015-agent-governance-contract-normalization/plan.md",
      "docs/03.specs/0015-agent-governance-contract-normalization/spec.md",
      "docs/03.specs/0016-active-control-surface-governance-hardening/plan.md",
      "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md",
      "docs/03.specs/0020-workspace-contract-governance-normalization/plan.md",
      "docs/03.specs/0022-control-cloud-doc-normalization/plan.md",
      "docs/03.specs/0022-control-cloud-doc-normalization/spec.md",
      "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md"
    ]
  }
]
```

### Historical Reference Evidence

This optional block records two explicit source-backed kinds: a literal path
in its exact historical consumer and a rendered symlink view with its exact
historical identity. Typed view references are Archive lookup only, never
regular recovery payloads.

<!-- archive-historical-reference-evidence:v1 format=json -->

```json
[
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0009-workspace-harness-research-pack/plan.md",
    "legacy_path": "docs/00.agent-governance/harness-implementation-map.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
    "legacy_path": "docs/00.agent-governance/common-governance.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
    "legacy_path": "docs/00.agent-governance/harness-implementation-map.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "legacy_path": "docs/00.agent-governance/common-governance.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "legacy_path": "docs/00.agent-governance/harness-implementation-map.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "legacy_path": "docs/00.agent-governance/providers/agents-md.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0014-workspace-document-contract-normalization/plan.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0014-workspace-document-contract-normalization/spec.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "legacy_path": "docs/00.agent-governance/harness-implementation-map.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "legacy_path": "docs/00.agent-governance/providers/agents-md.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0022-control-cloud-doc-normalization/spec.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "legacy_path": ".github/ABOUT.md"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "legacy_path": "docs/00.agent-governance/contracts/agent-role-semantics.json"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "legacy_path": "scripts/validate-agent-role-semantics.py"
  },
  {
    "kind": "literal-path",
    "consumer_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "legacy_path": "tests/fixtures/agent-role-semantics.json"
  },
  {
    "kind": "symlink-view",
    "consumer_path": "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md",
    "legacy_path": ".claude/output-styles",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_mode": "120000",
    "source_blob": "dbc840e231ed432539d2dde33ea90bebccb31a78",
    "link_target": "../.agents/output-styles",
    "lookup_path": "docs/98.archive/README.md"
  },
  {
    "kind": "symlink-view",
    "consumer_path": "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md",
    "legacy_path": ".claude/workflows",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_mode": "120000",
    "source_blob": "5b7fab0e8c0470399cbd247d77b1095e7e1da2b6",
    "link_target": "../.agents/workflows",
    "lookup_path": "docs/98.archive/README.md"
  },
  {
    "kind": "symlink-view",
    "consumer_path": "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md",
    "legacy_path": ".codex/output-styles",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_mode": "120000",
    "source_blob": "dbc840e231ed432539d2dde33ea90bebccb31a78",
    "link_target": "../.agents/output-styles",
    "lookup_path": "docs/98.archive/README.md"
  },
  {
    "kind": "symlink-view",
    "consumer_path": "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md",
    "legacy_path": ".codex/workflows",
    "source_commit": "bb55a1ae93c9fc3017f64b5f2246af11442265d3",
    "source_mode": "120000",
    "source_blob": "5b7fab0e8c0470399cbd247d77b1095e7e1da2b6",
    "link_target": "../.agents/workflows",
    "lookup_path": "docs/98.archive/README.md"
  }
]
```
