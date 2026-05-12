---
title: Atomic Note Template
type: system
status: active
tags:
  - template
  - zotero
  - atomic
---

# Atomic Note Template

```markdown
---
title: 原子笔记标题
type: atomic
source: "citekey"
category: concept
tags:
  - atomic
  - concept
source_note: "来源笔记标题"
source_path: obsidian/raw/papers/example.md
---

# 原子笔记标题

## 核心内容

一句话解释

## 详细解释

（允许后续扩展）

## 来源

来源笔记标题

## 可关联概念

```

Figure 类型会额外生成：

```yaml
physics_mapping:
  TB: probability density
  FEM: field profile
  experiment: emission
```
