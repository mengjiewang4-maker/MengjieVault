---
title: 下一步 SOI 光学测试样品计划
date: 2026-05-25
tags:
  - sample
  - SOI
  - optical-test
  - next-step
---

# 下一步 SOI 光学测试样品计划

## 1. 当前结论

当前 Si 样品：

```text
B15_20260522_Si_DiscFig2_EBLICP_S1_OK
```

验证结果：

```text
可以
```

这说明当前 Disclination cavity 的版图和 Si 工艺结果初步可用，可以进入 SOI 光学测试样品准备阶段。

## 2. 下一步目标

在 SOI 上制备光学测试样品。

## 3. SOI 样品前必须确认

| 信息 | 状态 | 说明 |
|---|---|---|
| SOI 器件层厚度 | 待确认 | 影响光学模式和刻蚀深度 |
| BOX 厚度 | 待确认 | BOX 是 buried oxide，埋氧层 |
| 刻蚀深度 | 待确认 | 需要明确是刻穿器件层还是部分刻蚀 |
| 当前 GDS 是否复用 | 待确认 | 可以先以 `disclination_a559_r0p2_n3p4_extended_100um.gds` 为基准 |
| 是否需要调整 GDS | 待确认 | SOI 光学测试可能需要加光栅、波导、对准标记或测试阵列 |
| 基底字段 | 必须改为 SOI | 文件名中不能继续写 Si |
| 涂胶参数 | 必须记录 | 当前最容易缺失 |
| RIE 去胶参数 | 必须记录 | 当前最容易缺失 |
| SEM 区域编号 | 必须记录 | 确保 SEM 文件名能反查区域 |

## 4. 新样品命名建议

```text
B16_YYYYMMDD_SOI_DiscFig2_EBLICP_S1_Optical
```

字段解释：

| 字段 | 含义 |
|---|---|
| B16 | 下一批次 |
| YYYYMMDD | 实际加工日期 |
| SOI | 基底从 Si 改为 SOI |
| DiscFig2 | Disclination cavity, Nature Photonics 2024 Fig.2 |
| EBLICP | 完成 EBL + ICP |
| S1 | SOI 样品 1 |
| Optical | 目标是光学测试 |

## 5. 建议下一步检查清单

- 确认 SOI 器件层厚度；
- 确认 BOX 厚度；
- 确认目标刻蚀深度；
- 决定是否复用当前 GDS；
- 如果需要光学测试，确认是否要加入波导、光栅、端面耦合结构或定位标记；
- 建立新的 SOI 区域映射表；
- SEM 文件名中明确写 `SOI`，不要沿用 `Si`。
