import numpy as np
import gdspy
import math
import matplotlib.pyplot as plt

def generate_disclination_gds(a=0.5, r_hole=0.13, rings=15, symmetry=5, filename="disclination_cavity.gds"):
    """
    a: 晶格常数 (um)
    r_hole: 空气孔半径 (um)
    rings: 环数
    symmetry: 目标对称性 (5代表C5)
    """
    print(f"正在生成 C{symmetry} 旋错结构...")
    
    # 1. 创建 GDSII 单元
    lib = gdspy.GdsLibrary()
    cell = lib.new_cell('DISCLINATION_CAVITY')
    
    # 2. 生成原始蜂窝晶格 (C6 Honeycomb)
    # 我们先生成一个足够大的正交网格，然后过滤出蜂窝结构
    points_orig = []
    for i in range(-rings*2, rings*2):
        for j in range(-rings*2, rings*2):
            # 蜂窝晶格由两套子晶格组成
            for offset in [(0, 0), (a/2, a*np.sqrt(3)/2)]:
                x = a * i + offset[0]
                y = a * np.sqrt(3) * j + offset[1]
                
                # 初始过滤：只保留 360 度范围内的点
                rho = np.sqrt(x**2 + y**2)
                if 0 < rho <= rings * a:
                    points_orig.append((x, y))

    # 3. 执行 Volterra 变换 (坐标映射)
    factor = symmetry / 6.0
    final_points = []
    seen_points = [] # 用于去重

    # 添加中心点 (奇点)
    final_points.append((0, 0))

    for x, y in points_orig:
        rho = math.sqrt(x**2 + y**2)
        phi = math.atan2(y, x)
        if phi < 0: phi += 2 * math.pi
        
        # 核心映射：将 360 度压缩至 300 度 (对于C5)
        new_phi = phi * factor
        
        nx = round(rho * math.cos(new_phi), 6)
        ny = round(rho * math.sin(new_phi), 6)
        
        # 简单的去重逻辑，防止拼接缝处的格点重叠
        is_duplicate = False
        for sx, sy in seen_points:
            if math.hypot(nx - sx, ny - sy) < a * 0.3: # 距离过近视为重复
                is_duplicate = True
                break
        
        if not is_duplicate:
            final_points.append((nx, ny))
            seen_points.append((nx, ny))

    # 4. 将点转化为 GDSII 图形
    for px, py in final_points:
        # Layer 1 为光子晶体孔，用于 EBL 曝光
        circle = gdspy.Round((px, py), r_hole, tolerance=0.001, layer=1)
        cell.add(circle)

    # 5. 保存与预览
    lib.write_gds(filename)
    print(f"成功！版图已保存至: {filename}")
    
    # 绘图预览 (不使用 plt.show 以防卡死)
    plt.figure(figsize=(8,8))
    px, py = zip(*final_points)
    plt.scatter(px, py, s=1, c='blue')
    plt.gca().set_aspect('equal')
    plt.savefig("disclination_preview.png")
    print("预览图已保存为 disclination_preview.png")

# 执行生成
generate_disclination_gds(a=0.48, r_hole=0.12, rings=25)
# --- 缝合算法核心逻辑 ---

def apply_stitching(orig_x, orig_y, factor=5/6):
    rho = math.sqrt(orig_x**2 + orig_y**2)
    phi_orig = math.atan2(orig_y, orig_x) # 范围 -pi 到 pi
    
    # 将角度标准化到 0 到 2pi
    if phi_orig < 0:
        phi_orig += 2 * math.pi
    
    # --- 关键：缝合步骤 ---
    # 我们把整个 2pi 的逻辑坐标，映射到 (2pi * factor) 的物理空间
    # 这就自动完成了“缝合”，因为 2pi 处的点和 0 处的点重合了
    new_phi = phi_orig * factor
    
    new_x = rho * math.cos(new_phi)
    new_y = rho * math.sin(new_phi)
    return new_x, new_y