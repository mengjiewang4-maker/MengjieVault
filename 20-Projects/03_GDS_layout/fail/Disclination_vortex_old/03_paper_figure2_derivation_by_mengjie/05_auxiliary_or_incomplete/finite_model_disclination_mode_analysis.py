"""
在有限尺寸紧束缚模型中添加旋错缺陷并提取中间能级附近的缺陷模。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np

def build_finite_model(model,Nx,Ny):
    """
    把周期模型沿 x/y 方向裁剪成有限尺寸模型。
    """

    m = model.cut_piece(Nx,0)
    m = m.cut_piece(Ny,1)

    return m
def add_disclination(model):
    """
    给满足位置条件的轨道加 onsite 项，用作缺陷扰动。
    """

    n = model._norb

    for i in range(n):

        x,y = model.get_orb(i)

        if x>0.5 and y>0.5:

            model.set_onsite(5,i)
def find_defect_mode(model):
    """
    求解模型并取中间能级附近的本征态作为缺陷模候选。
    """

    evals,evecs = model.solve_all(eig_vectors=True)

    mid = len(evals)//2

    psi = evecs[:,mid]

    density = abs(psi)**2

    return psi,density
import numpy as np

def vortex_charge(psi):
    """
    根据波函数相位变化范围估算涡旋荷。
    """

    phase = np.angle(psi)

    dphi = np.max(phase)-np.min(phase)

    l = dphi/(2*np.pi)

    return l