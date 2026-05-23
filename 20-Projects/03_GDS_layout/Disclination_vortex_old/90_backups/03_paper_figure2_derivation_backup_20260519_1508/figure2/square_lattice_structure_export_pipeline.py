"""
串联几何生成、旋错裁剪、可视化和仿真文件导出，是根目录简化流程入口。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

from square_lattice_volterra_sector_geometry import generate_structure, remove_sector
from visualize import plot_structure
from export_comsol import export_csv
from export_lumerical import export_lsf
import numpy as np

print("mode found")

# 生成 lattice
positions = generate_structure(10,10,500)

# 删除扇形区域（disclination）
positions = remove_sector(positions,np.pi/3)

# 画结构
plot_structure(positions)

# 导出
export_csv(positions)
export_lsf(positions)
