import numpy as np
import matplotlib.pyplot as plt
import math

def generate_perfect_c5_lattice(a=0.48, rings=20):
    """
    a: 晶格常数 (um)
    rings: 环数，决定阵列大小
    """
    print(f"开始生成对称修正后的 C5 旋错结构...")
    
    # 1. 参数设置
    s = 5/6.0  # 旋错因子 (C6 -> C5)
    raw_points = []
    
    # 2. 生成原始 C6 晶格并进行 Volterra 映射
    # 遍历足够大的范围以确保覆盖
    search_range = int(rings * 1.5)
    for i in range(-search_range, search_range):
        for j in range(-search_range, search_range):
            # 蜂窝晶格的 A/B 子晶格坐标
            xa = a * (i + 0.5 * j)
            ya = a * (np.sqrt(3)/2 * j)
            xb = xa
            yb = ya + a / np.sqrt(3)
            
            for px, py in [(xa, ya), (xb, yb)]:
                rho = np.sqrt(px**2 + py**2)
                if 0 < rho <= rings * a:
                    phi = math.atan2(py, px)
                    if phi < 0: phi += 2 * math.pi
                    
                    # 只保留 [0, 300度] 范围内的点进行压缩映射
                    if phi <= 2 * math.pi * s:
                        new_phi = phi / s
                        nx = rho * math.cos(new_phi)
                        ny = rho * math.sin(new_phi)
                        raw_points.append([nx, ny])

    # 3. 基础去重
    final_coords = [[0.0, 0.0]] # 强制包含中心点
    for pt in raw_points:
        is_duplicate = False
        for f_pt in final_coords:
            if np.linalg.norm(np.array(pt) - np.array(f_pt)) < a * 0.6:
                is_duplicate = True
                break
        if not is_duplicate:
            final_coords.append(pt)

    final_coords = np.array(final_coords)

    # 4. ⭐ 核心步骤：强制中心五个点完美对称 (C5 Symmetry Fix)
    # 计算所有点到中心的距离
    dist_to_origin = np.linalg.norm(final_coords, axis=1)
    
    # 找到距离中心最近的一圈（排除原点本身）
    # 在 a=0.48 时，第一圈孔通常在距离 0.4-0.6um 处
    core_mask = (dist_to_origin > 0.1) & (dist_to_origin < a * 1.2)
    core_indices = np.where(core_mask)[0]

    if len(core_indices) >= 5:
        # 如果找到的点多于5个，取最近的5个
        sorted_indices = core_indices[np.argsort(dist_to_origin[core_indices])][:5]
        
        # 强制这 5 个点分布在 72 度的倍数上
        # r_fix 是这五个点到中心的平均距离，通常接近 a
        r_fix = a 
        start_angle = np.pi / 2 # 让一个孔落在正上方，或者设为 0
        
        for k, idx in enumerate(sorted_indices):
            angle = start_angle + k * (2 * np.pi / 5)
            final_coords[idx, 0] = r_fix * np.cos(angle)
            final_coords[idx, 1] = r_fix * np.sin(angle)
        print("✅ 已完成中心 C5 对称性强制修正。")

    return final_coords

def save_and_plot(coords, a=0.48):
    # 保存 TXT
    np.savetxt("final_coords.txt", coords, fmt='%.6f', delimiter=', ')
    print(f"✅ 坐标已保存至 final_coords.txt，总孔数: {len(coords)}")

    # 绘制 Hopping Network (复现你要求的绿色连线图)
    plt.figure(figsize=(10, 10), facecolor='white')
    num = len(coords)
    
    # 绘制连线 (Hopping)
    print("正在绘制跳跃网络...")
    for i in range(num):
        for j in range(i + 1, num):
            d = np.linalg.norm(coords[i] - coords[j])
            if 0.2 < d < a * 1.1: # 最近邻距离判断
                plt.plot([coords[i,0], coords[j,0]], [coords[i,1], coords[j,1]], 
                         color='#2ecc71', lw=1.0, alpha=0.7, zorder=1)

    # 绘制格点
    # 普通点
    plt.scatter(coords[:,0], coords[:,1], c='#2c3e50', s=15, zorder=2, edgecolors='none')
    # 中心点高亮
    plt.scatter(0, 0, c='#3498db', s=50, zorder=3, edgecolors='white')

    plt.axis('equal')
    plt.axis('off')
    # 局部放大查看中心对称性
    plt.xlim(-a*5, a*5)
    plt.ylim(-a*5, a*5)
    plt.title("Symmetry-Corrected C5 Disclination", fontsize=15)
    plt.savefig("reproduced_network.png", dpi=300)
    plt.show()

# --- 执行脚本 ---
if __name__ == "__main__":
    coords = generate_perfect_c5_lattice(a=0.48, rings=25)
    save_and_plot(coords, a=0.48)