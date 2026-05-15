from pythtb import *
import numpy as np

def build_ssh_model():
    
    lat = [[1,0],[0,1]] # 定义晶格矢量
    
    orb = [
        [0,0],
        [0.5,0],
        [0.5,0.5],
        [0,0.5]
    ] # 定义轨道坐标，以倒格子基矢为单位

    model = tb_model(2,2,lat,orb) # 二维紧束缚模型
    
    t1 = -0.2
    t2 = -1.0 #胞内的连接（-0.2）比胞间的连接（-1.0）弱得多

    model.set_hop(t1,0,1,[0,0]) #t1跳跃强度 (Hopping Amplitude)。数值越大，电子越容易跳过去。
    model.set_hop(t1,1,2,[0,0]) #1:起始轨道索引；2:目标轨道索引
    model.set_hop(t1,2,3,[0,0]) #[0,0]晶格矢量位移 (Lattice Displacement)；
    model.set_hop(t1,3,0,[0,0]) #[0,0]电子在同一个单位晶胞（Cell）内跳跃

    model.set_hop(t2,1,0,[1,0]) #[1,0]电子跳向 x 方向下一个单位晶胞
    model.set_hop(t2,2,3,[1,0])
    model.set_hop(t2,2,1,[0,1]) #[0,1]电子跳向 y 方向下一个单位晶胞
    model.set_hop(t2,3,0,[0,1])

    return model