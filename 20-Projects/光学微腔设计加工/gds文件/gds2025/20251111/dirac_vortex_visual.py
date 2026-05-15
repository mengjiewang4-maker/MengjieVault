import gdsfactory as gf
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 基本参数设置（单位：微米）
# ============================================
a = 0.49             # 晶格常数 490 nm
r_hole = 0.32 * a     # 三角孔外接圆半径
m0 = 0.05             # 最大偏移量（对应 50 nm）
R = 5 * a             # 调制半径
alpha = 4             # 调制陡峭度
w = +1                # 拓扑绕数 (+1逆时针，-1顺时针)
Nx, Ny = 20, 20       # 晶格范围（越大越慢）

# 创建GDSfactory cell
c = gf.Component("dirac_vortex_cavity_um")

# ============================================
# 定义三角孔形状
# ============================================
def triangle(radius, rotation_deg=0):
    pts = []
    for i in range(3):
        theta = np.deg2rad(rotation_deg + i * 120)
        pts.append((radius * np.cos(theta), radius * np.sin(theta)))
    return np.array(pts)

# ============================================
# 定义Kekulé调制（Dirac-vortex）
# ============================================
def vortex_shift(x, y):
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    amplitude = m0 * np.tanh((r / R) ** alpha)
    dx = amplitude * np.cos(w * phi)
    dy = amplitude * np.sin(w * phi)
    return dx, dy

# ============================================
# 绘制蜂窝晶格
# ============================================
all_x, all_y = [], []

for i in range(-Nx, Nx):
    for j in range(-Ny, Ny):
        x0 = a * (i + 0.5 * (j % 2))
        y0 = np.sqrt(3)/2 * a * j

        # honeycomb两子晶格
        if (i + j) % 2 == 0:
            dx, dy = 0, 0  # A子晶格不调制
        else:
            dx, dy = vortex_shift(x0, y0)  # B子晶格调制

        # 绘制三角孔
        tri = triangle(r_hole, rotation_deg=30)
        tri = tri + np.array([x0 + dx, y0 + dy])
        c.add_polygon(tri, layer=(1, 0))

        # 收集用于可视化
        all_x.append(x0 + dx)
        all_y.append(y0 + dy)

# ============================================
# 输出GDS文件
# ============================================
c.write_gds("dirac_vortex_visual.gds")
print("✅ GDS 文件已生成：dirac_vortex_phc_um.gds")

# ============================================
# 可视化展示（matplotlib）
# ============================================
plt.figure(figsize=(7, 7))
# ============================================
# 相位分布可视化 (Dirac-vortex phase map)
# ============================================
x_arr = np.array(all_x)
y_arr = np.array(all_y)
r = np.sqrt(x_arr**2 + y_arr**2)
phi = np.arctan2(y_arr, x_arr)
# Dirac-vortex复质量相位
phase = (w * phi) % (2 * np.pi)

plt.figure(figsize=(7, 7))
sc = plt.scatter(x_arr, y_arr, c=phase, cmap='twilight_shifted', s=12, edgecolors='none')
plt.gca().set_aspect('equal')
plt.title("Dirac-Vortex Phase Field ϕ(r) (units: µm)")
plt.xlabel("x (µm)")
plt.ylabel("y (µm)")
plt.colorbar(sc, label="Phase (radians)")
plt.tight_layout()
plt.show()

