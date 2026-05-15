import gdsfactory as gf
import numpy as np
import os

# ========== 参数 ==========
a = 0.490
hole_radius = 0.32 * a
m0 = 0.050
R_vortex = 25.0
alpha = 4.0
w = 1
device_diameter = 80.0

# ========== 三角形模板 ==========
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1]
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_pts = list(zip(x_tri, y_tri))

# ========== 三角形元件（偏移后三色） ==========
triR = gf.Component("Tri_R"); triR.add_polygon(triangle_pts, layer=(1, 0))
triG = gf.Component("Tri_G"); triG.add_polygon(triangle_pts, layer=(2, 0))
triB = gf.Component("Tri_B"); triB.add_polygon(triangle_pts, layer=(3, 0))
tri_list = [triR, triG, triB]

# ========== 原始（未位移）三角形元件，放到可见层 (10,0) ==========
triOrig = gf.Component("Tri_Orig")
triOrig.add_polygon(triangle_pts, layer=(10, 0))

# ========== 生成蜂巢晶格坐标 ==========
N_grid = int(device_diameter / a * 1.2)
i_range = np.arange(-N_grid, N_grid)
j_range = np.arange(-N_grid, N_grid)
XX, YY = np.meshgrid(i_range, j_range)
x_grid = XX * a + YY * a * 0.5
y_grid = YY * a * np.sqrt(3) / 2
x_flat = x_grid.flatten(); y_flat = y_grid.flatten()
mask = (x_flat**2 + y_flat**2) < (device_diameter / 2)**2
x_valid = x_flat[mask]; y_valid = y_flat[mask]

print(f"有效晶格点数量: {len(x_valid)}")

# 定义相位列表，用于 RGB 三角形颜色的偏移
phase_list = np.array([0, 2 * np.pi / 3, 4 * np.pi / 3])

# ========== 创建主器件 ==========
C = gf.Component("Dirac_Vortex_GDS_with_Orig")

# ========== 先放置原始（未位移）三角形到 GDS 的 layer (10,0) ==========
for idx, (x, y) in enumerate(zip(x_valid, y_valid)):
    ref_o = C << triOrig
    ref_o.center = (x, y)

# ========== 放置偏移后的三色三角形（layer 1/2/3） ==========
new_x = []; new_y = []; color_id = []
for idx, (x, y) in enumerate(zip(x_valid, y_valid)):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    m_amp = m0 * np.tanh((r / R_vortex)**alpha)
    phase = phase_list[idx % 3]  # 这里用 phase_list
    phi = w * theta + phase
    dx = m_amp * np.cos(phi); dy = m_amp * np.sin(phi)
    fx = x + dx; fy = y + dy

    new_x.append(fx); new_y.append(fy); color_id.append(idx % 3)

    rot_deg = np.rad2deg(phi)
    tri_comp = tri_list[idx % 3]
    ref = C << tri_comp
    ref.center = (fx, fy)
    ref.rotate(rot_deg)

# ========== 中心标记与边框 ==========
marker = gf.components.cross(length=4.0, width=0.1, layer=(10,0))
ref_m = C << marker; ref_m.center = (0,0)
box = gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99,0))
ref_box = C << box; ref_box.center = (0,0)

# ========== 保存 GDS ==========
gds_name = 'dirac_vortex_layers_with_orig.gds'
C.write_gds(gds_name)

print("生成完成 GDS 文件：", gds_name)

# ========== 自动生成 .lyp 文件 ==========
lyp_filename = gds_name.replace('.gds', '.lyp')

# lyp 文件内容，配置图层样式
lyp_content = """<?xml version="1.0" encoding="UTF-8" ?>
<layer-properties>
    <layer number="1" color="ff0000" hatch_pattern="solid" width="3"/>
    <layer number="2" color="00ff00" hatch_pattern="solid" width="3"/>
    <layer number="3" color="0000ff" hatch_pattern="solid" width="3"/>
    <layer number="10" color="999999" hatch_pattern="solid" width="2"/>
    <layer number="99" color="ffff00" hatch_pattern="solid" width="2"/>
</layer-properties>
"""

# 保存 lyp 文件
with open(lyp_filename, 'w') as f:
    f.write(lyp_content)

print("生成完成 .lyp 文件：", lyp_filename)
