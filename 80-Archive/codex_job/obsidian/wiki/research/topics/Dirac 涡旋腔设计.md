---
title: Dirac 涡旋腔设计
type: concept
status: draft
created: 2026-04-18
updated: 2026-04-20
aliases:
  - Dirac-vortex cavity design
tags:
  - wiki
  - concept
  - optics
  - topological-photonics
  - design-method
sources:
  - mengjie-viki-new/obsidian/wiki/Methods/Dirac-vortex cavity design.md
---

# Dirac 涡旋腔设计

## 一句话定义

Dirac 涡旋腔设计，是从蜂窝晶格的 Dirac physics 与 Kekule modulation 出发，通过构造空间涡旋质量项，在 vortex core 处形成局域 mid-gap 模的拓扑光子腔设计路线。

## 直观理解

这条路线不是先做一个普通腔再去调模式形状，而是先在能带层面设计“带有涡旋结构的质量项”，再让局域模式自然出现在拓扑缺陷核心位置。

## 形式化描述

- 设计通常从具有 Dirac 点的晶格出发
- 通过广义 Kekule modulation 打开 Dirac gap
- 让质量项的相位在空间中形成 vortex
- 在 vortex core 处得到局域的 topological mid-gap mode
- 最后将这一模式翻译到可制造的 photonic crystal slab / membrane 结构

## 这条路线擅长什么

- 构造大面积但仍保持单模倾向的腔
- 引入可控简并度与矢量光束输出
- 为表面发射器或 PCSEL 类器件提供拓扑化设计语言
- 在你的目标里，更像负责“模式扩展、表面发射语言和更高功率可扩展性”

## 与其他概念的关系

- 上位概念：[[拓扑光子微腔]]
- 对照路线：[[光子位错腔设计]]
- 比较页：[[拓扑涡旋腔路线比较]]
- 指标框架：[[高性能涡旋光指标框架]]
- 相关问题：[[表面发射与大面积单模]]
- 目标总览：[[高性能涡旋光目标总览]]
- 英文对应：[[Dirac 涡旋腔设计|Dirac-vortex cavity design]]
- 相关论文：[[Dirac-vortex topological cavities]]

## 当前理解边界

- 当前页面主要保留方法主线，不记录未在原始摘录中确认的参数扫描细节
- 若后续继续整理 PCSEL、拓扑表面发射或大面积单模路线，这页适合作为中文方法入口

## 📄 相关来源

```dataview
TABLE file.link AS 文献, year AS 年份, tags AS 标签
FROM "来源"
WHERE contains(related, this.file.link)
SORT year DESC
```
