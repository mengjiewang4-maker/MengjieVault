"""
降低点数和阵列规模，生成更稳定、更容易打开的旋错 GDS。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import gdspy

from pathlib import Path
ROOT = Path(__file__).resolve().parent

# ==========================================
# 1. 降低参数负载 (确保能打开)
# ==========================================
a = 400.0          
target_n = 5       
delta = 0.10 * a   
r_hole = 0.2 * a  # 稍微减小半径，减少重合产生的极细碎碎片
Nx, Ny = 8, 8      # 降低阵列规模

# ==========================================
# 2. 坐标生成
# ==========================================
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        basis = np.array([[cx-delta, cy-delta], [cx+delta, cy-delta],
                          [cx-delta, cy+delta], [cx+delta, cy+delta]])
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)

coeff = (360.0 / target_n) / 90.0
# 极坐标变换
stretched = np.array([[np.sqrt(x**2+y**2), np.arctan2(y,x)*coeff] for x,y in q1_atoms])
stretched_pos = np.array([[r*np.cos(p), r*np.sin(p)] for r,p in stretched])

final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_pos @ rot.T)

pos = np.array(final_pos)
# 裁剪边缘
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-1.5) * a]

# ==========================================
# 3. 关键修复：禁用合并，极低点数，强制清除缓存
# ==========================================
# 彻底重置 gdspy 状态，防止旧数据干扰
gdspy.current_library = gdspy.GdsLibrary()

lib = gdspy.GdsLibrary(unit=1e-6, precision=1e-9) # 显式定义单位
cell = lib.new_cell('STABLE_CELL')

print(f"正在处理 {len(pos)} 个空气孔...")

# 核心策略：
# 1. 绝对不要使用 gdspy.boolean。
# 2. number_of_points 降低到 12 (对于 100nm 以下的孔，12 边形足够了)。
# 3. 分批添加到 cell。

for p in pos:
    # 直接以 um 为单位计算
    hole = gdspy.Round(
        (p[0] * 1e-3, p[1] * 1e-3),
        r_hole * 1e-3,
        number_of_points=12,
        layer=1
    )
    cell.add(hole)

file_name = 'fixed_layout.gds'
gds_path = ROOT / file_name
gds_path.parent.mkdir(parents=True, exist_ok=True)
lib.write_gds(str(gds_path))
print("GDS saved:", gds_path.resolve())
print(f"--- 导出成功！ ---")
print(f"文件名: {file_name}")