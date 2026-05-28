# vippy GDS 版图生成脚本说明

## 1. 文件夹用途

本文件夹用于管理 Disclination vortex 结构的 GDS 版图生成脚本、历史版本、输出 GDS 和对应关系。

## 2. 当前主脚本

当前推荐主脚本位于：`current/disclination_vortex_gds_current.py`

这个脚本来自原始文件 `disclination_vortex_gds.py`，用于生成 `mjYYYYMMDD_01.gds` 到 `mjYYYYMMDD_06.gds` 六个 disclination vortex GDS。

batch13 候选脚本位于：`current/generate_batch13_disclination_dose_matrix_v01.py`

这个脚本用于在保持 6 个结构几何不变的前提下，生成带 Dose/PEC mark 的 batch13 GDS 和区域对应表。当前环境缺少 `numpy` 和 `klayout` Python 模块，因此尚未实际运行生成 batch13 GDS；已完成 dry-run，生成了预计文件名和区域对应表。

## 3. 历史版本位置

历史版本放在：`archive/old_versions/`

包括早期 notebook、非当前主线的 Dirac/vortex 模板脚本等。

## 4. 测试脚本位置

测试脚本放在：`tests/test_scripts/`

当前没有明确测试脚本。

## 5. 输出文件位置

已有 GDS 输出放在：`outputs/gds/`

当前 20260517 这批 GDS 位于：`outputs/gds/20260517/`

参数记录和对应关系放在：`outputs/mapping/`

## 6. py 与 GDS 对应关系

详见：`Py_GDS_对应关系.md`

同一份对应关系也保存在：`outputs/mapping/Py_GDS_对应关系.md`

## 7. 后续开发建议

- 不要直接改 current 主脚本。
- 新版本先从 current 复制为 `vXX` 或带日期的新文件。
- 每次生成 GDS 必须更新 `Py_GDS_对应关系.md`。
- 每次用于 EBL 的 GDS 必须记录对应样品编号。
- 如果脚本位置发生移动，要特别检查输出路径，因为当前主脚本使用 `__file__` 所在目录作为输出根目录。
