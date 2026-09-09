"""Guard the purity contract that shared Markdown rendering caches depend on."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate-links-and-owners.py"

# A paragraph line, a setext delimiter that is not also a thematic break, and a
# definition. Whether the delimiter closes the paragraph decides whether the
# definition is reachable, and lazy-line provenance decides the delimiter.
LAZY_SENSITIVE_TEXT = "text\n===\n[label]: target\n"
DELIMITER_LINE = frozenset({1})


def load_link_module():
    """Load the canonical link owner under a private module identity."""

    spec = importlib.util.spec_from_file_location("_render_cache_subject", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical link owner is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts_path = str(MODULE_PATH.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


class ReferenceDefinitionInputIdentityTest(unittest.TestCase):
    """Lazy-line provenance is part of the scanner input, not decoration."""

    @classmethod
    def setUpClass(cls):
        cls.module = load_link_module()

    def test_lazy_lines_change_the_parsed_definitions(self):
        scan = self.module._reference_definitions_with_spans
        closed = scan(LAZY_SENSITIVE_TEXT, lazy_lines=frozenset())
        left_open = scan(LAZY_SENSITIVE_TEXT, lazy_lines=DELIMITER_LINE)
        self.assertNotEqual(
            closed,
            left_open,
            "a lazy delimiter line must keep the paragraph open",
        )

    def test_rendered_provenance_survives_string_equality(self):
        """A rendered string and its plain twin compare and hash alike."""

        rendered = self.module.RenderedMarkdown(LAZY_SENSITIVE_TEXT, DELIMITER_LINE)
        plain = LAZY_SENSITIVE_TEXT
        self.assertEqual(rendered, plain)
        self.assertEqual(hash(rendered), hash(plain))
        scan = self.module._reference_definitions_with_spans
        self.assertNotEqual(
            scan(rendered),
            scan(plain),
            "provenance carried on the value must reach the scanner, so a cache"
            " keyed on the text alone would answer one input with the other",
        )

    def test_returned_definitions_mapping_is_caller_owned(self):
        scan = self.module._reference_definitions_with_spans
        text = "[label]: target\n"
        first, _ = scan(text)
        first["injected"] = "value"
        second, _ = scan(text)
        self.assertNotIn(
            "injected",
            second,
            "callers own the mapping they receive from the scanner",
        )

    def test_container_rendering_depends_only_on_its_text(self):
        """The container renderer ignores provenance carried on its argument."""

        render = self.module._rendered_container_lines
        rendered = self.module.RenderedMarkdown(LAZY_SENSITIVE_TEXT, DELIMITER_LINE)
        self.assertEqual(
            render(rendered),
            render(LAZY_SENSITIVE_TEXT),
            "equal text must render to equal container lines",
        )


if __name__ == "__main__":
    unittest.main()
