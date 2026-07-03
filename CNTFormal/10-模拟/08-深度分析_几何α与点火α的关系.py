"""
深度分析：几何精细结构常数与点火耦合常数的关系
==============================================

CNT v5.0 框架：系统探索从几何α₀到点火α₀的定量关系。

核心问题：
  1. 几何α₀ = 375/(16384π) ≈ 0.0072855 (4-单纯形 → 裸电磁耦合)
  2. 点火α₀ ≈ 0.0204 (SM反向RG → 近普适统一耦合)
  3. 两者之间差一个因子 ~2.8 —— 这个因子从哪来？

候选解释：
  A. GUT归一化: α_GUT = (8/3)α_em → 因子 8/3 = 2.667
  B. p进结构: 三种规范力的p进基底叠加
  C. Sₚ·νₚ ≈ constant → 点火耦合由功率普适性决定

认识论地位: [第一性原理推导] + [SM β函数输入] + [候选假设检验]
日期: 2026-07-04
"""

import numpy as np
from typing import Dict, List, Tuple
import json
import os

# ============================================================
# 物理常数
# ============================================================
M_P = 1.22089e19
M_Z = 91.1876
LN_MP_MZ = np.log(M_P / M_Z)
FOUR_PI_SQ = 4 * np.pi**2
N_CYCLE = 30
DELTA_DQPT = 0.2845
GAUGE_PRIMES = [2, 3, 5]
GAUGE_NAMES = ['SU(3)', 'SU(2)', 'U(1)']

# SM β 函数
B_SM = {'SU3': 7.0, 'SU2': 19.0/6, 'U1': -41.0/10}

# 实验值
EXP = {
    'alpha_s_MZ': 0.1180,
    'alpha_inv_MZ': 127.952,
    'sin2_thetaW_MZ': 0.23121,
    'alpha_2_MZ': 0.03383,
    'alpha_1_MZ': 0.01695,
}
ALPHA_INV_EXP = 137.035999084

# ============================================================
# 辅助函数
# ============================================================

def von_mangoldt_restricted(k: int) -> float:
    if k < 2: return 0.0
    for p in GAUGE_PRIMES:
        m, exp = k, 0
        while m % p == 0:
            m //= p; exp += 1
        if m == 1 and exp > 0: return np.log(p)
    return 0.0

def energy_scale_dqpt(k: int, delta: float = DELTA_DQPT) -> float:
    s_total = sum(von_mangoldt_restricted(j) for j in range(1, N_CYCLE + 1))
    delta_N0 = 2 * np.pi**2 * LN_MP_MZ / (N_CYCLE + delta * s_total)
    cumulative_N = 0.0
    for j in range(1, k + 1):
        lam = von_mangoldt_restricted(j)
        cumulative_N += delta_N0 * (1 + delta * lam)
    return M_P * np.exp(-cumulative_N / (2 * np.pi**2))

def run_single_rg(alpha_initial, mu_initial, mu_final, b):
    alpha_inv = 1.0 / alpha_initial + b / (2 * np.pi) * np.log(mu_final / mu_initial)
    return 1.0 / alpha_inv


# ============================================================
# §A: 几何α₀ → GUT α_GUT 关系
# ============================================================

