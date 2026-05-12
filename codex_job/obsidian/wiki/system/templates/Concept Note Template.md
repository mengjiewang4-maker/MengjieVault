---
title: Concept Note Template
type: system
status: active
tags:
  - template
  - zotero
  - concept
---

# Concept Note Template

````markdown
---
title: 概念名称
type: concept
status: active
tags:
  - concept
aliases: []
---

# 概念名称

## 一句话定义

## 直观理解

## 形式化描述

## 相关原子笔记

```dataview
LIST FROM "obsidian/wiki/research/topics" OR "obsidian/wiki/knowledge" OR "obsidian/wiki/03_Atomic_Notes"
WHERE type = "atomic" AND (contains(file.outlinks, this.file.link) OR contains(related_concepts, this.file.link))
SORT file.mtime DESC
```

## 相关来源论文

```dataview
TABLE year, journal, status, file.link AS Note
FROM "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE type = "source" AND (contains(file.outlinks, this.file.link) OR contains(related_concepts, this.file.link))
SORT year DESC
```

## 与其他概念的关系

## 当前理解边界
````
