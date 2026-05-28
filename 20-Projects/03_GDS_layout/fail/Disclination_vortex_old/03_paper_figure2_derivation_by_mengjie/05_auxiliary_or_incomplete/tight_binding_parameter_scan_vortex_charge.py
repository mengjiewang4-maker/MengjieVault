"""
扫描紧束缚模型参数，记录不同耦合参数下的涡旋荷结果。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
from pythtb_2d_ssh_bbh_model_builder import *
from find_modes import *
from vortex_detector import *

def scan_parameters():
    """
    遍历 t1/t2 参数组合，记录对应的涡旋荷。
    """

    results=[]

    for t1 in np.linspace(-0.1,-0.5,10):

        for t2 in np.linspace(-0.8,-1.5,10):

            model=build_model(t1,t2)

            psi=find_mode(model)

            l=vortex_charge(psi)

            results.append((t1,t2,l))

    return results
