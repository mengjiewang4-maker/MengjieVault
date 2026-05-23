# current

这里放当前推荐主版本。

当前主文件：`disclination_vortex_gds_current.py`

batch13 候选文件：`generate_batch13_disclination_dose_matrix_v01.py`

注意：该脚本使用 `Path(__file__).resolve().parent` 作为输出根目录，因此在这里直接运行时，GDS 会输出到 `current/YYYYMMDD/`。如果需要统一输出到 `outputs/gds/`，请在复制出的新版本中修改输出路径。

`generate_batch13_disclination_dose_matrix_v01.py` 已经固定输出到 `outputs/gds/batch13_Si_EBL/YYYYMMDD/`，并会同步生成 GDS-Dose-PEC-区域对应表。

当前普通 `python3` 环境缺少 `klayout` Python 模块，但 `/Applications/klayout.app/Contents/MacOS/klayout` 可用于批处理生成 GDS。batch13 脚本已去掉 `numpy` 依赖，实际出图只需要 KLayout。

dry-run 命令：

```bash
python3 current/generate_batch13_disclination_dose_matrix_v01.py --dry-run
```

生成优先剂量 GDS 的命令：

```bash
BATCH13_PRIORITY_ONLY=1 /Applications/klayout.app/Contents/MacOS/klayout -b -r current/generate_batch13_disclination_dose_matrix_v01.py
```

dry-run 已生成：

- `outputs/gds/batch13_Si_EBL/20260519/batch13_20260519_GDS参数记录_dryrun.md`
- `outputs/mapping/batch13_20260519_GDS_Dose_PEC_区域对应表_dryrun.md`

priority 模式已生成：

- `outputs/gds/batch13_Si_EBL/20260519/` 下 24 个 GDS
- `outputs/gds/batch13_Si_EBL/20260519/batch13_20260519_GDS参数记录_priority.md`
- `outputs/mapping/batch13_20260519_GDS_Dose_PEC_区域对应表_priority.md`