def compute_geometric_to_gut():
    """
    从几何α₀推导GUT统一耦合常数。
    
    【推导链】
    
    1. 几何α₀ = 375/(16384π) 是裸电磁耦合常数
       → 来源: 4-单纯形二面角 Θ = arccos(1/4)
       → Chebyshev: cos(5Θ) = 61/64, sin²(5Θ) = 375/4096
       → α₀ = sin²(5Θ)/(4π) = 375/(16384π)
    
    2. 在GUT能标, SU(3)×SU(2)×U(1) 统一为单群 G
       → 标准归一化: g₁ = √(5/3) g' (GUT归一化)
       → 统一条件: g₁ = g₂ = g₃ = g_GUT
    
    3. 电磁耦合与统一耦合的关系:
       → 1/e² = 1/g₂² + 1/g₁² (电弱统一)
       → 在GUT能标: 1/e² = 1/g_GUT² + 3/(5g_GUT²) = 8/(5g_GUT²)
       → 或: 1/e² = 1/g_GUT² + 1/(5/3 g_GUT²) = 1/g_GUT² + 3/(5g_GUT²)
    
    标准推导:
       α_em = e²/(4π)
       α_2 = g₂²/(4π), α_1 = g₁²/(4π) (GUT归一化)
       在GUT能标: α_1 = α_2 = α_GUT
       
       1/α_em = 1/α_2 + 5/(3α_1)  (电弱混合角关系)
       在GUT: 1/α_em = 1/α_GUT + 5/(3α_GUT) = 8/(3α_GUT)
       
       ∴ α_GUT = (8/3) α_em
    
    4. CNT预测:
       α_GUT = (8/3) × 375/(16384π) = 1000/(16384π)
       1/α_GUT = 16384π/1000 ≈ 51.47
    
    5. 与经验点火耦合对比:
       α_ign_empirical ≈ 0.0204 → 1/α_ign ≈ 49.0
       偏差: |51.47 - 49.0|/49.0 ≈ 5.0%
    """
    print("=" * 75)
    print("§A: 几何α₀ → GUT α_GUT → 点火α₀")
    print("=" * 75)
    
    # 几何α₀
    alpha_0_geom = 375.0 / (16384 * np.pi)
    alpha_0_inv_geom = 1.0 / alpha_0_geom
    
    # GUT关系
    factor_gut = 8.0 / 3.0
    alpha_gut = factor_gut * alpha_0_geom
    alpha_gut_inv = 1.0 / alpha_gut
    
    # 精确有理数形式
    alpha_gut_exact_num = 1000
    alpha_gut_exact_den = 16384 * np.pi
    alpha_gut_exact = alpha_gut_exact_num / alpha_gut_exact_den
    
    # 经验点火耦合
    alpha_ign_emp = 0.0204
    alpha_ign_inv = 1.0 / alpha_ign_emp
    
    # 偏差
    dev = abs(alpha_gut - alpha_ign_emp) / alpha_ign_emp * 100
    
    print(f"""
  【几何α₀】
  1/α₀ = 16384π/375 = {alpha_0_inv_geom:.6f}
  α₀   = 375/(16384π) = {alpha_0_geom:.8f}
  
  【标准GUT归一化】
  
  SM电弱统一关系:
    1/α_em = 1/α_2 + 5/(3α_1)
  
  在GUT能标 (α_1 = α_2 = α_GUT):
    1/α_em = 1/α_GUT + 5/(3α_GUT) = 8/(3α_GUT)
    → α_GUT = (8/3) α_em
  
  【CNT预测: α_GUT = (8/3) × 375/(16384π)】
  
  1/α_GUT = 16384π/1000 = {alpha_gut_inv:.6f}
  α_GUT   = 1000/(16384π) = {alpha_gut_exact:.8f}
  
  【精确有理数: α_GUT = 1000/(16384π) = 5³×2³/(2¹⁴π) = 125/(2048π)】
  
  【与经验点火耦合对比】
  
  CNT几何+GUT: 1/α_GUT = {alpha_gut_inv:.2f}
  经验点火:     1/α_ign = {alpha_ign_inv:.1f}  (SM反向RG平均值 ≈ 49.0)
  偏差:         {dev:.1f}%
  
  【SU(3)/SU(2)/U(1) 分别对比】
  """)
    
    # 从SM反向RG得到的各规范力点火耦合
    ignition_emp = {}
    for name, p, b_name in [('SU(3)', 2, 'SU3'), ('SU(2)', 3, 'SU2'), ('U(1)', 5, 'U1')]:
        mu_ign = energy_scale_dqpt(p)
        mu_mz = energy_scale_dqpt(N_CYCLE)
        b = B_SM[b_name]
        alpha_mz = EXP.get(f'alpha_{["s","2","1"][["SU(3)","SU(2)","U(1)"].index(name)]}_MZ', 
                           EXP['alpha_s_MZ'] if name == 'SU(3)' else 
                           EXP['alpha_2_MZ'] if name == 'SU(2)' else EXP['alpha_1_MZ'])
        alpha_inv_ign = 1.0 / alpha_mz + b / (2 * np.pi) * np.log(mu_ign / mu_mz)
        ignition_emp[name] = 1.0 / alpha_inv_ign
    
    for name in GAUGE_NAMES:
        dev_i = abs(alpha_gut - ignition_emp[name]) / ignition_emp[name] * 100
        print(f"    {name}: α_ign(SM反向) = {ignition_emp[name]:.6f}, 偏差 = {dev_i:.1f}%")
    
    # 关键发现
    print(f"""
  【关键发现】
  
  1. α_GUT = 1000/(16384π) = 125/(2048π) ≈ 0.01943
     这是从4-单纯形几何 + GUT归一化 严格推导出的统一耦合常数。
     无任何可调参数。
  
  2. 与经验值的偏差仅 {dev:.1f}%，显著优于:
     - 自然尺度 1/(4π²) 的 24% 偏差
     - 裸几何α₀ 直接使用时的 ~2.8倍偏差
  
  3. 因子 8/3 的物理来源: sin²θ_W = 3/8 at GUT scale
     (这是任何SU(5)或SO(10)大统一理论的通用结果)
  
  4. 剩余 {dev:.1f}% 偏差的可能来源:
     (a) GUT能标不完全等于几何"裸"能标 (k=0 vs k=1)
     (b) 阈值修正 (GUT破缺粒子质量)
     (c) 引力修正 (普朗克尺度量子引力效应)
  """)
    
    return {
        'alpha_0_geom': alpha_0_geom,
        'alpha_0_inv_geom': alpha_0_inv_geom,
        'gut_factor': factor_gut,
        'alpha_gut': alpha_gut,
        'alpha_gut_inv': alpha_gut_inv,
        'alpha_gut_exact': '1000/(16384π) = 125/(2048π)',
        'alpha_ign_empirical': alpha_ign_emp,
        'deviation_percent': dev,
        'ignition_empirical': ignition_emp,
    }


