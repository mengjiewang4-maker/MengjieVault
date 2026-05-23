"""
根据本征模相位随方位角的线性变化，估算角动量或拓扑荷。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np

#phi ～ l*theta + phi_0
def angular_momentum(positions, mode):
    """
    计算给定本征态（mode）的轨道角动量/拓扑荷
    positions: 所有的格点坐标 [N, 2]
    mode: 对应格点上的复数波函数值 [N,]
    """
    phase = np.angle(mode)  # 1. 提取波函数的相位（取值范围通常在 -pi 到 pi 之间）

    # 2. 计算晶格的几何中心，以便确定旋转坐标系的原点
    x = positions[:,0]
    y = positions[:,1]

    xc = np.mean(x)      # x 方向的质心
    yc = np.mean(y)      # y 方向的质心

    # 3. 计算每个格点相对于中心的方位角 theta
    # np.arctan2(y, x) 返回 (-pi, pi] 之间的弧度值
    theta = np.arctan2(y-yc, x-xc)

    # 4. 相位解包裹（Unwrap）
    # 由于 np.angle 得到的相位在 +/-pi 处会发生跳转，
    # np.unwrap 可以消除这种由于分支切割导致的 2*pi 跳变，使其变成连续变化的曲线。
    phase = np.unwrap(phase)
    
    # 5. 线性拟合：寻找相位随角度变化的斜率
    # np.polyfit(x, y, 1) 会拟合一条直线 y = k*x + b
    # 这里我们拟合 phase = l_eff * theta + const
    coeff = np.polyfit(theta, phase, 1)
    
    # 6. 提取斜率并归一化
    # 因为相位绕一圈（2*pi）对应的角动量量子数是 l，所以除以 2*pi
    # 结果 l 理论上应该是整数（如 0, 1, -1 等）
    l = coeff[0]/(2*np.pi)

    return l