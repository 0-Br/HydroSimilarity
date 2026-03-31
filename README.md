# HydroSimilarity

水文相似性指标体系的构建研究 | Construction of a Hydrological Similarity Index System

清华大学杨大文老师「水文学」课程研究项目

刘滨瑞 / Binrui Liu, Tsinghua University

## 研究背景 / Background

在水文学中，"水文相似性"是一个核心问题：给定两个流域，如何量化判断它们在水文行为上是否相似？这对于无资料地区的水文预报（PUB, Prediction in Ungauged Basins）具有重要意义——如果能找到与目标流域水文相似的已观测流域，就可以将后者的水文模型参数迁移过去。然而水文相似性难以直接度量。本项目的核心思路是：**用流域的下垫面物理特征（容易获取）来预测水文行为的相似性（难以直接度量）**，从而建立一套可操作的水文相似性指标体系。

Hydrological similarity is a central question in hydrology: given two watersheds, how can we quantitatively determine whether they exhibit similar hydrological behavior? This is critical for Prediction in Ungauged Basins (PUB) — if a gauged watershed hydrologically similar to the target ungauged basin can be identified, its calibrated model parameters can be transferred. However, hydrological similarity is inherently difficult to measure directly. The core idea of this project is to **use easily obtainable underlying surface physical features to predict hydrological behavior similarity**, thereby constructing an operational hydrological similarity index system.

## 方法 / Methods

### 数据 / Data

项目使用了 25 个子流域的数据（编号 1–25，缺第 18 号），每个流域包含：

- **下垫面特征（14 维）**：平均高程、排水密度、坡度、TWI（地形湿度指数）、粘土/砂/粉砂含量、NDVI 趋势及四季值、耕地与城市用地比例
- **水文特征（5 维）**：径流系数、基流系数、退水系数（early / custom / late）

数据经 MinMax 归一化后用于建模。

The dataset covers 25 sub-watersheds (numbered 1–25, No. 18 missing), each characterized by:

- **Underlying surface features (14-dimensional)**: mean elevation, drainage density, slope, TWI (Topographic Wetness Index), clay/sand/silt content, NDVI trend and seasonal values, cropland and urban land proportions
- **Hydrological features (5-dimensional)**: runoff coefficient, baseflow coefficient, recession coefficients (early / custom / late)

All features are MinMax-normalized before modeling.

### 相似性度量 / Similarity Measures

定义了四种逐元素相似性函数，将两个特征向量映射为一个相似性向量：

Four element-wise similarity functions map a pair of feature vectors to a similarity vector:

| 函数 / Function | 公式 / Formula | 特点 / Characteristics |
|---|---|---|
| quotient | min(a, b) / max(a, b) | 商形式，对量级差异敏感 / Ratio form, sensitive to magnitude differences |
| delta | 1 − \|a − b\| | 差形式，线性衰减 / Difference form, linear decay |
| exponent | exp(−(a − b)²) | 指数形式，高斯核风格 / Exponential form, Gaussian kernel style |
| quadratic | 1 − (a − b)² | 距离形式，二次衰减 / Distance form, quadratic decay |

### 建模 / Modeling

使用正则化线性回归（Ridge / Lasso）建立下垫面相似性向量到水文相似性向量的映射：

1. 对训练集中所有流域对，计算下垫面相似性向量 **X**（14 维）和水文相似性向量 **Y**（5 维）
2. 用 Ridge 或 Lasso 回归拟合 X → Y
3. 通过 Lasso 路径分析识别对各水文特征最显著的下垫面因子
4. 对预测结果进行三级相似性评级

Regularized linear regression (Ridge / Lasso) maps underlying-surface similarity vectors to hydrological similarity vectors:

1. For all watershed pairs in the training set, compute the surface similarity vector **X** (14-dim) and the hydrological similarity vector **Y** (5-dim)
2. Fit X → Y with Ridge or Lasso regression
3. Identify the most significant surface factors for each hydrological feature via Lasso path analysis
4. Classify prediction results into a three-level similarity grading

### 评估 / Evaluation

将 24 个流域按编号分为训练集（12 个）和验证集（12 个），对比四种相似性函数在 Ridge 回归下的预测表现，并通过回归系数热力图进行显著性分析。

The 24 watersheds are split by index into a training set (12) and a validation set (12). Prediction performance is compared across the four similarity functions under Ridge regression, with significance analysis conducted through regression coefficient heatmaps.

## 研究思路详述 / Technical Framework

本项目将水文相似性预测问题分解为三个层次：

The project decomposes the hydrological similarity prediction problem into three layers:

