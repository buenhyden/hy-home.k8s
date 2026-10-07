"""Selected style input isolation and private hook projection boundaries."""

from __future__ import annotations

import importlib.util
from contextlib import redirect_stdout
from io import StringIO
import os
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "selected_style_tested", ROOT / "scripts/validate-selected-style.py"
)
assert SPEC is not None and SPEC.loader is not None
STYLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STYLE)


class SelectedStyleBoundaryTest(unittest.TestCase):
    def test_manual_stage_cannot_be_removed_from_style_projection(self) -> None:
        source = STYLE.yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        source["default_stages"] = ["pre-commit"]
        with self.assertRaisesRegex(STYLE.StyleError, "manual stage"):
            STYLE._style_repositories(STYLE.yaml.safe_dump(source).encode())
        source = STYLE.yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        first_style = next(
            hook
            for repository in source["repos"]
            for hook in repository["hooks"]
            if hook["id"] == STYLE.STYLE_IDS[0]
        )
        first_style["stages"] = ["pre-commit"]
        with self.assertRaisesRegex(STYLE.StyleError, "manual stage"):
            STYLE._style_repositories(STYLE.yaml.safe_dump(source).encode())

    def test_nul_path_transport_rejects_traversal_before_reading(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            listing = Path(temporary) / "paths.z"
            listing.write_bytes(b"../outside.md\0")
            with self.assertRaisesRegex(STYLE.StyleError, "STYLE-PATH"):
                STYLE._selected_paths(Namespace(paths_file=listing, include_path=[]))

    def test_symlink_leaf_is_skipped_without_reading_external_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root / "outside"
            outside.write_bytes(b"private-data")
            (root / "link.md").symlink_to(outside)
            selected = STYLE._selected_regular_files(
                root, ["link.md"], missing_is_error=True
            )
            self.assertEqual(selected, {})
            (root / "linked-parent").symlink_to(root, target_is_directory=True)
            with self.assertRaises(OSError):
                STYLE._selected_regular_files(
                    root, ["linked-parent/outside"], missing_is_error=True
                )

    def test_hosted_missing_selected_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(STYLE.StyleError, "STYLE-NODE"):
                STYLE._selected_regular_files(
                    Path(temporary), ["absent.md"], missing_is_error=True
                )

    def test_reviewed_projection_omits_security_hooks_without_changing_them(
        self,
    ) -> None:
        source = (ROOT / ".pre-commit-config.yaml").read_bytes()
        whitespace, language, markdown = STYLE._style_repositories(source)
        identifiers = {
            hook["id"]
            for config in (whitespace, language, markdown)
            for repository in config["repos"]
            for hook in repository["hooks"]
        }
        self.assertEqual(identifiers, set(STYLE.STYLE_IDS))
        self.assertNotIn("gitleaks", identifiers)
        self.assertNotIn("detect-secrets", identifiers)
        ruff_hooks = [
            hook
            for repository in language["repos"]
            for hook in repository["hooks"]
            if hook["id"].startswith("ruff-")
        ]
        self.assertTrue(
            all(".git/trusted-ruff.toml" in hook["args"] for hook in ruff_hooks)
        )

    def test_candidate_markdown_config_and_js_stay_out_of_language_workspace(
        self,
    ) -> None:
        source = (ROOT / ".pre-commit-config.yaml").read_bytes()
        _, language, markdown = STYLE._style_repositories(source)
        selected = {
            "README.md": b"# safe\n",
            ".markdownlint-cli2.jsonc": b'{"customRules":["./rules.mjs"]}',
            "rules.mjs": b"throw new Error('candidate JS executed')\n",
            "scripts/current.py": b"pass\n",
        }
        self.assertEqual(
            STYLE._language_files(selected, language),
            {"scripts/current.py": b"pass\n"},
        )
        markdown_files = {
            path: data for path, data in selected.items() if path.endswith(".md")
        }
        self.assertEqual(markdown_files, {"README.md": b"# safe\n"})
        self.assertEqual(
            [
                hook["id"]
                for repository in markdown["repos"]
                for hook in repository["hooks"]
            ],
            ["markdownlint-cli2"],
        )

    def test_python_module_shadow_isolated_from_private_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            shadow = Path(temporary) / "pre_commit.py"
            shadow.write_text("raise RuntimeError('untrusted shadow executed')\n")
            result = subprocess.run(
                [sys.executable, "-I", "-m", "pre_commit", "--version"],
                cwd=temporary,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("pre-commit", result.stdout)

    def test_no_ambient_cache_uses_one_private_cache_across_three_phases(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            candidate = base / "candidate"
            candidate.mkdir()
            (candidate / "README.md").write_bytes(b"# safe\n")
            trusted = base / "trusted"
            trusted.mkdir()
            for name in (
                ".pre-commit-config.yaml",
                ".markdownlint-cli2.yaml",
                ".ruff.toml",
            ):
                (trusted / name).write_bytes((ROOT / name).read_bytes())
            observed = []

            def record(files, config, trusted_files, cache_environment):
                del files, config, trusted_files
                cache = Path(cache_environment["PRE_COMMIT_HOME"])
                observed.append((cache, cache.stat().st_mode & 0o777))
                self.assertTrue(
                    cache_environment["npm_config_cache"].startswith(str(cache))
                )

            with (
                patch.dict(os.environ, {}, clear=True),
                patch.object(STYLE, "_private_check", side_effect=record),
                redirect_stdout(StringIO()),
            ):
                result = STYLE.main(
                    [
                        "--root",
                        str(candidate),
                        "--config",
                        str(trusted / ".pre-commit-config.yaml"),
                        "--markdown-config",
                        str(trusted / ".markdownlint-cli2.yaml"),
                        "--ruff-config",
                        str(trusted / ".ruff.toml"),
                        "--include-path",
                        "README.md",
                    ]
                )
            self.assertEqual(result, 0)
            self.assertEqual(len(observed), 3)
            self.assertEqual(len({cache for cache, _ in observed}), 1)
            self.assertEqual({mode for _, mode in observed}, {0o700})
            self.assertFalse(observed[0][0].exists())


if __name__ == "__main__":
    unittest.main()
