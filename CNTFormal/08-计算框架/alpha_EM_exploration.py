#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
α_EM 的探索性数值扫描：从格林函数公式与 p-adic AdS/CFT 出发

目标：在新 GL(3)-Langlands-p-adic 框架下，尝试构造 1/α_EM 的候选公式，
      并与实验值 1/α_EM(0) = 137.035999084 比较。

认识论地位：纯探索 / 事后启发。任何与实验接近的公式都必须进一步
      从第一性原理推导其物理来源，不能作为独立成功证据。
"""

import numpy as np
from math import pi, log

# ---------------------------------------------------------------------------
# 输入数据
# ---------------------------------------------------------------------------
alpha_exp_inv = 137.035999084  # 1/α_EM(0)
alpha_exp = 1.0 / alpha_exp_inv

# p=5 电磁扇区
p = 5
alpha_5 = 0.826  # 经验值
alpha_5_GF = 0.842  # Green 函数公式最优值

# p-adic AdS/CFT 质量-标度维关系给出体质量平方
m5_sq = -1.0 - p + p**alpha_5 + p**(1.0 - alpha_5)
m5_sq_GF = -1.0 - p + p**alpha_5_GF + p**(1.0 - alpha_5_GF)

# 博弈不动点权重
x_star = np.array([np.log(5/3), np.log(5/2), np.log(3/2)])
x_star /= x_star.sum()
x5_star = x_star[2]

# g_5 来自博弈不动点
m_p_MeV = 938.272
g5_MeV = x5_star * m_p_MeV  # ≈ 207.6 MeV

print("=" * 80)
print("α_EM 探索性数值扫描")
print("=" * 80)
print(f"\n实验值: 1/α_EM(0) = {alpha_exp_inv:.9f}")
print(f"p=5 扇区: α_5(经验) = {alpha_5:.4f}, α_5(GF最优) = {alpha_5_GF:.4f}")
print(f"p-adic AdS/CFT 体质量平方: m_5^2(α_5) = {m5_sq:.4f}, m_5^2(α_5^GF) = {m5_sq_GF:.4f}")
print(f"博弈不动点 g_5 = {g5_MeV:.2f} MeV")

# ---------------------------------------------------------------------------
# 候选公式
# ---------------------------------------------------------------------------
candidates = []

def add(name, val):
    candidates.append((name, val))

# 候选 1：纯幂次组合
# 1/α ~ p^{n(1-α)}，调整 n 使接近 137
for n in range(1, 50):
    val = p**(n * (1.0 - alpha_5))
    add(f"5^{{n(1-α_5)}}, n={n}", val)
    val_GF = p**(n * (1.0 - alpha_5_GF))
    add(f"5^{{n(1-α_5^GF)}}, n={n}", val_GF)

# 候选 2：含 π 的幂次组合
for n in [1, 2, 3, 4, 5]:
    val = pi * p**(n * (1.0 - alpha_5))
    add(f"π·5^{{n(1-α_5)}}, n={n}", val)
    val_GF = pi * p**(n * (1.0 - alpha_5_GF))
    add(f"π·5^{{n(1-α_5^GF)}}, n={n}", val_GF)

# 候选 3：与 p-adic AdS/CFT 质量平方相关
add("|m_5^2(α_5)|^{-1}", 1.0 / abs(m5_sq))
add("|m_5^2(α_5^GF)|^{-1}", 1.0 / abs(m5_sq_GF))
add("π / |m_5^2(α_5)|", pi / abs(m5_sq))
add("π / |m_5^2(α_5^GF)|", pi / abs(m5_sq_GF))

# 候选 4：与 g_5 和质量标度相关
# 1/α ~ (m_p / g_5) * 某个因子
add("m_p / g_5", m_p_MeV / g5_MeV)
add("π · m_p / g_5", pi * m_p_MeV / g5_MeV)

# 候选 5：与壳层指数相关（p=5 轻子壳层 (-21, 0, 11)）
k_diff = 11 - (-21)  # = 32
add("5^{(k_τ-k_e)(1-α_5)}", p**(k_diff * (1.0 - alpha_5)))
add("5^{(k_τ-k_e)(1-α_5^GF)}", p**(k_diff * (1.0 - alpha_5_GF)))
add("π · 5^{(k_τ-k_e)(1-α_5^GF)}", pi * p**(k_diff * (1.0 - alpha_5_GF)))

# 候选 6：旧4-单纯形路径作为参考
old_pred = 16384.0 * pi / 375.0
add("旧4-单纯形: 16384π/375", old_pred)

# 候选 7：基于三个素数的 adelic 组合
# 尝试 (2^a * 3^b * 5^c) / π 等形式
for a in range(-5, 6):
    for b in range(-5, 6):
        for c in range(-5, 6):
            if a == 0 and b == 0 and c == 0:
                continue
            val = (2**a) * (3**b) * (5**c) / pi
            add(f"2^{a}·3^{b}·5^{c}/π", val)
            val2 = (2**a) * (3**b) * (5**c) * pi
            add(f"2^{a}·3^{b}·5^{c}·π", val2)

# 候选 8：基于三个扇区格林函数的联合乘积
# 假设 1/α_EM 与三个扇区在特定壳层的格林函数乘积相关
alpha_vals = {'2': 1.545, '3': 0.443, '5': alpha_5}
seen_G = set()
for k2 in range(-5, 6):
    for k3 in range(-5, 6):
        for k5 in range(-5, 6):
            val = (2**(k2*(1-alpha_vals['2'])) *
                   3**(k3*(1-alpha_vals['3'])) *
                   5**(k5*(1-alpha_vals['5'])))
            # 限制结果数量：只记录接近目标值的，并去重
            key = (k2, k3, k5)
            if key not in seen_G and abs(val - alpha_exp_inv) / alpha_exp_inv < 0.5:
                seen_G.add(key)
                add(f"G_2({k2})·G_3({k3})·G_5({k5})", val)

# 候选 9：基于 p-adic AdS/CFT 质量平方的组合
m2_sq = -1.0 - 2 + 2**alpha_vals['2'] + 2**(1.0-alpha_vals['2'])
m3_sq = -1.0 - 3 + 3**alpha_vals['3'] + 3**(1.0-alpha_vals['3'])
add("|m_2^2·m_3^2·m_5^2|^{-1/2}", 1.0 / abs(m2_sq * m3_sq * m5_sq)**0.5)
add("π/|m_2^2·m_3^2·m_5^2|^{1/3}", pi / abs(m2_sq * m3_sq * m5_sq)**(1.0/3.0))
add("|m_2^2·m_3^2·m_5^2|^{1/3}/π", abs(m2_sq * m3_sq * m5_sq)**(1.0/3.0) / pi)

# 候选 10：与 N_cycle=30 相关的组合
N_cycle = 30
add("N_cycle^{2}/π", N_cycle**2 / pi)
add("N_cycle·π", N_cycle * pi)
add("N_cycle^{2}·π/100", N_cycle**2 * pi / 100.0)
add("N_cycle·(1-α_5)", N_cycle * (1.0 - alpha_5))
add("N_cycle·(1-α_5^GF)", N_cycle * (1.0 - alpha_5_GF))

# ---------------------------------------------------------------------------
# 排序并输出最佳候选
# ---------------------------------------------------------------------------
candidates.sort(key=lambda x: abs(x[1] - alpha_exp_inv))

print("\n" + "=" * 80)
print("Top 20 候选公式（按与实验值偏差排序）")
print("=" * 80)
print(f"{'Rank':<6} {'Formula':<45} {'Predicted 1/α':<18} {'Dev (%)':<12}")
print("-" * 80)
for i, (name, val) in enumerate(candidates[:20]):
    dev = abs(val - alpha_exp_inv) / alpha_exp_inv * 100
    print(f"{i+1:<6} {name:<45} {val:<18.6f} {dev:<12.4f}")

print("\n" + "=" * 80)
print("诚实说明：")
print("  以上扫描是探索性的，任何接近实验值的候选都需要独立的")
print("  第一性原理论证。当前没有从 GL(3)-Langlands 结构唯一导出")
print("  α_EM 的严格映射。")
print("=" * 80)
