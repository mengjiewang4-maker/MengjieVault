#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 17:01:46 2025

@author: mac
"""

import gdsfactory as gf
import numpy as np
import os
from datetime import datetime

# --- 第1步：定义物理参数 (单位：微米) ---
a = 0.490          # 晶格常数
hole_radius = 0.32 * a # 外接圆半径
m0 = 0.050         # 最大平移距离
R_vortex = 25.0    # 漩涡核心半径
alpha = 4.0        # 形状因子
w = 1              # 拓扑荷数

device_diameter = 1

# --- 第2步：创建基础元件 (A/B 分层) ---
C = gf.Component("Dirac_Vortex_Cavity_Separated")

# 1. 计算三角形顶点 (0, 120, 240度)
theta_tri = np.linspace(0, 2*np.pi, 4)[:-1] 
x_tri = hole_radius * np.cos(theta_tri)
y_tri = hole_radius * np.sin(theta_tri)
triangle_points = list(zip(x_tri, y_tri))

# 2. 创建两个独立的 Component，分别对应不同图层
# A 晶格元件 -> Layer (1, 0)
triangle_component_A = gf.Component("Triangle_Unit_A")
triangle_component_A.add_polygon(triangle_points, layer=(1, 0))

# B 晶格元件 -> Layer (2, 0)
triangle_component_B = gf.Component("Triangle_Unit_B")
triangle_component_B.add_polygon(triangle_points, layer=(2, 0))

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

# --- 第4步：绘制 B 晶格不动 (图层1，黄色虚线) ---
print("正在生成 B 晶格 (Layer 1，黄色虚线)...")
normal_layer_B = (1, 0)


# 在图层1上绘制虚线效果的 B 晶格
for x, y in zip(pos_B_x, pos_B_y):
    if (x**2 + y**2) < (device_diameter/2)**2:
        add_dashed_triangle(C, triangle_points, normal_layer_B)

# --- 第5步：绘制 A 晶格不动 (图层2) ---
print("正在生成 A 晶格 (Layer 2)...")
normal_layer_A = (2, 0)

# 在图层2上绘制不平移的 A 晶格
for x, y in zip(pos_A_x, pos_A_y):
    if (x**2 + y**2) < (device_diameter/2)**2:
        ref = C << triangle_component_A  # <--- 使用 A 组件
        ref.center = (x, y)

# --- 第6步：绘制 B 晶格平移后的图形 (图层3) ---
print("正在生成 B 晶格平移后的图形 (Layer 3)...")
shifted_layer_B = (3, 0)

for x, y in zip(pos_B_x, pos_B_y):
    if (x**2 + y**2) < (device_diameter/2)**2:
        # 计算平移幅度
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # 平移幅度 (假设平移只是简单的向外扩展)
        shift_x = m0 * np.cos(theta)
        shift_y = m0 * np.sin(theta)
        
        # 计算平移后的坐标
        final_x = x + shift_x
        final_y = y + shift_y
        
        # 在图层3上绘制平移后的 B 晶格
        ref = C << triangle_component_B  # <--- 使用 B 组件
        ref.center = (final_x, final_y)

# --- 第7步：添加中心位置标记 (图层4) ---
print("正在添加中心标记 (Layer 4)...")
marker_layer = (4, 0)
marker_length = 4.0  # 十字的总长度 (微米)
marker_width = 0.1   # 十字的线宽 (微米)



# 纵向矩形
rect_v = gf.components.rectangle(size=(marker_width, marker_length), layer=marker_layer)
ref_v = C << rect_v
ref_v.center = (0, 0)

# --- 第8步：保存到脚本所在的文件夹 ---
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
output_filename = f"dirac_vortex_new{current_date}_{new_number_str}.gds"
output_path = os.path.join(script_dir, output_filename)

C.write_gds(output_path)
print("-" * 30)
print(f"GDS 文件已成功生成！")
print(f"保存位置: {output_path}")
print("-" * 30)

