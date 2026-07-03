"""
双圈 RG 修正：系统误差分析
==========================

CNT v5.0 框架：引入双圈 β 函数修正，评估其对耦合常数预测精度的改进。

核心问题：
  单圈 RG 跑动 RMS 偏差 ~10.6%，其中 α⁻¹(M_Z) 偏差 ~16%
  双圈修正能否显著减小系统误差？
  双圈修正能否解释 α₀ 的 24% 偏差（1/(4π²) vs 0.0204）？

双圈 RG 方程（MS-bar 方案）：
  dα_i⁻¹/d(ln μ) = b_i/(2π) + Σ_j b_ij α_j/(8π²)

  其中 b_i 是单圈系数，b_ij 是双圈系数矩阵。

SM 双圈系数 (n_f=6, n_H=1, from Machacek & Vaughn 1983, PDG 2024):
  b_ij = [199/50    27/10    44/5 ]
         [9/10      35/6     12   ]
         [11/10     9/2      26   ]

  索引: 1=U(1), 2=SU(2), 3=SU(3)

认识论地位: [第一性原理推导] + [SM 微扰展开输入]
"""

import numpy as np
from typing import Dict, List, Tuple, Callable
import json
import os

# ============================================================
# 物理常数
# ============================================================
M_P = 1.22089e19       # 普朗克质量 (GeV)
M_Z = 91.1876           # Z 玻色子质量 (GeV)
LN_MP_MZ = np.log(M_P / M_Z)  # ≈ 39.44
FOUR_PI_SQUARED = 4 * np.pi**2  # = 39.4784

# ============================================================
# 单圈 β 函数系数 (MS-bar)
# 约定: dα⁻¹/d(ln μ) = b/(2π)
# ============================================================
B_1LOOP = np.array([-41.0/10, 19.0/6, 7.0])  # [U(1), SU(2), SU(3)]

# ============================================================
# 双圈 β 函数系数矩阵 (MS-bar, n_f=6, n_H=1)
# 约定: dα_i⁻¹/d(ln μ) = b_i/(2π) + Σ_j b_ij α_j/(8π²)
# 来源: Machacek & Vaughn, Nucl. Phys. B222 (1983) 83
#       PDG 2024, Ch. 94 "Grand Unified Theories"
# ============================================================
B_2LOOP = np.array([
    [199.0/50,  27.0/10,  44.0/5 ],   # U(1) 行: b_1j
    [9.0/10,    35.0/6,   12.0    ],   # SU(2) 行: b_2j
    [11.0/10,   9.0/2,    26.0    ],   # SU(3) 行: b_3j
])

# 规范力名称和索引
GAUGE_NAMES = ['U(1)', 'SU(2)', 'SU(3)']
GAUGE_PRIMES = [5, 3, 2]  # 对应 U(1), SU(2), SU(3)
N_CYCLE = 30

# M_Z 实验值 (PDG 2024)
EXP = {
    'alpha_s_MZ': 0.1180,   'alpha_s_MZ_err': 0.0009,
    'alpha_inv_MZ': 127.952, 'alpha_inv_MZ_err': 0.009,
    'sin2_thetaW_MZ': 0.23121, 'sin2_thetaW_MZ_err': 0.00004,
    'alpha_2_MZ': 0.03383,  'alpha_1_MZ': 0.01695,
    'alpha_3_MZ': 0.1180,
}

# ============================================================
# 能标函数 (DQPT 修正)
# ============================================================

def von_mangoldt_restricted(k: int, primes: List[int] = None) -> float:
    if primes is None: primes = [2, 3, 5]
    if k < 2: return 0.0
    for p in primes:
        m, exp = k, 0
        while m % p == 0:
            m //= p; exp += 1
        if m == 1 and exp > 0: return np.log(p)
    return 0.0

def energy_scale_dqpt(k: int, delta: float = 0.2845) -> float:
    """DQPT 修正能标函数。"""
    s_total = sum(von_mangoldt_restricted(j) for j in range(1, N_CYCLE + 1))
    delta_N0 = 2 * np.pi**2 * LN_MP_MZ / (N_CYCLE + delta * s_total)
    cumulative_N = 0.0
    for j in range(1, k + 1):
        lam = von_mangoldt_restricted(j)
        cumulative_N += delta_N0 * (1 + delta * lam)
    return M_P * np.exp(-cumulative_N / (2 * np.pi**2))

def energy_scale_log(k: int) -> float:
    """对数能标函数（无 DQPT 修正）。"""
    return M_P * (M_Z / M_P) ** (k / N_CYCLE)


# ============================================================
# 第1部分：单圈 RG 跑动（基准）
# ============================================================

def run_one_loop(alpha_initial: float, mu_initial: float, mu_final: float, b: float) -> float:
    """单圈 RG 跑动（解耦的）。"""
    alpha_inv = 1.0 / alpha_initial + b / (2 * np.pi) * np.log(mu_final / mu_initial)
    return 1.0 / alpha_inv

