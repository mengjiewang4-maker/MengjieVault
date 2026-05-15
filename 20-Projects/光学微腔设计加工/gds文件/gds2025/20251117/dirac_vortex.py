import gdsfactory as gf
import numpy as np
import os  # <--- 新增：用于处理文件路径

# --- 第1步：定义物理参数 (单位：微米) ---
a = 0.490          # 晶格常数
hole_radius = 0.32 * a # 外接圆半径
m0 = 0.050         # 最大平移距离
R_vortex = 25.0    # 漩涡核心半径
alpha = 4.0        # 形状因子
w = 1              # 拓扑荷数

device_diameter = 20.0 

# --- 第2步：创建基础元件 (最稳健的方法) ---
C = gf.Component("Dirac_Vortex_Cavity_Fixed")

# 1. 计算三角形顶点 (0, 120, 240度)
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1] 
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_points = list(zip(x_tri, y_tri))

# 2. 创建一个独立的 Component 来存放三角形
triangle_component = gf.Component("Triangle_Unit")
triangle_component.add_polygon(triangle_points, layer=(1, 0))


# --- 第3步：生成坐标 (使用 NumPy) ---
# 生成网格
N_grid = int(device_diameter / a * 1.2)
i_range = np.arange(-N_grid, N_grid)
j_range = np.arange(-N_grid, N_grid)
XX, YY = np.meshgrid(i_range, j_range)

# 转换为蜂巢晶格坐标
x_grid = XX * a + YY * a * 0.5
y_grid = YY * a * np.sqrt(3) / 2

x_flat = x_grid.flatten()
y_flat = y_grid.flatten()

# A 子晶格 (基点)
pos_A_x = x_flat
pos_A_y = y_flat

# B 子晶格 (偏移点)
offset_x = a * 0.5
offset_y = a * np.sqrt(3) / 6
pos_B_x = x_flat + offset_x
pos_B_y = y_flat + offset_y

# --- 第4步：绘制 A 子晶格 (Reference) ---
print("正在生成 A 子晶格...")
mask_A = (pos_A_x**2 + pos_A_y**2) < (device_diameter/2)**2
valid_A_x = pos_A_x[mask_A]
valid_A_y = pos_A_y[mask_A]

for x, y in zip(valid_A_x, valid_A_y):
    ref = C << triangle_component
    ref.center = (x, y)
    ref.rotate(30) # 旋转30度，使其变正/倒三角

# --- 第5步：绘制 B 子晶格 (Vortex Shift) ---
print("正在生成 B 子晶格...")
mask_B = (pos_B_x**2 + pos_B_y**2) < (device_diameter/2)**2
valid_B_x = pos_B_x[mask_B]
valid_B_y = pos_B_y[mask_B]

for x, y in zip(valid_B_x, valid_B_y):
    # 1. 极坐标
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # 2. 平移幅度
    if R_vortex == 0:
        m_amp = m0
    else:
        m_amp = m0 * np.tanh((r / R_vortex)**alpha)

    # 3. 广义相位 (Generalized Phase)
    phi_phase = w * theta 

    # 4. Kekule 畸变位移
    shift_x = m_amp * np.cos(phi_phase)
    shift_y = m_amp * np.sin(phi_phase)
    
    # 5. 应用位移
    final_x = x + shift_x
    final_y = y + shift_y

    # 6. 添加引用
    ref = C << triangle_component
    ref.center = (final_x, final_y)
    ref.rotate(-30) # B孔旋转方向与A相反

# --- 第6步：保存到脚本所在的文件夹 ---
# 加一个框方便看
ref_box = C << gf.components.rectangle(size=(device_diameter+2, device_diameter+2), layer=(99,0))
ref_box.center = (0, 0)

# 获取当前脚本的绝对路径目录
script_dir = os.path.dirname(os.path.abspath(__file__))
output_filename = "dirac_vortex_w1_final.gds"
output_path = os.path.join(script_dir, output_filename)

C.write_gds(output_path)
print("-" * 30)
print(f"GDS 文件已成功生成！")
print(f"保存位置: {output_path}")
print("-" * 30)