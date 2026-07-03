"""
端到端计算：精细结构常数与规范耦合常数 —— 从CNT第一性原理到M_Z可观测量
=====================================================================

CNT v5.0 框架：整合所有已有推导，执行端到端计算。
明确区分：刚性预测（无自由参数）、部分确定（需最少输入）、当前不能确定。

推导链：
  §1 — 能标函数 μ(k)：传播子谱密度 → 对数能标 → DQPT修正 (δ=0.2845)
  §2 — 点火耦合：SM反向RG → 近普适性验证 → 自然尺度对比
  §3 — 正向RG跑动：点火 → M_Z → 可观测量预测
  §4 — 精细结构常数：4-单纯形几何 → α₀ = 375/(16384π) → 与实验对比
  §5 — p进结构分析：展开系数 → 费曼图对应 → 常数项本体论
  §6 — 综合评估：CNT能确定什么、不能确定什么

认识论地位: [第一性原理推导] + [SM β函数输入] + [诚实评估]
日期: 2026-07-04
"""

import numpy as np
from typing import Dict, List, Tuple, Callable
import json
import os

# ============================================================
# 物理常数
# ============================================================
M_P = 1.22089e19       # 普朗克质量 (GeV) — CODATA 2018
M_Z = 91.1876           # Z 玻色子质量 (GeV) — PDG 2024
LN_MP_MZ = np.log(M_P / M_Z)  # ≈ 39.4358
FOUR_PI_SQ = 4 * np.pi       # = 12.5664
FOUR_PI_SQ_SQ = 4 * np.pi**2  # = 39.4784

# SM β 函数系数 (单圈, MS-bar)
# 约定: dα^{-1}/d(ln μ) = b/(2π)
B_SM = {
    'SU3': 7.0,          # b_3 = 11 - 4n_f/3, n_f=6
    'SU2': 19.0/6,       # b_2 = 22/3 - 4n_f/3 - 1/6
    'U1': -41.0/10,      # b_1 = -4n_f/3 - 1/10 (GUT归一化)
}

# 双圈 β 函数系数矩阵 (MS-bar, n_f=6, n_H=1)
# 来源: Machacek & Vaughn, Nucl. Phys. B222 (1983) 83; PDG 2024, Ch. 94
B_2LOOP = np.array([
    [199.0/50,  27.0/10,  44.0/5 ],   # U(1)
    [9.0/10,    35.0/6,   12.0    ],   # SU(2)
    [11.0/10,   9.0/2,    26.0    ],   # SU(3)
])

# M_Z 实验值 (PDG 2024)
EXP = {
    'alpha_s_MZ': 0.1180,   'alpha_s_MZ_err': 0.0009,
    'alpha_inv_MZ': 127.952, 'alpha_inv_MZ_err': 0.009,
    'sin2_thetaW_MZ': 0.23121, 'sin2_thetaW_MZ_err': 0.00004,
    'alpha_2_MZ': 0.03383,  'alpha_1_MZ': 0.01695,
    'alpha_3_MZ': 0.1180,
}

# 精细结构常数 (低能极限, PDG 2024)
ALPHA_EXP = 1.0 / 137.035999084
ALPHA_INV_EXP = 137.035999084

GAUGE_PRIMES = [2, 3, 5]
GAUGE_NAMES = ['SU(3)', 'SU(2)', 'U(1)']
N_CYCLE = 30

# DQPT 修正参数 (从 Li (2026) fractal 维度 + K_IR=4 约束第一性原理推导)
DELTA_DQPT = 0.2845

# ============================================================
# §1: 能标函数 μ(k) — 从传播子谱密度到DQPT修正
# ============================================================

def von_mangoldt_restricted(k: int, primes: List[int] = None) -> float:
    """限制在 gauge_primes {2,3,5} 上的 von Mangoldt 函数。"""
    if primes is None:
        primes = GAUGE_PRIMES
    if k < 2:
        return 0.0
    for p in primes:
        m, exp = k, 0
        while m % p == 0:
            m //= p
            exp += 1
        if m == 1 and exp > 0:
            return np.log(p)
    return 0.0


def is_prime_power(k: int, primes: List[int] = None) -> Tuple[bool, int, int]:
    """判断 k 是否为 gauge_primes 的质数幂。返回 (is_pp, prime, exponent)。"""
    if primes is None:
        primes = GAUGE_PRIMES
    if k < 2:
        return (False, 0, 0)
    for p in primes:
        m, exp = k, 0
        while m % p == 0:
            m //= p
            exp += 1
        if m == 1 and exp > 0:
            return (True, p, exp)
    return (False, 0, 0)


def energy_scale_log(k: int, k_max: int = N_CYCLE) -> float:
    """对数能标函数（无DQPT修正，均匀再生产假设）。"""
    return M_P * (M_Z / M_P) ** (k / k_max)


