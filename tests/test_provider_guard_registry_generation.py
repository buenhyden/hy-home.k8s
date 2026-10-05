"""The native pre-action guard reads only known Stage 99 registry formats."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "provider_guard_generation", ROOT / "scripts/provider_write_guard.py"
)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class RegistryGenerationAdmissionTests(unittest.TestCase):
    def test_known_formats_admit_routes_and_unknown_format_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guard-registry-format-") as directory:
            root = Path(directory)
            target = root / "docs/99.templates/registry.json"
            target.parent.mkdir(parents=True)
            for generation in (9, 10, 11, True):
                with self.subTest(generation=generation):
                    target.write_text(
                        json.dumps(
                            {
                                "schema_version": generation,
                                "profiles": [
                                    {
                                        "id": "common/readme",
                                        "path_pattern": r"^docs/README\.md$",
                                        "template_source": None,
                                    }
                                ],
                            }
                        ),
                        encoding="utf-8",
                    )
                    if type(generation) is int and generation in (9, 10):
                        routes = GUARD.load_document_routes(str(root))
                        self.assertEqual(routes[0]["id"], "common/readme")
                        self.assertTrue(
                            routes[0]["pattern"].fullmatch("docs/README.md")
                        )
                    else:
                        with self.assertRaises(SystemExit) as rejected:
                            GUARD.load_document_routes(str(root))
                        self.assertEqual(rejected.exception.code, 2)
            target.write_text('{"schema_version":10,"profiles":[', encoding="utf-8")
            with self.assertRaises(SystemExit) as malformed:
                GUARD.load_document_routes(str(root))
            self.assertEqual(malformed.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
