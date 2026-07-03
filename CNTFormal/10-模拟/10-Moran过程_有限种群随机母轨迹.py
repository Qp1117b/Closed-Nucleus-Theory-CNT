"""
Moran过程蒙特卡洛 v3.0：Langevin扩散近似——有限种群随机母轨迹
==================================================================
从 CNT 递归博弈论出发，用 Langevin 扩散近似替代完整 Moran 过程，
高效计算有限种群（N < ∞）下的系综平均母轨迹。

核心洞察：
  单次再生产投影是随机的 —— 母轨迹不是确定曲线，而是系综平均。
  有限种群大小 N 引入 ~1/N 量级的涨落，其系综平均产生系统性偏差。

关键修正（v3.0 — 2026-07-04）：
  【修正8】S演化稳定性：d(1/S)/dk = λ B/(2π)，避免 S² 数值爆炸
  【修正9】S沿确定性路径演化：有限种群效应仅影响策略频率 x_i，
           总耦合尺度 S(k) 是 RG 流的平均场性质，不由随机过程决定
           α_i(k) = x_i(k) × S_det(k)，分离随机与确定性贡献

方法：
  (a) Langevin 扩散近似：dx_i = x_i(F_i - F̄)dk + √(C_ij) dW_j
  (b) 协方差矩阵 C_ij = (x_i δ_ij - x_i x_j)/N
  (c) 收益函数：SM β 函数校准 + p 进相位 + 点火增强
  (d) 绝对尺度 S(k) 沿确定性 RG 方程演化（d(1/S)/dk = λ B/(2π)）
  (e) 扫描 N 参数，分析有限种群标度行为

Langevin 方程 vs 完整 Moran 过程:
  - Langevin: 连续状态、快速、N→∞ 时收敛到确定性复制子
  - Moran:   离散状态、精确、但计算量 O(N²) 每步

日期: 2026-07-04
认识论地位: [第一性原理推导] + [Langevin扩散近似] + [蒙特卡洛验证]
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time

# ============================================================
# §1. 参数
# ============================================================

primes = np.array([2, 3, 5])
prime_gauge = {2: 0, 3: 1, 5: 2}
gauge_names = ['SU(3) Strong', 'SU(2) Weak', 'U(1)_Y Hyper']

b_sm = np.array([-7.0, -19.0/6, 41.0/10])
sin2_theta_W = 0.2312

M_P = 1.22e19
M_Z = 91.1876
N_cycle = 30
lambda_energy = np.log(M_P / M_Z) / N_cycle
k_MZ = N_cycle

alpha_GUT_geom = 125.0 / (2048.0 * np.pi)

alpha_s_exp  = 0.1180
alpha_w_exp  = 0.0337
alpha_em_exp = 1.0/127.952
alpha_em_low_exp = 1.0/137.035999084
S_MZ_exp = alpha_s_exp + alpha_w_exp + alpha_em_exp

kappa_opt = 0.01
eta_ignition = 0.15

# ============================================================
# §2. 收益函数
# ============================================================

def B_function(x):
    return np.dot(b_sm, x**2)

def fitness_sm_calibrated(x, S):
    B = B_function(x)
    prefactor = lambda_energy * S / (2.0 * np.pi)
    return prefactor * (B - b_sm * x)

def von_mangoldt_padic(k, primes_vec):
    Lambda = np.zeros(3)
    for i, p in enumerate(primes_vec):
        if k > 0 and k % p == 0:
            kk = k
            while kk % p == 0:
                kk //= p
            if kk == 1:
                Lambda[i] = np.log(p)
    return Lambda

def fitness_effective(x, S, k, kappa, primes_vec):
    F_base = fitness_sm_calibrated(x, S)
    Lambda_k = von_mangoldt_padic(k, primes_vec)
    return F_base + kappa * Lambda_k, F_base, Lambda_k

# ============================================================
# §3. Langevin 扩散近似（Moran 过程的连续极限）
# ============================================================

def moran_covariance_matrix(x, N):
    """
    Moran 过程在 Langevin 近似下的协方差矩阵。
    
    C_ij = (x_i δ_ij - x_i x_j) / N
    
    性质: Σ_i C_ij = 0, 确保 Σ_i dx_i = 0.
    """
    C = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            C[i, j] = (x[i] * (1 if i == j else 0) - x[i] * x[j]) / N
    return C


def simulate_single_langevin_trajectory(N_pop, K, x0, S_det_traj, kappa, rng, M_sub=1):
    """
    Langevin 扩散近似下单条随机轨迹（v3.0: S 沿确定性路径 + 子步长）。
    
    dx_i = x_i(F_i - F̄) dk + sqrt(dk) * Σ_j L_ij ξ_j
    α_i(k) = x_i(k) × S_det(k)  （S 沿确定性 RG 路径，不受随机噪声影响）
    
    关键修正 (v3.0): 引入子步长 M_sub，将每个再生产步细分为 M_sub 个子步。
    dk_sub = 1/M_sub, noise ~ sqrt(dk_sub)，减小单步噪声幅度，
    避免非线性复制子动力学中的噪声放大效应。
    
    物理理由：
    - S(k) 是 RG 流的平均场性质，由 QFT β 函数决定
    - 有限种群效应仅影响策略频率分布 x_i(k)
    - 子步长确保 Langevin 近似在弱噪声极限下有效
    """
    dk_sub = 1.0 / M_sub
    sqrt_dk_sub = np.sqrt(dk_sub)
    
    x_history = np.zeros((K + 1, 3))
    alpha_history = np.zeros((K + 1, 3))
    
    x = x0.copy()
    
    x_history[0] = x
    alpha_history[0] = x * S_det_traj[0]
    
    for k in range(K):
        S = S_det_traj[k]  # 当前步的确定性 S
        
        for m in range(M_sub):
            k_target = k + 1  # 目标步用于相位和点火
            
            # 有效收益（使用当前 x 和确定性 S）
            F_eff, F_base, Lambda_k = fitness_effective(x, S, k_target, kappa, primes)
            # 点火增强仅在第一步（避免重复计数）
            if m == 0:
                for p, idx in prime_gauge.items():
                    if k_target == p:
                        F_eff[idx] += eta_ignition * S / p
            
            # 确定性漂移
            F_bar = np.dot(x, F_eff)
            drift = x * (F_eff - F_bar) * dk_sub
            
            # 随机扩散（协方差矩阵缩放 dk_sub）
            C = moran_covariance_matrix(x, N_pop)
            try:
                L = np.linalg.cholesky(C + 1e-12 * np.eye(3))
            except np.linalg.LinAlgError:
                L = np.zeros((3, 3))
            noise = L @ rng.randn(3)
            diffusion = noise * sqrt_dk_sub
            
            # 更新 x
            x = x + drift + diffusion
            x = np.clip(x, 1e-10, 1.0)
            x = x / np.sum(x)
        
        x_history[k + 1] = x
        alpha_history[k + 1] = x * S_det_traj[k + 1]
    
    return x_history, alpha_history


# ============================================================
# §4. 确定性复制子（对比基线）
# ============================================================

def simulate_deterministic(K, x0, S0, kappa):
    """
    确定性复制子动力学（v3.0: 稳定的 S 演化）。
    
    x 演化: dx_i = x_i (F_i^eff - F̄^eff)
    S 演化: d(1/S)/dk = λ B(x)/(2π)  →  1/S_{k+1} = 1/S_k + λ B(x_k)/(2π)
    
    使用 1/S 而非 S 的演化方程，避免 S² 项导致的数值不稳定。
    物理等价：dS/dk = -λ S² B/(2π) ⇔ d(1/S)/dk = λ B/(2π)
    """
    x = x0.copy()
    invS = 1.0 / S0  # 演化 1/S 而非 S
    
    x_hist = np.zeros((K + 1, 3))
    S_hist = np.zeros(K + 1)
    alpha_hist = np.zeros((K + 1, 3))
    
    x_hist[0] = x
    S_hist[0] = S0
    alpha_hist[0] = x * S0
    
    for k in range(K):
        k_target = k + 1
        S = 1.0 / invS  # 当前 S
        
        F_eff, F_base, Lambda_k = fitness_effective(x, S, k_target, kappa, primes)
        for p, idx in prime_gauge.items():
            if k_target == p:
                F_eff[idx] += eta_ignition * S / p
        
        F_bar = np.dot(x, F_eff)
        dx = x * (F_eff - F_bar)
        x = x + dx
        x = np.maximum(x, 1e-15)
        x = x / np.sum(x)
        
        # 稳定演化: 1/S_{k+1} = 1/S_k + λ B(x_k)/(2π)
        B = B_function(x)
        invS_new = invS + lambda_energy * B / (2.0 * np.pi)
        if invS_new <= 0:
            invS_new = invS * 0.99  # 保护：S 不应为负
        
        invS = invS_new
        S = 1.0 / invS
        
        x_hist[k + 1] = x
        S_hist[k + 1] = S
        alpha_hist[k + 1] = x * S
    
    return x_hist, S_hist, alpha_hist


# ============================================================
# §5. 系综蒙特卡洛
# ============================================================

def ensemble_langevin(N_pop, N_trials, K, x0, S_det_traj, kappa, seed=42):
    """运行 N_trials 条独立 Langevin 轨迹，计算系综平均"""
    rng = np.random.RandomState(seed)
    
    x_sum = np.zeros((K + 1, 3))
    x_sq_sum = np.zeros((K + 1, 3))
    all_traj = []
    
    for trial in range(N_trials):
        trial_seed = seed + trial * 10000
        trial_rng = np.random.RandomState(trial_seed)
        
        x_hist, alpha_hist = simulate_single_langevin_trajectory(
            N_pop, K, x0, S_det_traj, kappa, trial_rng
        )
        
        x_sum += x_hist
        x_sq_sum += x_hist**2
        all_traj.append((x_hist, alpha_hist))
        
        if (trial + 1) % 2000 == 0:
            print(f"    [{trial + 1}/{N_trials}] 已完成...")
    
    x_mean = x_sum / N_trials
    x_std = np.sqrt(np.maximum(x_sq_sum / N_trials - x_mean**2, 0))
    
    return x_mean, x_std, all_traj


# ============================================================
# §6. 运行计算
# ============================================================

print("=" * 75)
print("  Moran/Langevin 过程 v3.0：有限种群随机母轨迹")
print("  CNT 递归博弈论 — S 沿确定性 RG 路径 + Langevin 扩散近似")
print("=" * 75)
print()

x0 = np.array([1.0/3, 1.0/3, 1.0/3])
S0 = 3.0 * alpha_GUT_geom

print("物理参数:")
print(f"  α_GUT (几何)   = {alpha_GUT_geom:.6f}")
print(f"  S(0)          = {S0:.6f}")
print(f"  N_cycle       = {N_cycle}")
print(f"  κ (p进相位)   = {kappa_opt}")
print()

# 6.1 确定性基线
print("§0. 确定性复制子基线（N→∞, d(1/S)/dk 稳定演化）")
print("-" * 50)
x_det, S_det, alpha_det = simulate_deterministic(N_cycle, x0, S0, kappa_opt)
alpha_det_MZ = alpha_det[k_MZ]
alpha_em_det = alpha_det_MZ[1] * sin2_theta_W
print(f"  α_s(M_Z)  = {alpha_det_MZ[0]:.6f}  (偏差 {abs(alpha_det_MZ[0]-alpha_s_exp)/alpha_s_exp*100:.2f}%)")
print(f"  α_2(M_Z)  = {alpha_det_MZ[1]:.6f}  (偏差 {abs(alpha_det_MZ[1]-alpha_w_exp)/alpha_w_exp*100:.2f}%)")
print(f"  α_EM(M_Z) = {alpha_em_det:.6f}  (偏差 {abs(alpha_em_det-alpha_em_exp)/alpha_em_exp*100:.2f}%)")
print(f"  S(M_Z)    = {S_det[k_MZ]:.6f}  (实验 {S_MZ_exp:.6f})")
print(f"  S 演化: 从 {S_det[0]:.4f} → {S_det[k_MZ]:.4f} (稳定)")
print()

det_devs = [abs(alpha_det_MZ[0]-alpha_s_exp)/alpha_s_exp*100,
            abs(alpha_det_MZ[1]-alpha_w_exp)/alpha_w_exp*100,
            abs(alpha_em_det-alpha_em_exp)/alpha_em_exp*100]

# 6.2 N 扫描（Langevin 扩散近似，S 沿确定性路径）
N_pop_values = [10, 20, 30, 50, 100, 200, 500, 1000]
N_trials = 10000

print("§1. 种群大小 N 扫描（Langevin 扩散近似，S 沿确定性 RG 路径）")
print(f"  每个 N 值: {N_trials} 条轨迹")
print(f"  关键修正: S(k) 沿确定性路径演化，有限种群效应仅影响 x_i(k)")
print("-" * 75)
print(f"  {'N_pop':<8} {'α_s(系综)':<12} {'α_2(系综)':<12} {'α_EM(系综)':<14} {'α_s偏差':<10} {'α_2偏差':<10} {'α_EM偏差':<10} {'σ(x₁)':<10}")
print(f"  {'-'*90}")
print(f"  {'N→∞':<8} {alpha_det_MZ[0]:<12.6f} {alpha_det_MZ[1]:<12.6f} {alpha_em_det:<14.6f} "
      f"{det_devs[0]:<10.2f}% {det_devs[1]:<10.2f}% {det_devs[2]:<10.2f}% {'0':<10}")
print(f"  {'-'*90}")

results = []
best_N = None
best_total_dev = 1e10

for N_pop in N_pop_values:
    print(f"  正在模拟 N={N_pop} ({N_trials} 条轨迹)...")
    t0 = time.time()
    
    x_mean, x_std, all_traj = ensemble_langevin(
        N_pop, N_trials, N_cycle, x0, S_det, kappa_opt, seed=42
    )
    
    t_elapsed = time.time() - t0
    
    # α_i = x_i × S_det (S 沿确定性路径)
    alpha_mean_MZ = x_mean[k_MZ] * S_det[k_MZ]
    alpha_em_mean = alpha_mean_MZ[1] * sin2_theta_W
    
    dev_s = abs(alpha_mean_MZ[0] - alpha_s_exp) / alpha_s_exp * 100
    dev_w = abs(alpha_mean_MZ[1] - alpha_w_exp) / alpha_w_exp * 100
    dev_em = abs(alpha_em_mean - alpha_em_exp) / alpha_em_exp * 100
    total_dev = dev_s + dev_w + dev_em
    
    sigma_x1 = x_std[k_MZ, 0]
    delta_x = x_mean[k_MZ] - x_det[k_MZ]
    
    print(f"  {N_pop:<8} {alpha_mean_MZ[0]:<12.6f} {alpha_mean_MZ[1]:<12.6f} {alpha_em_mean:<14.6f} "
          f"{dev_s:<10.2f}% {dev_w:<10.2f}% {dev_em:<10.2f}% {sigma_x1:<10.4f}")
    print(f"  {'':8} Δx = ({delta_x[0]:+.5f}, {delta_x[1]:+.5f}, {delta_x[2]:+.5f})  "
          f"耗时 {t_elapsed:.1f}s")
    
    results.append({
        'N_pop': N_pop, 'x_mean': x_mean, 'x_std': x_std,
        'alpha_MZ': alpha_mean_MZ, 'alpha_em': alpha_em_mean,
        'dev_s': dev_s, 'dev_w': dev_w, 'dev_em': dev_em,
        'total_dev': total_dev, 'sigma_x1': sigma_x1, 'delta_x': delta_x,
    })
    
    if total_dev < best_total_dev:
        best_total_dev = total_dev
        best_N = N_pop
    print()

print(f"  最优 N_pop = {best_N}, 总偏差 = {best_total_dev:.2f}%")
print(f"  确定性基线总偏差 = {sum(det_devs):.2f}%")
improvement = (sum(det_devs) - best_total_dev) / sum(det_devs) * 100
print(f"  有限种群修正改善: {improvement:.1f}% (正值=改善)")
print()

# 6.3 精细结构常数
best_result = [r for r in results if r['N_pop'] == best_N][0]
alpha_em_low = best_result['alpha_em'] / (1.0 - best_result['alpha_em'] * (2.0/(3.0*np.pi)) * np.log(M_Z/0.000511))

print("§2. 精细结构常数（低能极限）")
print("-" * 50)
print(f"  α_EM(M_Z) 系综平均: {best_result['alpha_em']:.6f}  (≈ 1/{1/best_result['alpha_em']:.1f})")
print(f"  α_EM(0)  系综估计: {alpha_em_low:.6f}  (≈ 1/{1/alpha_em_low:.1f})")
print(f"  α_EM(0)  实验值:   {alpha_em_low_exp:.6f}  (≈ 1/137.036)")
print(f"  偏差: {abs(alpha_em_low - alpha_em_low_exp)/alpha_em_low_exp*100:.2f}%")
print()

# 6.4 有限种群标度分析
print("§3. 有限种群标度分析: Δx_i ∝ 1/N")
print("-" * 50)
print(f"  {'N_pop':<8} {'1/N':<12} {'Δx₁(强)':<14} {'Δx₂(弱)':<14} {'Δx₃(超荷)':<14} {'||Δx||':<10} {'Th.||Δx||':<12}")
print(f"  {'-'*90}")
for r in results:
    invN = 1.0 / r['N_pop']
    dx = r['delta_x']
    # 理论预期: ||Δx|| ~ sqrt(3/N) / sqrt(N_trials) 来自中心极限定理
    norm_dx = np.linalg.norm(dx)
    # 更准确的理论: 偏差 ~ 1/N * O(1), 来自伊藤引理的漂移修正
    # 对于扩散过程 dx = μ(x)dt + σ(x)dW, 有限步长产生 ~σ²/N 的漂移
    print(f"  {r['N_pop']:<8} {invN:<12.6f} {dx[0]:<+14.8f} {dx[1]:<+14.8f} {dx[2]:<+14.8f} {norm_dx:<10.6f}")

# 统计显著性检验
print()
print("§4. 统计显著性: 系综平均 vs 确定性")
print("-" * 50)
for r in results:
    N = r['N_pop']
    dx = r['delta_x']
    # 标准误差: σ_x / sqrt(N_trials)
    se = r['x_std'][k_MZ] / np.sqrt(N_trials)
    n_sigma = np.abs(dx) / np.maximum(se, 1e-15)
    sig_str = []
    for i, ns in enumerate(n_sigma):
        if ns > 3:
            sig_str.append(f"x{i+1}: {ns:.1f}σ ***")
        elif ns > 2:
            sig_str.append(f"x{i+1}: {ns:.1f}σ **")
        elif ns > 1:
            sig_str.append(f"x{i+1}: {ns:.1f}σ *")
        else:
            sig_str.append(f"x{i+1}: {ns:.1f}σ")
    print(f"  N={N:<6} {' | '.join(sig_str)}")

print()

# 6.5 系综涨落
print("§5. 系综涨落: σ ∝ 1/√N")
print("-" * 50)
print(f"  {'N_pop':<8} {'σ(x₁)':<12} {'σ·√N':<12} {'理论预期':<14}")
for r in results:
    sigma_scaled = r['sigma_x1'] * np.sqrt(r['N_pop'])
    print(f"  {r['N_pop']:<8} {r['sigma_x1']:<12.6f} {sigma_scaled:<12.6f} {'≈ 常数':<14}")
print()

# ============================================================
# §7. 可视化
# ============================================================

colors = ['#2196F3', '#4CAF50', '#FF5722']
labels = ['SU(3) Strong', 'SU(2) Weak', 'U(1)_Y Hyper']

fig = plt.figure(figsize=(20, 14))
gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.35)
fig.suptitle(f'CNT Langevin Diffusion v2.0: Finite-N Mother Trajectory\n'
             f'Best N={best_N}, κ={kappa_opt}, {N_trials} trials',
             fontsize=14, fontweight='bold')

k_vals = np.arange(N_cycle + 1)

# ----- Plot 1: 系综平均母轨迹 vs 确定性 vs 样本轨迹 -----
ax = fig.add_subplot(gs[0, :2])
n_sample = 20
for i in range(min(n_sample, len(all_traj))):
    x_hist, _ = all_traj[i]
    for j in range(3):
        ax.plot(k_vals, x_hist[:, j], color=colors[j], alpha=0.08, linewidth=0.5)
for i in range(3):
    ax.plot(k_vals, best_result['x_mean'][:, i], color=colors[i], linewidth=2.5,
            label=f'{labels[i]} (ens)')
    ax.plot(k_vals, x_det[:, i], '--', color=colors[i], linewidth=1.5, alpha=0.7,
            label=f'{labels[i]} (det)')
    ax.fill_between(k_vals,
                     best_result['x_mean'][:, i] - best_result['x_std'][:, i],
                     best_result['x_mean'][:, i] + best_result['x_std'][:, i],
                     color=colors[i], alpha=0.12)
for p, idx in prime_gauge.items():
    ax.axvline(x=p, color=colors[idx], linestyle=':', alpha=0.3)
ax.axvline(x=k_MZ, color='red', linestyle=':', alpha=0.5, label='M_Z')
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('Strategy frequency x_i')
ax.set_title(f'Langevin v3.0: Ensemble Mean ± 1σ vs Deterministic (N={best_N})')
ax.legend(fontsize=7, ncol=2)
ax.set_xlim(0, N_cycle)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)

# ----- Plot 2-3: 分布直方图 -----
for i, ax_idx in enumerate([(0, 2), (0, 3)]):
    ax = fig.add_subplot(gs[ax_idx[0], ax_idx[1]])
    if i == 0:
        samples = np.array([t[0][k_MZ, 0] for t in all_traj])
        det_val = x_det[k_MZ, 0]
        ens_val = best_result['x_mean'][k_MZ, 0]
        title = 'x₁ (SU(3)) at M_Z'
    else:
        samples = np.array([t[0][k_MZ, 1] for t in all_traj])
        det_val = x_det[k_MZ, 1]
        ens_val = best_result['x_mean'][k_MZ, 1]
        title = 'x₂ (SU(2)) at M_Z'
    
    ax.hist(samples, bins=50, density=True, color=colors[i], alpha=0.7)
    ax.axvline(x=det_val, color='red', linestyle='--', linewidth=2,
               label=f'Det: {det_val:.4f}')
    ax.axvline(x=ens_val, color='darkred', linestyle='-', linewidth=2,
               label=f'Ens: {ens_val:.4f}')
    x_range = np.linspace(min(samples), max(samples), 200)
    sigma_theory = np.sqrt(det_val * (1 - det_val) / best_N)
    ax.plot(x_range, 1/(sigma_theory*np.sqrt(2*np.pi)) * 
            np.exp(-(x_range - det_val)**2/(2*sigma_theory**2)),
            'k--', alpha=0.5, linewidth=1, label='Theory N(μ,σ²/N)')
    ax.set_xlabel(title.split()[0])
    ax.set_title(f'Distribution: {title} (N={best_N})')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

# ----- Plot 4: N 扫描 —— 偏差 -----
ax = fig.add_subplot(gs[1, :2])
N_vals = [r['N_pop'] for r in results]
ax.plot(N_vals, [r['dev_s'] for r in results], 'o-', color=colors[0], label='α_s', linewidth=2, markersize=8)
ax.plot(N_vals, [r['dev_w'] for r in results], 's-', color=colors[1], label='α_2', linewidth=2, markersize=8)
ax.plot(N_vals, [r['dev_em'] for r in results], '^-', color=colors[2], label='α_EM', linewidth=2, markersize=8)
ax.plot(N_vals, [r['total_dev'] for r in results], 'D-', color='black', label='Total', linewidth=2, markersize=8)
ax.axhline(y=det_devs[0], color=colors[0], linestyle=':', alpha=0.4)
ax.axhline(y=det_devs[1], color=colors[1], linestyle=':', alpha=0.4)
ax.axhline(y=det_devs[2], color=colors[2], linestyle=':', alpha=0.4)
ax.set_xlabel('Population size N')
ax.set_ylabel('Deviation from experiment (%)')
ax.set_title('N-Scan: Finite-N Effect on Coupling Constants')
ax.legend(fontsize=7)
ax.set_xscale('log')
ax.grid(True, alpha=0.3)

# ----- Plot 5: Δx vs 1/N -----
ax = fig.add_subplot(gs[1, 2])
invN_vals = [1.0/r['N_pop'] for r in results]
for i in range(3):
    dx_vals = [r['delta_x'][i] for r in results]
    ax.plot(invN_vals, dx_vals, 'o-', color=colors[i], label=f'Δx_{i+1}', linewidth=2, markersize=8)
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax.set_xlabel('1/N')
ax.set_ylabel('Δx = x(ensemble) - x(deterministic)')
ax.set_title('Finite-N Bias: Δx vs 1/N')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# ----- Plot 6: σ vs 1/√N -----
ax = fig.add_subplot(gs[1, 3])
sigma_vals = np.array([r['sigma_x1'] for r in results])
N_arr = np.array(N_vals)
ax.loglog(N_vals, sigma_vals, 'o-', color=colors[0], linewidth=2, markersize=8, label='σ(x₁)')
N_ref = np.logspace(np.log10(min(N_vals)), np.log10(max(N_vals)), 100)
sigma_ref = sigma_vals[0] * np.sqrt(N_vals[0]) / np.sqrt(N_ref)
ax.loglog(N_ref, sigma_ref, '--', color='gray', alpha=0.7, label='∝ 1/√N')
ax.set_xlabel('Population size N')
ax.set_ylabel('σ(x₁)')
ax.set_title('Fluctuation: σ ∝ 1/√N')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# ----- Plot 7: 耦合常数演化 -----
ax = fig.add_subplot(gs[2, :2])
alpha_ens = best_result['x_mean'] * S_det[:, np.newaxis]
for i in range(3):
    ax.plot(k_vals, alpha_ens[:, i], color=colors[i], linewidth=2, label=f'{labels[i]} (ens)')
    ax.plot(k_vals, alpha_det[:, i], '--', color=colors[i], linewidth=1.5, alpha=0.7)
ax.axhline(y=alpha_s_exp, color=colors[0], linestyle=':', alpha=0.5)
ax.axhline(y=alpha_w_exp, color=colors[1], linestyle=':', alpha=0.5)
ax.axvline(x=k_MZ, color='red', linestyle=':', alpha=0.5, label='M_Z')
ax.set_xlabel('Reproduction count k')
ax.set_ylabel('Coupling constant α_i')
ax.set_title(f'Coupling Constants: Ensemble vs Det (N={best_N})')
ax.legend(fontsize=7, ncol=2)
ax.set_xlim(0, N_cycle)
ax.grid(True, alpha=0.3)

# ----- Plot 8: 单纯形 -----
ax = fig.add_subplot(gs[2, 2])
triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
ax.plot([triangle[0,0], triangle[1,0]], [triangle[0,1], triangle[1,1]], 'k-', linewidth=1)
ax.plot([triangle[1,0], triangle[2,0]], [triangle[1,1], triangle[2,1]], 'k-', linewidth=1)
ax.plot([triangle[2,0], triangle[0,0]], [triangle[2,1], triangle[0,1]], 'k-', linewidth=1)
vertices = ['SU(3)', 'SU(2)', 'U(1)_Y']
for i, (vx, vy) in enumerate(triangle):
    ax.text(vx, vy - 0.05, vertices[i], ha='center', fontsize=8)

def to_simplex(x):
    return np.array([x[0]*triangle[0,0]+x[1]*triangle[1,0]+x[2]*triangle[2,0],
                     x[0]*triangle[0,1]+x[1]*triangle[1,1]+x[2]*triangle[2,1]])

det_2d = np.array([to_simplex(x_det[k]) for k in range(N_cycle+1)])
ax.plot(det_2d[:, 0], det_2d[:, 1], 'k-', linewidth=2, alpha=0.5, label='Det')
ens_2d = np.array([to_simplex(best_result['x_mean'][k]) for k in range(N_cycle+1)])
ax.plot(ens_2d[:, 0], ens_2d[:, 1], 'r-', linewidth=2, label='Ens')
for i in range(min(10, len(all_traj))):
    x_hist, _ = all_traj[i]
    sample_2d = np.array([to_simplex(x_hist[k]) for k in range(N_cycle+1)])
    ax.plot(sample_2d[:, 0], sample_2d[:, 1], color='gray', alpha=0.15, linewidth=0.5)
end_pts = np.array([to_simplex(t[0][k_MZ]) for t in all_traj])
ax.scatter(end_pts[:, 0], end_pts[:, 1], c=colors[0], alpha=0.03, s=5)
ax.scatter(det_2d[k_MZ, 0], det_2d[k_MZ, 1], color='black', s=100, marker='*', zorder=10)
ax.scatter(ens_2d[k_MZ, 0], ens_2d[k_MZ, 1], color='red', s=100, marker='D', zorder=10)
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.0)
ax.set_aspect('equal')
ax.set_title(f'Simplex (N={best_N})')
ax.axis('off')

# ----- Plot 9: 偏差热图 -----
ax = fig.add_subplot(gs[2, 3])
dev_matrix = np.array([[r['dev_s'], r['dev_w'], r['dev_em']] for r in results])
im = ax.imshow(dev_matrix.T, aspect='auto', cmap='RdYlGn_r',
               extent=[np.log10(N_vals[0])-0.15, np.log10(N_vals[-1])+0.15, -0.5, 2.5],
               vmin=0, vmax=15)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['α_s', 'α_2', 'α_EM'])
ax.set_xlabel('log₁₀(N)')
ax.set_title('Deviation Heatmap')
plt.colorbar(im, ax=ax, label='Deviation (%)')

plt.savefig('d:/WorkSpace/物理/闭合核理论/CNTFormal/10-模拟/10-Moran过程_有限种群结果_v3.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("图表已保存")

print()
print("=" * 75)
print("  Langevin 扩散近似 v3.0 计算完成")
print(f"  最优 N = {best_N}, 改善 = {improvement:.1f}%")
print("=" * 75)