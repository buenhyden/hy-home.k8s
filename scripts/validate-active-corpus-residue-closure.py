#!/usr/bin/env python3
"""Validate the ACER-006 terminal residue, cardinality, and lifecycle closure."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from pathlib import PurePosixPath
from typing import Any

try:
    from scripts.archive_recovery import (
        ArchiveContractError,
        RecoveryResult,
        WORK107_MIGRATION_DOCUMENT_SHA256,
        WORK107_MIGRATION_PATH,
        parse_archive_envelope,
        parse_work107_migration_document,
    )
except ModuleNotFoundError:  # Direct execution from scripts/.
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        RecoveryResult,
        WORK107_MIGRATION_DOCUMENT_SHA256,
        WORK107_MIGRATION_PATH,
        parse_archive_envelope,
        parse_work107_migration_document,
    )


SCHEMA = "active-corpus-residue-closure.v1"
FIXED_INPUT_COMMIT = (
    "09682e9e8feaeed028bd06ef6d1733617c82029e"  # pragma: allowlist secret
)
LEDGER_PATH = "docs/90.references/data/active-corpus-residue-closure.json"
SCRIPT_PATH = "scripts/validate-active-corpus-residue-closure.py"
AGGREGATE_PATH = "scripts/validate-repo-quality-gates.sh"
# History pins the combined registry at this path; the WORK-105 base projection
# below reads it from a base commit, not from the index.
RETIRED_REGISTRY_PATH = "docs/99.templates/support/document-profiles.json"
PROFILE_REGISTRY_PATH = "docs/99.templates/registry.json"
ROUTE_CONTRACT_PATH = "docs/99.templates/contracts/route-contract.json"
TAXONOMY_MANIFEST_PATH = "scripts/document-taxonomy-migration.json"
TAXONOMY_SOURCE_COMMIT = (
    "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
)
TAXONOMY_MANIFEST_BLOB = (
    "d82466f99b093dc39092a3f36d1c55452a45a7ed"  # pragma: allowlist secret
)
FROZEN_MIGRATION_RESULTS_BLOB = (
    "b208c65d203d97b5921e676f33e31e9df44508d7"  # pragma: allowlist secret
)
TRANSITION_MIGRATION_RESULTS_BLOB = (
    "cc63874ad523e1a531d7aeee2c4e291d67ee80bf"  # pragma: allowlist secret
)
TRANSITION_AUTHORITY_BLOBS = {
    "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md": (
        "71cbadc7f0798137e4b57b61615e69561c9cd449",  # pragma: allowlist secret
        "b806d3ba8f7b1dbc25dee81c07c3b4ebc213d2fb",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md": (
        "100a7bbb5354ced8d140a434757e9ca8df9312ae",  # pragma: allowlist secret
        "d7130da27c94d7bdf8d79efa794f03d0014557df",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md": (
        "c74a491ab21f5969058415b1251ce4bb08b6be5a",  # pragma: allowlist secret
        "7c45166536061ca971391532c9e296ce44597e44",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md": (
        "ad701ae2c7913c83413ba887c0666db114cf50d1",  # pragma: allowlist secret
        "60b9c1021a9a2a4811d492de3aad2a82add59740",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md": (
        "1e8bc54d7761f82c1b469dcef68ecad870e93a7d",  # pragma: allowlist secret
        "56354ecbf722b55fc2f783df215d26caa6d108a5",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0012-argo-notifications-slack.md": (
        "4e08d6edfa7162495b630e6e15e87b627d5aca53",  # pragma: allowlist secret
        "04597c0f3c4e5c42d88a5a18383846cb49ec8c1f",  # pragma: allowlist secret
    ),
    "docs/03.specs/0011-template-contract-governance-migration/spec.md": (
        "9bb00469ff54a0c9d062c60628067704d4a2f459",  # pragma: allowlist secret
        "99e80929ac13720f646286ce2ea95b02c194672e",  # pragma: allowlist secret
    ),
    "docs/03.specs/0012-template-governance-audit-enhancement/spec.md": (
        "de80e461ef8940ff9faf343f97ff627c963fc022",  # pragma: allowlist secret
        "4fdef1a7385620dc2113b3bc1568d6a72ec7217e",  # pragma: allowlist secret
    ),
    "docs/03.specs/0013-workspace-document-governance-hardening/spec.md": (
        "024f0fe32f50aab9cc730be1e2b7b533e752c1d5",  # pragma: allowlist secret
        "ded396714e0d734908bac7126d21b7f5ecd7c211",  # pragma: allowlist secret
    ),
    "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md": (
        "62ac4e67cc9ee40352f6ac1bea7919796dd708cb",  # pragma: allowlist secret
        "3e7e9c44aba500a454db557c78279185ae4c84f2",  # pragma: allowlist secret
    ),
    "docs/03.specs/0017-workspace-engineering-research-pack/spec.md": (
        "4e72760d4eee9705c8b5e06abeef87e8c62cf82c",  # pragma: allowlist secret
        "ddbe2d692da2c709017d271ff3d713eeec600da2",  # pragma: allowlist secret
    ),
    "docs/03.specs/0019-template-path-numbering-contract/spec.md": (
        "6bf8321ccfccca8ff20287c49cfc05c919ba6038",  # pragma: allowlist secret
        "4d268e2cd2a53ed3f563e79b6b80741bce00b090",  # pragma: allowlist secret
    ),
    "docs/03.specs/0022-control-cloud-doc-normalization/spec.md": (
        "a610eddc3ecbf7a004f168236fbd65d969a40c00",  # pragma: allowlist secret
        "32a6cb6803ac213edb69a9c5337b382c99c83edb",  # pragma: allowlist secret
    ),
    "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md": (
        "143db84ebd7ab90185b817b837d3f54663028b27",  # pragma: allowlist secret
        "5317314ce90b59b9066ec5d0f44d6184563afe33",  # pragma: allowlist secret
    ),
    "docs/03.specs/0024-observability-and-network-review-agents/spec.md": (
        "11dd647ee9ad5188a150e5c48a7892c9ee227590",  # pragma: allowlist secret
        "6517c83a052ee5785c61877c3e0928b9b2260520",  # pragma: allowlist secret
    ),
    "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md": (
        "e9aa1662ff557714a578b618875561542223e20e",  # pragma: allowlist secret
        "b56d1b3d99e20db6a1491ef51cbe3fd376da0fff",  # pragma: allowlist secret
    ),
    "docs/03.specs/0026-document-contract-registry/spec.md": (
        "75be3a6c279bab217bab734110e18edda638e700",  # pragma: allowlist secret
        "4a97eedf1f76b367335bc8b7153c7f28b20031b5",  # pragma: allowlist secret
    ),
    "docs/03.specs/0027-template-contract-consolidation/spec.md": (
        "5cff6d0b94e962cd188287d56ccf22f6bba7e109",  # pragma: allowlist secret
        "89daed767234baa10b3a44ad7a24ed325c362135",  # pragma: allowlist secret
    ),
    "docs/03.specs/0028-readme-workspace-profiles/spec.md": (
        "9554783c31404c91cca0e5e52a0b019162bf0d5d",  # pragma: allowlist secret
        "0efdbe887101a2c5000f55e31daeb37a0a42dc56",  # pragma: allowlist secret
    ),
    "docs/03.specs/0029-semantic-document-validation/spec.md": (
        "a1fa5a0a28179946dccd16a8a6e349a46037ddc9",  # pragma: allowlist secret
        "ea1d54f47a7288ebbf5cff2d11e0c805dea3788d",  # pragma: allowlist secret
    ),
    "docs/03.specs/0030-authored-document-migration/spec.md": (
        "89c0ad1acdcf3135515dea58a563857418c87a5e",  # pragma: allowlist secret
        "8b443403fb044a529cfdcbe748d1ffdb6b879dfb",  # pragma: allowlist secret
    ),
    "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md": (
        "9eb2e5c48aa30f79beaadb535d1b10c15ffe3a84",  # pragma: allowlist secret
        "a2fe213c905ce2d79623f24d728e5b32776fd06a",  # pragma: allowlist secret
    ),
}
WORK105_BASE_COMMIT = (
    "a6fa1806364ea0472baaad0906e1b5e4ddac8602"  # pragma: allowlist secret
)
WORK105_REGISTRY_BLOBS = (
    "fc9ba039906ef240d076de5eeb6c584b681ae09f",  # pragma: allowlist secret
    "fd842f60e801a39435600f35a27f22e1c659f1bd",  # pragma: allowlist secret
)
WORK107_REGISTRY_BLOB = (
    "7182c40ab8ee6b40173b408ec2c366314916f1e3"  # pragma: allowlist secret
)
WORK108_REGISTRY_BLOB = (
    "ce8da8f205cee1bba075bef7b26079a0708324b1"  # pragma: allowlist secret
)
MIG2_REGISTRY_BLOB = (
    "cd5fda0aee923f6010d6cbd0cfbb9ff889149233"  # pragma: allowlist secret
)
# Consolidation merge: the registry declares audits/2026-08-09-wgia as the
# current reference pack, because that pack exists in the merged tree while the
# worktree's registry still named its retired predecessor.
MERGE_REGISTRY_BLOB = (
    "0ce925cfb58ca04d4177ab85779d2d8e4149dc96"  # pragma: allowlist secret
)
# Stage 99 contract split: the profile registry and the route contract replaced
# the combined file as the current authority, so each carries its own admitted
# state rather than sharing the retired file's allowlist.
PROFILE_REGISTRY_BLOB = (
    "0ed2033bf61a5ffec0608b91bfa95ddc510b77e9"  # pragma: allowlist secret
)
SPEC0062_PROFILE_REGISTRY_BLOB = (
    "b9aa815007b39e751b8fb98b0e88677234666af1"  # pragma: allowlist secret
)
ROUTE_CONTRACT_BLOB = (
    "8ae4cabcbd67dc9e7cb500989b6431e0e7e2b1af"  # pragma: allowlist secret
)
WORK105_AUTHORITY_BLOBS = {
    "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md": (
        "b806d3ba8f7b1dbc25dee81c07c3b4ebc213d2fb",  # pragma: allowlist secret
        "b806d3ba8f7b1dbc25dee81c07c3b4ebc213d2fb",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md": (
        "d7130da27c94d7bdf8d79efa794f03d0014557df",  # pragma: allowlist secret
        "d7130da27c94d7bdf8d79efa794f03d0014557df",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md": (
        "e70dd6126fcab9c36a1a77cb839bf1059e44d4ff",  # pragma: allowlist secret
        "e70dd6126fcab9c36a1a77cb839bf1059e44d4ff",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0008-istio-install-and-ingress-coexist.md": (
        "7aa77303c5217c624e3bfe88a0c9a182283164c2",  # pragma: allowlist secret
        "7aa77303c5217c624e3bfe88a0c9a182283164c2",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0009-kiali-external-observability.md": (
        "48c24f79994c201ebc3e087d7764bd023bead95a",  # pragma: allowlist secret
        "48c24f79994c201ebc3e087d7764bd023bead95a",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md": (
        "56354ecbf722b55fc2f783df215d26caa6d108a5",  # pragma: allowlist secret
        "56354ecbf722b55fc2f783df215d26caa6d108a5",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0012-argo-notifications-slack.md": (
        "04597c0f3c4e5c42d88a5a18383846cb49ec8c1f",  # pragma: allowlist secret
        "04597c0f3c4e5c42d88a5a18383846cb49ec8c1f",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md": (
        "7c45166536061ca971391532c9e296ce44597e44",  # pragma: allowlist secret
        "7c45166536061ca971391532c9e296ce44597e44",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md": (
        "60b9c1021a9a2a4811d492de3aad2a82add59740",  # pragma: allowlist secret
        "60b9c1021a9a2a4811d492de3aad2a82add59740",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0015-declarative-document-contract-registry.md": (
        "7e09132e1a1278d96f4d9f1a0e57987144f21e65",  # pragma: allowlist secret
        "7e09132e1a1278d96f4d9f1a0e57987144f21e65",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0016-program-to-tranche-document-lineage.md": (
        "81c164b7a4a81e8cbd922597cff813528ab23d5f",  # pragma: allowlist secret
        "81c164b7a4a81e8cbd922597cff813528ab23d5f",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0017-program-follow-up-lineage-semantics.md": (
        "21c66759821e260621bde510574a58f4fe6b4de4",  # pragma: allowlist secret
        "21c66759821e260621bde510574a58f4fe6b4de4",  # pragma: allowlist secret
    ),
    "docs/02.architecture/decisions/0018-full-body-archive-record-and-retention.md": (
        "96daabd4098215e403237e016e771522c647bf4a",  # pragma: allowlist secret
        "0d1ae80fc1bad299491f9ab9dee49eddd472c6e8",  # pragma: allowlist secret
    ),
    "docs/03.specs/0009-workspace-harness-research-pack/spec.md": (
        "96ee4d63145234876145e0413d69b97b79b6823f",  # pragma: allowlist secret
        "0d647406d89fac9d975fd90fcee60daf4e5f382e",  # pragma: allowlist secret
    ),
    "docs/03.specs/0010-workspace-harness-implementation-audit-pack/spec.md": (
        "e485cd00e7c9766ebc2dad849cf719431f72c2c0",  # pragma: allowlist secret
        "797ce6835fe9d3327c7d6d657285179f5ca2aed7",  # pragma: allowlist secret
    ),
    "docs/03.specs/0011-template-contract-governance-migration/spec.md": (
        "99e80929ac13720f646286ce2ea95b02c194672e",  # pragma: allowlist secret
        "f14252c749ebf5a2001ac983ad012faef8972459",  # pragma: allowlist secret
    ),
    "docs/03.specs/0012-template-governance-audit-enhancement/spec.md": (
        "4fdef1a7385620dc2113b3bc1568d6a72ec7217e",  # pragma: allowlist secret
        "1b32064ab90fc30869c1b2b7ba69eaf7fa903c02",  # pragma: allowlist secret
    ),
    "docs/03.specs/0013-workspace-document-governance-hardening/spec.md": (
        "ded396714e0d734908bac7126d21b7f5ecd7c211",  # pragma: allowlist secret
        "4e3917e985c51bc4072d6528efea6d2bea0f6756",  # pragma: allowlist secret
    ),
    "docs/03.specs/0014-workspace-document-contract-normalization/spec.md": (
        "59a40eea737b1184340d41de2f94f9782c1f7a22",  # pragma: allowlist secret
        "3e18d32212b2c2f539230878f7bd675ba1316556",  # pragma: allowlist secret
    ),
    "docs/03.specs/0015-agent-governance-contract-normalization/spec.md": (
        "2651fd2638387e784c7579129b0862dab90048e6",  # pragma: allowlist secret
        "7d1c6e678a037a3d2b5e8f82e70f12895ae05cbc",  # pragma: allowlist secret
    ),
    "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md": (
        "3e7e9c44aba500a454db557c78279185ae4c84f2",  # pragma: allowlist secret
        "52ae3a2dc3f8fb4c1afb94145169a24464ad17d3",  # pragma: allowlist secret
    ),
    "docs/03.specs/0017-workspace-engineering-research-pack/spec.md": (
        "ddbe2d692da2c709017d271ff3d713eeec600da2",  # pragma: allowlist secret
        "c0ff46070bd2d66ffc7cc00f233c7119514601a4",  # pragma: allowlist secret
    ),
    "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md": (
        "d688e3ed234ab264711a7949d2e05f1d5df2fcc7",  # pragma: allowlist secret
        "d6fb204999d69de6d39c0d0781cba6028da34394",  # pragma: allowlist secret
    ),
    "docs/03.specs/0019-template-path-numbering-contract/spec.md": (
        "4d268e2cd2a53ed3f563e79b6b80741bce00b090",  # pragma: allowlist secret
        "4d268e2cd2a53ed3f563e79b6b80741bce00b090",  # pragma: allowlist secret
    ),
    "docs/03.specs/0020-workspace-contract-governance-normalization/spec.md": (
        "396a84f8e2de773ebb14bfda10c87db288779274",  # pragma: allowlist secret
        "4a11955b4e6dcbc27cefcc0d3e6da3810d8cd4d9",  # pragma: allowlist secret
    ),
    "docs/03.specs/0021-sdlc-lifecycle-contract/spec.md": (
        "e877cb560bd95fecc0c7d205c31484461a8f0c2a",  # pragma: allowlist secret
        "a0b6e71e44681af8894201ded088e478e747c9b5",  # pragma: allowlist secret
    ),
    "docs/03.specs/0022-control-cloud-doc-normalization/spec.md": (
        "32a6cb6803ac213edb69a9c5337b382c99c83edb",  # pragma: allowlist secret
        "ecab2fbd99d04d8d0d4f93f9f73d6e94afb03596",  # pragma: allowlist secret
    ),
    "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md": (
        "5317314ce90b59b9066ec5d0f44d6184563afe33",  # pragma: allowlist secret
        "b513c7f9b57b4fcaaaf4e4fb4c217a9bca055e29",  # pragma: allowlist secret
    ),
    "docs/03.specs/0024-observability-and-network-review-agents/spec.md": (
        "6517c83a052ee5785c61877c3e0928b9b2260520",  # pragma: allowlist secret
        "5f7a85c5c2020ce70b7e0ba6189be6331b4ff0a5",  # pragma: allowlist secret
    ),
    "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md": (
        "b56d1b3d99e20db6a1491ef51cbe3fd376da0fff",  # pragma: allowlist secret
        "1b75d59969a221d99ba4630feabd0b7b81a8a9fa",  # pragma: allowlist secret
    ),
    "docs/03.specs/0026-document-contract-registry/spec.md": (
        "4a97eedf1f76b367335bc8b7153c7f28b20031b5",  # pragma: allowlist secret
        "67d158839089e16a4a32fd0b79f5dc4ae9c58b1a",  # pragma: allowlist secret
    ),
    "docs/03.specs/0027-template-contract-consolidation/spec.md": (
        "89daed767234baa10b3a44ad7a24ed325c362135",  # pragma: allowlist secret
        "cae6322df3505482c790ed1f80b53000c2c3f072",  # pragma: allowlist secret
    ),
    "docs/03.specs/0028-readme-workspace-profiles/spec.md": (
        "0efdbe887101a2c5000f55e31daeb37a0a42dc56",  # pragma: allowlist secret
        "7d5439be1e77822e199ba4e94e3726f893a2a211",  # pragma: allowlist secret
    ),
    "docs/03.specs/0029-semantic-document-validation/spec.md": (
        "ea1d54f47a7288ebbf5cff2d11e0c805dea3788d",  # pragma: allowlist secret
        "20cf40876fff650874c8c818a9316e021d696020",  # pragma: allowlist secret
    ),
    "docs/03.specs/0030-authored-document-migration/spec.md": (
        "8b443403fb044a529cfdcbe748d1ffdb6b879dfb",  # pragma: allowlist secret
        "17b6ef6558878d88935d86218db5b2e3095b8cd1",  # pragma: allowlist secret
    ),
    "docs/03.specs/0031-affected-surface-agent-qa/spec.md": (
        "8314414e34d733e20d40536eb91b015d0c3e894b",  # pragma: allowlist secret
        "8130910b7c2a6d0e5e6e359a4c82bfa0fbce6533",  # pragma: allowlist secret
    ),
    "docs/03.specs/0032-protected-surface-supply-chain-hardening/spec.md": (
        "70cc3eb48e65de90a027f5a81e79c616fcf6c4da",  # pragma: allowlist secret
        "770b2ebac8591e61fb10c61bd820cd716d059a03",  # pragma: allowlist secret
    ),
    "docs/03.specs/0033-template-lifecycle-contract-normalization/spec.md": (
        "1bba28ab3cf65fc7fd3092f12ff53cc685a8398e",  # pragma: allowlist secret
        "9a5165c12d3a85cdc86cdc2c12bef26c7dd3cee4",  # pragma: allowlist secret
    ),
    "docs/03.specs/0034-authority-and-lineage-foundation/spec.md": (
        "84ebd53683214bbc2ce5f61037cea8121094b2a7",  # pragma: allowlist secret
        "a2edacfff567ae42c7edd54abfe12649c6ffd05a",  # pragma: allowlist secret
    ),
    "docs/03.specs/0035-document-schema-and-lifecycle-contract/spec.md": (
        "f217827d5867166c1a0b9ff38542caffa5618394",  # pragma: allowlist secret
        "195c8f66b9f1818e00a0729b0472445d190a0414",  # pragma: allowlist secret
    ),
    "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md": (
        "20b7bddc865cd7f18129e9cdf02b21944a3720dd",  # pragma: allowlist secret
        "c09228aba4c6dd3c7e859f33c55ef184c19cf30d",  # pragma: allowlist secret
    ),
    "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md": (
        "a2fe213c905ce2d79623f24d728e5b32776fd06a",  # pragma: allowlist secret
        "e359fb94010faa1c947521879737bf8c0dded22c",  # pragma: allowlist secret
    ),
}
WORK105_HISTORICAL_PATHS_BY_CURRENT = {
    path: (
        path.replace("docs/03.specs/0", "docs/03.specs/", 1)
        if path.startswith("docs/03.specs/")
        else path
    )
    for path in WORK105_AUTHORITY_BLOBS
}
WORK105_CURRENT_PATHS_BY_HISTORICAL = {
    historical: current
    for current, historical in WORK105_HISTORICAL_PATHS_BY_CURRENT.items()
}
WORK105_BASE_PATHS = (
    RETIRED_REGISTRY_PATH,
    *sorted(WORK105_CURRENT_PATHS_BY_HISTORICAL),
)
TRANSITION_AUTHORITY_REMAPS = {
    "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md": (
        (
            "docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md",
            "docs/98.archive/README.md#document-index",
        ),
    ),
    "docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md": (
        (
            "docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md",
            "docs/98.archive/README.md#document-index",
        ),
    ),
    "docs/02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md": (
        (
            "docs/04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md",
            "docs/03.specs/004-argo-rollouts-progressive-delivery/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md",
            "docs/03.specs/004-argo-rollouts-progressive-delivery/tasks.md",
        ),
    ),
    "docs/02.architecture/decisions/0012-argo-notifications-slack.md": (
        (
            "docs/04.execution/plans/2026-05-18-argo-notifications-slack.md",
            "docs/03.specs/005-argo-notifications-slack/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-05-18-argo-notifications-slack.md",
            "docs/03.specs/005-argo-notifications-slack/tasks.md",
        ),
    ),
    "docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md": (
        (
            "docs/04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md",
            "docs/98.archive/README.md#document-index",
        ),
        (
            "docs/04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md",
            "docs/98.archive/README.md#document-index",
        ),
    ),
    "docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md": (
        (
            "docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md",
            "docs/98.archive/README.md#document-index",
        ),
    ),
    "docs/03.specs/0011-template-contract-governance-migration/spec.md": (
        (
            "docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md",
            "docs/03.specs/0011-template-contract-governance-migration/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md",
            "docs/03.specs/0011-template-contract-governance-migration/tasks.md",
        ),
    ),
    "docs/03.specs/0012-template-governance-audit-enhancement/spec.md": (
        (
            "docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md",
            "docs/03.specs/0012-template-governance-audit-enhancement/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md",
            "docs/03.specs/0012-template-governance-audit-enhancement/tasks.md",
        ),
        (
            "docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md",
            "docs/03.specs/0012-template-governance-audit-enhancement/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md",
            "docs/03.specs/0012-template-governance-audit-enhancement/tasks.md",
        ),
    ),
    "docs/03.specs/0013-workspace-document-governance-hardening/spec.md": (
        (
            "docs/04.execution/plans/2026-07-03-workspace-document-governance-hardening.md",
            "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md",
            "docs/03.specs/0013-workspace-document-governance-hardening/tasks.md",
        ),
    ),
    "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md": (
        (
            "docs/04.execution/plans/2026-07-04-active-control-surface-governance-hardening.md",
            "docs/03.specs/0016-active-control-surface-governance-hardening/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md",
            "docs/03.specs/0016-active-control-surface-governance-hardening/tasks.md",
        ),
    ),
    "docs/03.specs/0017-workspace-engineering-research-pack/spec.md": (
        (
            "docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md",
            "docs/98.archive/README.md#document-index",
        ),
        (
            "docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md",
            "docs/98.archive/README.md#document-index",
        ),
        (
            "docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md",
            "docs/03.specs/0017-workspace-engineering-research-pack/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md",
            "docs/03.specs/0017-workspace-engineering-research-pack/tasks.md",
        ),
    ),
    "docs/03.specs/0019-template-path-numbering-contract/spec.md": (
        (
            "docs/04.execution/plans/2026-07-05-template-path-numbering-contract.md",
            "docs/03.specs/0019-template-path-numbering-contract/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md",
            "docs/03.specs/0019-template-path-numbering-contract/tasks.md",
        ),
    ),
    "docs/03.specs/0022-control-cloud-doc-normalization/spec.md": (
        (
            "docs/04.execution/plans/2026-07-06-control-cloud-doc-normalization.md",
            "docs/03.specs/0022-control-cloud-doc-normalization/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-06-control-cloud-doc-normalization.md",
            "docs/03.specs/0022-control-cloud-doc-normalization/tasks.md",
        ),
    ),
    "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md": (
        (
            "docs/04.execution/plans/2026-07-06-stage03-04-repo-static-gap-closure.md",
            "docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md",
        ),
        (
            "docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md",
            "docs/03.specs/0017-workspace-engineering-research-pack/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md",
            "docs/03.specs/0017-workspace-engineering-research-pack/tasks.md",
        ),
    ),
    "docs/03.specs/0024-observability-and-network-review-agents/spec.md": (
        (
            "docs/04.execution/plans/2026-07-06-observability-and-network-review-agents.md",
            "docs/03.specs/0024-observability-and-network-review-agents/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-06-observability-and-network-review-agents.md",
            "docs/03.specs/0024-observability-and-network-review-agents/tasks.md",
        ),
    ),
    "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md": (
        (
            "docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md",
            "docs/03.specs/0025-governance-owner-and-roster-currentness/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md",
            "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks.md",
        ),
    ),
    "docs/03.specs/0026-document-contract-registry/spec.md": (
        (
            "docs/04.execution/plans/2026-07-12-document-contract-registry.md",
            "docs/03.specs/0026-document-contract-registry/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-12-document-contract-registry.md",
            "docs/03.specs/0026-document-contract-registry/tasks.md",
        ),
    ),
    "docs/03.specs/0027-template-contract-consolidation/spec.md": (
        (
            "docs/04.execution/plans/2026-07-12-template-contract-consolidation.md",
            "docs/03.specs/0027-template-contract-consolidation/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md",
            "docs/03.specs/0027-template-contract-consolidation/tasks.md",
        ),
    ),
    "docs/03.specs/0028-readme-workspace-profiles/spec.md": (
        (
            "docs/04.execution/plans/2026-07-12-readme-workspace-profiles.md",
            "docs/03.specs/0028-readme-workspace-profiles/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-12-readme-workspace-profiles.md",
            "docs/03.specs/0028-readme-workspace-profiles/tasks.md",
        ),
    ),
    "docs/03.specs/0029-semantic-document-validation/spec.md": (
        (
            "docs/04.execution/plans/2026-07-12-semantic-document-validation.md",
            "docs/03.specs/0029-semantic-document-validation/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-12-semantic-document-validation.md",
            "docs/03.specs/0029-semantic-document-validation/tasks.md",
        ),
    ),
    "docs/03.specs/0030-authored-document-migration/spec.md": (
        (
            "docs/04.execution/plans/2026-07-12-authored-document-migration.md",
            "docs/03.specs/0030-authored-document-migration/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-12-authored-document-migration.md",
            "docs/03.specs/0030-authored-document-migration/tasks.md",
        ),
    ),
    "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md": (
        (
            "docs/04.execution/plans/2026-07-18-active-corpus-and-execution-retention.md",
            "docs/03.specs/0037-active-corpus-and-execution-retention/plan.md",
        ),
        (
            "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md",
            "docs/03.specs/0037-active-corpus-and-execution-retention/tasks.md",
        ),
    ),
}
OWNER_SPEC = "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md"
EXECUTION_PLAN = (
    "docs/04.execution/plans/2026-07-18-active-corpus-and-execution-retention.md"
)
EXECUTION_TASK = (
    "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md"
)
TERMINAL_LINEAGE = "2026-07-22-reference-information-architecture"
TERMINAL_SPEC = "docs/03.specs/0038-reference-information-architecture/spec.md"
TERMINAL_PLAN = f"docs/04.execution/plans/{TERMINAL_LINEAGE}.md"
TERMINAL_TASK = f"docs/04.execution/tasks/{TERMINAL_LINEAGE}.md"
TERMINAL_SUCCESSOR_SPEC = "docs/03.specs/0039-github-ci-qa-evidence/spec.md"
TERMINAL_SUCCESSOR_LINEAGE = "2026-07-26-github-ci-qa-evidence"
TERMINAL_SUCCESSOR_PLAN = f"docs/04.execution/plans/{TERMINAL_SUCCESSOR_LINEAGE}.md"
TERMINAL_SUCCESSOR_TASK = f"docs/04.execution/tasks/{TERMINAL_SUCCESSOR_LINEAGE}.md"
TERMINAL_FRONTIER_SPEC = (
    "docs/03.specs/0040-contract-cutover-and-program-closure/spec.md"
)
TERMINAL_FRONTIER_LINEAGE = "2026-07-27-contract-cutover-and-program-closure"
TERMINAL_FRONTIER_PLAN = f"docs/04.execution/plans/{TERMINAL_FRONTIER_LINEAGE}.md"
TERMINAL_FRONTIER_TASK = f"docs/04.execution/tasks/{TERMINAL_FRONTIER_LINEAGE}.md"
TERMINAL_PROGRAM_PLAN_PATHS = frozenset(
    {TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN, TERMINAL_FRONTIER_PLAN}
)
TERMINAL_PROGRAM_TASK_PATHS = frozenset(
    {TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK, TERMINAL_FRONTIER_TASK}
)
TERMINAL_CONTROL_REPLACEMENTS = {
    EXECUTION_PLAN: "docs/03.specs/0037-active-corpus-and-execution-retention/plan.md",
    EXECUTION_TASK: "docs/03.specs/0037-active-corpus-and-execution-retention/tasks.md",
    TERMINAL_PLAN: "docs/03.specs/0038-reference-information-architecture/plan.md",
    TERMINAL_TASK: "docs/03.specs/0038-reference-information-architecture/tasks.md",
    TERMINAL_SUCCESSOR_PLAN: "docs/03.specs/0039-github-ci-qa-evidence/plan.md",
    TERMINAL_SUCCESSOR_TASK: "docs/03.specs/0039-github-ci-qa-evidence/tasks.md",
    TERMINAL_FRONTIER_PLAN: "docs/03.specs/0040-contract-cutover-and-program-closure/plan.md",
    TERMINAL_FRONTIER_TASK: "docs/03.specs/0040-contract-cutover-and-program-closure/tasks.md",
}
TERMINAL_PROGRAM_CLOSURE_ADR = (
    "docs/02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md"
)
FROZEN_ACCEPTED_ADR_PATHS = (
    "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md",
    "docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md",
    "docs/02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md",
    "docs/02.architecture/decisions/0008-istio-install-and-ingress-coexist.md",
    "docs/02.architecture/decisions/0009-kiali-external-observability.md",
    "docs/02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md",
    "docs/02.architecture/decisions/0012-argo-notifications-slack.md",
    "docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md",
    "docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md",
    "docs/02.architecture/decisions/0015-declarative-document-contract-registry.md",
    "docs/02.architecture/decisions/0016-program-to-tranche-document-lineage.md",
    "docs/02.architecture/decisions/0017-program-follow-up-lineage-semantics.md",
    "docs/02.architecture/decisions/0018-full-body-archive-record-and-retention.md",
)
FROZEN_DONE_SPEC_PATHS = (
    "docs/03.specs/0009-workspace-harness-research-pack/spec.md",
    "docs/03.specs/0010-workspace-harness-implementation-audit-pack/spec.md",
    "docs/03.specs/0011-template-contract-governance-migration/spec.md",
    "docs/03.specs/0012-template-governance-audit-enhancement/spec.md",
    "docs/03.specs/0013-workspace-document-governance-hardening/spec.md",
    "docs/03.specs/0014-workspace-document-contract-normalization/spec.md",
    "docs/03.specs/0015-agent-governance-contract-normalization/spec.md",
    "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md",
    "docs/03.specs/0017-workspace-engineering-research-pack/spec.md",
    "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md",
    "docs/03.specs/0019-template-path-numbering-contract/spec.md",
    "docs/03.specs/0020-workspace-contract-governance-normalization/spec.md",
    "docs/03.specs/0021-sdlc-lifecycle-contract/spec.md",
    "docs/03.specs/0022-control-cloud-doc-normalization/spec.md",
    "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md",
    "docs/03.specs/0024-observability-and-network-review-agents/spec.md",
    "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md",
    "docs/03.specs/0026-document-contract-registry/spec.md",
    "docs/03.specs/0027-template-contract-consolidation/spec.md",
    "docs/03.specs/0028-readme-workspace-profiles/spec.md",
    "docs/03.specs/0029-semantic-document-validation/spec.md",
    "docs/03.specs/0030-authored-document-migration/spec.md",
    "docs/03.specs/0031-affected-surface-agent-qa/spec.md",
    "docs/03.specs/0032-protected-surface-supply-chain-hardening/spec.md",
    "docs/03.specs/0033-template-lifecycle-contract-normalization/spec.md",
    "docs/03.specs/0034-authority-and-lineage-foundation/spec.md",
    "docs/03.specs/0035-document-schema-and-lifecycle-contract/spec.md",
    "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
    "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md",
)
POST_CLOSURE_ADR_AUTHORITY_PATHS = frozenset(
    {
        "docs/02.architecture/decisions/"
        "0019-provider-native-agent-harness-and-loop-model.md",
        "docs/02.architecture/decisions/"
        "0021-canonical-surface-routing-and-evidence-depth.md",
        "docs/02.architecture/decisions/"
        "0022-direct-approval-standalone-execution-lineage.md",
        "docs/02.architecture/decisions/"
        "0023-work-unit-document-taxonomy-and-governance-authority.md",
        "docs/02.architecture/decisions/"
        "0024-terminal-artifact-identity-and-archive-layout.md",
        "docs/02.architecture/decisions/0025-four-digit-document-path-identity.md",
        "docs/02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md",
        "docs/02.architecture/decisions/0027-pod-security-standards-staged-adoption.md",
        "docs/02.architecture/decisions/"
        "0028-pod-security-admission-per-namespace-adoption.md",
        "docs/02.architecture/decisions/0029-mutable-target-revision-retention.md",
    }
)
POST_CLOSURE_PINNED_AUTHORITY_BLOBS = {
    "docs/02.architecture/decisions/0025-four-digit-document-path-identity.md": (
        "5d4bea9a3072259f9f530fda0b8873afba92ca39"  # pragma: allowlist secret
    )
}
POST_CLOSURE_SPEC_AUTHORITY_PATHS = frozenset(
    {
        "docs/03.specs/0041-stage-00-agent-governance-contract/spec.md",
        "docs/03.specs/0042-provider-native-runtime-and-model-evidence/spec.md",
        "docs/03.specs/0043-agent-harness-loop-lifecycle/spec.md",
        "docs/03.specs/0044-agent-roster-evaluation-and-admission/spec.md",
        "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
        "docs/03.specs/0046-agent-governance-program-closure/spec.md",
        "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/spec.md",
        "docs/03.specs/0055-workspace-governance-audit-and-remediation/spec.md",
        "docs/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md",
        "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/spec.md",
        "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md",
        "docs/03.specs/0059-workspace-research-full-corpus-refresh/spec.md",
        "docs/03.specs/0060-platform-currency-defect-closure/spec.md",
        "docs/03.specs/0061-workload-security-context-baseline/spec.md",
    }
)
PLAN_ROOT = "docs/04.execution/plans"
TASK_ROOT = "docs/04.execution/tasks"
ADR_ROOT = "docs/02.architecture/decisions"
SPEC_ROOT = "docs/03.specs"
ARCHIVE_PLAN_ROOT = "docs/98.archive/04.execution/plans"
ARCHIVE_TASK_ROOT = "docs/98.archive/04.execution/tasks"
ARCHIVE_CHANGES_ROOT = "docs/98.archive/changes"
ARCHIVE_TOMBSTONES_ROOT = "docs/98.archive/tombstones"
ARCHIVE_MIGRATIONS_ROOT = "docs/98.archive/migrations"
SOURCE_PATHS = (
    "docs/90.references/data/active-corpus-retention-census.json",
    "docs/90.references/data/active-corpus-eligibility-ledger.json",
    "docs/90.references/data/active-corpus-migration-results.json",
    "docs/90.references/data/active-corpus-role-audit.json",
)
CONTROL_PATHS = (LEDGER_PATH, SCRIPT_PATH, AGGREGATE_PATH)
SOURCE_SCHEMAS = {
    SOURCE_PATHS[0]: "active-corpus-retention-census.v1",
    SOURCE_PATHS[1]: "active-corpus-eligibility-ledger.v1",
    SOURCE_PATHS[2]: "active-corpus-migration-results.v1",
    SOURCE_PATHS[3]: "active-corpus-role-audit.v1",
}
INVENTORY_ROOTS = (
    PLAN_ROOT,
    TASK_ROOT,
    ADR_ROOT,
    SPEC_ROOT,
    ARCHIVE_PLAN_ROOT,
    ARCHIVE_TASK_ROOT,
    ARCHIVE_CHANGES_ROOT,
    ARCHIVE_TOMBSTONES_ROOT,
    ARCHIVE_MIGRATIONS_ROOT,
)
MANDATORY_OWNER_PATHS = {
    SPEC_ROOT: frozenset(
        {
            OWNER_SPEC,
            TERMINAL_SPEC,
            TERMINAL_SUCCESSOR_SPEC,
            TERMINAL_FRONTIER_SPEC,
            *TERMINAL_CONTROL_REPLACEMENTS.values(),
        }
    ),
}

DEFER_AUTHORITY = "current-execution-record-pending-exact-eligibility-evidence"
DEFER_CLOSURE_REASON = "migration-blocked-by-explicit-missing-evidence"
DEFER_TRIGGER = "exact-upstream-evidence-change"
TERMINAL_CONTROL_REASON = (
    "terminal-spec-037-lineage-awaiting-successor-migration-evidence"
)
TERMINAL_CONTROL_EVIDENCE_ROLE = "terminal-stage-04-closure-evidence"
TERMINAL_CONTROL_REFRESH_TRIGGER = "exact-successor-migration-evidence-change"
ADR_AUTHORITY = "accepted-decision-record"
SPEC_AUTHORITY = "current-done-specification"
AUTHORITY_REASON = "terminal-status-alone-is-not-an-archive-predicate"
FINDING_KEYS = (
    "duplicateCurrentOwner",
    "unexplainedResidue",
    "activeEligible",
    "staleEligible",
    "missingClosureField",
    "movedAdrOrSpec",
    "currentLinkError",
    "historicalLinkError",
)

EXPECTED_COUNTS = {
    "candidateInput": 110,
    "historicalEligible": 12,
    "historicalDefer": 98,
    "migratedClosed": 12,
    "currentStage04": 100,
    "currentPlans": 49,
    "currentTasks": 51,
    "currentDefer": 100,
    "currentRetain": 0,
    "activeEligible": 0,
    "pairKeys": 52,
    "completePairs": 48,
    "planOnly": 1,
    "taskOnly": 3,
    "duplicateSameKind": 0,
    "partialOwnedDefer": 4,
    "acceptedAdrs": 13,
    "doneSpecs": 29,
    "migratedAdrOrSpec": 0,
    "stage05Authored": 24,
    "helperTests": 33,
    "findings": 0,
}
TRANSITION_EXPECTED_COUNTS = {
    **EXPECTED_COUNTS,
    "currentStage04": 0,
    "currentPlans": 0,
    "currentTasks": 0,
    "currentDefer": 0,
    "pairKeys": 0,
    "completePairs": 0,
    "planOnly": 0,
    "taskOnly": 0,
    "partialOwnedDefer": 0,
    "taxonomyArchived": 50,
}

GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_FILE_BYTES = 2_000_000
SAFE_PATH = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
ACTIVE_CONTROL_LINEAGE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._@+-]*\Z")
TERMINAL_RELATION_IDENTITY = {
    "spec": "0038",
    "order": 5,
    "reason": "Reference information architecture",
    "decision": "0017",
}
TERMINAL_SUCCESSOR_IDENTITY = {
    "spec": "0039",
    "order": 6,
    "reason": "GitHub CI and QA evidence",
    "decision": "0017",
}
TERMINAL_FRONTIER_IDENTITY = {
    "spec": "0040",
    "order": 7,
    "reason": "Contract cutover and program closure",
    "decision": "0017",
}
FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
MODE_RECORD = re.compile(
    rb"(?P<mode>[0-9]{6}) (?P<oid>[0-9a-f]{40}|[0-9a-f]{64}) "
    rb"(?P<stage>[0-3])\t(?P<path>[^\0]+)\Z"
)
FRONTMATTER_LINE = re.compile(
    r"(?P<key>[A-Za-z][A-Za-z0-9_-]*):[ \t]*(?P<value>[^\r\n]*)\Z"
)
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_KEY_0": "core.fsmonitor",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_CONFIG_VALUE_0": "false",
    "GIT_LITERAL_PATHSPECS": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "cat",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "PAGER": "cat",
    "PATH": "/usr/bin:/bin",
}


def is_safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value):
        return False
    parts = value.split("/")
    return (
        not value.startswith("/")
        and all(part not in {"", ".", ".."} for part in parts)
        and parts[0] != "_workspace"
    )


def diagnostic_path(value: Any) -> str:
    if isinstance(value, str) and value in {".", ".git"}:
        return value
    return value if is_safe_path(value) else LEDGER_PATH


def _git_identity(oid: str) -> str:
    if FULL_OID.fullmatch(oid) is None:
        raise ClosureError("CLOSURE-BLOB-ID")
    algorithm = "sha1" if len(oid) == 40 else "sha256"
    return f"git:{algorithm}:{oid}"


def _sha256_identity(digest: Any) -> str:
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ClosureError("CLOSURE-DIGEST")
    return f"digest:sha256:{digest}"


class ClosureError(ValueError):
    """Stable, single-line, value-free closure diagnostic."""

    def __init__(self, code: str, path: Any = LEDGER_PATH) -> None:
        self.code = code
        self.path = diagnostic_path(path)
        super().__init__(self.code, self.path)

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    inventory_queries = {
        ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", root)
        for root in INVENTORY_ROOTS
    }
    inventory_queries.update(
        {("ls-files", "-z", "--stage", "--", root) for root in INVENTORY_ROOTS}
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", *SOURCE_PATHS))
    for authority_path in (PROFILE_REGISTRY_PATH, ROUTE_CONTRACT_PATH):
        inventory_queries.add(
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                authority_path,
            )
        )
        inventory_queries.add(("ls-files", "-z", "--stage", "--", authority_path))
    inventory_queries.add(
        (
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            TAXONOMY_MANIFEST_PATH,
        )
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", TAXONOMY_MANIFEST_PATH))
    inventory_queries.add(
        (
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            *CONTROL_PATHS,
        )
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", *CONTROL_PATHS))
    inventory_queries.add(
        (
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            TAXONOMY_SOURCE_COMMIT,
            "--",
            PLAN_ROOT,
            TASK_ROOT,
        )
    )
    inventory_queries.add(
        (
            "ls-tree",
            "-z",
            "--full-tree",
            WORK105_BASE_COMMIT,
            "--",
            *WORK105_BASE_PATHS,
        )
    )
    if arguments in inventory_queries:
        return True
    return (
        len(arguments) == 3
        and arguments[:2]
        in {
            ("cat-file", "-t"),
            ("cat-file", "-s"),
            ("cat-file", "blob"),
        }
        and FULL_OID.fullmatch(arguments[2]) is not None
    )


def _run_git(
    root: str, arguments: tuple[str, ...]
) -> subprocess.CompletedProcess[bytes]:
    if not _git_arguments_allowed(arguments):
        raise ClosureError("CLOSURE-GIT-QUERY", ".git")
    try:
        return subprocess.run(
            [GIT_EXECUTABLE, *arguments],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=CLOSED_GIT_ENVIRONMENT,
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ClosureError("CLOSURE-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise ClosureError("CLOSURE-GIT-STARTUP", ".git") from exc


def _git(root: str, arguments: tuple[str, ...], runner: GitRunner) -> bytes:
    if not _git_arguments_allowed(arguments):
        raise ClosureError("CLOSURE-GIT-QUERY", ".git")
    try:
        result = runner(root, arguments)
    except subprocess.TimeoutExpired as exc:
        raise ClosureError("CLOSURE-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise ClosureError("CLOSURE-GIT-STARTUP", ".git") from exc
    if (
        not isinstance(result, subprocess.CompletedProcess)
        or result.returncode != 0
        or not isinstance(result.stdout, bytes)
    ):
        raise ClosureError("CLOSURE-GIT-RESULT", ".git")
    return result.stdout


def _parse_nul_paths(payload: bytes, scope: str) -> list[str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    paths: list[str] = []
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            path = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or not path.startswith(f"{scope}/"):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", scope)
    return sorted(paths)


def _parse_exact_nul_paths(payload: bytes, allowed_paths: set[str]) -> list[str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    paths: list[str] = []
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            path = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or path not in allowed_paths:
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise ClosureError("CLOSURE-INVENTORY-DUPLICATE")
    return sorted(paths)


def _parse_modes(
    payload: bytes,
    *,
    scope: str | None = None,
    allowed_paths: set[str] | None = None,
) -> dict[str, str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    modes: dict[str, str] = {}
    for raw in payload[:-1].split(b"\0") if payload else ():
        match = MODE_RECORD.fullmatch(raw)
        if match is None:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
        try:
            path = match.group("path").decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        if scope is not None and not path.startswith(f"{scope}/"):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        if allowed_paths is not None and path not in allowed_paths:
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        expected_mode = b"100755" if path == AGGREGATE_PATH else b"100644"
        if match.group("mode") != expected_mode or match.group("stage") != b"0":
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", path)
        if path in modes:
            raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", path)
        modes[path] = match.group("oid").decode("ascii")
    return modes


def _normalize_root(root: str | os.PathLike[str]) -> str:
    try:
        value = os.fspath(root)
    except TypeError as exc:
        raise ClosureError("CLOSURE-ROOT", ".") from exc
    if not isinstance(value, str) or not value or "\0" in value:
        raise ClosureError("CLOSURE-ROOT", ".")
    normalized = os.path.abspath(value)
    if not os.path.isdir(normalized) or os.path.islink(normalized):
        raise ClosureError("CLOSURE-ROOT", ".")
    return normalized


def _read_descriptor_bytes(root: str, relative: str) -> bytes:
    if not is_safe_path(relative):
        raise ClosureError("CLOSURE-INVENTORY-PATH", relative)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptors: list[int] = []
    try:
        try:
            current = os.open(root, directory_flags)
        except OSError as exc:
            raise ClosureError("CLOSURE-ROOT", ".") from exc
        descriptors.append(current)
        parts = relative.split("/")
        for part in parts[:-1]:
            try:
                current = os.open(part, directory_flags, dir_fd=current)
            except OSError as exc:
                raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative) from exc
            descriptors.append(current)
        try:
            descriptor = os.open(parts[-1], file_flags, dir_fd=current)
        except FileNotFoundError as exc:
            raise ClosureError("CLOSURE-INVENTORY-MISSING", relative) from exc
        except OSError as exc:
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative) from exc
        descriptors.append(descriptor)
        try:
            metadata = os.fstat(descriptor)
        except OSError as exc:
            raise ClosureError("CLOSURE-READ", relative) from exc
        if not stat.S_ISREG(metadata.st_mode):
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative)
        if metadata.st_size > MAX_FILE_BYTES:
            raise ClosureError("CLOSURE-BOUNDS", relative)
        chunks: list[bytes] = []
        total = 0
        while True:
            try:
                chunk = os.read(descriptor, min(65_536, MAX_FILE_BYTES + 1 - total))
            except OSError as exc:
                raise ClosureError("CLOSURE-READ", relative) from exc
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ClosureError("CLOSURE-BOUNDS", relative)
        return b"".join(chunks)
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _index_blob(root: str, oid: str, path: str, runner: GitRunner) -> bytes:
    if FULL_OID.fullmatch(oid) is None:
        raise ClosureError("CLOSURE-BLOB-ID", path)
    if _git(root, ("cat-file", "-t", oid), runner) != b"blob\n":
        raise ClosureError("CLOSURE-BLOB-TYPE", path)
    size_payload = _git(root, ("cat-file", "-s", oid), runner)
    if re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", size_payload) is None:
        raise ClosureError("CLOSURE-BLOB-SIZE", path)
    size = int(size_payload)
    if size > MAX_FILE_BYTES:
        raise ClosureError("CLOSURE-BOUNDS", path)
    payload = _git(root, ("cat-file", "blob", oid), runner)
    if len(payload) != size:
        raise ClosureError("CLOSURE-BLOB-LENGTH", path)
    return payload


def _taxonomy_source_tree(
    root: str,
    expected_sources: set[str],
    runner: GitRunner,
) -> dict[str, str]:
    """Resolve every reviewed migration source from the frozen source tree."""

    payload = _git(
        root,
        (
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            TAXONOMY_SOURCE_COMMIT,
            "--",
            PLAN_ROOT,
            TASK_ROOT,
        ),
        runner,
    )
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-TAXONOMY-BLOB", ".git")
    resolved: dict[str, str] = {}
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            header, raw_path = raw.split(b"\t", 1)
            mode, object_type, raw_oid = header.split(b" ", 2)
            path = raw_path.decode("utf-8", errors="strict")
            oid = raw_oid.decode("ascii", errors="strict")
        except (ValueError, UnicodeDecodeError) as exc:
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", ".git") from exc
        if path not in expected_sources:
            continue
        if (
            mode != b"100644"
            or object_type != b"blob"
            or FULL_OID.fullmatch(oid) is None
            or path in resolved
        ):
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", path)
        resolved[path] = oid
    if set(resolved) != expected_sources:
        missing = sorted(expected_sources - set(resolved))
        raise ClosureError(
            "CLOSURE-TAXONOMY-BLOB", missing[0] if missing else TAXONOMY_MANIFEST_PATH
        )
    return resolved


def _work105_base_projection(root: str, runner: GitRunner = _run_git) -> dict[str, str]:
    """Bind the staged WORK-105 compatibility projection to its exact base tree."""

    expected = {
        RETIRED_REGISTRY_PATH: WORK105_REGISTRY_BLOBS[0],
        **{
            path: base_blob
            for path, (base_blob, _current_blob) in WORK105_AUTHORITY_BLOBS.items()
        },
    }
    payload = _git(
        root,
        (
            "ls-tree",
            "-z",
            "--full-tree",
            WORK105_BASE_COMMIT,
            "--",
            *WORK105_BASE_PATHS,
        ),
        runner,
    )
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
    resolved: dict[str, str] = {}
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            header, raw_path = raw.split(b"\t", 1)
            mode, object_type, raw_oid = header.split(b" ", 2)
            path = raw_path.decode("utf-8", errors="strict")
            oid = raw_oid.decode("ascii", errors="strict")
        except (ValueError, UnicodeDecodeError) as exc:
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT") from exc
        current_path = WORK105_CURRENT_PATHS_BY_HISTORICAL.get(path, path)
        if (
            current_path not in expected
            or mode != b"100644"
            or object_type != b"blob"
            or FULL_OID.fullmatch(oid) is None
            or current_path in resolved
        ):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT", path)
        resolved[current_path] = oid
    if resolved != expected:
        mismatch = next(
            (
                path
                for path in WORK105_BASE_PATHS
                if resolved.get(path) != expected[path]
            ),
            RETIRED_REGISTRY_PATH,
        )
        code = (
            "CLOSURE-TERMINAL-REGISTRY-AUTHORITY"
            if mismatch == RETIRED_REGISTRY_PATH
            else "CLOSURE-AUTHORITY-DRIFT"
        )
        raise ClosureError(code, mismatch)
    return resolved


def _taxonomy_archive_recoveries(
    root: str,
    archive_entries: Sequence[Mapping[str, Any]],
    source_tree: Mapping[str, str],
    runner: GitRunner,
) -> dict[str, RecoveryResult]:
    """Recover exact archive source bytes from their reviewed Git objects."""

    recoveries: dict[str, RecoveryResult] = {}
    for entry in archive_entries:
        source = str(entry["source"])
        target = str(entry["target"])
        oid = source_tree.get(source)
        if oid != entry.get("sourceBlob"):
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", source)
        source_bytes = _index_blob(root, oid, source, runner)
        recoveries[source] = RecoveryResult(
            original_path=source,
            source_commit=TAXONOMY_SOURCE_COMMIT,
            source_blob=oid,
            byte_count=len(source_bytes),
            content_sha256=hashlib.sha256(source_bytes).hexdigest(),
            inline_link_candidate_count=0,
            proposed_archive_path=target,
            source_bytes=source_bytes,
        )
    return recoveries


def _decode_text(payload: bytes, path: str) -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ClosureError("CLOSURE-UTF8", path) from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ClosureError("CLOSURE-JSON-DUPLICATE")
        result[key] = value
    return result


def _load_json_bytes(payload: bytes, path: str) -> Any:
    try:
        return json.loads(
            _decode_text(payload, path), object_pairs_hook=_reject_duplicate_pairs
        )
    except ClosureError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ClosureError("CLOSURE-JSON", path) from exc


def _frontmatter(text: str, path: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ClosureError("CLOSURE-FRONTMATTER", path)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ClosureError("CLOSURE-FRONTMATTER", path)
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "-")):
            continue
        match = FRONTMATTER_LINE.fullmatch(line)
        if match is None:
            continue
        key = match.group("key")
        if key in metadata:
            raise ClosureError("CLOSURE-FRONTMATTER", path)
        metadata[key] = match.group("value").strip().strip("'\"")
    return metadata


def _inventory(
    root: str, scope: str, runner: GitRunner
) -> tuple[list[str], dict[str, str]]:
    paths = _parse_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                scope,
            ),
            runner,
        ),
        scope,
    )
    modes = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", scope), runner),
        scope=scope,
    )
    if not set(modes).issubset(paths):
        raise ClosureError("CLOSURE-INVENTORY-DRIFT", scope)
    required = MANDATORY_OWNER_PATHS.get(scope, frozenset())
    missing = required - set(modes)
    if missing:
        raise ClosureError("CLOSURE-OWNER-INVENTORY", sorted(missing)[0])
    return paths, modes


def _source_index(root: str, runner: GitRunner) -> dict[str, str]:
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", *SOURCE_PATHS), runner),
        allowed_paths=set(SOURCE_PATHS),
    )
    if set(index) != set(SOURCE_PATHS):
        raise ClosureError("CLOSURE-SOURCE-INVENTORY", ".git")
    return index


def _control_inventory(root: str, runner: GitRunner) -> dict[str, str]:
    allowed = set(CONTROL_PATHS)
    paths = _parse_exact_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                *CONTROL_PATHS,
            ),
            runner,
        ),
        allowed,
    )
    if set(paths) != allowed:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", ".git")
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", *CONTROL_PATHS), runner),
        allowed_paths=allowed,
    )
    missing = allowed - set(index)
    if missing:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", sorted(missing)[0])
    if set(index) != allowed:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", ".git")
    return index


def _single_file_inventory(
    root: str, path: str, code: str, runner: GitRunner
) -> dict[str, str]:
    allowed = {path}
    paths = _parse_exact_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                path,
            ),
            runner,
        ),
        allowed,
    )
    if paths != [path]:
        raise ClosureError(code, path)
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", path), runner),
        allowed_paths=allowed,
    )
    if set(index) != allowed:
        raise ClosureError(code, path)
    return index


REGISTRY_AUTHORITY_BLOBS = {
    PROFILE_REGISTRY_PATH: (
        PROFILE_REGISTRY_BLOB,
        SPEC0062_PROFILE_REGISTRY_BLOB,
    ),
    ROUTE_CONTRACT_PATH: (ROUTE_CONTRACT_BLOB,),
}


def _registry_inventory(
    root: str, path: str, runner: GitRunner
) -> dict[str, str]:
    return _single_file_inventory(
        root, path, "CLOSURE-REGISTRY-INVENTORY", runner
    )


def _taxonomy_manifest_inventory(root: str, runner: GitRunner) -> dict[str, str]:
    return _single_file_inventory(
        root,
        TAXONOMY_MANIFEST_PATH,
        "CLOSURE-TAXONOMY-MANIFEST-INVENTORY",
        runner,
    )


def _proposed_or_index_bytes(
    root: str,
    path: str,
    index: Mapping[str, str],
    runner: GitRunner,
) -> bytes:
    descriptor = _read_descriptor_bytes(root, path)
    oid = index.get(path)
    if oid is None:
        return descriptor
    staged = _index_blob(root, oid, path, runner)
    if descriptor != staged:
        raise ClosureError("CLOSURE-WORKTREE-INDEX-DRIFT", path)
    return staged


def _load_registry_authority(
    root: str, runner: GitRunner = _run_git
) -> Mapping[str, Any]:
    """Merge both published contracts into the flat form this closure reads.

    The closure needs programLineage from the profile registry and routeState,
    archiveContractVersion, and archiveNamespaces from the route contract, so
    neither file alone answers it. Each is admitted against its own pinned
    state, and a key declared by both is a contract error rather than a
    silent precedence rule.
    """

    merged: dict[str, Any] = {}
    for path, admitted in REGISTRY_AUTHORITY_BLOBS.items():
        index = _registry_inventory(root, path, runner)
        payload = _proposed_or_index_bytes(root, path, index, runner)
        if index.get(path) not in admitted:
            raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", path)
        loaded = _load_json_bytes(payload, path)
        if not isinstance(loaded, Mapping):
            raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", path)
        for key, value in loaded.items():
            if key in {"$schema", "$id", "schemaVersion"}:
                continue
            if key in merged:
                raise ClosureError("CLOSURE-TERMINAL-REGISTRY-DUPLICATE", path)
            merged[key] = value
    return merged


def _authored_stage04(paths: Sequence[str], scope: str) -> list[str]:
    result: list[str] = []
    support_readme = f"{scope}/README.md"
    for path in paths:
        if path == support_readme:
            continue
        if not path.endswith(".md") or path.count("/") != 3:
            raise ClosureError("CLOSURE-STAGE04-PATH", path)
        result.append(path)
    return result


def _object_identity(
    path: str, index: Mapping[str, str], payload: bytes
) -> dict[str, str]:
    oid = index.get(path)
    if oid is not None:
        return {"objectMode": "index-stage-zero", "objectId": _git_identity(oid)}
    indexed_target = TERMINAL_CONTROL_REPLACEMENTS.get(path)
    if indexed_target is not None:
        target_oid = index.get(indexed_target)
        if target_oid is not None:
            return {
                "objectMode": "projected-replacement",
                "objectId": _git_identity(target_oid),
                "legacySource": path,
                "indexedTarget": indexed_target,
            }
    return {
        "objectMode": "proposed-nonignored-descriptor",
        "objectId": _sha256_identity(hashlib.sha256(payload).hexdigest()),
    }


def _git_blob_oid(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324 - Git identity


def _current_taxonomy_target(path: str) -> str:
    """Compose a frozen three-digit Spec target with the MIG-2 path cutover."""

    match = re.fullmatch(
        r"docs/03\.specs/(?P<id>[0-9]{3})-(?P<suffix>[a-z0-9][a-z0-9./-]*)",
        path,
    )
    if match is None:
        return path
    return f"docs/03.specs/0{match.group('id')}-{match.group('suffix')}"


def _work108_authority_object_identity(
    path: str, index: Mapping[str, str], payload: bytes
) -> dict[str, str]:
    """Project only the reviewed WORK-108 outer ID onto frozen authority bytes."""

    expected_blobs = WORK105_AUTHORITY_BLOBS.get(path)
    oid = index.get(path)
    if expected_blobs is None or oid is None or oid != _git_blob_oid(payload):
        return _object_identity(path, index, payload)
    decision = re.fullmatch(
        r"docs/02\.architecture/decisions/(?P<id>[0-9]{4})-[a-z0-9]+"
        r"(?:-[a-z0-9]+)*\.md",
        path,
    )
    specification = re.fullmatch(
        r"docs/03\.specs/(?P<id>[0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*/spec\.md",
        path,
    )
    if decision is not None:
        expected_id = f"ADR-{decision.group('id')}"
    elif specification is not None:
        expected_id = f"SPEC-{specification.group('id')}"
    else:
        return _object_identity(path, index, payload)
    expected = f'artifact_id: "{expected_id}"'.encode("ascii")
    lines = payload.splitlines(keepends=True)
    matches = [
        line_index
        for line_index, line in enumerate(lines)
        if line.rstrip(b"\r\n") == expected
    ]
    if len(matches) != 1 or matches[0] == 0:
        return _object_identity(path, index, payload)
    line_index = matches[0]
    projected = b"".join(lines[:line_index] + lines[line_index + 1 :])
    if (
        not lines[line_index - 1].startswith(b"updated:")
        or _git_blob_oid(projected) != expected_blobs[1]
    ):
        return _object_identity(path, index, payload)
    return {
        "objectMode": "index-stage-zero",
        "objectId": _git_identity(expected_blobs[1]),
    }


def _validate_reviewed_move_mapping(
    move_entries: Sequence[Mapping[str, Any]],
) -> None:
    """Bind every reviewed Stage 04 source to its exact Spec sibling pair."""

    source_pattern = re.compile(
        r"docs/04\.execution/(?P<scope>plans|tasks)/"
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md"
    )
    target_pattern = re.compile(
        r"docs/03\.specs/(?P<unit>[0-9]{3})-"
        r"(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<name>plan|tasks)\.md"
    )
    pairs: dict[tuple[str, str], set[str]] = defaultdict(set)
    for entry in move_entries:
        source = str(entry["source"])
        target = str(entry["target"])
        source_match = source_pattern.fullmatch(source)
        target_match = target_pattern.fullmatch(target)
        if source_match is None or target_match is None:
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", source)
        kind = "plan" if source_match.group("scope") == "plans" else "task"
        expected_name = "plan" if kind == "plan" else "tasks"
        expected_work_unit = f"Spec-{target_match.group('unit')}"
        if (
            source_match.group("slug") != target_match.group("slug")
            or target_match.group("name") != expected_name
            or entry["workUnit"] != expected_work_unit
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", source)
        pair_key = (expected_work_unit, str(PurePosixPath(target).parent))
        if kind in pairs[pair_key]:
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", source)
        pairs[pair_key].add(kind)
    if len(pairs) != 41 or any(kinds != {"plan", "task"} for kinds in pairs.values()):
        raise ClosureError("CLOSURE-TAXONOMY-MOVE", TAXONOMY_MANIFEST_PATH)


def _work107_archive_aliases(content: bytes) -> dict[str, str]:
    """Load the exact reviewed legacy-to-stable Stage 98 bijection."""

    if hashlib.sha256(content).hexdigest() != WORK107_MIGRATION_DOCUMENT_SHA256:
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    try:
        rows = parse_work107_migration_document(content)
    except ArchiveContractError as exc:
        raise ClosureError(
            "CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH
        ) from exc
    aliases: dict[str, str] = {}
    stable_paths: set[str] = set()
    for row in rows:
        legacy_path = row.get("legacy_path")
        stable_path = row.get("stable_path")
        if (
            not is_safe_path(legacy_path)
            or not is_safe_path(stable_path)
            or legacy_path in aliases
            or stable_path in stable_paths
        ):
            raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
        aliases[str(legacy_path)] = str(stable_path)
        stable_paths.add(str(stable_path))
    if len(aliases) != 93:
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    return aliases


def _build_taxonomy_transition_closure(
    registry: Mapping[str, Any],
    manifest: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    current_paths: set[str],
    archive_payloads: Mapping[str, bytes],
    archive_index: Mapping[str, str],
    source_tree: Mapping[str, str],
    archive_recoveries: Mapping[str, RecoveryResult],
    archive_aliases: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Reconcile the frozen ACER residue snapshot with exact WDTC archives."""

    if (
        not isinstance(registry, Mapping)
        or registry.get("routeState") != "transition"
        or not isinstance(manifest, Mapping)
        or manifest.get("state") != "transition"
    ):
        raise ClosureError("CLOSURE-TAXONOMY-TERMINAL", TAXONOMY_MANIFEST_PATH)
    if (
        registry.get("archiveContractVersion") != 2
        or manifest.get("sourceCommit") != TAXONOMY_SOURCE_COMMIT
        or set(manifest) != {"state", "sourceCommit", "entries"}
    ):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)

    namespaces = registry.get("archiveNamespaces")
    namespace_contract = (
        ("arwb-base", "exact-immutable", 31),
        ("acer-additive", "exact-immutable", 12),
        ("wdtc-execution", "exact-reviewed-manifest", 50),
        ("progress-snapshot", "append-only-unique", 0),
    )
    if not isinstance(namespaces, list) or len(namespaces) != len(namespace_contract):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", ROUTE_CONTRACT_PATH)
    by_namespace: dict[str, Mapping[str, Any]] = {}
    for raw_namespace, (expected_id, expected_policy, expected_count) in zip(
        namespaces, namespace_contract, strict=True
    ):
        if (
            not isinstance(raw_namespace, Mapping)
            or set(raw_namespace) != {"id", "policy", "records"}
            or raw_namespace.get("id") != expected_id
            or raw_namespace.get("policy") != expected_policy
            or not isinstance(raw_namespace.get("records"), list)
            or len(raw_namespace["records"]) != expected_count
            or raw_namespace["id"] in by_namespace
        ):
            raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", ROUTE_CONTRACT_PATH)
        by_namespace[raw_namespace["id"]] = raw_namespace
    namespace = by_namespace.get("wdtc-execution")
    if (
        namespace is None
        or namespace.get("policy") != "exact-reviewed-manifest"
        or not isinstance(namespace.get("records"), list)
        or any(not is_safe_path(path) for path in namespace["records"])
        or len(set(namespace["records"])) != 50
    ):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", ROUTE_CONTRACT_PATH)

    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 132:
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST-COUNT", TAXONOMY_MANIFEST_PATH)
    entry_keys = {
        "source",
        "target",
        "workUnit",
        "disposition",
        "sourceBlob",
        "reviewed",
    }
    sources: set[str] = set()
    targets: set[str] = set()
    archive_entries: list[Mapping[str, Any]] = []
    move_entries: list[Mapping[str, Any]] = []
    dispositions: Counter[str] = Counter()
    for entry in entries:
        if (
            not isinstance(entry, Mapping)
            or set(entry) != entry_keys
            or not is_safe_path(entry.get("source"))
            or not is_safe_path(entry.get("target"))
            or not isinstance(entry.get("workUnit"), str)
            or not entry["workUnit"]
            or entry.get("disposition") not in {"move-current", "archive-unique"}
            or not isinstance(entry.get("sourceBlob"), str)
            or re.fullmatch(r"[0-9a-f]{40}", entry["sourceBlob"]) is None
            or entry.get("reviewed") is not True
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
        source = entry["source"]
        target = entry["target"]
        if source in sources or target in targets:
            raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
        sources.add(source)
        targets.add(target)
        dispositions[entry["disposition"]] += 1
        if entry["disposition"] == "archive-unique":
            archive_entries.append(entry)
        else:
            move_entries.append(entry)
    if dispositions != Counter({"move-current": 82, "archive-unique": 50}):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST-COUNT", TAXONOMY_MANIFEST_PATH)
    _validate_reviewed_move_mapping(move_entries)
    if set(source_tree) != sources or any(
        source_tree.get(entry["source"]) != entry["sourceBlob"] for entry in entries
    ):
        raise ClosureError("CLOSURE-TAXONOMY-BLOB", TAXONOMY_MANIFEST_PATH)
    archive_sources = {entry["source"] for entry in archive_entries}
    if set(archive_recoveries) != archive_sources:
        raise ClosureError("CLOSURE-TAXONOMY-BLOB", TAXONOMY_MANIFEST_PATH)

    if (
        len(archive_aliases) != 93
        or len(set(archive_aliases.values())) != 93
        or any(
            not is_safe_path(legacy) or not is_safe_path(stable)
            for legacy, stable in archive_aliases.items()
        )
    ):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    archive_targets = {
        archive_aliases.get(entry["target"]) for entry in archive_entries
    }
    if archive_targets != set(namespace["records"]):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", ROUTE_CONTRACT_PATH)

    candidates = eligibility.get("candidateRows")
    if not isinstance(candidates, list):
        raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
    eligibility_by_path: dict[str, Mapping[str, Any]] = {}
    for candidate in candidates:
        if not isinstance(candidate, Mapping) or not is_safe_path(
            candidate.get("path")
        ):
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
        path = candidate["path"]
        if path in eligibility_by_path:
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
        eligibility_by_path[path] = candidate
    controls = eligibility.get("controls")
    if not isinstance(controls, list):
        raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
    control_by_path: dict[str, Mapping[str, Any]] = {}
    for control in controls:
        if not isinstance(control, Mapping) or not is_safe_path(control.get("path")):
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
        path = control["path"]
        if path in control_by_path or path in eligibility_by_path:
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", SOURCE_PATHS[1])
        control_by_path[path] = control

    rows: list[dict[str, Any]] = []
    for entry in sorted(archive_entries, key=lambda row: row["source"]):
        source = entry["source"]
        legacy_target = entry["target"]
        target = archive_aliases.get(legacy_target)
        expected_target = source.replace("docs/", "docs/98.archive/", 1)
        kind = (
            "plan"
            if source.startswith(f"{PLAN_ROOT}/")
            else "task"
            if source.startswith(f"{TASK_ROOT}/")
            else None
        )
        if (
            kind is None
            or legacy_target != expected_target
            or not isinstance(target, str)
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", source)
        if source in current_paths:
            raise ClosureError("CLOSURE-TAXONOMY-SOURCE", source)
        archive_bytes = archive_payloads.get(target)
        archive_oid = archive_index.get(target)
        if (
            not isinstance(archive_bytes, bytes)
            or not isinstance(archive_oid, str)
            or FULL_OID.fullmatch(archive_oid) is None
        ):
            raise ClosureError("CLOSURE-TAXONOMY-ARCHIVE", target)
        candidate = eligibility_by_path.get(source)
        if candidate is None or candidate.get("disposition") != "DEFER":
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", source)
        try:
            parsed = parse_archive_envelope(
                archive_bytes, expected=archive_recoveries[source]
            )
        except ArchiveContractError as exc:
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", source) from exc
        metadata = parsed.metadata
        if (
            metadata.get("original_path") != source
            or metadata.get("original_type") != f"sdlc/{kind}"
            or metadata.get("source_commit") != TAXONOMY_SOURCE_COMMIT
            or metadata.get("source_blob") != entry["sourceBlob"]
        ):
            raise ClosureError("CLOSURE-TAXONOMY-BLOB", source)
        rows.append(
            {
                "path": source,
                "kind": kind,
                "archivePath": target,
                "namespace": "wdtc-execution",
                "sourceCommit": _git_identity(TAXONOMY_SOURCE_COMMIT),
                "sourceBlob": _git_identity(entry["sourceBlob"]),
                "archiveObjectId": _git_identity(archive_oid),
                "disposition": "manifest-archive-closed",
                "currentSourcePresent": False,
                "archivePresent": True,
            }
        )
    frozen_paths = {
        path
        for path, candidate in eligibility_by_path.items()
        if candidate.get("disposition") == "DEFER"
    } | set(control_by_path)
    for entry in sorted(move_entries, key=lambda row: row["source"]):
        source = entry["source"]
        target = _current_taxonomy_target(entry["target"])
        kind = (
            "plan"
            if source.startswith(f"{PLAN_ROOT}/")
            else "task"
            if source.startswith(f"{TASK_ROOT}/")
            else None
        )
        expected_name = "plan.md" if kind == "plan" else "tasks.md"
        target_path = PurePosixPath(target)
        if (
            kind is None
            or source in current_paths
            or target not in current_paths
            or target_path.parts[:2] != ("docs", "03.specs")
            or len(target_path.parts) != 4
            or target_path.name != expected_name
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", source)
        target_bytes = archive_payloads.get(target)
        target_oid = archive_index.get(target)
        if (
            not isinstance(target_bytes, bytes)
            or not isinstance(target_oid, str)
            or FULL_OID.fullmatch(target_oid) is None
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", target)
        metadata = _frontmatter(_decode_text(target_bytes, target), target)
        if (
            metadata.get("type") != f"sdlc/{kind}"
            or metadata.get("owner") != "platform"
        ):
            raise ClosureError("CLOSURE-TAXONOMY-MOVE", target)
        if source not in frozen_paths:
            continue
        rows.append(
            {
                "path": source,
                "kind": kind,
                "replacementPath": target,
                "sourceCommit": _git_identity(TAXONOMY_SOURCE_COMMIT),
                "sourceBlob": _git_identity(entry["sourceBlob"]),
                "replacementObjectId": _git_identity(target_oid),
                "disposition": "manifest-move-closed",
                "currentSourcePresent": False,
                "replacementPresent": True,
            }
        )
    rows.sort(key=lambda row: row["path"])
    if len(rows) != len(frozen_paths):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST-COUNT", TAXONOMY_MANIFEST_PATH)
    return rows


def _build_current_rows(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    eligibility: Mapping[str, Any],
    transition_archived_paths: frozenset[str] = frozenset(),
) -> list[dict[str, Any]]:
    candidates = eligibility.get("candidateRows")
    controls = eligibility.get("controls")
    if not isinstance(candidates, list) or not isinstance(controls, list):
        raise ClosureError("CLOSURE-ELIGIBILITY-SCHEMA", SOURCE_PATHS[1])
    defer_by_path = {
        row.get("path"): row
        for row in candidates
        if isinstance(row, Mapping) and row.get("disposition") == "DEFER"
    }
    control_by_path = {
        row.get("path"): row for row in controls if isinstance(row, Mapping)
    }
    frozen_paths = set(defer_by_path) | set(control_by_path)
    if not transition_archived_paths.issubset(frozen_paths):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
    paths = sorted(frozen_paths - transition_archived_paths)
    if not set(paths).issubset(set(plan_paths) | set(task_paths)):
        raise ClosureError("CLOSURE-CURRENT-RESIDUE")
    entries: list[dict[str, Any]] = []
    for path in paths:
        payload = payloads[path]
        metadata = _frontmatter(_decode_text(payload, path), path)
        kind = "plan" if path.startswith(f"{PLAN_ROOT}/") else "task"
        if (
            metadata.get("type") != f"sdlc/{kind}"
            or metadata.get("owner") != "platform"
        ):
            raise ClosureError("CLOSURE-CURRENT-AUTHORITY", path)
        identity = _object_identity(path, index, payload)
        if path in defer_by_path:
            source = defer_by_path[path]
            if metadata.get("status") != "done":
                raise ClosureError("CLOSURE-CURRENT-STATUS", path)
            if (
                source.get("kind") != kind
                or source.get("owner") != "platform"
                or source.get("status") != "done"
                or not isinstance(source.get("reason"), str)
                or not source.get("reason")
                or not isinstance(source.get("refreshTrigger"), str)
                or not source.get("refreshTrigger")
                or not isinstance(source.get("missingAxes"), list)
                or not source.get("missingAxes")
                or source.get("residueClass")
                not in {"deferred-evidence", "resolved-partial-evidence"}
            ):
                raise ClosureError("CLOSURE-SOURCE-DEFER", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": source.get("pairKey"),
                    "profile": metadata.get("type"),
                    "status": "done",
                    **identity,
                    "sourceDisposition": "DEFER",
                    "sourceReason": source.get("reason"),
                    "sourceOwner": source.get("owner"),
                    "sourceRefreshTrigger": source.get("refreshTrigger"),
                    "missingAxes": source.get("missingAxes"),
                    "residueClass": source.get("residueClass"),
                    "disposition": "DEFER",
                    "owner": "platform",
                    "closureReason": DEFER_CLOSURE_REASON,
                    "postClosureRefreshTrigger": DEFER_TRIGGER,
                    "currentAuthority": DEFER_AUTHORITY,
                }
            )
        else:
            source = control_by_path[path]
            if metadata.get("status") != "done":
                raise ClosureError("CLOSURE-CONTROL-STATUS", path)
            if (
                source.get("kind") != kind
                or source.get("disposition") != "retain"
                or source.get("owner") != "platform"
                or source.get("reason") != "active-spec-037-control"
                or source.get("refreshTrigger") != "Spec037 closure"
            ):
                raise ClosureError("CLOSURE-CONTROL-SOURCE", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": source.get("pairKey"),
                    "profile": metadata.get("type"),
                    "status": "done",
                    **identity,
                    "sourceDisposition": "retain",
                    "sourceReason": source.get("reason"),
                    "sourceOwner": source.get("owner"),
                    "sourceRefreshTrigger": source.get("refreshTrigger"),
                    "missingAxes": ["successor-migration-evidence"],
                    "residueClass": "terminal-owned-defer",
                    "disposition": "DEFER",
                    "owner": "platform",
                    "reason": TERMINAL_CONTROL_REASON,
                    "currentEvidenceRole": TERMINAL_CONTROL_EVIDENCE_ROLE,
                    "successorRefreshTrigger": TERMINAL_CONTROL_REFRESH_TRIGGER,
                }
            )
    return entries


def _active_control_lineage(path: str, kind: str) -> str:
    scope = PLAN_ROOT if kind == "plan" else TASK_ROOT
    prefix = f"{scope}/"
    if not path.startswith(prefix) or not path.endswith(".md"):
        raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", path)
    lineage = path[len(prefix) : -len(".md")]
    if ACTIVE_CONTROL_LINEAGE.fullmatch(lineage) is None:
        raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", path)
    return lineage


def _terminal_program_control_scope(paths: Sequence[str], *, kind: str) -> list[str]:
    """Select only the PRD-0006 execution controls owned by ACER-006."""

    if kind == "plan":
        owned = TERMINAL_PROGRAM_PLAN_PATHS
    elif kind == "task":
        owned = TERMINAL_PROGRAM_TASK_PATHS
    else:
        raise ValueError(f"unsupported terminal control kind: {kind}")
    return [path for path in paths if path in owned]


def _project_terminal_control_replacements(
    index: Mapping[str, str], payloads: Mapping[str, bytes]
) -> tuple[dict[str, str], dict[str, bytes]]:
    """Project reviewed Stage 03 siblings into the frozen terminal-state model."""

    projected_index = dict(index)
    projected_payloads = dict(payloads)
    for source, target in TERMINAL_CONTROL_REPLACEMENTS.items():
        if (
            source in index
            or source in payloads
            or target not in index
            or target not in payloads
        ):
            raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", target)
        projected_payloads[source] = payloads[target]
    return projected_index, projected_payloads


def _terminal_registry_relations(
    registry: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    lineage = registry.get("programLineage")
    programs = lineage.get("programs") if isinstance(lineage, Mapping) else None
    if not isinstance(programs, list):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", PROFILE_REGISTRY_PATH)

    exact_programs: list[Mapping[str, Any]] = []
    relations: dict[str, list[tuple[Mapping[str, Any], str, Mapping[str, Any]]]] = {
        "0038": [],
        "0039": [],
        "0040": [],
    }
    for program in programs:
        if not isinstance(program, Mapping):
            raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", PROFILE_REGISTRY_PATH)
        if program.get("prd") == "0006" and program.get("ad") == "0009":
            if set(program) != {"prd", "ad", "tranches", "followUps"}:
                raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", PROFILE_REGISTRY_PATH)
            exact_programs.append(program)
        for collection_name in ("tranches", "followUps"):
            collection = program.get(collection_name)
            if not isinstance(collection, list):
                raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", PROFILE_REGISTRY_PATH)
            for relation in collection:
                if not isinstance(relation, Mapping):
                    raise ClosureError(
                        "CLOSURE-TERMINAL-REGISTRY-MALFORMED", PROFILE_REGISTRY_PATH
                    )
                spec_id = relation.get("spec")
                if spec_id in relations:
                    relations[str(spec_id)].append((program, collection_name, relation))

    if len(exact_programs) > 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-DUPLICATE", PROFILE_REGISTRY_PATH)
    if len(exact_programs) != 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", PROFILE_REGISTRY_PATH)
    if any(len(relations[spec_id]) > 1 for spec_id in relations):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-DUPLICATE", PROFILE_REGISTRY_PATH)
    if len(relations["0038"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", PROFILE_REGISTRY_PATH)
    if len(relations["0039"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if len(relations["0040"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)

    exact_program = exact_programs[0]
    program_038, collection_038, relation_038 = relations["0038"][0]
    if program_038 is not exact_program or collection_038 != "tranches":
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", PROFILE_REGISTRY_PATH)
    if set(relation_038) != {*TERMINAL_RELATION_IDENTITY, "state"} or any(
        relation_038.get(key) != value
        for key, value in TERMINAL_RELATION_IDENTITY.items()
    ):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", PROFILE_REGISTRY_PATH)
    if relation_038.get("state") not in {"active", "done"}:
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)

    program_039, collection_039, relation_039 = relations["0039"][0]
    if (
        program_039 is not exact_program
        or collection_039 != "tranches"
        or set(relation_039) != {*TERMINAL_SUCCESSOR_IDENTITY, "state"}
        or any(
            relation_039.get(key) != value
            for key, value in TERMINAL_SUCCESSOR_IDENTITY.items()
        )
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    program_040, collection_040, relation_040 = relations["0040"][0]
    if (
        program_040 is not exact_program
        or collection_040 != "tranches"
        or set(relation_040) != {*TERMINAL_FRONTIER_IDENTITY, "state"}
        or any(
            relation_040.get(key) != value
            for key, value in TERMINAL_FRONTIER_IDENTITY.items()
        )
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)
    return relation_038, relation_039, relation_040


def _partition_terminal_controls(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    spec_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    registry: Mapping[str, Any],
) -> dict[str, Any]:
    for paths, path in (
        (plan_paths, TERMINAL_PLAN),
        (task_paths, TERMINAL_TASK),
        (spec_paths, TERMINAL_SPEC),
        (spec_paths, TERMINAL_SUCCESSOR_SPEC),
        (spec_paths, TERMINAL_FRONTIER_SPEC),
    ):
        count = paths.count(path)
        if count > 1:
            raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
        if count != 1:
            code = (
                "CLOSURE-TERMINAL-FRONTIER"
                if path in {TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC}
                else "CLOSURE-TERMINAL-INCOMPLETE"
            )
            raise ClosureError(code, path)

    metadata: dict[str, dict[str, str]] = {}
    expected_profiles = {
        TERMINAL_SPEC: "sdlc/spec",
        TERMINAL_PLAN: "sdlc/plan",
        TERMINAL_TASK: "sdlc/task",
        TERMINAL_SUCCESSOR_SPEC: "sdlc/spec",
        TERMINAL_FRONTIER_SPEC: "sdlc/spec",
    }
    for path, profile in expected_profiles.items():
        if path not in payloads:
            raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
        values = _frontmatter(_decode_text(payloads[path], path), path)
        if values.get("type") != profile or values.get("owner") != "platform":
            raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
        metadata[path] = values

    relation, successor_relation, frontier_relation = _terminal_registry_relations(
        registry
    )
    successor_state = metadata[TERMINAL_SUCCESSOR_SPEC].get("status")
    frontier_state = metadata[TERMINAL_FRONTIER_SPEC].get("status")
    if (
        frontier_state not in {"active", "done"}
        or frontier_relation.get("state") != frontier_state
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)
    if (
        successor_state not in {"active", "done"}
        or successor_relation.get("state") != successor_state
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if frontier_state == "done" and successor_state != "done":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)

    document_states = {
        metadata[path].get("status")
        for path in (TERMINAL_SPEC, TERMINAL_PLAN, TERMINAL_TASK)
    }
    if document_states not in ({"active"}, {"done"}):
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)
    state = next(iter(document_states))
    if relation.get("state") != state:
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)
    if state == "active" and successor_state != "active":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if state == "active" and frontier_state != "active":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)

    successor_controls_required = state == "done" or any(
        path in paths
        for path, paths in (
            (TERMINAL_SUCCESSOR_PLAN, plan_paths),
            (TERMINAL_SUCCESSOR_TASK, task_paths),
        )
    )
    if successor_controls_required:
        for paths, path, profile in (
            (plan_paths, TERMINAL_SUCCESSOR_PLAN, "sdlc/plan"),
            (task_paths, TERMINAL_SUCCESSOR_TASK, "sdlc/task"),
        ):
            count = paths.count(path)
            if count > 1:
                raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
            if count != 1:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            if path not in payloads:
                raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
            values = _frontmatter(_decode_text(payloads[path], path), path)
            if values.get("type") != profile or values.get("owner") != "platform":
                raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
            if values.get("status") != successor_state:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            metadata[path] = values

    frontier_controls_required = frontier_state == "done" or any(
        path in paths
        for path, paths in (
            (TERMINAL_FRONTIER_PLAN, plan_paths),
            (TERMINAL_FRONTIER_TASK, task_paths),
        )
    )
    if frontier_controls_required:
        for paths, path, profile in (
            (plan_paths, TERMINAL_FRONTIER_PLAN, "sdlc/plan"),
            (task_paths, TERMINAL_FRONTIER_TASK, "sdlc/task"),
        ):
            count = paths.count(path)
            if count > 1:
                raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
            if count != 1:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            if path not in payloads:
                raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
            values = _frontmatter(_decode_text(payloads[path], path), path)
            if values.get("type") != profile or values.get("owner") != "platform":
                raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
            if values.get("status") != frontier_state:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            metadata[path] = values

    result = {
        "planPaths": sorted(plan_paths),
        "taskPaths": sorted(task_paths),
        "specPaths": sorted(spec_paths),
        "terminalControlRows": [],
        "terminalControlPairCardinality": [],
        "terminalSpecRows": [],
    }
    if state == "active":
        return result

    terminal_plans = {TERMINAL_PLAN}
    terminal_tasks = {TERMINAL_TASK}
    if successor_state == "done":
        terminal_plans.add(TERMINAL_SUCCESSOR_PLAN)
        terminal_tasks.add(TERMINAL_SUCCESSOR_TASK)
    if frontier_state == "done":
        terminal_plans.add(TERMINAL_FRONTIER_PLAN)
        terminal_tasks.add(TERMINAL_FRONTIER_TASK)
    result["planPaths"] = sorted(
        path for path in plan_paths if path not in terminal_plans
    )
    result["taskPaths"] = sorted(
        path for path in task_paths if path not in terminal_tasks
    )
    terminal_specs = {TERMINAL_SPEC}
    if successor_state == "done":
        terminal_specs.add(TERMINAL_SUCCESSOR_SPEC)
    if frontier_state == "done":
        terminal_specs.add(TERMINAL_FRONTIER_SPEC)
    result["specPaths"] = sorted(
        path for path in spec_paths if path not in terminal_specs
    )
    terminal_control_paths = [
        (TERMINAL_PLAN, "plan", TERMINAL_LINEAGE),
        (TERMINAL_TASK, "task", TERMINAL_LINEAGE),
    ]
    if successor_state == "done":
        terminal_control_paths.extend(
            [
                (
                    TERMINAL_SUCCESSOR_PLAN,
                    "plan",
                    TERMINAL_SUCCESSOR_LINEAGE,
                ),
                (
                    TERMINAL_SUCCESSOR_TASK,
                    "task",
                    TERMINAL_SUCCESSOR_LINEAGE,
                ),
            ]
        )
    if frontier_state == "done":
        terminal_control_paths.extend(
            [
                (
                    TERMINAL_FRONTIER_PLAN,
                    "plan",
                    TERMINAL_FRONTIER_LINEAGE,
                ),
                (
                    TERMINAL_FRONTIER_TASK,
                    "task",
                    TERMINAL_FRONTIER_LINEAGE,
                ),
            ]
        )
    result["terminalControlRows"] = sorted(
        [
            {
                "path": path,
                "kind": kind,
                "lineageId": lineage,
                "profile": f"sdlc/{kind}",
                "status": "done",
                "owner": "platform",
                **_object_identity(path, index, payloads[path]),
            }
            for path, kind, lineage in terminal_control_paths
        ],
        key=lambda row: str(row["path"]),
    )
    result["terminalControlPairCardinality"] = [
        {
            "lineageId": TERMINAL_LINEAGE,
            "state": "complete",
            "planPath": TERMINAL_PLAN,
            "taskPath": TERMINAL_TASK,
            "owner": "platform",
            "status": "done",
        }
    ]
    result["terminalSpecRows"] = [
        {
            "path": TERMINAL_SPEC,
            "profile": "sdlc/spec",
            "status": "done",
            "owner": "platform",
            **_object_identity(TERMINAL_SPEC, index, payloads[TERMINAL_SPEC]),
            "registryPath": PROFILE_REGISTRY_PATH,
            "programPrd": "0006",
            "programAd": "0009",
            "relationClass": "original-tranche",
            **TERMINAL_RELATION_IDENTITY,
            "state": "done",
        }
    ]
    if successor_state == "done":
        result["terminalControlPairCardinality"].append(
            {
                "lineageId": TERMINAL_SUCCESSOR_LINEAGE,
                "state": "complete",
                "planPath": TERMINAL_SUCCESSOR_PLAN,
                "taskPath": TERMINAL_SUCCESSOR_TASK,
                "owner": "platform",
                "status": "done",
            }
        )
        result["terminalSpecRows"].append(
            {
                "path": TERMINAL_SUCCESSOR_SPEC,
                "profile": "sdlc/spec",
                "status": "done",
                "owner": "platform",
                **_object_identity(
                    TERMINAL_SUCCESSOR_SPEC,
                    index,
                    payloads[TERMINAL_SUCCESSOR_SPEC],
                ),
                "registryPath": PROFILE_REGISTRY_PATH,
                "programPrd": "0006",
                "programAd": "0009",
                "relationClass": "original-tranche",
                **TERMINAL_SUCCESSOR_IDENTITY,
                "state": "done",
            }
        )
    if frontier_state == "done":
        result["terminalControlPairCardinality"].append(
            {
                "lineageId": TERMINAL_FRONTIER_LINEAGE,
                "state": "complete",
                "planPath": TERMINAL_FRONTIER_PLAN,
                "taskPath": TERMINAL_FRONTIER_TASK,
                "owner": "platform",
                "status": "done",
            }
        )
        result["terminalSpecRows"].append(
            {
                "path": TERMINAL_FRONTIER_SPEC,
                "profile": "sdlc/spec",
                "status": "done",
                "owner": "platform",
                **_object_identity(
                    TERMINAL_FRONTIER_SPEC,
                    index,
                    payloads[TERMINAL_FRONTIER_SPEC],
                ),
                "registryPath": PROFILE_REGISTRY_PATH,
                "programPrd": "0006",
                "programAd": "0009",
                "relationClass": "original-tranche",
                **TERMINAL_FRONTIER_IDENTITY,
                "state": "done",
            }
        )
    return result


def _build_active_control_rows(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for kind, paths in (("plan", plan_paths), ("task", task_paths)):
        for path in paths:
            payload = payloads[path]
            metadata = _frontmatter(_decode_text(payload, path), path)
            if (
                metadata.get("type") != f"sdlc/{kind}"
                or metadata.get("owner") != "platform"
            ):
                raise ClosureError("CLOSURE-ACTIVE-CONTROL-AUTHORITY", path)
            if metadata.get("status") != "active":
                raise ClosureError("CLOSURE-ACTIVE-CONTROL-STATUS", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": _active_control_lineage(path, kind),
                    "profile": metadata.get("type"),
                    "status": "active",
                    "owner": "platform",
                    **_object_identity(path, index, payload),
                }
            )
    return sorted(entries, key=lambda row: str(row["path"]))


def _build_active_control_pairs(
    active: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in active:
        lineage = row.get("lineageId")
        kind = row.get("kind")
        if (
            not isinstance(lineage, str)
            or ACTIVE_CONTROL_LINEAGE.fullmatch(lineage) is None
            or kind not in {"plan", "task"}
        ):
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", row.get("path"))
        if kind in grouped[lineage]:
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-DUPLICATE", row.get("path"))
        grouped[lineage][str(kind)] = row
    pairs: list[dict[str, Any]] = []
    for lineage, members in sorted(grouped.items()):
        if set(members) != {"plan", "task"}:
            member = next(iter(members.values()))
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-PAIR", member.get("path"))
        pairs.append(
            {
                "lineageId": lineage,
                "state": "complete",
                "planPath": members["plan"]["path"],
                "taskPath": members["task"]["path"],
                "owner": "platform",
                "status": "active",
            }
        )
    return pairs


def _validate_terminal_frontier_shape(observed: Mapping[str, Any]) -> str:
    """Reject every production frontier other than the three closed shapes."""

    control_keys = {
        "path",
        "kind",
        "lineageId",
        "profile",
        "status",
        "owner",
        "objectMode",
        "objectId",
    }
    projected_control_keys = control_keys | {"legacySource", "indexedTarget"}
    pair_keys = {
        "lineageId",
        "state",
        "planPath",
        "taskPath",
        "owner",
        "status",
    }
    spec_keys = {
        "path",
        "profile",
        "status",
        "owner",
        "objectMode",
        "objectId",
        "registryPath",
        "programPrd",
        "programAd",
        "relationClass",
        "spec",
        "order",
        "reason",
        "decision",
        "state",
    }
    families = (
        {
            "specPath": TERMINAL_SPEC,
            "planPath": TERMINAL_PLAN,
            "taskPath": TERMINAL_TASK,
            "lineageId": TERMINAL_LINEAGE,
            "relation": TERMINAL_RELATION_IDENTITY,
        },
        {
            "specPath": TERMINAL_SUCCESSOR_SPEC,
            "planPath": TERMINAL_SUCCESSOR_PLAN,
            "taskPath": TERMINAL_SUCCESSOR_TASK,
            "lineageId": TERMINAL_SUCCESSOR_LINEAGE,
            "relation": TERMINAL_SUCCESSOR_IDENTITY,
        },
        {
            "specPath": TERMINAL_FRONTIER_SPEC,
            "planPath": TERMINAL_FRONTIER_PLAN,
            "taskPath": TERMINAL_FRONTIER_TASK,
            "lineageId": TERMINAL_FRONTIER_LINEAGE,
            "relation": TERMINAL_FRONTIER_IDENTITY,
        },
    )

    def rows_for(key: str) -> list[Mapping[str, Any]]:
        rows = observed.get(key)
        if not isinstance(rows, list) or any(
            not isinstance(row, Mapping) for row in rows
        ):
            raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)
        return rows

    active_rows = rows_for("activeControlRows")
    active_pairs = rows_for("activeControlPairCardinality")
    terminal_rows = rows_for("terminalControlRows")
    terminal_pairs = rows_for("terminalControlPairCardinality")
    terminal_specs = rows_for("terminalSpecRows")
    terminal_authority = rows_for("terminalProgramClosureAuthority")

    spec_paths = tuple(row.get("path") for row in terminal_specs)
    modes = {
        (TERMINAL_SPEC,): ("current", 1),
        (TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC): ("advanced", 2),
        (
            TERMINAL_SPEC,
            TERMINAL_SUCCESSOR_SPEC,
            TERMINAL_FRONTIER_SPEC,
        ): ("terminal", 3),
    }
    mode = modes.get(spec_paths)
    if mode is None:
        unexpected = next(
            (
                path
                for path in spec_paths
                if is_safe_path(path)
                and path
                not in {
                    TERMINAL_SPEC,
                    TERMINAL_SUCCESSOR_SPEC,
                    TERMINAL_FRONTIER_SPEC,
                }
            ),
            TERMINAL_FRONTIER_SPEC,
        )
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", unexpected)
    mode_name, done_count = mode
    terminal_families = families[:done_count]
    active_families = families[done_count : done_count + 1]

    def object_id_is_git(row: Mapping[str, Any]) -> bool:
        value = row.get("objectId")
        if not isinstance(value, str):
            return False
        parts = value.split(":")
        return (
            len(parts) == 3
            and parts[0] == "git"
            and parts[1] in {"sha1", "sha256"}
            and FULL_OID.fullmatch(parts[2]) is not None
            and (parts[1] == "sha1") == (len(parts[2]) == 40)
        )

    def object_identity_is_indexed(row: Mapping[str, Any]) -> bool:
        return row.get("objectMode") == "index-stage-zero" and object_id_is_git(row)

    def control_identity_is_valid(row: Mapping[str, Any]) -> bool:
        path = row.get("path")
        indexed_target = TERMINAL_CONTROL_REPLACEMENTS.get(str(path))
        if indexed_target is None:
            return set(row) == control_keys and object_identity_is_indexed(row)
        return (
            set(row) == projected_control_keys
            and row.get("objectMode") == "projected-replacement"
            and row.get("legacySource") == path
            and row.get("indexedTarget") == indexed_target
            and object_id_is_git(row)
        )

    def control_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if not control_identity_is_valid(row):
            return None
        return (
            row.get("path"),
            row.get("kind"),
            row.get("lineageId"),
            row.get("profile"),
            row.get("status"),
            row.get("owner"),
        )

    def expected_control_rows(
        selected: Sequence[Mapping[str, Any]], status: str
    ) -> list[tuple[Any, ...]]:
        return sorted(
            [
                (
                    family[f"{kind}Path"],
                    kind,
                    family["lineageId"],
                    f"sdlc/{kind}",
                    status,
                    "platform",
                )
                for family in selected
                for kind in ("plan", "task")
            ],
            key=lambda row: str(row[0]),
        )

    def pair_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if set(row) != pair_keys:
            return None
        return (
            row.get("lineageId"),
            row.get("state"),
            row.get("planPath"),
            row.get("taskPath"),
            row.get("owner"),
            row.get("status"),
        )

    def expected_pairs(
        selected: Sequence[Mapping[str, Any]], status: str
    ) -> list[tuple[Any, ...]]:
        return [
            (
                family["lineageId"],
                "complete",
                family["planPath"],
                family["taskPath"],
                "platform",
                status,
            )
            for family in selected
        ]

    def spec_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if set(row) != spec_keys or not object_identity_is_indexed(row):
            return None
        return (
            row.get("path"),
            row.get("profile"),
            row.get("status"),
            row.get("owner"),
            row.get("registryPath"),
            row.get("programPrd"),
            row.get("programAd"),
            row.get("relationClass"),
            row.get("spec"),
            row.get("order"),
            row.get("reason"),
            row.get("decision"),
            row.get("state"),
        )

    def expected_specs(
        selected: Sequence[Mapping[str, Any]],
    ) -> list[tuple[Any, ...]]:
        return [
            (
                family["specPath"],
                "sdlc/spec",
                "done",
                "platform",
                PROFILE_REGISTRY_PATH,
                "0006",
                "0009",
                "original-tranche",
                family["relation"]["spec"],
                family["relation"]["order"],
                family["relation"]["reason"],
                family["relation"]["decision"],
                "done",
            )
            for family in selected
        ]

    expected_active_rows = expected_control_rows(active_families, "active")
    expected_terminal_rows = expected_control_rows(terminal_families, "done")
    expected_active_pairs = expected_pairs(active_families, "active")
    expected_terminal_pairs = expected_pairs(terminal_families, "done")
    expected_terminal_specs = expected_specs(terminal_families)

    def failure_path(
        rows: Sequence[Mapping[str, Any]],
        expected_paths: set[str],
        *,
        pair: bool = False,
    ) -> str:
        fields = ("planPath", "taskPath") if pair else ("path",)
        actual_paths = {
            row.get(field)
            for row in rows
            for field in fields
            if is_safe_path(row.get(field))
        }
        unexpected = sorted(actual_paths - expected_paths)
        if unexpected:
            return unexpected[0]
        missing = sorted(expected_paths - actual_paths)
        if missing:
            return missing[0]
        return next(iter(sorted(actual_paths)), TERMINAL_FRONTIER_SPEC)

    comparisons = (
        (
            [control_signature(row) for row in active_rows],
            expected_active_rows,
            active_rows,
            {str(row[0]) for row in expected_active_rows},
            False,
        ),
        (
            [pair_signature(row) for row in active_pairs],
            expected_active_pairs,
            active_pairs,
            {str(path) for row in expected_active_pairs for path in (row[2], row[3])},
            True,
        ),
        (
            [control_signature(row) for row in terminal_rows],
            expected_terminal_rows,
            terminal_rows,
            {str(row[0]) for row in expected_terminal_rows},
            False,
        ),
        (
            [pair_signature(row) for row in terminal_pairs],
            expected_terminal_pairs,
            terminal_pairs,
            {str(path) for row in expected_terminal_pairs for path in (row[2], row[3])},
            True,
        ),
        (
            [spec_signature(row) for row in terminal_specs],
            expected_terminal_specs,
            terminal_specs,
            {str(row[0]) for row in expected_terminal_specs},
            False,
        ),
    )
    for actual, expected, rows, paths, pair in comparisons:
        if actual != expected:
            raise ClosureError(
                "CLOSURE-TERMINAL-FRONTIER",
                failure_path(rows, paths, pair=pair),
            )
    expected_terminal_authority = (
        [
            (
                TERMINAL_PROGRAM_CLOSURE_ADR,
                "sdlc/adr",
                "accepted",
                "platform",
                "terminal-program-closure-decision",
                TERMINAL_FRONTIER_SPEC,
            )
        ]
        if mode_name == "terminal"
        else []
    )
    actual_terminal_authority: list[tuple[Any, ...] | None] = []
    for row in terminal_authority:
        if set(row) != {
            "path",
            "profile",
            "status",
            "owner",
            "objectMode",
            "objectId",
            "authorityRole",
            "frontierSpecPath",
        } or not object_identity_is_indexed(row):
            actual_terminal_authority.append(None)
            continue
        actual_terminal_authority.append(
            (
                row.get("path"),
                row.get("profile"),
                row.get("status"),
                row.get("owner"),
                row.get("authorityRole"),
                row.get("frontierSpecPath"),
            )
        )
    if actual_terminal_authority != expected_terminal_authority:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return mode_name


def _build_pairs(current: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in current:
        pair_key = row.get("lineageId")
        kind = row.get("kind")
        if (
            not isinstance(pair_key, str)
            or not pair_key
            or kind not in {"plan", "task"}
        ):
            raise ClosureError("CLOSURE-PAIR-KEY", row.get("path"))
        if kind in grouped[pair_key]:
            raise ClosureError("CLOSURE-PAIR-DUPLICATE", row.get("path"))
        grouped[pair_key][str(kind)] = row
    entries: list[dict[str, Any]] = []
    for pair_key, members in sorted(grouped.items()):
        state = (
            "complete"
            if set(members) == {"plan", "task"}
            else "plan-only"
            if "plan" in members
            else "task-only"
        )
        dispositions = {str(row.get("disposition")) for row in members.values()}
        if len(dispositions) != 1:
            raise ClosureError("CLOSURE-PAIR-DISPOSITION")
        disposition = next(iter(dispositions))
        if state != "complete" and (
            disposition != "DEFER"
            or any(row.get("owner") != "platform" for row in members.values())
        ):
            raise ClosureError("CLOSURE-PAIR-PARTIAL")
        entries.append(
            {
                "lineageId": pair_key,
                "state": state,
                "planPath": members.get("plan", {}).get("path"),
                "taskPath": members.get("task", {}).get("path"),
                "disposition": disposition,
                "owner": "platform",
                "partialEvidence": "explicit-owned-DEFER"
                if state != "complete"
                else None,
            }
        )
    return entries


def _build_migrations(
    eligibility: Mapping[str, Any],
    migration: Mapping[str, Any],
    current_paths: set[str],
    archive_paths: set[str],
    transition_archive_paths: frozenset[str] = frozenset(),
    archive_aliases: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    candidates = eligibility.get("candidateRows")
    batches = migration.get("batches")
    if not isinstance(candidates, list) or not isinstance(batches, list):
        raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
    eligible = {
        row.get("path"): row
        for row in candidates
        if isinstance(row, Mapping) and row.get("disposition") == "eligible"
    }
    result_by_path: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for batch in batches:
        if not isinstance(batch, Mapping) or not isinstance(batch.get("records"), list):
            raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
        for record in batch["records"]:
            if not isinstance(record, Mapping) or not isinstance(
                record.get("originalPath"), str
            ):
                raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
            original = record["originalPath"]
            if original in result_by_path:
                raise ClosureError("CLOSURE-MIGRATION-DUPLICATE", original)
            result_by_path[original] = (batch, record)
    if set(result_by_path) != set(eligible):
        raise ClosureError("CLOSURE-MIGRATION-STALE")
    expected_candidate_archives = {
        path.replace("docs/04.execution/", "docs/98.archive/04.execution/")
        for path in eligible
    }
    candidate_paths = {
        row.get("path") for row in candidates if isinstance(row, Mapping)
    }
    aliases = dict(archive_aliases or {})
    stable_to_legacy = {stable: legacy for legacy, stable in aliases.items()}
    if len(stable_to_legacy) != len(aliases):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    observed_candidate_archives = {
        stable_to_legacy.get(archive, archive)
        for archive in archive_paths
        if archive not in transition_archive_paths
        if stable_to_legacy.get(archive, archive).replace(
            "docs/98.archive/04.execution/", "docs/04.execution/"
        )
        in candidate_paths
    }
    if observed_candidate_archives != expected_candidate_archives:
        raise ClosureError("CLOSURE-MIGRATION-ROGUE")
    entries: list[dict[str, Any]] = []
    for path, source in sorted(eligible.items()):
        batch, record = result_by_path[path]
        archive_path = record.get("archivePath")
        if not isinstance(archive_path, str):
            raise ClosureError("CLOSURE-MIGRATION-SCOPE", path)
        indexed_archive_path = aliases.get(archive_path, archive_path)
        if path in current_paths:
            raise ClosureError("CLOSURE-MIGRATION-SOURCE", path)
        if indexed_archive_path not in archive_paths:
            raise ClosureError("CLOSURE-MIGRATION-ARCHIVE", archive_path)
        if not (
            path.startswith((f"{PLAN_ROOT}/", f"{TASK_ROOT}/"))
            and archive_path.startswith(
                (f"{ARCHIVE_PLAN_ROOT}/", f"{ARCHIVE_TASK_ROOT}/")
            )
        ):
            raise ClosureError("CLOSURE-MIGRATION-SCOPE", path)
        if (
            source.get("owner") != "platform"
            or not source.get("reason")
            or not batch.get("rollbackParentCommit")
            or not batch.get("currentClosureOwner")
            or record.get("validationResult") != "PASS"
            or record.get("archiveReason") != "completed-lineage"
        ):
            raise ClosureError("CLOSURE-MIGRATION-EVIDENCE", path)
        entries.append(
            {
                "path": path,
                "kind": source.get("kind"),
                "lineageId": source.get("pairKey"),
                "sourceCommit": _git_identity(str(source.get("sourceCommit"))),
                "sourceBlob": _git_identity(str(source.get("sourceBlob"))),
                "historicalDisposition": "eligible",
                "historicalReason": source.get("reason"),
                "disposition": "migrated-closed",
                "owner": "platform",
                "closureReason": "exact-atomic-migration-result-joined",
                "batchId": batch.get("batchId"),
                "batchSequence": batch.get("sequence"),
                "archivePath": archive_path,
                "payloadBytes": record.get("payloadBytes"),
                "payloadSha256": _sha256_identity(record.get("payloadSha256")),
                "archiveReason": record.get("archiveReason"),
                "currentClosureOwner": batch.get("currentClosureOwner"),
                "rollbackParentCommit": _git_identity(
                    str(batch.get("rollbackParentCommit"))
                ),
                "validationResult": record.get("validationResult"),
                "currentSourcePresent": False,
                "archivePresent": True,
            }
        )
    return entries


def _authority_entries(
    paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    *,
    kind: str,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    expected_type = f"sdlc/{kind}"
    expected_status = "accepted" if kind == "adr" else "done"
    authority = ADR_AUTHORITY if kind == "adr" else SPEC_AUTHORITY
    trigger = (
        "accepted-adr-authority-or-evidence-change"
        if kind == "adr"
        else "done-spec-authority-or-evidence-change"
    )
    for path in paths:
        payload = payloads[path]
        metadata = _frontmatter(_decode_text(payload, path), path)
        if metadata.get("status") != expected_status:
            continue
        if metadata.get("type") != expected_type or metadata.get("owner") != "platform":
            raise ClosureError("CLOSURE-AUTHORITY-PROFILE", path)
        entries.append(
            {
                "path": path,
                "profile": expected_type,
                "status": expected_status,
                "owner": "platform",
                **_work108_authority_object_identity(path, index, payload),
                "disposition": "retain",
                "reason": AUTHORITY_REASON,
                "currentAuthority": authority,
                "refreshTrigger": trigger,
            }
        )
    return entries


def _frozen_authority_scope(
    paths: Sequence[str],
    *,
    kind: str,
) -> list[str]:
    """Select the exact PRD-0006 authority paths and ignore later programs."""

    if kind == "adr":
        owned = FROZEN_ACCEPTED_ADR_PATHS
    elif kind == "spec":
        owned = FROZEN_DONE_SPEC_PATHS
    else:
        raise ValueError(f"unsupported frozen authority kind: {kind}")
    counts = Counter(paths)
    for path in owned:
        if counts[path] != 1:
            raise ClosureError("CLOSURE-AUTHORITY-SCOPE", path)
    return list(owned)


def _frozen_authority_entries(
    paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    *,
    kind: str,
) -> list[dict[str, Any]]:
    """Build only the exact PRD-0006 authority rows and require their state."""

    scoped_paths = _frozen_authority_scope(paths, kind=kind)
    entries = _authority_entries(scoped_paths, index, payloads, kind=kind)
    entries_by_path = {row["path"] for row in entries}
    for path in scoped_paths:
        if path not in entries_by_path:
            raise ClosureError("CLOSURE-AUTHORITY-SCOPE", path)
    allowed_later = (
        POST_CLOSURE_ADR_AUTHORITY_PATHS
        if kind == "adr"
        else POST_CLOSURE_SPEC_AUTHORITY_PATHS
    )
    frozen_paths = frozenset(scoped_paths)
    later_authority = _authority_entries(
        [path for path in paths if path not in frozen_paths],
        index,
        payloads,
        kind=kind,
    )
    for row in later_authority:
        if row["path"] not in allowed_later:
            raise ClosureError("CLOSURE-AUTHORITY-SCOPE", row["path"])
        pinned_blob = POST_CLOSURE_PINNED_AUTHORITY_BLOBS.get(row["path"])
        if pinned_blob is not None and row["objectId"] != _git_identity(pinned_blob):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT", row["path"])
    return entries


def _terminal_program_closure_authority(
    adr_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    terminal_spec_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Classify ADR-0020 only at the exact closed Spec 040 frontier."""

    final_frontier = tuple(row.get("path") for row in terminal_spec_rows) == (
        TERMINAL_SPEC,
        TERMINAL_SUCCESSOR_SPEC,
        TERMINAL_FRONTIER_SPEC,
    )
    if not final_frontier:
        return []
    if (
        adr_paths.count(TERMINAL_PROGRAM_CLOSURE_ADR) != 1
        or TERMINAL_PROGRAM_CLOSURE_ADR not in payloads
    ):
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    payload = payloads[TERMINAL_PROGRAM_CLOSURE_ADR]
    metadata = _frontmatter(
        _decode_text(payload, TERMINAL_PROGRAM_CLOSURE_ADR),
        TERMINAL_PROGRAM_CLOSURE_ADR,
    )
    if {
        "type": metadata.get("type"),
        "status": metadata.get("status"),
        "owner": metadata.get("owner"),
    } != {
        "type": "sdlc/adr",
        "status": "accepted",
        "owner": "platform",
    }:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return [
        {
            "path": TERMINAL_PROGRAM_CLOSURE_ADR,
            "profile": "sdlc/adr",
            "status": "accepted",
            "owner": "platform",
            **_object_identity(TERMINAL_PROGRAM_CLOSURE_ADR, index, payload),
            "authorityRole": "terminal-program-closure-decision",
            "frontierSpecPath": TERMINAL_FRONTIER_SPEC,
        }
    ]


def _generic_adr_authority_paths(
    adr_paths: Sequence[str],
    terminal_program_closure_authority: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Keep every accepted ADR generic except exact final ADR-0020 authority."""

    if not terminal_program_closure_authority:
        return list(adr_paths)
    if [row.get("path") for row in terminal_program_closure_authority] != [
        TERMINAL_PROGRAM_CLOSURE_ADR
    ]:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return [path for path in adr_paths if path != TERMINAL_PROGRAM_CLOSURE_ADR]


def _validate_repository_archive_projection(migration: Mapping[str, Any]) -> None:
    if migration.get("repositoryArchive") != {
        "contractVersion": 2,
        "managedNamespaces": ["arwb-base", "acer-additive"],
        "managedRecords": 43,
        "repositoryRecords": 93,
    }:
        raise ClosureError("CLOSURE-TAXONOMY-PROJECTION", SOURCE_PATHS[2])


def _validate_source_ledger_transition(
    ledger_sources: Any,
    observed_sources: Any,
    transition: Sequence[Mapping[str, Any]],
) -> None:
    if not transition:
        if ledger_sources != observed_sources:
            raise ClosureError("CLOSURE-SOURCE-DRIFT")
        return
    if not isinstance(ledger_sources, list) or not isinstance(observed_sources, list):
        raise ClosureError("CLOSURE-SOURCE-DRIFT")
    ledger_by_path = {
        row.get("path"): row for row in ledger_sources if isinstance(row, Mapping)
    }
    observed_by_path = {
        row.get("path"): row for row in observed_sources if isinstance(row, Mapping)
    }
    if (
        len(ledger_by_path) != len(SOURCE_PATHS)
        or len(observed_by_path) != len(SOURCE_PATHS)
        or tuple(row.get("path") for row in ledger_sources) != SOURCE_PATHS
        or tuple(row.get("path") for row in observed_sources) != SOURCE_PATHS
    ):
        raise ClosureError("CLOSURE-SOURCE-DRIFT")
    migration_path = SOURCE_PATHS[2]
    for path in SOURCE_PATHS:
        if path == migration_path:
            continue
        if ledger_by_path[path] != observed_by_path[path]:
            raise ClosureError("CLOSURE-SOURCE-DRIFT", path)
    ledger_migration = ledger_by_path[migration_path]
    observed_migration = observed_by_path[migration_path]
    expected_common = {
        "path": migration_path,
        "schema": SOURCE_SCHEMAS[migration_path],
    }
    if (
        {key: ledger_migration.get(key) for key in expected_common} != expected_common
        or {key: observed_migration.get(key) for key in expected_common}
        != expected_common
        or ledger_migration.get("objectId")
        != _git_identity(FROZEN_MIGRATION_RESULTS_BLOB)
        or observed_migration.get("objectId")
        != _git_identity(TRANSITION_MIGRATION_RESULTS_BLOB)
        or set(ledger_migration) != {*expected_common, "objectId"}
        or set(observed_migration) != {*expected_common, "objectId"}
    ):
        raise ClosureError("CLOSURE-SOURCE-DRIFT", migration_path)


def _validate_transition_authority_semantics(
    payloads: Mapping[str, bytes], taxonomy_sources: frozenset[str]
) -> None:
    if set(TRANSITION_AUTHORITY_REMAPS) != set(TRANSITION_AUTHORITY_BLOBS):
        raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
    for authority_path, remaps in TRANSITION_AUTHORITY_REMAPS.items():
        retired_sources = {source for source, _replacement in remaps}
        if not retired_sources.issubset(taxonomy_sources):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT", authority_path)
        payload = payloads.get(authority_path)
        if not isinstance(payload, bytes):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT", authority_path)
        text = _decode_text(payload, authority_path)
        start = posixpath.dirname(authority_path)
        expected_targets = Counter(replacement for _source, replacement in remaps)
        for replacement, expected_count in expected_targets.items():
            replacement_target = posixpath.relpath(replacement, start)
            if text.count(f"]({replacement_target})") != expected_count:
                raise ClosureError("CLOSURE-AUTHORITY-DRIFT", authority_path)
        for retired_source in retired_sources:
            retired_target = posixpath.relpath(retired_source, start)
            if f"]({retired_target})" in text:
                raise ClosureError("CLOSURE-AUTHORITY-DRIFT", authority_path)


def _validate_authority_guard_transition(
    ledger_guards: Any,
    observed_guards: Any,
    transition: Sequence[Mapping[str, Any]],
) -> None:
    if not transition:
        if ledger_guards != observed_guards:
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
        return
    if (
        not isinstance(ledger_guards, Mapping)
        or not isinstance(observed_guards, Mapping)
        or set(ledger_guards) != {"acceptedAdrs", "doneSpecs"}
        or set(observed_guards) != {"acceptedAdrs", "doneSpecs"}
    ):
        raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
    admitted_transition: set[str] = set()
    admitted_work105: set[str] = set()
    for key in ("acceptedAdrs", "doneSpecs"):
        ledger_rows = ledger_guards[key]
        observed_rows = observed_guards[key]
        if not isinstance(ledger_rows, list) or not isinstance(observed_rows, list):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
        ledger_by_path = {
            WORK105_CURRENT_PATHS_BY_HISTORICAL.get(
                row.get("path"), row.get("path")
            ): row
            for row in ledger_rows
            if isinstance(row, Mapping)
        }
        observed_by_path = {
            row.get("path"): row for row in observed_rows if isinstance(row, Mapping)
        }
        if (
            len(ledger_by_path) != len(ledger_rows)
            or len(observed_by_path) != len(observed_rows)
            or set(ledger_by_path) != set(observed_by_path)
        ):
            raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
        for path, ledger_row in ledger_by_path.items():
            observed_row = observed_by_path[path]
            work105_blobs = WORK105_AUTHORITY_BLOBS.get(path)
            if work105_blobs is None:
                raise ClosureError("CLOSURE-AUTHORITY-DRIFT", path)
            admitted_work105.add(path)
            work105_base_blob, current_blob = work105_blobs
            transition_blobs = TRANSITION_AUTHORITY_BLOBS.get(path)
            if transition_blobs is None:
                old_blob = work105_base_blob
                transition_blob = work105_base_blob
            else:
                admitted_transition.add(path)
                old_blob, transition_blob = transition_blobs
            if (
                work105_base_blob != transition_blob
                or ledger_row.get("objectId") != _git_identity(old_blob)
                or observed_row.get("objectId") != _git_identity(current_blob)
                or {
                    key: path if key == "path" else value
                    for key, value in ledger_row.items()
                    if key != "objectId"
                }
                != {
                    key: value
                    for key, value in observed_row.items()
                    if key != "objectId"
                }
            ):
                raise ClosureError("CLOSURE-AUTHORITY-DRIFT", path)
    if admitted_transition != set(
        TRANSITION_AUTHORITY_BLOBS
    ) or admitted_work105 != set(WORK105_AUTHORITY_BLOBS):
        raise ClosureError("CLOSURE-AUTHORITY-DRIFT")


def build_observed(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, Any]:
    normalized = _normalize_root(root)
    if _git(normalized, ("cat-file", "-t", FIXED_INPUT_COMMIT), runner) != b"commit\n":
        raise ClosureError("CLOSURE-FIXED-COMMIT", ".git")
    if _git(normalized, ("cat-file", "-t", WORK105_BASE_COMMIT), runner) != b"commit\n":
        raise ClosureError("CLOSURE-FIXED-COMMIT", ".git")
    _work105_base_projection(normalized, runner)
    registry = _load_registry_authority(normalized, runner)
    taxonomy_index = _taxonomy_manifest_inventory(normalized, runner)
    if taxonomy_index.get(TAXONOMY_MANIFEST_PATH) != TAXONOMY_MANIFEST_BLOB:
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
    taxonomy_manifest = _load_json_bytes(
        _proposed_or_index_bytes(
            normalized,
            TAXONOMY_MANIFEST_PATH,
            taxonomy_index,
            runner,
        ),
        TAXONOMY_MANIFEST_PATH,
    )
    source_index = _source_index(normalized, runner)
    sources: dict[str, Any] = {}
    source_rows: list[dict[str, Any]] = []
    for path in SOURCE_PATHS:
        document = _load_json_bytes(
            _proposed_or_index_bytes(normalized, path, source_index, runner), path
        )
        if (
            not isinstance(document, Mapping)
            or document.get("$schema") != SOURCE_SCHEMAS[path]
        ):
            raise ClosureError("CLOSURE-SOURCE-SCHEMA", path)
        sources[path] = document
        source_rows.append(
            {
                "path": path,
                "schema": SOURCE_SCHEMAS[path],
                "objectId": _git_identity(source_index[path]),
            }
        )
    census, eligibility, migration, role_audit = (
        sources[path] for path in SOURCE_PATHS
    )
    if (
        census.get("candidateBaseline", {}).get("candidateCounts", {}).get("total")
        != 110
        or eligibility.get("counts")
        != {"candidates": 110, "eligible": 12, "DEFER": 98, "retain": 2, "residue": 0}
        or migration.get("counts", {}).get("batches") != 6
        or migration.get("counts", {}).get("records") != 12
    ):
        raise ClosureError("CLOSURE-SOURCE-COUNTS")
    _validate_repository_archive_projection(migration)

    inventories = {
        scope: _inventory(normalized, scope, runner) for scope in INVENTORY_ROOTS
    }
    combined_index: dict[str, str] = {}
    inventory_payloads: dict[str, bytes] = {}
    for paths, modes in inventories.values():
        overlap = set(combined_index) & set(modes)
        if overlap:
            raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", next(iter(overlap)))
        combined_index.update(modes)
        for path in paths:
            if path in inventory_payloads:
                raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", path)
            inventory_payloads[path] = _proposed_or_index_bytes(
                normalized, path, modes, runner
            )
    plan_paths = _authored_stage04(inventories[PLAN_ROOT][0], PLAN_ROOT)
    task_paths = _authored_stage04(inventories[TASK_ROOT][0], TASK_ROOT)
    archive_paths = {
        path
        for scope in (ARCHIVE_CHANGES_ROOT, ARCHIVE_TOMBSTONES_ROOT)
        for path in inventories[scope][0]
        if path.endswith(".md")
    }
    migration_payload = inventory_payloads.get(WORK107_MIGRATION_PATH)
    if not isinstance(migration_payload, bytes):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    archive_aliases = _work107_archive_aliases(migration_payload)
    if set(archive_paths) != set(archive_aliases.values()):
        raise ClosureError("CLOSURE-TAXONOMY-NAMESPACE", WORK107_MIGRATION_PATH)
    raw_taxonomy_entries = taxonomy_manifest.get("entries")
    if not isinstance(raw_taxonomy_entries, list) or any(
        not isinstance(entry, Mapping) or not is_safe_path(entry.get("source"))
        for entry in raw_taxonomy_entries
    ):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
    taxonomy_source_tree = _taxonomy_source_tree(
        normalized,
        {str(entry["source"]) for entry in raw_taxonomy_entries},
        runner,
    )
    taxonomy_archive_entries = [
        entry
        for entry in raw_taxonomy_entries
        if entry.get("disposition") == "archive-unique"
    ]
    taxonomy_archive_recoveries = _taxonomy_archive_recoveries(
        normalized,
        taxonomy_archive_entries,
        taxonomy_source_tree,
        runner,
    )
    taxonomy_transition = _build_taxonomy_transition_closure(
        registry,
        taxonomy_manifest,
        eligibility,
        set(inventory_payloads),
        inventory_payloads,
        combined_index,
        taxonomy_source_tree,
        taxonomy_archive_recoveries,
        archive_aliases,
    )
    taxonomy_sources = frozenset(row["path"] for row in taxonomy_transition)
    taxonomy_archives = frozenset(
        row["archivePath"]
        for row in taxonomy_transition
        if row["disposition"] == "manifest-archive-closed"
    )
    _validate_transition_authority_semantics(inventory_payloads, taxonomy_sources)
    current = _build_current_rows(
        plan_paths,
        task_paths,
        combined_index,
        inventory_payloads,
        eligibility,
        taxonomy_sources,
    )
    pairs = _build_pairs(current)
    spec_paths = [
        path for path in inventories[SPEC_ROOT][0] if path.endswith("/spec.md")
    ]
    terminal_index, terminal_payloads = _project_terminal_control_replacements(
        combined_index, inventory_payloads
    )
    terminal = _partition_terminal_controls(
        _terminal_program_control_scope(
            [
                path
                for path in TERMINAL_PROGRAM_PLAN_PATHS
                if TERMINAL_CONTROL_REPLACEMENTS[path] in inventory_payloads
            ],
            kind="plan",
        ),
        _terminal_program_control_scope(
            [
                path
                for path in TERMINAL_PROGRAM_TASK_PATHS
                if TERMINAL_CONTROL_REPLACEMENTS[path] in inventory_payloads
            ],
            kind="task",
        ),
        spec_paths,
        terminal_index,
        terminal_payloads,
        registry,
    )
    active_controls = _build_active_control_rows(
        terminal["planPaths"],
        terminal["taskPaths"],
        terminal_index,
        terminal_payloads,
    )
    active_control_pairs = _build_active_control_pairs(active_controls)
    migrated = _build_migrations(
        eligibility,
        migration,
        {row["path"] for row in current},
        archive_paths,
        taxonomy_archives,
        archive_aliases,
    )

    adr_paths = [
        path
        for path in inventories[ADR_ROOT][0]
        if path.endswith(".md") and path != f"{ADR_ROOT}/README.md"
    ]
    terminal_program_closure_authority = _terminal_program_closure_authority(
        adr_paths,
        combined_index,
        inventory_payloads,
        terminal["terminalSpecRows"],
    )
    generic_adr_paths = _generic_adr_authority_paths(
        adr_paths,
        terminal_program_closure_authority,
    )
    accepted_adrs = _frozen_authority_entries(
        generic_adr_paths,
        combined_index,
        inventory_payloads,
        kind="adr",
    )
    done_specs = _frozen_authority_entries(
        terminal["specPaths"],
        combined_index,
        inventory_payloads,
        kind="spec",
    )
    migrated_paths = {row["path"] for row in migrated} | {
        row["archivePath"] for row in migrated
    }
    if migrated_paths & (
        {row["path"] for row in accepted_adrs} | {row["path"] for row in done_specs}
    ):
        raise ClosureError("CLOSURE-AUTHORITY-MOVED")

    role_stage = role_audit.get("stage05", {}).get("finalCounts", {}).get("total")
    role_helpers = role_audit.get("helperTests", {}).get("finalCounts", {}).get("total")
    role_findings = role_audit.get("findings")
    if (
        role_stage != 24
        or role_helpers != 33
        or not isinstance(role_findings, Mapping)
        or any(value for value in role_findings.values())
    ):
        raise ClosureError("CLOSURE-ACER004", SOURCE_PATHS[3])
    dependency = {
        "path": SOURCE_PATHS[3],
        "objectId": _git_identity(source_index[SOURCE_PATHS[3]]),
        "stage05Authored": 24,
        "helperTests": 33,
        "roleAuditFindings": 0,
        "status": "satisfied",
        "requiredForClosure": True,
    }

    pair_counts = Counter(row["state"] for row in pairs)
    disposition_counts = Counter(row["disposition"] for row in current)
    status_dispositions = Counter(
        (row["status"], row["disposition"]) for row in current
    )
    residue_counts = Counter(
        row.get("residueClass") for row in current if row["disposition"] == "DEFER"
    )
    if residue_counts:
        raise ClosureError("CLOSURE-RESIDUE-CLASS")
    counts = {
        "candidateInput": 110,
        "historicalEligible": len(migrated),
        "historicalDefer": len(
            [
                row
                for row in eligibility["candidateRows"]
                if row.get("disposition") == "DEFER"
            ]
        ),
        "migratedClosed": len(migrated),
        "currentStage04": len(current),
        "currentPlans": len([row for row in current if row["kind"] == "plan"]),
        "currentTasks": len([row for row in current if row["kind"] == "task"]),
        "currentDefer": disposition_counts["DEFER"],
        "currentRetain": disposition_counts["retain"],
        "activeEligible": status_dispositions[("active", "eligible")],
        "pairKeys": len(pairs),
        "completePairs": pair_counts["complete"],
        "planOnly": pair_counts["plan-only"],
        "taskOnly": pair_counts["task-only"],
        "duplicateSameKind": 0,
        "partialOwnedDefer": len(
            [
                row
                for row in pairs
                if row["state"] != "complete" and row["disposition"] == "DEFER"
            ]
        ),
        "acceptedAdrs": len(accepted_adrs),
        "doneSpecs": len(done_specs),
        "migratedAdrOrSpec": 0,
        "stage05Authored": role_stage,
        "helperTests": role_helpers,
        "findings": 0,
        "taxonomyArchived": len(taxonomy_archives),
    }
    if counts != TRANSITION_EXPECTED_COUNTS:
        raise ClosureError("CLOSURE-COUNTS")
    return {
        "sourceLedgers": source_rows,
        "counts": counts,
        "migratedClosed": migrated,
        "taxonomyTransitionClosed": taxonomy_transition,
        "currentRows": current,
        "pairCardinality": pairs,
        "activeControlRows": active_controls,
        "activeControlPairCardinality": active_control_pairs,
        "terminalControlRows": terminal["terminalControlRows"],
        "terminalControlPairCardinality": terminal["terminalControlPairCardinality"],
        "terminalSpecRows": terminal["terminalSpecRows"],
        "terminalProgramClosureAuthority": terminal_program_closure_authority,
        "authorityGuards": {
            "acceptedAdrs": accepted_adrs,
            "doneSpecs": done_specs,
        },
        "acer004Dependency": dependency,
    }


def _ledger_from_observed(observed: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "$schema": SCHEMA,
        "schemaVersion": 1,
        "observedAt": "2026-07-19",
        "authority": {
            "fixedInputCommit": _git_identity(FIXED_INPUT_COMMIT),
            "ownerSpec": OWNER_SPEC,
            "owner": "platform",
            "evidenceClass": "repository-static-post-cutover-closure",
        },
        "sourceLedgers": copy.deepcopy(observed["sourceLedgers"]),
        "inventoryBoundary": {
            "gitReference": None,
            "trackedAndProposedNonignored": True,
            "trackedObjectMode": "index-stage-zero",
            "proposedObjectMode": "bounded-no-follow-descriptor",
            "ignoredWorkspaceRead": False,
            "liveRuntimeClaim": False,
            "executionTracker": EXECUTION_TASK,
        },
        "counts": copy.deepcopy(observed["counts"]),
        "migratedClosed": copy.deepcopy(observed["migratedClosed"]),
        "currentRows": copy.deepcopy(observed["currentRows"]),
        "pairCardinality": copy.deepcopy(observed["pairCardinality"]),
        "authorityGuards": copy.deepcopy(observed["authorityGuards"]),
        "acer004Dependency": copy.deepcopy(observed["acer004Dependency"]),
        "linkEvidenceBoundary": {
            "evidenceClass": "repository-static-aggregate",
            "currentLinks": "strict-cross-document-validation",
            "historicalLinks": "archive-and-migration-validation",
            "liveRuntimeClaim": False,
        },
        "findings": {key: [] for key in FINDING_KEYS},
    }


def _ordered_unique_paths(rows: Any, code: str, field: str = "path") -> None:
    if not isinstance(rows, list):
        raise ClosureError(code)
    paths = [row.get(field) if isinstance(row, Mapping) else None for row in rows]
    if any(not is_safe_path(path) for path in paths):
        bad = next((path for path in paths if not is_safe_path(path)), LEDGER_PATH)
        raise ClosureError(f"{code}-PATH", bad)
    if len(paths) != len(set(paths)):
        raise ClosureError(f"{code}-DUPLICATE")
    if paths != sorted(paths):
        raise ClosureError(f"{code}-ORDER")


def validate_ledger(ledger: Any, observed: Mapping[str, Any]) -> None:
    top_keys = {
        "$schema",
        "schemaVersion",
        "observedAt",
        "authority",
        "sourceLedgers",
        "inventoryBoundary",
        "counts",
        "migratedClosed",
        "currentRows",
        "pairCardinality",
        "authorityGuards",
        "acer004Dependency",
        "linkEvidenceBoundary",
        "findings",
    }
    if not isinstance(ledger, Mapping) or set(ledger) != top_keys:
        raise ClosureError("CLOSURE-SCHEMA")
    if (
        ledger.get("$schema") != SCHEMA
        or ledger.get("schemaVersion") != 1
        or ledger.get("observedAt") != "2026-07-19"
    ):
        raise ClosureError("CLOSURE-SCHEMA")
    expected = _ledger_from_observed(observed)
    ledger_authority = ledger.get("authority")
    if isinstance(ledger_authority, Mapping):
        ledger_authority = {
            **ledger_authority,
            "ownerSpec": WORK105_CURRENT_PATHS_BY_HISTORICAL.get(
                ledger_authority.get("ownerSpec"), ledger_authority.get("ownerSpec")
            ),
        }
    if ledger_authority != expected["authority"]:
        raise ClosureError("CLOSURE-AUTHORITY")
    if ledger.get("inventoryBoundary") != expected["inventoryBoundary"]:
        raise ClosureError("CLOSURE-BOUNDARY")
    transition = observed.get("taxonomyTransitionClosed", [])
    if not isinstance(transition, list):
        raise ClosureError("CLOSURE-TAXONOMY-MANIFEST", TAXONOMY_MANIFEST_PATH)
    _validate_source_ledger_transition(
        ledger.get("sourceLedgers"), observed.get("sourceLedgers"), transition
    )
    if ledger.get("counts") != EXPECTED_COUNTS:
        raise ClosureError("CLOSURE-COUNTS")

    if transition:
        _ordered_unique_paths(transition, "CLOSURE-TAXONOMY")
        if len(transition) != 100:
            raise ClosureError(
                "CLOSURE-TAXONOMY-MANIFEST-COUNT", TAXONOMY_MANIFEST_PATH
            )

    current = ledger.get("currentRows")
    _ordered_unique_paths(current, "CLOSURE-CURRENT")
    if any(row.get("disposition") == "eligible" for row in current):
        raise ClosureError("CLOSURE-ACTIVE-ELIGIBLE")
    if any(row.get("disposition") != "DEFER" for row in current):
        raise ClosureError("CLOSURE-CURRENT-DISPOSITION")
    for row in current:
        if row.get("sourceDisposition") == "DEFER":
            if (
                not row.get("sourceReason")
                or row.get("sourceOwner") != "platform"
                or not row.get("sourceRefreshTrigger")
                or not row.get("missingAxes")
                or row.get("residueClass")
                not in {"deferred-evidence", "resolved-partial-evidence"}
                or row.get("closureReason") != DEFER_CLOSURE_REASON
                or row.get("postClosureRefreshTrigger") != DEFER_TRIGGER
                or row.get("currentAuthority") != DEFER_AUTHORITY
                or row.get("owner") != "platform"
            ):
                raise ClosureError("CLOSURE-CURRENT-FIELDS", row.get("path"))
        elif row.get("sourceDisposition") == "retain":
            if (
                row.get("status") != "done"
                or row.get("sourceReason") != "active-spec-037-control"
                or row.get("sourceOwner") != "platform"
                or row.get("sourceRefreshTrigger") != "Spec037 closure"
                or row.get("missingAxes") != ["successor-migration-evidence"]
                or row.get("residueClass") != "terminal-owned-defer"
                or row.get("owner") != "platform"
                or row.get("reason") != TERMINAL_CONTROL_REASON
                or row.get("currentEvidenceRole") != TERMINAL_CONTROL_EVIDENCE_ROLE
                or row.get("successorRefreshTrigger")
                != TERMINAL_CONTROL_REFRESH_TRIGGER
                or "currentAuthority" in row
                or "closureTrigger" in row
            ):
                raise ClosureError("CLOSURE-CONTROL-FIELDS", row.get("path"))
        else:
            raise ClosureError("CLOSURE-CURRENT-FIELDS", row.get("path"))
    if transition:
        observed_current = observed.get("currentRows")
        _ordered_unique_paths(observed_current, "CLOSURE-CURRENT")
        ledger_by_path = {row["path"]: row for row in current}
        observed_by_path = {row["path"]: row for row in observed_current}
        transition_by_path = {row["path"]: row for row in transition}
        if set(observed_by_path) & set(transition_by_path) or set(
            ledger_by_path
        ) != set(observed_by_path) | set(transition_by_path):
            raise ClosureError("CLOSURE-CURRENT-DRIFT")
        if any(ledger_by_path[path] != row for path, row in observed_by_path.items()):
            raise ClosureError("CLOSURE-CURRENT-DRIFT")
        for path, closed in transition_by_path.items():
            frozen = ledger_by_path[path]
            if (
                frozen.get("kind") != closed.get("kind")
                or frozen.get("objectMode") != "index-stage-zero"
                or frozen.get("objectId") != closed.get("sourceBlob")
                or frozen.get("sourceDisposition") not in {"DEFER", "retain"}
                or (
                    frozen.get("sourceDisposition") == "retain"
                    and closed.get("disposition") != "manifest-move-closed"
                )
            ):
                raise ClosureError("CLOSURE-TAXONOMY-BLOB", path)
    elif current != expected["currentRows"]:
        raise ClosureError("CLOSURE-CURRENT-DRIFT")

    migrated = ledger.get("migratedClosed")
    _ordered_unique_paths(migrated, "CLOSURE-MIGRATION")
    if len(migrated) != 12:
        raise ClosureError("CLOSURE-MIGRATION-STALE")
    if any(row.get("currentSourcePresent") is not False for row in migrated):
        raise ClosureError("CLOSURE-MIGRATION-SOURCE")
    if any(
        row.get("disposition") != "migrated-closed"
        or row.get("historicalDisposition") != "eligible"
        or row.get("archivePresent") is not True
        or row.get("owner") != "platform"
        or not row.get("rollbackParentCommit")
        for row in migrated
    ):
        raise ClosureError("CLOSURE-MIGRATION-EVIDENCE")
    if migrated != expected["migratedClosed"]:
        raise ClosureError("CLOSURE-MIGRATION-DRIFT")

    pairs = ledger.get("pairCardinality")
    if not isinstance(pairs, list):
        raise ClosureError("CLOSURE-PAIR-SCHEMA")
    keys = [row.get("lineageId") if isinstance(row, Mapping) else None for row in pairs]
    if any(not isinstance(key, str) or not key for key in keys):
        raise ClosureError("CLOSURE-PAIR-KEY")
    if len(keys) != len(set(keys)):
        raise ClosureError("CLOSURE-PAIR-DUPLICATE")
    if keys != sorted(keys):
        raise ClosureError("CLOSURE-PAIR-ORDER")
    if any(
        row.get("state") != "complete"
        and (
            row.get("disposition") != "DEFER"
            or row.get("owner") != "platform"
            or row.get("partialEvidence") != "explicit-owned-DEFER"
        )
        for row in pairs
    ):
        raise ClosureError("CLOSURE-PAIR-PARTIAL")
    if transition:
        if pairs != _build_pairs(current):
            raise ClosureError("CLOSURE-PAIR-DRIFT")
        if observed.get("pairCardinality") != _build_pairs(
            observed.get("currentRows", [])
        ):
            raise ClosureError("CLOSURE-PAIR-DRIFT")
    elif pairs != expected["pairCardinality"]:
        raise ClosureError("CLOSURE-PAIR-DRIFT")

    guards = ledger.get("authorityGuards")
    if not isinstance(guards, Mapping) or set(guards) != {"acceptedAdrs", "doneSpecs"}:
        raise ClosureError("CLOSURE-AUTHORITY-SCHEMA")
    for key, authority, status in (
        ("acceptedAdrs", ADR_AUTHORITY, "accepted"),
        ("doneSpecs", SPEC_AUTHORITY, "done"),
    ):
        rows = guards.get(key)
        _ordered_unique_paths(rows, "CLOSURE-AUTHORITY")
        if any(
            row.get("status") != status
            or row.get("owner") != "platform"
            or row.get("disposition") != "retain"
            or row.get("reason") != AUTHORITY_REASON
            or row.get("currentAuthority") != authority
            or not row.get("refreshTrigger")
            for row in rows
        ):
            raise ClosureError("CLOSURE-AUTHORITY-GUARD")
    _validate_authority_guard_transition(
        guards, observed.get("authorityGuards"), transition
    )
    if ledger.get("acer004Dependency") != expected["acer004Dependency"]:
        raise ClosureError("CLOSURE-ACER004")
    if ledger.get("linkEvidenceBoundary") != expected["linkEvidenceBoundary"]:
        raise ClosureError("CLOSURE-LINK-BOUNDARY")
    findings = ledger.get("findings")
    if not isinstance(findings, Mapping) or tuple(findings) != FINDING_KEYS:
        raise ClosureError("CLOSURE-FINDINGS")
    if any(not isinstance(value, list) or value for value in findings.values()):
        raise ClosureError("CLOSURE-FINDINGS")


def load_ledger(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
    *,
    control_index: Mapping[str, str] | None = None,
) -> Any:
    normalized = _normalize_root(root)
    index = (
        dict(control_index)
        if control_index is not None
        else _control_inventory(normalized, runner)
    )
    return _load_json_bytes(
        _proposed_or_index_bytes(normalized, LEDGER_PATH, index, runner), LEDGER_PATH
    )


def verify_entrypoints(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, str]:
    normalized = _normalize_root(root)
    index = _control_inventory(normalized, runner)
    script = _decode_text(
        _proposed_or_index_bytes(normalized, SCRIPT_PATH, index, runner), SCRIPT_PATH
    )
    aggregate = _decode_text(
        _proposed_or_index_bytes(normalized, AGGREGATE_PATH, index, runner),
        AGGREGATE_PATH,
    )
    if not script.startswith("#!/usr/bin/env python3\n"):
        raise ClosureError("CLOSURE-ENTRYPOINT", SCRIPT_PATH)
    required = (
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR" --self-test',
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR"',
    )
    lines = aggregate.splitlines()
    if any(lines.count(command) != 1 for command in required):
        raise ClosureError("CLOSURE-ENTRYPOINT", AGGREGATE_PATH)
    return index


def validate_active_corpus_residue_closure(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, int]:
    control_index = verify_entrypoints(root, runner)
    observed = build_observed(root, runner)
    _validate_terminal_frontier_shape(observed)
    validate_ledger(load_ledger(root, runner, control_index=control_index), observed)
    counts = observed["counts"]
    return {
        "migratedClosed": counts["migratedClosed"],
        "taxonomyArchived": counts.get("taxonomyArchived", 0),
        "currentRows": counts["currentStage04"],
        "defer": counts["currentDefer"],
        "retain": counts["currentRetain"],
        "pairKeys": counts["pairKeys"],
        "completePairs": counts["completePairs"],
        "planOnly": counts["planOnly"],
        "taskOnly": counts["taskOnly"],
        "acceptedAdrs": counts["acceptedAdrs"],
        "doneSpecs": counts["doneSpecs"],
        "findings": counts["findings"],
        "activeControlRows": len(observed["activeControlRows"]),
        "activeControlPairs": len(observed["activeControlPairCardinality"]),
        "terminalControlRows": len(observed["terminalControlRows"]),
        "terminalControlPairs": len(observed["terminalControlPairCardinality"]),
        "terminalSpecs": len(observed["terminalSpecRows"]),
    }


def _self_test_observed() -> dict[str, Any]:
    current: list[dict[str, Any]] = []
    for index in range(48):
        source_disposition = "retain" if index == 47 else "DEFER"
        for kind, collection in (("plan", "plans"), ("task", "tasks")):
            path = f"docs/04.execution/{collection}/fixture-{index:02d}.md"
            common = {
                "path": path,
                "kind": kind,
                "lineageId": f"fixture-{index:02d}",
                "profile": f"sdlc/{kind}",
                "status": "done",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("0" * 40),
                "sourceDisposition": source_disposition,
                "sourceReason": "active-spec-037-control"
                if source_disposition == "retain"
                else "missing-evidence",
                "sourceOwner": "platform",
                "sourceRefreshTrigger": "Spec037 closure"
                if source_disposition == "retain"
                else "ACER-005-or-exact-upstream-evidence-change",
                "disposition": "DEFER",
                "owner": "platform",
            }
            if source_disposition == "DEFER":
                common.update(
                    {
                        "missingAxes": ["axis"],
                        "residueClass": "deferred-evidence",
                        "closureReason": DEFER_CLOSURE_REASON,
                        "postClosureRefreshTrigger": DEFER_TRIGGER,
                        "currentAuthority": DEFER_AUTHORITY,
                    }
                )
            else:
                common.update(
                    {
                        "missingAxes": ["successor-migration-evidence"],
                        "residueClass": "terminal-owned-defer",
                        "reason": TERMINAL_CONTROL_REASON,
                        "currentEvidenceRole": TERMINAL_CONTROL_EVIDENCE_ROLE,
                        "successorRefreshTrigger": TERMINAL_CONTROL_REFRESH_TRIGGER,
                    }
                )
            current.append(common)
    for index, kind, collection in (
        (48, "plan", "plans"),
        (49, "task", "tasks"),
        (50, "task", "tasks"),
        (51, "task", "tasks"),
    ):
        current.append(
            {
                "path": f"docs/04.execution/{collection}/fixture-{index:02d}.md",
                "kind": kind,
                "lineageId": f"fixture-{index:02d}",
                "profile": f"sdlc/{kind}",
                "status": "done",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("0" * 40),
                "sourceDisposition": "DEFER",
                "sourceReason": "missing-evidence",
                "sourceOwner": "platform",
                "sourceRefreshTrigger": "evidence-change",
                "missingAxes": ["axis"],
                "residueClass": "deferred-evidence",
                "disposition": "DEFER",
                "owner": "platform",
                "closureReason": DEFER_CLOSURE_REASON,
                "postClosureRefreshTrigger": DEFER_TRIGGER,
                "currentAuthority": DEFER_AUTHORITY,
            }
        )
    current.sort(key=lambda row: row["path"])
    pairs = _build_pairs(current)
    migrated = [
        {
            "path": f"docs/04.execution/{'plans' if index % 2 == 0 else 'tasks'}/migrated-{index:02d}.md",
            "kind": "plan" if index % 2 == 0 else "task",
            "lineageId": f"migrated-{index // 2:02d}",
            "sourceCommit": _git_identity("1" * 40),
            "sourceBlob": _git_identity("2" * 40),
            "historicalDisposition": "eligible",
            "historicalReason": "complete-evidence",
            "disposition": "migrated-closed",
            "owner": "platform",
            "closureReason": "exact-atomic-migration-result-joined",
            "batchId": f"ACER-003-{index // 2 + 1:03d}",
            "batchSequence": index // 2 + 1,
            "archivePath": f"docs/98.archive/04.execution/{'plans' if index % 2 == 0 else 'tasks'}/migrated-{index:02d}.md",
            "payloadBytes": 1,
            "payloadSha256": _sha256_identity("3" * 64),
            "archiveReason": "completed-lineage",
            "currentClosureOwner": "docs/03.specs/fixture/spec.md",
            "rollbackParentCommit": _git_identity("4" * 40),
            "validationResult": "PASS",
            "currentSourcePresent": False,
            "archivePresent": True,
        }
        for index in range(12)
    ]
    migrated.sort(key=lambda row: row["path"])

    def guards(count: int, kind: str) -> list[dict[str, Any]]:
        status = "accepted" if kind == "adr" else "done"
        authority = ADR_AUTHORITY if kind == "adr" else SPEC_AUTHORITY
        trigger = (
            "accepted-adr-authority-or-evidence-change"
            if kind == "adr"
            else "done-spec-authority-or-evidence-change"
        )
        return [
            {
                "path": f"docs/{'02.architecture/decisions' if kind == 'adr' else '03.specs'}/fixture-{index:02d}{'.md' if kind == 'adr' else '/spec.md'}",
                "profile": f"sdlc/{kind}",
                "status": status,
                "owner": "platform",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("5" * 40),
                "disposition": "retain",
                "reason": AUTHORITY_REASON,
                "currentAuthority": authority,
                "refreshTrigger": trigger,
            }
            for index in range(count)
        ]

    return {
        "sourceLedgers": [
            {
                "path": path,
                "schema": SOURCE_SCHEMAS[path],
                "objectId": _git_identity("0" * 40),
            }
            for path in SOURCE_PATHS
        ],
        "counts": copy.deepcopy(EXPECTED_COUNTS),
        "migratedClosed": migrated,
        "currentRows": current,
        "pairCardinality": pairs,
        "authorityGuards": {
            "acceptedAdrs": guards(13, "adr"),
            "doneSpecs": guards(29, "spec"),
        },
        "acer004Dependency": {
            "path": SOURCE_PATHS[3],
            "objectId": _git_identity("0" * 40),
            "stage05Authored": 24,
            "helperTests": 33,
            "roleAuditFindings": 0,
            "status": "satisfied",
            "requiredForClosure": True,
        },
    }


def _self_test_terminal_frontier() -> int:
    def payload(profile: str, status: str) -> bytes:
        return (
            f"---\ntype: {profile}\nstatus: {status}\nowner: platform\n---\n# Fixture\n"
        ).encode()

    def registry(successor_state: str, frontier_state: str) -> dict[str, Any]:
        return {
            "programLineage": {
                "programs": [
                    {
                        "prd": "0006",
                        "ad": "0009",
                        "tranches": [
                            {**TERMINAL_RELATION_IDENTITY, "state": "done"},
                            {
                                **TERMINAL_SUCCESSOR_IDENTITY,
                                "state": successor_state,
                            },
                            {
                                **TERMINAL_FRONTIER_IDENTITY,
                                "state": frontier_state,
                            },
                        ],
                        "followUps": [],
                    }
                ]
            }
        }

    retained_spec = "docs/03.specs/fixture-retained/spec.md"
    payloads = {
        TERMINAL_SPEC: payload("sdlc/spec", "done"),
        TERMINAL_PLAN: payload("sdlc/plan", "done"),
        TERMINAL_TASK: payload("sdlc/task", "done"),
        TERMINAL_SUCCESSOR_SPEC: payload("sdlc/spec", "active"),
        TERMINAL_SUCCESSOR_PLAN: payload("sdlc/plan", "active"),
        TERMINAL_SUCCESSOR_TASK: payload("sdlc/task", "active"),
        TERMINAL_FRONTIER_SPEC: payload("sdlc/spec", "active"),
        retained_spec: payload("sdlc/spec", "done"),
    }
    spec_paths = [
        TERMINAL_SPEC,
        TERMINAL_SUCCESSOR_SPEC,
        TERMINAL_FRONTIER_SPEC,
        retained_spec,
    ]
    cases = 0

    active = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK],
        spec_paths,
        {},
        payloads,
        registry("active", "active"),
    )
    if (
        active["specPaths"]
        != [TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC, retained_spec]
        or active["planPaths"] != [TERMINAL_SUCCESSOR_PLAN]
        or active["taskPaths"] != [TERMINAL_SUCCESSOR_TASK]
        or len(active["terminalControlRows"]) != 2
        or [row["path"] for row in active["terminalSpecRows"]] != [TERMINAL_SPEC]
    ):
        raise AssertionError("active terminal frontier partition drift")
    cases += 1

    advanced_payloads = dict(payloads)
    advanced_payloads[TERMINAL_SUCCESSOR_SPEC] = payload("sdlc/spec", "done")
    advanced_payloads[TERMINAL_SUCCESSOR_PLAN] = payload("sdlc/plan", "done")
    advanced_payloads[TERMINAL_SUCCESSOR_TASK] = payload("sdlc/task", "done")
    advanced_payloads[TERMINAL_FRONTIER_PLAN] = payload("sdlc/plan", "active")
    advanced_payloads[TERMINAL_FRONTIER_TASK] = payload("sdlc/task", "active")
    advanced = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN, TERMINAL_FRONTIER_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK, TERMINAL_FRONTIER_TASK],
        spec_paths,
        {},
        advanced_payloads,
        registry("done", "active"),
    )
    if (
        advanced["specPaths"] != [TERMINAL_FRONTIER_SPEC, retained_spec]
        or advanced["planPaths"] != [TERMINAL_FRONTIER_PLAN]
        or advanced["taskPaths"] != [TERMINAL_FRONTIER_TASK]
        or len(advanced["terminalControlRows"]) != 4
        or len(advanced["terminalControlPairCardinality"]) != 2
        or [row["path"] for row in advanced["terminalSpecRows"]]
        != [TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC]
    ):
        raise AssertionError("advanced terminal frontier partition drift")
    cases += 1

    final_payloads = dict(advanced_payloads)
    final_payloads[TERMINAL_FRONTIER_SPEC] = payload("sdlc/spec", "done")
    final_payloads[TERMINAL_FRONTIER_PLAN] = payload("sdlc/plan", "done")
    final_payloads[TERMINAL_FRONTIER_TASK] = payload("sdlc/task", "done")
    final = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN, TERMINAL_FRONTIER_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK, TERMINAL_FRONTIER_TASK],
        spec_paths,
        {},
        final_payloads,
        registry("done", "done"),
    )
    if (
        final["specPaths"] != [retained_spec]
        or final["planPaths"]
        or final["taskPaths"]
        or len(final["terminalControlRows"]) != 6
        or len(final["terminalControlPairCardinality"]) != 3
        or [row["path"] for row in final["terminalSpecRows"]]
        != [TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC]
    ):
        raise AssertionError("final terminal frontier partition drift")
    cases += 1

    blocked_payloads = dict(advanced_payloads)
    blocked_payloads[TERMINAL_FRONTIER_SPEC] = payload("sdlc/spec", "done")
    try:
        _partition_terminal_controls(
            [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN],
            [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK],
            spec_paths,
            {},
            blocked_payloads,
            registry("done", "done"),
        )
    except ClosureError as exc:
        if (
            exc.code != "CLOSURE-TERMINAL-FRONTIER"
            or exc.path != TERMINAL_FRONTIER_PLAN
        ):
            raise
        cases += 1
    else:
        raise AssertionError("closed terminal frontier was accepted")

    return cases


def _self_test_post_closure_adr_scope() -> int:
    expected_later = frozenset(
        {
            "docs/02.architecture/decisions/"
            "0019-provider-native-agent-harness-and-loop-model.md",
            "docs/02.architecture/decisions/"
            "0021-canonical-surface-routing-and-evidence-depth.md",
            "docs/02.architecture/decisions/"
            "0022-direct-approval-standalone-execution-lineage.md",
            "docs/02.architecture/decisions/"
            "0023-work-unit-document-taxonomy-and-governance-authority.md",
            "docs/02.architecture/decisions/"
            "0024-terminal-artifact-identity-and-archive-layout.md",
            "docs/02.architecture/decisions/0025-four-digit-document-path-identity.md",
            "docs/02.architecture/decisions/"
            "0026-argo-cd-source-integrity-non-adoption.md",
            "docs/02.architecture/decisions/"
            "0027-pod-security-standards-staged-adoption.md",
            "docs/02.architecture/decisions/"
            "0028-pod-security-admission-per-namespace-adoption.md",
            "docs/02.architecture/decisions/0029-mutable-target-revision-retention.md",
        }
    )
    if POST_CLOSURE_ADR_AUTHORITY_PATHS != expected_later:
        raise AssertionError("post-closure ADR authority set drift")

    def accepted_payload() -> bytes:
        return b"---\ntype: sdlc/adr\nstatus: accepted\nowner: platform\n---\n# ADR\n"

    known_paths = [*FROZEN_ACCEPTED_ADR_PATHS, *sorted(expected_later)]
    payloads = {path: accepted_payload() for path in known_paths}
    index = {
        path: POST_CLOSURE_PINNED_AUTHORITY_BLOBS.get(path, "0" * 40)
        for path in known_paths
    }
    rows = _frozen_authority_entries(
        known_paths,
        index,
        payloads,
        kind="adr",
    )
    if tuple(row["path"] for row in rows) != FROZEN_ACCEPTED_ADR_PATHS:
        raise AssertionError("frozen accepted ADR guard drift")
    cases = 1

    unknown = "docs/02.architecture/decisions/9999-unknown-post-closure-authority.md"
    unknown_paths = [*known_paths, unknown]
    unknown_payloads = {**payloads, unknown: accepted_payload()}
    unknown_index = {**index, unknown: "0" * 40}
    try:
        _frozen_authority_entries(
            unknown_paths,
            unknown_index,
            unknown_payloads,
            kind="adr",
        )
    except ClosureError as exc:
        if exc.code != "CLOSURE-AUTHORITY-SCOPE" or exc.path != unknown:
            raise
        cases += 1
    else:
        raise AssertionError("unknown post-closure ADR authority was accepted")
    return cases


def run_self_test() -> int:
    observed = _self_test_observed()
    ledger = _ledger_from_observed(observed)
    validate_ledger(ledger, observed)
    cases = 1 + _self_test_terminal_frontier() + _self_test_post_closure_adr_scope()
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("CLOSURE-SCHEMA", lambda item: item.__setitem__("schemaVersion", 2)),
        ("CLOSURE-SOURCE-DRIFT", lambda item: item["sourceLedgers"].pop()),
        (
            "CLOSURE-COUNTS",
            lambda item: item["counts"].__setitem__("currentStage04", 99),
        ),
        (
            "CLOSURE-CURRENT-DUPLICATE",
            lambda item: item["currentRows"].append(
                copy.deepcopy(item["currentRows"][0])
            ),
        ),
        (
            "CLOSURE-ACTIVE-ELIGIBLE",
            lambda item: item["currentRows"][0].__setitem__("disposition", "eligible"),
        ),
        (
            "CLOSURE-CURRENT-FIELDS",
            lambda item: item["currentRows"][0].__setitem__("closureReason", ""),
        ),
        (
            "CLOSURE-CONTROL-FIELDS",
            lambda item: next(
                row
                for row in item["currentRows"]
                if row["sourceDisposition"] == "retain"
            ).__setitem__("currentEvidenceRole", ""),
        ),
        (
            "CLOSURE-CONTROL-FIELDS",
            lambda item: next(
                row
                for row in item["currentRows"]
                if row["sourceDisposition"] == "retain"
            ).__setitem__("status", "active"),
        ),
        ("CLOSURE-MIGRATION-STALE", lambda item: item["migratedClosed"].pop()),
        (
            "CLOSURE-MIGRATION-SOURCE",
            lambda item: item["migratedClosed"][0].__setitem__(
                "currentSourcePresent", True
            ),
        ),
        (
            "CLOSURE-PAIR-PARTIAL",
            lambda item: next(
                row for row in item["pairCardinality"] if row["state"] != "complete"
            ).__setitem__("disposition", "retain"),
        ),
        (
            "CLOSURE-AUTHORITY-GUARD",
            lambda item: item["authorityGuards"]["acceptedAdrs"][0].__setitem__(
                "disposition", "migrated-closed"
            ),
        ),
        (
            "CLOSURE-ACER004",
            lambda item: item["acer004Dependency"].__setitem__("helperTests", 32),
        ),
        (
            "CLOSURE-FINDINGS",
            lambda item: item["findings"]["unexplainedResidue"].append(
                {"path": "docs/x.md"}
            ),
        ),
    ]
    for expected_code, mutation in mutations:
        candidate = copy.deepcopy(ledger)
        mutation(candidate)
        try:
            validate_ledger(candidate, observed)
        except ClosureError as exc:
            if exc.code != expected_code:
                raise AssertionError(
                    f"unexpected mutation diagnostic: {exc.code}"
                ) from exc
            cases += 1
        else:
            raise AssertionError("closed residue mutation was accepted")
    try:
        _reject_duplicate_pairs([("a", 1), ("a", 2)])
    except ClosureError as exc:
        if exc.code != "CLOSURE-JSON-DUPLICATE":
            raise
        cases += 1
    else:
        raise AssertionError("duplicate JSON key was accepted")
    for path in ("../outside", "/absolute", "_workspace/private"):
        if is_safe_path(path):
            raise AssertionError("unsafe path was accepted")
        cases += 1
    return cases


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            cases = run_self_test()
            print(f"PASS active-corpus-residue-closure self-test cases={cases}")
        else:
            counts = validate_active_corpus_residue_closure(arguments.root)
            print(
                "PASS active-corpus-residue-closure "
                f"migrated={counts['migratedClosed']} "
                f"taxonomy_archived={counts['taxonomyArchived']} "
                f"current={counts['currentRows']} "
                f"dispositions={counts['defer']}/{counts['retain']} "
                f"pairs={counts['pairKeys']}:{counts['completePairs']}/{counts['planOnly']}/{counts['taskOnly']} "
                f"active_controls={counts['activeControlRows']}/{counts['activeControlPairs']} "
                f"terminal_controls={counts['terminalControlRows']}/{counts['terminalControlPairs']} "
                f"terminal_specs={counts['terminalSpecs']} "
                f"guards={counts['acceptedAdrs']}/{counts['doneSpecs']} "
                f"findings={counts['findings']}"
            )
        return 0
    except (ClosureError, AssertionError) as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
