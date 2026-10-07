"""Pure canonical-form ownership and content validation."""

import collections
import pathlib
import re


def collect_physical_form_paths(
    repository_root: pathlib.Path,
    forms_root: pathlib.Path,
) -> set[pathlib.PurePosixPath]:
    return {
        pathlib.PurePosixPath(path.relative_to(repository_root).as_posix())
        for path in forms_root.rglob("*")
        if path.is_file() and path != forms_root / "README.md"
    }


def canonical_form_contract_errors(
    physical_forms: set[pathlib.PurePosixPath],
    profile_form_references: list[tuple[str, pathlib.PurePosixPath]],
    profile_form_owners: list[tuple[str, pathlib.PurePosixPath]],
) -> list[str]:
    owners_by_form: dict[pathlib.PurePosixPath, list[str]] = collections.defaultdict(
        list
    )
    for profile_id, form_path in profile_form_owners:
        owners_by_form[form_path].append(profile_id)
    registry_forms = {form_path for _, form_path in profile_form_references}
    errors = []
    canonical_form_name = re.compile(
        r"^[a-z0-9][a-z0-9-]*\.template\.(md|yaml|graphql|proto|toml)$"
    )
    noncanonical_names = sorted(
        str(form)
        for form in physical_forms
        if not canonical_form_name.fullmatch(form.name)
    )
    if noncanonical_names:
        errors.append(
            "physical form filenames must match "
            "<name>.template.(md|yaml|graphql|proto|toml): "
            f"{noncanonical_names}"
        )
    missing = sorted(registry_forms - physical_forms, key=str)
    if missing:
        errors.append(f"registry-owned forms are missing: {missing}")
    unowned = sorted(physical_forms - set(owners_by_form), key=str)
    if unowned:
        errors.append(f"physical forms have no registry owner: {unowned}")
    duplicate_owners = {
        str(form): sorted(owners)
        for form, owners in owners_by_form.items()
        if len(owners) != 1
    }
    if duplicate_owners:
        errors.append(
            f"physical forms must have exactly one profile owner: {duplicate_owners}"
        )
    return errors


