import klayout.db as db
import numpy as np

# ---------------------------------------------------------
# 1. 参数设置 (已调整为约 100um 直径)
# ---------------------------------------------------------
a = 0.490      # 晶格常数 a = 490 nm (注意：单位设为 0.490 um)
m = 0.15       # 相对位移量 (相对于 a)
R = 638        # 半径层数 (R=128 对应约 100um 直径)
core = 3       # 核心半径 (以 a 为单位)
s = 0.32       # 三角形边长缩放比例
w = -1         # 涡旋拓扑荷 (Vortex winding)

# ---------------------------------------------------------
# 2. 初始化 KLayout 布局
# ---------------------------------------------------------
ly = db.Layout()
ly.dbu = 0.001           # 数据库精度设为 1nm
top_cell = ly.create_cell("SAMPLE")

# [关键修改] 只创建图案层 layer1，不再创建 layer2
layer1 = ly.layer(1, 0)  

# ---------------------------------------------------------
# 3. 计算晶格点坐标
# ---------------------------------------------------------
a1 = np.array([1/2, np.sqrt(3)/2])
a2 = np.array([-1/2, np.sqrt(3)/2])
down = np.array([0, 0])
up = np.array([0, -2*np.sqrt(3)/3])

down_list = []
up_list = []

print(f"开始计算坐标点 (R={R})...")

for i in range(-R, 2*R + 1):
    for j in range(-R, 2*R + 1):
        # 筛选圆形区域内的点 (0.8系数用于切成圆形)
        if np.linalg.norm(i*a1 + j*a2 + down) < 0.8 * R:
            # 计算广义 Haldane 模型所需的位移相位
            phi0 = ((-i + j) % 3) * 2 * np.pi / 3
            
            # 核心区域不移动，外部区域施加涡旋位移
            if np.linalg.norm(i*a1 + j*a2 + down) < core:
                shift = np.array([0, 0])
            else:
                r = i*a1 + j*a2 + down
                theta = np.arctan2(r[1], r[0])
                shift = np.array([np.cos(-w*theta + phi0), np.sin(-w*theta + phi0)])
            
            # 记录下三角 (Down triangle) 的中心坐标
            down_list.append(i*a1 + j*a2 + down + shift*m)
            
        # 记录上三角 (Up triangle) 的中心坐标 (背景)
        if np.linalg.norm(i*a1 + j*a2 + up) < 0.8 * R:
            up_list.append(i*a1 + j*a2 + up)

down_list = np.array(down_list)
up_list = np.array(up_list)

# ---------------------------------------------------------
# 4. 生成 GDS 图形
# ---------------------------------------------------------
# 定义三角形顶点 (单位已经是微米，因为 a=0.490)
down_triangle = -s * a * np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])
up_triangle = s * a * np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])

print(f"开始绘制图形，共约 {len(down_list) + len(up_list)} 个孔洞...")

# 绘制下三角 (红色部分)
for point in down_list:
    x = point[0] * a
    y = point[1] * a
    # 创建多边形顶点
    d0 = db.DPoint(down_triangle.flatten()[0], down_triangle.flatten()[1])
    d1 = db.DPoint(down_triangle.flatten()[2], down_triangle.flatten()[3])
    d2 = db.DPoint(down_triangle.flatten()[4], down_triangle.flatten()[5])
    # 移动到对应位置并插入 layer1
    tri = db.DPolygon([d0, d1, d2]).moved(x, y)
    top_cell.shapes(layer1).insert(tri)

# 绘制上三角 (背景部分)
for point in up_list:
    x = point[0] * a
    y = point[1] * a
    d0 = db.DPoint(up_triangle.flatten()[0], up_triangle.flatten()[1])
    d1 = db.DPoint(up_triangle.flatten()[2], up_triangle.flatten()[3])
    d2 = db.DPoint(up_triangle.flatten()[4], up_triangle.flatten()[5])
    tri = db.DPolygon([d0, d1, d2]).moved(x, y)
    top_cell.shapes(layer1).insert(tri)

# [关键修改] 此处删除了 Layer 2 (envelope) 的相关代码

# ---------------------------------------------------------
# 5. 保存文件
# ---------------------------------------------------------
output_file = "basic1217_200.gds"
ly.write(output_file)
print(f"完成！GDS 文件已保存为: {output_file}")