import gdspy
import numpy as np
import sys

# 检查 gdspy 版本
print(f"gdspy version: {gdspy.__version__}")
if int(gdspy.__version__[0]) < 1:
    print("警告：此脚本需要 gdspy 1.0 或更高版本。")

def create_dirac_vortex_gds(
    w: int = 1,
    R_vortex_um: float = 25.0,
    a_lattice_um: float = 0.49,
    r_hole_frac: float = 0.32,
    m0_mod_um: float = 0.05,
    alpha_shape: float = 4.0,
    n_hex_layers: int = 150,
    gds_filename: str = "dirac_vortex.gds",
    use_experimental_center: bool = True
) -> None:
    """
    根据 "Dirac-vortex topological cavities" (Nature Nanotechnology) 一文
    生成 GDSII 版图文件, 并添加图 S3 中的标注和辅助线。

    参数:
    w: 拓扑绕线数 (Winding Number)。
    R_vortex_um: 涡旋半径 (R)，单位: 微米 (µm)。
                 注意 2R=50um 是实验中使用的值。
    a_lattice_um: 晶格常数 (a)，单位: µm。实验值为 490 nm。
    r_hole_frac: 三角形气孔尺寸 (半径 r) 与 a 的比例。
                 文章中为 r = 0.32a。
    m0_mod_um: 最大调制幅度 (m0)，单位: µm。实验值为 50 nm。
    alpha_shape: 势阱形状因子 (α)。α=4 是文中的选择。
    n_hex_layers: 生成的光子晶格的六边形层数 (用于包层)。
    gds_filename: 输出的 GDSII 文件名。
    use_experimental_center: 
        True:  为所有w值使用 w=1 的腔体中心 (复现实验光谱)。
        [cite_start]False: 为每个w值选择保持 C3v 对称性的理想中心 (复现图S3) [cite: 640-643]。
    """
    
    print(f"--- 正在生成 GDS 文件: {gds_filename} ---")
    print(f"参数: w={w}, 2R={2*R_vortex_um}µm, a={a_lattice_um}µm, m0={m0_mod_um}µm, alpha={alpha_shape}")

    # 1. 初始化 GDS 库和单元
    gdspy.current_library = gdspy.GdsLibrary(unit=1.0e-6, precision=1.0e-9)
    cell_name = f'DiracVortex_W{w}_R{int(R_vortex_um)}'
    cell = gdspy.Cell(cell_name)

    # 2. 定义几何参数 (单位：µm)
    r_hole_um = r_hole_frac * a_lattice_um
    triangle_A_coords = [
        (-r_hole_um, 0),
        (r_hole_um / 2, r_hole_um * np.sqrt(3) / 2),
        (r_hole_um / 2, -r_hole_um * np.sqrt(3) / 2)
    ]
    triangle_B_coords = [
        (r_hole_um, 0),
        (-r_hole_um / 2, r_hole_um * np.sqrt(3) / 2),
        (-r_hole_um / 2, -r_hole_um * np.sqrt(3) / 2)
    ]

    # 3. 定义蜂窝晶格向量
    u1 = (a_lattice_um * np.sqrt(3), 0)
    u2 = (a_lattice_um * np.sqrt(3) / 2, 3 * a_lattice_um / 2)
    delta_B = (a_lattice_um * np.sqrt(3) / 2, a_lattice_um / 2)

    # 4. 选择腔体中心 (r0)
    if use_experimental_center:
        cavity_center = (0.0, 0.0)
        print("使用实验中心 (w=1 的中心)")
    else:
        if w % 3 == 1:  # w = 1, 4, -2...
            cavity_center = (0.0, 0.0)
            print("使用理想 C3v 中心: 子晶格 A (w=3n+1)")
        elif w % 3 == 2:  # w = 2, 5, -1...
            cavity_center = delta_B
            print("使用理想 C3v 中心: 子晶格 B (w=3n+2)")
        else:  # w = 3, 6, 0...
            cavity_center = (delta_B[0] / 2, delta_B[1] / 2) 
            print("使用理想 C3v 中心: 超胞中心 (w=3n+3)")
            
    # 估算晶格的整体半径，用于放置标注和辅助线
    lattice_radius_est = (n_hex_layers + 2) * a_lattice_um * np.sqrt(3) / 2

    # ----------------------------------------------------
    # 5. 【新增】添加与截图匹配的标注 (基于图 S3)
    # ----------------------------------------------------
    label_layer = 100  # GDS 标注层号
    text_size_um = 5   # 文本高度 (µm)
    label_pos_y = lattice_radius_est + 4 * text_size_um
    label_pos_x = -lattice_radius_est

    cell.add(gdspy.Label("D. CHOICE OF CAVITY CENTER FOR C3v SYMMETRY", 
                         (label_pos_x, label_pos_y), 
                         layer=label_layer, 
                         magnification=text_size_um))
    
    if w % 3 == 1:
        label_text = "(A) w = 3n+1 = -2, +1, +4"
    elif w % 3 == 2:
        label_text = "(B) w = 3n+2 = -1, +2, +5"
    else: # w % 3 == 0
        label_text = "(C) w = 3n+3 = -3, 0, +3"
    
    cell.add(gdspy.Label(label_text, 
                         (label_pos_x, label_pos_y - 1.5 * text_size_um), 
                         layer=label_layer, 
                         magnification=text_size_um))

    center_choice_text = f"CENTER USED: {'Experimental (w=1 center)' if use_experimental_center else 'Ideal C3v Center'}"
    cell.add(gdspy.Label(center_choice_text,
                         (label_pos_x, label_pos_y - 3 * text_size_um),
                         layer=label_layer,
                         magnification=text_size_um * 0.8))

    print(f"已添加GDS标注 (Layer {label_layer}): {label_text}")

    # ----------------------------------------------------
    # 6. 【新增】添加辅助线 (Symmetry Axes)
    # ----------------------------------------------------
    line_layer = 200     # GDS 辅助线层号
    line_width_um = a_lattice_um / 10  # 辅助线宽度
    L_line = lattice_radius_est + 10 # 辅助线长度 (确保穿过整个晶格)
    cx, cy = cavity_center

    # --- 这里是修复的地方 ---
    # 水平线 (0 度)
    path_horiz = gdspy.Path(line_width_um, (cx - L_line, cy))
    path_horiz.segment(2 * L_line, "+x", layer=line_layer) # 这个是正确的

    # +60 度线
    angle_rad_60 = np.deg2rad(60)
    start_x_60 = cx - L_line * np.cos(angle_rad_60)
    start_y_60 = cy - L_line * np.sin(angle_rad_60)
    path_60 = gdspy.Path(line_width_um, (start_x_60, start_y_60))
    # 移除了 'angle=' 关键字
    path_60.segment(2 * L_line, angle_rad_60, layer=line_layer) 

    # -60 度线
    angle_rad_n60 = np.deg2rad(-60)
    start_x_n60 = cx - L_line * np.cos(angle_rad_n60)
    start_y_n60 = cy - L_line * np.sin(angle_rad_n60)
    path_n60 = gdspy.Path(line_width_um, (start_x_n60, start_y_n60))
    # 移除了 'angle=' 关键字
    path_n60.segment(2 * L_line, angle_rad_n60, layer=line_layer)
    # --- 修复结束 ---
    
    cell.add([path_horiz, path_60, path_n60])
    print(f"已添加 GDS 辅助线 (Layer {line_layer})")

    # 7. 生成晶格并应用调制
    print("正在生成晶格... (这可能需要几秒钟)")
    count_A = 0
    count_B = 0
    
    for n in range(-n_hex_layers, n_hex_layers + 1):
        for m in range(max(-n_hex_layers, -n_hex_layers - n), 
                       min(n_hex_layers, n_hex_layers - n) + 1):
            
            # (A) 固定子晶格 (Layer 1)
            base_pos = (n * u1[0] + m * u2[0], n * u1[1] + m * u2[1])
            pos_A = base_pos
            poly_A = gdspy.Polygon(triangle_A_coords, layer=1).translate(pos_A[0], pos_A[1])
            cell.add(poly_A)
            count_A += 1

            # (B) 移位子晶格 (Layer 2)
            pos_B_orig = (base_pos[0] + delta_B[0], base_pos[1] + delta_B[1])
            rel_x = pos_B_orig[0] - cavity_center[0]
            rel_y = pos_B_orig[1] - cavity_center[1]
            r = np.sqrt(rel_x**2 + rel_y**2)
            theta = np.arctan2(rel_y, rel_x)

            # --- 调制核心 ---
            if R_vortex_um == 0:
                m_mag = m0_mod_um if r > 1e-9 else 0.0 
            else:
                m_mag = m0_mod_um * np.tanh((r / R_vortex_um)**alpha_shape)
            phi = w * theta
            delta_x = m_mag * np.cos(phi)
            delta_y = m_mag * np.sin(phi)
            pos_B_final = (pos_B_orig[0] + delta_x, pos_B_orig[1] + delta_y)
            # --- 结束 ---

            poly_B = gdspy.Polygon(triangle_B_coords, layer=2).translate(pos_B_final[0], pos_B_final[1])
            cell.add(poly_B)
            count_B += 1

    # 8. 保存 GDS 文件
    lib = gdspy.current_library
    lib.write_gds(gds_filename)
    
    print(f"--- 完成 ---")
    print(f"总计添加了 {count_A} 个固定气孔 (Layer 1) 和 {count_B} 个移位气孔 (Layer 2)。")
    print(f"GDS 文件 '{gds_filename}' 已成功保存。")
    print(f"您可以在 KLayout 或其他 GDS 查看器中打开它。")


