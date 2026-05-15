import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 关键参数调整区
# ==========================================
target_n = 5       # 目标对称性
Nx, Ny = 8, 8      
a = 1.0            

# ⭐ 调整 delta：delta 越小，中心三个点靠得越近
# 建议尝试 0.1 (极度聚集) 到 0.2 (中等聚集)
delta = 0.12       

# 物理参数：胞内紧、胞外松
t_intra = 1.0      
t_inter = 0.2      

# ==========================================
# 2. 自动化流程
# ==========================================
plt.figure(figsize=(20, 5))

# --- STEP 1: 晶胞内切割 (Cell-centered Cut) ---
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        # 生成胞内 4 个原子
        basis = np.array([
            [cx - delta, cy - delta], [cx + delta, cy - delta],
            [cx - delta, cy + delta], [cx + delta, cy + delta]
])
        # 严格保留第一象限原子 (含坐标为 0 的点)
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

plt.subplot(141)
plt.scatter(q1_pos[:,0], q1_pos[:,1], s=20, c='royalblue')
plt.axvline(0, color='r', ls='--'); plt.axhline(0, color='r', ls='--')
plt.gca().set_aspect('equal')
plt.title(f"Step 1: Cell-centered\n(delta={delta})")

# --- STEP 2: 角度映射 ---
coeff = (360.0 / target_n) / 90.0
stretched_unit = []
for x, y in q1_pos:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * coeff
    stretched_unit.append([r * np.cos(phi), r * np.sin(phi)])
stretched_unit = np.array(stretched_unit)

plt.subplot(142)
plt.scatter(stretched_unit[:,0], stretched_unit[:,1], s=20, c='green')
plt.gca().set_aspect('equal'); plt.title("Step 2: Angular Mapping")

# --- STEP 3: 旋转拼接 (看中心聚集情况) ---
final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_unit @ rot.T)
pos = np.array(final_pos)

# 严格去重 (防止重叠点)
_, indices = np.unique(np.round(pos, 6), axis=0, return_index=True)
pos = pos[indices]
pos = pos[np.linalg.norm(pos, axis=1) < Nx * a * 0.8]

plt.subplot(143)
plt.scatter(pos[:,0], pos[:,1], s=15, c='gray', alpha=0.5)
# 放大中心观察
plt.xlim(-2, 2); plt.ylim(-2, 2)
plt.gca().set_aspect('equal'); plt.title("Step 3: Center Zoom-in")

# --- STEP 4: 拓扑局域态 ---
num = len(pos)
H = np.zeros((num, num))
d_intra = (2 * delta) * 1.2
d_inter = (a - 2 * delta) * 1.2

for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        if r < d_intra: H[i, j] = H[j, i] = t_intra
        elif r < d_inter: H[i, j] = H[j, i] = t_inter

E, V = np.linalg.eigh(H)
mode = V[:, len(E)//2]
intensity = np.abs(mode)**2

plt.subplot(144)
plt.scatter(pos[:,0], pos[:,1], c=np.angle(mode), s=intensity*10000+10, cmap="twilight")
plt.gca().set_aspect('equal')
plt.title(f"Step 4: Mode Profile\n(Center Aggregated)")

plt.tight_layout(); plt.show()