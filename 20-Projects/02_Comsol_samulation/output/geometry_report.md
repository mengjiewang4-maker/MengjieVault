# Geometry Report

生成时间：2026-05-21 22:00:54

## 输入

- DXF：`/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/disclination.dxf`
- 单位转换：auto: raw extent < 1e-3, treat as meter

## 修复流程

1. `ezdxf` 读取所有 entity。
2. 删除 construction/aux/helper/axis 等辅助线。
3. CIRCLE 用 128 点离散，ARC 自动离散，SPLINE flattening 采样。
4. `shapely.unary_union` 合并和去重线段。
5. `shapely.linemerge` 合并连续线段。
6. `shapely.polygonize` 自动闭合边界生成 polygon。
7. `unary_union` 合并 polygon。
8. `buffer(0)` 修复 invalid 几何。
9. 从 polygonize 小面片重建孔轮廓，从修复后的大面提取参考边界。

## 统计

- entity 统计：`{"LWPOLYLINE": 3445}`
- 删除辅助 entity：0
- 原始线段数量：22469
- polygonize 后 polygon 数：5409
- 修复后 polygon 数：1
- 空气孔/刻蚀孔：285
- 外边界/参考边界：1
- 总宽度：26.460000 um
- 总高度：26.460000 um
- 最大尺寸：26.460000 um
- 最小 polygon 尺寸：0.147000 um
- 最小 polygon 面积：1.695848e-02 um^2
- 近似最小孔边距：0.128511 um

## 几何有效性

- 修复前 invalid polygon：0
- 修复后 invalid polygon：0
- 过小结构数量：0

## 可加工性分析

结论：适合进入电子束曝光前检查流程

风险：

- 未发现小于 20 nm 的小特征
- 近似最小孔边距未低于 20 nm
- buffer(0) 后未检测到 invalid polygon
- 已用 polygonize + unary_union + buffer(0) 修复，但送厂前仍建议用 KLayout 做工艺 DRC

## 对比图

- 修复前：`output/disclination_before_repair.png`
- 修复后：`output/disclination_after_repair.png`
