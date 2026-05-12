---
title: Review Note Template
type: system
status: active
tags:
  - template
  - zotero
  - review
---

# Review Note Template

````markdown
---
title: 综述主题
type: review
status: draft
tags:
  - review
topic_tags: []
related_concepts: []
---

# 综述主题

## 综述问题

## 主题论文

```dataview
TABLE year, journal, status, file.link AS Note
FROM "obsidian/raw/papers" OR "obsidian/wiki/papers"
WHERE type = "source" AND any(topic_tags, (t) => contains(tags, t))
SORT year DESC
```

## 核心概念

## 路线比较

## 共识结论

## 分歧与未解问题

## 可写入最终输出的段落
````
