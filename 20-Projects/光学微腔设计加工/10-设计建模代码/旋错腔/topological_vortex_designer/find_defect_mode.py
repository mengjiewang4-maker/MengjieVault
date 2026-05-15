import numpy as np

def build_finite_model(model,Nx,Ny):  #构建有限尺寸模型

    m = model.cut_piece(Nx,0)         #在第 0 个维度（通常是 x 方向）上重复单元格 Nx 次，并截断边界。
    m = m.cut_piece(Ny,1)             #在第 1 个维度（通常是 y 方向）上重复 Ny 次

    return m

def add_disclination(model):          #添加旋错（或局部势场）

    n = model._norb                   #获取模型中总的轨道数量

    for i in range(n):                #遍历每一个轨道

        x,y = model.get_orb(i)        #获取第 i 个轨道的空间坐标

        if x>0.5 and y>0.5:           #判断轨道是否位于第一象限（假设坐标范围在 0 到 1 之间）

            model.set_onsite(5,i)     #如果是，则将该轨道的**原位能（On-site energy）**设置为 5。这通常用于在特定区域制造势垒，诱导局域态

def find_defect_mode(model):          #寻找缺陷态

    evals,evecs = model.solve_all(eig_vectors=True)
    #求解哈密顿量的所有特征值（能量）和特征向量（波函数）

    mid = len(evals)//2
    #找到能谱中间的索引。在拓扑绝缘体中，零能模（Zero Mode）通常出现在能隙中间

    psi = evecs[:,mid]
    #提取中间能级的特征向量（波函数 $\psi$）

    density = abs(psi)**2
    #计算电荷密度（波函数模平方），用于观察态的局域化情况

    return psi,density
import numpy as np

def vortex_charge(psi):                #计算涡旋电荷（拓扑荷）

    phase = np.angle(psi)              #提取波函数每个分量的相位 phi

    dphi = np.max(phase)-np.min(phase) #计算相位差

    l = dphi/(2*np.pi)                 #尝试计算拓扑荷l

    return l