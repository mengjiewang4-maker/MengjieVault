---
title: Zotero Dataview Panels
type: workflow
status: active
tags:
  - zotero
  - dataview
  - obsidian
---

# Zotero Dataview Panels

## 未读论文

```dataview
TABLE title, authors, year, journal, doi, file.link AS Note
FROM "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE type = "source" AND (status = "unread" OR !status)
SORT year DESC, file.mtime DESC
```

## 正在精读论文

```dataview
TABLE title, authors, year, journal, related_concepts, file.link AS Note
FROM "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE type = "source" AND status = "reading"
SORT file.mtime DESC
```

## 某主题论文（按 tag）

把 `topology` 换成目标标签，例如 `TB`、`disclination`、`vortex-light`。

```dataview
TABLE title, authors, year, journal, status, file.link AS Note
FROM "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE type = "source" AND contains(tags, "topology")
SORT year DESC
```

## 某概念关联所有笔记

这段适合放进任意概念页，自动读取当前概念页 `this.file.link`。

```dataview
TABLE type, status, source, file.link AS Note
FROM "obsidian/wiki/research/topics" OR "obsidian/wiki/knowledge" OR "obsidian/wiki/03_Atomic_Notes" OR "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE contains(file.outlinks, this.file.link) OR contains(related_concepts, this.file.link)
SORT type ASC, file.mtime DESC
```

## 来源论文到原子笔记

在来源笔记中使用，查看从当前论文拆出的知识点。

```dataview
TABLE category, source, file.link AS AtomicNote
FROM "obsidian/wiki/research/topics" OR "obsidian/wiki/knowledge" OR "obsidian/wiki/03_Atomic_Notes"
WHERE type = "atomic" AND (source_note = this.file.link OR contains(file.outlinks, this.file.link))
SORT file.ctime ASC
```
