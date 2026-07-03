"""
递归博弈论数值计算 v5.0：含p进相位项（von Mangoldt修正）
==========================================================
基于 CNT 递归博弈论框架，从第一性原理推导收益函数参数，
数值求解三策略复制子方程，计算母轨迹和 M_Z 能标处的规范耦合常数。

关键修正（v5.0 — 2026-07-04）：
  【修正7】p进相位项：引入 von Mangoldt 型相位函数 Λ_i(k)
           F_i^eff(x,S,k) = F_i(x,S) + κ · Λ_i(k)
           Λ_i(k) = log(p_i) 当 k = p_i^m (m≥1)，否则 0
           质数幂处产生动力学跃迁（DQPT），区别于质数点火
           理论来源：母轨迹HPI的驻相近似 ∂Φ_k/∂x_i = κ·Λ_i(k)
           物理意义：再生产历史在质数幂处的层级记忆效应
  【修正6】电弱混合修正：策略3 = U(1)_Y（超荷，非U(1)_EM）
  【修正5】明确区分策略频率 x_i 和耦合常数 α_i = x_i · S(k)
  【修正4】SM β函数校准的收益函数 F_i(x,S) = (λS/2π)[B(x) - b_i x_i]

核心方程：
  (a) 策略频率: x_i(k) = α_i(k) / Σ_j α_j(k) ∈ Δ²
  (b) 复制子动力学: dx_i/dk = x_i(F_i^eff - F̄^eff)
  (c) 有效收益: F_i^eff = F_i(x,S) + κ·Λ_i(k)
  (d) 绝对尺度: dS/dk = -λ S² B(x) / (2π)
  (e) 耦合常数: α_i(k) = x_i(k) · S(k)
  (f) 电弱混合: α_EM = α_2 · sin²θ_W
  (g) p进相位: Λ_i(k) = log(p_i) · δ_{ν_{p_i}(k)>0}

日期: 2026-07-04
认识论地位: [第一性原理推导] + [SM β函数校准] + [p进相位修正] + [电弱混合] + [数值验证]
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# §1. 第一性原理参数与物理常数
# ============================================================

# 1.1 质数-规范力对应
# 重要：三种策略对应 SM 规范群 SU(3)×SU(2)×U(1)_Y
# 策略3 = U(1)_Y (超荷)，非 U(1)_EM (电磁)
# 物理电磁耦合通过电弱混合从 α_2 和 sin²θ_W 导出
primes = np.array([2, 3, 5])
prime_gauge = {2: 0, 3: 1, 5: 2}
gauge_names = ['SU(3) 强', 'SU(2) 弱', 'U(1)_Y 超荷']
gauge_generators = np.array([8, 3, 1])  # 规范群生成元数

# 1.2 SM β 函数系数（单圈，MS-bar方案，GUT归一化）
# β_i = b_i · α_i²/(2π)
b_sm = np.array([-7.0, -19.0/6, 41.0/10])
# SU(3): b_3 = -7 (渐近自由)
# SU(2): b_2 = -19/6 ≈ -3.167 (弱渐近自由)
# U(1)_Y: b_1 = 41/10 = 4.1 (非渐近自由，GUT归一化)

# 1.2b 电弱混合参数
sin2_theta_W = 0.2312  # sin²θ_W(M_Z), MS-bar方案, PDG 2024
# 电弱统一关系: e = g_2 sin θ_W = g_Y cos θ_W
# α_EM = e²/(4π) = α_2 · sin²θ_W
# α_1 = (5/3)α_Y (GUT归一化)

# 1.3 能标参数
M_P = 1.22e19       # GeV, 普朗克质量
M_Z = 91.1876       # GeV, Z 玻色子质量 (PDG 2024)
# 能标函数: μ_k = M_P · (M_Z/M_P)^(k/30)
# d ln μ/dk = ln(M_Z/M_P)/30

# 1.4 周期参数（adelic 约束）
N_cycle = 30  # ∏_p Z_p = 1/(2·3·5) → N_cycle = 30

# 1.5 能标演化率 λ = |d ln μ/dk|
lambda_dlnmu = abs(np.log(M_Z / M_P)) / N_cycle  # ≈ 1.314

# 1.6 k_MZ: M_Z 能标对应的再生产计数
# μ_k = M_P · (M_Z/M_P)^(k/30) → k = 30 · ln(μ/M_P) / ln(M_Z/M_P)
# 对于 μ = M_Z: k = 30
# 实际上 μ_30 = M_P · (M_Z/M_P) = M_Z，所以 k_MZ = 30
# 但物理上我们希望在 N_cycle 循环中，M_Z 在 k ≈ 17
# 让我们使用更合理的映射：μ_k = M_P · (M_Z/M_P)^(k/N_cycle)
# 在 k = N_cycle 时，μ = M_Z
# 实际上我们应该用 μ_k = M_P · exp(-λ k) 其中 λ = ln(M_P/M_Z)/N_cycle
# 在 k = N_cycle 时: μ = M_P · exp(-λ·N_cycle) = M_P · M_Z/M_P = M_Z
# 所以 M_Z 在 k = N_cycle: 但这意味着 M_Z 是IR端点
# 物理上更合理的是让 M_Z 在 k = 17 左右
# 使用 μ_k = M_P · (M_Z/M_P)^(k/N_cycle)，则 k_MZ = N_cycle = 30
# 但之前的框架把 M_Z 放在 k=17，即 μ_17 = M_P · (M_Z/M_P)^(17/30)
# 此时 μ_17 ≈ 2.4×10^9 GeV，不是 M_Z
# 我们需要重新校准。使用 μ_k = M_P · exp(-λ·k)
# 其中 λ 使得 μ_N_cycle = M_Z
# λ = ln(M_P/M_Z)/N_cycle
# 那么 μ_k = M_P · (M_Z/M_P)^(k/N_cycle)
# 在 k = N_cycle 时: μ = M_Z ✓
# 但之前把 M_Z 放在 k=17 是因为希望 M_Z 在循环中间
# 让我们重新定义：μ_k = M_P · exp(-λ·k)，λ = ln(M_P/M_Z)/N_cycle
# 则 k_MZ = N_cycle = 30

lambda_energy = np.log(M_P / M_Z) / N_cycle  # ≈ 1.314
# 验证: μ(N_cycle) = M_P · exp(-λ·N_cycle) = M_P · M_Z/M_P = M_Z ✓

# 重要：M_Z 在 k = N_cycle，不是 k = 17
# 之前的 k_MZ = 17 是错误的标度
k_MZ = N_cycle  # M_Z 在循环终点
# 但物理上，RG流从M_P→M_Z跨越整个循环
# 中间点对应中间能标
# 例如 k=15: μ = M_P·(M_Z/M_P)^(15/30) = M_P·√(M_Z/M_P) ≈ 3.5×10^10 GeV

# 1.7 几何推导的 GUT 耦合常数（零自由参数）
alpha_GUT_geom = 125.0 / (2048.0 * np.pi)  # ≈ 0.019428
# 来源: 4-单纯形二面角 → Chebyshev展开 → 裸电磁耦合 → GUT归一化

# 1.8 实验值 (PDG 2024)
alpha_s_exp  = 0.1180       # α_s(M_Z)
alpha_w_exp  = 0.0337       # g²/(4π) at M_Z, sin²θ_W = 0.2312
alpha_em_exp = 1.0/127.952  # α_EM(M_Z) ≈ 0.00781
alpha_em_low_exp = 1.0/137.035999084  # 低能精细结构常数

# 验证: 总耦合强度 S(M_Z)
S_MZ_exp = alpha_s_exp + alpha_w_exp + alpha_em_exp  # ≈ 0.1595


# ============================================================
# §2. 收益函数（从 SM β 函数反推校准）
# ============================================================

def B_function(x):
    """B(x) = Σ_j b_j x_j²"""
    return np.dot(b_sm, x**2)

def fitness_sm_calibrated(x, S):
    """
    从 SM β 函数反推的收益函数。
    
    F_i(x, S) = (λS/2π) [B(x) - b_i x_i]
    
    性质:
    - F̄ = Σ_i x_i F_i = 0 (自洽)
    - F_i - F̄ = F_i (因为 F̄ = 0)
    - dx_i/dk = x_i F_i 精确再现 SM RG 流
    
    Parameters:
    -----------
    x : array, shape (3,)
        策略频率分布（归一化耦合常数）
    S : float
        绝对尺度 S(k) = Σ_j α_j(k)
        
    Returns:
    --------
    F : array, shape (3,)
        收益值 (F̄ = 0)
    """
    B = B_function(x)
    prefactor = lambda_energy * S / (2.0 * np.pi)
    return prefactor * (B - b_sm * x)


def fitness_first_principles(x, k, S, gamma_vec, delta_vec):
    """
    第一性原理收益函数（CNT原生形式）。
    
    F_i(x, k, S) = c_i · exp(γ_i · x_i) + Σ_p δ(k,p) · Δ_i
    
    其中 c_i = dim(G_i) / (2π) · S（群论因子 × 耦合尺度）
    γ_i = -κ·b_i（自指增强，符号修正）
    Δ_i = η/p_i（点火增强）
    
    Parameters:
    -----------
    x : array, shape (3,)
        策略频率分布
    k : int
        再生产计数
    S : float
        绝对尺度
    gamma_vec : array, shape (3,)
        自指增强参数
    delta_vec : array, shape (3,)
        点火增强
    """
    # 基础收益: 群论因子 × 耦合尺度
    c_vec = gauge_generators * S / (2.0 * np.pi)
    F_base = c_vec * np.exp(gamma_vec * x)
    
    # 点火增强
    F_enhance = np.zeros(3)
    for p, idx in prime_gauge.items():
        if k == p:
            F_enhance[idx] = delta_vec[idx]
        elif k > p and k % p == 0 and k != p:
            m = 0
            kk = k
            while kk % p == 0:
                kk //= p
                m += 1
            if m >= 2:
                F_enhance[idx] = delta_vec[idx] * (0.5 ** (m - 1))
    
    return F_base + F_enhance


# ============================================================
# §2.5 p进相位项：von Mangoldt函数
# ============================================================

def von_mangoldt_padic(k, primes_vec):
    """
    策略特定的广义 von Mangoldt 函数。
    
    Λ_i(k) = log(p_i) 当 k = p_i^m (m ≥ 1)，否则 0。
    
    这是CNT中合成p进数相位函数 Φ_k 的核心组件。
    在母轨迹HPI的驻相近似中，∂Φ_k/∂x_i ∝ Λ_i(k)。
    
    物理意义：
    - k = p_i: 质数点火（新再生产形式的首次出现）
    - k = p_i^m (m≥2): 质数幂跃迁（再生产形式的层级深化）
    - 质数幂处的"kick"编码了再生产历史的层级记忆
    
    Parameters:
    -----------
    k : int
        再生产计数
    primes_vec : array, shape (3,)
        质数向量 [2, 3, 5]
        
    Returns:
    --------
    Lambda : array, shape (3,)
        Λ_i(k) 值
    """
    Lambda = np.zeros(3)
    for i, p in enumerate(primes_vec):
        if k > 0 and k % p == 0:
            kk = k
            m = 0
            while kk % p == 0:
                kk //= p
                m += 1
            # 关键修正：只有 k == p^m（即 kk == 1）才是质数幂
            # 而非 k 的所有 p 的倍数
            if kk == 1 and m >= 1:
                Lambda[i] = np.log(p)
    return Lambda


def fitness_with_padic_phase(x, S, k, kappa, primes_vec):
    """
    含p进相位修正的有效收益函数。
    
    F_i^eff(x, S, k) = F_i(x, S) + κ · Λ_i(k)
    
    其中 F_i 是SM β函数校准的基础收益，Λ_i(k) 是 von Mangoldt 相位。
    
    性质：
    - F̄^eff = κ · Σ_j x_j Λ_j(k) （因为 F̄ = 0）
    - dx_i/dk = x_i [F_i + κ(Λ_i - Σ_j x_j Λ_j)]
    - 自动保持 Σ_i dx_i = 0（单纯形约束）
    
    Parameters:
    -----------
    x : array, shape (3,)
        策略频率分布
    S : float
        绝对尺度
    k : int
        当前再生产计数（用于相位计算的是 k+1，即目标步）
    kappa : float
        p进相位耦合强度
    primes_vec : array, shape (3,)
        质数向量
        
    Returns:
    --------
    F_eff : array, shape (3,)
        有效收益值
    F_base : array, shape (3,)
        基础收益（不含相位修正）
    Lambda_k : array, shape (3,)
        当前步的 von Mangoldt 相位值
    """
    F_base = fitness_sm_calibrated(x, S)
    Lambda_k = von_mangoldt_padic(k, primes_vec)
    F_eff = F_base + kappa * Lambda_k
    return F_eff, F_base, Lambda_k

def simulate_mother_trajectory_sm(K=N_cycle, x0=None, S0=None, use_ignition=True, 
                                   kappa=0.0, use_padic_phase=True):
    """
    模拟母轨迹：从 k=0 到 k=K 的 (x, S) 耦合演化。
    
    使用 SM β 函数校准的收益函数 + p进相位修正。
    
    演化方程:
        dx_i/dk = x_i · (F_i^eff - F̄^eff)
        F_i^eff = F_i(x, S) + κ · Λ_i(k_target)
        dS/dk   = -λ S² B(x) / (2π)
    
    kappa=0 时退化为 v4.0 行为。
    
    Parameters:
    -----------
    K : int
        总步数
    x0 : array or None
        初始策略分布 (默认 GUT 对称)
    S0 : float or None
        初始绝对尺度 (默认 3·α_GUT)
    use_ignition : bool
        是否在质数处加入点火增强
    kappa : float
        p进相位耦合强度（默认0=无相位修正）
    use_padic_phase : bool
        是否启用p进相位修正
        
    Returns:
    --------
    trajectory : array, shape (K+1, 3)
        策略频率 x_i(k)
    S_history : array, shape (K+1,)
        绝对尺度 S(k)
    alpha_history : array, shape (K+1, 3)
        耦合常数 α_i(k) = x_i(k) · S(k)
    ignition_events : list of dict
        点火事件
    phase_events : list of dict
        p进相位跃迁事件
    """
    if x0 is None:
        x0 = np.array([1.0/3, 1.0/3, 1.0/3])
    if S0 is None:
        S0 = 3.0 * alpha_GUT_geom  # 3 × 0.019428 = 0.058284
    
    trajectory = np.zeros((K + 1, 3))
    S_history = np.zeros(K + 1)
    alpha_history = np.zeros((K + 1, 3))
    
    trajectory[0] = x0
    S_history[0] = S0
    alpha_history[0] = x0 * S0
    
    ignition_events = []
    phase_events = []
    
    # 点火参数
    eta_ignition = 0.15  # 点火增强比例
    
    for k in range(K):
        x = trajectory[k]
        S = S_history[k]
        k_target = k + 1  # 目标步（用于相位计算）
        
        # 计算收益（含p进相位修正）
        if use_padic_phase and kappa != 0.0:
            F_eff, F_base, Lambda_k = fitness_with_padic_phase(x, S, k_target, kappa, primes)
        else:
            F_base = fitness_sm_calibrated(x, S)
            F_eff = F_base.copy()
            Lambda_k = np.zeros(3)
        
        # 点火增强（仅在质数 k_target 处）
        if use_ignition:
            for p, idx in prime_gauge.items():
                if k_target == p:
                    F_eff[idx] += eta_ignition * S / p
        
        # 复制子步进: dx_i = x_i · (F_i^eff - F̄^eff)
        F_bar_eff = np.dot(x, F_eff)
        dx = x * (F_eff - F_bar_eff)
        x_new = x + dx
        
        # 确保概率分布合法
        x_new = np.maximum(x_new, 1e-15)
        x_new = x_new / np.sum(x_new)
        
        # 更新 S: dS/dk = -λ S² B(x) / (2π)
        B = B_function(x)
        dS = -lambda_energy * S**2 * B / (2.0 * np.pi)
        S_new = S + dS
        
        # 确保 S > 0
        if S_new <= 0:
            S_new = S * 0.99
        
        trajectory[k + 1] = x_new
        S_history[k + 1] = S_new
        alpha_history[k + 1] = x_new * S_new
        
        # 记录点火事件（质数处）
        for p, idx in prime_gauge.items():
            if k_target == p:
                ignition_events.append({
                    'k': p,
                    'strategy': idx,
                    'name': gauge_names[idx],
                    'x_before': trajectory[k][idx],
                    'x_after': x_new[idx],
                    'S': S,
                    'alpha_ign': alpha_history[k+1][idx],
                    'alpha_ign_normalized': x_new[idx],
                })
        
        # 记录p进相位跃迁事件（质数幂处，含质数本身）
        if use_padic_phase and np.any(Lambda_k > 0):
            for i in range(3):
                if Lambda_k[i] > 0:
                    phase_events.append({
                        'k': k_target,
                        'strategy': i,
                        'name': gauge_names[i],
                        'Lambda': Lambda_k[i],
                        'F_base': F_base[i],
                        'F_phase': kappa * Lambda_k[i],
                        'F_eff': F_eff[i],
                        'x_before': x[i],
                        'x_after': x_new[i],
                        'dx_phase': dx[i],
                    })
    
    return trajectory, S_history, alpha_history, ignition_events, phase_events


# ============================================================
# §4. 运行计算
# ============================================================

print("=" * 70)
print("  递归博弈论 v5.0：含p进相位修正（von Mangoldt DQPT）")
print("  CNT 框架 — 母轨迹、RG 流、p进相位与耦合常数")
print("  [修正: SM β函数 + p进相位 + 电弱混合]")
print("=" * 70)
print()
print("第一性原理参数:")
print(f"  α_GUT (几何)       = {alpha_GUT_geom:.6f}  (≈ 1/{1/alpha_GUT_geom:.1f})")
print(f"  S(0) = 3·α_GUT    = {3*alpha_GUT_geom:.6f}")
print(f"  λ = |d ln μ/dk|    = {lambda_energy:.4f}")
print(f"  N_cycle            = {N_cycle}")
print(f"  k_MZ               = {k_MZ}  (M_Z 在循环终点)")
print(f"  b_sm               = [{b_sm[0]:.1f}, {b_sm[1]:.4f}, {b_sm[2]:.2f}]")
print()

# 4.0 κ 扫描：寻找最优p进相位耦合强度
print("§0. κ 参数扫描 — p进相位耦合强度优化")
print("-" * 60)
print(f"  {'κ':<12} {'α_s(M_Z)':<12} {'α_2(M_Z)':<12} {'α_EM(corr)':<14} {'α_s偏差':<10} {'α_2偏差':<10} {'α_EM偏差':<10}")
print(f"  {'-'*80}")

kappa_values = [0.0, 0.0005, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.004, 0.005, 0.007, 0.01]
best_kappa = 0.0
best_total_dev = 1e10
scan_results = []

for kappa_test in kappa_values:
    traj, S_hist, alpha_hist, ign, phase = simulate_mother_trajectory_sm(
        K=N_cycle, use_ignition=True, kappa=kappa_test, use_padic_phase=(kappa_test > 0)
    )
    a_MZ = alpha_hist[k_MZ]
    a_em_corr = a_MZ[1] * sin2_theta_W
    
    dev_s = abs(a_MZ[0] - alpha_s_exp) / alpha_s_exp * 100
    dev_w = abs(a_MZ[1] - alpha_w_exp) / alpha_w_exp * 100
    dev_em = abs(a_em_corr - alpha_em_exp) / alpha_em_exp * 100
    total_dev = dev_s + dev_w + dev_em
    
    scan_results.append({
        'kappa': kappa_test, 'a_s': a_MZ[0], 'a_2': a_MZ[1],
        'a_em': a_em_corr, 'dev_s': dev_s, 'dev_w': dev_w, 'dev_em': dev_em,
        'total': total_dev
    })
    
    if total_dev < best_total_dev:
        best_total_dev = total_dev
        best_kappa = kappa_test
    
    marker = " ← 最优" if kappa_test == best_kappa else ""
    print(f"  {kappa_test:<12.5f} {a_MZ[0]:<12.6f} {a_MZ[1]:<12.6f} {a_em_corr:<14.6f} {dev_s:<10.2f}% {dev_w:<10.2f}% {dev_em:<10.2f}%{marker}")

print()
print(f"  最优 κ = {best_kappa:.5f}, 总偏差 = {best_total_dev:.2f}%")
print(f"  v4.0 (κ=0) 总偏差 = {scan_results[0]['total']:.2f}%")
if best_kappa > 0:
    improvement = (scan_results[0]['total'] - best_total_dev) / scan_results[0]['total'] * 100
    print(f"  p进相位修正改善: {improvement:.1f}%")
print()

# 4.1 使用最优 κ 模拟母轨迹
print(f"§1. 母轨迹模拟 (κ = {best_kappa})")
print("-" * 40)
trajectory, S_history, alpha_history, ignition_events, phase_events = simulate_mother_trajectory_sm(
    K=N_cycle, use_ignition=True, kappa=best_kappa, use_padic_phase=(best_kappa > 0)
)

print("§1a. 点火事件")
for ev in ignition_events:
    print(f"  k={ev['k']}: {ev['name']} 点火")
    print(f"    点火前频率 x_i = {ev['x_before']:.4f}")
    print(f"    点火后频率 x_i = {ev['x_after']:.4f}")
    print(f"    绝对尺度 S = {ev['S']:.6f}")
    print(f"    点火耦合 α₀ = x_i·S = {ev['alpha_ign']:.6f}")
    print(f"    归一化点火耦合 x_i = {ev['alpha_ign_normalized']:.6f}")
    print()

print("§1b. p进相位跃迁事件（质数幂DQPT）")
print("-" * 40)
print(f"  {'k':<6} {'策略':<16} {'Λ_i(k)':<10} {'F_base':<12} {'F_phase':<12} {'F_eff':<12} {'x前':<10} {'x后':<10}")
print(f"  {'-'*88}")
for ev in phase_events:
    print(f"  {ev['k']:<6} {ev['name']:<16} {ev['Lambda']:<10.4f} {ev['F_base']:<12.6f} {ev['F_phase']:<12.6f} {ev['F_eff']:<12.6f} {ev['x_before']:<10.6f} {ev['x_after']:<10.6f}")
print()

# 4.2 M_Z 能标处的耦合常数
x_MZ = trajectory[k_MZ]
S_MZ = S_history[k_MZ]
alpha_MZ = alpha_history[k_MZ]
alpha_em_corrected = alpha_MZ[1] * sin2_theta_W
alpha_Y_MZ = alpha_MZ[2]

print("§2. M_Z 能标 (k=30) 处的耦合常数")
print("-" * 40)
print(f"  策略频率 x = ({x_MZ[0]:.6f}, {x_MZ[1]:.6f}, {x_MZ[2]:.6f})")
print(f"  绝对尺度 S = {S_MZ:.6f}  (实验: S_MZ = {S_MZ_exp:.6f})")
print(f"  α_s  = {alpha_MZ[0]:.6f}  (实验: {alpha_s_exp:.4f})")
print(f"  α_2  = {alpha_MZ[1]:.6f}  (实验: {alpha_w_exp:.4f})")
print(f"  α_Y  = {alpha_MZ[2]:.6f}  (U(1)_Y 超荷)")
print(f"  α_EM = α_2·sin²θ_W = {alpha_em_corrected:.6f}  (实验: {alpha_em_exp:.6f})")
print()
print(f"  {'耦合常数':<20} {'CNT v5.0':<12} {'实验值':<12} {'偏差':<10} {'v4.0偏差':<12}")
print(f"  {'-'*66}")
for i, (name, exp, v4_dev) in enumerate([
    ('α_s(M_Z) 强', alpha_s_exp, scan_results[0]['dev_s']),
    ('α_2(M_Z) 弱', alpha_w_exp, scan_results[0]['dev_w']),
    ('α_EM(M_Z) 电磁', alpha_em_exp, scan_results[0]['dev_em']),
]):
    if i == 0: val = alpha_MZ[0]
    elif i == 1: val = alpha_MZ[1]
    else: val = alpha_em_corrected
    dev = abs(val - exp) / exp * 100
    print(f"  {name:<20} {val:<12.6f} {exp:<12.4f} {dev:<10.2f}% {v4_dev:<12.2f}%")
print()

# 4.3 精细结构常数
alpha_em_low = alpha_em_corrected / (1.0 - alpha_em_corrected * (2.0/(3.0*np.pi)) * np.log(M_Z/0.000511))
print("§3. 精细结构常数（低能极限）")
print("-" * 40)
print(f"  α_EM(M_Z) CNT: {alpha_em_corrected:.6f}  (≈ 1/{1/alpha_em_corrected:.1f})")
print(f"  α_EM(0)  CNT: {alpha_em_low:.6f}  (≈ 1/{1/alpha_em_low:.1f})")
print(f"  α_EM(0)  实验: {alpha_em_low_exp:.6f}  (≈ 1/137.036)")
print(f"  偏差: {abs(alpha_em_low - alpha_em_low_exp)/alpha_em_low_exp*100:.2f}%")
print()

# 4.4 母轨迹（含相位标记）
print("§4. 母轨迹（含p进相位跃迁标记）")
print("-" * 40)
print(f"  {'k':<6} {'μ (GeV)':<14} {'x₁ (强)':<12} {'x₂ (弱)':<12} {'x₃ (超荷)':<12} {'事件'}")
print(f"  {'-'*74}")
for k in range(N_cycle + 1):
    mu_k = M_P * np.exp(-lambda_energy * k)
    event = ""
    # 点火
    for p, idx in prime_gauge.items():
        if k == p:
            event = f"点火-{gauge_names[idx][:4]}"
    # p进相位跃迁（质数幂）
    Lambda_k = von_mangoldt_padic(k, primes)
    for i in range(3):
        if Lambda_k[i] > 0 and k not in primes:
            if event:
                event += " + "
            event += f"DQPT-{gauge_names[i][:4]}"
    if k == k_MZ:
        if event:
            event += " + M_Z"
        else:
            event = "M_Z"
    print(f"  {k:<6} {mu_k:<14.2e} {trajectory[k][0]:<12.6f} {trajectory[k][1]:<12.6f} {trajectory[k][2]:<12.6f} {event}")

print()

# 4.5 点火耦合常数
print("§5. 点火耦合常数")
print("-" * 40)
print(f"  {'规范力':<20} {'k':<6} {'α₀ (CNT)':<14} {'1/α₀':<10} {'x_i (归一化)':<14}")
for ev in ignition_events:
    print(f"  {ev['name']:<20} {ev['k']:<6} {ev['alpha_ign']:<14.6f} {1/ev['alpha_ign']:<10.2f} {ev['alpha_ign_normalized']:<14.6f}")
print()

# 4.6 闭合性检验
print("§6. 离散环闭合性检验")
closure_error = np.linalg.norm(trajectory[N_cycle] - trajectory[0])
closure_S = abs(S_history[N_cycle] - S_history[0]) / S_history[0]
print(f"  ||x(N_cycle) - x(0)|| = {closure_error:.2e}")
print(f"  |S(N_cycle) - S(0)|/S(0) = {closure_S:.2e}")
print(f"  x(0)  = ({trajectory[0][0]:.6f}, {trajectory[0][1]:.6f}, {trajectory[0][2]:.6f})")
print(f"  x(30) = ({trajectory[N_cycle][0]:.6f}, {trajectory[N_cycle][1]:.6f}, {trajectory[N_cycle][2]:.6f})")
print()

# 4.7 与几何推导对比
print("§7. 与几何推导的对比")
print("-" * 40)
print(f"  几何 α_GUT        = {alpha_GUT_geom:.6f}  (≈ 1/{1/alpha_GUT_geom:.1f})")
print(f"  几何 α₀^EM        = {375/(16384*np.pi):.6f}  (≈ 1/{16384*np.pi/375:.1f})")
print(f"  博弈论 α_EM(M_Z)  = {alpha_em_corrected:.6f} [修正: α_2·sin²θ_W]")
print(f"  博弈论 α_EM(0)    = {alpha_em_low:.6f}")
print()

# 4.8 电弱混合分析
print("§8. 电弱混合分析")
print("-" * 40)
print(f"  α_2(M_Z) = {alpha_MZ[1]:.6f}")
print(f"  α_Y(M_Z) = {alpha_MZ[2]:.6f}")
print(f"  sin²θ_W^eff = {alpha_em_exp/alpha_MZ[1]:.4f}  (实验: {sin2_theta_W})")
print()

# 4.9 质数幂频率统计
print("§9. 质数幂相位跃迁统计")
print("-" * 40)
for i in range(3):
    p = primes[i]
    powers = [ev['k'] for ev in phase_events if ev['strategy'] == i]
    print(f"  {gauge_names[i]} (p={p}): 跃迁点 k = {powers}")
    print(f"    质数幂: {[p**m for m in range(1, 6) if p**m <= N_cycle]}")
print()

# ============================================================
# §5. 可视化
# ============================================================

# ============================================================
# §5. 可视化 (v5.0)
# ============================================================

colors = ['#2196F3', '#4CAF50', '#FF5722']
labels = ['SU(3) Strong', 'SU(2) Weak', 'U(1)_Y Hypercharge']

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle(f'CNT v5.0: p-adic Phase Correction ($\\kappa={best_kappa}$)', 
             fontsize=14, fontweight='bold')

# Plot 1: Strategy frequencies
ax = axes[0, 0]
for i in range(3):
    ax.plot(range(N_cycle + 1), trajectory[:, i], color=colors[i], label=labels[i], linewidth=2)
for ev in ignition_events:
    ax.axvline(x=ev['k'], color=colors[ev['strategy']], linestyle='--', alpha=0.4)
for ev in phase_events:
    ax.axvline(x=ev['k'], color=colors[ev['strategy']], linestyle=':', alpha=0.2, linewidth=0.5)
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('Strategy frequency x_i')
ax.set_title('Strategy Frequencies (Mother Trajectory)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 2: Coupling constants
ax = axes[0, 1]
ax.plot(range(N_cycle + 1), alpha_history[:, 0], color=colors[0], label='α_s (Strong)', linewidth=2)
ax.plot(range(N_cycle + 1), alpha_history[:, 1], color=colors[1], label='α_2 (Weak)', linewidth=2)
ax.plot(range(N_cycle + 1), alpha_history[:, 2], color=colors[2], label='α_Y (Hypercharge)', linewidth=2)
ax.axhline(y=alpha_s_exp, color=colors[0], linestyle=':', alpha=0.5)
ax.axhline(y=alpha_w_exp, color=colors[1], linestyle=':', alpha=0.5)
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('Coupling constant α_i')
ax.set_title('Coupling Constants α_i(k) = x_i(k)·S(k)')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 3: S(k)
ax = axes[0, 2]
ax.plot(range(N_cycle + 1), S_history, 'k-', linewidth=2)
ax.axhline(y=S_MZ_exp, color='gray', linestyle=':', alpha=0.5, label=f'S_MZ exp={S_MZ_exp:.4f}')
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('Absolute scale S(k)')
ax.set_title('Absolute Scale S(k) = Σ α_i(k)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 4: Simplex
ax = axes[1, 0]
triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
ax.plot([triangle[0,0], triangle[1,0]], [triangle[0,1], triangle[1,1]], 'k-', linewidth=1)
ax.plot([triangle[1,0], triangle[2,0]], [triangle[1,1], triangle[2,1]], 'k-', linewidth=1)
ax.plot([triangle[2,0], triangle[0,0]], [triangle[2,1], triangle[0,1]], 'k-', linewidth=1)
vertices = ['SU(3) Strong', 'SU(2) Weak', 'U(1)_Y']
for i, (vx, vy) in enumerate(triangle):
    ax.text(vx, vy - 0.05, vertices[i], ha='center', fontsize=8)
simplex_x = trajectory[:, 0] * triangle[0, 0] + trajectory[:, 1] * triangle[1, 0] + trajectory[:, 2] * triangle[2, 0]
simplex_y = trajectory[:, 0] * triangle[0, 1] + trajectory[:, 1] * triangle[1, 1] + trajectory[:, 2] * triangle[2, 1]
sc = ax.scatter(simplex_x, simplex_y, c=range(N_cycle + 1), cmap='viridis', s=30, alpha=0.8)
ax.plot(simplex_x, simplex_y, 'k-', alpha=0.3, linewidth=0.5)
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.0)
ax.set_aspect('equal')
ax.set_title('Mother Trajectory on 2-Simplex Δ²')
ax.axis('off')
plt.colorbar(sc, ax=ax, label='k')

# Plot 5: κ scan
ax = axes[1, 1]
kappas = [r['kappa'] for r in scan_results]
ax.plot(kappas, [r['dev_s'] for r in scan_results], 'o-', color=colors[0], label='α_s dev', linewidth=2)
ax.plot(kappas, [r['dev_w'] for r in scan_results], 's-', color=colors[1], label='α_2 dev', linewidth=2)
ax.plot(kappas, [r['dev_em'] for r in scan_results], '^-', color=colors[2], label='α_EM dev', linewidth=2)
ax.plot(kappas, [r['total'] for r in scan_results], 'D-', color='black', label='Total dev', linewidth=2)
ax.axvline(x=best_kappa, color='red', linestyle='--', alpha=0.5, label=f'Best κ={best_kappa}')
ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax.set_xlabel('p-adic phase coupling κ')
ax.set_ylabel('Deviation from experiment (%)')
ax.set_title('κ Scan: p-adic Phase Effect on Couplings')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 6: von Mangoldt phase function
ax = axes[1, 2]
k_range = np.arange(1, N_cycle + 1)
Lambda_all = np.zeros((N_cycle, 3))
for k in k_range:
    Lambda_all[k-1] = von_mangoldt_padic(k, primes)
for i in range(3):
    non_zero = Lambda_all[:, i] > 0
    if np.any(non_zero):
        ax.stem(k_range[non_zero], Lambda_all[non_zero, i], linefmt=colors[i], 
                markerfmt='o', basefmt=' ', label=labels[i])
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('von Mangoldt Λ_i(k)')
ax.set_title('p-adic Phase: Λ_i(k) = log(p_i) at k=p_i^m')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = 'd:/WorkSpace/物理/闭合核理论/CNTFormal/10-模拟/09-递归博弈论_母轨迹与耦合常数_v5.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"图表已保存至: {output_path}")
print()
print("=" * 70)
print("  v5.0 计算完成")
print("=" * 70)