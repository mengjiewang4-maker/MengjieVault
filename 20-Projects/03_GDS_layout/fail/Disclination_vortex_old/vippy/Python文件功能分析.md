---
title: Python 文件功能分析
date: 2026-05-19
tags:
  - GDS
  - Python
  - vippy
---

# Python文件功能分析

| py文件 | 原路径 | 用途 | 输出GDS | 输出路径 | 关键参数 | 使用库 | 是否可运行 | 与主版本关系 | 建议分类 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `disclination_vortex_gds_current.py` | `disclination_vortex_gds.py` | 生成四角晶格切开并添加 1/4 扇区后的 disclination vortex 空气孔 GDS | `mjYYYYMMDD_01.gds` 到 `mjYYYYMMDD_06.gds`；20260517 已存在 6 个 | `脚本所在目录/YYYYMMDD`；整理后直接运行会变为 `current/YYYYMMDD` | PARAM_SETS=[a=0.554,r/a=0.20; a=0.559,r/a=0.20; a=0.559,r/a=0.15]；R=60；R_half=30；n_vertex=256；4+1 扇区；angle_ratio=0.8；radius_ratio=0.8 | `klayout.db`、`numpy`、`pathlib`、`datetime` | 理论可运行；依赖 KLayout Python API；未在本次整理中重新运行，避免生成新 GDS | 当前主版本；已生成 20260517 最新 6 个 GDS | current |
| `generate_batch13_disclination_dose_matrix_v01.py` | 新增于 `current/` | batch13 专用生成脚本；保持 6 个结构几何不变，按 6 个 Dose/PEC 组合生成带 mark 的 GDS 和区域对应表 | 预计生成 36 个 GDS：6 个结构 x 6 个 Dose；文件名形如 `batch13_YYYYMMDD_D3_dose30_pec_on_GDS01_a0p554_r0p111.gds` | `outputs/gds/batch13_Si_EBL/YYYYMMDD/`；对应表输出到 `outputs/mapping/` | 沿用 current 几何参数；新增 DOSE_MATRIX=20%、25%、30%、35%、40%、45%，PEC=on；mark 形如 `d30-01` | `klayout.db`、`numpy`、`pathlib`、`datetime` | 已通过 `py_compile` 语法检查；当前终端环境缺少 `klayout` 模块，尚未实际运行生成 GDS | 从 current 派生的 batch13 候选版本；几何不变，只增加 Dose/PEC 映射和 mark | current |
| `generate_dirac_vortex_wm1_R100_template_v01.py` | `gds_template_1.py` | 生成 Dirac/vortex 三角孔阵列 GDS 模板，并写入 `w` 标识 | `wmjYYYYMMDDw-1R100.gds` | `脚本所在目录/output`；整理后直接运行会变为 `archive/old_versions/output` | a=0.490；m0=0.15；R=125；core=60；s=0.32；w=-1；alpha=4 | `klayout.db`、`numpy`、`pathlib`、`datetime` | 理论可运行；依赖 KLayout Python API；与当前 6 个 disclination GDS 无直接对应 | 历史模板；结构类型不同，不是当前 disclination 主版本 | archive/old_versions |

## 补充判断

- `generate_batch13_disclination_dose_matrix_v01.py` 已加入 dose matrix 和 PEC 记录，但 PEC 仍是曝光设备设置，不改变 GDS 几何。
- 三个 `.py` 都包含或复用了版图文字 mark：主版本写 `a..._r...`，batch13 版本写 `d剂量-GDS序号`，历史模板写 `w=-1`。
- `disclination_vortex_1.ipynb` 不是 `.py` 文件，但它是 disclination 晶格推导和可视化历史版本；里面没有 GDS 写出逻辑，且保留了一次 `site_disclination[:,0]` 的列表切片报错记录。
- 本机当前 `python3` 环境没有安装 `klayout` 模块；需要在 KLayout Python 环境或已安装 `klayout` Python 包的环境中运行实际 GDS 生成。
