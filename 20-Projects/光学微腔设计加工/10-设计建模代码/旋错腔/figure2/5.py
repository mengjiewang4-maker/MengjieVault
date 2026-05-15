import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设置
# ==========================================
target_n = 5       # 手动改为 3, 5, 6
Nx, Ny = 8, 8      
a = 1.0            
delta = 0.35       # 胞内松 (delta > 0.25)
t_intra = 0.2      # 胞内弱耦合
t_inter = 1.0      # 胞外强耦合 (拓扑相)

# ==========================================
# 2. 自动化流程：晶胞内切割版
# ==========================================
plt.figure(figsize=(20, 5))

# --- STEP 1: 晶胞内切割 (原点在晶胞中心) ---
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        # 核心改动：不再偏移 0.5a，直接从 0 开始
        # 这样 x=0 和 y=0 的切割线会正好穿过 i=0, j=0 那个晶胞的中心
        cx, cy = i * a, j * a
        
        basis = np.array([
            [cx - delta, cy - delta], [cx + delta, cy - delta],
            [cx - delta, cy + delta], [cx + delta, cy + delta]
        ])
        
        # 只保留落在第一象限内的原子 (由于原点在晶胞中心，每个晶胞会有部分原子被切掉)
        # 在 i=0, j=0 的晶胞中，只有 [cx+d, cy+d] 这一个原子会被留下
        for atom in basis:
            if atom[0] >= 0 and atom[1] >= 0:
                q1_atoms.append(atom)

q1_pos = np.array(q1_atoms)

plt.subplot(141)
plt.scatter(q1_pos[:,0], q1_pos[:,1], s=15, c='royalblue', edgecolors='k')
# 绘制切割线：现在它们穿过了最左下角的晶胞
plt.axvline(0, color='red', linestyle='--', alpha=0.8)
plt.axhline(0, color='red', linestyle='--', alpha=0.8)
plt.gca().set_aspect('equal')
plt.title("Step 1: Cell-centered Cut\n(Cutting through unit cell)")

# --- STEP 2: 角度映射 (90 -> 360/n) ---
coeff = (360.0 / target_n) / 90.0
stretched_list = []
for x, y in q1_pos:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * coeff
    stretched_list.append([r * np.cos(phi), r * np.sin(phi)])
stretched_unit = np.array(stretched_list)

plt.subplot(142)
plt.scatter(stretched_unit[:,0], stretched_unit[:,1], s=15, c='forestgreen', edgecolors='k')
plt.gca().set_aspect('equal')
plt.title(f"Step 2: Transform to C{target_n}")

# --- STEP 3: 旋转拼接 (完美缝合) ---
final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_unit @ rot.T)

pos = np.array(final_pos)
# 严格去重：由于切割线经过原子间，缝合处可能会有极近的点
_, indices = np.unique(np.round(pos, 5), axis=0, return_index=True)
pos = pos[indices]
# 圆形截断
pos = pos[np.linalg.norm(pos, axis=1) < Nx * a * 0.85]

plt.subplot(143)
plt.scatter(pos[:,0], pos[:,1], s=10, c='gray', alpha=0.3)
plt.gca().set_aspect('equal')
plt.title(f"Step 3: C{target_n} Stitched Lattice")

# --- STEP 4: 拓扑态求解 ---
num = len(pos)
H = np.zeros((num, num), dtype=complex)
# 判定距离
d_small = (a - 2 * delta) * 1.15 # 胞外 (紧)
d_large = (2 * delta) * 1.15     # 胞内 (松)

for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        if r < d_small:
            H[i, j] = H[j, i] = t_inter
        elif r < d_large:
            H[i, j] = H[j, i] = t_intra

E, V = np.linalg.eigh(H)
mid_idx = len(E) // 2
mode = V[:, mid_idx]
intensity = np.abs(mode)**2

plt.subplot(144)
plt.scatter(pos[:,0], pos[:,1], c=np.angle(mode), s=intensity*15000+10, cmap="twilight", edgecolors='k', lw=0.2)
plt.gca().set_aspect('equal')
plt.title(f"Step 4: Disclination Mode\nE={E[mid_idx]:.4f}")

plt.tight_layout()
plt.show()