def canonical_form_content_errors(
    form_sources: dict[pathlib.PurePosixPath, str],
    registry_form_owners: list[tuple[str, pathlib.PurePosixPath]],
    registry_profiles_by_id: dict[str, object],
) -> list[str]:
    def html_comments_balanced(source: str) -> bool:
        offset = 0
        in_comment = False
        while offset < len(source):
            marker = "-->" if in_comment else "<!--"
            marker_offset = source.find(marker, offset)
            opposite = "<!--" if in_comment else "-->"
            opposite_offset = source.find(opposite, offset)
            if opposite_offset != -1 and (
                marker_offset == -1 or opposite_offset < marker_offset
            ):
                return False
            if marker_offset == -1:
                break
            in_comment = not in_comment
            offset = marker_offset + len(marker)
        return not in_comment

    def strip_html_comments(raw_line: str, in_comment: bool) -> tuple[str, bool]:
        visible = []
        offset = 0
        while offset < len(raw_line):
            if in_comment:
                end = raw_line.find("-->", offset)
                if end == -1:
                    return "".join(visible), True
                offset = end + 3
                in_comment = False
                continue
            start = raw_line.find("<!--", offset)
            if start == -1:
                visible.append(raw_line[offset:])
                break
            visible.append(raw_line[offset:start])
            offset = start + 4
            in_comment = True
        return "".join(visible), in_comment

    def markdown_sections(source: str, heading_level: int) -> dict[str, str]:
        sections: dict[str, list[str]] = collections.defaultdict(list)
        current_heading = None
        in_comment = False
        fence_character = None
        fence_length = 0
        opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
        for raw_line in source.splitlines(keepends=True):
            if fence_character is not None:
                closing = re.compile(
                    rf"^ {{0,3}}{re.escape(fence_character)}"
                    rf"{{{fence_length},}}[ \t]*(?:\r?\n)?$"
                )
                if closing.fullmatch(raw_line):
                    fence_character = None
                    fence_length = 0
                if current_heading is not None:
                    sections[current_heading].append(raw_line)
                continue
            visible, in_comment = strip_html_comments(raw_line, in_comment)
            fence = opening.match(visible)
            if fence:
                marker = fence.group(1)
                if marker[0] != "`" or "`" not in fence.group(2):
                    fence_character = marker[0]
                    fence_length = len(marker)
                if current_heading is not None:
                    sections[current_heading].append(raw_line)
                continue
            heading = re.match(
                r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*?)[ \t]*(?:\r?\n)?$",
                visible,
            )
            if heading and len(heading.group(1)) <= heading_level:
                if len(heading.group(1)) == heading_level:
                    current_heading = re.sub(
                        r"[ \t]+##+[ \t]*$", "", heading.group(2).strip()
                    )
                    sections.setdefault(current_heading, [])
                else:
                    current_heading = None
                continue
            if current_heading is not None:
                sections[current_heading].append(raw_line)
        return {heading: "".join(lines) for heading, lines in sections.items()}

    errors = []
    retired_markers = (
        "Target: " + "docs/",
        "Owner docs from target directory",
        "Replace every placeholder",
        "Describe the topic-specific",
    )
    author_comment = re.compile(r"<!-- Author prompt: [^\n]+ -->")
    useful_author_comment = re.compile(
        r"(?m)^[ \t]*<!-- Author prompt: (?P<prompt>[^\n]*?) -->[ \t]*$"
    )
    markdownlint_directive = "<!-- markdownlint-disable-file MD033 MD041 -->"
    archive_envelope_marker = (
        "<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->"
    )
    archive_migration_marker = "<!-- archive-migration-ledger:v1 format=json -->"
    # The migration form also opens the consumer block the Archive parser owns.
    archive_consumers_marker = "<!-- archive-historical-consumers:v1 format=json -->"
    for form_path, source in sorted(
        form_sources.items(), key=lambda item: str(item[0])
    ):
        for marker in retired_markers:
            if marker in source:
                errors.append(f"{form_path} contains retired form residue: {marker}")
        if form_path.suffix != ".md":
            continue
        if not html_comments_balanced(source):
            errors.append(f"{form_path} contains an unbalanced HTML comment")
            continue
        for match in re.finditer(r"<!--.*?-->", source, re.DOTALL):
            comment = match.group(0)
            if comment in {
                markdownlint_directive,
                archive_envelope_marker,
                archive_migration_marker,
                archive_consumers_marker,
            } or author_comment.fullmatch(comment):
                continue
            errors.append(f"{form_path} contains a non-author form comment")

    for profile_id, form_path in registry_form_owners:
        profile = registry_profiles_by_id[profile_id]
        source = form_sources.get(form_path)
        if source is None or form_path.suffix != ".md":
            continue
        required_section_groups = [(2, profile.headings.required, False)]
        for (
            heading_level,
            required_headings,
            allow_structured_starter,
        ) in required_section_groups:
            sections = markdown_sections(source, heading_level)
            for heading in required_headings:
                section_body = sections.get(heading, "")
                if (
                    allow_structured_starter
                    and re.sub(r"<!--.*?-->", "", section_body, flags=re.DOTALL).strip()
                ):
                    continue
                prompts = [
                    match.group("prompt").strip()
                    for match in useful_author_comment.finditer(section_body)
                ]
                if not any(prompts):
                    errors.append(
                        f"{form_path} section {heading!r} must contain a useful Author prompt"
                    )
        contract = profile.body_contract
        if contract is None:
            continue
        table_heading = f"### {contract.table_heading}"
        table_header = "| " + " | ".join(contract.required_columns) + " |"
        if source.count(table_heading) != 1 or source.count(table_header) != 1:
            errors.append(
                f"{form_path} must contain one exact registry-owned lifecycle table"
            )
    return errors
