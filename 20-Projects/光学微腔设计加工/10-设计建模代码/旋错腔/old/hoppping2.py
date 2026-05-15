import numpy as np
import matplotlib.pyplot as plt

def plot_perfect_hopping_network(coords_file, w=0.2, v=1.0):
    # 1. 加载坐标
    try:
        coords = np.loadtxt(coords_file, delimiter=',')
    except:
        print("Error: Could not find final_coords.txt")
        return
    num_sites = len(coords)
    
    # 2. 设置绘图：白色背景，确保 equal aspect 以防几何变形
    plt.figure(figsize=(10, 10), facecolor='white')
    ax = plt.gca()
    
    # 定义最近邻判定距离
    # 这里假设坐标单位是归一化的(a~1)。如果是um，请使用 0.35 并在 set("x", ...)时乘1e-6
    nn_dist_threshold = 0.7  
    
    print(f"Plotting network for {num_sites} sites with topological color mapping...")
    
    # 3. 建立跳跃邻接矩阵（用于颜色映射）
    H_temp = np.zeros((num_sites, num_sites))
    
    # 第一次遍历：判定强弱键
    # 这里必须使用与 TB 计算脚本相同的 $w/v$ 分配逻辑（例如径向逻辑）
    for i in range(num_sites):
        xi, yi = coords[i]
        ri = np.linalg.norm(coords[i])
        for j in range(i + 1, num_sites):
            xj, yj = coords[j]
            d = np.sqrt((xi-xj)**2 + (yi-yj)**2)
            
            if 0.1 < d < nn_dist_threshold:
                # 使用相同的径向强弱键判断逻辑 (假设 a_eff = 1.0)
                mid_r = np.linalg.norm((coords[i]+coords[j])/2)
                if (int(mid_r / 0.5) % 2 == 0):
                    H_temp[i, j] = v  # 强键 (胞间)
                else:
                    H_temp[i, j] = w  # 弱键 (胞内)

    # 4. 第二次遍历：绘制连线 (Hopping Lines) - 设置 zorder=1
    # 目标：强键用绿色实线，弱键用浅绿色虚线
    for i in range(num_sites):
        xi, yi = coords[i]
        for j in range(i + 1, num_sites):
            t_ij = H_temp[i, j]
            if t_ij > 0:
                xj, yj = coords[j]
                if t_ij == v:
                    # 强键：鲜艳的绿色实线
                    plt.plot([xi, xj], [yi, yj], color='#2ecc71', lw=1.2, alpha=0.9, zorder=1)
                else:
                    # 弱键：浅绿色/灰色，线宽减小，透明度增加
                    plt.plot([xi, xj], [yi, yj], color='#a9dfbf', lw=0.6, alpha=0.4, ls='--', zorder=1)

    # 5. 第三次遍历：绘制格点 (Points) - 设置 zorder=2，实现“点压线”
    for i in range(num_sites):
        r = np.linalg.norm(coords[i])
        # 目标：高亮中心天蓝色奇点
        if r < 0.2:
            # 天蓝色 (#3498db)，尺寸加大
            plt.scatter(coords[i,0], coords[i,1], c='#3498db', s=60, zorder=2, edgecolors='none')
        else:
            # 普通格点用深色 (#2c3e50)，尺寸适中
            plt.scatter(coords[i,0], coords[i,1], c='#2c3e50', s=20, zorder=2, edgecolors='none')

    # 6. 视角缩放与美化
    plt.axis('equal')
    plt.axis('off') # 隐藏轴线
    
    # 核心：局部放大到中心奇点 (复现原图视角)
    plt.xlim(-3.8, 3.8)
    plt.ylim(-3.8, 3.8)
    
    plt.title("Reproduced Topological Hopping Network", fontsize=16)
    
    plt.savefig("reproduced_network.png", dpi=300, bbox_inches='tight')
    plt.show()

# 运行复现（假设 w=0.2, v=1.0 能够产生明显的颜色区分）
if __name__ == "__main__":
    plot_perfect_hopping_network("final_coords.txt", w=0.2, v=1.0)