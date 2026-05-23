# 05-ModuleNotFoundError 排查

错误形式：

```text
ModuleNotFoundError: No module named 'xxx'
```

意思是：Python 在当前搜索路径里找不到 `xxx`。

## 先判断 xxx 是什么

| xxx 类型 | 例子 | 处理方式 |
|---|---|---|
| 第三方库 | `numpy`, `gdspy`, `scipy` | 安装环境 |
| 项目内部文件 | `geometry`, `export_gds` | 检查运行目录和文件位置 |
| 已经不存在的历史模块 | `find_modes`, `vortex_detector` | 查旧版本或标记为缺失 |

## 第一步：项目里有没有这个文件

```bash
find . -name "xxx.py"
find . -type d -name "xxx"
```

如果找不到，说明它不是当前项目里的文件。

## 第二步：是不是第三方库没装

```bash
python -c "import xxx; print(xxx.__file__)"
```

如果报错，说明当前 Python 环境没有这个库。

常见安装：

```bash
pip install gdspy
pip install scipy
pip install pythtb
```

但科研项目最好先看有没有：

```text
requirements.txt
environment.yml
pyproject.toml
```

## 第三步：是不是运行目录错了

查看当前位置：

```bash
pwd
```

推荐从项目根目录运行：

```bash
cd project_root
python path/to/script.py
```

不要随便进入脚本所在子目录运行，除非 README 明确要求。

## 第四步：打印 Python 搜索路径

```bash
python - <<'PY'
import sys
for p in sys.path:
    print(p)
PY
```

`sys.path` 就是 Python 找模块的路径列表。

## 第五步：文件名是否冲突

不要把自己的文件命名为：

```text
numpy.py
matplotlib.py
gdspy.py
scipy.py
pathlib.py
```

否则 Python 可能优先导入你的文件，而不是第三方库。

## 临时解决办法

可以临时设置 `PYTHONPATH`：

```bash
PYTHONPATH=. python scripts/run.py
```

意思是把当前目录加入 Python 搜索路径。

这适合临时排查，不建议长期依赖。

## 最稳妥的工程解决

把项目整理成：

```text
project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── geometry.py
│       └── export.py
└── scripts/
    └── generate.py
```

然后脚本中写：

```python
from my_project.geometry import build_lattice
```

