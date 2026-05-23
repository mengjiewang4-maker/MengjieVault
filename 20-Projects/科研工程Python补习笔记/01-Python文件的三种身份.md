# 01-Python 文件的三种身份

一个 `.py` 文件通常有三种身份：

1. 主程序
2. 模块
3. 包的一部分

读陌生项目时，第一件事不是看懂每一行代码，而是判断这个文件属于哪一种。

## 1. 主程序

主程序就是“入口文件”，通常可以直接运行：

```bash
python run.py
python generate_gds.py
python main.py
```

主程序常见特征：

- 文件名像 `main.py`、`run.py`、`generate_*.py`、`export_*.py`
- 代码里有实际执行步骤
- 会读取参数、生成图、导出 GDS/CSV/PNG
- 可能包含 `if __name__ == "__main__"`

典型结构：

```python
def main():
    generate_layout()
    save_gds("output.gds")


if __name__ == "__main__":
    main()
```

## 2. 模块

模块就是“工具文件”或“函数库文件”，通常被别的 `.py` 调用。

模块常见特征：

- 主要内容是 `def` 函数或 `class` 类
- 自己不直接生成结果
- 文件名像 `geometry.py`、`solver.py`、`utils.py`、`plotting.py`

例子：

```python
def build_lattice(a, nx, ny):
    ...


def solve_mode(H):
    ...
```

这种文件通常不是第一入口。它更像实验室里的工具箱。

## 3. 包

包是一个文件夹，里面放多个模块。

例如：

```text
project/
├── photonic_gds/
│   ├── __init__.py
│   ├── geometry.py
│   ├── export.py
│   └── dose_matrix.py
└── scripts/
    └── generate_batch13.py
```

其中 `photonic_gds/` 就是包。

`__init__.py` 的作用是告诉 Python：这个文件夹可以作为包被导入。

## 重点：`if __name__ == "__main__"`

这句代码是判断“当前文件是被直接运行，还是被别人导入”。

```python
if __name__ == "__main__":
    main()
```

意思是：

- 如果你运行 `python this_file.py`，就执行 `main()`
- 如果别的文件 `import this_file`，就不执行 `main()`

## 为什么这很重要

没有这个保护时，导入一个文件可能会立刻执行它的顶层代码。

危险例子：

```python
import gdspy

lib = gdspy.GdsLibrary()
lib.write_gds("test.gds")
```

这个文件如果被别人 `import`，也会直接写出 `test.gds`。

更好的写法：

```python
import gdspy


def main():
    lib = gdspy.GdsLibrary()
    lib.write_gds("test.gds")


if __name__ == "__main__":
    main()
```

## 3 分钟判断法

打开一个 `.py` 文件，先看：

1. 有没有 `if __name__ == "__main__"`？
2. 有没有很多顶层代码，例如 `plt.show()`、`write_gds()`、`np.savetxt()`？
3. 文件里主要是 `def`/`class`，还是直接执行？
4. 有没有被其他文件 `import`？

判断规则：

| 现象 | 判断 |
|---|---|
| 有 `main()` 和 `if __name__ == "__main__"` | 标准主程序 |
| 没有 main，但顶层直接画图/导出文件 | 可运行脚本 |
| 基本都是函数和类 | 模块 |
| 文件夹里有多个 py 和 `__init__.py` | 包 |

