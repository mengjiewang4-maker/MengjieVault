---
title: Atomic Dedupe Dataview
type: workflow
status: active
tags:
  - atomic
  - dedupe
  - dataview
---

# Atomic Dedupe Dataview

## 逻辑唯一原子笔记

```dataviewjs
const pages = dv.pages()
  .where(p => p.type === "atomic" && p.canonical_id)
  .array();

const byCanonical = new Map();
for (const page of pages) {
  const id = String(page.canonical_id);
  if (!byCanonical.has(id)) byCanonical.set(id, []);
  byCanonical.get(id).push(page);
}

const rows = [];
for (const [id, group] of byCanonical.entries()) {
  group.sort((a, b) => a.file.path.localeCompare(b.file.path));
  const primary = group[0];
  rows.push([
    primary.file.link,
    primary.category ?? "",
    id,
    group.length,
    group.slice(1).map(p => p.file.link)
  ]);
}

rows.sort((a, b) => String(a[2]).localeCompare(String(b[2])));
dv.table(["主笔记", "类别", "canonical_id", "重复数", "重复笔记"], rows);
```

## 仅显示无重复主笔记

```dataviewjs
const pages = dv.pages()
  .where(p => p.type === "atomic" && p.canonical_id)
  .array();

const seen = new Set();
const rows = [];
for (const page of pages.sort((a, b) => a.file.path.localeCompare(b.file.path))) {
  const id = String(page.canonical_id);
  if (seen.has(id)) continue;
  seen.add(id);
  rows.push([page.file.link, page.category ?? "", id]);
}

dv.table(["原子笔记", "类别", "canonical_id"], rows);
```
