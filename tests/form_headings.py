"""Section headings of a Stage 99 common form, read from the registry that owns them.

Fixture builders compose a current-form body from `form_body` so a heading the
registry renames or reorders is not pinned again in a test literal.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "docs/99.templates/registry.json"
FILLER = "Concrete fixture text."


@cache
def _sections(form_id: str) -> tuple[dict, ...]:
    forms = json.loads(REGISTRY.read_text(encoding="utf-8"))["common_forms"]["forms"]
    return tuple(next(form for form in forms if form["form_id"] == form_id)["sections"])


def form_body(
    form_id: str,
    content: dict[str, list[str]] | None = None,
    *,
    filler: str = FILLER,
    partial: bool = False,
) -> list[str]:
    """Heading lines of `form_id` in registry order, each followed by its body.

    A section's body is `content[title]`; otherwise a leaf gets `filler` and a
    parent gets nothing. A section that is not required appears only when
    `content` names it or a descendant. `partial` renders only the named
    sections and their ancestors. A title the form does not register raises,
    so a renamed section fails the fixture instead of vanishing from it.
    """

    content = content or {}
    seen: set[str] = set()

    def named(section: dict) -> bool:
        return section["title"] in content or any(
            named(child) for child in section.get("children", [])
        )

    def walk(sections) -> list[str]:
        lines: list[str] = []
        for section in sorted(sections, key=lambda item: item["order"]):
            title, children = section["title"], section.get("children", [])
            if (partial or section["requiredness"] != "required") and not named(
                section
            ):
                continue
            seen.add(title)
            lines.append(f"{'#' * section['level']} {title}")
            lines.extend(content.get(title, [] if children else [filler]))
            lines.extend(walk(children))
        return lines

    lines = walk(_sections(form_id))
    unknown = sorted(set(content) - seen)
    if unknown:
        raise KeyError(f"{form_id} registers no section {unknown}")
    return lines