def one_loop_forward(alphas_ignition: np.ndarray, mu_ign: np.ndarray, mu_mz: float) -> np.ndarray:
    """单圈正向 RG 跑动（三个规范力独立）。"""
    alphas_mz = np.zeros(3)
    for i in range(3):
        alphas_mz[i] = run_one_loop(alphas_ignition[i], mu_ign[i], mu_mz, B_1LOOP[i])
    return alphas_mz


# ============================================================
# 第2部分：双圈 RG 跑动 — 耦合 ODE 系统
# ============================================================

def two_loop_rhs_alpha_inv(t: float, alpha_inv: np.ndarray) -> np.ndarray:
    """
    双圈 RG 方程的右端项。
    
    变量: alpha_inv = [α₁⁻¹, α₂⁻¹, α₃⁻¹]
    自变量: t = ln μ
    
    方程:
    d(α_i⁻¹)/dt = b_i/(2π) + Σ_j b_ij/(8π² α_j⁻¹)
    
    注意: 这是耦合的 ODE 系统，因为双圈项包含其他耦合。
    """
    alpha = 1.0 / alpha_inv  # α_i = 1/α_i⁻¹
    d_inv_dt = B_1LOOP / (2 * np.pi) + np.dot(B_2LOOP, alpha) / (8 * np.pi**2)
    return d_inv_dt


def two_loop_rk4_step(alpha_inv: np.ndarray, t: float, dt: float) -> np.ndarray:
    """RK4 积分一步。"""
    k1 = dt * two_loop_rhs_alpha_inv(t, alpha_inv)
    k2 = dt * two_loop_rhs_alpha_inv(t + dt/2, alpha_inv + k1/2)
    k3 = dt * two_loop_rhs_alpha_inv(t + dt/2, alpha_inv + k2/2)
    k4 = dt * two_loop_rhs_alpha_inv(t + dt, alpha_inv + k3)
    return alpha_inv + (k1 + 2*k2 + 2*k3 + k4) / 6


def run_two_loop_forward(alphas_ignition: np.ndarray, mu_ign: np.ndarray, 
                         mu_mz: float, n_steps: int = 1000) -> np.ndarray:
    """
    双圈正向 RG 跑动（耦合 ODE 系统）。
    
    从 μ_ign 积分到 μ_mz，使用 RK4 方法。
    由于三个规范力的点火能标不同（μ_ign[i]），需要分段积分。
    """
    t_ign = np.log(mu_ign)
    t_mz = np.log(mu_mz)
    
    # 按点火能标排序
    sort_idx = np.argsort(mu_ign)  # 从高能标到低能标
    # 实际上从最大 μ_ign（最早点火）到 μ_mz
    
    # 方法：从最大 μ_ign 开始，逐步加入新点火的规范力
    # 三个规范力在 k=2,3,5 点火，μ_ign = [μ(5), μ(3), μ(2)]
    # μ(5) < μ(3) < μ(2): SU(3) 最先点火（k=2, 最高能标），U(1) 最后点火（k=5）
    # 实际上点火顺序：SU(3) @ k=2 → SU(2) @ k=3 → U(1) @ k=5
    
    # 点火能标从高到低: μ(2) > μ(3) > μ(5)
    # 即 SU(3) 在最高能标点火，U(1) 在最低能标点火
    
    # 简化：假设所有三个力同时从各自点火能标开始跑动
    # 实际上在点火之前，耦合常数为 0（规范力尚未出现）
    # 但 RG 方程在 α=0 处奇异，所以我们需要从点火时刻开始
    
    # 对于双圈耦合 ODE，我们同时积分三个耦合
    # 但在点火之前，对应耦合应该是 0 或未定义
    # 简化处理：所有三个力从 M_P 开始一起跑动
    # 这对应于"同时点火"的近似
    
    # 更精确的处理：从最高点火能标开始
    t_start = np.log(np.max(mu_ign))  # 从最高能标开始
    alpha_inv = np.array([1.0 / a for a in alphas_ignition])
    
    # 从 t_start 到 t_mz 积分
    t_span = t_mz - t_start
    dt = t_span / n_steps
    
    t = t_start
    for step in range(n_steps):
        alpha_inv = two_loop_rk4_step(alpha_inv, t, dt)
        t += dt
    
    return 1.0 / alpha_inv


