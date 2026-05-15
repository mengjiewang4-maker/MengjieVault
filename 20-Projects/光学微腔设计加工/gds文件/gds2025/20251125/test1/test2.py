# -*- coding: utf-8 -*-
# 正确导入：导入 gdsCAD 的 core 子模块（真正包含 Cell 类的模块）
from gdsCAD import core
# 若需要用到 shapes（如矩形、多边形），也需正确导入
from gdsCAD import shapes

# ----------------------
# 你的原有绘图逻辑（保留不变）
# ----------------------
# 示例：如果你的代码是创建蜂窝晶格，这里替换为你的实际代码
# 以下是模拟的蜂窝晶格绘制逻辑（如果你的代码不同，保持你的核心绘图部分）
top = core.Cell('TOP')
example = core.Cell('EXAMPLE')
cont_algn = core.Cell('CONT_ALGN')

# 假设你添加了蜂窝晶格的图形（比如多边形、线条等）
# 这里用简单图形示例，替换为你的实际绘图代码
hexagon = core.shapes.Polygon([(0,0), (5,10), (15,10), (20,0), (15,-10), (5,-10)])
example.add(hexagon)
top.add(core.Reference(example))  # 引用示例单元格到 TOP

# ----------------------
# 仅保存 GDS 文件（删除 show()）
# ----------------------
layout = core.GdsLibrary()
layout.add_cell(top)
layout.add_cell(example)
layout.add_cell(cont_algn)

# 保存 GDS 文件到脚本所在目录（文件名可自定义）
output_path = '/Users/mac/mengjie/honeycomb lattice/20251125/test1/honeycomb_lattice.gds'
layout.write_gds(output_path)

print("✅ GDS 文件生成成功！")
print("📁 文件路径：%s" % output_path)