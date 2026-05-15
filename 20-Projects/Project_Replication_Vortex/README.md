# Project Replication Vortex

这个目录用于把 disclination vortex 结构生成成 GDS 版图文件。

术语说明：

- GDS：芯片/纳米加工常用的版图文件格式，可以用 KLayout 打开。
- lattice constant `a`：晶格常数，单位是 um，决定整体结构缩放。
- air hole radius `r_hole`：空气孔半径，单位是 um。文件名里的 `r0p111`、`r0p112`、`r0p084` 是实际孔半径，不是比例。
- `r_ratio`：孔半径比例，脚本中用 `r_hole = r_ratio * a` 计算。
- `R`：六边形晶格半径，单位是晶格格点数，不是物理长度。

## 文件说明

- `disclination_vortex_gds.py`：当前用于批量生成 disclination vortex GDS 的脚本。
- `disclination_vortex_1.ipynb`：早期 notebook 推导和画图记录。
- `gds_template_1.py`：早期三角孔 vortex GDS 参考模板，不是最新这批圆孔文件的主生成脚本。
- `environment.yml`：conda 环境定义。
- `output/`：生成出来的 GDS 文件。

## 曝光用 GDS 参数

按文件修改时间看，当前曝光用 GDS 是在 `2026-04-20 18:03` 生成的 6 个文件，来源于 `disclination_vortex_gds.py`。文件名已统一改成 `mj+日期+序号`，例如 `mj20260420_01.gds`。

| 序号 | 曝光用文件 | 原始文件名 | R | a (um) | a (nm) | r_ratio | r_hole (um) | r_hole (nm) | GDS 内文字标记 | 说明 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 01 | `output/mj20260420_01.gds` | `output/wmj20260420disc_R60_a0p554_r0p111.gds` | 60 | 0.554 | 554 | 0.20 | 0.1108 | 110.8 | `a0p554_r0p111` | 大尺寸版本 |
| 02 | `output/mj20260420_02.gds` | `output/wmj20260420disc_R30_a0p554_r0p111.gds` | 30 | 0.554 | 554 | 0.20 | 0.1108 | 110.8 | `a0p554_r0p111` | 半径减半版本 |
| 03 | `output/mj20260420_03.gds` | `output/wmj20260420disc_R60_a0p559_r0p112.gds` | 60 | 0.559 | 559 | 0.20 | 0.1118 | 111.8 | `a0p559_r0p112` | 大尺寸版本 |
| 04 | `output/mj20260420_04.gds` | `output/wmj20260420disc_R30_a0p559_r0p112.gds` | 30 | 0.559 | 559 | 0.20 | 0.1118 | 111.8 | `a0p559_r0p112` | 半径减半版本 |
| 05 | `output/mj20260420_05.gds` | `output/wmj20260420disc_R60_a0p559_r0p084.gds` | 60 | 0.559 | 559 | 0.15 | 0.08385 | 83.85 | `a0p559_r0p084` | 大尺寸、小孔版本 |
| 06 | `output/mj20260420_06.gds` | `output/wmj20260420disc_R30_a0p559_r0p084.gds` | 30 | 0.559 | 559 | 0.15 | 0.08385 | 83.85 | `a0p559_r0p084` | 半径减半、小孔版本 |

这一批参数单位统一按 um 记录。脚本设置了 `ly.dbu = 0.001`，在 KLayout 中表示 1 个数据库单位是 0.001 um。`r_ratio` 是空气孔比例，计算方式是 `r_hole / a`。

## 固定生成参数

`disclination_vortex_gds.py` 中这批文件共用以下固定参数：

| 参数 | 当前值 | 含义 |
| --- | ---: | --- |
| `sample_name` | `DISCLINATION_VORTEX` | GDS 顶层 cell 名称 |
| `n_vertex` | 256 | 每个圆形空气孔用 256 个多边形顶点近似 |
| `eps` | 0.001 | 角度裁剪容差 |
| `angle_ratio` | 6/5 | disclination 角度重映射比例 |
| `radius_ratio` | 6/5 | disclination 半径重映射比例 |
| `layer` | `(1, 0)` | GDS 图层/datatype |
| `dbu` | 0.001 | GDS 数据库单位 |

空气孔数量由 `R` 决定：

| R | 原始晶格点数 | disclination 后空气孔数，不含文字标识 |
| ---: | ---: | ---: |
| 60 | 84966 | 70805 |
| 30 | 20886 | 17405 |

## 文件名规则

脚本使用当天日期自动命名：

```text
output/mjYYYYMMDD_{seq}.gds
```

其中：

- `YYYYMMDD` 是生成日期。
- `seq` 是两位序号，从 `01` 开始。
- 每组参数会同时生成 `R = 60` 和 `R = 30` 两个版本，先生成 `R = 60`，再生成 `R = 30`。
- GDS 里还会在图案上方写入参数文字，例如 `a0p559_r0p112`。
- README 中的“曝光用 GDS 参数”表是送曝光时的参数索引，不要只依赖短文件名判断版图参数。

## 环境配置

首次使用时创建 conda 环境：

```bash
cd /Users/mac/Documents/mengjie/MengjieVault/20-Projects/Project_Replication_Vortex
conda env create -f environment.yml
```

运行前激活环境：

```bash
conda activate project_vortex_layout
```

检查 `klayout.db` 是否可用：

```bash
python -c "import klayout.db; print('klayout ok')"
```

## 重新生成

在项目目录中运行：

```bash
python disclination_vortex_gds.py
```

如果只想改孔径或晶格常数，优先修改脚本开头的 `PARAM_SETS`：

```python
PARAM_SETS = [
    {"a": 0.554, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.15},
]
```

如果要改版图尺寸，修改脚本开头的 `R`。脚本会自动额外生成一个 `R // 2` 的半径减半版本。

## 注意事项

- 当前 `mj20260420_01` 到 `mj20260420_06` 是圆形空气孔 disclination vortex；早期 `vortex230/vortex260` 文件来自旧命名和旧流程，不要和这批参数混用。
- `output/` 里的 GDS 文件较大，建议保留最终需要送工艺或检查的版本即可。
- 修改参数后重新运行会按当前日期生成新文件，不会自动覆盖旧日期文件。
