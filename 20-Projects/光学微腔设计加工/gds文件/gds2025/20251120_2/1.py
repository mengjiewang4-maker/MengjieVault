import os
import numpy as np
import gdspy
from datetime import datetime

# 定义超胞的大小和属性
a = 1.0  # 晶格常数（边长）
r = 0.4  # 涡旋半径，按需调整
phi_0 = np.pi / 3  # 涡旋调制的角度，相位偏移
m_0 = 0.1  # 最大调制，可以变化

# 获取当前时间作为文件名的一部分
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"dirac_vortex_cavity_{timestamp}_001.gds"  # 序号可以根据需求增加

# 获取当前文件所在路径，并创建子文件夹
current_dir = os.path.dirname(os.path.realpath(__file__))
subfolder = os.path.join(current_dir, 'output_files')

# 如果子文件夹不存在，则创建
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

# 创建一个新的GDS库和单元
lib = gdspy.GdsLibrary()
cell = lib.new_cell('DIRAC_VORTEX')

# 创建单个三角形的函数
def create_triangle(x, y, size):
    points = [
        (x, y),
        (x + size, y),
        (x + size / 2, y + np.sqrt(3) * size / 2)
    ]
    return gdspy.Polygon(points)

# 旋转一个形状的函数
def rotate_shape(shape, angle, center=(0, 0)):
    return shape.rotate(angle, center=center)

# 生成六角密排晶格并应用涡旋调制
def create_lattice():
    for i in range(-3, 4):  # 可以调整晶格的范围
        for j in range(-3, 4):
            # 计算每个三角形的位置
            x_offset = i * a  # 水平方向间隔为a
            y_offset = j * np.sqrt(3) * a  # 垂直方向间隔为sqrt(3) * a
            
            # 偶数行和奇数行需要偏移
            #if i % 2 == 1:
               # y_offset += np.sqrt(3) * a / 2  # 偶数行和奇数行之间有偏移

            angle = (i + j) * phi_0  # 基于索引应用相位偏移或旋转
            triangle = create_triangle(x_offset, y_offset, a / 2)
            rotated_triangle = rotate_shape(triangle, angle, center=(x_offset, y_offset))
            cell.add(rotated_triangle)

# 生成晶格并应用涡旋调制
create_lattice()

# 保存GDS文件到子文件夹
gds_file_path = os.path.join(subfolder, file_name)
lib.write_gds(gds_file_path)

print(f"GDS文件已保存: {gds_file_path}")
