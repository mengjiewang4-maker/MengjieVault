#!/usr/bin/env python3
"""Layer a Zotero/Better BibTeX workflow onto the existing Obsidian vault.

The script is intentionally conservative:
- it never deletes, moves, or renames existing notes;
- it only adds missing frontmatter fields to source notes;
- it only appends the standard Zotero sections when they are absent;
- atomic-note generation is opt-in and only uses explicit extraction bullets.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "obsidian"
RAW_PAPERS = VAULT / "raw" / "papers"
WIKI_PAPERS = VAULT / "wiki" / "papers"
TEMPLATES = VAULT / "wiki" / "system" / "templates"
WORKFLOWS = VAULT / "wiki" / "system" / "workflows"

SOURCE_SECTIONS = ("## Zotero Notes", "## 可拆分知识点")
ATOMIC_SECTION_MAP = {
    "concepts": ("concept", 20),
    "concept": ("concept", 20),
    "概念": ("concept", 20),
    "models": ("model", 30),
    "model": ("model", 30),
    "模型": ("model", 30),
    "figures": ("figure", 40),
    "figure": ("figure", 40),
    "fig": ("figure", 40),
    "图": ("figure", 40),
    "图表": ("figure", 40),
    "methods": ("method", 50),
    "method": ("method", 50),
    "方法": ("method", 50),
    "流程": ("method", 50),
    "insights": ("insight", 10),
    "insight": ("insight", 10),
    "洞察": ("insight", 10),
}
ATOMIC_CATEGORY_LABELS = {
    "concept": "定义型原子笔记",
    "model": "方法型原子笔记",
    "figure": "图解型原子笔记",
    "method": "流程型原子笔记",
    "insight": "洞察型原子笔记",
}
SOURCE_DIR_HINTS = ("papers", "literature", "来源", "文献")
CONCEPT_DIR_HINTS = ("concept", "concepts", "topic", "topics", "knowledge", "概念", "主题", "知识")
REVIEW_DIR_HINTS = ("review", "reviews", "summary", "summaries", "report", "reports", "综述", "总结", "报告")
SKIP_NAMES = {"README.md", "AGENTS.md"}


@dataclass
class Frontmatter:
    start: str
    body: str
    rest: str
    keys: set[str]


@dataclass
class AtomicItem:
    title: str
    detail: str
    category: str
    tags: list[str]
    priority: int


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def split_frontmatter(text: str) -> Frontmatter:
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            closing_end = text.find("\n", end + 4)
            if closing_end == -1:
                closing_end = len(text)
            body = text[4:end]
            rest = text[closing_end + 1 :] if closing_end < len(text) else ""
            return Frontmatter("---\n", body, rest, frontmatter_keys(body))
    return Frontmatter("", "", text, set())


def frontmatter_keys(body: str) -> set[str]:
    keys: set[str] = set()
    for line in body.splitlines():
        match = re.match(r"^([A-Za-z0-9_\-\u4e00-\u9fff]+):(?:\s|$)", line)
        if match:
            keys.add(match.group(1))
    return keys


def yaml_scalar(value: str | int | None) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, int):
        return str(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: list[str]) -> str:
    if not values:
        return "[]"
    return "\n" + "\n".join(f"  - {yaml_scalar(value)}" for value in values)


def yaml_link_list(values: list[str]) -> str:
    return yaml_list([f"[[{value}]]" if not value.startswith("[[") else value for value in values])


def first_heading(text: str) -> str | None:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def existing_title(frontmatter: str) -> str | None:
    match = re.search(r"^title:\s*(.+?)\s*$", frontmatter, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def infer_title(path: Path, text: str, fm: Frontmatter) -> str:
    return existing_title(fm.body) or first_heading(fm.rest or text) or path.stem


def frontmatter_value(body: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def infer_year(path: Path, text: str, fm: Frontmatter | None = None) -> str:
    match = re.search(r"\b(19\d{2}|20\d{2})\b", path.stem)
    if match:
        return match.group(1)

    body_text = split_frontmatter(text).rest if fm is None else fm.rest

    metadata_patterns = (
        r"(?:年份|发表年份|出版年份)\s*[：:]\s*(19\d{2}|20\d{2})",
        r"(?:paper year|publication year|year)\s*[：:]\s*(19\d{2}|20\d{2})",
    )
    for pattern in metadata_patterns:
        match = re.search(pattern, body_text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    if fm:
        existing = frontmatter_value(fm.body, "year")
        if re.fullmatch(r"19\d{2}|20\d{2}", existing) and existing != "2026":
            return existing

    for source in (body_text[:2500],):
        match = re.search(r"\b(19\d{2}|20\d{2})\b", source)
        if match:
            return match.group(1)
    return ""


def infer_authors(path: Path) -> list[str]:
    stem = path.stem
    match = re.match(r"^(.+?)-(?:19\d{2}|20\d{2}|unknown)-", stem)
    if not match:
        return []
    raw = match.group(1).strip()
    if not raw or len(raw) > 80:
        return []
    if any(token in raw.lower() for token in ("the ", "a ", "an ")):
        return []
    return [part.strip() for part in re.split(r"\s*(?:,| and |&)\s*", raw) if part.strip()]


def infer_doi(text: str) -> str:
    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", text)
    return match.group(0).rstrip(".,;") if match else ""


def infer_journal(text: str) -> str:
    patterns = (
        r"期刊[：:]\s*([^\n]+)",
        r"Journal[：:]\s*([^\n]+)",
        r"Venue[：:]\s*([^\n]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().strip("`")
    return ""


def infer_citekey(path: Path, title: str, year: str, existing: set[str]) -> str:
    author = infer_authors(path)
    if author:
        seed = author[0]
    else:
        words = re.findall(r"[A-Za-z][A-Za-z0-9]+", title)
        seed = words[0] if words else path.stem
    base = re.sub(r"[^A-Za-z0-9]+", "", seed).lower()
    base = base or "source"
    citekey = f"{base}{year}" if year else base
    candidate = citekey
    index = 2
    while candidate in existing:
        candidate = f"{citekey}_{index}"
        index += 1
    existing.add(candidate)
    return candidate


def infer_related_concepts(text: str) -> list[str]:
    concepts: list[str] = []
    seen: set[str] = set()
    for link in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", text):
        normalized = link.strip()
        lower = normalized.lower()
        if any(hint in lower for hint in ("概念/", "concept", "topic", "比较/", "综述/")):
            if normalized not in seen:
                concepts.append(f"[[{normalized}]]")
                seen.add(normalized)
    return concepts[:12]


def source_note_paths() -> list[Path]:
    paths: list[Path] = []
    for base in (RAW_PAPERS, WIKI_PAPERS / "notes"):
        if base.exists():
            paths.extend(sorted(path for path in base.glob("*.md") if path.name not in SKIP_NAMES))
    return paths


def replace_simple_frontmatter_value(text: str, key: str, value: str) -> str:
    fm = split_frontmatter(text)
    if not fm.start or key not in fm.keys:
        return text
    pattern = rf"^({re.escape(key)}:\s*).*$"
    new_body = re.sub(pattern, rf"\g<1>{value}", fm.body, count=1, flags=re.MULTILINE)
    return f"---\n{new_body.rstrip()}\n---\n{fm.rest}"


def append_frontmatter_fields(path: Path, existing_citekeys: set[str], refresh_citekeys: bool = False) -> bool:
    text = read_text(path)
    fm = split_frontmatter(text)
    title = infer_title(path, text, fm)
    year = infer_year(path, text, fm)
    fields: list[tuple[str, str]] = []

    def add_missing(key: str, value: str) -> None:
        if key not in fm.keys:
            fields.append((key, value))

    if "citekey" not in fm.keys:
        add_missing("citekey", yaml_scalar(infer_citekey(path, title, year, existing_citekeys)))
    if "title" not in fm.keys:
        add_missing("title", yaml_scalar(title))
    if "authors" not in fm.keys:
        add_missing("authors", yaml_list(infer_authors(path)))
    if "year" not in fm.keys:
        add_missing("year", yaml_scalar(year))
    if "journal" not in fm.keys:
        add_missing("journal", yaml_scalar(infer_journal(text)))
    if "doi" not in fm.keys:
        add_missing("doi", yaml_scalar(infer_doi(text)))
    if "zotero" not in fm.keys:
        add_missing("zotero", "")
    if "tags" not in fm.keys:
        add_missing("tags", yaml_list(["literature", "source", "paper", "zotero"]))
    if "status" not in fm.keys:
        add_missing("status", yaml_scalar("unread"))
    if "related_concepts" not in fm.keys:
        add_missing("related_concepts", yaml_list(infer_related_concepts(text)))

    changed = False
    if fields:
        lines = []
        if fm.body.strip():
            lines.append(fm.body.rstrip())
        lines.extend(f"{key}: {value}" for key, value in fields)
        new_fm = "\n".join(lines).rstrip() + "\n"
        text = f"---\n{new_fm}---\n{fm.rest}"
        changed = True

    if refresh_citekeys:
        refreshed = infer_citekey(path, title, year, existing_citekeys)
        new_text = replace_simple_frontmatter_value(text, "citekey", yaml_scalar(refreshed))
        if new_text != text:
            text = new_text
            changed = True
        refreshed_fm = split_frontmatter(text)
        if "year" in refreshed_fm.keys and frontmatter_value(refreshed_fm.body, "year") == "2026":
            new_text = replace_simple_frontmatter_value(text, "year", yaml_scalar(year))
            if new_text != text:
                text = new_text
                changed = True

    for section in SOURCE_SECTIONS:
        if section not in text:
            text = text.rstrip() + f"\n\n{section}\n"
            changed = True

    if changed:
        write_text(path, text)
    return changed


def atomic_destination() -> Path:
    candidates = [
        VAULT / "wiki" / "research" / "topics",
        VAULT / "wiki" / "knowledge",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    destination = VAULT / "wiki" / "03_Atomic_Notes"
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def safe_note_name(name: str) -> str:
    name = re.sub(r"[\[\]#|:/\\：*?\"<>]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:90] or "Untitled Atomic Note"


def split_source_splittable_section(text: str) -> str:
    match = re.search(r"^## 可拆分知识点\s*$([\s\S]*?)(?=^## |\Z)", text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def normalize_atomic_section_name(heading: str) -> tuple[str, int] | None:
    cleaned = re.sub(r"[（(].*?[）)]", "", heading).strip().lower()
    cleaned = re.sub(r"[^a-z\u4e00-\u9fff]+", " ", cleaned).strip()
    first = cleaned.split()[0] if cleaned else ""
    return ATOMIC_SECTION_MAP.get(first)


def strip_inline_tags(raw: str) -> tuple[str, list[str]]:
    tags = re.findall(r"#([\w\-/\u4e00-\u9fff]+)", raw)
    title = re.sub(r"#([\w\-/\u4e00-\u9fff]+)", "", raw).strip()
    return title, tags


def atomic_title_from_bullet(raw: str) -> str:
    title, _ = strip_inline_tags(raw)
    title = re.sub(r"\[\[|\]\]", "", title).strip(" -")
    return safe_note_name(title)


def concept_name_from_bullet(raw: str) -> str:
    title = atomic_title_from_bullet(raw)
    if " - " in title:
        return title.split(" - ", 1)[0].strip()
    return title


def extract_explicit_atomic_items(path: Path, text: str) -> list[AtomicItem]:
    section = split_source_splittable_section(text)
    if not section:
        return []

    current: tuple[str, int] | None = None
    items: list[AtomicItem] = []
    sequence = 0
    for line in section.splitlines():
        heading = re.match(r"^\s*###\s+(.+?)\s*$", line)
        if heading:
            current = normalize_atomic_section_name(heading.group(1))
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if not bullet:
            continue
        if current is None:
            continue
        raw = bullet.group(1).strip()
        if not raw:
            continue
        category, priority = current
        title_without_tags, tags = strip_inline_tags(raw)
        sequence += 1
        items.append(
            AtomicItem(
                title=atomic_title_from_bullet(title_without_tags),
                detail=title_without_tags,
                category=category,
                tags=tags,
                priority=priority * 1000 + sequence,
            )
        )
    return sorted(items, key=lambda item: item.priority)


def extract_concepts_from_splittable_section(text: str) -> list[str]:
    return [
        concept_name_from_bullet(item.detail)
        for item in extract_explicit_atomic_items(Path(), text)
        if item.category == "concept"
    ]


def yaml_block_list_from_frontmatter(body: str, key: str) -> tuple[int, int, list[str]] | None:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        key_match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not key_match:
            continue
        values: list[str] = []
        inline = key_match.group(1).strip()
        if inline == "[]":
            return index, index + 1, values
        if inline.startswith("[") and inline.endswith("]"):
            values = [
                item.strip().strip('"').strip("'")
                for item in inline[1:-1].split(",")
                if item.strip()
            ]
            return index, index + 1, values
        if inline:
            return index, index + 1, [inline.strip().strip('"').strip("'")]
        end = index + 1
        while end < len(lines):
            next_line = lines[end]
            if re.match(r"^[A-Za-z0-9_\-\u4e00-\u9fff]+:\s*", next_line):
                break
            item = re.match(r"^\s*-\s*(.+?)\s*$", next_line)
            if item:
                values.append(item.group(1).strip().strip('"').strip("'"))
            end += 1
        return index, end, values
    return None


def merge_related_concepts(text: str, concepts: list[str]) -> str:
    concepts = [f"[[{concept}]]" if not concept.startswith("[[") else concept for concept in concepts]
    concepts = [concept for concept in concepts if concept.strip()]
    if not concepts:
        return text

    fm = split_frontmatter(text)
    if not fm.start:
        return text

    found = yaml_block_list_from_frontmatter(fm.body, "related_concepts")
    if found is None:
        addition = "related_concepts:" + yaml_list(concepts)
        body = fm.body.rstrip() + "\n" + addition
        return f"---\n{body.rstrip()}\n---\n{fm.rest}"

    start, end, existing = found
    normalized_existing = {value for value in existing}
    merged = existing[:]
    for concept in concepts:
        if concept not in normalized_existing:
            merged.append(concept)
            normalized_existing.add(concept)
    lines = fm.body.splitlines()
    replacement = [f"related_concepts:{yaml_list(merged)}"]
    new_body_lines = lines[:start] + replacement + lines[end:]
    return f"---\n{chr(10).join(new_body_lines).rstrip()}\n---\n{fm.rest}"


def citekey_for_source(text: str, source_title: str) -> str:
    citekey = frontmatter_value(split_frontmatter(text).body, "citekey")
    return citekey or safe_note_name(source_title)


def atomic_filename(citekey: str, item: AtomicItem) -> str:
    return safe_note_name(f"{citekey} - {item.category} - {item.title}") + ".md"


def atomic_tags(item: AtomicItem) -> list[str]:
    tags = ["atomic", item.category]
    for tag in item.tags:
        cleaned = tag.lstrip("#").strip()
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    return tags


def figure_mapping_frontmatter(item: AtomicItem) -> str:
    if item.category != "figure":
        return ""
    return """physics_mapping:
  TB: probability density
  FEM: field profile
  experiment: emission
