---
name: zotero-obsidian-topology-notes
description: Turn a paper excerpt plus a Zotero citation key into an Obsidian atomic note for topological photonics or related physics topics. Use when the user provides text with @citekey, wants Zotero-to-Obsidian knowledge linking, asks to save a note into the vault, or needs physics descriptions mapped into formulas and Python/NumPy matrix logic.
---

# Zotero Obsidian Topology Notes

<!-- 中文注释：这个 skill 面向“Zotero 文献片段 -> Obsidian 原子笔记”的工作流，尤其适合拓扑光子学和相关物理主题。 -->

Use this skill when the user is building an Obsidian knowledge base from literature snippets and wants the note anchored to a Zotero citation key.

## What This Skill Produces

<!-- 中文注释：输出目标不是普通摘要，而是带 Zotero 溯源、概念链接、中文解释、公式和代码映射的原子知识卡。 -->

Given:

- a paper excerpt
- an `@citekey`

produce an Obsidian atomic note block with:

- `source: @citekey`
- `zotero: zotero://select/items/@citekey`
- a concise concept title
- wikilinks such as `[[二维SSH模型]]`
- a plain Chinese explanation
- core formulas when the text implies a model
- Python/NumPy mapping from the physics description to matrix operations

## Input Handling

<!-- 中文注释：输入解析时首先锁定论文片段和 `@citekey`，后续 source 与 Zotero 跳转都围绕这个引用键展开。 -->

1. Extract the paper snippet and the citation key.
2. Treat the provided `@citekey` as the source anchor even if it is verbose.
3. Generate the Zotero jump link as:

```text
zotero://select/items/@citekey
```

4. Infer 1 to 5 atomic concepts from the snippet and express them as `[[概念名]]`.

## Output Format

<!-- 中文注释：默认输出结构已经符合本 vault 的原子笔记格式；保存前只需要替换标题、日期、citekey 和相关概念。 -->

Use this structure by default:

````markdown
---
title: 概念标题
type: concept
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - wiki
  - concept
  - optics
source: "@Citekey"
zotero: "zotero://select/items/@Citekey"
concepts:
  - "[[概念标题]]"
related:
  - "[[相关概念]]"
---

# [[概念标题]]

## Source