def run_two_loop_sequential(alphas_ignition: np.ndarray, mu_ign: np.ndarray,
                            mu_mz: float, n_steps: int = 1000) -> np.ndarray:
    """
    双圈 RG 跑动 — 分段点火方案。
    
    物理图像：
    - k=2: SU(3) 点火（最高能标 μ(2) ≈ 5.5×10¹⁷ GeV）
    - k=3: SU(2) 点火（μ(3) ≈ 4.2×10¹⁶ GeV）
    - k=5: U(1) 点火（μ(5) ≈ 2.5×10¹⁴ GeV）
    
    在点火之前，对应规范力的耦合 = 0（或无穷大 α⁻¹）。
    在数值上，我们用非常大的 α⁻¹ 表示"未点火"状态。
    
    分段积分：
    段1: μ(2) → μ(3): 只有 SU(3) 活跃，单圈
    段2: μ(3) → μ(5): SU(3) + SU(2) 活跃，双圈耦合
    段3: μ(5) → μ(M_Z): 全部三个力活跃，双圈耦合
    """
    # 按 k 排序：k=2(SU3), k=3(SU2), k=5(U1)
    # μ_ign 按此顺序: [μ(5), μ(3), μ(2)] for [U1, SU2, SU3]
    # 能标从高到低: μ(2) > μ(3) > μ(5) > M_Z
    
    sort_by_mu = np.argsort(mu_ign)[::-1]  # 从高能标到低能标
    # sort_by_mu = [2, 1, 0] = [SU3, SU2, U1]
    
    # 初始化
    alpha_inv = np.ones(3) * 1e15  # 近似无穷大（耦合 = 0）
    
    # 段1: μ(2) → μ(3) — 只有 SU(3)
    mu_high = mu_ign[sort_by_mu[0]]  # μ(2)
    mu_mid = mu_ign[sort_by_mu[1]]   # μ(3)
    
    idx_high = sort_by_mu[0]  # SU(3) index
    alpha_inv[idx_high] = 1.0 / alphas_ignition[idx_high]
    
    # 对 SU(3) 单独跑单圈（从 μ(2) 到 μ(3)）
    t_span = np.log(mu_mid / mu_high)
    dt = t_span / n_steps
    t = 0.0
    for _ in range(n_steps):
        # 只有 SU(3) 活跃
        alpha = 1.0 / alpha_inv
        d_inv3 = B_1LOOP[idx_high] / (2 * np.pi) + B_2LOOP[idx_high, idx_high] * alpha[idx_high] / (8 * np.pi**2)
        alpha_inv[idx_high] += d_inv3 * dt
        t += dt
    
    # 段2: μ(3) → μ(5) — SU(3) + SU(2)
    mu_mid2 = mu_ign[sort_by_mu[2]]  # μ(5)
    idx_mid = sort_by_mu[1]  # SU(2) index
    alpha_inv[idx_mid] = 1.0 / alphas_ignition[idx_mid]
    
    active = [idx_high, idx_mid]  # [SU3, SU2]
    
    t_span = np.log(mu_mid2 / mu_mid)
    dt = t_span / n_steps
    for _ in range(n_steps):
        alpha = 1.0 / alpha_inv
        for i in active:
            d_inv = B_1LOOP[i] / (2 * np.pi)
            for j in active:
                d_inv += B_2LOOP[i, j] * alpha[j] / (8 * np.pi**2)
            alpha_inv[i] += d_inv * dt
        t += dt
    
    # 段3: μ(5) → M_Z — 全部三个力
    idx_low = sort_by_mu[2]  # U(1) index
    alpha_inv[idx_low] = 1.0 / alphas_ignition[idx_low]
    
    t_span = np.log(mu_mz / mu_mid2)
    dt = t_span / n_steps
    for _ in range(n_steps):
        alpha = 1.0 / alpha_inv
        for i in range(3):
            d_inv = B_1LOOP[i] / (2 * np.pi)
            for j in range(3):
                d_inv += B_2LOOP[i, j] * alpha[j] / (8 * np.pi**2)
            alpha_inv[i] += d_inv * dt
        t += dt
    
    return 1.0 / alpha_inv


# ============================================================
# 第3部分：同时点火方案（简化双圈）
# ============================================================

def run_two_loop_simultaneous(alphas_ignition: np.ndarray, mu_ign: np.ndarray,
                              mu_mz: float, n_steps: int = 2000) -> np.ndarray:
    """
    双圈 RG 跑动 — 同时点火方案（简化）。
    
    假设三个规范力从各自点火能标同时开始，都从最高点火能标积分。
    这在物理上是近似，但数学上更简单，且精度足够。
    """
    t_start = np.log(np.max(mu_ign))  # 从最高能标开始
    alpha_inv = np.array([1.0 / a for a in alphas_ignition])
    
    t_end = np.log(mu_mz)
    t_span = t_end - t_start
    dt = t_span / n_steps
    
    t = t_start
    for _ in range(n_steps):
        alpha_inv = two_loop_rk4_step(alpha_inv, t, dt)
        t += dt
    
    return 1.0 / alpha_inv


# ============================================================
# 第4部分：从 SM 反向确定点火耦合（双圈）
# ============================================================

def compute_ignition_two_loop(alphas_mz: np.ndarray, mu_ign: np.ndarray, 
                              mu_mz: float, n_steps: int = 2000) -> np.ndarray:
    """
    从 SM 实验值反向跑动（双圈），确定点火耦合。
    
    使用牛顿迭代法求解反向问题。
    """
    # 初始猜测：单圈反向
    alpha_ign_guess = np.zeros(3)
    for i in range(3):
        alpha_ign_guess[i] = run_one_loop(alphas_mz[i], mu_mz, mu_ign[i], B_1LOOP[i])
    
    # 牛顿迭代
    for iteration in range(10):
        # 正向跑动
        alphas_mz_pred = run_two_loop_simultaneous(alpha_ign_guess, mu_ign, mu_mz, n_steps)
        
        # 误差
        error = alphas_mz_pred - alphas_mz
        if np.max(np.abs(error)) < 1e-10:
            break
        
        # 数值梯度（简化：单圈梯度近似）
        gradient = np.zeros((3, 3))
        eps = 1e-6
        for i in range(3):
            alpha_ign_pert = alpha_ign_guess.copy()
            alpha_ign_pert[i] += eps
            alphas_mz_pert = run_two_loop_simultaneous(alpha_ign_pert, mu_ign, mu_mz, n_steps)
            gradient[:, i] = (alphas_mz_pert - alphas_mz_pred) / eps
        
        # 牛顿步
        try:
            delta = np.linalg.solve(gradient, -error)
            alpha_ign_guess += delta
        except np.linalg.LinAlgError:
            # 使用简化更新
            alpha_ign_guess -= error * 0.5
    
    return alpha_ign_guess


