from geometry_generator import generate_structure, remove_sector
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