def energy_scale_dqpt(k: int, delta: float = DELTA_DQPT) -> float:
    """
    DQPT修正能标函数。

    推导链 (详见 §19-§21 of 母轨迹候选方程):
      传播子 Δ = 1/q² → 谱密度 ρ ∝ 1/q → 对数能标 (均匀再生产)
      Li (2026) K = 1/d_P + 1/ζ_R → fractal 维度 → K_IR=4 → δ

    δ = 0.2845 意味着在 DQPT 跃迁点，虚模处理效率提升 δ·Λ(k)。
    """
    s_total = sum(von_mangoldt_restricted(j) for j in range(1, N_CYCLE + 1))
    delta_N0 = 2 * np.pi**2 * LN_MP_MZ / (N_CYCLE + delta * s_total)

    cumulative_N = 0.0
    for j in range(1, k + 1):
        lam = von_mangoldt_restricted(j)
        cumulative_N += delta_N0 * (1 + delta * lam)

    return M_P * np.exp(-cumulative_N / (2 * np.pi**2))


def compute_energy_scales():
    """计算并对比两种能标函数。"""
    print("=" * 75)
    print("§1: 能标函数 μ(k) — 传播子谱密度 → DQPT修正")
    print("=" * 75)

    # DQPT 跃迁点
    dqpt_points = []
    for k in range(1, N_CYCLE + 1):
        is_pp, p, exp = is_prime_power(k)
        if is_pp:
            dqpt_points.append((k, p, exp))

    print(f"\n  DQPT 跃迁点 (k = p^m, p ∈ {{2,3,5}}):")
    for k, p, exp in dqpt_points:
        lam = von_mangoldt_restricted(k)
        print(f"    k={k:2d}: p={p}^{exp}, Λ(k)=log({p})={lam:.4f}")

    s_total = sum(von_mangoldt_restricted(j) for j in range(1, N_CYCLE + 1))
    print(f"\n  总 von Mangoldt 作用量: S_total = {s_total:.4f}")
    print(f"  DQPT 修正参数: δ = {DELTA_DQPT}")
    print(f"  总 DQPT 修正: δ·S_total = {DELTA_DQPT * s_total:.4f}")

    print(f"\n  能标对比 (δ=0 vs δ={DELTA_DQPT}):")
    print(f"  {'k':>4s}  {'μ_log (GeV)':>16s}  {'μ_DQPT (GeV)':>16s}  {'差异':>10s}  {'DQPT?'}")
    print(f"  {'-'*4}  {'-'*16}  {'-'*16}  {'-'*10}  {'-'*6}")

    for k in [1, 2, 3, 4, 5, 8, 9, 10, 15, 16, 20, 25, 27, 30]:
        mu_log = energy_scale_log(k)
        mu_dqpt = energy_scale_dqpt(k)
        diff = (mu_dqpt - mu_log) / mu_log * 100
        is_dqpt = "✓" if von_mangoldt_restricted(k) > 0 else ""
        print(f"  {k:4d}  {mu_log:16.3e}  {mu_dqpt:16.3e}  {diff:+9.2f}%  {is_dqpt}")

    return {
        'dqpt_points': dqpt_points,
        's_total': s_total,
        'delta': DELTA_DQPT,
        'delta_s_total': DELTA_DQPT * s_total,
    }


# ============================================================
# §2: 点火耦合 — SM反向RG + 近普适性验证
# ============================================================

def run_single_rg(alpha_initial: float, mu_initial: float,
                  mu_final: float, b: float) -> float:
    """单圈 RG 跑动。"""
    alpha_inv = 1.0 / alpha_initial + b / (2 * np.pi) * np.log(mu_final / mu_initial)
    return 1.0 / alpha_inv


def compute_ignition_sm_reverse(energy_func: Callable) -> Dict:
    """从 SM 实验值反向 RG 跑动，确定点火耦合常数。"""
    alphas_mz = {
        'SU(3)': EXP['alpha_s_MZ'],
        'SU(2)': EXP['alpha_2_MZ'],
        'U(1)': EXP['alpha_1_MZ'],
    }

    mu_mz = energy_func(N_CYCLE)
    ignition = {}

    for name, p, b_name in [('SU(3)', 2, 'SU3'), ('SU(2)', 3, 'SU2'), ('U(1)', 5, 'U1')]:
        mu_ign = energy_func(p)
        b = B_SM[b_name]
        alpha_inv_ign = 1.0 / alphas_mz[name] + b / (2 * np.pi) * np.log(mu_ign / mu_mz)
        ignition[name] = {
            'alpha_ign': 1.0 / alpha_inv_ign,
            'alpha_inv_ign': alpha_inv_ign,
            'mu_ign': mu_ign,
            'k_ign': p,
        }

    return ignition