**第一层：特征表示 / Layer 1: Feature Representation.**
每个流域被表示为两组特征向量。下垫面特征向量 S ∈ ℝ¹⁴ 涵盖地形（高程、坡度、TWI）、土壤（粘土/砂/粉砂含量）、植被（NDVI 趋势与四季值）和土地利用（耕地、城市）四个维度；水文特征向量 H ∈ ℝ⁵ 描述径流系数、基流系数及三个时段的退水系数。下垫面特征可通过遥感和 GIS 数据获取，而水文特征需要长期实测径流资料。

Each watershed is represented by two feature vectors. The surface feature vector S ∈ ℝ¹⁴ spans four dimensions: topography (elevation, slope, TWI), soil (clay/sand/silt content), vegetation (NDVI trend and seasonal values), and land use (cropland, urban). The hydrological feature vector H ∈ ℝ⁵ captures the runoff coefficient, baseflow coefficient, and three recession coefficients. Surface features are obtainable via remote sensing and GIS, while hydrological features require long-term observed streamflow records.

**第二层：相似性量化 / Layer 2: Similarity Quantification.**
对任意一对流域 (i, j)，通过逐元素相似性函数将其特征向量映射为相似性向量。以下垫面为例，sim_S(i, j) = f(Sᵢ, Sⱼ) ∈ ℝ¹⁴，每个分量表示该流域对在对应属性上的相似程度。四种函数（quotient / delta / exponent / quadratic）提供了不同的衰减特性，适用于不同尺度和分布的属性。

For any watershed pair (i, j), element-wise similarity functions map their feature vectors to similarity vectors. For instance, sim_S(i, j) = f(Sᵢ, Sⱼ) ∈ ℝ¹⁴, where each component indicates the degree of similarity on the corresponding attribute. The four functions (quotient / delta / exponent / quadratic) offer different decay characteristics suited to attributes of varying scales and distributions.

**第三层：相似性迁移 / Layer 3: Similarity Transfer.**
核心假设是：下垫面相似性向量与水文相似性向量之间存在线性映射关系，即 sim_H ≈ W · sim_S，其中 W ∈ ℝ⁵ˣ¹⁴ 是待学习的权重矩阵。通过 Ridge 或 Lasso 回归估计 W：
- **Ridge 回归**用于在特征共线性较强时稳定估计
- **Lasso 回归**通过 L1 正则化将不重要特征的系数压缩至零，天然实现特征筛选

The core hypothesis is a linear mapping between surface similarity and hydrological similarity vectors: sim_H ≈ W · sim_S, where W ∈ ℝ⁵ˣ¹⁴ is the weight matrix to be learned. W is estimated via Ridge or Lasso regression:
- **Ridge regression** stabilizes estimation under strong feature collinearity
- **Lasso regression** applies L1 regularization to shrink insignificant coefficients to zero, achieving built-in feature selection

### 特征筛选 / Feature Selection

通过绘制 Lasso 路径图（正则化系数 α 从 0.001 到 0.12 变化时各特征系数的变化轨迹），可以直观识别对每个水文特征最重要的下垫面因子。系数最后被压缩至零的特征即为最显著的预测因子。类似地，Ridge 路径图（α 从 0.21 到 1.2）展示了各特征在正则化增强时的稳定性。

Lasso path plots (α varying from 0.001 to 0.12) visualize the coefficient trajectories of each feature, enabling intuitive identification of the most important surface factors for each hydrological feature — the last coefficients to be shrunk to zero are the most significant predictors. Similarly, Ridge path plots (α from 0.21 to 1.2) reveal coefficient stability under increasing regularization.

### 相似性评级 / Similarity Grading

预测结果被映射为三级相似性评级：
- 相似度 > 0.80：**高度相似**
- 0.60 < 相似度 ≤ 0.80：**大致相似**
- 相似度 ≤ 0.60：**不相似**

Predicted similarities are classified into three grades:
- Similarity > 0.80: **Highly similar**
- 0.60 < Similarity ≤ 0.80: **Roughly similar**
- Similarity ≤ 0.60: **Dissimilar**

在验证集上对比四种相似性函数的表现，评估指标包括预测误差和评级一致率。通过回归系数矩阵的热力图进行显著性分析，揭示哪些下垫面属性对哪些水文特征的预测贡献最大。

Performance of the four similarity functions is compared on the validation set using prediction error and grading agreement rate. Significance analysis is conducted via regression coefficient heatmaps to reveal which surface attributes contribute most to predicting each hydrological feature.

## 项目结构 / Project Structure

```
HydroSimilarity/
├── watershed.py      # 流域数据类 / Watershed data class
├── similarity.py     # 四种相似性度量函数 / Four similarity measures
├── model.py          # 训练、预测与评级 / Training, prediction & grading
├── report.ipynb      # 完整实验流程 / Full experiment pipeline
├── data/             # 原始数据 / Raw data (Excel)
└── cache/            # 预处理缓存 / Preprocessed cache (pickle)
```
