---
title: COMSOL 到 GDS 画图研究
date: 2026-05-21
tags:
  - comsol
  - gds
  - nanofabrication
  - photonic-crystal
aliases:
  - mph到gds画图研究
---

# COMSOL 到 GDS 画图研究

这个文件夹记录这次从 COMSOL `.mph` 仿真文件生成 GDS 版图的完整过程。

> [!important] 核心结论
> 我们没有把仿真截图直接描边成版图。截图只适合看模式场和人工核对外观，不适合加工。真正用于 GDS 的几何来自 `.mph` 内部 `dmodel.xml` 里的圆孔中心、半径、边界等参数。

## 阅读顺序

1. [[01_总流程图|总流程图]]
2. [[02_mph文件里读到了什么|mph 文件里读到了什么]]
3. [[03_如何从参数画出孔阵列|如何从参数画出孔阵列]]
4. [[04_GDS文件是怎样写出来的|GDS 文件是怎样写出来的]]
5. [[05_尺寸扩展和版本记录|尺寸扩展和版本记录]]
6. [[06_术语表|术语表]]

## 关键输出位置

- 项目目录：`20-Projects/02_Comsol_samulation`
- 脚本目录：`20-Projects/02_Comsol_samulation/scripts`
- GDS 输出目录：`20-Projects/02_Comsol_samulation/output`
- 总生成记录：[[20-Projects/02_Comsol_samulation/output/GDS_generation_records.md|GDS_generation_records]]

## 最重要的脚本

- `scripts/comsol_mph_to_gds.py`：从 `.mph` 里提取参数并生成 GDS。
- `scripts/gds_utils.py`：画圆孔 polygon、写 GDS、生成 PNG 预览、做基本检查。
- `scripts/convert_dxf_to_gds.py`：备用流程，用于以后从 COMSOL 手动导出 DXF/SVG/CSV 后再转 GDS。

## 当前主要版图

| 版本 | 参数 | 实际外包络直径 | 文件 |
|---|---|---:|---|
| 20 um 扩展版 | `a=554 nm, r=0.2a, R=18a` | 19.1475 um | `disclination_a554_r0p2_n3p33_extended_20um.gds` |
| 50 um 扩展版 | `a=554 nm, r=0.2a, R=18a` | 49.8382 um | `disclination_a554_r0p2_n3p33_extended_50um.gds` |
| 图 1 参数 100 um | `a=554 nm, r=0.2a, R=18a` | 99.2842 um | `disclination_a554_r0p2_n3p33_extended_100um.gds` |
| 图 2 参数 100 um | `a=559 nm, r=0.2a, R=18a` | 100.1803 um | `disclination_a559_r0p2_n3p4_extended_100um.gds` |
| 图 3 参数 100 um | `a=555 nm, r=0.15a, R=18a` | 99.4079 um | `disclination_a555_r0p15_n3p4_extended_100um.gds` |

## 预览图

50 um 扩展版：

![[20-Projects/02_Comsol_samulation/output/disclination_a554_r0p2_n3p33_extended_50um_preview.png|500]]

100 um 图 1 参数扩展版：

![[20-Projects/02_Comsol_samulation/output/disclination_a554_r0p2_n3p33_extended_100um_preview.png|500]]

