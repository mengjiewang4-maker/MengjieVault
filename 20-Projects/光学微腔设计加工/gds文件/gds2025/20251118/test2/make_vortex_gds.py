import gdsfactory as gf
import numpy as np
import matplotlib.pyplot as plt
import os

# ======================================
# 参数设置（与你之前保持一致）
# ======================================
a = 0.490
hole_radius = 0.32 * a
m0 = 0.050
R_vortex = 25.0
alpha = 4.0
w = 1
device_diameter = 80.0

# ======================================
# 三角形模板（外接圆半径）
# ======================================
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1]
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_pts = list(zip(x_tri, y_tri))

# 三类三角形元件：红(1)、绿(2)、蓝(3)
triR = gf.Component("Tri_R")
triR.add_polygon(triangle_pts, layer=(1, 0))

triG = gf.Component("Tri_G")
triG.add_polygon(triangle_pts, layer=(2, 0))

triB = gf.Component("Tri_B")
triB.add_polygon(triangle_pts, layer=(3, 0))

tri_list = [triR, triG, triB]


# ======================================
# 生成蜂巢晶格坐标
# ======================================
N_grid = int(device_diameter / a * 1.2)
i_range = np.arange(-N_grid, N_grid)
j_range = np.arange(-N_grid, N_grid)
XX, YY = np.meshgrid(i_range, j_range)

x_grid = XX * a + YY * a * 0.5
y_grid = YY * a * np.sqrt(3) / 2

x_flat = x_grid.flatten()
y_flat = y_grid.flatten()

mask = (x_flat**2 + y_flat**2) < (device_diameter / 2)**2
x_valid = x_flat[mask]
y_valid = y_flat[mask]

print(f"有效晶格点数量: {len(x_valid)}")

# Kekulé 三相（红/绿/蓝）
phase_list = np.array([0, 2*np.pi/3, 4*np.pi/3])


# ======================================
# 新坐标（用于 PNG）
# ======================================
new_x = []
new_y = []
color_id = []


# ======================================
# 创建 GDS 主器件
# ======================================
C = gf.Component("Dirac_Vortex_GDS")

print("开始生成三角形偏移结构...")

for idx, (x, y) in enumerate(zip(x_valid, y_valid)):

    # 极坐标
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # 位移幅度
    m_amp = m0 * np.tanh((r / R_vortex)**alpha)

    # 三类相位
    phase = phase_list[idx % 3]

    # 偏移方向 φ
    phi = w * theta + phase

    # 坐标位移
    dx = m_amp * np.cos(phi)
    dy = m_amp * np.sin(phi)

    fx = x + dx
    fy = y + dy

    # 用于 PNG
    new_x.append(fx)
    new_y.append(fy)
    color_id.append(idx % 3)

    # 三角形旋转角度（围绕中心）
    rot_deg = np.rad2deg(phi)

    # 选择图层：红 / 绿 / 蓝
    tri_comp = tri_list[idx % 3]

    # 放置元件
    ref = C << tri_comp
    ref.center = (fx, fy)
    ref.rotate(rot_deg)


# ======================================
# 中心十字对准
# ======================================
marker = gf.components.cross(length=4.0, width=0.1, layer=(10, 0))
ref_m = C << marker
ref_m.center = (0, 0)

# 边界盒
box = gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99, 0))
ref_box = C << box
ref_box.center = (0, 0)


# ======================================
# 生成 PNG 图（原始晶格 + 3 色偏移后）
# ======================================
print("正在生成 PNG ...")

plt.figure(figsize=(8, 8))

# 原始晶格（灰色）
plt.scatter(x_valid, y_valid, s=3, c="lightgray", label="Original lattice", alpha=0.6)

# 三类偏移（红 / 绿 / 蓝）
colors = ["red", "green", "blue"]
new_x = np.array(new_x)
new_y = np.array(new_y)
color_id = np.array(color_id)

for k in range(3):
    plt.scatter(
        new_x[color_id == k],
        new_y[color_id == k],
        s=6,
        c=colors[k],
        label=f"Shifted Layer {k+1}"
    )

plt.gca().set_aspect("equal")
plt.legend()
plt.title("Original vs Shifted Triangular Lattice (Three Layers)")

png_name = "dirac_vortex_layers.png"
plt.savefig(png_name, dpi=300)
plt.close()


# ======================================
# 保存 GDS
# ======================================
gds_name = "dirac_vortex_layers.gds"
C.write_gds(gds_name)

print("\n====================================")
print("🎉 GDS 与 PNG 生成完毕！")
print(f"GDS 文件: {gds_name}")
print(f"PNG 文件: {png_name}")
print("====================================\n")
