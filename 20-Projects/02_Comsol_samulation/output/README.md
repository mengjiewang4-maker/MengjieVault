# COMSOL DXF to GDS

## 输入文件

- `/Users/mac/Documents/mengjie/MengjieVault/20-Projects/02_Comsol_samulation/disclination.dxf`

## 输出文件

- `output/disclination_from_comsol.gds`
- `output/disclination_preview.png`
- `output/disclination_before_repair.png`
- `output/disclination_after_repair.png`
- `output/disclination_params.json`
- `output/geometry_report.md`

## 单位

- DXF 原始单位：auto: raw extent < 1e-3, treat as meter
- GDS 输出单位：um
- GDS 数据库精度：1 nm

## Layer 定义

- layer 1：空气孔/刻蚀孔
- layer 10：外边界
- layer 20：文字说明 `Generated_from_COMSOL`

## 生成时间

2026-05-21 22:00:54

## 运行方法

```bash
PYTHONPATH=.python_deps python3 scripts/dxf_to_gds.py
```

## 可加工性

适合进入电子束曝光前检查流程
