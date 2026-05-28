# GDS 生成记录

生成日期：2026-05-21

## 说明

- 输入来源：`disclination_1.mph` 内部 `dmodel.xml` 的 COMSOL 几何参数。
- 版图来源：真实圆孔几何参数，不是仿真截图轮廓。
- 单位：所有尺寸均为 `um`。
- GDS 精度：数据库精度为 `1 nm`。
- 圆孔数量：每个版本均为 1125 个圆孔。
- layer 1：主体刻蚀区域/光子晶体圆孔。
- layer 10：参考边界，包括 substrate、PML 和分区 square。
- layer 20：文本标注。

术语说明：

- GDS：微纳加工常用版图文件格式。
- layer：版图图层，不同层可代表不同加工步骤或参考标记。
- 外包络直径：这里指 layer 1 圆孔阵列的最大宽度/高度，不包含外侧 PML 参考圆。
- 最小孔边距：相邻孔边缘之间的最小距离；负数表示孔之间有重叠。

## 汇总表

| 版本                 | GDS                                               | 参数来源             |     a |       r |      R | n_substrate | 孔阵列外包络直径 |   缩放倍数 |   最小孔径 |   最小孔边距 |
| ------------------ | ------------------------------------------------- | ---------------- | ----: | ------: | -----: | ----------: | -------: | -----: | -----: | ------: |
| 默认 COMSOL          | `disclination_from_comsol.gds`                    | mph 原始参数         | 0.490 |  0.0735 |  8.820 |         3.4 |  10.8543 | 1.0000 | 0.1470 | -0.0538 |
| 20 um 扩展阵列         | `disclination_a554_r0p2_n3p33_extended_20um.gds`  | 截图图 1 参数 + 外圈补阵列 | 0.554 |  0.1108 |  9.972 |        3.33 |  19.1475 | 1.0000 | 0.2216 | -0.1162 |
| 50 um 扩展阵列（推荐）     | `disclination_a554_r0p2_n3p33_extended_50um.gds`  | 截图图 1 参数 + 外圈补阵列 | 0.554 |  0.1108 |  9.972 |        3.33 |  49.8382 | 1.0000 | 0.2216 | -0.1162 |
| 图 1 参数 100 um 扩展阵列 | `disclination_a554_r0p2_n3p33_extended_100um.gds` | 截图图 1 参数 + 外圈补阵列 | 0.554 |  0.1108 |  9.972 |        3.33 |  99.2842 | 1.0000 | 0.2216 | -0.1162 |
| 图 2 参数 100 um 扩展阵列 | `disclination_a559_r0p2_n3p4_extended_100um.gds`  | 截图图 2 参数 + 外圈补阵列 | 0.559 |  0.1118 | 10.062 |         3.4 | 100.1803 | 1.0000 | 0.2236 | -0.1173 |
| 图 3 参数 100 um 扩展阵列 | `disclination_a555_r0p15_n3p4_extended_100um.gds` | 截图图 3 参数 + 外圈补阵列 | 0.555 | 0.08325 |  9.990 |         3.4 |  99.4079 | 1.0000 | 0.1665 | -0.0609 |
| 图 1 参数             | `disclination_a554_r0p2_n3p33.gds`                | 截图参数表覆盖          | 0.554 |  0.1108 |  9.972 |        3.33 |  12.3274 | 1.0000 | 0.2216 | -0.1162 |
| 图 2 参数             | `disclination_a559_r0p2_n3p4.gds`                 | 截图参数表覆盖          | 0.559 |  0.1118 | 10.062 |         3.4 |  12.4386 | 1.0000 | 0.2236 | -0.1173 |
| 图 3 参数             | `disclination_a555_r0p15_n3p4.gds`                | 截图参数表覆盖          | 0.555 | 0.08325 |  9.990 |         3.4 |  12.2941 | 1.0000 | 0.1665 | -0.0609 |

## 每个版本的文件

### 默认 COMSOL 参数

- GDS：`output_20260521_1/disclination_from_comsol.gds`
- 预览：`output_20260521_1/disclination_from_comsol_preview.png`
- 参数 JSON：`output_20260521_1/disclination_from_comsol_params.json`
- README：`output_20260521_1/README_comsol_to_gds.md`
- 参数：`a=490[nm]`，`r=0.15*a`，`R=18.0*a`，`n_substrate=3.4`

### 20 um 扩展阵列版本

- GDS：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_20um.gds`
- 预览：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_20um_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_20um_params.json`
- README：`output_20260521_1/README_disclination_a554_r0p2_n3p33_extended_20um.md`
- 参数：`a=554[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.33`
- 扩展方式：保持单元尺寸不变，把原始 5 扇区 disclination 扩展/裁定为 `5 x 23 x 23`。
- 圆孔数量：2645
- 实际孔阵列外包络直径：19.1475 um

### 50 um 扩展阵列版本