# --- 主程序入口 ---
if __name__ == "__main__":
    
    # --- 参数设置 (基于文章的实验) ---
    A_LATTICE_UM = 0.490     # 晶格常数 a = 490 nm
    R_HOLE_FRAC = 0.32        # 气孔尺寸 r = 0.32a
    M0_MOD_UM = 0.050       # 最大调制 m0 = 50 nm
    ALPHA_SHAPE = 4.0         # 形状因子 α = 4
    N_HEX_LAYERS = 150        

    # --- 示例 1: 复现文章中的 w=+1 腔体 ---
    create_dirac_vortex_gds(
        w = 1,
        R_vortex_um = 25.0,  # 2R = 50 µm
        a_lattice_um = A_LATTICE_UM,
        r_hole_frac = R_HOLE_FRAC,
        m0_mod_um = M0_MOD_UM,
        alpha_shape = ALPHA_SHAPE,
        n_hex_layers = N_HEX_LAYERS,
        gds_filename = "dirac_vortex_W+1_R25_final.gds",
        use_experimental_center = True # 匹配实验
    )
    
    print("\n" + "="*30 + "\n")

    # --- 示例 2: 复现文章中的 w=+2 腔体 ---
    create_dirac_vortex_gds(
        w = 2,
        R_vortex_um = 25.0,  # 2R = 50 µm
        a_lattice_um = A_LATTICE_UM,
        r_hole_frac = R_HOLE_FRAC,
        m0_mod_um = M0_MOD_UM,
        alpha_shape = ALPHA_SHAPE,
        n_hex_layers = N_HEX_LAYERS,
        gds_filename = "dirac_vortex_W+2_R25_final.gds",
        use_experimental_center = True # 匹配实验 (使用 w=1 的中心)
    )

    print("\n" + "="*30 + "\n")

    # --- 示例 3: R=0 的腔体 ---
    create_dirac_vortex_gds(
        w = 1,
        R_vortex_um = 0.0,  # 2R = 0 µm
        a_lattice_um = A_LATTICE_UM,
        r_hole_frac = R_HOLE_FRAC,
        m0_mod_um = M0_MOD_UM,
        alpha_shape = ALPHA_SHAPE,
        n_hex_layers = N_HEX_LAYERS,
        gds_filename = "dirac_vortex_W+1_R0_final.gds",
        use_experimental_center = True
    )