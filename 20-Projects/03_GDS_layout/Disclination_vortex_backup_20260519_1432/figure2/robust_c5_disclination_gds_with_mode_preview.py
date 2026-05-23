"""
生成稳健版 C5 旋错空气孔 GDS，尝试合并重叠孔并预览局域模强度。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import gdspy
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from pathlib import Path
ROOT = Path(__file__).resolve().parent

# ==========================================
# 1. 参数设置 (nm)
# ==========================================
a = 400.0          
target_n = 5       
delta = 0.10 * a   
r_hole = 0.12 * a  # 48nm, 必然重合
Nx, Ny = 10, 10    

# ==========================================
# 2. 构建旋错几何坐标
# ==========================================
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        basis = np.array([
            [cx-delta, cy-delta], [cx+delta, cy-delta],
            [cx-delta, cy+delta], [cx+delta, cy+delta]
        ])
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

coeff = (360.0 / target_n) / 90.0
stretched_unit = []
for x, y in q1_pos:
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
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-2) * a]

# ==========================================
# 3. 极速求解 (TB Model)
# ==========================================
num = len(pos)
H = np.zeros((num, num), dtype=complex)
for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        if r < 0.5: H[i, j] = H[j, i] = -1.5
        elif r < 2*delta*1.1: H[i, j] = H[j, i] = -1.0
        elif r < a * 1.2: H[i, j] = H[j, i] = -0.1
E, V = np.linalg.eigh(H)
target_idx = np.argmax(np.sum(np.abs(V)**4, axis=0))
mode_intensity = np.abs(V[:, target_idx])**2 / np.max(np.abs(V[:, target_idx])**2)

# ==========================================
# 4. 稳健版 GDS 导出 (解决崩溃关键)
# ==========================================
# 重置 gdspy 内部状态
gdspy.current_library = gdspy.GdsLibrary()

lib = gdspy.GdsLibrary()
cell = lib.new_cell('FINAL_CAVITY')
unit_conv = 1e-3 # nm -> um

print("正在生成几何形状...")

# 策略：不直接使用 gdspy.boolean，而是通过多边形集合管理
# 减少边数到 24 (对于 96nm 的孔，24 边形在加工中已经足够圆润)
poly_list = []
for p in pos:
    # 直接生成多边形顶点，不使用 Round 对象以减少元数据开销
    circle_poly = gdspy.Round(
        (p[0] * unit_conv, p[1] * unit_conv),
        r_hole * unit_conv,
        number_of_points=24,
        layer=1
    )
    poly_list.append(circle_poly)

# 将所有多边形添加到一个 PolygonSet 中
# PolygonSet 会在写入 GDS 时自动处理某些几何连接，但不会强行执行昂贵的布尔运算
ps = gdspy.PolygonSet(
    [p.polygons[0] for p in poly_list], 
    layer=1
)

# 如果你仍然需要合并重合孔（为了减少 KLayout 压力），使用这个轻量化合并：
try:
    print("正在尝试合并重叠孔（优化 GDS）...")
    # 'max_points' 设置可以防止生成过于复杂的多边形
    merged = gdspy.boolean(ps, None, 'or', layer=1, max_points=199)
    cell.add(merged)
except Exception as e:
    print(f"合并失败 ({e})，将使用原始重叠图层导出以防止崩溃。")
    cell.add(ps)

file_name = 'robust_disclination.gds'
gds_path = ROOT / file_name
gds_path.parent.mkdir(parents=True, exist_ok=True)
lib.write_gds(str(gds_path))
print("GDS saved:", gds_path.resolve())
print(f"--- 导出完成！--- \n文件名: {file_name}\n总孔数: {len(pos)}")

# ==========================================
# 5. 快速预览
# ==========================================
plt.figure(figsize=(6,6))
plt.scatter(pos[:,0], pos[:,1], s=5, c=mode_intensity, cmap='hot')
plt.title("Physics Preview (Intensity)")
plt.gca().set_aspect('equal')
plt.show()