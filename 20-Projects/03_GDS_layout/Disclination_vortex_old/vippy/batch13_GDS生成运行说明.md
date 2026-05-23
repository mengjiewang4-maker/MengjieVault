---
title: batch13 GDS 生成运行说明
date: 2026-05-19
tags:
  - batch13_Si_EBL
  - GDS
  - KLayout
---

# batch13 GDS 生成运行说明

## 当前脚本

`current/generate_batch13_disclination_dose_matrix_v01.py`

## 已完成结果

- 已生成 priority 模式 GDS：24 个
- Dose：25%、30%、35%、40%
- PEC：文件名和对应表中标记为 `pec_on`
- 结构：GDS_01 到 GDS_06，保持 batch12 几何参数不变
- 输出目录：`outputs/gds/batch13_Si_EBL/20260519/`
- 总大小：约 359 MB

## 未生成内容

- 20% 低剂量边界：未生成实际 GDS
- 45% 对照剂量：未生成实际 GDS

如需完整 36 个 GDS，可运行完整模式命令。

## 依赖检查

普通 `python3` 环境没有 `klayout` 模块，不能直接写 GDS。KLayout app 内部命令行可用：

`/Applications/klayout.app/Contents/MacOS/klayout`

依赖检查命令：

```bash
BATCH13_CHECK_DEPS=1 /Applications/klayout.app/Contents/MacOS/klayout -b -r current/generate_batch13_disclination_dose_matrix_v01.py
```

已检查结果：`klayout.db` 可用。

## dry-run 预演

不生成 GDS，只生成预计文件名和区域对应表：

```bash
python3 current/generate_batch13_disclination_dose_matrix_v01.py --dry-run
```

只预演优先剂量 25%、30%、35%、40%：

```bash
python3 current/generate_batch13_disclination_dose_matrix_v01.py --dry-run --priority-only
```

## 实际生成 GDS

生成优先剂量 24 个 GDS：

```bash
BATCH13_PRIORITY_ONLY=1 /Applications/klayout.app/Contents/MacOS/klayout -b -r current/generate_batch13_disclination_dose_matrix_v01.py
```

生成完整 36 个 GDS：

```bash
/Applications/klayout.app/Contents/MacOS/klayout -b -r current/generate_batch13_disclination_dose_matrix_v01.py
```

## 文件命名规则

示例：

`batch13_20260519_D3_dose30_pec_on_GDS01_a0p554_r0p111.gds`

含义：

- `batch13_20260519`：batch13，生成日期 2026-05-19
- `D3`：Dose 组别
- `dose30`：剂量 30%
- `pec_on`：建议开启 PEC
- `GDS01`：第 1 个结构
- `a0p554`：周期 a = 0.554 um
- `r0p111`：孔半径约 0.111 um

## 注意

- GDS 文件里的 PEC 只是文件名和表格标记；真正 PEC 必须在 JBX-6300FS 曝光设置中开启。
- priority 模式未包含 20% 和 45%；如果需要对照点，需额外生成完整模式或单独扩展脚本。
- 每次实际用于 EBL 前，必须确认区域编号和 JBX job 中的实际版图区域一致。