"""


def figure_mapping_body(item: AtomicItem) -> str:
    if item.category != "figure":
        return ""
    fig_match = re.search(r"\b(Fig\.?\s*\d+[A-Za-z]?(?:\([A-Za-z0-9]+\))?)", item.detail, flags=re.I)
    fig_label = fig_match.group(1).replace(" ", "") if fig_match else item.title
    return f"""
## {fig_label} 三层映射

### {fig_label} - 能级层

- 能级 / 模式分裂：

### {fig_label} - TB 概率密度层

- TB → probability density：

### {fig_label} - 光场 / 实验层

- FEM → field profile：
- experiment → emission：
"""


def atomic_note_content(item: AtomicItem, source_title: str, citekey: str, source_path: Path) -> str:
    tag_lines = "\n".join(f"  - {yaml_scalar(tag)}" for tag in atomic_tags(item))
    return f"""---
title: {yaml_scalar(item.title)}
type: atomic
source: "[[{citekey}]]"
category: {yaml_scalar(item.category)}
tags:
{tag_lines}
source_note: "[[{source_title}]]"
source_path: {yaml_scalar(rel(source_path))}
created: {date.today().isoformat()}
{figure_mapping_frontmatter(item)}---

# {item.title}

## 核心内容

{item.detail}

## 详细解释

