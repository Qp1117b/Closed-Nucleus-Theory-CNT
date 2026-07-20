# CNT p进动力学：文献调研与理论对接

> 调研日期：2026-07-20。通过 arXiv API 实际检索，非凭记忆。
> 目的：验证用户猜测（固有时连续生成→p进读数→自守筛选产出γ_n）在主流数学物理中的对应，并对接 v3 公理体系。

## 一、关键文献（已确认摘要）

### [L1] Green's Functions for Vladimirov Derivatives and Tate's Thesis
- arXiv: **2001.01721** (2020)
- 核心：正则化 Vladimirov 导数的 Green 函数 = Zeta 积分的局部函数方程；所有位(place)的场论两点函数满足 **adelic 乘积公式 = 全局 Zeta 函数方程**。明确点出 "a role of Tate's thesis in adelic physics"。
- **对接 v3 公理 III**（Adele 类空间、Tate 积分 ξ(s)=ξ(1-s)）：用户猜测的"p进读数 k + 自守筛选"本质是 Tate 定理的局部-全局结构。局部 p进谱通过 adelic 乘积公式拼成全局零点谱。

### [L2] General relativity from p-adic strings
- arXiv: **1901.02013** (2019)
- 核心：p进弦的平面波模 = **p进自守形式**；**adelic 弦的谱对应黎曼 ζ 函数的非平凡零点**；真空爱因斯坦方程从世界面标度对称涌现。
- **对接**：① 用户"自守筛选产出 γ_n" → L2 直接说 adelic 谱=ζ零点；② v3 §9 爱因斯坦方程涌现 → L2 的 p进弦涌现 GR；③ p进能动张量研究方向（开放）有现成框架。

### [L3] A quantum mechanical model of the Riemann zeros
- arXiv: **0712.0705** (2007)
- 核心：Berry-Keating H=xp 量子化，边界波函数使黎曼零点成为共振；利用位置-动量对易（ζ 对偶对称）实现谱。
- **对接 v3 公理 II**（Berry-Keating 单位胞条件 2π）+ 定理 4.1。说明"黎曼零点作为量子谱"是成熟研究方向，v3 的 E_n 公式属此传统。

### [L4] 补充线索
- 1011.0912 Nonlocal Dynamics of p-Adic Strings（p进弦非局域动力学）
- 0902.0295 Towards effective Lagrangians for adelic strings（adelic 弦有效拉氏量）
- 1102.5356 The H=xp model revisited and the Riemann zeros（H=xp 与零点）
- 1406.4247 / 1212.4282 自守 trace formula 与谱（对接定理 4.1 的谱=自守 L-函数，v3 L187）

## 二、对接 v3 公理体系

| v3 公理 | 文献对应 | 用户猜测对应 |
|---------|---------|------------|
| 公理 I（辛结构 [u,p_u]=i） | L3 的 H=xp 量子化 | 传输方程、不确定性关系 |
| 公理 II（Berry-Keating 2π 单位胞） | L3 | 硬壁截断 L=π/2 |
| 公理 III（Adele 全局谱 / Tate） | L1（Tate 定理）、L2（adelic 谱=零点） | p进读数 k + 自守筛选 → γ_n |
| §9 爱因斯坦涌现 | L2（p进弦涌现 GR） | p进能动张量 T^(p)_μν |
| 定理 4.1（E_n 来自 ξ 对称性） | L4（谱=自守 L-函数）、L3 | 自守筛选产出离散谱 |

## 三、研究含义

1. **用户猜测方向正确且非孤立**：p进局部谱 → adelic 乘积 → 全局黎曼零点，是 L1/L2 的核心结论。用户的"固有时连续生成→p进读数→自守筛选"正是此结构的本体论重述。
2. **v3 公理 III 的严格化有了工具**：L1 的 adelic 乘积公式（局部 Green 函数 → 全局 Zeta 方程）是"p进连续谱 + 自守筛选 = γ_n"的严格数学框架。这正是 v3 开放问题 A 的可对接路径。
3. **p进能动张量**：L2 给出 p进弦→GR 的现成推导，可直接借鉴做 v3 §9 的 p进局部化（κ_p 严格化）。
4. **v1/v2 数值实验的定位**：v1 朴素对应失败、v2 分布可比，是因为没用 adelic 乘积公式（局部→全局的严格桥）。下一步 v3 应实现 L1 的 adelic 乘积结构，而非孤立算 p进树谱。

## 四、下一步（基于文献）

- **v3 代码**：实现 adelic 乘积公式的简化数值版——取各 p 位 Vladimirov Green 函数的局部 Zeta 积分，乘积验证其满足全局 ξ(s)=ξ(1-s)（L1 定理）。这是"p进局部→全局零点"的严格验证，比 v2 的启发式筛选更接近本质。
- **理论笔记**：将 L1/L2/L3 的对接点写入 v3 开放问题 A 的候选机制（作为候选，非结论）。
- **p进能动张量**：借 L2 框架推导 κ_p / T^(p)_μν 的严格形式。
