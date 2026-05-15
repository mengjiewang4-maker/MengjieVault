import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设置 (为了拓扑态更明显，拉大 t1 和 t2 的差距)
# ==========================================
target_n = 5       # 旋错对称性: 3, 5, 6
Nx, Ny = 10, 10    # 稍微增大尺寸，对比更强烈
a = 1.0            
delta = 0.15       # 较小的 delta 使胞内耦合更内聚

t1 = -0.1          # 胞内 (弱)
t2 = -1.0          # 胞间 (强) - 拓扑非平凡相的核心
tn = t2 / 1.414    # 旋错中心跨区域耦合

# ==========================================
# 2. 构建几何结构 (旋错拼接)
# ==========================================
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        basis = np.array([
            [cx-delta, cy-delta], [cx+delta, cy-delta],
            [cx-delta, cy+delta], [cx+delta, cy+delta]
        ])
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

# 角度映射
coeff = (360.0 / target_n) / 90.0
stretched_unit = []
for x, y in q1_pos:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * coeff
    stretched_unit.append([r * np.cos(phi), r * np.sin(phi)])
stretched_unit = np.array(stretched_unit)

# 旋转拼接
final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_unit @ rot.T)

pos = np.array(final_pos)
# 边缘截断
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-2) * a]

# ==========================================
# 3. 构建哈密顿量与求解
# ==========================================
num = len(pos)
H = np.zeros((num, num), dtype=complex)
d_intra = 2 * delta
d_inter = a - 2 * delta

for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        if 0.05 < r < d_intra * 1.2:
            H[i, j] = H[j, i] = t1
        elif d_intra * 1.2 <= r < d_inter * 1.2:
            H[i, j] = H[j, i] = t2
        elif r < 0.5: # 针对中心极近原子的特殊耦合
            H[i, j] = H[j, i] = tn

E, V = np.linalg.eigh(H)

# --- 关键：自动寻找最局域化的拓扑态 ---
# 计算每个态的 IPR (Inverse Participation Ratio)，IPR 越大越局域
iprs = np.sum(np.abs(V)**4, axis=0) / (np.sum(np.abs(V)**2, axis=0)**2)
target_idx = np.argmax(iprs) # 找到全局最“亮”的点

mode = V[:, target_idx]
intensity = np.abs(mode)**2
# 归一化强度用于绘图显示
norm_intensity = intensity / np.max(intensity)

# ==========================================
# 4. 绘图展示
# ==========================================
plt.figure(figsize=(14, 6))

# --- 左图：能谱图 (显示能带隙和零能模) ---
plt.subplot(121)
plt.scatter(range(len(E)), E, s=5, c='k', alpha=0.5)
plt.scatter(target_idx, E[target_idx], color='red', s=40, label='Target Localized Mode')
plt.xlabel("Mode Index")
plt.ylabel("Energy")
plt.title("Energy Spectrum & Gap")
plt.legend()
plt.grid(alpha=0.3)

# --- 右图：拓扑态分布 (优化后的视觉映射) ---
plt.subplot(122)

# 1. 绘制底层所有格点 (浅色背景)
plt.scatter(pos[:,0], pos[:,1], c='lightgray', s=10, alpha=0.2, edgecolors=None)

# 2. 绘制波函数 (仅显示显著的部分)
# 只有强度大于 1% 的点才会显示颜色，突出中心
mask = norm_intensity > 0.01 
scatter = plt.scatter(pos[mask, 0], pos[mask, 1], 
                      c=np.angle(mode[mask]), 
                      s=norm_intensity[mask] * 500, # 动态调整点的大小
                      cmap="hsv", # 使用 HSV 更好地观察相位循环
                      edgecolors='k', lw=0.5, alpha=0.9, zorder=10)

plt.colorbar(scatter, label="Phase (Angle)")
plt.gca().set_aspect('equal')
plt.xlim(-Nx*0.6, Nx*0.6); plt.ylim(-Nx*0.6, Nx*0.6)
plt.title(f"Disclination Mode (C{target_n})\nEnergy: {E[target_idx]:.4f}")

plt.tight_layout()
plt.show()