（允许后续扩展）

## 来源

[[{source_title}]]

## 可关联概念
{figure_mapping_body(item)}
"""


def create_atomic_notes() -> list[Path]:
    destination = atomic_destination()
    created: list[Path] = []
    for source in source_note_paths():
        text = read_text(source)
        source_title = infer_title(source, text, split_frontmatter(text))
        citekey = citekey_for_source(text, source_title)
        related_text = merge_related_concepts(text, extract_concepts_from_splittable_section(text))
        if related_text != text:
            write_text(source, related_text)
            text = related_text
        for item in extract_explicit_atomic_items(source, text):
            target = destination / atomic_filename(citekey, item)
            if target.exists():
                continue
            write_text(target, atomic_note_content(item, source_title, citekey, source))
            created.append(target)
    return created


def classify_dirs() -> dict[str, list[str]]:
    buckets = {"来源": [], "概念": [], "综述": [], "其他笔记": []}
    for directory in sorted(path for path in VAULT.rglob("*") if path.is_dir()):
        relative = rel(directory)
        lower = relative.lower()
        if any(hint in lower for hint in REVIEW_DIR_HINTS):
            buckets["综述"].append(relative)
        elif any(hint in lower for hint in SOURCE_DIR_HINTS):
            buckets["来源"].append(relative)
        elif any(hint in lower for hint in CONCEPT_DIR_HINTS):
            buckets["概念"].append(relative)
        else:
            buckets["其他笔记"].append(relative)
    return buckets


def write_structure_report(changed_sources: list[Path], created_atomic: list[Path]) -> Path:
    buckets = classify_dirs()
    report = WORKFLOWS / "Zotero_Structure_Report.md"
    lines = [
        "---",
        'title: "Zotero Structure Report"',
        "type: workflow",
        "status: active",
        f"updated: {date.today().isoformat()}",
        "tags:",
        "  - zotero",
        "  - obsidian",
        "  - workflow",
        "---",
        "",
        "# Zotero Structure Report",
        "",
        "## 自动识别结果",
        "",
    ]
    for bucket, paths in buckets.items():
        lines.append(f"### {bucket}")
        if paths:
            lines.extend(f"- `{path}`" for path in paths[:40])
        else:
            lines.append("- 未发现明确目录。")
        lines.append("")
    lines.extend(
        [
            "## 当前工作流落点",
            "",
            f"- 来源笔记：`{rel(RAW_PAPERS)}` 与 `{rel(WIKI_PAPERS / 'notes')}`",
            f"- 概念 / 原子笔记：`{rel(atomic_destination())}`",
            f"- 综述：`{rel(WIKI_PAPERS / 'reviews')}`，以及 `obsidian/outputs/summaries` 或 `obsidian/outputs/reports`",
            f"- 模板：`{rel(TEMPLATES)}`",
            f"- 工作流说明：`{rel(WORKFLOWS)}`",
            "",
            "## 本次脚本处理",
            "",
            f"- 补充来源笔记数量：{len(changed_sources)}",
            f"- 新建原子笔记数量：{len(created_atomic)}",
            "",
        ]
    )
    if changed_sources:
        lines.append("### 已追加字段或章节的来源笔记")
        lines.extend(f"- `{rel(path)}`" for path in changed_sources)
        lines.append("")
    if created_atomic:
        lines.append("### 已生成原子笔记")
        lines.extend(f"- `{rel(path)}`" for path in created_atomic)
        lines.append("")
    write_text(report, "\n".join(lines).rstrip() + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-atomic", action="store_true", help="create atomic notes from explicit bullets under ## 可拆分知识点")
    parser.add_argument("--dry-run", action="store_true", help="scan without writing changes")
    parser.add_argument("--refresh-citekeys", action="store_true", help="refresh provisional citekeys and inferred years")
    args = parser.parse_args()

    existing_citekeys: set[str] = set()
    changed_sources: list[Path] = []
    created_atomic: list[Path] = []

    if args.dry_run:
        print("Source notes:")
        for path in source_note_paths():
            print(f"- {rel(path)}")
        print(f"Atomic destination: {rel(atomic_destination())}")
        return

    for path in source_note_paths():
        if append_frontmatter_fields(path, existing_citekeys, refresh_citekeys=args.refresh_citekeys):
            changed_sources.append(path)

    if args.generate_atomic:
        created_atomic = create_atomic_notes()

    report = write_structure_report(changed_sources, created_atomic)
    print(f"Updated source notes: {len(changed_sources)}")
    print(f"Created atomic notes: {len(created_atomic)}")
    print(f"Wrote report: {rel(report)}")


if __name__ == "__main__":
    main()
