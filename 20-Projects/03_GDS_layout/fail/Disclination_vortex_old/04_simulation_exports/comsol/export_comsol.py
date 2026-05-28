"""
把坐标列表导出为 resonators.csv，供 COMSOL 或其他仿真软件读取。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import csv

def export_csv(positions):
    """
    把二维坐标逐行写入 CSV 文件。
    """

    with open("resonators.csv","w") as f:

        writer = csv.writer(f)

        for p in positions:

            writer.writerow(p)