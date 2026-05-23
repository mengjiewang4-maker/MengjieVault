# 08-自己搭建规范科研 Python 项目

目标不是做大型软件，而是让未来的自己能看懂、能复现、能追踪实验。

## 推荐结构

```text
project/
├── README.md
├── environment.yml
├── scripts/
│   └── generate_batch13_gds.py
├── src/
│   └── project_name/
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
    └── 运行记录.md
```

## 脚本和模块分开

`scripts/` 放可运行入口：

```python
from project_name.geometry import build_lattice
from project_name.gds_export import write_gds


def main():
    holes = build_lattice()
    write_gds(holes, "outputs/gds/test.gds")


if __name__ == "__main__":
    main()
```

`src/project_name/` 放模块：

```python
def build_lattice():
    ...
```

模块不要偷偷写文件，除非函数名明确叫 `write_*` 或 `export_*`。

## 每个入口脚本必须输出运行信息

建议最少输出：

```python
print("Start generate_batch13_gds")
print(f"Output directory: {out_dir}")
print(f"GDS count: {len(gds_files)}")
print("Done")
```

## 不要覆盖旧结果

输出文件建议带日期或版本：

```text
batch13_20260519_GDS01_D25_PEC_ON.gds
```

如果已存在：

```python
if path.exists():
    raise FileExistsError(path)
```

科研数据宁可多一个文件，也不要覆盖原始结果。

## README 至少写什么

```markdown
# 项目名

## 当前主入口

`scripts/generate_batch13_gds.py`

## 输入

- 参数表
- 参考 GDS

## 输出

- `outputs/gds/`
- `outputs/mapping/`

## 运行方式

```bash
cd project
python scripts/generate_batch13_gds.py
```
```

## 对 GDS/EBL 项目的额外建议

每次真正用于 EBL 的 GDS 必须记录：

- 样品编号
- GDS 文件名
- 生成脚本
- commit 或日期
- 周期
- 孔径/线宽
- 阵列尺寸
- dose
- PEC
- SEM 文件名

