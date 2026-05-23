# COMSOL 几何到 GDS 版图

## 输入文件

- COMSOL 仿真文件：`disclination_1.mph`
- 读取来源：`.mph` 内部的 `dmodel.xml` 几何特征，而不是仿真截图。

## 输出文件

- GDS：`disclination_a555_r0p15_n3p4_extended_100um.gds`
- PNG 预览：`disclination_a555_r0p15_n3p4_extended_100um_preview.png`
- 参数 JSON：`disclination_a555_r0p15_n3p4_extended_100um_params.json`
- 本说明：`README_disclination_a555_r0p15_n3p4_extended_100um.md`

## 单位

- 脚本内部和 JSON 均使用 `um`。
- GDS library unit 为 `1 um`，数据库精度为 `1 nm`。

## Layer 定义

- layer 1：光子晶体圆孔/刻蚀图形，共 `68445` 个圆孔，多边形近似。
- layer 10：参考边界，包括 COMSOL 中的 `substrate1`、`PML1` 和四个 partition square；不建议直接作为刻蚀层。
- layer 20：文本标注。

## 缩放

- 原始孔阵列外包络直径：`99.40794449798463` um
- 当前缩放倍数：`1.0`
- 当前孔阵列外包络直径：`99.40794449798463` um
- 扩展阵列 grid size：`117`
- 扩展阵列说明：`保持 a=0.555 um、r=0.08325 um 不变，按原始 5 扇区 disclination 规律扩展为 5 x 117 x 117 个圆孔。`

## 重新运行

在当前目录执行：

```bash
python3 scripts/comsol_mph_to_gds.py disclination_1.mph
```

如果需要改变圆孔近似精度：

```bash
python3 scripts/comsol_mph_to_gds.py disclination_1.mph --circle-points 64
```

## 几何来源

- 来自 COMSOL：参数 `a/R/r`、原始 5 扇区坐标规律、`substrate1`/`PML1` 参考圆、四个 `square_*` 分区边界。
- 手动设定：按原始规律向外扩展为 `5 x 117 x 117` 个圆孔、圆孔多边形近似点数、layer 编号、GDS 文本标注、最小线宽/间距检查阈值。
- 未使用：微信截图/仿真场图。截图只适合人工核对外观，不适合直接加工。

## 基本检查结果

- GDS 写入方式：`builtin_simple_gds_writer`
- 最小孔径：`0.1665` um
- 最小孔边到孔边距离：`-0.060932726691246594` um
- 超出 substrate 的孔数量：`64225`
- 超出 PML 的孔数量：`58920`

注意：如果最小孔间距为负数，表示同层圆孔有重叠。GDS 文件本身有效，但正式送厂前建议在 KLayout/gdstk 中做 Boolean union（布尔并集，把重叠图形合成一个图形）和工艺 DRC。
