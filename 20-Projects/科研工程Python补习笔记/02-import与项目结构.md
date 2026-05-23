# 02-import 与项目结构

`import` 是读懂多文件 Python 工程的核心。

一句话理解：

> `import xxx` 就是让当前文件使用另一个文件、包或第三方库里的代码。

## Python 会去哪里找 import

当你写：

```python
import geometry
```

Python 会在一些路径里找 `geometry.py` 或 `geometry/` 包。

最常见的查找位置：

1. 当前运行命令所在目录
2. 当前环境安装的第三方库
3. `PYTHONPATH` 里指定的路径
4. 标准库路径

关键点：Python 不一定按“这个脚本所在目录”找，而是经常按“你从哪里运行命令”找。

## 为什么同一个脚本有时能跑，有时不能跑

假设项目结构：

```text
project/
├── geometry.py
└── scripts/
    └── run.py
```

`run.py` 里写：

```python
import geometry
```

如果你在 `project/` 目录运行：

```bash
python scripts/run.py
```

可能能找到 `geometry.py`。

如果你在 `scripts/` 目录运行：

```bash
python run.py
```

就可能找不到，因为当前目录变成了 `scripts/`。

## `import x` 和 `from x import y`

```python
import geometry
```

表示导入整个模块，使用时写：

```python
geometry.build_lattice()
```

```python
from geometry import build_lattice
```

表示只导入某个函数，使用时直接写：

```python
build_lattice()
```

## 相对导入

```python
from .geometry import build_lattice
```

开头的点 `.` 表示“从当前包里找”。

这通常要求项目是一个包，并且用类似下面的方式运行：

```bash
python -m package_name.script_name
```

科研项目里经常不用包结构，所以相对导入容易报错。

## 常见混乱来源

| 混乱来源 | 表现 |
|---|---|
| 从错误目录运行脚本 | `ModuleNotFoundError` |
| 文件被移动后 import 没改 | 找不到旧模块 |
| 文件名和第三方库重名 | 导入了错误文件 |
| 没有 `__init__.py` | 文件夹不能按包导入 |
| notebook 和 py 混用 | notebook 的工作目录和 py 不一致 |

## 快速查看 import

```bash
rg -n "^import |^from .* import" .
```

只看项目内部 import：

```bash
find . -name "*.py" | sed "s#.*/##; s#.py$##" | sort
```

然后对照 `rg` 输出，看哪些 import 名称和项目内文件同名。

## 建议习惯

对于科研工程，尽量固定一种运行方式：

```bash
cd project_root
python scripts/generate_gds.py
```

不要一会儿从根目录运行，一会儿进入子目录运行。

