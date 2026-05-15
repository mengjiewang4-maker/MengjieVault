import numpy as np

def solve_tb(H):
    """
    求解紧束缚模型哈密顿量的本征值和本征向量
    H: 构建好的哈密顿量矩阵 (N x N)
    """
    # 使用 np.linalg.eigh 求解厄米矩阵（Hermitian Matrix）的特征值和特征向量
    # eigh 是专门为对称矩阵或厄米矩阵优化的函数，比普通的 eig 函数更快且更稳定
    # eigenvalues: 返回从小到大排列的能量谱 (能级)
    # eigenvectors: 返回对应的波函数（每一列代表一个特征向量）
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    # 返回求解结果
    return eigenvalues, eigenvectors