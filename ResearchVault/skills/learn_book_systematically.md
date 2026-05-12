name: learn_book_systematically
description: 系统化学习一本教材或专业书籍（适用于量子力学/科研书籍）

## Goal
将一本书从“阅读”转化为：
- 概念网络
- 可计算模型
- 可复用知识

## Steps

### 1. 结构拆解（Book Mapping）
- 列出章节结构
- 提取核心主题（3–5个）
- 建立总入口（MOC）

输出：
obsidian/wiki/book_name_map.md

---

### 2. 概念提取（Concept Extraction）
- 每章提取：
  - 核心概念
  - 关键公式
  - 物理意义

规则：
一个概念 = 一个原子笔记

输出：
obsidian/concepts/

---

### 3. 模型识别（Model Identification）
- 找出：
  - 可计算模型（势阱、谐振子）
  - 本征问题
  - 边界条件

输出：
code/models/

---

### 4. 可视化（Visualization）
- 用 Python 实现：
  - 波函数
  - 能级结构
  - 参数变化

输出：
results/plots/

---

### 5. Skill沉淀（Skill Extraction）
- 将解题过程写成：
  - 通用步骤
  - 可复用流程

输出：
skills/

---

### 6. 知识连接（Linking）
- 建立：
  - concept ↔ model
  - model ↔ code
  - code ↔ figure

---

## Output
一本书 → 一个“知识系统”