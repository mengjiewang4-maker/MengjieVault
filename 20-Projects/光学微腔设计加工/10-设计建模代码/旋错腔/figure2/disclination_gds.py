import numpy as np
import gdspy  # 用于导出 GDSII 格式

# ==========================================
# 1. 物理参数设置 (单位: nm)
# ==========================================
a = 0.400          # 晶格常数 (400nm)
target_n = 5       # C5 对称性旋错
delta = 0.12 * a   # 位移量 (48nm)
r_hole = 0.2 * a  # 空气孔半径 (40nm)

Nx, Ny = 10, 10    # 尺寸规模

# 计算关键加工参数
d_intra = 2 * delta
d_inter = a - 2 * delta
min_bridge = d_intra - 2 * r_hole

print(f"--- 结构参数 (nm) ---")
print(f"晶格常数 a: {a}")
print(f"孔半径 r: {r_hole} (直径 {2*r_hole})")
print(f"胞内中心距: {d_intra}")
print(f"最小壁厚 (Bridge): {min_bridge}")

if min_bridge < 10:
    print("⚠️ 警告: 最小壁厚过小，加工极难！建议减小 r_hole 或增大 delta。")

# ==========================================
# 2. 构建旋错几何坐标 (算法逻辑同前)
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
# 截断边缘，保持圆形区域
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-2) * a]

# ==========================================
# 3. 生成 GDSII 文件
# ==========================================
# 创建一个 GDSII 库，单位为微米 (1e-6)，精度为纳米 (1e-9)
# 注意：gdspy 默认单位通常是微米，所以我们要把 nm 转换为 um
unit_conv = 1e-3 
lib = gdspy.GdsLibrary()
cell = lib.new_cell('DISCLINATION_CAVITY')

# 定义层号 (Layer 1, Datatype 0)
ld_layer = 1

# 在每个坐标处生成圆孔 (Round 是多边形近似)
# number_of_points 决定圆的平滑度，通常 64 或 128 足够
for p in pos:
    hole = gdspy.Round(
        (p[0] * unit_conv, p[1] * unit_conv), # 中心坐标 (um)
        r_hole * unit_conv,                  # 半径 (um)
        layer=ld_layer,
        number_of_points=64
    )
    cell.add(hole)

# 保存文件
file_name = f'disclination_C{target_n}_a{int(a)}.gds'
lib.write_gds(file_name)

print(f"--- GDS 导出成功 ---")
print(f"文件名: {file_name}")
print(f"总孔数: {len(pos)}")

# ==========================================
# 4. 简易预览 (Matplotlib)
# ==========================================
import matplotlib.pyplot as plt
plt.figure(figsize=(6,6))
plt.scatter(pos[:,0], pos[:,1], s=10, c='blue', alpha=0.6)
plt.gca().set_aspect('equal')
plt.title(f"GDS Preview (a={a}nm, C{target_n})")
plt.xlabel("x (nm)")
plt.ylabel("y (nm)")
plt.show()