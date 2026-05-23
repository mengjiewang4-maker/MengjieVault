# 0325 TB Script vs Fig.2 GDS Script Comparison

## 文件

- 旧脚本：`/Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/Disclination_vortex_old/03_paper_figure2_derivation_by_mengjie/03_c5_mode_analysis/c5_cell_center_cut_mode_workflow_0325.py`
- 新脚本：`/Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/disclination/scripts/disclination_fig2_def_gds.py`

## 关键结论

- 旧脚本是 TB/SSH 模式求解探索脚本，不生成 GDS。
- 新脚本是 Fig.2 C5 photonic cavity 的 GDS 生成脚本，不求解 TB 模式。
- 两者都使用 C5 的 90° -> 72° Volterra 角度压缩逻辑。
- 两者的单胞内部点位不同：旧脚本用 `delta=0.2`，等效 `d0/a=0.2828`；新脚本用论文参数 `d0/a=0.45`。

## 定量对比

| 项目 | 旧 0325 TB 脚本 | 新 Fig.2 GDS 脚本 |
|---|---:|---:|
| 原始 1/4 扇区点数 | 225 | 571 |
| 最终点/孔数 | 710 | 2250 |
| d0/a | 0.2828 | 0.4500 |
| 结构范围参数 | Nx=Ny=8 | lattice_range=13 |

## 输出

- 对比图：`0325_tb_vs_fig2_gds_geometry_comparison.png`
- 指标 JSON：`comparison_metrics.json`

## 下一步建议

如果要让 GDS 和 TB 严格一致，应把新脚本生成的孔位中心作为 TB site，重新构建 Hamiltonian，避免几何和模式计算使用两套不同坐标。