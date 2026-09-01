"""Independent fixture tests for Vault/ESO repository contracts."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

from tests.vault_eso_contract_cases import (
    apply_fixture_mutation,
    contract_diagnostics,
    run_internal_boundaries,
    valid_contracts,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/validate-vault-eso-contracts.py"
FIXTURE_PATH = ROOT / "tests/fixtures/vault-eso-contracts.json"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_vault_eso_contracts", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class VaultEsoContractFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_fixture_mutations_have_exact_diagnostics(self) -> None:
        baseline = valid_contracts(self.validator)
        for case in self.fixture["cases"]:
            with self.subTest(case=case["name"]):
                contracts = copy.deepcopy(baseline)
                apply_fixture_mutation(contracts, case["mutation"])
                self.assertEqual(
                    contract_diagnostics(self.validator, contracts),
                    case["expected"],
                )

    def test_internal_security_boundaries(self) -> None:
        run_internal_boundaries(self.validator)


if __name__ == "__main__":
    unittest.main()
