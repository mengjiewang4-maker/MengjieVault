import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def solve_radial_ssh_disclination(coords_file, w=0.15, v=1.0, t_nnn=0.02):
    # 1. 加载坐标
    try:
        coords = np.loadtxt(coords_file, delimiter=',')
    except:
        print("错误：未找到 final_coords.txt，请确保文件在当前目录下。")
        return
    
    num_sites = len(coords)
    a = 0.48  # 晶格常数
    
    # 2. 构建哈密顿矩阵
    H = np.zeros((num_sites, num_sites), dtype=complex)
    
    # 判定距离
    nn_dist = 0.35    # 最近邻
    nnn_dist = 0.55   # 次近邻
    
    print(f"正在构建哈密顿矩阵 (格点数: {num_sites})...")
    
    for i in range(num_sites):
        xi, yi = coords[i]
        for j in range(i + 1, num_sites):
            xj, yj = coords[j]
            d = np.sqrt((xi-xj)**2 + (yi-yj)**2)
            
            if d < nn_dist:
                # --- 核心修改：径向二聚化判断 ---
                mid_x, mid_y = (xi + xj) / 2, (yi + yj) / 2
                dist_to_center = np.sqrt(mid_x**2 + mid_y**2)
                
                # 逻辑：以 0.5*a 为周期切换强弱键
                # 这种径向排列能强行在中心奇点制造拓扑不连续
                if (int(dist_to_center / (0.5 * a)) % 2 == 0):
                    H[i, j] = H[j, i] = v  # 强键
                else:
                    H[i, j] = H[j, i] = w  # 弱键
                    
            elif d < nnn_dist:
                H[i, j] = H[j, i] = t_nnn

    # 3. 对角化求解
    print("正在计算能谱...")
    energies, wavs = eigh(H)
    
    # 4. 绘图
    plt.figure(figsize=(12, 5))
    
    # --- 左图：能谱 ---
    plt.subplot(1, 2, 1)
    plt.plot(energies, 'ko', markersize=1, alpha=0.3)
    
    # 自动识别带隙中心的态 (零能模)
    zero_modes = np.where(np.abs(energies) < 0.15)[0]
    plt.plot(zero_modes, energies[zero_modes], 'ro', markersize=4, label='Disclination States')
    
    plt.axhline(y=0, color='blue', linestyle='--', linewidth=0.5)
    plt.title("Energy Spectrum (Radial SSH)")
    plt.ylabel("Energy")
    plt.legend()

    # --- 右图：空间局域化 ---
    plt.subplot(1, 2, 2)
    # 选取能量最接近 0 的那个态
    target_idx = np.argmin(np.abs(energies))
    prob = np.abs(wavs[:, target_idx])**2
    
    # 使用 log 尺度或调整 s 使得中心点更明显
    sc = plt.scatter(coords[:,0], coords[:,1], c=prob, s=10, cmap='magma', edgecolors='none')
    plt.colorbar(sc, label="Probability Density")
    plt.title(f"Core Localization (State {target_idx})")
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig("tb_radial_result.png")
    plt.show()
    
    print(f"完成！中心态索引: {target_idx}，能量: {energies[target_idx]:.6f}")

if __name__ == "__main__":
    # 参数建议：w 越小，中心局域化越强
    solve_radial_ssh_disclination("final_coords.txt", w=0.1, v=1.0, t_nnn=0.03)