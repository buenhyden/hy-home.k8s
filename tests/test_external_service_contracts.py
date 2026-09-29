"""Static joins preserve external-service backend contracts without live access."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
from unittest import mock
from contextlib import redirect_stdout
from io import StringIO
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHECKER = (
    ROOT
    / ".agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py"
)
PREFIX = Path("gitops/platform/external-services")


class ExternalServiceContractsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "external_contract_checker", CHECKER
        )
        cls.checker = importlib.util.module_from_spec(spec)
        with mock.patch.object(sys, "dont_write_bytecode", True):
            spec.loader.exec_module(cls.checker)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / PREFIX).mkdir(parents=True)
        self.documents = list(
            yaml.safe_load_all((ROOT / PREFIX / "valkey-external.yaml").read_text())
        )

    def check(self, documents=None):
        path = self.root / PREFIX / "contract.yaml"
        path.write_text(
            yaml.safe_dump_all(self.documents if documents is None else documents)
        )
        return self.checker.validate_documents(self.root, [path])

    def test_backend_port_may_differ_from_frontend(self):
        self.assertEqual(self.check(), [])

    def test_identical_endpoints_and_split_ports_across_slices(self):
        service, first = list(
            yaml.safe_load_all((ROOT / PREFIX / "alloy-external.yaml").read_text())
        )
        second = copy.deepcopy(first)
        second["metadata"]["name"] = "alloy-external-2"
        first["ports"] = first["ports"][:1]
        second["ports"] = second["ports"][1:]
        self.assertEqual(self.check([service, first, second]), [])

    def test_missing_or_mismatched_backend_rejects(self):
        for field, value in (("port", 6379), ("protocol", "UDP"), ("name", "wrong")):
            with self.subTest(field=field):
                docs = copy.deepcopy(self.documents)
                docs[1]["ports"][0][field] = value
                self.assertTrue(self.check(docs))
        self.assertTrue(self.check(self.documents[:1]))

    def test_namespace_and_address_family_must_match(self):
        docs = copy.deepcopy(self.documents)
        docs[1]["metadata"]["namespace"] = "wrong"
        self.assertTrue(self.check(docs))
        docs = copy.deepcopy(self.documents)
        docs[1]["addressType"] = "IPv6"
        self.assertTrue(self.check(docs))

    def test_malformed_documents_are_bounded_redacted_findings(self):
        for document in (
            "private-payload",
            {"kind": "Service", "metadata": []},
            {
                "kind": "EndpointSlice",
                "metadata": {"name": "x"},
                "ports": "private-payload",
            },
        ):
            with self.subTest(document=document):
                errors = self.check([document])
                self.assertTrue(errors)
                self.assertNotIn("private-payload", str(errors))

    def test_unroutable_endpoint_addresses_reject(self):
        for address in ("127.0.0.1", "0.0.0.0", "224.0.0.1", "169.254.0.1"):
            with self.subTest(address=address):
                docs = copy.deepcopy(self.documents)
                docs[1]["endpoints"][0]["addresses"] = [address]
                self.assertTrue(self.check(docs))

    def test_malformed_selector_cannot_be_classified_as_selectorless(self):
        for selector in ([], "", 0):
            with self.subTest(selector=selector):
                docs = copy.deepcopy(self.documents)
                docs[0]["spec"]["selector"] = selector
                self.assertTrue(self.check(docs))

    def test_selector_services_do_not_need_manual_slices(self):
        service = copy.deepcopy(self.documents[0])
        service["spec"]["selector"] = {"app": "managed"}
        self.assertEqual(self.check([service]), [])

    def test_paths_cannot_escape_or_follow_links(self):
        outside = self.root / "outside.yaml"
        outside.write_text("private-payload")
        self.assertTrue(self.checker.validate_documents(self.root, [outside]))
        link = self.root / PREFIX / "link.yaml"
        link.symlink_to(outside)
        errors = self.checker.validate_documents(self.root, [link])
        self.assertTrue(errors)
        self.assertNotIn("private-payload", str(errors))

    def test_cli_includes_new_nonignored_manifest_and_redacts_failure(self):
        subprocess.run(
            ["git", "init", "-q", str(self.root)], check=True, capture_output=True
        )
        self.assertEqual(self.check(), [])
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(self.checker.main(["--root", str(self.root)]), 0)
        (self.root / PREFIX / "new.yaml").write_text("private-payload")
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(self.checker.main(["--root", str(self.root)]), 1)
        self.assertNotIn("private-payload", output.getvalue())

    def test_actual_repository_contracts(self):
        self.assertEqual(
            self.checker.validate_documents(
                ROOT, sorted((ROOT / PREFIX).glob("*.yaml"))
            ),
            [],
        )
