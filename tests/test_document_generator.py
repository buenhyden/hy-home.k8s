"""Round-trip and refusal regressions of the Stage 99 document generator.

Every generable profile is generated, loaded with the one frontmatter loader and
checked with the strict profile check. Every refusal reason has a direct case
that asserts the reason ID, exit code 2 and an unchanged tree.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import importlib
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TODAY = dt.date(2026, 11, 14)
SHARED_MARKERS = ("TITLE", "OWNER", "UPDATED", "ARTIFACT_ID", "PARENT_ID")


def load_module(name: str, path: Path):
    scripts = str(SCRIPTS)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


GENERATOR = load_module(
    "document_generator_under_test", SCRIPTS / "document-generator.py"
)
PROFILE_CHECK = load_module(
    "document_generator_test_profile_check", SCRIPTS / "validate-markdown-profiles.py"
)
LOADER = importlib.import_module("frontmatter_yaml")

# profile id -> (sample target, expected identity, expected parent identity).
# Numbers are fixture values the caller writes; the generator allocates none.
SPEC = "docs/03.specs/9001-sample"
SAMPLES: dict[str, tuple[str, str | None, str | None]] = {
    "sdlc/architecture-description": (
        "docs/02.architecture/descriptions/9001-sample.md",
        "AD-9001",
        None,
    ),
    "sdlc/architecture-decision": (
        "docs/02.architecture/decisions/9001-sample.md",
        "ADR-9001",
        None,
    ),
    "sdlc/spec": (f"{SPEC}/spec.md", "SPEC-9001", None),
    "sdlc/plan": (f"{SPEC}/plan.md", "SPEC-9001-PLAN-0001", "SPEC-9001"),
    "sdlc/task": (
        f"{SPEC}/tasks/tsk-0001-sample.md",
        "SPEC-9001-TSK-0001",
        "SPEC-9001-PLAN-0001",
    ),
    "operation/guide": ("docs/05.operations/guides/9001-sample.md", "GDE-9001", None),
    "operation/policy": (
        "docs/05.operations/policies/9001-sample.md",
        "POL-9001",
        None,
    ),
    "operation/runbook": (
        "docs/05.operations/runbooks/9001-sample.md",
        "RUN-9001",
        None,
    ),
    "operation/incident": (
        "docs/05.operations/incidents/2026/inc-9001-sample/incident.md",
        "inc-2026-9001",
        None,
    ),
    "operation/postmortem": (
        "docs/05.operations/incidents/2026/inc-9001-sample/postmortem.md",
        "inc-2026-9001-PM",
        None,
    ),
    "reference/audit": (
        "docs/90.references/audits/9001-sample/m0001-sample.md",
        "AUD-9001-m0001",
        None,
    ),
    "reference/research": (
        "docs/90.references/research/9001-sample/m0001-sample.md",
        "RES-9001-m0001",
        None,
    ),
    "reference/data": (
        "docs/90.references/data/9001-sample/m0001-sample.md",
        "DATA-9001-m0001",
        None,
    ),
    "reference/audit-pack": (
        "docs/90.references/audits/9001-sample/README.md",
        "AUD-9001",
        None,
    ),
    "reference/research-pack": (
        "docs/90.references/research/9001-sample/README.md",
        "RES-9001",
        None,
    ),
    "reference/data-pack": (
        "docs/90.references/data/9001-sample/README.md",
        "DATA-9001",
        None,
    ),
    "governance/knowledge": (".agents/knowledge/sample.md", None, None),
    "governance/vocabulary": (".agents/knowledge/glossary.md", None, None),
    "governance/prompt": (".agents/prompts/sample.md", None, None),
    "governance/provider": (".claude/provider.md", None, None),
    "governance/role": (".agents/roles/sample.md", None, None),
    "governance/rule": (".agents/governance/git.md", None, None),
    "governance/skill": (".agents/workflows/work-lifecycle.md", None, None),
    "common/readme-repository": ("README.md", None, None),
    "common/readme-stage-index": ("docs/01.requirements/README.md", None, None),
    "common/readme-collection-index": (".agents/knowledge/README.md", None, None),
    "common/readme-implementation": (".agents/README.md", None, None),
    "common/readme-workspace-staging": ("_workspace/README.md", None, None),
    "common/readme-runtime-governance": (".github/repository-surface.md", None, None),
    "common/folder-agents-guide": ("scripts/AGENTS.md", None, None),
    "evaluation/task": (".agents/evaluations/harnesses/sample/task.md", None, None),
    "evaluation/score": (".agents/evaluations/harnesses/sample/score.md", None, None),
    "evaluation/results": (".agents/evaluations/results.md", None, None),
}
# A fresh document keeps these authoring findings until the author replaces
# the prompts, the starter H1, the empty sections and the sample rows.
AUTHORING_RULES = frozenset(
    {
        "BODY-AUTHOR-PROMPT",
        "BODY-H1-PLACEHOLDER",
        "BODY-HEADING-EMPTY",
        "BODY-SECTION-EMPTY",
    }
)
IDENTITY_RULES = frozenset(
    {
        "ARTIFACT-IDENTITY",
        "PARENT-IDENTITY",
        "REQUIREMENT-PACKAGE-IDENTITY",
    }
)


def frontmatter_block(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    closing = text.find("\n---\n", 4)
    return None if closing < 0 else text[4:closing]


def expected_generable_ids() -> frozenset[str]:
    """Compute the generable set from the raw registry, apart from the generator."""

    registry = json.loads(
        (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
    )
    found = set()
    for profile in registry["profiles"]:
        template = profile.get("template_source")
        if (
            profile["mode"] == "template"
            or not template
            or not template.endswith(".md")
        ):
            continue
        block = frontmatter_block((ROOT / template).read_text(encoding="utf-8")) or ""
        tokens = set(re.findall(r"\{\{([A-Z][A-Z0-9_]*)\}\}", block))
        tokens |= set(re.findall(r"__[A-Z][A-Z0-9_]*__", block))
        if tokens <= set(SHARED_MARKERS):
            found.add(profile["id"])
    return frozenset(found)


def build_tree(destination: Path) -> None:
    """Copy the Stage 99 registry, schemas and forms that the registry loader reads."""

    shutil.copytree(ROOT / "docs/99.templates", destination / "docs/99.templates")
    registry = json.loads(
        (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
    )
    for profile in registry["profiles"]:
        for named in profile.get("template_definition", {}).get("consumer_paths", ()):
            target = destination / named
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / named, target)


def snapshot(root: Path) -> list[tuple[str, str, bytes]]:
    found = []
    for directory, names, files in os.walk(root):
        for name in names + files:
            path = Path(directory, name)
            kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
            content = path.read_bytes() if kind == "file" else b""
            found.append((path.relative_to(root).as_posix(), kind, content))
    return sorted(found)


class TreeCase(unittest.TestCase):
    """A fresh fixture tree for each test, with a registry that already loads."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._base = tempfile.TemporaryDirectory(prefix="generator-base-")
        cls.addClassCleanup(cls._base.cleanup)
        build_tree(Path(cls._base.name))

    def setUp(self) -> None:
        holder = tempfile.TemporaryDirectory(prefix="generator-tree-")
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name) / "tree"
        shutil.copytree(self._base.name, self.root, symlinks=True)

    def write(self, relative: str, text: str = "x\n") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def generate(
        self, profile, target, *, title="Sample Title", owner="platform", registry=None
    ):
        return GENERATOR.generate(
            self.root, profile, title, owner, target, today=TODAY, registry=registry
        )

    def run_main(self, *arguments: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = GENERATOR.main(["--root", str(self.root), *arguments])
            except SystemExit as exit_:  # argparse usage errors
                code = exit_.code
        return code, out.getvalue(), err.getvalue()

    def refuse(self, rule: str, profile: str, target: str, **inputs: str) -> str:
        """Assert one refusal by the function and by the command, tree unchanged."""

        before = snapshot(self.root)
        with self.assertRaises(GENERATOR.Refusal) as caught:
            self.generate(profile, target, **inputs)
        self.assertEqual(caught.exception.rule_id, rule)
        code, out, err = self.run_main(
            "--profile",
            profile,
            "--title",
            inputs.get("title", "Sample Title"),
            "--owner",
            inputs.get("owner", "platform"),
            target,
        )
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        self.assertIn(rule, err)
        self.assertEqual(snapshot(self.root), before)
        return err

    def edit(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


class RoundTripTests(TreeCase):
    def setUp(self) -> None:
        super().setUp()
        self.registry = PROFILE_CHECK.load_registry(self.root)
        self.profiles = {item.profile_id: item for item in self.registry.profiles}

    def prepare(self, profile_id: str) -> str:
        """Free the sample target and give a Plan or Task its parents, as a caller would."""

        target = SAMPLES[profile_id][0]
        (self.root / target).unlink(missing_ok=True)
        parents = {"sdlc/plan": ("sdlc/spec",), "sdlc/task": ("sdlc/spec", "sdlc/plan")}
        for parent in parents.get(profile_id, ()):
            self.write(SAMPLES[parent][0])
        return target

    def test_sample_set_equals_the_generable_set_computed_from_the_registry(
        self,
    ) -> None:
        # The Requirement profile is generable by form but refused by its status rule.
        self.assertEqual(
            set(SAMPLES) | {"sdlc/requirement"}, set(expected_generable_ids())
        )
        for profile_id in SAMPLES:
            self.assertIn(profile_id, self.profiles)

    def test_every_generable_profile_round_trips(self) -> None:
        for profile_id, (target, identity, parent) in SAMPLES.items():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                self.prepare(profile_id)
                text = self.generate(profile_id, target, registry=self.registry)
                template = (ROOT / profile.template).read_text(encoding="utf-8")
                markers = {
                    "TITLE": "Sample Title",
                    "OWNER": "platform",
                    "UPDATED": "2026-11-14",
                    "ARTIFACT_ID": identity,
                    "PARENT_ID": parent,
                }
                expected = template
                for name, value in markers.items():
                    if value is not None:
                        expected = expected.replace("{{" + name + "}}", value)
                self.assertEqual(text, expected)
                for name in SHARED_MARKERS:
                    self.assertNotIn("{{" + name + "}}", text)

                block = frontmatter_block(text)
                if profile_id == "common/folder-agents-guide":
                    self.assertIsNone(block)
                else:
                    data = LOADER.load_frontmatter(block)
                    template_data = LOADER.load_frontmatter(frontmatter_block(template))
                    self.assertEqual(data["title"], "Sample Title")
                    self.assertEqual(data["owner"], "platform")
                    self.assertEqual(data["updated"], "2026-11-14")
                    self.assertEqual(data["type"], template_data["type"])
                    self.assertEqual(data["status"], template_data["status"])
                    self.assertEqual(data["version"], "0.1.0")
                    self.assertEqual(data.get("artifact_id"), identity)
                    self.assertEqual(
                        data.get("parent_ids"), None if parent is None else [parent]
                    )

                found = PROFILE_CHECK.validate_document_text(
                    text, PurePosixPath(target), profile, "strict", today=TODAY
                )
                rules = {item.rule_id for item in found}
                self.assertFalse(
                    {rule for rule in rules if rule.startswith("FM-")}
                    | (rules & IDENTITY_RULES),
                    sorted(rules),
                )
                self.assertLessEqual(rules, AUTHORING_RULES, sorted(rules))

    def test_command_writes_one_file_and_prints_one_line(self) -> None:
        for profile_id in ("sdlc/spec", "sdlc/plan", "sdlc/task"):
            target, identity, parent = SAMPLES[profile_id]
            with self.subTest(profile=profile_id):
                self.prepare(profile_id)
                before = {
                    path for path, kind, _ in snapshot(self.root) if kind == "file"
                }
                code, out, err = self.run_main(
                    *("--profile", profile_id, "--title", "Sample Title"),
                    *("--owner", "platform", target),
                )
                self.assertEqual((code, err), (0, ""))
                self.assertEqual(len(out.strip().splitlines()), 1, out)
                for word in (target, profile_id, str(identity)):
                    self.assertIn(word, out)
                if parent is not None:
                    self.assertIn(parent, out)
                created = {
                    path for path, kind, _ in snapshot(self.root) if kind == "file"
                } - before
                self.assertEqual(created, {target})

    def test_spec_plan_task_are_generated_in_order_in_a_new_package(self) -> None:
        self.assertFalse((self.root / SPEC).exists())
        for profile_id in ("sdlc/spec", "sdlc/plan", "sdlc/task"):
            target = SAMPLES[profile_id][0]
            code, out, err = self.run_main(
                *("--profile", profile_id, "--title", "Sample Title"),
                *("--owner", "platform", target),
            )
            self.assertEqual((code, err), (0, ""), out)
            self.assertTrue((self.root / target).is_file())

    def test_no_status_input_exists(self) -> None:
        before = snapshot(self.root)
        code, _, err = self.run_main(
            *("--profile", "operation/guide", "--title", "T", "--owner", "o"),
            *("--status", "active", SAMPLES["operation/guide"][0]),
        )
        self.assertEqual(code, 2)
        self.assertIn("--status", err)
        self.assertEqual(snapshot(self.root), before)

    def test_the_h1_stays_as_in_the_template(self) -> None:
        self.prepare("sdlc/spec")
        text = self.generate("sdlc/spec", SAMPLES["sdlc/spec"][0], title="Another")
        template = (
            ROOT / "docs/99.templates/templates/specs/spec.template.md"
        ).read_text(encoding="utf-8")
        heading = next(line for line in template.splitlines() if line.startswith("# "))
        self.assertIn("\n" + heading + "\n", text)
        self.assertNotIn("# Another", text)


class ProfileAndRouteRefusalTests(TreeCase):
    def test_unknown_profile(self) -> None:
        self.refuse("GENERATOR-PROFILE", "no/such-profile", "docs/x.md")

    def test_non_generable_profiles(self) -> None:
        cases = {
            "common/native-skill-package": ".agents/skills/sample/SKILL.md",
            "common/provider-native-metadata": ".claude/agents/sample.md",
            "common/provider-native-command": ".claude/commands/sample.md",
            "common/codex-agent-binding": ".codex/agents/sample.toml",
            "common/template-sdlc-spec": "docs/99.templates/templates/specs/x.md",
            "common/native-skill-reference": ".agents/skills/sample/references/x.md",
        }
        for profile_id, target in cases.items():
            with self.subTest(profile=profile_id):
                self.refuse("GENERATOR-PROFILE", profile_id, target)

    def test_target_paths_that_leave_or_miss_the_registry(self) -> None:
        for target in (
            "/tmp/9001-sample.md",
            "../9001-sample.md",
            "docs/05.operations/guides/../guides/9001-sample.md",
            "docs/05.operations/guides/./9001-sample.md",
            "docs/05.operations/guides//9001-sample.md",
            "docs/05.operations/guides/9001-sample.md/",
            "docs/05.operations/guides/9001-Sample.md",
            "notes/9001-sample.md",
            "",
        ):
            with self.subTest(target=target):
                self.refuse("GENERATOR-ROUTE", "operation/guide", target)

    def test_target_routed_to_another_profile(self) -> None:
        self.refuse("GENERATOR-ROUTE", "operation/guide", SAMPLES["sdlc/spec"][0])

    def test_symlinked_ancestor_is_refused(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="generator-outside-"))
        self.addCleanup(shutil.rmtree, outside, True)
        harnesses = self.root / ".agents/evaluations/harnesses"
        harnesses.mkdir(parents=True, exist_ok=True)
        (harnesses / "sample").symlink_to(outside)
        self.refuse("GENERATOR-ROUTE", "evaluation/task", SAMPLES["evaluation/task"][0])
        self.assertEqual(list(outside.iterdir()), [])

    def test_occupied_target_of_any_kind(self) -> None:
        guide = SAMPLES["operation/guide"][0]
        self.write(guide, "keep\n")
        self.refuse("GENERATOR-OCCUPIED", "operation/guide", guide)
        self.assertEqual((self.root / guide).read_text(encoding="utf-8"), "keep\n")
        folder = "docs/05.operations/guides/9002-sample.md"
        (self.root / folder).mkdir()
        self.refuse("GENERATOR-OCCUPIED", "operation/guide", folder)
        link = "docs/05.operations/guides/9003-sample.md"
        (self.root / link).symlink_to("missing-target")
        self.refuse("GENERATOR-OCCUPIED", "operation/guide", link)

    def test_exclusive_create_never_overwrites(self) -> None:
        name = "docs/05.operations/guides/9001-sample.md"
        path = self.write(name, "keep\n")
        with self.assertRaises(GENERATOR.Refusal) as caught:
            GENERATOR.create_exclusive(self.root, PurePosixPath(name), "new\n")
        self.assertEqual(caught.exception.rule_id, "GENERATOR-OCCUPIED")
        self.assertEqual(path.read_text(encoding="utf-8"), "keep\n")

    def test_failed_create_leaves_no_folder_behind(self) -> None:
        before = snapshot(self.root)
        target = PurePosixPath("docs/90.references/audits/9001-sample/README.md")
        with mock.patch.object(GENERATOR.os, "open", side_effect=FileExistsError):
            with self.assertRaises(GENERATOR.Refusal) as caught:
                GENERATOR.create_exclusive(self.root, target, "new\n")
        self.assertEqual(caught.exception.rule_id, "GENERATOR-OCCUPIED")
        self.assertEqual(snapshot(self.root), before)


class IdentityParentAndStatusRefusalTests(TreeCase):
    def test_identity_that_cannot_be_derived(self) -> None:
        with (
            mock.patch.object(PROFILE_CHECK, "expected_artifact_id", return_value=None),
            mock.patch.object(GENERATOR, "_profile_check", return_value=PROFILE_CHECK),
        ):
            with self.assertRaises(GENERATOR.Refusal) as caught:
                self.generate("operation/guide", SAMPLES["operation/guide"][0])
        self.assertEqual(caught.exception.rule_id, "GENERATOR-IDENTITY")

    def test_identity_owned_by_a_document_at_another_path(self) -> None:
        self.write(
            "docs/05.operations/guides/9001-other.md",
            '---\nartifact_id: "GDE-9001"\n---\n\n# Other\n',
        )
        self.refuse(
            "GENERATOR-IDENTITY", "operation/guide", SAMPLES["operation/guide"][0]
        )

    def test_identity_reserved_by_an_archived_lineage(self) -> None:
        lineage = (
            "# Requirement\n\n### Archived Lineage\n\n"
            "| Source | Kind | Summary | Path |\n| --- | --- | --- | --- |\n"
            "| SPEC-0777 | spec | retired | `docs/03.specs/0777-x/spec.md` |\n"
        )
        self.write("docs/01.requirements/0004-sample.md", lineage)
        self.refuse("GENERATOR-IDENTITY", "sdlc/spec", "docs/03.specs/0777-x/spec.md")
        # An extension of a reserved identity is reserved too.
        self.write("docs/03.specs/0777-x/spec.md")
        self.refuse("GENERATOR-IDENTITY", "sdlc/plan", "docs/03.specs/0777-x/plan.md")

    def test_plan_and_task_without_a_parent_are_refused(self) -> None:
        self.refuse("GENERATOR-PARENT", "sdlc/plan", SAMPLES["sdlc/plan"][0])
        self.write(f"{SPEC}/spec.md")
        self.refuse("GENERATOR-PARENT", "sdlc/task", SAMPLES["sdlc/task"][0])
        (self.root / SPEC / "plan.md").mkdir()
        self.refuse("GENERATOR-PARENT", "sdlc/task", SAMPLES["sdlc/task"][0])

    def test_requirement_has_no_creation_state_and_is_refused(self) -> None:
        self.refuse(
            "GENERATOR-STATUS",
            "sdlc/requirement",
            "docs/01.requirements/9001-sample.md",
        )

    def test_template_status_outside_the_creation_states_is_refused(self) -> None:
        self.edit(
            "docs/99.templates/templates/specs/spec.template.md",
            'status: "draft"',
            'status: "approved"',
        )
        self.refuse("GENERATOR-STATUS", "sdlc/spec", SAMPLES["sdlc/spec"][0])

    def test_template_without_status_in_a_stateful_domain_is_refused(self) -> None:
        self.edit(
            "docs/99.templates/templates/specs/spec.template.md",
            'status: "draft"\n',
            "",
        )
        self.refuse("GENERATOR-STATUS", "sdlc/spec", SAMPLES["sdlc/spec"][0])


class InputRefusalTests(TreeCase):
    def test_bad_titles_and_owners(self) -> None:
        target = SAMPLES["operation/guide"][0]
        bad = {
            "empty": "",
            "blank": "   ",
            "quote": 'say "hi"',
            "backslash": "back\\slash",
            "newline": "two\nlines",
            "carriage return": "two\rlines",
            "line separator": "two lines",
            "control": "bell\x07",
            "marker": "x {{ARTIFACT_ID}} y",
        }
        for name, value in bad.items():
            for field in ("title", "owner"):
                with self.subTest(field=field, value=name):
                    self.refuse(
                        "GENERATOR-INPUT", "operation/guide", target, **{field: value}
                    )

    def test_ordinary_punctuation_is_kept_verbatim(self) -> None:
        title = "Colon: hash # single 'quote' and (parentheses)"
        text = self.generate(
            "operation/guide", SAMPLES["operation/guide"][0], title=title
        )
        data = LOADER.load_frontmatter(frontmatter_block(text))
        self.assertEqual(data["title"], title)


class OutputCheckRefusalTests(TreeCase):
    GUIDE_TEMPLATE = "docs/99.templates/templates/operations/guide.template.md"

    def test_template_with_a_duplicate_key(self) -> None:
        self.edit(
            self.GUIDE_TEMPLATE,
            'version: "0.1.0"\n',
            'version: "0.1.0"\nversion: "0.1.1"\n',
        )
        self.refuse(
            "GENERATOR-OUTPUT", "operation/guide", SAMPLES["operation/guide"][0]
        )

    def test_injected_impossible_date(self) -> None:
        class ImpossibleDate(dt.date):
            def isoformat(self) -> str:
                return "2026-02-30"

        with self.assertRaises(GENERATOR.Refusal) as caught:
            GENERATOR.generate(
                self.root,
                "operation/guide",
                "T",
                "platform",
                SAMPLES["operation/guide"][0],
                today=ImpossibleDate(2026, 11, 14),
            )
        self.assertEqual(caught.exception.rule_id, "GENERATOR-OUTPUT")

    def test_profile_that_requires_a_key_its_template_lacks(self) -> None:
        path = self.root / "docs/99.templates/registry.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        profile = next(
            item for item in registry["profiles"] if item["id"] == "operation/guide"
        )
        profile["frontmatter"]["optional"].remove("superseded_by")
        profile["frontmatter"]["required"].append("superseded_by")
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        self.refuse(
            "GENERATOR-OUTPUT", "operation/guide", SAMPLES["operation/guide"][0]
        )

    def test_template_that_carries_a_key_its_profile_does_not_list(self) -> None:
        self.edit(
            self.GUIDE_TEMPLATE,
            'version: "0.1.0"\n',
            'version: "0.1.0"\nextra_key: "x"\n',
        )
        self.refuse(
            "GENERATOR-OUTPUT", "operation/guide", SAMPLES["operation/guide"][0]
        )

    def test_shared_marker_left_in_the_output(self) -> None:
        # A parent marker in a template whose route derives no parent.
        self.edit(
            self.GUIDE_TEMPLATE,
            'owner: "{{OWNER}}"\n',
            'owner: "{{OWNER}}"\nparent_ids: ["{{PARENT_ID}}"]\n',
        )
        self.refuse(
            "GENERATOR-OUTPUT", "operation/guide", SAMPLES["operation/guide"][0]
        )

    def test_a_template_that_is_not_text_is_refused(self) -> None:
        (self.root / self.GUIDE_TEMPLATE).write_bytes(b"---\n\xff\n---\n")
        self.refuse(
            "GENERATOR-PROFILE", "operation/guide", SAMPLES["operation/guide"][0]
        )


if __name__ == "__main__":
    unittest.main()
