# Fig.2 d/e/f C5 Photonic Disclination Cavity GDS

## 复现目标

复现论文《Vortex nanolaser based on a photonic disclination cavity》Fig.2 中 d/e/f 对应的 C5 photonic disclination cavity。
本输出不是示意图，而是可导入 KLayout/COMSOL/Lumerical 的平面空气孔 GDS。

## 参考论文

- 本地论文路径：`/Users/mac/Documents/mengjie/MengjieVault/90-Local_Not_Upload/PDF/papers/02_on_chip_lasers/Vortex nanolaser based on a photonic disclination cavity.pdf`
- DOI/页面：`https://www.nature.com/articles/s41566-023-01338-2`
- 关键参数来源：主文 Fig.2、Methods、Extended Data Fig.3。

## Fig.2 d/e/f 与 GDS 的对应关系

| 图 | 内容 | 是否独立 GDS 几何 | 本输出对应关系 |
|---|---|---|---|
| Fig.2d | C5 symmetric disclination 的 TB in-gap states | 否 | TB 能级结果，不单独生成 GDS |
| Fig.2e | 五个 C5 能态的概率密度和角动量分类 | 否 | TB 模式结果，不单独生成 GDS |
| Fig.2f | C5 photonic disclination cavity 和 Hz 模式 | 是 | `fig2def_c5_added_quarter_sector.gds` |

## 参数表

| 参数 | 数值 | 来源/说明 |
|---|---:|---|
| lattice constant a | 500.0 nm | Extended Data Fig.3 C5 2D FEM |
| hole radius r0 | 0.200 a = 100.0 nm | Extended Data Fig.3 C5 |
| center-to-hole distance d0 | 0.450 a = 225.0 nm | Extended Data Fig.3 C5 |
| added sector angle | 0.50 pi | +1/4 sector |
| target symmetry | C5 | C5, added one sector to C4 |
| core shift dc | 0.250 a = 125.0 nm | Extended Data Fig.3 C5 |
| boundary shift db | 0.230 a = 115.0 nm | 记录为参数，逐点规则待确认 |
| interior corner shift di | 0.000 a | Extended Data Fig.3 C5 |
| lattice range | 13 unit cells per side | 可调参数 |
| GDS layer/datatype | 1/0 | 可调参数 |
| hole count | 2755 | 生成结果 |

## 输出文件

- GDS：`fig2def_c5_added_quarter_sector.gds`
- PNG：`fig2def_c5_added_quarter_sector_preview.png`
- 参数 JSON：`parameters.json`
- README：`README.md`

## 孔类型统计

| 类型 | 数量 |
|---|---:|
| bulk_0325_style | 2755 |

## 代码运行方式

```bash
cd /Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/disclination
python3 scripts/disclination_fig2_def_gds.py
```

常用可调参数示例：

```bash
python3 scripts/disclination_fig2_def_gds.py --lattice-constant-nm 500 --hole-radius-ratio 0.20 --center-to-hole-ratio 0.45 --lattice-range 13
```

## 当前假设

- 使用 KLayout Python API (`klayout.db`) 写 GDS。
- 使用 square SSH-like 单胞：每个 C4 单胞四个圆孔，孔中心距单胞中心为 d0。
- 默认使用 0325 TB 脚本风格的第一象限点阵角度映射，避免 5 个硬扇区拼接产生明显分界线。
- 旧版 `generate_square_ssh_lattice + apply_volterra_added_quarter_sector` 扇区复制函数仍保留在源码中，便于对照。
- GDS 仅描述空气孔平面图形；材料、厚度、PML、端口等仿真设置不在 GDS 中。

## 尚未确认的问题

- 论文 Fig. 2d/e 是 TB 结果，不是独立 GDS 几何；本脚本只输出对应 C5 photonic cavity 几何。
- COMSOL 目录只有截图，没有可机器读取的 mph/txt/md 参数文件；截图参数仅作为本地历史参考。
- 论文 Extended Data Fig. 3 给出 db/di，但没有完整说明每个边界孔的逐点位移规则；当前 GDS 使用 0325 TB 风格连续点阵并显式应用核心 dc 修正，db/di 写入参数等待进一步核对。
- GDS 只包含平面空气孔图形；slab 厚度和折射率写入 JSON/README，供 COMSOL/Lumerical 建模使用。

## 后续导入建议

### KLayout

直接打开 `.gds`，检查 layer/datatype、孔径、中心五重对称结构和总尺寸。

### COMSOL

将 GDS 导入为二维几何后，按论文设置折射率 n=3.33；如做 3D slab，需要额外设置 slab thickness。

### Lumerical

可将 GDS 作为 mask 导入，再将空气孔区域设为 air，背景 slab 设为目标材料。
