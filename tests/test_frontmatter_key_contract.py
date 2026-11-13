"""SPEC-0181: the frontmatter key registry, its checks, its projection and its dialect."""

from __future__ import annotations

import copy
import datetime as dt
import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

import ruamel.yaml as ruamel_yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_contracts as CONTRACTS  # noqa: E402
from frontmatter_yaml import FrontmatterError, load_frontmatter  # noqa: E402


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MARKDOWN = _load_script("key_contract_markdown", "validate-markdown-profiles.py")
AGENT_GOVERNANCE = _load_script(
    "key_contract_agent_governance", "validate-agent-governance.py"
)
TODAY = dt.date(2026, 11, 13)
REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
SCHEMA_FILE = ROOT / "docs/99.templates/contracts/frontmatter.schema.json"
BINDINGS_FILE = ROOT / ".claude/bindings.json"

KEYS = (
    "title",
    "version",
    "type",
    "status",
    "owner",
    "updated",
    "artifact_id",
    "supersedes",
    "superseded_by",
    "layer",
    "cancellation",
    "description",
    "parent_ids",
    "name",
    "resolved_at",
    "metadata",
    "disable-model-invocation",
    "model",
    "effort",
    "tools",
    "argument-hint",
    "allowed-tools",
)

GOV_PATH = ".agents/governance/document-lifecycle.md"
GOV = {
    "title": '"Example"',
    "version": '"1.0.0"',
    "type": '"governance/rule"',
    "status": '"active"',
    "owner": '"platform"',
    "updated": '"2026-11-13"',
}
SPEC_PATH = "docs/03.specs/0999-example/spec.md"
SPEC = {
    "title": '"Example"',
    "version": '"1.0.0"',
    "type": '"sdlc/spec"',
    "status": '"draft"',
    "owner": '"platform"',
    "updated": '"2026-11-13"',
    "artifact_id": '"SPEC-0999"',
}
ADR_PATH = "docs/02.architecture/decisions/0999-example.md"
ADR = {
    "title": '"Example"',
    "version": '"1.0.0"',
    "type": '"sdlc/architecture-decision"',
    "status": '"accepted"',
    "owner": '"platform"',
    "updated": '"2026-11-13"',
    "artifact_id": '"ADR-0999"',
}
PLAN_PATH = "docs/03.specs/0999-example/plan.md"
PLAN = {
    **SPEC,
    "type": '"sdlc/plan"',
    "artifact_id": '"SPEC-0999-PLAN-0001"',
    "parent_ids": '["SPEC-0999"]',
}
TASK_PATH = "docs/03.specs/0999-example/tasks/tsk-0001-example.md"
TASK = {
    **SPEC,
    "type": '"sdlc/task"',
    "status": '"cancelled"',
    "artifact_id": '"SPEC-0999-TSK-0001"',
    "parent_ids": '["SPEC-0999-PLAN-0001"]',
}
AGENT_PATH = ".claude/agents/example.md"
AGENT = {
    "name": '"example"',
    "description": '"One bounded responsibility."',
    "model": '"sonnet"',
    "effort": '"high"',
    "tools": '"Read, Grep"',
}
COMMAND_PATH = ".claude/commands/example.md"
COMMAND = {"description": '"Run one check."'}


def layered(fields: dict[str, str]) -> dict[str, str]:
    """Insert layer after updated, where the profile order puts it."""
    out: dict[str, str] = {}
    for key, value in fields.items():
        out[key] = value
        if key == "updated":
            out["layer"] = '"architecture"'
    return out


def doc(fields: dict[str, str]) -> str:
    return (
        "---\n" + "".join(f"{k}: {v}\n" for k, v in fields.items()) + "---\n\nBody.\n"
    )


