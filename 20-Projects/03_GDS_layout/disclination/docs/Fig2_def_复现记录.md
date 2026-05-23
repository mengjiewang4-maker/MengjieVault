# Fig.2 d/e/f 复现记录

日期：2026-05-19

## 输出位置

`Fig2_def_GDS_outputs/`

## 生成文件

| 文件 | 说明 |
|---|---|
| `fig2def_c5_added_quarter_sector.gds` | C5 added-quarter-sector photonic disclination cavity GDS |
| `fig2def_c5_added_quarter_sector_preview.png` | PNG 预览图 |
| `parameters.json` | 参数、来源、待确认事项 |
| `README.md` | 输出说明 |

## 参数来源

论文 Extended Data Fig.3 给出 Fig.2 2D FEM cavity 参数：

- C5: `a = 500 nm`
- C5: `(r0, d0) = (0.20a, 0.45a)`
- C5: `(dc, db, di) = (0.25a, 0.23a, 0)`
- 折射率：`n = 3.33`

本地 COMSOL 截图仅提供历史测试参数：

- `a = 554 nm, R = 18a, r = 0.20a, n = 3.33`
- `a = 559 nm, R = 18a, r = 0.20a, n = 3.4`
- `a = 555 nm, R = 18a, r = 0.15a, n = 3.4`

## 重要判断

Fig.2d/e/f 不是三套不同几何。

- Fig.2d：C5 TB in-gap states。
- Fig.2e：C5 TB probability density 和角动量分类。
- Fig.2f：C5 photonic disclination cavity 几何和 Hz 模式。

因此本次只生成一套对应 Fig.2f 的 C5 GDS，README 中说明它同时是 Fig.2d/e TB 计算所对应的光子晶体几何。

## 核对结果

- GDS 可由 `klayout.db` 读入。
- top cell：`FIG2_DEF_C5_PHOTONIC_DISCLINATION_CAVITY`
- 图形数量：2250 个圆孔
- bbox：约 `(-5.504, -5.528) um` 到 `(5.307, 5.528) um`

## 待确认

- Extended Data Fig.3 给出了 `db/di`，但没有完整逐孔位移规则；当前脚本显式应用 `dc` 核心修正，`db/di` 写入参数记录。
- GDS 是二维空气孔 mask；slab 厚度、折射率、PML 等仍需在 COMSOL/Lumerical 中设置。

## 与 0325 TB 脚本的比较

已生成定量比较：

`Fig2_0325_comparison_outputs/`

结论：

- 0325 脚本是 TB/SSH 模式求解探索脚本，不输出 GDS。
- 新 Fig.2 脚本是 GDS 版图生成脚本，不求解 TB 模式。
- 两者都使用 C5 的 `90° -> 72°` Volterra 角度压缩逻辑。
- 0325 脚本使用 `delta=0.2`，等效 `d0/a=sqrt(2)*delta=0.2828`。
- 新 Fig.2 脚本使用论文 Extended Data Fig.3 的 C5 参数 `d0/a=0.45`。

## 使用新 GDS 孔位做 TB 检查

已新增脚本：

`scripts/tb_from_fig2_gds_sites.py`

输出目录：

`Fig2_GDS_site_TB_outputs/`

本脚本复用 `scripts/disclination_fig2_def_gds.py` 的孔位中心，选取中心半径 `2.5 um` 内的孔作为 TB site，构建一个局域 tight-binding Hamiltonian。

运行结果：

- 全部 GDS 孔位：2250
- 中心选取 site：485
- strong bonds：480
- weak bonds：1161
- core bonds：10
- total bonds：1651

近零本征值：

- `0.016858`
- `0.017022`
- `0.019124`
- `0.019874`
- `0.022478`
- `0.025489`
- `0.027960`
- `0.029441`
- `0.033448`

重要说明：

- 这是“GDS 几何一致性检查”，不是论文 Fig.2d/e 的严格 TB 复现。
- 当前环境没有 `scipy`，所以没有对全部 2250 个孔做稀疏矩阵求解。
- strong/weak bond 目前按孔中心距离近似分类，仍需和论文 Extended Data Fig.2/3 的完整 coupling rule 对齐。