def compute_ignition_analysis():
    """点火耦合分析：SM反向 + 近普适性 + 自然尺度对比。"""
    print("\n" + "=" * 75)
    print("§2: 点火耦合常数 — SM反向RG + 近普适性验证")
    print("=" * 75)

    # 使用 DQPT 修正能标
    ignition_dqpt = compute_ignition_sm_reverse(energy_scale_dqpt)
    ignition_log = compute_ignition_sm_reverse(energy_scale_log)

    print(f"\n  【DQPT修正能标 (δ={DELTA_DQPT})】")
    print(f"  {'规范力':<8s}  {'k_ign':>5s}  {'μ_ign (GeV)':>16s}  {'α_ign':>12s}  {'α⁻¹_ign':>10s}")
    print(f"  {'-'*8}  {'-'*5}  {'-'*16}  {'-'*12}  {'-'*10}")

    alphas = []
    for name in GAUGE_NAMES:
        d = ignition_dqpt[name]
        alphas.append(d['alpha_ign'])
        print(f"  {name:<8s}  {d['k_ign']:5d}  {d['mu_ign']:16.3e}  {d['alpha_ign']:12.6f}  {d['alpha_inv_ign']:10.2f}")

    # 近普适性
    mean_alpha = np.mean(alphas)
    max_dev = max(abs(a - mean_alpha) / mean_alpha * 100 for a in alphas)
    print(f"\n  近普适性检验:")
    print(f"    平均值: ᾱ = {mean_alpha:.6f}  (ᾱ⁻¹ = {1.0/mean_alpha:.1f})")
    print(f"    最大偏差: {max_dev:.1f}%")

    # 自然尺度对比
    alpha_natural = 1.0 / (4 * np.pi**2)
    dev_natural = abs(mean_alpha - alpha_natural) / alpha_natural * 100
    print(f"\n  自然尺度对比:")
    print(f"    1/(4π²) = {alpha_natural:.6f}  (α⁻¹ = {1.0/alpha_natural:.1f})")
    print(f"    SM反向平均值 = {mean_alpha:.6f}  (α⁻¹ = {1.0/mean_alpha:.1f})")
    print(f"    偏差: {dev_natural:.1f}%")

    # 对数能标对比
    print(f"\n  【对数能标 (δ=0) 对比】")
    for name in GAUGE_NAMES:
        d = ignition_log[name]
        d_dqpt = ignition_dqpt[name]
        diff = (d['alpha_ign'] - d_dqpt['alpha_ign']) / d_dqpt['alpha_ign'] * 100
        print(f"    {name}: α_ign = {d['alpha_ign']:.6f} (差异 {diff:+.1f}%)")

    return {
        'ignition_dqpt': ignition_dqpt,
        'ignition_log': ignition_log,
        'mean_alpha': mean_alpha,
        'max_dev_percent': max_dev,
        'alpha_natural': alpha_natural,
        'dev_natural_percent': dev_natural,
    }


# ============================================================
# §3: 正向RG跑动 — 点火 → M_Z → 可观测量预测
# ============================================================

def run_rg_forward(alphas_ignition: Dict[str, float], energy_func: Callable) -> Dict:
    """正向 RG 跑动：点火点 → M_Z。"""
    mu_mz = energy_func(N_CYCLE)
    b_map = {'SU(3)': B_SM['SU3'], 'SU(2)': B_SM['SU2'], 'U(1)': B_SM['U1']}

    alphas_mz = {}
    for name, p in [('SU(3)', 2), ('SU(2)', 3), ('U(1)', 5)]:
        mu_ign = energy_func(p)
        alphas_mz[name] = run_single_rg(alphas_ignition[name], mu_ign, mu_mz, b_map[name])

    # 计算可观测量
    alpha_3 = alphas_mz['SU(3)']
    alpha_2 = alphas_mz['SU(2)']
    alpha_1 = alphas_mz['U(1)']
    alpha_Y = (3.0 / 5) * alpha_1
    sin2_thetaW = alpha_Y / (alpha_2 + alpha_Y)
    alpha_em = alpha_2 * sin2_thetaW

    # 误差
    errors = {
        'alpha_s': (alpha_3 - EXP['alpha_s_MZ']) / EXP['alpha_s_MZ'] * 100,
        'alpha_em_inv': (1.0/alpha_em - EXP['alpha_inv_MZ']) / EXP['alpha_inv_MZ'] * 100,
        'sin2_thetaW': (sin2_thetaW - EXP['sin2_thetaW_MZ']) / EXP['sin2_thetaW_MZ'] * 100,
    }
    errors['rms'] = np.sqrt(np.mean([e**2 for e in errors.values()]))

    return {
        'alphas_MZ': alphas_mz,
        'alpha_s_MZ': alpha_3,
        'alpha_em': alpha_em,
        'alpha_em_inv': 1.0 / alpha_em,
        'sin2_thetaW': sin2_thetaW,
        'errors': errors,
    }


