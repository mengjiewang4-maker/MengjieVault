import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ==========================================
# 1. 物理与几何参数设置
# ==========================================
target_n = 5       # 定义旋错对称性 (例如 5 代表 C5 对称性，将 360° 空间分为 5 份)
Nx, Ny = 10, 10    # 定义初始矩形区域的横向和纵向原胞数量
a = 1.0            # 理想光子晶体单位晶格常数
delta = 0.15       # 位移参数：决定胞内/胞间距。delta > 0 且 |t2| > |t1| 时为拓扑非平凡相

# 光子晶体孔参数
r_hole = 0.20 * a   # 设置空气孔半径，通常取 0.2a 左右以形成能隙

# 紧束缚模型 (Tight-Binding) 耦合参数
t1 = -0.1          # 胞内跳跃系数 (对应物理上较远的孔间距，耦合弱)
t2 = -1.0          # 胞间跳跃系数 (对应物理上较近的孔间距，耦合强)
tn = t2 / 1.414    # 旋错中心处，由于几何挤压导致的特殊跨区域耦合强度

# ==========================================
# ==========================================
# 步骤 2a: 在第一象限 (Q1) 生成基础的四原子原胞阵列
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a  # 计算每个原胞的中心坐标
        # 定义一个原胞内的四个原子位点 (基于 SSH 模型扩展的二维版)
        basis = np.array([
            [cx-delta, cy-delta], [cx+delta, cy-delta],
            [cx-delta, cy+delta], [cx+delta, cy+delta]
        ])
        for atom in basis:
            # 只保留第一象限的原子，防止拼接重叠
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

# 步骤 2b: 角度映射 (将 90° 的扇区拉伸或压缩到 360/target_n 度)
coeff = (360.0 / target_n) / 90.0  # 计算拉伸系数
stretched_unit = []
for x, y in q1_pos:
    r = np.sqrt(x**2 + y**2)       # 计算极径
    phi = np.arctan2(y, x) * coeff # 计算拉伸后的极角
    stretched_unit.append([r * np.cos(phi), r * np.sin(phi)]) # 转回直角坐标
stretched_unit = np.array(stretched_unit)

# 步骤 2c: 旋转拼接 (将拉伸后的扇区旋转 target_n 次，填满 360°)
final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n) # 计算旋转角度
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]) # 旋转矩阵
    final_pos.extend(stretched_unit @ rot.T) # 旋转并加入列表

pos = np.array(final_pos)

# 步骤 2d: 边缘截断 (切除外部原子，使整体结构呈现圆形，美观且符合实验样品形状)
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-2) * a]

# ==========================================
# 3. 构建哈密顿量与数值求解
# ==========================================
num = len(pos) # 总原子(空气孔)数量
H = np.zeros((num, num), dtype=complex) # 初始化全零哈密顿矩阵
d_intra = 2 * delta     # 理论胞内距离
d_inter = a - 2 * delta # 理论胞间距离

# 遍历所有原子对，根据距离分配耦合强度 (跳跃能)
for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j]) # 计算两点间距
        if 0.05 < r < d_intra * 1.2:        # 如果满足胞内距离
            H[i, j] = H[j, i] = t1
        elif d_intra * 1.2 <= r < d_inter * 1.2: # 如果满足胞间距离
            H[i, j] = H[j, i] = t2
        elif r < 0.5: # 针对中心旋错点处极近原子的强耦合处理
            H[i, j] = H[j, i] = tn

# 对矩阵进行对角化，求解能量(特征值)和波函数(特征向量)
E, V = np.linalg.eigh(H)

# 自动寻找局域态：计算反参与率 (IPR)，IPR 越高代表态越局域
iprs = np.sum(np.abs(V)**4, axis=0) # 计算每个模态的 IPR
target_idx = np.argmax(iprs)        # 找到最局域的态索引 (通常是能隙中的旋错模)

mode = V[:, target_idx]             # 提取该模态的波函数
intensity = np.abs(mode)**2         # 计算强度分布
norm_intensity = intensity / np.max(intensity) # 归一化强度

# ==========================================
# 4. 可视化
# ==========================================
fig = plt.figure(figsize=(20, 6.5)) # 创建画布

# --- 图 1：能谱图 ---
ax1 = plt.subplot(131)
plt.scatter(range(len(E)), E, s=5, c='gray', alpha=0.5) # 绘制所有能级
plt.scatter(target_idx, E[target_idx], color='red', s=50, edgecolors='k', label='Cavity Mode') # 突出拓扑态
plt.xlabel("Mode Index")
plt.ylabel("Normalized Frequency (a/λ)")
plt.title(f"Spectrum (C{target_n})")
plt.legend()

# --- 图 2：仅空气孔几何结构 ---
ax2 = plt.subplot(132)
for p in pos:
    # 在每个原子位点画一个圆圈，代表空气孔
    circle = Circle((p[0], p[1]), r_hole, color='white', ec='gray', lw=0.4)
    ax2.add_patch(circle)
ax2.set_facecolor('lightgray') # 灰色背景代表硅基底
plt.gca().set_aspect('equal')
plt.xlim(-Nx*0.6, Nx*0.6); plt.ylim(-Nx*0.6, Nx*0.6) # 设置坐标轴范围
plt.title("Air Hole Geometry")

# --- 图 3：拓扑态场分布 ---
ax3 = plt.subplot(133)
for p in pos:
    # 绘制底层空气孔作为背景
    circle = Circle((p[0], p[1]), r_hole, color='white', ec='gray', lw=0.4)
    ax3.add_patch(circle)
# 绘制波函数：颜色代表相位 (hsv)，大小代表强度
mask = norm_intensity > 0.001 # 仅显示强度明显的点
plt.scatter(pos[mask, 0], pos[mask, 1], c=np.angle(mode[mask]), 
            s=norm_intensity[mask] * 1500, cmap="hsv", edgecolors='k', zorder=10)
ax3.set_facecolor('lightgray')
plt.gca().set_aspect('equal')
plt.xlim(-Nx*0.6, Nx*0.6); plt.ylim(-Nx*0.6, Nx*0.6)
plt.title("Localized Cavity Mode")

plt.tight_layout() # 自动调整布局防止重叠
plt.show() # 显示图形