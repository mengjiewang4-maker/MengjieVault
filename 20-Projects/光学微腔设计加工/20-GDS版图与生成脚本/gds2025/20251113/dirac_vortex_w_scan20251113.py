import gdsfactory as gf
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 参数设置
# ============================================
# 1. 物理参数
a = 0.49            # 晶格常数 (µm)
r_hole = 0.32 * a   # 孔半径
m0 = 0.05           # 调制幅度
R = 5 * a           # 调制半径
alpha = 4           # 陡峭度
w = +1              # 拓扑荷
Nx, Ny = 20, 20     # 晶格大小

# 2. 图层定义 (GDS Layer, DataType)
LAYER_DEVICE = (1, 0)    # 光子晶体结构层
LAYER_MARKER = (100, 0)  # 中心标记层 (设置为 100 以便区分)

# ============================================
# 辅助函数
# ============================================
def triangle(radius, rotation_deg=0):
    """生成三角孔多边形点集"""
    pts = []
    for i in range(3):
        theta = np.deg2rad(rotation_deg + i * 120)
        pts.append((radius * np.cos(theta), radius * np.sin(theta)))
    return np.array(pts)

def vortex_shift(x, y):
    """计算 Dirac-Vortex 位移场"""
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    # 防止除零 (虽然 x,y 不会完全为0，但为了鲁棒性)
    if r == 0: return 0, 0, 0, 0, 0
    
    amplitude = m0 * np.tanh((r / R) ** alpha)
    dx = amplitude * np.cos(w * phi)
    dy = amplitude * np.sin(w * phi)
    return dx, dy, r, phi, amplitude

# ============================================
# 主程序：生成 GDS
# ============================================
c = gf.Component("dirac_vortex_with_marker")
all_x, all_y, all_amp, all_phi = [], [], [], []

# 1. 生成蜂窝晶格结构
for i in range(-Nx, Nx):
    for j in range(-Ny, Ny):
        x0 = a * (i + 0.5 * (j % 2))
        y0 = np.sqrt(3)/2 * a * j

        # 区分 A/B 子格 (这里简化处理，假设中心附近的点都进行计算)
        # 注意：蜂窝晶格有两个格点，这里用简单的奇偶逻辑近似生成
        dx, dy = 0, 0
        if (i + j) % 2 != 0: # 仅对部分格点施加位移（简化逻辑，具体视晶格定义而定）
             dx, dy, _, _, _ = vortex_shift(x0, y0)

        # 生成三角形并移动
        tri = triangle(r_hole, rotation_deg=30)
        tri = tri + np.array([x0 + dx, y0 + dy])
        c.add_polygon(tri, layer=LAYER_DEVICE)

        # 记录数据用于绘图
        all_x.append(x0 + dx)
        all_y.append(y0 + dy)
        # 重新计算实际位置的参数用于绘图颜色
        r_curr = np.sqrt((x0+dx)**2 + (y0+dy)**2)
        phi_curr = np.arctan2(y0+dy, x0+dx)
        all_amp.append(m0 * np.tanh((r_curr / R) ** alpha))
        all_phi.append(phi_curr)

# 2. 添加中心标记 (十字准星) 到独立图层
marker_len = 2 * a  # 十字线长度
marker_wid = 0.1 * a # 十字线宽度

# 垂直线
rect_v = gf.components.rectangle(size=(marker_wid, marker_len), layer=LAYER_MARKER)
ref_v = c.add_ref(rect_v)
ref_v.move((-marker_wid/2, -marker_len/2)) # 居中

# 水平线
rect_h = gf.components.rectangle(size=(marker_len, marker_wid), layer=LAYER_MARKER)
ref_h = c.add_ref(rect_h)
ref_h.move((-marker_len/2, -marker_wid/2)) # 居中

# (可选) 添加一个圆圈
circle_marker = gf.components.circle(radius=marker_len/2, layer=LAYER_MARKER)
c.add_ref(circle_marker).move((0,0))

# ============================================
# 输出与保存
# ============================================
gds_filename = "dirac_vortex_marked_L100.gds"
c.write_gds(gds_filename)
print(f"✅ GDS 已保存: {gds_filename}")
print(f"   - 结构图层: {LAYER_DEVICE}")
print(f"   - 标记图层: {LAYER_MARKER} (含十字与圆)")

# ============================================
# 绘图验证
# ============================================
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(all_x, all_y, s=2, c='gray', alpha=0.5, label='Structure')
# 绘制中心红十字
ax.plot([-marker_len/2, marker_len/2], [0, 0], 'r-', linewidth=2, label='Marker (Layer 100)')
ax.plot([0, 0], [-marker_len/2, marker_len/2], 'r-', linewidth=2)
ax.set_aspect('equal')
ax.legend()
ax.set_title(f"GDS Layout Preview\nMarker on Layer {LAYER_MARKER[0]}")
plt.tight_layout()
plt.show()