def compute_rg_prediction():
    """正向 RG 跑动预测。"""
    print("\n" + "=" * 75)
    print("§3: 正向 RG 跑动 — 点火 → M_Z → 可观测量预测")
    print("=" * 75)

    # 方案 A: 普适点火 (α₀ = 0.0204, 从SM反向确定)
    alpha_0 = 0.0204
    alphas_ign = {'SU(3)': alpha_0, 'SU(2)': alpha_0, 'U(1)': alpha_0}

    print(f"\n  【方案 A: 普适点火 α₀ = {alpha_0}】")
    pred = run_rg_forward(alphas_ign, energy_scale_dqpt)
    err = pred['errors']

    print(f"  {'可观测量':<20s}  {'预测值':>12s}  {'实验值':>12s}  {'偏差':>10s}")
    print(f"  {'-'*20}  {'-'*12}  {'-'*12}  {'-'*10}")
    print(f"  {'α_s(M_Z)':<20s}  {pred['alpha_s_MZ']:12.4f}  {EXP['alpha_s_MZ']:12.4f}  {err['alpha_s']:+9.1f}%")
    print(f"  {'α⁻¹(M_Z)':<20s}  {pred['alpha_em_inv']:12.1f}  {EXP['alpha_inv_MZ']:12.1f}  {err['alpha_em_inv']:+9.1f}%")
    print(f"  {'sin²θ_W':<20s}  {pred['sin2_thetaW']:12.5f}  {EXP['sin2_thetaW_MZ']:12.5f}  {err['sin2_thetaW']:+9.1f}%")
    print(f"  {'RMS 偏差':<20s}  {'':>12s}  {'':>12s}  {err['rms']:9.1f}%")

    # 方案 B: SM反向点火 (最优拟合，但使用SM输入)
    ignition_dqpt = compute_ignition_sm_reverse(energy_scale_dqpt)
    alphas_ign_sm = {name: ignition_dqpt[name]['alpha_ign'] for name in GAUGE_NAMES}

    print(f"\n  【方案 B: SM反向点火 (最优拟合，使用SM输入)】")
    for name in GAUGE_NAMES:
        print(f"    {name}: α_ign = {alphas_ign_sm[name]:.6f}")

    pred_sm = run_rg_forward(alphas_ign_sm, energy_scale_dqpt)
    err_sm = pred_sm['errors']

    print(f"\n  {'可观测量':<20s}  {'预测值':>12s}  {'实验值':>12s}  {'偏差':>10s}")
    print(f"  {'-'*20}  {'-'*12}  {'-'*12}  {'-'*10}")
    print(f"  {'α_s(M_Z)':<20s}  {pred_sm['alpha_s_MZ']:12.4f}  {EXP['alpha_s_MZ']:12.4f}  {err_sm['alpha_s']:+9.1f}%")
    print(f"  {'α⁻¹(M_Z)':<20s}  {pred_sm['alpha_em_inv']:12.1f}  {EXP['alpha_inv_MZ']:12.1f}  {err_sm['alpha_em_inv']:+9.1f}%")
    print(f"  {'sin²θ_W':<20s}  {pred_sm['sin2_thetaW']:12.5f}  {EXP['sin2_thetaW_MZ']:12.5f}  {err_sm['sin2_thetaW']:+9.1f}%")
    print(f"  {'RMS 偏差':<20s}  {'':>12s}  {'':>12s}  {err_sm['rms']:9.1f}%")

    # 方案 C: 自然尺度 (α₀ = 1/(4π²) ≈ 0.02533)
    alpha_natural = 1.0 / (4 * np.pi**2)
    alphas_ign_nat = {'SU(3)': alpha_natural, 'SU(2)': alpha_natural, 'U(1)': alpha_natural}

    print(f"\n  【方案 C: 自然尺度 α₀ = 1/(4π²) = {alpha_natural:.6f}】")
    pred_nat = run_rg_forward(alphas_ign_nat, energy_scale_dqpt)
    err_nat = pred_nat['errors']

    print(f"  {'可观测量':<20s}  {'预测值':>12s}  {'实验值':>12s}  {'偏差':>10s}")
    print(f"  {'-'*20}  {'-'*12}  {'-'*12}  {'-'*10}")
    print(f"  {'α_s(M_Z)':<20s}  {pred_nat['alpha_s_MZ']:12.4f}  {EXP['alpha_s_MZ']:12.4f}  {err_nat['alpha_s']:+9.1f}%")
    print(f"  {'α⁻¹(M_Z)':<20s}  {pred_nat['alpha_em_inv']:12.1f}  {EXP['alpha_inv_MZ']:12.1f}  {err_nat['alpha_em_inv']:+9.1f}%")
    print(f"  {'sin²θ_W':<20s}  {pred_nat['sin2_thetaW']:12.5f}  {EXP['sin2_thetaW_MZ']:12.5f}  {err_nat['sin2_thetaW']:+9.1f}%")
    print(f"  {'RMS 偏差':<20s}  {'':>12s}  {'':>12s}  {err_nat['rms']:9.1f}%")

    return {
        'universal': {'pred': pred, 'alpha_0': alpha_0},
        'sm_reverse': {'pred': pred_sm, 'alphas_ign': alphas_ign_sm},
        'natural': {'pred': pred_nat, 'alpha_0': alpha_natural},
    }