- GDS：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_50um.gds`
- 预览：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_50um_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_50um_params.json`
- README：`output_20260521_1/README_disclination_a554_r0p2_n3p33_extended_50um.md`
- 参数：`a=554[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.33`
- 扩展方式：保持单元尺寸不变，把原始 5 扇区 disclination 从 `5 x 15 x 15` 扩展为 `5 x 59 x 59`。
- 圆孔数量：17405
- 实际孔阵列外包络直径：49.8382 um
- 说明：`R=18a` 参考圆保持不变，因此扩展后的很多孔会位于 layer 10 参考圆外侧，这是本版本的预期行为。

### 100 um 扩展阵列版本

- GDS：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_100um.gds`
- 预览：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_100um_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a554_r0p2_n3p33_extended_100um_params.json`
- README：`output_20260521_1/README_disclination_a554_r0p2_n3p33_extended_100um.md`
- 参数：`a=554[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.33`
- 扩展方式：保持单元尺寸不变，把原始 5 扇区 disclination 扩展为 `5 x 117 x 117`。
- 圆孔数量：68445
- 实际孔阵列外包络直径：99.2842 um
- 说明：`R=18a` 参考圆保持不变，因此扩展后的很多孔会位于 layer 10 参考圆外侧，这是本版本的预期行为。

### 图 2 参数 100 um 扩展阵列版本

- GDS：`output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um.gds`
- 预览：`output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a559_r0p2_n3p4_extended_100um_params.json`
- README：`output_20260521_1/README_disclination_a559_r0p2_n3p4_extended_100um.md`
- 参数：`a=559[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.4`
- 扩展方式：保持单元尺寸不变，把原始 5 扇区 disclination 扩展为 `5 x 117 x 117`。
- 圆孔数量：68445
- 实际孔阵列外包络直径：100.1803 um

### 图 3 参数 100 um 扩展阵列版本

- GDS：`output_20260521_1/disclination_a555_r0p15_n3p4_extended_100um.gds`
- 预览：`output_20260521_1/disclination_a555_r0p15_n3p4_extended_100um_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a555_r0p15_n3p4_extended_100um_params.json`
- README：`output_20260521_1/README_disclination_a555_r0p15_n3p4_extended_100um.md`
- 参数：`a=555[nm]`，`r=0.15*a`，`R=18.0*a`，`n_substrate=3.4`
- 扩展方式：保持单元尺寸不变，把原始 5 扇区 disclination 扩展为 `5 x 117 x 117`。
- 圆孔数量：68445
- 实际孔阵列外包络直径：99.4079 um

### 图 1 参数版本

- GDS：`output_20260521_1/disclination_a554_r0p2_n3p33.gds`
- 预览：`output_20260521_1/disclination_a554_r0p2_n3p33_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a554_r0p2_n3p33_params.json`
- README：`output_20260521_1/README_disclination_a554_r0p2_n3p33.md`
- 参数：`a=554[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.33`

### 图 2 参数版本

- GDS：`output_20260521_1/disclination_a559_r0p2_n3p4.gds`
- 预览：`output_20260521_1/disclination_a559_r0p2_n3p4_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a559_r0p2_n3p4_params.json`
- README：`output_20260521_1/README_disclination_a559_r0p2_n3p4.md`
- 参数：`a=559[nm]`，`r=0.2*a`，`R=18.0*a`，`n_substrate=3.4`

### 图 3 参数版本

- GDS：`output_20260521_1/disclination_a555_r0p15_n3p4.gds`
- 预览：`output_20260521_1/disclination_a555_r0p15_n3p4_preview.png`
- 参数 JSON：`output_20260521_1/disclination_a555_r0p15_n3p4_params.json`
- README：`output_20260521_1/README_disclination_a555_r0p15_n3p4.md`
- 参数：`a=555[nm]`，`r=0.15*a`，`R=18.0*a`，`n_substrate=3.4`

## 重新生成命令

```bash
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_from_comsol
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a554_r0p2_n3p33_extended_20um --set-param 'a=554[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.33' --extend-pattern-diameter-um 20
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a554_r0p2_n3p33_extended_50um --set-param 'a=554[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.33' --extend-pattern-diameter-um 50
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a554_r0p2_n3p33_extended_100um --set-param 'a=554[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.33' --extend-pattern-diameter-um 100
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a559_r0p2_n3p4_extended_100um --set-param 'a=559[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.4' --extend-pattern-diameter-um 100
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a555_r0p15_n3p4_extended_100um --set-param 'a=555[nm]' --set-param 'R=18.0*a' --set-param 'r=0.15*a' --set-param 'n_substrate=3.4' --extend-pattern-diameter-um 100
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a554_r0p2_n3p33 --set-param 'a=554[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.33'
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a559_r0p2_n3p4 --set-param 'a=559[nm]' --set-param 'R=18.0*a' --set-param 'r=0.2*a' --set-param 'n_substrate=3.4'
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --output-prefix disclination_a555_r0p15_n3p4 --set-param 'a=555[nm]' --set-param 'R=18.0*a' --set-param 'r=0.15*a' --set-param 'n_substrate=3.4'
```

## 加工前提醒

这些 GDS 文件是有效的 GDSII 文件，但最小孔边距为负数，说明同层圆孔有重叠。若这是设计意图，可以在送厂前用 KLayout 做 Boolean union（布尔并集，把重叠图形合成一个图形）和工艺 DRC（设计规则检查）。
