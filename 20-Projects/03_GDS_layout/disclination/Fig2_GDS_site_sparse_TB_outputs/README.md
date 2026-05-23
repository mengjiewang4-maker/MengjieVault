# TB From Fig.2 GDS Sites

本目录使用新 Fig.2 GDS 生成脚本的全部孔位中心作为 TB site，构建 scipy.sparse 稀疏 Hamiltonian 并求近零模式。

## 重要说明

- 这是几何一致性检查，不是论文完整 TB 复现。
- `scipy.sparse` 是稀疏矩阵工具，只保存非零耦合项，适合 2250 个孔位的 Hamiltonian。
- 默认使用全部 GDS 孔位；如需快速调试，可用 `--analysis-radius-um` 只取中心区域。
- 这里的 strong/weak bond 用距离近邻近似分类，仍需要后续和论文完整 coupling rule 对齐。

## 参数

- analysis radius: `None`，使用全部孔位
- selected site count: `2250`
- total GDS site count: `2250`
- Hamiltonian shape: `[2250, 2250]`
- Hamiltonian non-zero entries: `16332`
- eigensolver: `scipy.sparse.linalg.eigsh(sigma)`
- t_strong: `-1.0`
- t_weak: `-0.2`
- t_core: `-0.7071067811865475`

## 输出

- `tb_spectrum_from_gds_sites.png`：能谱图
- `tb_near_zero_modes_from_gds_sites.png`：近零模式图
- `tb_from_gds_sites_results.json`：数值结果

## 近零本征值

- computed rank `31`: E = `-0.004337`
- computed rank `32`: E = `-0.004137`
- computed rank `33`: E = `-0.004105`
- computed rank `34`: E = `-0.003982`
- computed rank `35`: E = `-0.001866`
- computed rank `36`: E = `-0.001862`
- computed rank `37`: E = `-0.001087`
- computed rank `38`: E = `-0.001063`
- computed rank `39`: E = `-0.000886`

## 下一步

如果需要更接近论文 Fig.2d/e，应显式实现论文 Extended Data Fig.2/3 中的 boundary coupling rule，而不只按距离把键分成 strong/weak。