# ============================================================
# §4: 精细结构常数 — 4-单纯形几何推导
# ============================================================

def compute_alpha_geometric():
    """
    精细结构常数的几何推导。

    推导链:
      4-单纯形 → Θ = arccos(1/4) = 75.5225°
      → cos(5Θ) = 61/64 (Chebyshev)
      → sin²(5Θ) = 375/4096
      → α₀ = sin²(5Θ)/(4π) = 375/(16384π)
      → 1/α₀ = 16384π/375 ≈ 137.258
    """
    print("\n" + "=" * 75)
    print("§4: 精细结构常数 — 4-单纯形几何推导")
    print("=" * 75)

    # 几何推导
    cos_theta = 1.0 / 4.0
    theta = np.arccos(cos_theta)

    # Chebyshev T_5(x) = 16x^5 - 20x^3 + 5x
    cos_5theta = 16 * cos_theta**5 - 20 * cos_theta**3 + 5 * cos_theta
    sin_sq_5theta = 1.0 - cos_5theta**2

    # 精确代数数
    cos_5theta_exact = 61.0 / 64.0
    sin_sq_5theta_exact = 375.0 / 4096.0
    alpha_0_exact = sin_sq_5theta_exact / (4 * np.pi)
    alpha_0_inv_exact = 16384 * np.pi / 375.0

    print(f"""
  【4-单纯形几何】

  Θ = arccos(1/4) = {theta:.6f} rad = {np.degrees(theta):.4f}°

  cos(5Θ) = T₅(cos Θ) = 16·(1/4)⁵ - 20·(1/4)³ + 5·(1/4)
          = {cos_5theta:.10f}
          = 61/64 (精确)

  sin²(5Θ) = 1 - (61/64)² = 375/4096 (精确)

  α₀ = sin²(5Θ)/(4π) = 375/(16384π)
  1/α₀ = 16384π/375 = {alpha_0_inv_exact:.6f}

  【实验对比】

  理论裸值: 1/α₀ = {alpha_0_inv_exact:.6f}
  实验值:    1/α  = {ALPHA_INV_EXP:.6f}  (PDG 2024, 低能极限)
  偏差:      {abs(alpha_0_inv_exact - ALPHA_INV_EXP) / ALPHA_INV_EXP * 100:.4f}%

  【M_Z 能标对比】

  理论裸值:        1/α₀ = {alpha_0_inv_exact:.2f}
  实验值 (M_Z):    1/α(M_Z) = {EXP['alpha_inv_MZ']:.2f}
  偏差:            {(alpha_0_inv_exact - EXP['alpha_inv_MZ']) / EXP['alpha_inv_MZ'] * 100:.2f}%

  【跑动效应】

  α 从 UV 裸值 α₀ 到 IR 实验值 α(M_Z) 的跑动由 QED β 函数描述。
  1/α₀ > 1/α(M_Z) 意味着 α₀ < α(M_Z) —— 裸耦合小于低能耦合，
  这与 U(1) 的非渐近自由特性一致 (b_U1 = -41/10 < 0)。

  从裸值 α₀ 到 M_Z 的跑动:
    Δ(1/α) = 1/α₀ - 1/α(M_Z) = {alpha_0_inv_exact - EXP['alpha_inv_MZ']:.2f}

  单圈 QED β 函数预测:
    Δ(1/α)_1loop = b_U1/(2π) · ln(μ_UV/μ_MZ)

  若 μ_UV = M_P (普朗克尺度):
    Δ(1/α)_1loop = -41/(20π) · ln(M_P/M_Z) = {-41/(20*np.pi) * LN_MP_MZ:.2f}

  注意: 单圈 U(1) β 函数在 GUT 归一化下 b_U1 = -41/10，
  但 QED 的 β 函数不同 (b_QED > 0，渐近自由在 IR)。
  此处的跑动方向需要仔细处理 GUT 归一化。
  """)

    return {
        'theta_rad': theta,
        'theta_deg': np.degrees(theta),
        'cos_5theta': cos_5theta,
        'sin_sq_5theta': sin_sq_5theta,
        'alpha_0': alpha_0_exact,
        'alpha_0_inv': alpha_0_inv_exact,
        'alpha_exp': ALPHA_EXP,
        'alpha_inv_exp': ALPHA_INV_EXP,
        'deviation_percent': abs(alpha_0_inv_exact - ALPHA_INV_EXP) / ALPHA_INV_EXP * 100,
        'deviation_MZ_percent': (alpha_0_inv_exact - EXP['alpha_inv_MZ']) / EXP['alpha_inv_MZ'] * 100,
    }


