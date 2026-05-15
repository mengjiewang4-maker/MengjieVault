import klayout.db as db
import numpy as np
from pathlib import Path
from datetime import datetime

# ==================== 1. 参数设置 ====================
a = 0.490         # lattice constant in nm
m0 = 0.15       # shift in a
R = 125         # 1.25x Lattice Radius in a
core = 60      # core radius in a
s = 0.32        # triangle side size in a
w = -1          # vortex winding mod3==-1
alpha = 4       # power of m=tanh((r/R)^alpha)

# ==================== 2. 初始化布局 ====================
ly = db.Layout()
ly.dbu = 0.001
top_cell = ly.create_cell("SAMPLE")
layer1 = ly.layer(1, 0)

# 定义三角形形状
down_triangle = -s*a*np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])
up_triangle = s*a*np.array([[0, np.sqrt(3)/3], [-1/2, -np.sqrt(3)/6], [1/2, -np.sqrt(3)/6]])

# ==================== 3. 计算与绘制图案 (Layer 1) ====================
a1 = np.array([1/2, np.sqrt(3)/2])
a2 = np.array([-1/2, np.sqrt(3)/2])
down_pos = np.array([0, 0])
up_pos = np.array([0, -2*np.sqrt(3)/3])

for i in range(-R, 2*R+1):
    for j in range(-R, 2*R+1):
        r_vec_down = i*a1 + j*a2 + down_pos
        dist_down = np.linalg.norm(r_vec_down)
        if dist_down < 0.8*R:
            phi0 = ((-i+j)%3) * 2*np.pi/3
            theta = np.arctan2(r_vec_down[1], r_vec_down[0])
            shift = np.array([np.cos(-w*theta+phi0), np.sin(-w*theta+phi0)])
            m = np.tanh((dist_down/core)**alpha) * m0
            pos = (r_vec_down + shift*m) * a
            pts = [db.DPoint(p[0], p[1]) for p in down_triangle]
            top_cell.shapes(layer1).insert(db.DPolygon(pts).moved(pos[0], pos[1]))
        
        r_vec_up = i*a1 + j*a2 + up_pos
        if np.linalg.norm(r_vec_up) < 0.8*R:
            pos = r_vec_up * a
            pts = [db.DPoint(p[0], p[1]) for p in up_triangle]
            top_cell.shapes(layer1).insert(db.DPolygon(pts).moved(pos[0], pos[1]))

# ==================== 4. 矢量字符绘制函数 (SEM 标识) ====================
def draw_vector_text(cell, layer, text, center_x, bottom_y, h):
    width = h / 6.0     # 线条粗细
    char_w = h * 0.6    # 单个字符宽度
    gap = h * 0.3       # 字符间距
    
    total_width = len(text) * char_w + (len(text) - 1) * gap
    curr_x = center_x - total_width / 2
    
    def rect(x, y, w_rect, h_rect):
        cell.shapes(layer).insert(db.DBox(x, y, x + w_rect, y + h_rect))

    for char in text:
        l, b, r, t = curr_x, bottom_y, curr_x + char_w, bottom_y + h
        m = b + h/2
        
        if char == 'w' or char == 'W':
            rect(l, b, width, h)           # 左竖
            rect(r-width, b, width, h)     # 右竖
            rect(l+char_w/2-width/2, b, width, h*0.6) # 中间短竖
            rect(l, b, char_w, width)      # 底横
        elif char == '-':
            rect(l, m-width/2, char_w, width)
        elif char == '=':
            rect(l, m+width, char_w, width)
            rect(l, m-width*2, char_w, width)
        elif char == '0':
            rect(l, b, width, h); rect(r-width, b, width, h)
            rect(l, b, char_w, width); rect(l, t-width, char_w, width)
        elif char == '1':
            rect(l+char_w/2, b, width, h)
        elif char == '2':
            rect(l, t-width, char_w, width); rect(r-width, m, width, h/2)
            rect(l, m-width/2, char_w, width); rect(l, b, width, h/2)
            rect(l, b, char_w, width)
        elif char == '3':
            rect(l, t-width, char_w, width); rect(r-width, b, width, h)
            rect(l, m-width/2, char_w, width); rect(l, b, char_w, width)
        elif char == '4':
            rect(l, m, width, h/2); rect(r-width, b, width, h)
            rect(l, m-width/2, char_w, width)
        elif char == '5':
            rect(l, t-width, char_w, width); rect(l, m, width, h/2)
            rect(l, m-width/2, char_w, width); rect(r-width, b, width, h/2)
            rect(l, b, char_w, width)
        
        curr_x += char_w + gap

# 绘制位置：图案顶部上方
mark_h = 10 * a  # 标识高度
mark_y = 0.85 * R * a  # 距离中心的垂直高度
draw_vector_text(top_cell, layer1, f"w={w}", 0, mark_y, mark_h)

# ==================== 5. 命名并保存 ====================
date_str = datetime.now().strftime("%Y%m%d")
output_dir = Path(__file__).resolve().parent / "output"
output_dir.mkdir(exist_ok=True)
filename = output_dir / f"wmj{date_str}w{w}R100.gds"
ly.write(filename)

print(f"完成！文件已保存为: {filename}")