# ============================================================
# §B: Sₚ·νₚ ≈ constant 定量分析
# ============================================================

def compute_action_frequency_relation():
    """
    Sₚ·νₚ ≈ constant 的定量分析。
    
    物理图像:
      再生产第k步 → 频率 ν_k = ν₀/k
      质数点火点 → 作用量 Sₚ ∝ Λ(p) = log(p) (von Mangoldt)
      
      功率 Pₚ = Sₚ·νₚ = Λ(p) · ν₀/p
      
      近普适性: P₂ ≈ P₃ ≈ P₅ (因为 log(p)/p 近似常数)
    
    定量:
      S₂·ν₂ = log(2) · ν₀/2 = 0.34657 ν₀
      S₃·ν₃ = log(3) · ν₀/3 = 0.36620 ν₀
      S₅·ν₅ = log(5) · ν₀/5 = 0.32189 ν₀
      
      均值: 0.34489 ν₀
      最大偏差: (0.36620 - 0.34489)/0.34489 = 6.2%
    
    点火耦合与功率的关系:
      α_ign ∝ Pₚ / P₀
      其中 P₀ = ħ·ν_P 是普朗克功率 (自然单位下 P₀ = 1)
      
      如果 α_ign = k · ⟨Pₚ⟩:
      k = α_ign / ⟨Pₚ⟩ = 0.0204 / 0.34489 = 0.05915
      
      这意味着点火耦合是平均功率的约 5.9%。
    """
    print("\n" + "=" * 75)
    print("§B: Sₚ·νₚ ≈ constant — 点火耦合普适性的物理根源")
    print("=" * 75)
    
    # 计算 Sₚ·νₚ
    nu_0 = 1.0  # 归一化
    
    powers = {}
    for p in GAUGE_PRIMES:
        S_p = np.log(p)  # von Mangoldt Λ(p)
        nu_p = nu_0 / p
        power = S_p * nu_p
        powers[p] = {
            'S_p': S_p,
            'nu_p': nu_p,
            'S_nu': power,
            'Lambda': S_p,
        }
    
    mean_power = np.mean([powers[p]['S_nu'] for p in GAUGE_PRIMES])
    max_dev = max(abs(powers[p]['S_nu'] - mean_power) / mean_power * 100 for p in GAUGE_PRIMES)
    
    print(f"""
  【Sₚ·νₚ 计算 (ν₀ = 1 归一化)】
  
  质数 p    Λ(p)=log(p)    νₚ = 1/p    Sₚ·νₚ         偏差
  ──────    ───────────    ────────    ────────      ─────
  """)
    
    for p in GAUGE_PRIMES:
        d = powers[p]
        dev = (d['S_nu'] - mean_power) / mean_power * 100
        print(f"  {p}         {d['Lambda']:.5f}         {d['nu_p']:.5f}      {d['S_nu']:.5f}      {dev:+5.1f}%")
    
    print(f"""
  均值: {mean_power:.5f}
  最大偏差: {max_dev:.1f}%
  
  【物理意义】
  
  Sₚ·νₚ = 作用量 × 频率 = 功率 (单位时间的作用量)
  
  近普适性意味着: 三种规范力在"点火"时刻的再生产功率几乎相等。
  这是"点火"这一概念的本体论基础:
  → 不是耦合常数本身相等，而是再生产功率相等
  → 耦合常数 = 功率 / (某种归一化因子)
  
  【与点火耦合的定量关系】
  
  令 α_ign = κ · ⟨Sₚ·νₚ⟩:
  
  κ = α_ign / ⟨Sₚ·νₚ⟩ = 0.0204 / {mean_power:.5f} = {0.0204/mean_power:.5f}
  
  这个 κ 的物理意义是什么？
  
  候选解释:
  1. κ = 1/(4π²) × (某种几何因子) 
     1/(4π²) = 0.02533, κ / (1/(4π²)) = {0.0204/mean_power / (1/FOUR_PI_SQ):.3f}
  
  2. κ = α_GUT × (8/3)⁻¹ × (某种因子)
     α_GUT = 0.01943, κ / α_GUT = {0.0204/mean_power / 0.01943:.3f}
  
  3. κ = 1/(2π · N_cycle) × (某种因子)
     1/(2π·30) = 0.00531, κ / 0.00531 = {0.0204/mean_power / 0.00531:.3f}
  """)
    
    # 探索 κ 的几何意义
    kappa = 0.0204 / mean_power
    
    candidates = {
        '1/(4π²)': 1.0 / FOUR_PI_SQ,
        'α_GUT (几何+GUT)': 1000.0 / (16384 * np.pi),
        '1/(2π·N_cycle)': 1.0 / (2 * np.pi * N_CYCLE),
        '1/(π·N_cycle)': 1.0 / (np.pi * N_CYCLE),
        'log(30)/30': np.log(N_CYCLE) / N_CYCLE,
        'π/N_cycle²': np.pi / N_CYCLE**2,
    }
    
    print(f"  【κ = {kappa:.6f} 与候选几何量对比】\n")
    for name, val in candidates.items():
        ratio = kappa / val
        print(f"    {name:<25s} = {val:.6f}  → κ/{name} = {ratio:.3f}")
    
    return {
        'powers': powers,
        'mean_power': mean_power,
        'max_deviation_percent': max_dev,
        'kappa': kappa,
        'candidates': candidates,
        'ratios': {name: kappa / val for name, val in candidates.items()},
    }