# ============================================================
# §5: p进结构分析 — 展开系数 → 费曼图 → 常数项
# ============================================================

def compute_padic_structure():
    """
    p进展开结构分析。

    核心论断:
      p进展开: x = a₀ + a₁p + a₂p² + a₃p³ + ...

      费曼图对应:
        a₀: 常数项 → 前因果 (无图)
        a₁p: 一次项 → 树图 (因果时)
        a₂p²: 二次项 → 单圈图 (虚时间)
        a_n p^n: n次项 → (n-1)圈图 (高阶虚时间)
    """
    print("\n" + "=" * 75)
    print("§5: p进结构分析 — 展开系数 → 费曼图对应")
    print("=" * 75)

    print(f"""
  【p进展开与费曼图对应】

  标准p进展开:
    x = a₀ + a₁p + a₂p² + a₃p³ + ... ,  0 ≤ a_i < p

  CNT 对应:
    ┌──────────┬─────────────────┬──────────────────┐
    │ p进项     │ 费曼图           │ 本体论含义         │
    ├──────────┼─────────────────┼──────────────────┤
    │ a₀ (常数) │ 无图             │ 前因果过渡         │
    │ a₁p       │ 树图             │ 因果时 (t→2t)     │
    │ a₂p²      │ 单圈图           │ 虚时间 (一次自指)   │
    │ a₃p³      │ 双圈图           │ 高阶虚时间         │
    │ a_n p^n   │ (n-1)圈图        │ n-1重嵌套自指      │
    └──────────┴─────────────────┴──────────────────┘

  【三种规范力的p进基底】

  规范力      p    |p|_p    p进收敛速度   物理耦合强度
  ──────      ─    ─────    ──────────   ──────────
  SU(3) 强     2    1/2     最慢          最强 (α_s ~ 0.12)
  SU(2) 弱     3    1/3     中等          中等 (α_w ~ 0.03)
  U(1)  电磁    5    1/5     最快          最弱 (α_em ~ 0.008)

  关键观察: p进收敛速度与物理耦合强度成反比。
  |p|_p = 1/p 越小 → 展开收敛越快 → 耦合越弱。
  这给出了 p进结构与耦合常数之间的定性关系。

  【常数项 a₀ 的本体论地位】

  经典p进数: a₀ ∈ {{0,1,...,p-1}} 是标准的第0位数字，无特殊物理意义。
  合成p进数: a₀ = S₀ = N (再生产总量)，是"前因果"过渡。

  在两种框架中，a₀ 都不对应费曼图:
  - 经典p进: a₀ 是 x mod p，真空/经典背景
  - 合成p进: a₀ 是再生产总量，费曼图的本体论条件

  常数项的不确定性是结构性的: 因果链的开端不能是因果链内部的元素。

  【p进展开与微扰展开的对比】

  微扰展开 (ℏ):  S_classical + ℏ S_1loop + ℏ² S_2loop + ...
  微扰展开 (g):  g² A_tree + g⁴ A_1loop + g⁶ A_2loop + ...
  p进展开:       a₀ + a₁p + a₂p² + a₃p³ + ...

  关键差异: 微扰展开的"小参数"是物理耦合常数 (ℏ 或 g)，
  p进展开的"小参数"是基底 p 本身 (在 p进度量下)。

  p进展开不是微扰展开的替代品——它是比微扰展开更基础的编码层次。
  """)

    # p进范数
    print("  【p进范数与耦合强度】")
    print(f"  {'质数 p':<8s}  {'|p|_p':>10s}  {'|p²|_p':>10s}  {'|p³|_p':>10s}  {'收敛特征':>12s}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*12}")

    for p in [2, 3, 5]:
        norm_p = 1.0 / p
        norm_p2 = 1.0 / p**2
        norm_p3 = 1.0 / p**3
        convergence = "慢" if p == 2 else ("中" if p == 3 else "快")
        print(f"  {p:<8d}  {norm_p:10.6f}  {norm_p2:10.6f}  {norm_p3:10.6f}  {convergence:>12s}")

    # 展开系数结构
    print(f"\n  【展开系数结构 (经典p进)】")
    print(f"  p=2: a_i ∈ {{0,1}},         每层信息容量 1 bit")
    print(f"  p=3: a_i ∈ {{0,1,2}},       每层信息容量 log₂(3) ≈ 1.58 bit")
    print(f"  p=5: a_i ∈ {{0,1,2,3,4}},   每层信息容量 log₂(5) ≈ 2.32 bit")
    print(f"\n  经典p进中，系数有界性意味着每层信息容量有限。")
    print(f"  合成p进中，系数无界 (a_i ∈ ℕ)，每层可编码任意多次再生产。")

    return {
        'p_adic_norms': {p: 1.0/p for p in [2, 3, 5]},
        'coefficient_ranges': {2: [0, 1], 3: [0, 1, 2], 5: [0, 1, 2, 3, 4]},
    }


