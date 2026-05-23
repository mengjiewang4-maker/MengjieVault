---
title: mph 文件里读到了什么
date: 2026-05-21
tags:
  - comsol
  - geometry
---

# mph 文件里读到了什么

## 文件检查结果

在目录 `20-Projects/02_Comsol_samulation` 中找到：

- `disclination_1.mph`
- 三张 COMSOL 截图
- 没有现成的 DXF/SVG/CSV/TXT 几何导出文件

本机没有检测到：

- `comsol` 命令
- COMSOL LiveLink
- `gdstk`
- `gdspy`

因此不能直接调用 COMSOL 官方接口导出 DXF。不过 `.mph` 可以作为 zip 容器读取，里面有 `dmodel.xml`。

## 读到的 COMSOL 参数

原始 `.mph` 里读到：

| 参数 | 表达式 | 数值 |
|---|---:|---:|
| `a` | `490[nm]` | 0.49 um |
| `R` | `18.0*a` | 8.82 um |
| `r` | `0.15*a` | 0.0735 um |
| `n_substrate` | `3.4` | 3.4 |

截图中后来又给了三组参数：

| 来源 | `a` | `r` | `R` | `n_substrate` |
|---|---:|---:|---:|---:|
| 图 1 | 554 nm | `0.2a` | `18a` | 3.33 |
| 图 2 | 559 nm | `0.2a` | `18a` | 3.4 |
| 图 3 | 555 nm | `0.15a` | `18a` | 3.4 |

脚本用 `--set-param` 覆盖这些参数，而不是改 `.mph` 原文件。

## 读到的几何特征

`dmodel.xml` 中读到：

- 1125 个 `Circle` 圆孔，名字形如 `circle_1` 到 `circle_1125`
- 1 个 `substrate1` 圆形参考边界
- 1 个 `PML1` 圆形参考边界
- 4 个 `Square` 分区参考边界
- `Difference` 和 `Partition` 几何操作
- `Finalize` 最终联合体

这说明 `.mph` 里确实保存了二维结构几何，不需要从截图反推。

## 脚本对应位置

- 参数解析：`scripts/comsol_mph_to_gds.py` 的 `parse_parameters`
- 参数覆盖：`scripts/comsol_mph_to_gds.py` 的 `apply_parameter_overrides`
- 几何解析：`scripts/comsol_mph_to_gds.py` 的 `parse_geometry`

> [!tip]
> 如果以后有 COMSOL 官方导出的 DXF，优先用 DXF。DXF 是二维工程图格式，比截图可靠得多。

