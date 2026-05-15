---
title: Disclination-vortex加工路线总结
date: 2026-05-14
tags:
  - disclination-vortex
  - 微腔加工
  - 加工路线
  - 待整理
---

# Disclination-vortex 加工路线总结

## 用途

本页用于从 `codex_job` 中的论文笔记、概念页和 GDS 代码说明中提炼 disclination vortex 当前加工路线。它不是原始代码说明，而是后续加工、SEM 和问题排查用的总结页。

## 当前状态

- disclination vortex：正在加工。
- 当前加工入口：[[微腔加工与光学测试/02-微腔加工/01-样品设计/Disclination当前加工入口|Disclination 当前加工入口]]
- 当前样品批次：[[微腔加工与光学测试/02-微腔加工/01-样品设计/MC-20260514-01-样品与器件索引|MC-20260514-01 样品与器件索引]]
- 当前 GDS：[[微腔加工与光学测试/02-微腔加工/02-版图设计/GDS-mj20260420-版图索引|GDS-mj20260420 版图索引]]
- 当前工艺参数：[[微腔加工与光学测试/02-微腔加工/10-工艺参数数据库/MC-20260514-01-工艺参数卡|MC-20260514-01 工艺参数卡]]

## 当前加工链条

```text
论文与模式判据 -> GDS脚本 -> GDS输出 -> 曝光 -> 刻蚀 -> 去胶清洗 -> SEM -> 后续测试预留
```

## 需要重点记录

| 环节 | 需要记录 |
|---|---|
| GDS | 文件名、R、a、孔径、角度/半径重映射参数 |
| 曝光 | 胶、胶厚、旋涂、前烘、剂量、设备 |
| 刻蚀 | 气体、功率、压强、时间、刻蚀深度 |
| SEM | 孔径、周期、塌陷、残胶、边缘粗糙度 |
| 问题 | 过曝、欠刻、孔径偏差、结构损伤 |

## 需要参考的资料

- `/Users/mac/Documents/mengjie/MengjieVault/codex_job/obsidian/raw/papers/02_on_chip_lasers/Vortex nanolaser based on a photonic-unknown-Vortex nanolaser based on a photonic.md`
- `/Users/mac/Documents/mengjie/MengjieVault/codex_job/obsidian/raw/notes/Vortex nanolaser based on a photonic disclination cavity - source note.md`
- `/Users/mac/Documents/mengjie/MengjieVault/codex_job/obsidian/wiki/research/topics/Photonic disclination cavity.md`
- `/Users/mac/Documents/mengjie/MengjieVault/codex_job/obsidian/wiki/research/topics/Angular momentum labeling in TB.md`
- `/Users/mac/Documents/mengjie/MengjieVault/codex_job/obsidian/wiki/research/topics/TB-to-photonic mapping.md`
- `/Users/mac/Documents/mengjie/MengjieVault/20-Projects/Project_Replication_Vortex/README.md`
- `/Users/mac/Documents/mengjie/MengjieVault/20-Projects/Project_Replication_Vortex/disclination_vortex_gds.py`

## 待补

- [ ] 补充 disclination 结构的模式判据。
- [ ] 补充当前 GDS 与论文结构的差异。
- [ ] 补充加工风险：过曝、孔径偏差、刻蚀深度不足。
- [ ] SEM 后补实际形貌判断。
- [ ] 加工完成后再建立正式光学测试记录。

