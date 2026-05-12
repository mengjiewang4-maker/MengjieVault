---
title: Literature Note Template
type: system
status: active
tags:
  - template
  - zotero
  - literature
---

# Literature Note Template

```markdown
---
citekey: "{{citekey}}"
title: "{{title}}"
authors:
  - "{{authorString}}"
year: {{year}}
journal: "{{publicationTitle}}"
doi: "{{DOI}}"
zotero: "{{zoteroSelectURI}}"
tags:
  - literature
  - source
  - paper
status: unread
related_concepts: []
---

# {{title}}

## 基本信息

- Zotero：{{zoteroSelectURI}}
- PDF：{{pdfZoteroLink}}
- DOI：{{DOI}}
- 期刊 / 会议：{{publicationTitle}}
- 年份：{{year}}

## 核心问题

## 方法与模型

## 关键结论

## 图表解释

## Zotero Notes

{{note}}

## 可拆分知识点

<!--
按固定分区写可自动拆分的条目，然后运行：
python code/zotero_obsidian_workflow/zotero_obsidian_setup.py --generate-atomic
-->

### Concepts

- HOTI 高阶拓扑绝缘体
- Disclination 旋错
- Angular momentum 角动量

### Models

- Tight-binding model 用于旋错态能级计算
- Disclination 的角度缺陷映射（C6 → C5/C7）

### Figures

- Fig2(a): 能级图，显示 l=0,1,2 模式分裂
- Fig2(b): TB 概率密度分布，对应不同角动量
- Fig2(c): 光学场分布，对应实验验证

### Methods

- 将 TB 模型与 FEM 仿真进行对应
- 利用对称性分类模式

### Insights

- 角动量来自“角点之间的相位差”
- TB → 光学模式之间存在一一映射关系
```
