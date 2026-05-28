---
title: Py 与 GDS 对应关系
date: 2026-05-19
tags:
  - GDS
  - Python
  - mapping
---

# Py_GDS_对应关系

| Python文件 | 可能生成的GDS文件 | GDS输出路径 | 是否已存在 | 备注 |
| --- | --- | --- | --- | --- |
| `disclination_vortex_gds_current.py` | `mj20260517_01.gds` 到 `mj20260517_06.gds`；若今天重跑则为 `mjYYYYMMDD_01.gds` 到 `mjYYYYMMDD_06.gds` | `outputs/gds/20260517/` 中已有；脚本重跑默认输出到脚本所在目录的日期子文件夹 | 是 | 当前 20260517 六个 GDS 与该脚本参数记录完全对应 |
| `generate_batch13_disclination_dose_matrix_v01.py` | 完整模式预计 36 个 GDS；priority 模式已生成 24 个 GDS：25%、30%、35%、40% × GDS_01-06 | `outputs/gds/batch13_Si_EBL/20260519/`；区域对应表在 `outputs/mapping/` | 是 | 已用 KLayout 生成 priority 版本 24 个 GDS；未生成 20% 和 45% 对照 GDS |
| `generate_dirac_vortex_wm1_R100_template_v01.py` | `wmjYYYYMMDDw-1R100.gds` | `output/`，整理后直接运行会在 `archive/old_versions/output/` | 否 | 不是当前 disclination 结构；未发现已存在的输出 GDS |

## 注意

- `disclination_vortex_gds_current.py` 的输出文件名包含运行日期，因此实际 GDS 文件名会随运行日期变化。
- 当前用于 batch12 的实际 GDS 是 `mj20260517_01.gds` 到 `mj20260517_06.gds`。
- batch13 已新增候选脚本 `current/generate_batch13_disclination_dose_matrix_v01.py`。运行前建议先确认是否真的需要 36 个带 mark 的 GDS，还是只需要沿用 6 个无 dose mark 的结构 GDS。
- dry-run 预演文件：`outputs/gds/batch13_Si_EBL/20260519/batch13_20260519_GDS参数记录_dryrun.md`
- dry-run 区域对应表：`outputs/mapping/batch13_20260519_GDS_Dose_PEC_区域对应表_dryrun.md`
- priority 实际 GDS 参数记录：`outputs/gds/batch13_Si_EBL/20260519/batch13_20260519_GDS参数记录_priority.md`
- priority 实际区域对应表：`outputs/mapping/batch13_20260519_GDS_Dose_PEC_区域对应表_priority.md`
