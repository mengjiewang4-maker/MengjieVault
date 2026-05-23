# 从 COMSOL 导出几何给 GDS 转换

当前机器没有检测到 COMSOL 或 LiveLink，因此不能用官方 API 直接执行 `mph` 几何导出。这里给出半自动流程，供你在有 COMSOL 的电脑上导出真实二维几何。

## 推荐导出格式

优先级：

1. DXF：适合二维版图轮廓，后续最容易转 GDS。
2. SVG：适合简单曲线/多边形，但单位和缩放要仔细核对。
3. CSV/TXT：如果你能导出圆孔中心和半径，最适合参数化重建。
4. STL：主要是三维网格，二维 GDS 不优先使用，除非只能导出 STL。

## COMSOL GUI 操作

1. 打开 `disclination_1.mph`。
2. 在 Model Builder 中确认几何为 `Geometry 1 (geom1)`。
3. 右键 `Geometry 1` 或进入几何节点的导出功能。
4. 选择 `Export`。
5. 格式选择 `DXF`。如果没有 DXF，尝试 `SVG` 或导出几何数据。
6. 单位选择 `um`；如果只能选择 SI 单位，请记录导出单位是 `m`。
7. 只导出二维几何轮廓，不导出仿真场图。
8. 保存到本目录，例如：

```text
20-Projects/02_Comsol_samulation/comsol_export/geometry.dxf
```

## 如果导出 CSV/TXT

建议列名：

```csv
tag,x,y,r
circle_1,0.1398053,-0.1924255,0.0735
```

所有数值使用 `um`。`x/y` 是圆心坐标，`r` 是半径。

## 转换为 GDS

导出后在本目录运行：

```bash
python3 scripts/convert_dxf_to_gds.py comsol_export/geometry.dxf
```

或：

```bash
python3 scripts/convert_dxf_to_gds.py comsol_export/holes.csv
```

输出会写到 `output/`。

## 为什么不要用截图

仿真截图包含颜色场、坐标轴、抗锯齿、缩放和 UI 元素，无法可靠代表真实加工轮廓。截图轮廓提取会引入孔径误差、边界误差和拓扑错误，因此只能用于人工核对外观，不能作为微纳加工版图来源。

