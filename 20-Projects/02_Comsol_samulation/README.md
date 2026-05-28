---
title: COMSOL disclination GDS 项目整理
date: 2026-05-25
tags:
  - project
  - comsol
  - gds
---

# COMSOL disclination GDS 项目整理

这个文件夹用于把 COMSOL 的 disclination 结构转换成 GDS 版图文件。

## 目录说明

| 目录/文件 | 用途 |
| --- | --- |
| `origin/` | 原始输入文件，包括 COMSOL `.mph`、DXF 和参考图片。 |
| `scripts_20260521_1/` | 当前保留的可用 Python 脚本。 |
| `output_20260521_1/` | 已生成的 GDS、预览 PNG、参数 JSON 和说明文档。 |
| `requirements.txt` | 运行脚本需要安装的 Python 包。 |
| `.python_deps/` | 本地安装的 Python 依赖缓存；可重新安装，不建议当作项目成果看。 |
| `export_from_comsol_instructions.md` | 从 COMSOL 导出文件的操作说明。 |

## 推荐使用文件

优先看这个总记录：

- `output_20260521_1/GDS_generation_records.md`

如果要找 100 um 版本，对应文件是：

- `output_20260521_1/disclination_a554_r0p2_n3p33_extended_100um.gds`
- `output_20260521_1/disclination_a554_r0p2_n3p33_extended_100um_preview.png`
- `output_20260521_1/README_disclination_a554_r0p2_n3p33_extended_100um.md`

## 重新生成 100 um 版本

在本项目目录执行：

```bash
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a554_r0p2_n3p33_extended_100um --set-param 'a=554[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.33' --extend-pattern-diameter-um 100
```

说明：

- `GDS`：微纳加工常用的版图文件格式。
- `PNG preview`：预览图，方便肉眼检查版图形状。
- `JSON`：参数记录文件，方便之后追溯生成条件。
- `output-prefix`：输出文件名前缀。

## 当前整理状态

- 原始输入集中在 `origin/`。
- 可用脚本集中在 `scripts_20260521_1/`。
- 成品输出集中在 `output_20260521_1/`。
- 已忽略 `.DS_Store`、`__pycache__`、`.python_deps/` 这类缓存文件。
