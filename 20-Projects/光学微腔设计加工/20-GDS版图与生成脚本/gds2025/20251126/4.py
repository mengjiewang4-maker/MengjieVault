import gdsfactory as gf
import numpy as np
import os
from datetime import datetime

# --------------------------
# 基础参数配置（可按需调整）
# --------------------------
SIDE_LENGTH = 0.2  # 六边形边长（单位：μm，200nm = 0.2μm）
LAYER_HEXAGON = 1  # 六边形所在图层
LAYER_TRIANGLES = 2  # 三角形所在图层
SCALE_FACTOR = 1/3  # 三角形缩小比例（重心不变）
FILE_SERIAL = 1  # 文件序号（可手动调整或自动递增）

# --------------------------
# 生成带时间戳和序号的文件名
# --------------------------
def get_gds_filename(serial_num):
    """生成包含时间戳、序号的GDS文件名"""
    # 获取当前时间（格式：年-月-日_时-分-秒）
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 文件名格式：hexagon_triangles_时间戳_序号.gds
    filename = f"hexagon_triangles_{current_time}_serial{serial_num}.gds"
    # 获取代码所在文件夹的绝对路径
    code_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接完整文件路径（保存在代码文件夹下）
    full_path = os.path.join(code_dir, filename)
    return full_path

# --------------------------
# 图形生成函数
# --------------------------
def create_hexagon_points(side_length):
    """生成正六边形顶点坐标（重心在原点）"""
    points = []
    angles = np.linspace(0, 2*np.pi, 6, endpoint=False)  # 6个顶点均匀分布
    for angle in angles:
        x = side_length * np.cos(angle)
        y = side_length * np.sin(angle)
        points.append((x, y))
    return points

def create_triangle_points(side_length, scale_factor, triangle_index):
    """生成单个缩小版等边三角形顶点坐标（重心在原点）"""
    base_angle = triangle_index * np.pi / 3  # 每个三角形间隔60°
    angles = [base_angle, base_angle + np.pi/3]  # 两个顶点的角度
    
    points = []
    # 前两个顶点：按比例缩小后的六边形顶点
    for angle in angles:
        x = (side_length * scale_factor) * np.cos(angle)
        y = (side_length * scale_factor) * np.sin(angle)
        points.append((x, y))
    # 第三个顶点：原点（重心）
    points.append((0, 0))
    return points

# --------------------------
# 主程序：创建GDS布局并保存
# --------------------------
if __name__ == "__main__":
    # 1. 创建GDS组件
    c = gf.Component("hexagon_with_triangles")
    
    # 2. 绘制图层1的正六边形
    hexagon_points = create_hexagon_points(SIDE_LENGTH)
    c.add_polygon(hexagon_points, layer=LAYER_HEXAGON)
    
    # 3. 绘制图层2的6个等边三角形
    for i in range(6):
        triangle_points = create_triangle_points(SIDE_LENGTH, SCALE_FACTOR, i)
        c.add_polygon(triangle_points, layer=LAYER_TRIANGLES)
    
    # 4. 生成GDS文件路径
    gds_path = get_gds_filename(FILE_SERIAL)
    
    # 5. 保存GDS文件（无预览、不自动打开KLayout）
    c.write_gds(gds_path)
    
    # 6. 输出结果信息
    print("="*50)
    print("GDS文件生成完成！")
    print(f"文件路径：{gds_path}")
    print(f"核心参数：")
    print(f"  - 六边形（图层{LAYER_HEXAGON}）：边长{int(SIDE_LENGTH*1000)}nm，重心(0,0)")
    print(f"  - 三角形（图层{LAYER_TRIANGLES}）：6个等边三角形，缩小比例{SCALE_FACTOR}")
    print(f"  - 文件序号：{FILE_SERIAL}")
    print("="*50)