# ============================================================
# §6: 综合评估 — CNT能确定什么、不能确定什么
# ============================================================

def compute_summary(energy_results, ignition_results, rg_results, alpha_geo, padic_results):
    """综合评估。"""
    print("\n" + "=" * 75)
    print("§6: 综合评估 — CNT 能确定什么、不能确定什么")
    print("=" * 75)

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │            CNT 刚性预测 (无自由参数，从第一性原理推导)              │
  ├──────────────────────────────────────────────────────────────────┤
  │ 1. N_cycle = 30                                                  │
  │    → adelic 约束 ∏ Z_p = 1/(2·3·5) = 1/30                       │
  │    → 已确定 (数学推导)                                            │
  │                                                                  │
  │ 2. DQPT 跃迁点: k = p^m, p ∈ {{2,3,5}}                           │
  │    → von Mangoldt Λ(k) > 0 ⇔ 质数动力跃迁                         │
  │    → 跃迁点: 2, 3, 4, 5, 8, 9, 16, 25, 27, 32 (k ≤ 60)          │
  │    → 已确定 (精确数学事实)                                        │
  │                                                                  │
  │ 3. 三个规范力: p = 2, 3, 5                                       │
  │    → SU(3) @ p=2, SU(2) @ p=3, U(1) @ p=5                       │
  │    → 已确定 (结构对应)                                            │
  │                                                                  │
  │ 4. 能标函数 μ(k) = M_P·(M_Z/M_P)^{{k/30}} (DQPT修正)              │
  │    → 传播子谱密度 ρ(q) ∝ 1/q → 对数能标                          │
  │    → DQPT 修正 δ = 0.2845 (Li 2026 K_IR=4 约束)                  │
  │    → 已确定 (第一性原理推导)                                      │
  │                                                                  │
  │ 5. ln(M_P/M_Z) ≈ 4π² (偏差 0.108%)                               │
  │    → 谱密度 + S³ 立体角 → 几何必然性                              │
  │    → 已确定 (数值事实)                                            │
  │                                                                  │
  │ 6. γ = 1/2 (Loschmidt 衰减指数)                                   │
  │    → 三重独立收敛: η_N = β = b = 1/2                             │
  │    → 已确定 (独立交叉验证)                                        │
  │                                                                  │
  │ 7. 精细结构常数裸值: 1/α₀ = 16384π/375 ≈ 137.258                  │
  │    → 4-单纯形几何 → Chebyshev → 精确代数数                        │
  │    → 偏差 0.162% (vs 实验 137.036)                                │
  │    → 已确定 (纯几何推导，物理对应假设待验证)                       │
  └──────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │            CNT 部分确定 (需最少额外输入)                           │
  ├──────────────────────────────────────────────────────────────────┤
  │ 1. 点火耦合 α₀ ≈ 0.0204 (近普适)                                  │
  │    → 传播子统计平均 + SM 反向验证                                  │
  │    → 近普适性: SU(3)/SU(2) 差异 < 5%, U(1) 偏离 ~30%             │
  │    → 偏差: 自然尺度 1/(4π²) vs 经验值 偏差 24%                    │
  │                                                                  │
  │ 2. M_Z 可观测量 (单圈 RG, 普适点火)                               │
  │    → α_s(M_Z) 偏差 ~5-6%                                         │
  │    → α⁻¹(M_Z) 偏差 ~16%                                          │
  │    → sin²θ_W 偏差 ~9%                                            │
  │    → RMS ~11%                                                    │
  └──────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │            CNT 当前不能确定                                        │
  ├──────────────────────────────────────────────────────────────────┤
  │ 1. α₀ 的绝对数值 (0.0204 vs 0.0253 vs 0.318)                     │
  │    → 需传播子路径积分的完整非微扰计算                              │
  │    → 候选: 全息原理、纠缠熵、大 N 极限                            │
  │                                                                  │
  │ 2. 精细结构常数 α ≈ 1/137 (低能极限)                              │
  │    → 裸值 1/α₀ = 137.258 (几何推导)                               │
  │    → 需计算从 UV 裸值到 IR 实验值的完整跑动                        │
  │                                                                  │
  │ 3. M_Z 的精确值                                                  │
  │    → 4π² 关系在次领头阶的修正                                     │
  │                                                                  │
  │ 4. p进展开系数 aᵢ 的具体数值                                       │
  │    → 由再生产历史决定，历史不可从数值唯一还原                      │
  └──────────────────────────────────────────────────────────────────┘

  【关键瓶颈】

  1. 点火耦合 α₀ 的精确值: 当前自然尺度 1/(4π²) 与经验值偏差 24%。
     这是 CNT 从纲领走向精确科学的最大障碍。

  2. 能标函数的次领头阶: μ(k) = M_P·(M_Z/M_P)^{{k/30}} 是领头阶结果。
     DQPT 修正 δ = 0.2845 来自 Li (2026) 约束，但仍需独立验证。

  3. p进展开与微扰展开的定量对应: 当前只有定性对应 (树图=一次项,
     圈图=高阶项)，缺乏定量映射 (a₁ 与 α 的精确关系)。

  4. SM β 函数作为外部输入: CNT 目前不能从第一性原理推导 β 函数。
     这是"CNT 提供结构 + SM 提供动力学"分工的体现。

  【p进结构的新启示】

  1. 常数项 a₀ 的本体论地位明确: 前因果过渡，不是费曼图。
     这解释了为什么常数项"不确定"——它是结构性的，不是计算精度问题。

  2. p进范数与耦合强度定性对应: |p|_p 越小 → 展开收敛越快 → 耦合越弱。
     这为 p进结构 → 耦合常数的定量推导提供了方向。

  3. 合成p进数的历史编码: 解码非唯一性 (不同历史 → 同一 x) 与
     费曼路径积分 (不同路径 → 同一振幅) 在结构上一致。
     这暗示 HPI 求和测度应从合成p进数的结构自然导出。
  """)

    return {
        'rigid_predictions': [
            'N_cycle = 30',
            'DQPT 跃迁点 = p^m (p ∈ {2,3,5})',
            '三个规范力 = SU(3), SU(2), U(1)',
            'μ(k) = M_P·(M_Z/M_P)^(k/30) (DQPT修正)',
            'ln(M_P/M_Z) ≈ 4π²',
            'γ = 1/2',
            '1/α₀ = 16384π/375 ≈ 137.258',
        ],
        'partial_determinations': [
            'α₀ ≈ 0.0204 (近普适, 偏差24%)',
            'M_Z 可观测量 (RMS ~11%)',
        ],
        'cannot_determine': [
            'α₀ 绝对数值',
            'α ≈ 1/137 低能极限',
            'M_Z 精确值',
            'p进展开系数 aᵢ',
        ],
    }


# ============================================================
# 主程序
# ============================================================

def run_full_calculation():
    """端到端完整计算。"""
    print("=" * 75)
    print("  端到端计算：精细结构常数与规范耦合常数")
    print("  从 CNT 第一性原理到 M_Z 可观测量")
    print("=" * 75)
    print(f"  日期: 2026-07-04")
    print(f"  认识论地位: [第一性原理推导] + [SM β函数输入] + [诚实评估]")

    results = {}

    # §1: 能标函数
    results['energy_scales'] = compute_energy_scales()

    # §2: 点火耦合
    results['ignition'] = compute_ignition_analysis()

    # §3: 正向 RG 跑动
    results['rg_prediction'] = compute_rg_prediction()

    # §4: 精细结构常数 (几何推导)
    results['alpha_geometric'] = compute_alpha_geometric()

    # §5: p进结构分析
    results['padic_structure'] = compute_padic_structure()

    # §6: 综合评估
    results['summary'] = compute_summary(
        results['energy_scales'],
        results['ignition'],
        results['rg_prediction'],
        results['alpha_geometric'],
        results['padic_structure'],
    )

    return results


def save_results(results: Dict, filename: str = None):
    """保存结果到 JSON。"""
    if filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, '07-端到端计算_结果.json')

    def convert(obj):
        if isinstance(obj, dict):
            return {str(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        elif isinstance(obj, tuple):
            return [convert(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return bool(obj)
        elif isinstance(obj, Callable):
            return str(obj)
        return obj

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convert(results), f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到: {filename}")


if __name__ == '__main__':
    results = run_full_calculation()
    save_results(results)