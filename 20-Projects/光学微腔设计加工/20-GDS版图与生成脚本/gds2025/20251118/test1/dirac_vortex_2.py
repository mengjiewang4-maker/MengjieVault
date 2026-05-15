import gdsfactory as gf
import numpy as np
import os

# ===========================
# 基本参数
# ===========================
a = 0.490                      # 晶格常数
hole_radius = 0.32 * a         # 三角形外接圆半径
m0 = 0.050                     # 最大位移
R_vortex = 25.0                # 漩涡半径
alpha = 4.0                    # 调制陡峭度
w = 1                          # 拓扑荷数
device_diameter = 80.0         # 器件尺寸

# ===========================
# 创建主器件
# ===========================
C = gf.Component("Dirac_Vortex_Final")

# ===========================
# 生成标准三角形（不偏移）
# ===========================
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1]
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_pts = list(zip(x_tri, y_tri))

# 三类三角形（不同图层 = 红 / 绿 / 蓝）
triA = gf.Component("Tri_A")
triA.add_polygon(triangle_pts, layer=(1, 0))

triB = gf.Component("Tri_B")
triB.add_polygon(triangle_pts, layer=(2, 0))

triC = gf.Component("Tri_C")
triC.add_polygon(triangle_pts, layer=(3, 0))

tri_list = [triA, triB, triC]

# ===========================
# 生成蜂巢晶格点
# ===========================
N_grid = int(device_diameter / a * 1.2)
i_range = np.arange(-N_grid, N_grid)
j_range = np.arange(-N_grid, N_grid)
XX, YY = np.meshgrid(i_range, j_range)

x_grid = XX * a + YY * a * 0.5
y_grid = YY * a * np.sqrt(3) / 2

x_flat = x_grid.flatten()
y_flat = y_grid.flatten()

mask = (x_flat**2 + y_flat**2) < (device_diameter/2)**2
x_valid = x_flat[mask]
y_valid = y_flat[mask]

print(f"有效晶格点数量: {len(x_valid)}")

# 三类相位偏移 (0°,120°,240°)
phase_list = np.array([0, 2*np.pi/3, 4*np.pi/3])

# ===========================
# 放置所有三角形（核心逻辑）
# ===========================
print("生成三角形阵列 ...")

for idx, (x, y) in enumerate(zip(x_valid, y_valid)):

    # --- 1. 极坐标 ---
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # --- 2. 位移幅度 ---
    m_amp = m0 * np.tanh((r / R_vortex)**alpha)

    # --- 3. 当前三角形属于哪一类 (0,1,2) ---
    phase = phase_list[idx % 3]

    # --- 4. 偏移方向 φ ---
    phi = w * theta + phase

    # --- 5. 坐标偏移 ---
    dx = m_amp * np.cos(phi)
    dy = m_amp * np.sin(phi)

    fx = x + dx
    fy = y + dy

    # --- 6. 围绕中心的旋转角（与偏移方向一致） ---
    rot_deg = np.rad2deg(phi)

    # --- 7. 根据类别选择图层 ---
    tri_comp = tri_list[idx % 3]

    ref = C << tri_comp
    ref.center = (fx, fy)
    ref.rotate(rot_deg)

# ===========================
# 中心十字对准标记
# ===========================
marker = gf.components.cross(length=4.0, width=0.1, layer=(10, 0))
ref_m = C << marker
ref_m.center = (0, 0)

# ===========================
# 边界框
# ===========================
box = gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99, 0))
ref_box = C << box
ref_box.center = (0, 0)

# ===========================
# 保存 GDS
# ===========================
output_file = "dirac_vortex_final.gds"
C.write_gds(output_file)

print("====================================")
print("GDS 生成成功!")
print("文件名:", output_file)
print("====================================")
