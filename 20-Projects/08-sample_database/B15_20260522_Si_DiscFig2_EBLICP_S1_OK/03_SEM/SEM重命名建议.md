---
title: B15 SEM 重命名建议
date: 2026-05-25
tags:
  - sample
  - batch15
  - SEM
  - rename-suggestion
---

# SEM 重命名建议

> [!warning]
> 这是建议表，不要直接重命名原始 SEM 文件。先人工确认位置和倍率，再把确认后的副本放入 `重命名图/`。

## 1. SEM 文件命名规则

推荐格式：

```text
B15_20260522_Si_DiscFig2_a559r0p2n3p4_D90_R01_center_30k_OK_001.tif
```

字段解释：

| 字段 | 含义 |
|---|---|
| B15 | Batch15 |
| 20260522 | 日期 |
| Si | 基底 |
| DiscFig2 | 结构来源 |
| a559r0p2n3p4 | GDS 关键参数 |
| D90 | EBL 剂量 90% |
| R01 | 区域编号 |
| center | SEM 位置 |
| 30k | SEM 倍率 |
| OK | 结果 |
| 001 | 第几张图 |

## 2. 当前重命名建议表

| 原SEM文件名 | 建议新文件名 | 样品 | 区域 | GDS | Dose | 位置 | 倍率 | 结果 |
|---|---|---|---|---|---|---|---|---|
| `BATCH15_20260522_EBL_ICP_RIE_S1_P1_1.tif` | `B15_20260522_Si_DiscFig2_a559r0p2n3p4_D90_R01_unknown_unknown_OK_001.tif` | `B15_20260522_Si_DiscFig2_EBLICP_S1_OK` | R01 | `disclination_a559_r0p2_n3p4_extended_100um.gds` | 90% | unknown | unknown | OK |

## 3. 待人工补充

| 原字段 | 当前值 | 需要补充成 |
|---|---|---|
| 位置 | unknown | `center`、`edge`、`corner`、`overview` 或 `defect` |
| 倍率 | unknown | 例如 `10k`、`30k`、`50k` |
| 区域 | R01 | 如果 P1_1 不是 R01，需要改成实际区域编号 |

## 4. 重要限制

- 不删除原始 SEM 图；
- 不覆盖原始 SEM 图；
- 不立即批量重命名；
- 先确认 `P1_1` 对应的版图区域、SEM 位置和倍率。
