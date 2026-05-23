# TB From Fig.2 GDS Sites

本目录使用新 Fig.2 GDS 生成脚本的孔位中心作为 TB site，重新做一个局域 tight-binding 检查。

## 重要说明

- 这是几何一致性检查，不是论文完整 TB 复现。
- 由于当前环境没有 `scipy`，没有对全部 2250 个孔做稀疏矩阵求解。
- 默认只取中心半径内的孔位，用 `numpy.linalg.eigh` 做 dense matrix 求解。
- 这里的 strong/weak bond 用距离近邻近似分类，仍需要后续和论文完整 coupling rule 对齐。

## 参数

- analysis radius: `2.5 um`
- selected site count: `485`
- total GDS site count: `2250`
- t_strong: `-1.0`
- t_weak: `-0.2`
- t_core: `-0.7071067811865475`

## 输出

- `tb_spectrum_from_gds_sites.png`：能谱图
- `tb_near_zero_modes_from_gds_sites.png`：近零模式图
- `tb_from_gds_sites_results.json`：数值结果

## 近零本征值

- index `166`: E = `0.016858`
- index `167`: E = `0.017022`
- index `168`: E = `0.019124`
- index `169`: E = `0.019874`
- index `170`: E = `0.022478`
- index `171`: E = `0.025489`
- index `172`: E = `0.027960`
- index `173`: E = `0.029441`
- index `174`: E = `0.033448`

## 下一步

如果需要更接近论文 Fig.2d/e，应安装 `scipy` 后对全部 2250 个孔位构建稀疏 Hamiltonian，并显式实现论文 Extended Data Fig.2/3 中的 boundary coupling rule。