# ============================================================
# 第5部分：综合对比分析
# ============================================================

def compute_observables(alphas: np.ndarray) -> Dict:
    """从 (α₁, α₂, α₃) 计算可观测量。"""
    alpha_1, alpha_2, alpha_3 = alphas
    alpha_Y = (3.0 / 5) * alpha_1
    sin2_thetaW = alpha_Y / (alpha_2 + alpha_Y)
    alpha_em = alpha_2 * sin2_thetaW
    return {
        'alpha_3': alpha_3,
        'alpha_2': alpha_2,
        'alpha_1': alpha_1,
        'alpha_em': alpha_em,
        'alpha_em_inv': 1.0 / alpha_em,
        'sin2_thetaW': sin2_thetaW,
    }

def compute_errors(pred: Dict) -> Dict:
    errors = {}
    for key, exp_key in [('alpha_3', 'alpha_s_MZ'), 
                          ('alpha_em_inv', 'alpha_inv_MZ'),
                          ('sin2_thetaW', 'sin2_thetaW_MZ')]:
        errors[key] = (pred[key] - EXP[exp_key]) / EXP[exp_key] * 100
    errors['rms'] = np.sqrt(np.mean([v**2 for v in errors.values()]))
    return errors


def run_full_analysis():
    results = {}
    
    print("=" * 75)
    print("双圈 RG 修正：系统误差分析")
    print("=" * 75)
    
    # 能标
    mu_ign = np.array([energy_scale_dqpt(p) for p in GAUGE_PRIMES])  # [U1@5, SU2@3, SU3@2]
    mu_mz = energy_scale_dqpt(30)
    
    print(f"""
  【点火能标】
  SU(3) @ k=2: μ = {mu_ign[2]:.3e} GeV
  SU(2) @ k=3: μ = {mu_ign[1]:.3e} GeV
  U(1) @ k=5: μ = {mu_ign[0]:.3e} GeV
  M_Z  @ k=30: μ = {mu_mz:.3e} GeV
  """)
    
    # ================================================================
    # §1: 单圈基准
    # ================================================================
    print("=" * 75)
    print("§1: 单圈 RG 基准（使用经验 α₀ = 0.0204）")
    print("=" * 75)
    
    alpha_0 = 0.0204
    alphas_ign_1loop = np.array([alpha_0, alpha_0, alpha_0])
    alphas_mz_1loop = one_loop_forward(alphas_ign_1loop, mu_ign, mu_mz)
    obs_1loop = compute_observables(alphas_mz_1loop)
    err_1loop = compute_errors(obs_1loop)
    
    print(f"""
  点火耦合: α₀ = {alpha_0:.4f} (普适)
  
  M_Z 预测:
    α_s(M_Z)  = {obs_1loop['alpha_3']:.4f}  (实验: {EXP['alpha_s_MZ']:.4f})  [{err_1loop['alpha_3']:+.1f}%]
    α⁻¹(M_Z)  = {obs_1loop['alpha_em_inv']:.1f}  (实验: {EXP['alpha_inv_MZ']:.1f})  [{err_1loop['alpha_em_inv']:+.1f}%]
    sin²θ_W   = {obs_1loop['sin2_thetaW']:.5f}  (实验: {EXP['sin2_thetaW_MZ']:.5f})  [{err_1loop['sin2_thetaW']:+.1f}%]
  
  RMS 偏差: {err_1loop['rms']:.1f}%
  """)
    results['one_loop_benchmark'] = {
        'alpha_0': alpha_0,
        'alphas_ign': alphas_ign_1loop.tolist(),
        'alphas_mz': alphas_mz_1loop.tolist(),
        'observables': {k: float(v) if isinstance(v, (np.floating,)) else v for k, v in obs_1loop.items()},
        'errors': {k: float(v) for k, v in err_1loop.items()},
    }
    
    # ================================================================
    # §2: 双圈 RG（同时点火方案）
    # ================================================================
    print("=" * 75)
    print("§2: 双圈 RG 跑动（同时点火方案，α₀ = 0.0204）")
    print("=" * 75)
    
    alphas_mz_2loop = run_two_loop_simultaneous(alphas_ign_1loop, mu_ign, mu_mz)
    obs_2loop = compute_observables(alphas_mz_2loop)
    err_2loop = compute_errors(obs_2loop)
    
    print(f"""
  点火耦合: α₀ = {alpha_0:.4f} (普适)
  
  M_Z 预测 (双圈):
    α_s(M_Z)  = {obs_2loop['alpha_3']:.4f}  (实验: {EXP['alpha_s_MZ']:.4f})  [{err_2loop['alpha_3']:+.1f}%]
    α⁻¹(M_Z)  = {obs_2loop['alpha_em_inv']:.1f}  (实验: {EXP['alpha_inv_MZ']:.1f})  [{err_2loop['alpha_em_inv']:+.1f}%]
    sin²θ_W   = {obs_2loop['sin2_thetaW']:.5f}  (实验: {EXP['sin2_thetaW_MZ']:.5f})  [{err_2loop['sin2_thetaW']:+.1f}%]
  
  RMS 偏差: {err_2loop['rms']:.1f}%
  
  单圈 → 双圈变化:
    Δα_s     = {obs_2loop['alpha_3'] - obs_1loop['alpha_3']:+.4f}  ({abs(obs_2loop['alpha_3'] - obs_1loop['alpha_3'])/obs_1loop['alpha_3']*100:.1f}%)
    Δα⁻¹     = {obs_2loop['alpha_em_inv'] - obs_1loop['alpha_em_inv']:+.1f}  ({abs(obs_2loop['alpha_em_inv'] - obs_1loop['alpha_em_inv'])/obs_1loop['alpha_em_inv']*100:.1f}%)
    Δsin²θ_W = {obs_2loop['sin2_thetaW'] - obs_1loop['sin2_thetaW']:+.5f}  ({abs(obs_2loop['sin2_thetaW'] - obs_1loop['sin2_thetaW'])/obs_1loop['sin2_thetaW']*100:.1f}%)
  """)
    results['two_loop_simultaneous'] = {
        'alpha_0': alpha_0,
        'alphas_ign': alphas_ign_1loop.tolist(),
        'alphas_mz': alphas_mz_2loop.tolist(),
        'observables': {k: float(v) if isinstance(v, (np.floating,)) else v for k, v in obs_2loop.items()},
        'errors': {k: float(v) for k, v in err_2loop.items()},
        'delta_from_1loop': {
            'alpha_3': float(obs_2loop['alpha_3'] - obs_1loop['alpha_3']),
            'alpha_em_inv': float(obs_2loop['alpha_em_inv'] - obs_1loop['alpha_em_inv']),
            'sin2_thetaW': float(obs_2loop['sin2_thetaW'] - obs_1loop['sin2_thetaW']),
        }
    }
    
    # ================================================================
    # §3: 双圈 RG（分段点火方案）
    # ================================================================
    print("=" * 75)
    print("§3: 双圈 RG 跑动（分段点火方案，α₀ = 0.0204）")
    print("=" * 75)
    
    alphas_mz_2loop_seq = run_two_loop_sequential(alphas_ign_1loop, mu_ign, mu_mz)
    obs_2loop_seq = compute_observables(alphas_mz_2loop_seq)
    err_2loop_seq = compute_errors(obs_2loop_seq)
    
    print(f"""
  点火耦合: α₀ = {alpha_0:.4f} (普适)
  
  M_Z 预测 (双圈分段):
    α_s(M_Z)  = {obs_2loop_seq['alpha_3']:.4f}  (实验: {EXP['alpha_s_MZ']:.4f})  [{err_2loop_seq['alpha_3']:+.1f}%]
    α⁻¹(M_Z)  = {obs_2loop_seq['alpha_em_inv']:.1f}  (实验: {EXP['alpha_inv_MZ']:.1f})  [{err_2loop_seq['alpha_em_inv']:+.1f}%]
    sin²θ_W   = {obs_2loop_seq['sin2_thetaW']:.5f}  (实验: {EXP['sin2_thetaW_MZ']:.5f})  [{err_2loop_seq['sin2_thetaW']:+.1f}%]
  
  RMS 偏差: {err_2loop_seq['rms']:.1f}%
  
  同时 vs 分段差异:
    Δα_s     = {obs_2loop_seq['alpha_3'] - obs_2loop['alpha_3']:+.6f}
    Δα⁻¹     = {obs_2loop_seq['alpha_em_inv'] - obs_2loop['alpha_em_inv']:+.3f}
    Δsin²θ_W = {obs_2loop_seq['sin2_thetaW'] - obs_2loop['sin2_thetaW']:+.6f}
  """)
    results['two_loop_sequential'] = {
        'alpha_0': alpha_0,
        'alphas_mz': alphas_mz_2loop_seq.tolist(),
        'observables': {k: float(v) if isinstance(v, (np.floating,)) else v for k, v in obs_2loop_seq.items()},
        'errors': {k: float(v) for k, v in err_2loop_seq.items()},
    }
    
    # ================================================================
    # §4: 从 SM 反向确定点火耦合（双圈）
    # ================================================================
    print("=" * 75)
    print("§4: 双圈反向 — 从 SM 实验值确定点火耦合")
    print("=" * 75)
    
    alphas_mz_exp = np.array([EXP['alpha_1_MZ'], EXP['alpha_2_MZ'], EXP['alpha_3_MZ']])
    
    # 单圈反向
    alphas_ign_1loop_rev = np.zeros(3)
    for i in range(3):
        alphas_ign_1loop_rev[i] = run_one_loop(alphas_mz_exp[i], mu_mz, mu_ign[i], B_1LOOP[i])
    
    # 双圈反向（牛顿迭代）
    alphas_ign_2loop_rev = compute_ignition_two_loop(alphas_mz_exp, mu_ign, mu_mz)
    
    print(f"""
  【单圈反向点火耦合】
    U(1)  α_ign = {alphas_ign_1loop_rev[0]:.6f}
    SU(2) α_ign = {alphas_ign_1loop_rev[1]:.6f}
    SU(3) α_ign = {alphas_ign_1loop_rev[2]:.6f}
    平均值 = {np.mean(alphas_ign_1loop_rev):.6f}
    最大偏差 = {max(abs(a - np.mean(alphas_ign_1loop_rev)) for a in alphas_ign_1loop_rev)/np.mean(alphas_ign_1loop_rev)*100:.1f}%
  
  【双圈反向点火耦合】
    U(1)  α_ign = {alphas_ign_2loop_rev[0]:.6f}
    SU(2) α_ign = {alphas_ign_2loop_rev[1]:.6f}
    SU(3) α_ign = {alphas_ign_2loop_rev[2]:.6f}
    平均值 = {np.mean(alphas_ign_2loop_rev):.6f}
    最大偏差 = {max(abs(a - np.mean(alphas_ign_2loop_rev)) for a in alphas_ign_2loop_rev)/np.mean(alphas_ign_2loop_rev)*100:.1f}%
  
  【单圈 vs 双圈差异】
    Δα_ign(U1)  = {alphas_ign_2loop_rev[0] - alphas_ign_1loop_rev[0]:+.6f} ({(alphas_ign_2loop_rev[0] - alphas_ign_1loop_rev[0])/alphas_ign_1loop_rev[0]*100:+.1f}%)
    Δα_ign(SU2) = {alphas_ign_2loop_rev[1] - alphas_ign_1loop_rev[1]:+.6f} ({(alphas_ign_2loop_rev[1] - alphas_ign_1loop_rev[1])/alphas_ign_1loop_rev[1]*100:+.1f}%)
    Δα_ign(SU3) = {alphas_ign_2loop_rev[2] - alphas_ign_1loop_rev[2]:+.6f} ({(alphas_ign_2loop_rev[2] - alphas_ign_1loop_rev[2])/alphas_ign_1loop_rev[2]*100:+.1f}%)
  """)
    results['ignition_reverse'] = {
        'one_loop': alphas_ign_1loop_rev.tolist(),
        'two_loop': alphas_ign_2loop_rev.tolist(),
        'one_loop_mean': float(np.mean(alphas_ign_1loop_rev)),
        'two_loop_mean': float(np.mean(alphas_ign_2loop_rev)),
        'one_loop_max_deviation': float(max(abs(a - np.mean(alphas_ign_1loop_rev)) for a in alphas_ign_1loop_rev) / np.mean(alphas_ign_1loop_rev) * 100),
        'two_loop_max_deviation': float(max(abs(a - np.mean(alphas_ign_2loop_rev)) for a in alphas_ign_2loop_rev) / np.mean(alphas_ign_2loop_rev) * 100),
    }
    
    # ================================================================
    # §5: 双圈 + 1/(4π²) 自然尺度
    # ================================================================
    print("=" * 75)
    print("§5: 双圈 RG + 自然尺度 α₀ = 1/(4π²) = 0.02533")
    print("=" * 75)
    
    alpha_0_natural = 1.0 / (4 * np.pi**2)
    alphas_ign_natural = np.array([alpha_0_natural, alpha_0_natural, alpha_0_natural])
    
    alphas_mz_2loop_nat = run_two_loop_simultaneous(alphas_ign_natural, mu_ign, mu_mz)
    obs_2loop_nat = compute_observables(alphas_mz_2loop_nat)
    err_2loop_nat = compute_errors(obs_2loop_nat)
    
    # 单圈版本用于对比
    alphas_mz_1loop_nat = one_loop_forward(alphas_ign_natural, mu_ign, mu_mz)
    obs_1loop_nat = compute_observables(alphas_mz_1loop_nat)
    err_1loop_nat = compute_errors(obs_1loop_nat)
    
    print(f"""
  点火耦合: α₀ = 1/(4π²) = {alpha_0_natural:.6f} (纯理论)
  
  ┌──────────────┬───────────────────────┬───────────────────────┐
  │   可观测量    │   单圈 (α₀=1/4π²)     │   双圈 (α₀=1/4π²)     │
  ├──────────────┼───────────────────────┼───────────────────────┤
  │ α_s(M_Z)     │ {obs_1loop_nat['alpha_3']:.4f} [{err_1loop_nat['alpha_3']:+.1f}%]        │ {obs_2loop_nat['alpha_3']:.4f} [{err_2loop_nat['alpha_3']:+.1f}%]        │
  │ α⁻¹(M_Z)     │ {obs_1loop_nat['alpha_em_inv']:.1f} [{err_1loop_nat['alpha_em_inv']:+.1f}%]       │ {obs_2loop_nat['alpha_em_inv']:.1f} [{err_2loop_nat['alpha_em_inv']:+.1f}%]       │
  │ sin²θ_W      │ {obs_1loop_nat['sin2_thetaW']:.5f} [{err_1loop_nat['sin2_thetaW']:+.1f}%]        │ {obs_2loop_nat['sin2_thetaW']:.5f} [{err_2loop_nat['sin2_thetaW']:+.1f}%]        │
  │ RMS          │ {err_1loop_nat['rms']:.1f}%                  │ {err_2loop_nat['rms']:.1f}%                  │
  └──────────────┴───────────────────────┴───────────────────────┘
  """)
    results['natural_scale'] = {
        'alpha_0': alpha_0_natural,
        'one_loop': {
            'alphas_mz': alphas_mz_1loop_nat.tolist(),
            'observables': {k: float(v) if isinstance(v, (np.floating,)) else v for k, v in obs_1loop_nat.items()},
            'errors': {k: float(v) for k, v in err_1loop_nat.items()},
        },
        'two_loop': {
            'alphas_mz': alphas_mz_2loop_nat.tolist(),
            'observables': {k: float(v) if isinstance(v, (np.floating,)) else v for k, v in obs_2loop_nat.items()},
            'errors': {k: float(v) for k, v in err_2loop_nat.items()},
        },
    }
    
    # ================================================================
    # §6: 双圈效应分解
    # ================================================================
    print("=" * 75)
    print("§6: 双圈效应分解 — 各双圈项的贡献")
    print("=" * 75)
    
    # 分析双圈矩阵各元素的贡献
    alpha_ref = np.array([EXP['alpha_1_MZ'], EXP['alpha_2_MZ'], EXP['alpha_3_MZ']])
    
    print(f"""
  【双圈贡献矩阵分析 (在 M_Z 处)】
  
  b_ij α_j / (8π²) 对各规范力 β 函数的贡献:
  
  对 U(1) 的双圈贡献:
    b_11 × α₁ = {B_2LOOP[0,0]:.2f} × {alpha_ref[0]:.4f} = {B_2LOOP[0,0] * alpha_ref[0]:.4f} → {B_2LOOP[0,0] * alpha_ref[0] / (8*np.pi**2):.6f} (in dα⁻¹/dt)
    b_12 × α₂ = {B_2LOOP[0,1]:.2f} × {alpha_ref[1]:.4f} = {B_2LOOP[0,1] * alpha_ref[1]:.4f} → {B_2LOOP[0,1] * alpha_ref[1] / (8*np.pi**2):.6f}
    b_13 × α₃ = {B_2LOOP[0,2]:.2f} × {alpha_ref[2]:.4f} = {B_2LOOP[0,2] * alpha_ref[2]:.4f} → {B_2LOOP[0,2] * alpha_ref[2] / (8*np.pi**2):.6f}
    总双圈/U(1) = {(B_2LOOP[0,0]*alpha_ref[0] + B_2LOOP[0,1]*alpha_ref[1] + B_2LOOP[0,2]*alpha_ref[2])/(8*np.pi**2):.6f}
    单圈/U(1)   = {B_1LOOP[0]/(2*np.pi):.6f}
    双圈/单圈   = {(B_2LOOP[0,0]*alpha_ref[0] + B_2LOOP[0,1]*alpha_ref[1] + B_2LOOP[0,2]*alpha_ref[2])/(8*np.pi**2)/(B_1LOOP[0]/(2*np.pi))*100:.1f}%
  
  对 SU(2) 的双圈贡献:
    b_21 × α₁ = {B_2LOOP[1,0]:.2f} × {alpha_ref[0]:.4f} = {B_2LOOP[1,0] * alpha_ref[0]:.4f} → {B_2LOOP[1,0] * alpha_ref[0] / (8*np.pi**2):.6f}
    b_22 × α₂ = {B_2LOOP[1,1]:.2f} × {alpha_ref[1]:.4f} = {B_2LOOP[1,1] * alpha_ref[1]:.4f} → {B_2LOOP[1,1] * alpha_ref[1] / (8*np.pi**2):.6f}
    b_23 × α₃ = {B_2LOOP[1,2]:.2f} × {alpha_ref[2]:.4f} = {B_2LOOP[1,2] * alpha_ref[2]:.4f} → {B_2LOOP[1,2] * alpha_ref[2] / (8*np.pi**2):.6f}
    总双圈/SU(2) = {(B_2LOOP[1,0]*alpha_ref[0] + B_2LOOP[1,1]*alpha_ref[1] + B_2LOOP[1,2]*alpha_ref[2])/(8*np.pi**2):.6f}
    单圈/SU(2)   = {B_1LOOP[1]/(2*np.pi):.6f}
    双圈/单圈   = {(B_2LOOP[1,0]*alpha_ref[0] + B_2LOOP[1,1]*alpha_ref[1] + B_2LOOP[1,2]*alpha_ref[2])/(8*np.pi**2)/(B_1LOOP[1]/(2*np.pi))*100:.1f}%
  
  对 SU(3) 的双圈贡献:
    b_31 × α₁ = {B_2LOOP[2,0]:.2f} × {alpha_ref[0]:.4f} = {B_2LOOP[2,0] * alpha_ref[0]:.4f} → {B_2LOOP[2,0] * alpha_ref[0] / (8*np.pi**2):.6f}
    b_32 × α₂ = {B_2LOOP[2,1]:.2f} × {alpha_ref[1]:.4f} = {B_2LOOP[2,1] * alpha_ref[1]:.4f} → {B_2LOOP[2,1] * alpha_ref[1] / (8*np.pi**2):.6f}
    b_33 × α₃ = {B_2LOOP[2,2]:.2f} × {alpha_ref[2]:.4f} = {B_2LOOP[2,2] * alpha_ref[2]:.4f} → {B_2LOOP[2,2] * alpha_ref[2] / (8*np.pi**2):.6f}
    总双圈/SU(3) = {(B_2LOOP[2,0]*alpha_ref[0] + B_2LOOP[2,1]*alpha_ref[1] + B_2LOOP[2,2]*alpha_ref[2])/(8*np.pi**2):.6f}
    单圈/SU(3)   = {B_1LOOP[2]/(2*np.pi):.6f}
    双圈/单圈   = {(B_2LOOP[2,0]*alpha_ref[0] + B_2LOOP[2,1]*alpha_ref[1] + B_2LOOP[2,2]*alpha_ref[2])/(8*np.pi**2)/(B_1LOOP[2]/(2*np.pi))*100:.1f}%
  """)
    
    # ================================================================
    # §7: 综合评估
    # ================================================================
    print("=" * 75)
    print("§7: 综合评估 — 双圈修正的意义")
    print("=" * 75)
    
    # 对比所有方案
    all_schemes = [
        ('单圈 (经验 α₀)', err_1loop['rms']),
        ('双圈同时 (经验 α₀)', err_2loop['rms']),
        ('双圈分段 (经验 α₀)', err_2loop_seq['rms']),
        ('单圈 (自然 α₀=1/4π²)', err_1loop_nat['rms']),
        ('双圈同时 (自然 α₀=1/4π²)', err_2loop_nat['rms']),
    ]
    
    print(f"\n  {'方案':<35s}  {'RMS 偏差':>10s}")
    print(f"  {'-'*35}  {'-'*10}")
    for name, rms in all_schemes:
        marker = " ← 最佳" if rms == min(rms for _, rms in all_schemes) else ""
        print(f"  {name:<35s}  {rms:>8.1f}%{marker}")
    
    # 双圈修正的定量影响
    delta_rms = err_2loop['rms'] - err_1loop['rms']
    delta_rms_nat = err_2loop_nat['rms'] - err_1loop_nat['rms']
    
    print(f"""
  【关键结论】
  
  1. 双圈修正对 RMS 偏差的影响:
     - 经验 α₀:  RMS 变化 {delta_rms:+.1f}% (单圈 {err_1loop['rms']:.1f}% → 双圈 {err_2loop['rms']:.1f}%)
     - 自然 α₀:  RMS 变化 {delta_rms_nat:+.1f}% (单圈 {err_1loop_nat['rms']:.1f}% → 双圈 {err_2loop_nat['rms']:.1f}%)
  
  2. 双圈修正对点火耦合的影响:
     - 单圈反向: ᾱ_ign = {np.mean(alphas_ign_1loop_rev):.6f}
     - 双圈反向: ᾱ_ign = {np.mean(alphas_ign_2loop_rev):.6f}
     - 差异: {abs(np.mean(alphas_ign_2loop_rev) - np.mean(alphas_ign_1loop_rev))/np.mean(alphas_ign_1loop_rev)*100:.1f}%
  
  3. 双圈修正能否解释 α₀ 的 24% 偏差?
     - 自然尺度 α₀ = 1/(4π²) = {alpha_0_natural:.6f}
     - 双圈反向 α₀ = {np.mean(alphas_ign_2loop_rev):.6f}
     - 剩余偏差: {abs(np.mean(alphas_ign_2loop_rev) - alpha_0_natural)/alpha_0_natural*100:.1f}%
  
  4. 物理意义:
     - 双圈修正是微扰展开的次领头阶，效应量级 ~O(α/(4π)) ~ 0.1-1%
     - 不能解释 24% 量级的偏差
     - 点火耦合 α₀ 的精确值问题需要超越微扰展开的新物理
     - 双圈修正主要改善的是 RG 跑动精度，而非边界条件
  """)
    
    results['summary'] = {
        'schemes': [{'name': name, 'rms': float(rms)} for name, rms in all_schemes],
        'delta_rms_empirical': float(delta_rms),
        'delta_rms_natural': float(delta_rms_nat),
        'ignition_1loop_mean': float(np.mean(alphas_ign_1loop_rev)),
        'ignition_2loop_mean': float(np.mean(alphas_ign_2loop_rev)),
        'remaining_deviation_percent': float(abs(np.mean(alphas_ign_2loop_rev) - alpha_0_natural) / alpha_0_natural * 100),
    }
    
    return results


def save_results(results: Dict, filename: str = None):
    if filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, '06-双圈RG修正_结果.json')
    
    def convert(obj):
        if isinstance(obj, dict):
            return {str(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return bool(obj)
        elif callable(obj):
            return str(obj)
        return obj
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convert(results), f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存到: {filename}")


if __name__ == '__main__':
    results = run_full_analysis()
    save_results(results)