---
title: 20-Projects 目录说明
date: 2026-05-15
updated: 2026-05-28
tags:
  - 库结构
  - projects
  - index
---

# 20-Projects 目录说明

`20-Projects/` 只放正在推进、会产生代码、实验文件、加工文件或测试数据的项目。

当前主项目入口：[[20-Projects/00-首页|微腔加工与光学测试首页]]

## 快速入口

| 目录 | 内容 |
| --- | --- |
| [[20-Projects/01_Paper_read/]] | 论文阅读入口。 |
| [[20-Projects/02_Comsol_samulation/README|02_Comsol_samulation]] | COMSOL 仿真材料。COMSOL 是有限元仿真软件。 |
| [[20-Projects/03_GDS_layout/README|03_GDS_layout]] | GDS 版图、版图脚本和参数索引。 |
| [[20-Projects/04_weijiagong/README|04_weijiagong]] | 加工、样品、器件编号和 SEM 记录。 |
| [[20-Projects/05_Experiment_Log/]] | 每日实验日志。 |
| [[20-Projects/06_Optical_Test/]] | 光学测试计划、测试流程和模式判据。 |
| [[20-Projects/07_Result/]] | 数据分析入口。 |
| [[20-Projects/08-sample_database/]] | 样品数据库和样品追踪入口。 |
| [[20-Projects/09-papers_presentations/README|09-papers_presentations]] | 论文图、周报、组会和复现清单。 |
| [[20-Projects/00_Templates/]] | 可复制的记录模板。 |
| [[20-Projects/Skills/]] | Codex / Obsidian 工具技能，不属于科研主线。 |

## 当前主线

| 复现线 | 当前阶段 | 主要入口 |
| --- | --- | --- |
| Dirac-vortex topological cavities | Dirac cavity 已加工，等待光学测试 | [[06_Optical_Test/Dirac-vortex已加工样品光学测试入口|Dirac-vortex 光学测试入口]] |
| Vortex nanolaser based on a photonic disclination cavity | Disclination cavity 正在加工 | [[04_weijiagong/微腔加工样品记录 2026-05-14|MC-20260514-01 样品记录]] |

## 使用规则

- 论文笔记和精读：优先放 `01_Paper_read/`，长期文献综述可再迁到 `10-Research/`。
- 复现产生的代码、GDS、加工文件、测试计划：放当前项目对应目录。
- 原始 PDF 和大文件：放 `90-Local_Not_Upload/`，不上传 GitHub。
- 临时想法和未分类材料：先放 `00-Inbox/`，确认有用后再移入正式目录。

## 术语说明

- GDS：芯片和微纳加工常用的版图文件格式。
- 光学测试：对加工好的样品测光谱、远场、偏振、干涉等，用来判断腔模是否符合预期。
