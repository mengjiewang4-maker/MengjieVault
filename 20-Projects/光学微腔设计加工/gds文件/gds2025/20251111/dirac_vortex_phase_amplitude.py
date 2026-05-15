import gdsfactory as gf
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 基本参数设置（单位：微米）
# ============================================
a = 0.49             # 晶格常数 490 nm
r_hole = 0.32 * a     # 三角孔半径
m0 = 0.05             # 最大偏移（µm）
R = 5 * a             # 调制半径
alpha = 4             # 调制陡峭度
w = +1                # 拓扑绕数 (+1逆时针)
Nx, Ny = 20, 20       # 晶格范围

# ============================================
# 三角孔定义
# ============================================
def triangle(radius, rotation_deg=0):
    pts = []
    for i in range(3):
        theta = np.deg2rad(rotation_deg + i * 120)
        pts.append((radius * np.cos(theta), radius * np.sin(theta)))
    return np.array(pts)

# ============================================
# Dirac-Vortex 调制函数
# ============================================
def vortex_shift(x, y):
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    amplitude = m0 * np.tanh((r / R) ** alpha)
    dx = amplitude * np.cos(w * phi)
    dy = amplitude * np.sin(w * phi)
    return dx, dy, r, phi, amplitude

# ============================================
# 构建蜂窝晶格 + 调制
# ============================================
c = gf.Component("dirac_vortex_cavity_um")
all_x, all_y, all_r, all_phi, all_amp = [], [], [], [], []

for i in range(-Nx, Nx):
    for j in range(-Ny, Ny):
        x0 = a * (i + 0.5 * (j % 2))
        y0 = np.sqrt(3)/2 * a * j

        if (i + j) % 2 == 0:
            dx = dy = 0
            r = np.sqrt(x0**2 + y0**2)
            phi = np.arctan2(y0, x0)
            amplitude = 0
        else:
            dx, dy, r, phi, amplitude = vortex_shift(x0, y0)

        tri = triangle(r_hole, rotation_deg=30)
        tri = tri + np.array([x0 + dx, y0 + dy])
        c.add_polygon(tri, layer=(1, 0))

        all_x.append(x0 + dx)
        all_y.append(y0 + dy)
        all_r.append(r)
        all_phi.append(phi)
        all_amp.append(amplitude)

# ============================================
# 写入 GDS 文件
# ============================================
c.write_gds("dirac_vortex_phase_amplitude.gds")
print("✅ GDS 文件已生成：dirac_vortex_phase_amplitude.gds")

# ============================================
# 可视化（幅度 + 相位）
# ============================================
x_arr, y_arr = np.array(all_x), np.array(all_y)
r_arr, phi_arr = np.array(all_r), np.array(all_phi)
amp_arr = np.array(all_amp)
phase_arr = (w * phi_arr) % (2 * np.pi)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# 幅度图 |m(r)|
sc1 = axes[0].scatter(x_arr, y_arr, c=amp_arr, cmap="magma", s=10, edgecolors="none")
axes[0].set_title("|m(r)|  (Amplitude modulation)")
axes[0].set_xlabel("x (µm)")
axes[0].set_ylabel("y (µm)")
axes[0].set_aspect("equal")
plt.colorbar(sc1, ax=axes[0], label="Amplitude (µm)")

# 相位图 arg(m(r))
sc2 = axes[1].scatter(x_arr, y_arr, c=phase_arr, cmap="twilight_shifted", s=10, edgecolors="none")
axes[1].set_title("arg(m(r))  (Phase vortex)")
axes[1].set_xlabel("x (µm)")
axes[1].set_ylabel("y (µm)")
axes[1].set_aspect("equal")
plt.colorbar(sc2, ax=axes[1], label="Phase (radians)")

plt.suptitle("Dirac-Vortex Honeycomb Photonic Crystal", fontsize=14)
plt.tight_layout()
plt.show()
