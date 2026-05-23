# Disclination GDS Project

本项目是一个规范化的科研 Python/GDS 项目骨架，用于后续整理 disclination 结构的几何生成、GDS 导出、Dose matrix 和实验记录。

## 当前主入口

`scripts/generate_disclination_gds.py`

这个脚本默认只做 dry-run，也就是只打印参数和输出路径，不真正写 GDS。需要真正写文件时显式加 `--write`。

Fig.2 d/e/f 复现入口：

`scripts/disclination_fig2_def_gds.py`

该脚本使用 `klayout.db` 生成 C5 added-quarter-sector photonic disclination cavity，对应论文 Fig.2f 的几何；Fig.2d/e 是 TB 结果，不是独立 GDS 几何。

## 项目结构

```text
disclination/
├── README.md
├── environment.yml
├── scripts/
│   └── generate_disclination_gds.py
├── src/
│   └── disclination/
│       ├── __init__.py
│       ├── geometry.py
│       ├── gds_export.py
│       └── dose_matrix.py
├── outputs/
│   ├── gds/
│   ├── png/
│   └── mapping/
└── docs/
    ├── 参数表.md
    ├── 运行记录.md
    └── GDS文件对应表.md
```

## 输入

- `docs/参数表.md`
- 后续可加入论文参数、SEM 反馈、Dose/PEC 区域表

## 输出

- `outputs/gds/`：GDS 文件
- `outputs/png/`：版图预览图或分析图
- `outputs/mapping/`：Python -> GDS、GDS -> 参数、GDS -> Dose/PEC 对应表

## 运行方式

先进入项目目录：

```bash
cd /Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/disclination
```

试运行，不写 GDS：

```bash
python scripts/generate_disclination_gds.py
```

真正写出示例 GDS：

```bash
python scripts/generate_disclination_gds.py --write
```

生成 Fig.2 d/e/f 对应 C5 结构：

```bash
MPLCONFIGDIR=/private/tmp/matplotlib /Users/mac/miniconda3/bin/python3 scripts/disclination_fig2_def_gds.py
```

用新 GDS 孔位中心做局域 TB 检查：

```bash
MPLCONFIGDIR=/private/tmp/matplotlib /Users/mac/miniconda3/bin/python3 scripts/tb_from_fig2_gds_sites.py
```

## 设计原则

- `scripts/` 只放可运行入口。
- `src/disclination/` 只放模块，也就是被入口调用的函数。
- 模块不要偷偷写文件，只有 `write_*` 或 `export_*` 函数才写文件。
- 输出文件如果已经存在，默认报错，不覆盖。
- 每次真正用于 EBL 的 GDS，必须在 `docs/GDS文件对应表.md` 里记录对应脚本和参数。

## 当前状态

这是项目骨架，不是最终 EBL 版图生成代码。后续应把已经验证过的 disclination 几何参数和 GDS 生成逻辑逐步迁移进来。
