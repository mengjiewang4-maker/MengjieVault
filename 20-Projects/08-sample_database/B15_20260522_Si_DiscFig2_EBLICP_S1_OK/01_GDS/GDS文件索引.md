---
title: B15 GDS 文件索引
date: 2026-05-25
tags:
  - sample
  - batch15
  - GDS
  - traceability
---

# GDS 文件索引

## 1. 当前样品使用的 GDS

| GDS编号 | GDS文件 | GDS简写 | 结构参数 | 基底 | Dose | 结果 | 备注 |
|---|---|---|---|---|---|---|---|
| GDS01 | `disclination_a559_r0p2_n3p4_extended_100um.gds` | `a559r0p2n3p4` | `a=559 nm`，`r=0.2*a`，`n_substrate=3.4`，`extended=100 um` | Si | 90% | 可以 | 当前已成功样品 |

## 2. 文件路径

GDS 文件路径：

```text
/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um.gds
```

GDS 预览图：

```text
/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um_preview.png
```

参数 JSON：

```text
/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um_params.json
```

实际确认的生成脚本：

```text
/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/scripts_20260521_1/comsol_mph_to_gds.py
```

旧记录中的脚本路径：

```text
/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/scripts/dxf_to_gds.py
```

> [!warning]
> 旧记录中的 `scripts/dxf_to_gds.py` 当前不存在。后续追溯和复现优先使用实际确认的 `comsol_mph_to_gds.py`。

## 3. 重新生成命令

在 `20-Projects/02_Comsol_samulation/` 中运行：

```bash
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a559_r0p2_n3p4_extended_100um --set-param 'a=559[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.4' --extend-pattern-diameter-um 100
```

## 4. 术语说明

- `GDS`：微纳加工常用版图文件。
- `GDS简写`：放进 SEM 文件名里的短参数名，方便从文件名反查 GDS。
- `n3p4`：表示 `n_substrate=3.4`，这里的 `p` 是小数点的替代写法。
