"""Shared offline JSON Schema evaluation; policy diagnostics stay with callers."""

from __future__ import annotations

import functools
import json
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


class SchemaEvaluationError(ValueError):
    """A redacted schema configuration or evaluation failure."""


def _forbid_external(uri: str) -> Any:
    """Refuse every reference this repository does not already carry."""

    raise ValueError("external schema resources are forbidden")


try:
    # jsonschema 4.18 supersedes RefResolver with the referencing registry and
    # deprecates the old name on import. A validator writes evidence, so the
    # warning that import would print is itself a defect on the pinned
    # interpreter; the older path stays for interpreters without referencing.
    from referencing import Registry
    from referencing.jsonschema import DRAFT202012

    def _validator(schema: dict[str, Any]) -> Draft202012Validator:
        registry = Registry(retrieve=_forbid_external).with_resource(
            "", DRAFT202012.create_resource(schema)
        )
        return Draft202012Validator(schema, registry=registry)

except ImportError:
    from jsonschema import RefResolver

    class _LocalSchemaResolver(RefResolver):
        """Resolve embedded definitions only; never retrieve schema resources."""

        def resolve_remote(self, uri: str) -> Any:
            return _forbid_external(uri)

    def _validator(schema: dict[str, Any]) -> Draft202012Validator:
        return Draft202012Validator(
            schema, resolver=_LocalSchemaResolver.from_schema(schema)
        )


@functools.lru_cache(maxsize=32)
def _checked_validator(schema_text: str) -> Draft202012Validator:
    """Check one schema against its meta-schema once per distinct content.

    The key is the canonical JSON text, so a changed schema is checked again; a
    schema that fails the check raises and is never cached.
    """

    schema = json.loads(schema_text)
    Draft202012Validator.check_schema(schema)
    return _validator(schema)


def schema_errors(schema: dict[str, Any], instance: Any) -> list[ValidationError]:
    """Return sorted instance findings, or a typed value-free evaluation error."""

    try:
        validator = _checked_validator(
            json.dumps(schema, sort_keys=True, ensure_ascii=False, allow_nan=False)
        )
        return sorted(
            validator.iter_errors(instance),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
    except Exception:
        # jsonschema versions expose different resolver/configuration exception
        # types. None of their messages or schema values cross this boundary.
        raise SchemaEvaluationError("invalid local JSON Schema") from None
