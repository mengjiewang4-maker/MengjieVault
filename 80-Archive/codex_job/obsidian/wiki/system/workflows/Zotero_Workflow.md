---
title: Zotero Workflow
type: workflow
status: active
tags:
  - zotero
  - obsidian
  - workflow
---

# Zotero Workflow

## 目标

在现有 `obsidian/raw/`、`obsidian/wiki/`、`obsidian/outputs/` 结构上叠加 Zotero 知识流，不重构、不移动、不覆盖已有笔记。

## 目录映射

- 原始 PDF、网页剪藏、导入材料先放入 `obsidian/raw/`，论文优先放入 `obsidian/raw/papers/`。
- 清理后的来源笔记放在 `obsidian/raw/papers/` 或 `obsidian/wiki/papers/notes/`。
- 原子笔记与概念页优先放入现有主题/知识目录：`obsidian/wiki/research/topics/` 或 `obsidian/wiki/knowledge/`。
- 综述与阶段性整合放入 `obsidian/wiki/papers/reviews/`，最终报告放入 `obsidian/outputs/`。
- 模板放入 `obsidian/wiki/system/templates/`。

## 导入一篇论文

1. 在 Zotero 中保存论文条目与 PDF。
2. 用 Better BibTeX 固定 citekey，避免后续重命名导致链接失效。
3. 在 Obsidian 中用 Zotero Integration 选择 `Literature Note Template` 导入元数据与 PDF 标注。
4. 如果是原始材料，先保存到 `obsidian/raw/papers/`；如果已经进入精读，可在 `obsidian/wiki/papers/notes/` 建立整理版来源笔记。
5. 检查 frontmatter 至少包含 `citekey`、`title`、`authors`、`year`、`journal`、`doi`、`zotero`、`tags`、`status`、`related_concepts`。

## 生成来源笔记

- 新文献用 `Literature Note Template`。
- 旧来源笔记可运行维护脚本补齐缺失字段和标准章节：

```bash
python code/zotero_obsidian_workflow/zotero_obsidian_setup.py
```

脚本只追加缺失 frontmatter 字段和缺失章节，不覆盖已有正文。

## 拆原子笔记

在来源笔记的 `## 可拆分知识点` 下写固定分区。生成器只读取这些 `###` 小节，保证输出稳定：

```markdown
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

然后运行：

```bash
python code/zotero_obsidian_workflow/zotero_obsidian_setup.py --generate-atomic
```

脚本会把每个条目生成独立原子笔记，并带上 `source: citekey`、来源笔记反链、`category`、标签与 `source_path`。生成优先级为 `Insights`、`Concepts`、`Models`、`Figures`、`Methods`。

分区到原子笔记类型的映射：

- `Concepts` → `category: concept`，定义型原子笔记。
- `Models` → `category: model`，方法型原子笔记。
- `Figures` → `category: figure`，图解型原子笔记，并自动加入 `physics_mapping` 与“能级 / TB 概率密度 / 光场实验”三层结构。
- `Methods` → `category: method`，流程型原子笔记。
- `Insights` → `category: insight`，洞察型原子笔记，最高优先级。

运行生成时，脚本还会把 `### Concepts` 里的条目回填到来源笔记 frontmatter 的 `related_concepts`，只追加缺失项。

## 链接概念

- 原子笔记只写一个知识点，并在 `related_concepts` 或正文里链接概念页。
- 如果概念页已存在，直接链接它。
- 如果概念页不存在，用 `Concept Note Template` 新建。
- 概念页内的 Dataview 会自动汇总引用它的原子笔记与来源论文。

## 汇总成综述

1. 为一个研究问题新建综述页，使用 `Review Note Template`。
2. 在 `topic_tags` 中列出主题标签，如 `topological-photonics`、`TB`、`vortex-light`。
3. 用 Dataview 汇总主题论文。
4. 从相关概念页回看原子笔记，抽取共识、分歧、路线比较与未解问题。
5. 成熟后把最终表达写入 `obsidian/outputs/summaries/`、`obsidian/outputs/reports/` 或 `obsidian/outputs/slides/`。

## 日常状态

- `unread`：已导入但未读。
- `reading`：正在精读、摘图、拆知识点。
- `done`：已完成来源笔记、关键原子笔记和概念链接。

已有笔记如果使用了 `draft`、`reviewed`、`active` 等旧状态，可以暂时保留；新 Zotero 文献建议使用上面的三种状态。
