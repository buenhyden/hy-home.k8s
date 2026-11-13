"""Load one governed frontmatter block as YAML 1.2 with stated refusals."""

from __future__ import annotations

from typing import Any

try:
    from ruamel.yaml import YAML
    from ruamel.yaml.composer import Composer, ComposerError
    from ruamel.yaml.constructor import SafeConstructor
    from ruamel.yaml.error import YAMLError
    from ruamel.yaml.events import AliasEvent, ScalarEvent
    from ruamel.yaml.parser import Parser
    from ruamel.yaml.tokens import DirectiveToken
except ImportError as exc:  # pragma: no cover - exercised by the missing-library test
    raise ImportError(
        "frontmatter needs ruamel.yaml, which the hashed lock "
        ".github/requirements/ci-validation.txt pins. Install it with the command "
        "in .agents/governance/git.md: python3 -m pip install --only-binary :all: "
        "--require-hashes -r .github/requirements/ci-validation.txt"
    ) from exc

_TIMESTAMP = "tag:yaml.org,2002:timestamp"
_MERGE = "tag:yaml.org,2002:merge"
_STR = "tag:yaml.org,2002:str"


class FrontmatterError(ValueError):
    """A refused frontmatter block: a reason code and, for a duplicate, the key."""

    def __init__(self, reason: str, key: object = None):
        self.reason = reason
        self.key = key
        super().__init__(reason if key is None else f"{reason}: {key}")


class _Parser(Parser):
    def process_directives(self) -> Any:
        if self.scanner.check_token(DirectiveToken):
            raise FrontmatterError("directive")
        return super().process_directives()


class _Composer(Composer):
    def compose_node(self, parent: Any, index: Any) -> Any:
        if self.parser.check_event(AliasEvent):
            raise FrontmatterError("alias")
        event = self.parser.peek_event()
        if event.anchor is not None:
            raise FrontmatterError("anchor")
        if event.ctag is not None:
            raise FrontmatterError("tag")
        is_key = parent is not None and index is None
        if is_key and not isinstance(event, ScalarEvent):
            raise FrontmatterError("non-scalar-key")
        node = super().compose_node(parent, index)
        if node.tag == _MERGE:
            raise FrontmatterError("merge-key")
        return node


class _Constructor(SafeConstructor):
    def check_mapping_key(
        self, node: Any, key_node: Any, mapping: Any, key: Any, value: Any
    ) -> bool:
        if key in mapping:
            raise FrontmatterError("duplicate-key", key)
        return True


# Timestamps stay text: a date is a string here, as the profile check always read it.
_Constructor.add_constructor(_TIMESTAMP, SafeConstructor.construct_yaml_str)


def load_frontmatter(text: str) -> Any:
    """Return the plain Python value of one frontmatter block or raise FrontmatterError."""

    yaml = YAML(typ="safe", pure=True)
    yaml.version = (1, 2)
    yaml.Parser = _Parser
    yaml.Composer = _Composer
    yaml.Constructor = _Constructor
    try:
        return yaml.load(text)
    except FrontmatterError:
        raise
    except RecursionError as exc:
        raise FrontmatterError("too-deep") from exc
    except ComposerError as exc:
        reason = (
            "multi-document"
            if exc.problem == "but found another document"
            else "invalid-yaml"
        )
        raise FrontmatterError(reason) from exc
    except YAMLError as exc:
        raise FrontmatterError("invalid-yaml") from exc