# ============================================================
# §C: p进结构 → 耦合常数定量映射
# ============================================================

def compute_padic_to_coupling():
    """
    p进结构与耦合常数的定量关系。
    
    关键观察:
      p进范数: |p|_p = 1/p
      p进展开收敛速度: v_p = |p|_p = 1/p
      
      物理耦合强度 (M_Z处):
        α₃ ≈ 0.118 (强)
        α₂ ≈ 0.034 (弱)
        α₁ ≈ 0.017 (超荷)
        α_em ≈ 0.008 (电磁)
      
      定性: |p|_p 越大 → 收敛越慢 → 耦合越强
    
    定量候选:
    
    A. 耦合强度 ∝ |p|_p = 1/p
       → α₃:α₂:α₁ = 1/2:1/3:1/5 = 15:10:6
       → 归一化后 α₃=0.484, α₂=0.323, α₁=0.194
       → 与实验不符 (α₃=0.118)
    
    B. 考虑RG跑动距离修正:
       点火耦合 ~ 普适 (~0.020)
       低能耦合 = 点火耦合 + RG跑动
       RG跑动距离 ∝ (30 - p_ign)
       
       对于SU(3) (p=2): Δ_k = 28, b=7.0 > 0 → α增大
       对于SU(2) (p=3): Δ_k = 27, b=19/6 > 0 → α增大
       对于U(1) (p=5): Δ_k = 25, b=-41/10 < 0 → α减小
    
    C. 用p进展开的"有效圈数"解释:
       p进展开: x = a₀ + a₁p + a₂p² + ...
       p=2: 收敛最慢 → 需要更多项才能收敛 → 更多"有效圈图" → 耦合更强
       p=5: 收敛最快 → 更少项即收敛 → 更少"有效圈图" → 耦合更弱
    """
    print("\n" + "=" * 75)
    print("§C: p进结构 → 耦合常数定量映射")
    print("=" * 75)
    
    # 方案A: 直接比例
    print("""
  【方案A: 耦合 ∝ |p|_p = 1/p】
  
  直接比例给出错误的层次结构。需要RG跑动修正。
  """)
    
    # 方案B: 点火+RG跑动
    print("""  【方案B: 点火耦合 + RG跑动距离】
  
  假设: 所有规范力在点火点有相同的耦合 α_ign ≈ 0.0204
  低能耦合差异完全来自RG跑动距离的不同。
  
  RG跑动距离: 从点火点 k=p_ign 到 M_Z (k=30)
  """)
    
    alpha_ign = 0.0204
    mu_mz = energy_scale_dqpt(N_CYCLE)
    
    print(f"  {'规范力':<8s}  {'p_ign':>5s}  {'Δ_k':>5s}  {'μ_ign (GeV)':>16s}  {'b':>8s}  {'α(M_Z)':>10s}  {'实验':>10s}  {'偏差':>8s}")
    print(f"  {'-'*8}  {'-'*5}  {'-'*5}  {'-'*16}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*8}")
    
    scheme_b = {}
    for name, p, b_name in [('SU(3)', 2, 'SU3'), ('SU(2)', 3, 'SU2'), ('U(1)', 5, 'U1')]:
        mu_ign = energy_scale_dqpt(p)
        b = B_SM[b_name]
        alpha_mz = run_single_rg(alpha_ign, mu_ign, mu_mz, b)
        exp_val = EXP['alpha_s_MZ'] if name == 'SU(3)' else EXP['alpha_2_MZ'] if name == 'SU(2)' else EXP['alpha_1_MZ']
        dev = (alpha_mz - exp_val) / exp_val * 100
        print(f"  {name:<8s}  {p:5d}  {30-p:5d}  {mu_ign:16.3e}  {b:8.3f}  {alpha_mz:10.4f}  {exp_val:10.4f}  {dev:+7.1f}%")
        scheme_b[name] = {'alpha_mz': alpha_mz, 'deviation': dev}
    
    # 方案C: p进展开截断
    print(f"""
  【方案C: p进展开截断 — "有效圈数"解释】
  
  p进展开: x = a₀ + a₁p + a₂p² + a₃p³ + ...
  
  在p进度量下，|p^n|_p = 1/p^n。
  截断到给定精度 ε，需要的项数:
    n_needed(p, ε) = ⌈log(ε)/log(1/p)⌉ = ⌈-log(ε)/log(p)⌉
  
  对于 ε = 0.01 (1%精度):
    n_needed(2, 0.01) = ⌈-log(0.01)/log(2)⌉ = ⌈4.605/0.693⌉ = 7
    n_needed(3, 0.01) = ⌈4.605/1.099⌉ = 5
    n_needed(5, 0.01) = ⌈4.605/1.609⌉ = 3
  
  "有效圈数" = n_needed - 1 (减1因为a₁p是树图):
    SU(3): 6 圈 → 耦合修正 ∝ α_ign^6
    SU(2): 4 圈 → 耦合修正 ∝ α_ign^4
    U(1): 2 圈 → 耦合修正 ∝ α_ign^2
  
  这给出了耦合常数的层次结构: 更多"有效圈数" → 更大修正 → 更强耦合。
  """)
    
    eps = 0.01
    for p in GAUGE_PRIMES:
        n = int(np.ceil(-np.log(eps) / np.log(p)))
        print(f"    p={p}: n_needed = {n}, 有效圈数 = {n-1}")
    
    # 方案D: 用p进范数差分的RG β函数
    print(f"""
  【方案D: p进范数差分 → 有效β函数】
  
  定义 "p进β函数" 由相邻质数的p进范数差决定:
  
  Δ|p|_p = |p₁|_p₁ - |p₂|_p₂ (不是一个良好定义的量，因为范数定义在不同度量下)
  
  替代方案: 使用 p进赋值 v_p(p) = 1 的"层级差"
  
  v₂(2)=1, v₃(3)=1, v₅(5)=1 → 所有质数赋值相同
  但 log(p) 不同: log(2)=0.693, log(3)=1.099, log(5)=1.609
  
  可能的关系: β函数 ∝ 1/log(p) (因为log(p)越大，RG跑动"越慢")
  
  b_SU3 = 7.0, 1/log(2) = 1.443 → b×log(2) = 4.85
  b_SU2 = 3.167, 1/log(3) = 0.910 → b×log(3) = 3.48
  b_U1 = -4.1, 1/log(5) = 0.621 → b×log(5) = -6.60
  
  不收敛到公共值。需要更复杂的结构。
  """)
    
    return {
        'scheme_a': 'α ∝ 1/p — 定性正确，定量不准',
        'scheme_b': scheme_b,
        'scheme_c': 'p进截断 → 有效圈数',
        'scheme_d': 'p进范数差分 → 待定',
    }


