---
title: 80-Archive 入口
date: 2026-05-28
updated: 2026-05-28
tags:
  - 库结构
  - archive
  - index
---

# 80-Archive 入口

`80-Archive/` 是归档区，用来保存旧库、迁移残留、历史项目和不再作为主线推进的资料。

这里默认只读：可以查、可以引用，但不要把新的研究主线继续写在这里。

## 当前结构

| 目录 | 用途 |
| --- | --- |
| [[80-Archive/ResearchVault/]] | 旧 ResearchVault 学习库，主要是量子力学学习、OCR、脚本和历史输出。 |
| [[80-Archive/codex_job/]] | 旧 Codex 工作目录，包含历史代码、结果和 Obsidian 资料。 |
| [[80-Archive/onenote/]] | OneNote 迁移遗留资料和转换脚本。 |

## 使用规则

- 需要查旧资料时，从这里搜索。
- 如果某个旧内容重新变成主线，复制或迁移到 `10-Research/` 或 `20-Projects/`。
- 不要在这里新建长期项目。
- 不要把大文件继续堆在这里；大文件应放入 `90-Local_Not_Upload/`。

## 迁移判断

| 情况 | 处理 |
| --- | --- |
| 只是历史记录 | 留在 `80-Archive/`。 |
| 仍会被引用的理论笔记 | 移到 `10-Research/`，并保留来源链接。 |
| 有代码、脚本、实验流程 | 移到 `20-Projects/`。 |
| 是 PDF、图片、模型、大型输出 | 移到 `90-Local_Not_Upload/`。 |
| 已经重复或无价值 | 删除前先确认是否已有备份。 |

## 当前提醒

- `80-Archive/ResearchVault/` 里有较多旧 Obsidian 和量子力学资料。
- `80-Archive/codex_job/` 里可能包含历史代码和运行结果。
- `80-Archive/onenote/` 主要用于追溯 OneNote 迁移过程。
