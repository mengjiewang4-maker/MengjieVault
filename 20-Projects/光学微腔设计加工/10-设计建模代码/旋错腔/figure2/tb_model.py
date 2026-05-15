import numpy as np

def build_tb(positions, t1=1.0, t2=0.5, cutoff=1.5):
    """
    构建紧束缚模型哈密顿量矩阵
    positions: 晶格点坐标列表或数组 [[x1,y1], [x2,y2], ...]
    t1: 近邻跳跃能（通常指最近邻，强度较大）
    t2: 次近邻跳跃能（通常指较远的耦合，强度较小）
    cutoff: 截断半径（超过此距离的原子间认为没有耦合）
    """
    N = len(positions)   # 获取系统中的总原子数（格点数）

    # 初始化一个 N x N 的全零矩阵，作为哈密顿量 H
    # H[i, j] 代表电子从第 j 个轨道跳跃到第 i 个轨道的几率幅
    H = np.zeros((N,N))

    # 使用双重循环遍历所有原子对，计算它们之间的相互作用
    for i in range(N):

        xi,yi = positions[i]     # 提取原子 i 的坐标
        
        # 内层循环从 i+1 开始，利用哈密顿量的厄米性（对称性），只计算上三角部分
        for j in range(i+1,N):
            
            xj,yj = positions[j]    # 提取原子 j 的坐标

            r = np.sqrt((xi-xj)**2 + (yi-yj)**2)  # 计算原子 i 和原子 j 之间的欧几里得距离 r

            if r < cutoff:    # 判断原子间距离是否在截断半径内

                # 根据距离区分耦合强度
                if r < cutoff*0.7:  # 如果距离很近（小于截断半径的 70%），判定为强耦合 t1
                    coupling = t1
                else:               # 如果距离稍远（在 70% 到 100% 之间），判定为弱耦合 t2
                    coupling = t2
                
                # 填充哈密顿量矩阵
                H[i,j] = coupling   # 设置上三角部分
                H[j,i] = coupling   # 设置下三角部分（保证矩阵是对称的/厄米的）

    return H    # 返回构建好的哈密顿量矩阵