class KeyProfileCheckTests(unittest.TestCase):
    """One accepted and one refused case per key through the profile check."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.schema = MARKDOWN.load_frontmatter_schema(ROOT)

    def rules(self, path: str, fields: dict[str, str]) -> set[str]:
        posix = PurePosixPath(path)
        profile = CONTRACTS.classify_path(self.registry, posix)
        return {
            item.rule_id
            for item in MARKDOWN.validate_document_text(
                doc(fields),
                posix,
                profile,
                "strict",
                today=TODAY,
                include_body=False,
                frontmatter_schema=self.schema,
            )
        }

    def accepted(self, path: str, fields: dict[str, str]) -> None:
        self.assertEqual(self.rules(path, fields), set())

    def refused(self, path: str, fields: dict[str, str], rule: str) -> None:
        self.assertIn(rule, self.rules(path, fields))

    def test_title_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "title": '"A different title"'})

    def test_title_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "title": "1"}, "FM-TITLE")

    def test_version_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "version": '"2.3.4"'})

    def test_version_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "version": '"1.0"'}, "FM-SCHEMA")

    def test_type_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "type": '"governance/rule"'})

    def test_type_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "type": '"governance/role"'}, "FM-TYPE")

    def test_status_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "status": '"deprecated"'})

    def test_status_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "status": '"bogus"'}, "FM-STATUS")

    def test_owner_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "owner": '"platform"'})

    def test_owner_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "owner": '""'}, "FM-SCHEMA")

    def test_updated_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "updated": '"2026-11-13"'})

    def test_artifact_id_accepted(self) -> None:
        self.accepted(SPEC_PATH, {**SPEC, "artifact_id": '"SPEC-0999"'})

    def test_artifact_id_refused(self) -> None:
        self.refused(
            SPEC_PATH, {**SPEC, "artifact_id": '"SPEC-0998"'}, "ARTIFACT-IDENTITY"
        )

    def test_supersedes_accepted(self) -> None:
        self.accepted(GOV_PATH, {**GOV, "supersedes": '["POL-0001", "POL-0002"]'})

    def test_supersedes_refused(self) -> None:
        self.refused(GOV_PATH, {**GOV, "supersedes": '"nope"'}, "FM-SCHEMA")

    def test_superseded_by_accepted(self) -> None:
        self.accepted(
            GOV_PATH, {**GOV, "status": '"superseded"', "superseded_by": '"POL-0002"'}
        )

    def test_superseded_by_refused(self) -> None:
        self.refused(
            GOV_PATH,
            {**GOV, "status": '"superseded"', "superseded_by": '"nope"'},
            "FM-SCHEMA",
        )

    def test_layer_accepted(self) -> None:
        self.accepted(ADR_PATH, ADR)
        self.accepted(ADR_PATH, layered(ADR))

    def test_layer_refused(self) -> None:
        for status in ("proposed", "rejected", "superseded", "deprecated"):
            with self.subTest(status=status):
                self.refused(
                    ADR_PATH,
                    layered({**ADR, "status": f'"{status}"'}),
                    "FM-LAYER-ADR",
                )
        self.refused(ADR_PATH, {**ADR, "layer": '"specs"'}, "FM-VALUE-CONSTANT")
        for path, fields in ((SPEC_PATH, SPEC), (GOV_PATH, GOV)):
            with self.subTest(path=path):
                self.refused(path, {**fields, "layer": '"specs"'}, "FM-KEYSET")

    def test_cancellation_accepted(self) -> None:
        self.accepted(
            TASK_PATH,
            {
                **TASK,
                "cancellation": (
                    '\n  reason: "withdrawn"'
                    '\n  authorization_ref: "SPEC-0999-PLAN-0001"'
                    '\n  criteria_disposition: "none open"'
                ),
            },
        )

    def test_description_accepted(self) -> None:
        self.accepted(AGENT_PATH, {**AGENT, "description": '"Another responsibility."'})

    def test_description_refused(self) -> None:
        fields = {k: v for k, v in AGENT.items() if k != "description"}
        self.refused(AGENT_PATH, fields, "FM-KEYSET")

    def test_parent_ids_accepted(self) -> None:
        self.accepted(PLAN_PATH, {**PLAN, "parent_ids": '["SPEC-0999"]'})

    def test_parent_ids_refused(self) -> None:
        self.refused(
            PLAN_PATH, {**PLAN, "parent_ids": '["SPEC-0998"]'}, "PARENT-IDENTITY"
        )

    def test_name_accepted(self) -> None:
        self.accepted(AGENT_PATH, {**AGENT, "name": '"another"'})

    def test_name_refused(self) -> None:
        fields = {k: v for k, v in AGENT.items() if k != "name"}
        self.refused(AGENT_PATH, fields, "FM-KEYSET")

    def test_model_accepted(self) -> None:
        self.accepted(AGENT_PATH, {**AGENT, "model": '"opus"'})

    def test_effort_accepted(self) -> None:
        self.accepted(AGENT_PATH, {**AGENT, "effort": '"xhigh"'})

    def test_effort_refused(self) -> None:
        fields = {
            "name": AGENT["name"],
            "description": AGENT["description"],
            "effort": AGENT["effort"],
            "model": AGENT["model"],
            "tools": AGENT["tools"],
        }
        self.refused(AGENT_PATH, fields, "FM-KEY-ORDER")

    def test_argument_hint_accepted(self) -> None:
        self.accepted(COMMAND_PATH, {**COMMAND, "argument-hint": '"[file]"'})

    def test_argument_hint_refused(self) -> None:
        self.refused(AGENT_PATH, {**AGENT, "argument-hint": '"[file]"'}, "FM-KEYSET")

    def test_allowed_tools_accepted(self) -> None:
        self.accepted(COMMAND_PATH, {**COMMAND, "allowed-tools": '"Bash(ls:*)"'})

    def test_allowed_tools_refused(self) -> None:
        fields = {
            "description": COMMAND["description"],
            "allowed-tools": '"Bash(ls:*)"',
            "argument-hint": '"[file]"',
        }
        self.refused(COMMAND_PATH, fields, "FM-KEY-ORDER")


class RegistryKeyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_FILE.read_text("utf-8"))
        cls.bindings = json.loads(BINDINGS_FILE.read_text("utf-8"))

    def raw(self) -> dict:
        return json.loads(REGISTRY_FILE.read_text("utf-8"))

    def rules(self, raw: dict) -> set[str]:
        return {
            item.rule_id for item in CONTRACTS.current_registry_diagnostics(ROOT, raw)
        }

    def entry(self, raw: dict, key: str) -> dict:
        return next(item for item in raw["frontmatter_keys"] if item["key"] == key)

    def test_repository_registry_describes_exactly_the_used_keys(self) -> None:
        raw = self.raw()
        self.assertEqual(self.rules(raw), set())
        self.assertEqual([item["key"] for item in raw["frontmatter_keys"]], list(KEYS))
        used = {
            key
            for profile in raw["profiles"]
            for field in ("required", "optional", "forbidden", "order")
            for key in profile["frontmatter"][field]
        }
        self.assertEqual(used, set(KEYS))

    def test_every_entry_carries_every_field_and_both_tests(self) -> None:
        for item in self.raw()["frontmatter_keys"]:
            with self.subTest(key=item["key"]):
                self.assertEqual(set(item), set(CONTRACTS.FRONTMATTER_KEY_FIELDS))
                self.assertIn(item["authoring_owner"], {"author", "tool", "derived"})
                self.assertTrue(item["consumer_paths"])
                for field in ("positive_test", "negative_test"):
                    self.assertEqual(set(item[field]), {"module", "test"})

    def test_title_and_layer_name_their_duplicate_sources(self) -> None:
        raw = self.raw()
        self.assertIn("H1", self.entry(raw, "title")["duplicate_source"])
        self.assertIn("W03-D23", self.entry(raw, "title")["duplicate_source"])
        layer = self.entry(raw, "layer")
        self.assertIn("stage folder", layer["duplicate_source"])
        self.assertIn("accepted ADR", layer["condition"])
        self.assertIn("W03-D22", layer["migration"])
        self.assertIn("SPEC-0184", layer["migration"])
        self.assertIn(
            "scripts/validate-document-contract-registry.py", layer["consumer_paths"]
        )

    def test_a_missing_entry_is_refused(self) -> None:
        raw = self.raw()
        raw["frontmatter_keys"].remove(self.entry(raw, "owner"))
        self.assertIn("REGISTRY_FRONTMATTER_KEY", self.rules(raw))

    def test_a_stray_entry_is_refused(self) -> None:
        raw = self.raw()
        raw["frontmatter_keys"].append({**self.entry(raw, "owner"), "key": "stray"})
        self.assertIn("REGISTRY_FRONTMATTER_KEY", self.rules(raw))

    def test_a_duplicate_entry_is_refused(self) -> None:
        raw = self.raw()
        raw["frontmatter_keys"].append(copy.deepcopy(self.entry(raw, "owner")))
        self.assertIn("REGISTRY_FRONTMATTER_KEY", self.rules(raw))

    def test_missing_sections_are_refused(self) -> None:
        for section, rule in (
            ("frontmatter_keys", "REGISTRY_FRONTMATTER_KEY"),
            ("frontmatter_dialect", "REGISTRY_FRONTMATTER_DIALECT"),
        ):
            with self.subTest(section=section):
                raw = self.raw()
                del raw[section]
                self.assertIn(rule, self.rules(raw))

    def test_an_empty_or_missing_consumer_path_is_refused(self) -> None:
        for consumers in ([], ["scripts/no-such-consumer.py"], ["scripts"]):
            with self.subTest(consumers=consumers):
                raw = self.raw()
                self.entry(raw, "owner")["consumer_paths"] = consumers
                self.assertIn("REGISTRY_KEY_CONSUMER", self.rules(raw))

    def test_a_test_reference_must_resolve(self) -> None:
        mutations = {
            "module": {"module": "tests/test_no_such_module.py"},
            "name": {"test": "test_no_such_test"},
            "key literal": {
                "module": "tests/test_frontmatter_key_contract.py",
                "test": "test_a_missing_entry_is_refused",
            },
        }
        for label, change in mutations.items():
            for field in ("positive_test", "negative_test"):
                with self.subTest(label=label, field=field):
                    raw = self.raw()
                    entry = self.entry(raw, "effort")
                    entry[field] = {**entry[field], **change}
                    self.assertIn("REGISTRY_KEY_TEST", self.rules(raw))

    def test_an_unverified_extension_field_is_refused(self) -> None:
        for field in ("condition", "owner", "verification", "review", "removal"):
            with self.subTest(field=field):
                raw = self.raw()
                raw["shared_contract"]["extensions"][0][field] = "unverified"
                self.assertIn("REGISTRY_SHARED_EXTENSION", self.rules(raw))

    def test_a_base_registry_without_the_sections_still_loads(self) -> None:
        raw = self.raw()
        del raw["frontmatter_keys"], raw["frontmatter_dialect"]
        for extension in raw["shared_contract"]["extensions"]:
            extension.update(
                condition=extension["name"],
                owner="unverified",
                verification="unverified",
                review="unverified",
                removal="unverified",
            )
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        self.assertEqual(loaded.frontmatter_keys, ())
        self.assertIsNone(loaded.frontmatter_dialect)
        self.assertEqual(
            len(CONTRACTS.validate_registry(ROOT, self.raw()).frontmatter_keys),
            len(KEYS),
        )

    def test_the_key_table_covers_every_profile_and_key(self) -> None:
        raw = self.raw()
        rows = CONTRACTS.frontmatter_key_table(raw, self.schema, self.bindings)
        self.assertEqual(
            {tuple(row) for row in rows}, {tuple(CONTRACTS.KEY_TABLE_COLUMNS)}
        )
        self.assertEqual(len(CONTRACTS.KEY_TABLE_COLUMNS), 14)
        by_profile: dict[str, dict[str, dict]] = {}
        for row in rows:
            by_profile.setdefault(row["document_type"], {})[row["key"]] = row
            self.assertTrue(row["allowed_values"], row)
            self.assertTrue(row["consumer_paths"], row)
        listed = 0
        for profile in raw["profiles"]:
            lists = profile["frontmatter"]
            keys = [*lists["required"], *lists["optional"], *lists["forbidden"]]
            with self.subTest(profile=profile["id"]):
                self.assertEqual(set(by_profile.get(profile["id"], {})), set(keys))
                for key in lists["required"]:
                    self.assertEqual(
                        by_profile[profile["id"]][key]["requiredness"], "required"
                    )
                for key in lists["forbidden"]:
                    self.assertEqual(
                        by_profile[profile["id"]][key]["requiredness"], "forbidden"
                    )
            listed += len(keys)
        self.assertEqual(len(rows), listed)
        self.assertEqual({row["key"] for row in rows}, set(KEYS))

    def test_the_key_table_takes_values_from_their_owners(self) -> None:
        rows = CONTRACTS.frontmatter_key_table(self.raw(), self.schema, self.bindings)
        table = {(row["document_type"], row["key"]): row for row in rows}
        self.assertIn("sdlc/spec", table[("sdlc/spec", "type")]["allowed_values"])
        adr = table[("sdlc/architecture-decision", "layer")]
        self.assertIn("architecture", adr["allowed_values"])
        self.assertNotIn(("sdlc/spec", "layer"), table)
        self.assertIn("[0-9]+", table[("sdlc/spec", "version")]["allowed_values"])
        self.assertIn("draft", table[("sdlc/spec", "status")]["allowed_values"])
        self.assertTrue(
            table[("sdlc/task", "cancellation")]["requiredness"].startswith(
                "conditional"
            )
        )
        agent = "common/provider-native-metadata"
        for key, values in (
            ("model", ("opus", "sonnet", "fable")),
            ("effort", ("xhigh", "high", "medium")),
            ("tools", ("Read", "Bash", "Task")),
        ):
            for value in values:
                self.assertIn(value, table[(agent, key)]["allowed_values"])
        self.assertIn(
            "provider-owned",
            table[("common/provider-native-command", "argument-hint")][
                "allowed_values"
            ],
        )

    def test_the_codex_twin_is_bound_with_its_binding(self) -> None:
        profiles = {item["id"]: item for item in self.raw()["profiles"]}
        twin = profiles["common/template-exception-provider-native-codex"]
        source = profiles["common/codex-agent-binding"]
        self.assertEqual(twin["mode"], "template")
        self.assertEqual(twin["frontmatter"]["mode"], "absent")
        self.assertEqual(twin["placeholder_policy"], "template-only")
        self.assertEqual(twin["relationships"]["source_profile_ids"], [source["id"]])
        self.assertEqual(twin["template_source"], source["template_source"])
        self.assertEqual(twin["document_role"], "provider-native")
        self.assertEqual(source["document_role"], "provider-native")
        self.assertEqual(twin["template_definition"]["tables"], [])


class FrontmatterDialectTests(unittest.TestCase):
    """The recorded loader behavior is the behavior of the one loader."""

    @staticmethod
    def recorded() -> dict:
        return json.loads(REGISTRY_FILE.read_text("utf-8"))["frontmatter_dialect"]

    def test_the_dialect_records_the_current_target_and_schema_dialects(self) -> None:
        dialect = self.recorded()
        self.assertEqual(
            dialect["current"]["yaml"],
            "YAML 1.2 (ruamel.yaml 0.19.1, with stated refusals)",
        )
        self.assertEqual(dialect["current"]["library"], "ruamel.yaml 0.19.1")
        self.assertEqual(ruamel_yaml.__version__, "0.19.1")
        self.assertEqual(dialect["target"]["yaml"], "YAML 1.2.2")
        self.assertEqual(dialect["target"]["decision"], "W03-D29")
        self.assertIs(dialect["target"]["asserted_by_check"], True)
        self.assertEqual(dialect["schema"]["dialect"], "JSON Schema Draft 2020-12")
        self.assertEqual(dialect["schema"]["format"], "annotation-only")
        self.assertEqual(dialect["dates"]["rule"], "FM-DATE")
        schema = json.loads(SCHEMA_FILE.read_text("utf-8"))
        self.assertEqual(
            schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )

    def test_each_recorded_loader_is_the_one_loader(self) -> None:
        loaders = self.recorded()["current"]["loaders"]
        self.assertEqual(
            {item["path"] for item in loaders},
            {
                "scripts/validate-markdown-profiles.py",
                "scripts/document_lifecycle.py",
                "scripts/validate-agent-governance.py",
                "scripts/validate-links-and-owners.py",
                "scripts/validation/repository/quality.py",
            },
        )
        for item in loaders:
            with self.subTest(path=item["path"]):
                self.assertEqual(item["loader"], "frontmatter_yaml.load_frontmatter")
                self.assertEqual(item["duplicate_keys"], "refused")
                self.assertEqual(item["timestamps"], "kept-as-text")
                source = (ROOT / item["path"]).read_text("utf-8")
                self.assertRegex(source, r"from frontmatter_yaml import[^\n]*")
                self.assertIn("load_frontmatter(", source)

    def test_the_one_loader_behaves_as_recorded(self) -> None:
        with self.assertRaises(FrontmatterError) as caught:
            load_frontmatter("a: 1\na: 2\n")
        self.assertEqual(caught.exception.reason, "duplicate-key")
        self.assertEqual(
            load_frontmatter("updated: 2026-11-13\n"), {"updated": "2026-11-13"}
        )


if __name__ == "__main__":
    unittest.main()