@Citekey
[zotero://select/items/@Citekey](zotero://select/items/@Citekey)

## 白话解释

用中文把原文物理含义讲清楚，优先说明系统、自由度、机制和结论。

## 核心公式

如果原文可抽象为哈密顿量、本征方程、耦合矩阵、边界条件或守恒量，就给出最小必要公式。

## 代码映射

```python
import numpy as np
```

把物理对象逐项映射到数组、矩阵、特征值问题、参数扫描或场分布计算。

## 原子关联

- [[相关概念A]]
- [[相关概念B]]
````

## Physics Mapping Rules

<!-- 中文注释：物理内容按“图像 -> 数学 -> 代码”的顺序写，避免直接跳到公式导致笔记难以复用。 -->

- 先写物理图像，再写数学表达，再写代码。
- 遇到 tight-binding、effective Hamiltonian、coupled-mode、Bloch model 时，优先映射为矩阵或本征值问题。
- 遇到界面态、边界态、角态、缺陷态时，明确指出判据：
  - 能量或频率是否在带隙中
  - 模式是否局域
- 遇到拓扑相变时，优先点出控制参数，例如胞内/胞间耦合、质量项、对称性破缺项。
- 代码默认使用 `numpy`；只有在确有必要时再引入 `scipy`.

## Saving Rules

<!-- 中文注释：只有用户要求保存时才写入 vault；保存后应维护来源笔记和少量高价值概念链接。 -->

If the user asks to save the note:

1. Prefer saving concept-like atomic cards under `概念/`.
2. Use the concept title as the filename, for example:

```text
概念/HOTI界面态的紧束缚求解.md
```

3. Keep frontmatter aligned with the existing vault style:
   - `title`
   - `type: concept`
   - `status: draft`
   - `created`
   - `updated`
   - `tags`
   - `source`
   - `zotero`
   - `concepts`
   - optional `related`
4. If a matching paper source note already exists under `来源/`, add the new note to its `related` list.
5. If a nearby parent concept exists, add a short explicit link there so the new note is not isolated.

## Vault Conventions For This Workspace

<!-- 中文注释：本工作区已有自己的目录习惯，新增笔记应沿用 `概念/` 与 `来源/` 的结构，避免另建平行体系。 -->

- Atomic concept cards are usually stored in `概念/`.
- Literature/source notes are stored in `来源/`.
- Existing notes may already use links such as `[[概念/某概念]]` in frontmatter `related`.
- Preserve existing user edits. Never rewrite unrelated metadata or remove existing links.

## Writing Guidance

<!-- 中文注释：解释优先使用中文，保留标准英文术语；不要凭空补 DOI、期刊、作者等未提供的文献信息。 -->

- Keep the explanation concrete and non-generic.
- Use Chinese for explanation and section text unless the user asks otherwise.
- Preserve English model names when they are standard, such as `HOTI`, `SSH`, `tight-binding`.
- Do not invent bibliographic metadata that was not provided.
- If the text is too sparse for a formula, say so and provide only the physically justified minimal model.

## Typical Flow

<!-- 中文注释：标准流程是先产出原子卡，再按需保存、补来源反链和父概念链接。 -->

1. Parse `论文片段 + @citekey`.
2. Generate the atomic note block.
3. If requested, save it as a `.md` note in the vault.
4. Update `来源/` backlinks.
5. Add one or two high-value semantic links from nearby concept notes when appropriate.

## Note Type Routing

<!-- 中文注释：先判断笔记类型再写内容；概念、方法和来源摘要的保存路径与 frontmatter 不完全相同。 -->

Choose the note type before writing:

1. `概念卡`
   Use when the snippet explains a physical idea, mechanism, criterion, or abstraction.
   Default save path:

```text
概念/概念标题.md
```

2. `方法卡`
   Use when the snippet mainly describes a calculational method, modeling workflow, simulation approach, or derivation strategy.
   Default save path:

```text
概念/方法标题.md
```

   In this workspace, method cards can still live under `概念/` if there is no dedicated `方法/` directory.

3. `来源摘要卡`
   Use when the user wants to summarize the paper itself rather than isolate one atomic concept.
   Default save path:

```text
来源/论文名-年份-论文名.md
```

Route by dominant intent:

- if the center is "这是什么/为什么成立", prefer `概念卡`
- if the center is "怎么算/怎么建模", prefer `方法卡`
- if the center is "这篇论文讲了什么", prefer `来源摘要卡`

## Frontmatter Standards

<!-- 中文注释：frontmatter 保持小而稳定，只写检索和溯源真正需要的字段。 -->

Use the smallest valid frontmatter that still matches the workspace.

For `概念卡` and `方法卡`, prefer:

```yaml
---
title: 标题
type: concept
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - English title if useful
tags:
  - wiki
  - concept
  - optics
source: "@Citekey"
zotero: "zotero://select/items/@Citekey"
concepts:
  - "[[标题]]"
related:
  - "[[概念/相关页]]"
---
```

For `来源摘要卡`, prefer:

```yaml
---
title: 论文标题
year: 2025
type: source
status: to-read
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: 学习资料/论文/待整理/文件名.pdf
tags:
  - literature
  - source
  - paper
related:
  - "[[概念/相关概念]]"
---
```

Rules:

- Always include `title`, `type`, `status`, `created`, `updated`.
- Only add `aliases` when they improve retrieval.
- Only add `year` for source notes.
- Do not fabricate DOI, journal, authors, or year.
- Keep `source` as the Zotero cite anchor for atomic cards, and as the local file path for source-summary cards when that path is known.

## Recommended Tag Sets

<!-- 中文注释：标签要少而准；只有片段明确支持某主题时才添加专题标签。 -->

Use a small stable tag set. Do not over-tag.

Base tags for atomic cards:

- `wiki`
- `concept`
- `optics`

Add topic tags only when they are directly supported by the snippet:

- `topological-photonics`
- `hoti`
- `2d-ssh`
- `tight-binding`
- `nanolaser`
- `vortex-light`
- `photonic-crystal`
- `dirac-vortex`
- `interface-state`
- `corner-state`

Base tags for source notes:

- `literature`
- `source`
- `paper`

## Title Generation Rules

<!-- 中文注释：标题要可搜索、概念化，优先中文表达，保留 SSH、HOTI、TB 等标准缩写。 -->

- Titles should be short, searchable, and concept-centered.
- Prefer Chinese titles for saved notes in this workspace.
- Keep standard model acronyms in English, such as `SSH`, `HOTI`, `TB`.
- Avoid generic titles like `论文笔记1`, `模型分析`, `方法总结`.
- If the snippet is about a criterion or operation, encode that in the title:
  - `HOTI界面态的紧束缚求解`
  - `二维SSH模型中的胞内胞间耦合判据`
  - `位错腔中的涡旋模式局域条件`

## Link Maintenance Rules

<!-- 中文注释：链接维护要克制，只补来源反链和一个强相关父概念，避免大范围改动 vault。 -->

- When saving a new atomic card, search for an existing source note under `来源/` that matches the citekey or paper title.
- Add the new note to that source note's `related` field if not already present.
- Search for one nearby parent concept and add a concise link there when the semantic relationship is strong.
- Do not mass-edit the vault to create backlinks everywhere; prefer one source backlink and one parent-concept backlink.

## Code Mapping Heuristics

<!-- 中文注释：代码映射以 NumPy 思路为主，把物理概念落到矩阵、本征值、场强或相位绕转等可计算对象。 -->

- `tight-binding` -> Hamiltonian matrix assembly + eigendecomposition
- `coupled-mode` -> low-dimensional non-Hermitian or Hermitian coupling matrix
- `band structure` -> parameter sweep over momentum or geometry
- `localized state` -> inspect eigenvector amplitude or field intensity
- `phase winding / vortex` -> compute phase with `np.angle` and winding around a loop
- `symmetry protection` -> state explicitly which matrix term preserves or breaks the symmetry

## Response Modes

<!-- 中文注释：根据用户意图选择响应模式：只要内容就返回块，要求保存才写文件，要求知识链才补链接。 -->

Match the response to the request:

1. If the user asks only for output, return the Obsidian block.
2. If the user asks to save, write the note and then report the saved path.
3. If the user asks to update the knowledge chain, also patch `来源/` and one nearby concept note.
