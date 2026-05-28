

## 1. 核心结论

本次成功构建了一套用于 Raman 光谱自动分析的 Python 批处理流程，实现了：

- 批量读取 `.txt` Raman 光谱文件
    
- 仅对 370–430 cm⁻¹ 区间进行分析
    
- Savitzky-Golay 平滑处理
    
- 3 次以内多项式背景扣除
    
- Gaussian 多峰拟合
    
- 自动输出：
    
    - 峰位
        
    - 峰强度
        
    - FWHM（半高宽）
        
- 自动生成：
    
    - PNG 图像
        
    - CSV 峰参数汇总
        
    - PDF 报告
        

最终形成了一套可直接用于：

- Raman 数据标准化处理
    
- MoS₂ 峰分析
    
- 实验批量统计
    
- 科研图生成
    
- 实验报告归档
    

的自动化分析流程。

---

# 2. 方法流程

## Step 1：批量读取 Raman txt 数据

使用：

```python
os.listdir()
np.loadtxt()
```

读取同根目录 `20250714/` 文件夹中的所有 `.txt` 文件。

数据格式：

```txt
Wavenumber    Intensity
370.1         1023
370.2         1030
...
```

---

## Step 2：截取 Raman 拟合区间

仅保留：

```python
370–430 cm⁻¹
```

区间数据：

```python
mask = (wavenumber >= 370) & (wavenumber <= 430)
```

原因：

- MoS₂ Raman 主峰位于此范围
    
- 降低背景影响
    
- 提高拟合稳定性
    
- 减少无关峰干扰
    

---

## Step 3：Savitzky-Golay 平滑

使用：

```python
savgol_filter()
```

目的：

- 去除高频噪声
    
- 保留峰形结构
    
- 提高峰检测稳定性
    

---

## Step 4：3 次多项式背景拟合

使用：

```python
Polynomial.fit()
```

对背景进行：

[  
I_{background}(x)  
]

拟合。

然后进行背景扣除：

[  
I_{corrected} = I_{raw} - I_{background}  
]

目的：

- 消除荧光背景
    
- 消除漂移
    
- 提高峰拟合准确性
    

---

## Step 5：峰值检测

使用：

```python
find_peaks()
```

自动寻找 Raman 峰。

筛选条件：

- 峰高
    
- 峰间距
    

然后：

- 按峰强排序
    
- 仅保留最强的 3 个峰
    

---

## Step 6：Gaussian 多峰拟合

Gaussian 函数：

[  
f(x)=A\exp\left(-\frac{(x-x_0)^2}{2\sigma^2}\right)  
]

参数：

- A：峰强
    
- x₀：峰中心
    
- σ：峰宽
    

使用：

```python
curve_fit()
```

进行：

- 单峰 Gaussian
    
- 多峰叠加 Gaussian
    

拟合。

---

## Step 7：计算 FWHM

使用：

[  
FWHM = 2.3548\sigma  
]

得到：

- 峰宽
    
- 峰品质
    
- 峰分辨率
    

---

## Step 8：自动生成图像

输出：

- 原始谱
    
- 背景
    
- 背景扣除谱
    
- Gaussian 拟合曲线
    
- 单独峰曲线
    

全部英文标注。

---

## Step 9：生成 PDF 报告

使用：

```python
PdfPages
```

自动：

- 将所有 PNG 图整合
    
- 输出 Raman PDF 报告
    

适合：

- 实验记录
    
- 汇报
    
- Obsidian 存档
    
- 论文补充材料
    

---

# 3. 参数

## Raman 区间

```python
range_min = 370
range_max = 430
```

---

## 平滑参数

```python
smooth_window = 11
smooth_poly = 3
```

---

## 背景拟合

```python
poly_order = 3
```

即：

- 1~3 次多项式背景拟合
    

---

## 峰值检测

```python
peak_height = 5
peak_distance = 5
```

---

## 最大拟合峰数

```python
max_peaks = 3
```

---

## Gaussian 初值

```python
sigma0 = 3
```

---

# 4. 遇到的问题

## 问题 1：缺少 fpdf 模块

错误：

```python
ModuleNotFoundError: No module named 'fpdf'
```

原因：

- 当前 Python 环境未安装 `fpdf`
    

解决：

```bash
pip3 install fpdf
```

---

## 问题 2：路径错误

错误：

```python
FileNotFoundError
```

原因：

- data 文件夹不存在
    

解决：

改为：

```python
script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "20250714")
```

---

## 问题 3：curve_fit 边界错误

错误：

```python
Each lower bound must be strictly less than each upper bound
```

原因：

- 上下界相等
    

解决：

加入：

```python
1e-4
```

安全距离。

---

## 问题 4：Initial guess outside bounds

错误：

```python
Initial guess is outside of provided bounds
```

原因：

- 初始值等于边界
    
- 峰位位于 370 边界
    

解决：

构建：

```python
safe_bounds_for_x0()
```

自动边界保护函数。

---

# 5. 下一步

## 方向 1：Lorentz / Voigt 拟合

当前：

- Gaussian
    

未来：

- Lorentzian
    
- Voigt
    

适合真实 Raman 峰。

---

## 方向 2：自动识别 MoS₂ 层数

根据：

- E₂g
    
- A₁g
    

峰间距自动判断：

- 单层
    
- 双层
    
- 多层
    

---

## 方向 3：GUI 图形界面

可加入：

- PyQt
    
- Tkinter
    

实现：

- 拖拽 Raman 文件
    
- 一键生成报告
    

---

## 方向 4：实验数据库化

未来：

- Raman
    
- SEM
    
- ICP
    
- EBL
    

统一进入实验数据库。

---

## 方向 5：Obsidian 自动归档

自动：

- 保存 PDF
    
- 保存 CSV
    
- 生成 md 笔记
    

形成完整实验知识库。

---

# 6. Obsidian 文件建议

## 建议目录结构

```txt
Raman/
├── raw_data/
├── results/
├── reports/
├── figures/
├── scripts/
└── notes/
```

---

## 建议命名

```txt
Sample1_0701_0.5mw
```

结构：

```txt
样品_日期_功率
```

---

## 建议 Obsidian 笔记模板

```md
# Raman Analysis

## Sample
Sample1_0701_0.5mw

## Raman Range
370–430 cm⁻¹

## Processing
- SG smoothing
- Polynomial background subtraction
- Gaussian fitting

## Results
- Peak1:
- Peak2:
- FWHM:

## Files
- PDF report
- CSV results
- PNG figures
```