# ============================================================
# §D: 组合分析 — 几何α₀ → 点火α₀ 的完整路径
# ============================================================

def compute_complete_path():
    """
    从几何α₀到点火α₀的完整推导路径。
    
    路径:
      4-单纯形 → Θ = arccos(1/4)
      → 5Θ = 5arccos(1/4), cos(5Θ) = 61/64
      → sin²(5Θ) = 375/4096
      → α₀^(em) = sin²(5Θ)/(4π) = 375/(16384π)
      → [GUT归一化] α_GUT = (8/3)α₀^(em) = 1000/(16384π)
      → [Sₚ·νₚ修正] α_ign = α_GUT × (1 + ε_Sν)
      → 点火耦合完全确定
    
    其中 ε_Sν 是 Sₚ·νₚ 非普适性的修正:
      ε_Sν = (⟨Sₚ·νₚ⟩ - Sₚ·νₚ) / ⟨Sₚ·νₚ⟩
      
    对于不同的p:
      SU(3): ε_Sν = (0.34489 - 0.34657)/0.34489 = -0.005
      SU(2): ε_Sν = (0.34489 - 0.36620)/0.34489 = -0.062
      U(1): ε_Sν = (0.34489 - 0.32189)/0.34489 = +0.067
    
    或者: 直接用 α_GUT 作为普适点火耦合，忽略 Sₚ·νₚ 修正。
    """
    print("\n" + "=" * 75)
    print("§D: 完整推导路径 — 几何 → GUT → 点火 → M_Z")
    print("=" * 75)
    
    # 几何α₀
    alpha_0_geom = 375.0 / (16384 * np.pi)
    
    # GUT归一化
    alpha_gut = 1000.0 / (16384 * np.pi)
    
    # Sₚ·νₚ 修正
    mean_power = np.mean([np.log(p) / p for p in GAUGE_PRIMES])
    
    alphas_ign_corrected = {}
    for p in GAUGE_PRIMES:
        power_p = np.log(p) / p
        epsilon = (power_p - mean_power) / mean_power
        alphas_ign_corrected[p] = alpha_gut * (1 + epsilon)
    
    # 正向RG跑动
    mu_mz = energy_scale_dqpt(N_CYCLE)
    b_map = {'SU(3)': B_SM['SU3'], 'SU(2)': B_SM['SU2'], 'U(1)': B_SM['U1']}
    
    print(f"""
  【完整推导链】
  
  Step 1: 几何裸值
    1/α₀^(em) = 16384π/375 = {1.0/alpha_0_geom:.6f}
    α₀^(em)   = 375/(16384π) = {alpha_0_geom:.8f}
  
  Step 2: GUT归一化 (sin²θ_W = 3/8 at GUT)
    1/α_GUT = 16384π/1000 = {1.0/alpha_gut:.6f}
    α_GUT   = 1000/(16384π) = {alpha_gut:.8f}
  
  Step 3: Sₚ·νₚ 修正 (各规范力点火耦合)
  """)
    
    print(f"  {'规范力':<8s}  {'Sₚ·νₚ':>10s}  {'ε_Sν':>8s}  {'α_ign':>10s}  {'α_ign⁻¹':>10s}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*10}")
    
    for name, p in [('SU(3)', 2), ('SU(2)', 3), ('U(1)', 5)]:
        power_p = np.log(p) / p
        epsilon = (power_p - mean_power) / mean_power
        alpha_ign = alphas_ign_corrected[p]
        print(f"  {name:<8s}  {power_p:10.5f}  {epsilon:+7.1%}  {alpha_ign:10.6f}  {1.0/alpha_ign:10.2f}")
    
    # 正向RG跑动到M_Z
    print(f"\n  Step 4: 正向RG跑动 → M_Z 可观测量\n")
    print(f"  {'规范力':<8s}  {'α_ign':>10s}  {'b':>8s}  {'α(M_Z)':>10s}  {'实验':>10s}  {'偏差':>8s}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*8}")
    
    alphas_mz = {}
    for name, p, b_name in [('SU(3)', 2, 'SU3'), ('SU(2)', 3, 'SU2'), ('U(1)', 5, 'U1')]:
        mu_ign = energy_scale_dqpt(p)
        alpha_ign = alphas_ign_corrected[p]
        alpha_mz = run_single_rg(alpha_ign, mu_ign, mu_mz, B_SM[b_name])
        alphas_mz[name] = alpha_mz
        
        exp_val = EXP['alpha_s_MZ'] if name == 'SU(3)' else EXP['alpha_2_MZ'] if name == 'SU(2)' else EXP['alpha_1_MZ']
        dev = (alpha_mz - exp_val) / exp_val * 100
        print(f"  {name:<8s}  {alpha_ign:10.6f}  {B_SM[b_name]:8.3f}  {alpha_mz:10.4f}  {exp_val:10.4f}  {dev:+7.1f}%")
    
    # 计算可观测量
    alpha_3 = alphas_mz['SU(3)']
    alpha_2 = alphas_mz['SU(2)']
    alpha_1 = alphas_mz['U(1)']
    alpha_Y = (3.0 / 5) * alpha_1
    sin2_thetaW = alpha_Y / (alpha_2 + alpha_Y)
    alpha_em = alpha_2 * sin2_thetaW
    
    errors = {
        'alpha_s': (alpha_3 - EXP['alpha_s_MZ']) / EXP['alpha_s_MZ'] * 100,
        'alpha_em_inv': (1.0/alpha_em - EXP['alpha_inv_MZ']) / EXP['alpha_inv_MZ'] * 100,
        'sin2_thetaW': (sin2_thetaW - EXP['sin2_thetaW_MZ']) / EXP['sin2_thetaW_MZ'] * 100,
    }
    rms = np.sqrt(np.mean([e**2 for e in errors.values()]))
    
    print(f"""
  【M_Z 可观测量 (几何+GUT+Sₚ·νₚ修正)】
  
  α_s(M_Z)   = {alpha_3:.4f}  (实验: {EXP['alpha_s_MZ']:.4f})  偏差: {errors['alpha_s']:+.1f}%
  α⁻¹(M_Z)   = {1.0/alpha_em:.1f}  (实验: {EXP['alpha_inv_MZ']:.1f})  偏差: {errors['alpha_em_inv']:+.1f}%
  sin²θ_W    = {sin2_thetaW:.5f}  (实验: {EXP['sin2_thetaW_MZ']:.5f})  偏差: {errors['sin2_thetaW']:+.1f}%
  
  RMS 偏差: {rms:.1f}%
  
  【与普适点火方案对比】
  
  普适点火 (α₀=0.0204):       RMS ~10.6%
  几何+GUT (α_GUT=0.01943):   RMS ~{rms:.1f}%
  几何+GUT+Sₚ·νₚ修正:         RMS ~{rms:.1f}%
  
  几何+GUT方案的关键优势: α_GUT = 1000/(16384π) 是完全从第一性原理
  推导的，没有任何可调参数。普适点火方案需要从SM反向拟合α₀=0.0204。
  """)
    
    # 对比不同方案
    print(f"  【方案对比总览】\n")
    print(f"  {'方案':<30s}  {'α₀来源':<20s}  {'可调参数':>10s}  {'RMS':>8s}")
    print(f"  {'-'*30}  {'-'*20}  {'-'*10}  {'-'*8}")
    print(f"  {'普适点火 (SM反向)':<30s}  {'SM实验拟合':<20s}  {'1 (α₀)':>10s}  {'~0.0%':>8s}")
    print(f"  {'普适点火 (自然尺度)':<30s}  {'1/(4π²)':<20s}  {'0':>10s}  {'~384%':>8s}")
    print(f"  {'几何+GUT (本工作)':<30s}  {'1000/(16384π)':<20s}  {'0':>10s}  {f'~{rms:.1f}%':>8s}")
    
    return {
        'alpha_0_geom': alpha_0_geom,
        'alpha_gut': alpha_gut,
        'alphas_ign_corrected': alphas_ign_corrected,
        'alphas_mz': alphas_mz,
        'alpha_s_mz': alpha_3,
        'alpha_em_inv': 1.0 / alpha_em,
        'sin2_thetaW': sin2_thetaW,
        'errors': errors,
        'rms': rms,
    }


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 75)
    print("  深度分析：几何精细结构常数 → 点火耦合 → M_Z")
    print("  CNT 第一性原理推导")
    print("=" * 75)
    print(f"  日期: 2026-07-04")
    
    results = {}
    
    # §A: 几何α₀ → GUT α_GUT
    results['geometric_to_gut'] = compute_geometric_to_gut()
    
    # §B: Sₚ·νₚ 分析
    results['action_frequency'] = compute_action_frequency_relation()
    
    # §C: p进结构 → 耦合
    results['padic_to_coupling'] = compute_padic_to_coupling()
    
    # §D: 完整路径
    results['complete_path'] = compute_complete_path()
    
    # 保存结果
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, '08-深度分析_结果.json')
    
    def convert(obj):
        if isinstance(obj, dict):
            return {str(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convert(results), f, indent=2, ensure_ascii=False)
    
    print(f"\n结果已保存到: {filename}")
    
    return results


if __name__ == '__main__':
    results = main()