# Disclination_vortex 文件夹说明

本文件夹用于管理 Disclination vortex 相关的 GDS 版图、Python 生成脚本、论文 Fig.2 推导代码、仿真导出文件和历史版本。

## 快速入口

| 目录 | 用途 | 说明 |
|---|---|---|
| `vippy/` | 当前主线 | 当前推荐使用的 GDS 生成脚本、batch13 GDS 输出、py-GDS 对应关系都在这里 |
| `00_docs/` | 说明和笔记 | 历史 README、版图索引、Python 学习笔记、晶格分类笔记 |
| `01_current_mainline/` | 当前主线说明 | 指向 `vippy/`，避免移动当前主线导致路径混乱 |
| `02_historical_gds_outputs/` | 历史 GDS | 20260417、20260420、20260515、20260516 等早期 GDS 输出 |
| `03_paper_figure2_derivation/` | 论文 Fig.2 推导 | tight-binding、C5/disclination 推导、早期 GDS 探索脚本，内部已按用途分类 |
| `04_simulation_exports/` | 仿真相关 | COMSOL/Lumerical 导出脚本、`structure.lsf`、`resonators.csv` |
| `05_hexagonal_legacy/` | 六边形旧版 | 早期六边形 disclination notebook 和 GDS 脚本 |
| `90_backups/` | 局部备份 | `vippy` 整理前备份 |
| `99_environment_system_files/` | 环境/系统文件 | `environment.yml`、原 `.gitignore`、`.DS_Store` |

## 当前最重要文件

- 当前主线目录：`vippy/`
- 当前主脚本：`vippy/current/disclination_vortex_gds_current.py`
- batch13 生成脚本：`vippy/current/generate_batch13_disclination_dose_matrix_v01.py`
- batch13 priority GDS：`vippy/outputs/gds/batch13_Si_EBL/20260519/`
- batch13 区域对应表：`vippy/outputs/mapping/batch13_20260519_GDS_Dose_PEC_区域对应表_priority.md`
- Fig.2 推导索引：`03_paper_figure2_derivation/文件分类索引.md`

## 备份

整理前已备份整个文件夹到：

`03_GDS_layout/Disclination_vortex_backup_20260519_1432`

## 注意

- 没有删除任何 `.py` 文件。
- 没有删除任何 `.gds` 文件。
- `vippy/` 是当前主线，为了保持已生成记录中的路径稳定，本次没有把它移动到子目录。
- 旧版 GDS 和论文推导脚本已归入分类目录，方便查找和阅读。
