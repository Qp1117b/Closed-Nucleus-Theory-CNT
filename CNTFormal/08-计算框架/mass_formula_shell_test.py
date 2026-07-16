#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量公式与整数壳层约束的数值检验（向量化版本）

目标：测试多种由 p-adic AdS/CFT / Vladimirov 格林函数启发的质量公式，
      检查它们能否同时满足：
      (1) 壳层指数 k_i 为整数；
      (2) 最优 α 接近当前经验值（来自重子激发态）；
      (3) g_p 的标度因子保持在物理合理范围（接近博弈不动点值）。

粒子数据（单位 MeV，PDG 2024/2022）:
- p=5 电磁/带电轻子：e, μ, τ
- p=3 弱/up-type 夸克：u, c, t（当前占位）
- p=2 强/down-type 夸克：d, s, b（当前占位）

当前经验 α_p（来自 N(1440), Δ(1232), N(1520) 反解）：
  α_2 = 1.545, α_3 = 0.443, α_5 = 0.826

博弈不动点权重归一化的 g_p（单位 MeV）：
  g_2 ≈ 261.5, g_3 ≈ 469.1, g_5 ≈ 207.6
"""

import numpy as np
from typing import Callable, Tuple, List

# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------

EMPIRICAL_ALPHA = {2: 1.545, 3: 0.443, 5: 0.826}
G_P = {2: 261.5, 3: 469.1, 5: 207.6}

MASSES = {
    5: np.array([0.51099895000, 105.6583755, 1776.86]),          # e, μ, τ
    3: np.array([2.16, 1270.0, 172760.0]),                         # u, c, t
    2: np.array([4.67, 93.4, 4180.0]),                             # d, s, b
}

LABELS = {
    5: ["e", "μ", "τ"],
    3: ["u", "c", "t"],
    2: ["d", "s", "b"],
}

# ---------------------------------------------------------------------------
# 候选质量公式
# ---------------------------------------------------------------------------

def formula_original(p: int, alpha: float, k: np.ndarray) -> np.ndarray:
    """原始公式：m_k = p^{-k*α}（忽略 g 标度）"""
    return np.power(p, -k * alpha)


def formula_shifted(p: int, alpha: float, k: np.ndarray, c: float = 0.0) -> np.ndarray:
    """平移壳层：m_k = p^{-(k+c)*α}"""
    return np.power(p, -(k + c) * alpha)


def formula_green(p: int, alpha: float, k: np.ndarray) -> np.ndarray:
    """
    Vladimirov 格林函数启发：G(x) ~ |x|_p^{α-1}。
    在 |x|_p = p^{-k} 处取值，质量 ∝ p^{-k(α-1)} = p^{k(1-α)}。
    """
    return np.power(p, k * (1.0 - alpha))


def formula_ads_mass(p: int, alpha: float, k: np.ndarray) -> np.ndarray:
    """
    p-adic AdS/CFT 质量-标度维关系，取 Δ = k·α：
      m² = -1 - p + p^{kα} + p^{1-kα}
    质量取 |m²| 的平方根。
    """
    val = -1.0 - p + np.power(p, k * alpha) + np.power(p, 1.0 - k * alpha)
    return np.sqrt(np.abs(val))


def formula_inverse_ads(p: int, alpha: float, k: np.ndarray) -> np.ndarray:
    """
    反用 p-adic AdS/CFT 关系：m ∝ 1 / sqrt(| -1-p+p^{kα}+p^{1-kα} |)。
    """
    val = -1.0 - p + np.power(p, k * alpha) + np.power(p, 1.0 - k * alpha)
    return 1.0 / np.sqrt(np.abs(val))


def formula_cosh(p: int, alpha: float, k: np.ndarray) -> np.ndarray:
    """
    双曲余弦型：m_k = 1 / (p^{kα} + p^{-kα}) = 1 / (2 cosh(k α ln p))。
    """
    return 1.0 / (np.power(p, k * alpha) + np.power(p, -k * alpha))


# ---------------------------------------------------------------------------
# 向量化整数壳层搜索
# ---------------------------------------------------------------------------

def find_best_shells_vectorized(masses: np.ndarray, g: float, p: int, alpha: float,
                                formula: Callable, max_k_diff: int = 50,
                                extra_args: Tuple = ()) -> dict:
    """
    对给定 α 和质量公式，向量化寻找最佳整数壳层 k_i。
    固定 k2 = 0（相对壳层），搜索 dk12 = k1-k2, dk23 = k2-k3。
    """
    dk = np.arange(-max_k_diff, max_k_diff + 1, dtype=np.float64)
    DK12, DK23 = np.meshgrid(dk, dk, indexing='ij')
    DK12 = DK12.ravel()
    DK23 = DK23.ravel()

    # k1 = dk12, k2 = 0, k3 = -dk23
    K = np.stack([DK12, np.zeros_like(DK12), -DK23], axis=0)  # shape (3, N)

    # 计算预测形状 (3, N)
    pred_shape = formula(p, alpha, K, *extra_args)

    # 过滤无效值
    valid = np.all(np.isfinite(pred_shape) & (pred_shape > 0), axis=0)
    pred_shape = pred_shape[:, valid]
    DK12 = DK12[valid]
    DK23 = DK23[valid]

    if pred_shape.size == 0:
        return None

    # 最小二乘拟合标度因子 s：s * pred_shape ≈ masses
    # s = (m · pred) / |pred|² 对每个壳层组合
    s = np.sum(masses[:, None] * pred_shape, axis=0) / np.sum(pred_shape ** 2, axis=0)

    # 只保留 s > 0 的解
    pos = s > 0
    if not np.any(pos):
        return None

    pred_shape = pred_shape[:, pos]
    s = s[pos]
    DK12 = DK12[pos]
    DK23 = DK23[pos]

    pred = s[None, :] * pred_shape
    rel_err = np.sqrt(np.mean(((pred - masses[:, None]) / masses[:, None]) ** 2, axis=0))

    best_idx = np.argmin(rel_err)
    k1 = int(DK12[best_idx])
    k2 = 0
    k3 = -int(DK23[best_idx])

    g_eff = s[best_idx]
    scale_factor = g_eff / g
    return {
        "ks": (k1, k2, k3),
        "scale": scale_factor,        # dimensionless: g_eff / g_p
        "g_eff": g_eff,               # mass scale at reference shell k=0
        "relative_error": rel_err[best_idx],
        "predicted": pred[:, best_idx],
    }


def scan_alpha_for_formula(masses: np.ndarray, g: float, p: int,
                           formula: Callable, alpha_grid: np.ndarray,
                           max_k_diff: int = 50, extra_args: Tuple = ()) -> dict:
    """
    在 α 网格上扫描，找到使整数壳层约束最好满足的最优 α。
    """
    best_overall = None
    best_score = np.inf

    for alpha in alpha_grid:
        res = find_best_shells_vectorized(masses, g, p, alpha, formula,
                                          max_k_diff=max_k_diff, extra_args=extra_args)
        if res is None:
            continue
        # 评分：相对误差 + α 偏离经验值的惩罚 + g 标度偏离惩罚
        alpha_penalty = 0.5 * abs(alpha - EMPIRICAL_ALPHA[p]) / EMPIRICAL_ALPHA[p]
        scale_penalty = 0.5 * max(0.0, np.log10(max(res["scale"], 1e-6))) / 3.0  # 抑制过大标度
        score = res["relative_error"] + alpha_penalty + scale_penalty
        if score < best_score:
            best_score = score
            best_overall = {
                "alpha": alpha,
                **res,
                "score": score,
            }

    return best_overall


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------

def main():
    alpha_grid = np.linspace(0.02, 2.5, 1000)

    formulas: List[Tuple[str, Callable, Tuple]] = [
        ("原始指数 m = g·p^{-kα}", formula_original, ()),
        ("格林函数启发 m = g·p^{k(1-α)}", formula_green, ()),
        ("平移指数 c=1/2", formula_shifted, (0.5,)),
        ("平移指数 c=1", formula_shifted, (1.0,)),
        ("p-adic AdS/CFT m²=-1-p+p^{kα}+p^{1-kα}", formula_ads_mass, ()),
        ("反 AdS/CFT", formula_inverse_ads, ()),
        ("双曲余弦型 m = g/(p^{kα}+p^{-kα})", formula_cosh, ()),
    ]

    print("=" * 90)
    print("质量公式 vs 整数壳层约束 —— 数值扫描结果（向量化）")
    print("=" * 90)

    for p in [5, 3, 2]:
        print(f"\n{'='*90}")
        print(f"p = {p} 扇区 | 经验 α = {EMPIRICAL_ALPHA[p]:.4f} | g_p = {G_P[p]:.2f} MeV")
        print(f"粒子：{LABELS[p]}")
        print(f"质量：{MASSES[p]}")
        print(f"{'-'*90}")

        for name, f, args in formulas:
            res = scan_alpha_for_formula(MASSES[p], G_P[p], p, f, alpha_grid,
                                         max_k_diff=80, extra_args=args)
            if res is None:
                print(f"\n{name}: 无有效整数解")
                continue

            alpha_opt = res["alpha"]
            ks = res["ks"]
            s = res["scale"]
            rel_err = res["relative_error"]
            pred = res["predicted"]
            dev_alpha = alpha_opt - EMPIRICAL_ALPHA[p]

            print(f"\n{name}")
            print(f"  最优 α        = {alpha_opt:.4f}  (偏离经验值 {dev_alpha:+.4f})")
            print(f"  最佳整数壳层  = {ks}")
            print(f"  标度因子 s    = {s:.4f}  (g_eff = s·g = {s*G_P[p]:.2f} MeV)")
            print(f"  相对 RMS 误差 = {rel_err*100:.3f}%")
            print(f"  预测质量      = {pred}")
            print(f"  实验质量      = {MASSES[p]}")


if __name__ == "__main__":
    main()
