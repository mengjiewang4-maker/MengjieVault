"""
把坐标列表导出为 Lumerical FDTD 脚本 structure.lsf，每个坐标生成一个圆形结构。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

def export_lsf(positions):
    """
    把二维坐标写成 Lumerical addcircle 脚本。
    """

    f=open("structure.lsf","w")

    for x,y in positions:

        f.write(f"""

addcircle;
set("x",{x});
set("y",{y});
set("radius",100e-9);

""")

    f.close()