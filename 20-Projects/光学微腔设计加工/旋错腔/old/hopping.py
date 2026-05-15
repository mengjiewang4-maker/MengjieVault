import numpy as np
import matplotlib.pyplot as plt

def plot_hopping_network(coords_file, a=0.48):
    # 1. 加载坐标
    coords = np.loadtxt(coords_file, delimiter=',')
    num_sites = len(coords)
    
    # 2. 设置绘图
    plt.figure(figsize=(10, 10), facecolor='white')
    ax = plt.gca()
    
    # 3. 定义判定距离 (与 TB 脚本一致)
    nn_dist = 0.35    # 最近邻判定
    nnn_dist = 0.55   # 次近邻判定 (可选)

    print(f"正在绘制 {num_sites} 个点的连通网络...")
    
    # 4. 遍历所有点对，绘制连线 (Hopping Lines)
    # 为了提高速度，只遍历一次上三角矩阵
    for i in range(num_sites):
        xi, yi = coords[i]
        for j in range(i + 1, num_sites):
            xj, yj = coords[j]
            dist = np.sqrt((xi-xj)**2 + (yi-yj)**2)
            
            # 如果是最近邻，画绿色的线
            if 0.2 < dist < nn_dist:
                # 绘制连线：[x1, x2], [y1, y2]
                # lw 为线宽，alpha 为透明度
                plt.plot([xi, xj], [yi, yj], color='#2ecc71', lw=0.8, alpha=0.6, zorder=1)
            
            # 如果你想画次近邻(NNN)，可以用浅灰色虚线表示
            # elif nn_dist < dist < nnn_dist:
            #     plt.plot([xi, xj], [yi, yj], color='gray', lw=0.3, alpha=0.2, ls='--', zorder=1)

    # 5. 绘制格点 (Points)
    # 中心奇点用蓝色，其他用黑色或深灰色
    for i in range(num_sites):
        r = np.sqrt(coords[i,0]**2 + coords[i,1]**2)
        if r < 0.1: # 标记中心点
            plt.scatter(coords[i,0], coords[i,1], c='#3498db', s=30, zorder=2, edgecolors='white')
        else:
            plt.scatter(coords[i,0], coords[i,1], c='#2c3e50', s=10, zorder=2)

    # 6. 图表美化
    plt.axis('equal')
    plt.axis('off') # 隐藏轴线，更有艺术感
    plt.title("Real-space Disclination Hopping Network", fontsize=15)
    
    plt.savefig("hopping_network_reproduction.png", dpi=300, bbox_inches='tight')
    plt.show()

# 运行复现
if __name__ == "__main__":
    plot_hopping_network("final_coords.txt")
