import gdsfactory as gf
import numpy as np
import os
from datetime import datetime
# ========== 参数 ==========
a = 0.490
hole_radius = 0.32 * a
m0 = 0.050
R_vortex = 25.0
alpha = 4.0
w = 1
device_diameter = 5.0

# ========== 1. 定义三角形形状 (统一朝向) ==========
# 提示：如果想要倒三角，可以改 theta_tri 的初始角度，或者最后 rotate 一次
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1]
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_pts = list(zip(x_tri, y_tri))

# ========== 2. 创建元件 (只定义用于移动的元件) ==========
# 为了区分相位，保留 RGB 分层逻辑，这对检查很有帮助
triR = gf.Component("Tri_R"); triR.add_polygon(triangle_pts, layer=(1, 0))
triG = gf.Component("Tri_G"); triG.add_polygon(triangle_pts, layer=(2, 0))
triB = gf.Component("Tri_B"); triB.add_polygon(triangle_pts, layer=(3, 0))
tri_list = [triR, triG, triB]

# ========== 3. 生成晶格坐标 (三角晶格) ==========
N_grid = int(device_diameter / a * 1.2)
i_range = np.arange(-N_grid, N_grid)
j_range = np.arange(-N_grid, N_grid)
XX, YY = np.meshgrid(i_range, j_range)

# 三角晶格坐标公式
x_grid = XX * a + YY * a * 0.5
y_grid = YY * a * np.sqrt(3) / 2

x_flat = x_grid.flatten() 
y_flat = y_grid.flatten()

# 筛选圆内的点
mask = (x_flat**2 + y_flat**2) < (device_diameter / 2)**2
x_valid = x_flat[mask]
y_valid = y_flat[mask]

print(f"有效晶格点数量: {len(x_valid)}")

# Kekule 调制的相位 (0, 120, 240度)
phase_list = np.array([0, 2*np.pi/3, 4*np.pi/3])

# ========== 4. 创建主器件并放置 ==========
C = gf.Component("Dirac_Vortex_No_Duplicate")

# --- [重要] 这里我们只写一个循环，只画移动后的孔，不画原始孔 ---
for idx, (x, y) in enumerate(zip(x_valid, y_valid)):
    # 1. 计算极坐标
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    
    # 2. 计算位移量 m(r)
    if R_vortex == 0:
        m_amp = m0
    else:
        m_amp = m0 * np.tanh((r / R_vortex)**alpha)
    
    # 3. 计算局部相位
    # idx % 3 实现了三角晶格上的 Kekule 周期性
    phase = phase_list[idx % 3]
    
    # 4. 广义相位 Phi
    phi = w * theta + phase
    
    # 5. 计算位移向量 (dx, dy)
    dx = m_amp * np.cos(phi)
    dy = m_amp * np.sin(phi)
    
    # 6. 最终位置
    fx = x + dx
    fy = y + dy
    
    # 7. 放置元件
    # 根据 idx 分配 R/G/B 图层
    tri_comp = tri_list[idx % 3]
    ref = C << tri_comp
    ref.center = (fx, fy)
    
    # [修正] 通常 Dirac Vortex 的孔是不自旋转的，只移动位置。
    # 如果你的论文明确要求孔要旋转，请把下面这行注释打开。
    # rot_deg = np.rad2deg(phi)
    # ref.rotate(rot_deg)
    
    # 如果你想让所有三角形统一转 30 度变成“倒三角”或“正三角”，可以在这里加：
    ref.rotate(30) # 可选

# ========== 5. 中心标记与边框 (辅助层) ==========
# 放在 Layer 10 和 99，不影响器件结构
marker = gf.components.cross(length=4.0, width=0.1, layer=(10,0))
ref_m = C << marker; ref_m.center = (0,0)

box = gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99,0))
ref_box = C << box; ref_box.center = (0,0)

# --- 第6步：保存到脚本所在的文件夹 ---
# 加一个框方便看
ref_box = C << gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99,0))
ref_box.center = (0, 0)

# 获取当前脚本的绝对路径目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 获取当前日期 (格式：YYYYMMDD)
current_date = datetime.now().strftime('%Y%m%d')

# 检查当前文件夹中已经存在的 GDS 文件，并生成一个序号
existing_files = [f for f in os.listdir(script_dir) if f.endswith('.gds') and f.startswith('dirac_vortex_')]
existing_numbers = [int(f.split('_')[-1].split('.')[0]) for f in existing_files if f.split('_')[-1].split('.')[0].isdigit()]
new_number = max(existing_numbers, default=0) + 1
new_number_str = f"{new_number:02d}"

# 生成新的文件名
output_filename = f"dirac_vortex_{current_date}_{new_number_str}.gds"
output_path = os.path.join(script_dir, output_filename)
C.write_gds(output_path)

print("-" * 30)
print("GDS 生成完成 (已去除重复三角形)！")
print(f"保存路径: {output_path}")
print("-" * 30)