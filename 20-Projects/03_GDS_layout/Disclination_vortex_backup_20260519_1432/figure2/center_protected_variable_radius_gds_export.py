"""
在旋错核心附近缩小空气孔半径，减少中心区域刻穿或孔重叠风险。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import gdspy

from pathlib import Path
ROOT = Path(__file__).resolve().parent

# ==========================================
# 1. 物理参数设置 (单位: nm)
# ==========================================
a = 400.0          
target_n = 5       
delta = 0.10 * a   # 40nm
r_hole_base = 0.12 * a  # 基础半径 48nm

# --- 防刻穿调制参数 ---
# 减小中心孔的比例 (例如 0.8 表示中心孔半径变为原来的 80%)
center_r_scale = 0.75  
# 调制影响的半径范围 (单位: nm, 建议 1.5a 到 2.0a)
protection_zone = 1.8 * a 

Nx, Ny = 10, 10    

# ==========================================
# 2. 坐标生成 (保持逻辑一致)
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
stretched_unit = []
for x, y in q1_atoms:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * coeff
    stretched_unit.append([r * np.cos(phi), r * np.sin(phi)])
stretched_unit = np.array(stretched_unit)

final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_unit @ rot.T)

pos = np.array(final_pos)
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-1.5) * a]

# ==========================================
# 3. 稳健导出：带局部半径调控 (GDS 导出)
# ==========================================
gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()
cell = lib.new_cell('PROTECTED_CAVITY')
unit_conv = 1e-3 

print("正在计算变半径孔并导出 GDS...")

for p in pos:
    r_dist = np.linalg.norm(p)
    
    # --- 半径调制逻辑 ---
    # 如果在保护区内，半径根据距离线性平滑缩小
    if r_dist < protection_zone:
        # 计算缩放因子：从中心 center_r_scale 线性过渡到 1.0
        scale = center_r_scale + (1.0 - center_r_scale) * (r_dist / protection_zone)
        current_r = r_hole_base * scale
    else:
        current_r = r_hole_base
    
    # 导出圆孔 (使用低点数确保 Windows/Mac 都能打开)
    hole = gdspy.Round(
        (p[0] * unit_conv, p[1] * unit_conv),
        current_r * unit_conv,
        number_of_points=16, 
        layer=1
    )
    cell.add(hole)

file_name = 'center_protected_a400.gds'
gds_path = ROOT / file_name
gds_path.parent.mkdir(parents=True, exist_ok=True)
lib.write_gds(str(gds_path))
print("GDS saved:", gds_path.resolve())
print(f"--- 导出成功！ ---")
print(f"文件名: {file_name}")
print(f"中心孔半径已缩小至: {r_hole_base * center_r_scale:.2f} nm")