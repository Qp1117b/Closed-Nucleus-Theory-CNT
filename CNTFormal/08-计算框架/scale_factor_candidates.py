#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标度因子 S_p 的候选公式数值比较

背景：Green 函数质量公式 m_k^{(p)} = g_p^{eff} * p^{k(1-alpha_p)}
要求 g_p^{eff} = S_p * g_p，其中 g_p = x_p^* * m_p 来自博弈不动点。
观测到的 S_p（来自 mass_formula_shell_test.py）约为 10^2 - 10^3。

本脚本测试从 GL(3) 局部表示归一化/局部 L-因子/epsilon 因子/p-adic 体积
等自然候选公式得到的 S_p，并与观测值比较。

结论预期：简单局部 L-因子/体积/epsilon 因子无法单独复现 ~10^2-10^3 的标度；
S_p 需要更具体的 GL(3) 自守表示数据（目前未知）。
"""

import numpy as np

# ---------------------------------------------------------------------------
# 观测值（来自 Green 函数公式拟合，mass_formula_shell_test.py）
# ---------------------------------------------------------------------------
# 注意：S_OBS = g_eff / g_p 为无量纲标度因子。mass_formula_shell_test.py
# 输出的 g_eff 单位与 g_p 相同（MeV），因此 s 为无量纲比值。
# 旧版本曾误将 g_eff 的 MeV 数值当作 s，导致量级混淆，此处已修正。
P = np.array([2, 3, 5])
S_OBS = {2: 0.3613, 3: 2.5032, 5: 0.5191}

# 博弈不动点权重（用于 g_p = x_p^* m_p）
x_star = np.array([np.log(5/3), np.log(5/2), np.log(3/2)])
x_star /= x_star.sum()

# ---------------------------------------------------------------------------
# 候选 S_p 公式
# ---------------------------------------------------------------------------

def S_trivial(p):
    """无标度因子"""
    return 1.0


def S_L_factor_trivial_s1(p):
    """未分歧平凡表示的局部 L-因子在 s=1：L(1,1_p) = (1-p^{-1})^{-1}"""
    return 1.0 / (1.0 - 1.0/p)


def S_L_factor_trivial_s0(p):
    """未分歧平凡表示的局部 L-因子在 s=0：L(0,1_p) = (1-1)^{-1} = ∞，不可取"""
    return np.inf


def S_L_factor_weight_minus1_s1(p):
    """三个 Satake 参数均为 p^{-1}（Tate motive Q(1)^3）在 s=1"""
    return (1.0 / (1.0 - 1.0/p**2))**3


def S_L_factor_alpha_s1(p, alpha):
    """
    假设 Satake 参数为 {p^{-alpha}, p^{alpha}, 1}（HT 权 {alpha,-alpha,0}）
    在 s=1 的局部 L-因子的绝对值。
    """
    p = float(p)
    return abs(1.0 / (1.0 - p**(-1-alpha)) *
               1.0 / (1.0 - p**(-1+alpha)) *
               1.0 / (1.0 - 1.0/p))


def S_volume_GL3(p):
    """GL(3,Z_p) 体积的倒数：Vol^{-1} = prod_{i=1}^3 (1-p^{-i})"""
    p = float(p)
    vol = 1.0
    for i in range(1, 4):
        vol *= (1.0 - p**(-i))
    return 1.0 / vol


def S_epsilon_conductor(p, f):
    """
    导体为 p^f 的表示的 epsilon 因子在 s=0 的绝对值：
    |ε(0,π_p,ψ)| = p^{f/2}（对标准非分歧加法特征 ψ）
    """
    return p**(f/2.0)


def S_idele(p, a):
    """S_p = |a|_p^{-1} = p^{v_p(a)}，其中 a 是有理数/idele"""
    # 这里用 a 作为占位：实际 a 未知
    return p**a


def S_eff_vs_Yukawa_scale(p):
    """
    现象学比较：若质量标度由 SM Higgs VEV v 提供，则应满足
    g_p^{eff} ~ v * x_p^*。此函数返回实际 g_eff 与 v*x_p^* 的比值。
    """
    m_p_MeV = 938.272
    v_MeV = 246.0 * 1000.0
    # g_eff = S_OBS * g_p，其中 g_p = x_p^* * m_p（MeV）
    g_p_MeV = x_star[list(P).index(p)] * m_p_MeV
    g_eff_MeV = S_OBS[p] * g_p_MeV
    return g_eff_MeV / (v_MeV * x_star[list(P).index(p)])


# ---------------------------------------------------------------------------
# 比较并输出
# ---------------------------------------------------------------------------
def print_comparison(name, S_pred):
    print(f"\n{name}:")
    print(f"  {'p':<6} {'S_pred':<14} {'S_obs':<14} {'S_pred/S_obs':<14} {'|dev|':<10}")
    ratios = []
    for p in P:
        pred = S_pred(p)
        obs = S_OBS[p]
        ratio = pred / obs if np.isfinite(pred) and obs != 0 else np.inf
        ratios.append(ratio)
        dev = abs(ratio - 1.0) * 100 if np.isfinite(ratio) else np.inf
        print(f"  {p:<6} {pred:<14.4f} {obs:<14.2f} {ratio:<14.4f} {dev:<10.1f}%")
    return ratios


def main():
    print("=" * 80)
    print("标度因子 S_p = g_p^{eff}/g_p 的候选公式比较")
    print("=" * 80)
    print(f"\n观测值（Green 函数公式拟合）：")
    for p in P:
        print(f"  p={p}: S_obs = {S_OBS[p]:.2f}")

    # 1. 平凡候选
    print_comparison("S_p = 1（无标度）", S_trivial)

    # 2. 局部 L-因子（平凡表示，s=1）
    print_comparison("S_p = L(1, 1_p) = (1-p^{-1})^{-1}", S_L_factor_trivial_s1)

    # 3. GL(3,Z_p) 体积倒数
    print_comparison("S_p = Vol(GL(3,Z_p))^{-1}", S_volume_GL3)

    # 4. 用各扇区自身经验 alpha_p 的局部 L-因子
    alpha = {2: 1.545, 3: 0.443, 5: 0.826}
    def S_L_factor_alpha_s1_per_p(p_arg):
        a = alpha[p_arg]
        return S_L_factor_alpha_s1(p_arg, a)
    print_comparison("S_p = L(1, π_p), HT={±α_p,0}（各扇区用自身 α_p）", S_L_factor_alpha_s1_per_p)

    # 5. Epsilon 因子（不同导体指数）
    for f in [1, 3, 6, 12]:
        S_pred = lambda p_arg, f_arg=f: S_epsilon_conductor(p_arg, f_arg)
        print_comparison(f"S_p = |ε(0,π_p)| = p^{f/2}, f={f}", S_pred)

    # 6. 与 SM Higgs VEV 的现象学比较
    print_comparison("g_eff / (v*x_p^*)（若质量标度来自 v=246 GeV）", S_eff_vs_Yukawa_scale)

    print("\n" + "=" * 80)
    print("诚实结论（2026-07-16 修正）：")
    print("  - 修正后的观测标度因子 S_p = g_eff/g_p 为 O(1) 量级（p=2:0.36, p=3:2.50, p=5:0.52），")
    print("    不再是旧版本中误报的 O(10^2)-O(10^3)。")
    print("  - 局部 L-因子、体积、epsilon 因子等候选在 f~0-6 时给出的 S_p 为 O(1)-O(10^2)，")
    print("    与 O(1) 观测值处于同一数量级范围，但具体数值仍不匹配；")
    print("    简单候选无法精确复现三个扇区的 S_p 同时一致的要求。")
    print("  - S_p 的具体形式仍需等待 GL(3) 自守表示（对应质子）被确定后")
    print("    才能从第一性原理导出；当前 O(1) 量级可由合理的表示归一化容纳。")
    print("=" * 80)


if __name__ == "__main__":
    main()
