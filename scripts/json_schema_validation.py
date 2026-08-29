"""Shared offline JSON Schema evaluation; policy diagnostics stay with callers."""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator, RefResolver
from jsonschema.exceptions import ValidationError


class SchemaEvaluationError(ValueError):
    """A redacted schema configuration or evaluation failure."""


class _LocalSchemaResolver(RefResolver):
    """Resolve embedded definitions only; never retrieve schema resources."""

    def resolve_remote(self, uri: str) -> Any:
        raise ValueError("external schema resources are forbidden")


def schema_errors(schema: dict[str, Any], instance: Any) -> list[ValidationError]:
    """Return sorted instance findings, or a typed value-free evaluation error."""

    try:
        Draft202012Validator.check_schema(schema)
        return sorted(
            Draft202012Validator(
                schema, resolver=_LocalSchemaResolver.from_schema(schema)
            ).iter_errors(instance),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
    except Exception:
        # jsonschema versions expose different resolver/configuration exception
        # types. None of their messages or schema values cross this boundary.
        raise SchemaEvaluationError("invalid local JSON Schema") from None
