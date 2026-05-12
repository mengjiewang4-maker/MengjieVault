# Project Replication Vortex

## 项目文件 | Files

- `disclination_vortex_1.ipynb`: 原始 notebook 画图逻辑 | Original plotting logic in notebook form
- `gds_template_1.py`: GDS 参考模板 | Reference GDS template
- `disclination_vortex_gds.py`: 当前用于生成 GDS 的脚本 | Current script for generating the GDS layouts
- `environment.yml`: 本项目的 conda 环境定义文件 | Conda environment definition for this project

## 环境配置 | Environment Setup

首次使用时创建项目环境 | Create the project environment once:

```bash
cd /Users/mac/Documents/mengjie/codex_job/工作区/Project_Replication_Vortex
conda env create -f environment.yml
```

运行脚本前激活环境 | Activate the environment before running the script:

```bash
conda activate project_vortex_layout
```

## 运行方法 | Run

生成 GDS 文件 | Generate the GDS files:

```bash
python disclination_vortex_gds.py
```

当前输出文件 | Current output files:

- 输出目录：`output/`
- `output/wmjYYYYMMDDvortex260.gds`: `R = 60` 的版图 | Layout with `R = 60`
- `output/wmjYYYYMMDDvortex230.gds`: `R = 30` 的版图 | Layout with `R = 30`
- `output/wmjYYYYMMDDvortex260_half.gds` 或同类变体：辅助版图输出 | Auxiliary layout variant when generated

`gds_template_1.py` 生成的参考文件也会写入 `output/`。

## 环境检查 | Verify Python Environment

检查当前项目使用的 Python 路径 | Check that the project is using the expected Python:

```bash
python -c "import sys; print(sys.executable)"
```

检查 `klayout.db` 是否可用 | Check that `klayout.db` is available:

```bash
python -c "import klayout.db; print('klayout ok')"
```

## 说明 | Notes

- 本项目建议使用 conda 环境 `project_vortex_layout` | This project should use the conda environment `project_vortex_layout`
- 不要依赖系统自带 Python 运行本项目 | Do not rely on the system Python for this project
- GDS 输出中的空气孔通过 `klayout.db` 的 ellipse 接口生成 | The GDS output uses circular air holes via `klayout.db` ellipse generation
- 当前统一将 GDS 产物写入 `output/`，避免和源码混放 | GDS artifacts are now written to `output/` to keep sources and outputs separate
