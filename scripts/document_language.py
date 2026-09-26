"""SPEC-0093: pure rules that judge a document's language."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

HANGUL = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]")
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(`+)(?!`).*?(?<!`)\1(?!`)")
LINK_DESTINATION = re.compile(r"\]\([^)]*\)|\]\[[^\]]*\]")
BARE_URL = re.compile(r"<?https?://[^\s>]+>?")
COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:\s|$)")
REFERENCE_DEFINITION = re.compile(r"^ {0,3}\[[^\]]+\]:\s")
AUTHOR_PROMPT = re.compile(r"<!--\s*Author prompt:(.*?)-->", re.S)
ARCHIVE_PREFIX = "docs/98.archive/"
ARCHIVE_INDEX = "docs/98.archive/README.md"


def _body(text: str) -> str:
    """Blank the frontmatter so line numbers stay true."""

    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return "\n" * text[: end + 4].count("\n") + text[end + 4 :]
    return text


def _blank_comments(text: str) -> str:
    return COMMENT.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def _outside_code(text: str) -> list[str]:
    """Lines with fenced blocks blanked and code spans removed."""

    lines: list[str] = []
    fence: str | None = None
    for line in text.split("\n"):
        opener = FENCE.match(line)
        if fence is None and opener:
            fence = opener.group(1)[0] * 3
            lines.append("")
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                fence = None
            lines.append("")
            continue
        lines.append(CODE_SPAN.sub("", line))
    return lines


def _hangul_lines(lines: list[str]) -> list[str]:
    return [
        f"line {number}: {line.strip()[:60]}"
        for number, line in enumerate(lines, start=1)
        if HANGUL.search(line)
    ]


def _paragraphs(lines: list[str]) -> list[tuple[str | None, str]]:
    """Plain and blockquote paragraphs, each with its H2 section."""

    found: list[tuple[str | None, str]] = []
    section: str | None = None
    buffer: list[str] = []
    in_list = False
    after_blank = True

    def flush() -> None:
        if buffer:
            found.append((section, " ".join(buffer)))
            buffer.clear()

    for line in lines:
        stripped = line.strip()
        heading = HEADING.match(line)
        if heading:
            flush()
            in_list = False
            level = len(heading.group(1))
            if level == 1:
                section = None
            elif level == 2:
                section = heading.group(2)
            after_blank = True
            continue
        if not stripped:
            flush()
            after_blank = True
            continue
        if LIST_ITEM.match(line):
            flush()
            in_list, after_blank = True, False
            continue
        if in_list:
            # An indented line, or a lazy line right after the item, continues it.
            if line.startswith((" ", "\t")) or not after_blank:
                after_blank = False
                continue
            in_list = False
        after_blank = False
        if (
            stripped.startswith(("|", "<"))
            or REFERENCE_DEFINITION.match(line)
            or line.startswith(("    ", "\t"))
        ):
            flush()
            continue
        buffer.append(
            stripped.lstrip(">").strip() if stripped.startswith(">") else stripped
        )
    flush()
    return found


def _latin_words(paragraph: str) -> int:
    text = BARE_URL.sub("", LINK_DESTINATION.sub("]", paragraph))
    return len(LATIN_WORD.findall(text))


def classify(
    path: PurePosixPath,
    profile_id: str,
    mode: str,
    template_output: str | None,
    terminal: bool,
    contract: Any,
) -> str | None:
    """Name the language rule a document answers to, or None when unchecked."""

    value = path.as_posix()
    if value.startswith(contract.english_only_roots):
        return "english-only"
    if value.startswith(ARCHIVE_PREFIX) and value != ARCHIVE_INDEX:
        return None
    if mode == "template":
        if template_output is None:
            return None
        korean = template_output in contract.korean_first_profiles
        return "template-korean" if korean else "template-english"
    if mode not in {"authored", "router"} or terminal:
        return None
    if profile_id in contract.korean_first_profiles:
        return "korean-first"
    return "english-first"


def findings(text: str, language: str, contract: Any) -> list[tuple[str, str]]:
    """Return (rule_id, detail) pairs for one document under one language."""

    if language == "english-only":
        return [("LANG-ENGLISH-ONLY", item) for item in _hangul_lines(text.split("\n"))]
    body = _body(text)
    if language == "template-korean":
        return [
            ("LANG-TEMPLATE", f"author prompt without Hangul: {prompt.strip()[:60]}")
            for prompt in AUTHOR_PROMPT.findall(body)
            if not HANGUL.search(prompt)
        ]
    if language == "template-english":
        return [("LANG-TEMPLATE", item) for item in _hangul_lines(_outside_code(body))]
    if language == "english-first":
        return [
            ("LANG-ENGLISH-FIRST", item) for item in _hangul_lines(_outside_code(body))
        ]
    result: list[tuple[str, str]] = []
    for section, paragraph in _paragraphs(_outside_code(_blank_comments(body))):
        if section in contract.english_sections:
            if HANGUL.search(paragraph):
                result.append(("LANG-ENGLISH-FIRST", f"{section}: {paragraph[:60]}"))
            continue
        if (
            not HANGUL.search(paragraph)
            and _latin_words(paragraph) >= contract.min_latin_words
        ):
            result.append(("LANG-KOREAN-FIRST", paragraph[:60]))
    return result
