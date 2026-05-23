import klayout.db as db
import numpy as np

from pathlib import Path
ROOT = Path(__file__).resolve().parent

# --- 1. 参数设置 ---
a = 0.168       # 晶格常数 (Lattice constant)
m = 0.15        # 位移量 (Shift in a)
R = 112         # 半径 (Radius in a)
core = 50      # 核心半径 (Core radius in a)
s = 0.32        # 三角形边长大小 (Triangle side size in a)
w = -1          # 涡旋缠绕数 (Vortex winding), 对应标签中的数字

# --- 2. 初始化 KLayout 数据库 ---
ly = db.Layout()
# 设置数据库单位为 1 nm (通常 GDS 默认为 0.001 um)
ly.dbu = 0.001
# 添加顶层单元
top_cell = ly.create_cell("SAMPLE")
# 创建图层 (Layer 1, Datatype 0)
layer1 = ly.layer(1, 0)

# 基础向量
a1 = np.array([1/2, np.sqrt(3)/2])
a2 = np.array([-1/2, np.sqrt(3)/2])
down = np.array([0, 0])
up = np.array([0, -2*np.sqrt(3)/3])

# 列表初始化
down_list = []
up_list = []
# (保留原代码中的列表定义，虽然后面绘图只用了 down_list 和 up_list)
down_list_coords = []
down_list_site = []
up_list_coords = []
colors_list = []

print("正在计算坐标点...")

# --- 3. 计算坐标点 ---
for i in range(-R, 2*R + 1):
    for j in range(-R, 2*R + 1):
        # 检查是否在六边形/圆形区域内
        if np.linalg.norm(i*a1 + j*a2 + down) < 0.8 * R:
            phi0 = ((-i + j) % 3) * 2 * np.pi / 3
            
            # 计算位移 (Shift)
            if np.linalg.norm(i*a1 + j*a2 + down) < core:
                shift = np.array([0, 0])
            else:
                r_vec = i*a1 + j*a2 + down
                theta = np.arctan2(r_vec[1], r_vec[0])
                shift = np.array([np.cos(-w*theta + phi0), np.sin(-w*theta + phi0)])
            
            # (保留原有的颜色逻辑，虽然 GDS 不直接存储颜色，但在逻辑上保留)
            if ((i-j) % 3) == 0:
                colors_list.append('tab:red')
            elif ((i-j) % 3) == 1:
                colors_list.append('tab:blue')
            else:
                colors_list.append('tab:green')
                
            down_list.append(i*a1 + j*a2 + down + shift*m)
            down_list_coords.append([i, j])
            down_list_site.append(i*a1 + j*a2 + down)
            
        if np.linalg.norm(i*a1 + j*a2 + up) < 0.8 * R:
            up_list.append(i*a1 + j*a2 + up)
            up_list_coords.append([i, j])

down_list = np.array(down_list)
up_list = np.array(up_list)

print(f"坐标计算完成。Down点数: {len(down_list)}, Up点数: {len(up_list)}")
print("正在生成几何图形...")

# --- 4. 绘制三角形图案 ---
# 定义三角形形状 (缩放系数 s * a)
down_triangle = -s * a * np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])
up_triangle = s * a * np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])

# 绘制下三角 (Down Triangles)
for point in down_list:
    x = point[0] * a
    y = point[1] * a
    # 将 numpy 坐标转换为 KLayout 的 DPoint
    d0 = db.DPoint(down_triangle[0, 0], down_triangle[0, 1])
    d1 = db.DPoint(down_triangle[1, 0], down_triangle[1, 1])
    d2 = db.DPoint(down_triangle[2, 0], down_triangle[2, 1])
    # 创建多边形并移动到指定位置
    tri = db.DPolygon([d0, d1, d2]).moved(x, y)
    top_cell.shapes(layer1).insert(tri)

# 绘制上三角 (Up Triangles)
for point in up_list:
    x = point[0] * a
    y = point[1] * a
    d0 = db.DPoint(up_triangle[0, 0], up_triangle[0, 1])
    d1 = db.DPoint(up_triangle[1, 0], up_triangle[1, 1])
    d2 = db.DPoint(up_triangle[2, 0], up_triangle[2, 1])
    tri = db.DPolygon([d0, d1, d2]).moved(x, y)
    top_cell.shapes(layer1).insert(tri)

# --- 5. 添加 SEM 身份标记 ---
def draw_sem_text_simple(cell, layer, text, center_x, bottom_y, h):
    """
    简易矢量字库，在指定位置绘制实体文字 (W, -, 1, 2, 4)
    如果遇到未定义的字符（如空格），会留出空白间距但不会报错。
    """
    width = h / 6.0     # 线宽
    char_w = h * 0.6    # 字符宽
    gap = h * 0.2       # 字符间距
    
    # 计算总宽度以居中
    total_width = len(text) * char_w + (len(text) - 1) * gap
    current_x = center_x - total_width / 2
    
    for char in text:
        l = current_x
        r = current_x + char_w
        b = bottom_y
        t = bottom_y + h
        mid = bottom_y + h/2
        
        # 绘制矩形的辅助函数 (使用 DBox)
        rect = lambda x1, y1, x2, y2: cell.shapes(layer).insert(db.DBox(x1, y1, x2, y2))
        
        if char == 'W': 
            rect(l, b, l+width, t) # 左竖
            rect(r-width, b, r, t) # 右竖
            rect(l+char_w/2-width/2, b, l+char_w/2+width/2, mid) # 中竖
            rect(l, b, r, b+width) # 底横
        elif char == '-': 
            rect(l, mid-width/2, r, mid+width/2)
        elif char == '1': 
            rect(l+char_w/2-width/2, b, l+char_w/2+width/2, t)
        elif char == '2':
            rect(l, t-width, r, t) # 顶
            rect(r-width, mid, r, t) # 右上
            rect(l, mid-width/2, r, mid+width/2) # 中
            rect(l, b, l+width, mid) # 左下
            rect(l, b, r, b+width) # 底
        elif char == '4':
            rect(l, mid, l+width, t) # 左上
            rect(l, mid-width/2, r, mid+width/2) # 中横
            rect(r-width, b, r, t) # 右长竖
            
        current_x += char_w + gap

# 计算标记位置 (放在图案上方)
mark_height = 8 * a          
mark_y_pos = 0.8 * R * a + 2 * a 

# 绘制标记
label_text = f"W {w}"
print(f"正在绘制标记: {label_text}")
draw_sem_text_simple(top_cell, layer1, label_text, 0, mark_y_pos, mark_height)

# --- 6. 保存文件 ---
filename = "bit_wmj_532_30um_w-1_20260115.gds"
gds_path = ROOT / filename
gds_path.parent.mkdir(parents=True, exist_ok=True)
ly.write(str(gds_path))
print("GDS saved:", gds_path.resolve())
print(f"Done! Generated: {filename}")