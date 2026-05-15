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

# ========== 1. 定义三角形形状 (统一朝向) ==========
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1]
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_pts = list(zip(x_tri, y_tri))

# ========== 2. 创建元件 (分层以便检查) ==========
triR = gf.Component("Tri_R"); triR.add_polygon(triangle_pts, layer=(1, 0))
triG = gf.Component("Tri_G"); triG.add_polygon(triangle_pts, layer=(2, 0))
triB = gf.Component("Tri_B"); triB.add_polygon(triangle_pts, layer=(3, 0))
# 在极坐标生成中，我们轮流使用颜色，仅为了视觉区分
tri_list = [triR, triG, triB]

# ========== 3. 生成晶格坐标 (修改为：极坐标/同心圆生成) ==========
# [响应你的要求]：不再使用 meshgrid 生成周期性网格。
# 而是使用 r, theta 生成同心圆分布 (Polar Lattice)。

x_valid = []
y_valid = []
r_valid = []      # 存下来备用
theta_valid = []  # 存下来备用
color_indices = [] # 存颜色索引

# 0. 中心点
x_valid.append(0); y_valid.append(0)
r_valid.append(0); theta_valid.append(0)
color_indices.append(0)

# 1. 逐层生成圆环
num_rings = int((device_diameter / 2) / a) # 半径方向能放几圈
print(f"正在生成同心圆晶格，共 {num_rings} 圈...")

for n in range(1, num_rings + 1):
    # 当前圈的半径
    r_ring = n * a
    
    # 计算这一圈应该放多少个三角形，才能保持间距约为 a
    # 周长 C = 2 * pi * r
    # 数量 N = C / a = 2 * pi * n
    n_points_in_ring = int(2 * np.pi * n)
    
    for m in range(n_points_in_ring):
        # 当前点的角度 (0 到 2pi)
        theta_p = 2 * np.pi * m / n_points_in_ring
        
        # 极坐标 -> 直角坐标 (仅用于最后保存，生成逻辑完全是极坐标的)
        x_p = r_ring * np.cos(theta_p)
        y_p = r_ring * np.sin(theta_p)
        
        x_valid.append(x_p)
        y_valid.append(y_p)
        r_valid.append(r_ring)
        theta_valid.append(theta_p)
        
        # 简单的颜色轮替
        color_indices.append(m % 3)

print(f"有效晶格点数量: {len(x_valid)}")

# ========== 4. 创建主器件并放置 ==========
C = gf.Component("Dirac_Vortex_Polar_Lattice")

# 遍历每一个生成的点
for i in range(len(x_valid)):
    # 获取之前生成的极坐标参数
    x = x_valid[i]
    y = y_valid[i]
    r = r_valid[i]
    theta = theta_valid[i]
    
    # --- 计算涡旋位移 ---
    
    # 1. 位移幅度 m(r)
    if R_vortex == 0:
        m_amp = m0
    else:
        m_amp = m0 * np.tanh((r / R_vortex)**alpha)
    
    # 2. 广义相位 Phi
    # 在同心圆结构中，通常不再加 Kekule 相位 (phase_list)，只保留涡旋相位
    phi = w * theta
    
    # 3. 计算位移向量 (dx, dy)
    # 这里依然要投射到 x, y 方向去移动
    dx = m_amp * np.cos(phi)
    dy = m_amp * np.sin(phi)
    
    # 4. 最终位置
    fx = x + dx
    fy = y + dy
    
    # 5. 放置元件
    idx = color_indices[i]
    tri_comp = tri_list[idx]
    ref = C << tri_comp
    ref.center = (fx, fy)
    
    # 统一旋转 30 度 (倒/正三角)
    ref.rotate(30) 
    
    # 如果你想让三角形“头朝向圆心” (Radial Orientation)，可以用下面这行代替上一行：
    # ref.rotate(np.rad2deg(theta) + 90) 

# ========== 5. 中心标记与边框 ==========
marker = gf.components.cross(length=4.0, width=0.1, layer=(10,0))
ref_m = C << marker; ref_m.center = (0,0)

box = gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99,0))
ref_box = C << box; ref_box.center = (0,0)

# ========== 6. 保存文件 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
output_filename = 'dirac_vortex_polar.gds'
output_path = os.path.join(script_dir, output_filename)

C.write_gds(output_path)

print("-" * 30)
print("GDS 生成完成 (极坐标/同心圆生成模式)！")
print(f"保存路径: {output_path}")
print("-" * 30)