#!/usr/bin/env python3
"""Add logical de-duplication metadata to Obsidian atomic notes.

This script never deletes, moves, or renames files. It only:
- adds a canonical_id frontmatter field when missing;
- gives punctuation/spacing-only title variants the same canonical_id;
- appends a duplicate_of blockquote to non-canonical duplicates.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "obsidian"
SYSTEM_DIR = VAULT / "wiki" / "system"


@dataclass
class Note:
    path: Path
    body: str
    rest: str
    keys: set[str]
    title: str
    canonical_id: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    closing_end = text.find("\n", end + 4)
    if closing_end == -1:
        closing_end = len(text)
    body = text[4:end]
    rest = text[closing_end + 1 :] if closing_end < len(text) else ""
    return body, rest


def frontmatter_keys(body: str) -> set[str]:
    keys: set[str] = set()
    for line in body.splitlines():
        match = re.match(r"^([A-Za-z0-9_\-\u4e00-\u9fff]+):(?:\s|$)", line)
        if match:
            keys.add(match.group(1))
    return keys


def frontmatter_value(body: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def first_heading(rest: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", rest, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def is_atomic_frontmatter(body: str) -> bool:
    return frontmatter_value(body, "type") == "atomic"


def canonicalize_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    normalized = re.sub(r"[\s\W_]+", "", normalized, flags=re.UNICODE)
    return normalized or "untitled"


def note_link(path: Path) -> str:
    return f"[[{path.stem}]]"


def atomic_notes() -> list[Note]:
    notes: list[Note] = []
    for path in sorted(VAULT.rglob("*.md")):
        if SYSTEM_DIR in path.parents:
            continue
        text = read_text(path)
        split = split_frontmatter(text)
        if not split:
            continue
        body, rest = split
        if not is_atomic_frontmatter(body):
            continue
        title = frontmatter_value(body, "title") or first_heading(rest) or path.stem
        notes.append(
            Note(
                path=path,
                body=body,
                rest=rest,
                keys=frontmatter_keys(body),
                title=title,
                canonical_id=canonicalize_title(title),
            )
        )
    return notes


def set_frontmatter_field(text: str, key: str, value: str) -> str:
    split = split_frontmatter(text)
    if not split:
        return text
    body, rest = split
    keys = frontmatter_keys(body)
    if key in keys:
        return text
    body = body.rstrip() + f"\n{key}: {yaml_scalar(value)}"
    return f"---\n{body}\n---\n{rest}"


def append_duplicate_marker(text: str, master: Path) -> str:
    marker = f"> duplicate_of: {note_link(master)}"
    if marker in text or re.search(r"^>\s*duplicate_of:\s*\[\[.+?\]\]\s*$", text, flags=re.MULTILINE):
        return text
    return text.rstrip() + f"\n\n{marker}\n"


def main() -> None:
    notes = atomic_notes()
    groups: dict[str, list[Note]] = {}
    for note in notes:
        groups.setdefault(note.canonical_id, []).append(note)

    changed = 0
    duplicate_count = 0
    for canonical_id, group in sorted(groups.items()):
        master = sorted(group, key=lambda note: rel(note.path))[0]
        for note in group:
            text = read_text(note.path)
            new_text = set_frontmatter_field(text, "canonical_id", canonical_id)
            if note.path != master.path:
                new_text = append_duplicate_marker(new_text, master.path)
                duplicate_count += 1
            if new_text != text:
                write_text(note.path, new_text)
                changed += 1

    print(f"Atomic notes scanned: {len(notes)}")
    print(f"Logical groups: {len(groups)}")
    print(f"Duplicate notes marked: {duplicate_count}")
    print(f"Files changed: {changed}")


if __name__ == "__main__":
    main()
