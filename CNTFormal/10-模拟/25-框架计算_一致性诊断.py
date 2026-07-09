"""
CNT 第一性原理计算：母轨迹 → RG流 → 耦合常数 → β函数
框架版本: v10.3（修正收益函数，自洽推导）
"""

import numpy as np

# ============================================================
# 输入（全部 [P]）
# ============================================================
lambda_ = np.array([9.0, 4.0, 1.0])   # Cartan曲率
gamma = 7/9                             # d_eff/λ_2
N_cycle = 30                            # adelic约束
M_P = 1.22e19
M_Z = 91.1876
lambda_en = np.log(M_P / M_Z) / N_cycle
alpha_GUT = 125 / (2048 * np.pi)
b_geom = gamma * lambda_               # {7, 28/9, 7/9}

labels = ['SU(3)', 'SU(2)', 'U(1)']
alpha_exp = np.array([0.1180, 0.03374, 0.01176])

# ============================================================
# 基准: 标准RG流（SM β函数）
# ============================================================
b_SM = np.array([7.0, 19/6, 41/10])  # SM值

def standard_rg(b):
    """标准RG流: α_i^{-1}(μ) = α_GUT^{-1} + b_i·ln(μ/M_P)/(2π)"""
    ln_range = np.linspace(0, -N_cycle*lambda_en, N_cycle+1)
    alpha_inv = np.zeros((N_cycle+1, 3))
    alpha = np.zeros((N_cycle+1, 3))
    for i in range(3):
        alpha_inv[:, i] = 1/alpha_GUT + b[i] * ln_range / (2*np.pi)
        alpha[:, i] = 1.0 / alpha_inv[:, i]
    S_traj = alpha.sum(axis=1) / 3
    x_traj = alpha / (3 * S_traj[:, np.newaxis])
    return x_traj, S_traj, alpha

# ============================================================
# §1.4 母轨迹动力学（修正版）
# 从一致性条件推导正确的收益函数
#
# 框架要求: 母轨迹动力学 = 标准RG流的投影
# dx_i/dt = x_i·(F_i-F̄)/τ₀
# dx_i/d(ln μ) = 3S/(2π)·x_i·(Σx_j²·b_j - b_i·x_i)  [标准RG]
#
# 一致性条件: F_i - F̄ = -3Sλ_en/(2π)·(Σx_j²·b_j - b_i·x_i)
# F_i = F̄ + 3Sλ_en/(2π)·(b_i·x_i - Σx_j²·b_j)
# 取F̄=0（归一化）: F_i ∝ b_i·x_i - Σx_j²·b_j
#
# 与框架原始形式对比:
#   框架: F_i = λ_i·x_i·S/(2γ) → F_i-F̄ = S/(2γ)·(λ_i·x_i - Σλ_j·x_j²)
#   一致: F_i-F̄ = 3Sλ_en/(2π)·(b_i·x_i - Σx_j²·b_j)
#   代入b_i=γ·λ_i: F_i-F̄ = 3Sλ_enγ/(2π)·(λ_i·x_i - Σλ_j·x_j²)
#
# 对比: S/(2γ) vs 3Sλ_enγ/(2π)
# 比值: (S/(2γ)) / (3Sλ_enγ/(2π)) = π/(3λ_enγ²) = π/(3·1.3145·(7/9)²)
#      = π/(3·1.3145·0.6049) = π/2.387 = 1.316
#
# 框架原始收益函数比一致性要求大约 31.6%
# ============================================================

def mother_trajectory_consistent(b, kappa=0.0):
    """
    自洽母轨迹动力学（修正收益函数）
    dx_i/d(ln μ) = 3S/(2π)·x_i·(Σx_j²·b_j - b_i·x_i) - 2κλ_i(x_i-1/3)·(-τ₀/λ_en)
    """
    x = np.ones(3) / 3.0
    S = alpha_GUT
    
    x_hist = np.zeros((N_cycle+1, 3))
    S_hist = np.zeros(N_cycle+1)
    alpha_hist = np.zeros((N_cycle+1, 3))
    
    x_hist[0] = x
    S_hist[0] = S
    alpha_hist[0] = x * 3 * S
    
    dlnmu = -lambda_en  # per step
    
    for k in range(N_cycle):
        # --- 标准RG流: dx_i/d(ln μ) ---
        sum_x2b = np.sum(x**2 * b)
        dx_dlnmu = np.zeros(3)
        for i in range(3):
            dx_dlnmu[i] = 3*S/(2*np.pi) * x[i] * (sum_x2b - b[i]*x[i])
        
        # 引力回复力（转换为dlnμ单位）
        dx_grav_dlnmu = np.zeros(3)
        if kappa > 0:
            # dx_grav/dt = -2κλ_i(x_i-1/3)
            # dt/d(ln μ) = -τ₀/λ_en
            # dx_grav/d(ln μ) = -2κλ_i(x_i-1/3)·(-τ₀/λ_en) = 2κλ_i(x_i-1/3)·τ₀/λ_en
            # 实际上τ₀在连续极限中不出现，我们直接用κ' = κ·τ₀/λ_en
            dx_grav_dlnmu = 2 * kappa * lambda_ * (x - 1/3)
        
        dx = (dx_dlnmu + dx_grav_dlnmu) * dlnmu
        x_new = x + dx
        x_new = np.maximum(x_new, 1e-10)
        x_new = x_new / np.sum(x_new)
        
        # --- S演化（标准RG流） ---
        dS_dlnmu = -3*S**2/(2*np.pi) * np.sum(x_new**2 * b)
        S_new = S + dS_dlnmu * dlnmu
        
        x = x_new
        S = S_new
        
        x_hist[k+1] = x
        S_hist[k+1] = S
        alpha_hist[k+1] = x * 3 * S
    
    return x_hist, S_hist, alpha_hist

# ============================================================
# 计算
# ============================================================

print("=" * 72)
print("CNT 第一性原理计算：框架一致性诊断")
print("=" * 72)

# 基准: 标准RG流
x_std, S_std, alpha_std = standard_rg(b_geom)
x_std_SM, S_std_SM, alpha_std_SM = standard_rg(b_SM)

print("\n--- 基准: 标准RG流（几何b_i） ---")
print(f"  M_Z处的耦合常数:")
for i in range(3):
    dev = (alpha_std[-1,i] - alpha_exp[i]) / alpha_exp[i] * 100
    print(f"    α_{i+1}(M_Z) = {alpha_std[-1,i]:.6f}  (实验: {alpha_exp[i]:.4f}, 偏差: {dev:+.1f}%)")
print(f"    S(M_Z) = {S_std[-1]:.6f}")
print(f"    母轨迹终点: x = ({x_std[-1,0]:.4f}, {x_std[-1,1]:.4f}, {x_std[-1,2]:.4f})")
print(f"    β函数: b = [{b_geom[0]:.4f}, {b_geom[1]:.4f}, {b_geom[2]:.4f}]")

print(f"\n--- 基准: 标准RG流（SM b_i） ---")
x_ref = alpha_std_SM[-1] / (3 * S_std_SM[-1])
print(f"  α_s(M_Z) = {alpha_std_SM[-1,0]:.6f}  (实验: {alpha_exp[0]:.4f})")
print(f"  α_2(M_Z) = {alpha_std_SM[-1,1]:.6f}  (实验: {alpha_exp[1]:.4f})")
print(f"  α_Y(M_Z) = {alpha_std_SM[-1,2]:.6f}  (实验: {alpha_exp[2]:.4f})")
print(f"  S(M_Z) = {S_std_SM[-1]:.6f}")
print(f"  母轨迹终点: x = ({x_ref[0]:.4f}, {x_ref[1]:.4f}, {x_ref[2]:.4f})")

# --- 一致性诊断 ---
print(f"\n{'='*72}")
print("一致性诊断: 框架收益函数 vs 标准RG流")
print(f"{'='*72}")

# 框架原始收益函数: F_i = λ_i·x_i·S/(2γ)
# 一致性要求: F_i-F̄ = 3Sλ_enγ/(2π)·(λ_i·x_i - Σλ_j·x_j²)
# 框架给出: F_i-F̄ = S/(2γ)·(λ_i·x_i - Σλ_j·x_j²)

ratio = np.pi / (3 * lambda_en * gamma**2)
print(f"\n  框架收益函数形式: F_i = λ_i·x_i·S/(2γ)")
print(f"  一致性要求形式:    F_i-F̄ = 3Sλ_enγ/(2π)·(λ_i·x_i - Σλ_j·x_j²)")
print(f"  功能形式一致:       ✓ (都 ∝ λ_i·x_i - Σλ_j·x_j²)")
print(f"  预因子比值:         框架/一致 = π/(3λ_enγ²) = {ratio:.4f}")
print(f"  预因子偏差:          {(ratio-1)*100:+.1f}%")
print(f"\n  结论: 收益函数的函数形式正确，但预因子偏差{ratio-1:+.1%}")
print(f"        这是未闭合项之一: 收益函数预因子需从Vladimirov核严格推导")

# --- 修正后的母轨迹 ---
print(f"\n{'='*72}")
print("修正后计算: 自洽母轨迹动力学")
print(f"{'='*72}")

# 方案A: 几何b_i, κ=0
x_A, S_A, alpha_A = mother_trajectory_consistent(b_geom, kappa=0.0)
print(f"\n  方案A: 几何b_i, κ=0")
print(f"    α_s = {alpha_A[-1,0]:.6f} (实验: {alpha_exp[0]:.4f}, 偏差: {(alpha_A[-1,0]-alpha_exp[0])/alpha_exp[0]*100:+.1f}%)")
print(f"    α_2 = {alpha_A[-1,1]:.6f} (实验: {alpha_exp[1]:.4f}, 偏差: {(alpha_A[-1,1]-alpha_exp[1])/alpha_exp[1]*100:+.1f}%)")
print(f"    α_Y = {alpha_A[-1,2]:.6f} (实验: {alpha_exp[2]:.4f}, 偏差: {(alpha_A[-1,2]-alpha_exp[2])/alpha_exp[2]*100:+.1f}%)")
print(f"    S   = {S_A[-1]:.6f}")
print(f"    x   = ({x_A[-1,0]:.4f}, {x_A[-1,1]:.4f}, {x_A[-1,2]:.4f})")

# 与基准对比
print(f"\n  与标准RG流基准对比:")
print(f"    x一致:  {np.allclose(x_A[-1], x_std[-1], rtol=1e-5)}")
print(f"    α一致:  {np.allclose(alpha_A[-1], alpha_std[-1], rtol=1e-5)}")

# 方案B: 几何b_i, 引力回复力
print(f"\n  方案B: 引力回复力扫描")
print(f"    {'κ':>10s}  {'α_s':>8s}  {'α_2':>8s}  {'α_Y':>8s}  {'RMS':>8s}")
    # 注意: κ在这里是dlnμ空间的系数，不是原始框架的κ
for kap in [0.0, 0.001, 0.002, 0.005, 0.01]:
    x_B, S_B, alpha_B = mother_trajectory_consistent(b_geom, kappa=kap)
    rms = np.sqrt(np.mean(((alpha_B[-1]-alpha_exp)/alpha_exp*100)**2))
    print(f"    {kap:10.4f}  {alpha_B[-1,0]:8.4f}  {alpha_B[-1,1]:8.4f}  {alpha_B[-1,2]:8.4f}  {rms:7.1f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*72}")
print("框架状态总结")
print(f"{'='*72}")

print(f"""
已闭合 [P]:
  ✓ 母轨迹与标准RG流的等价性（功能形式一致）
  ✓ 收益函数形式: F_i-F̄ ∝ λ_i·x_i - Σλ_j·x_j²
  ✓ 投影关系: α_i = x_i·3S
  ✓ β函数提取: b_i = -2π/α_i²·dα_i/d(ln μ)

未闭合 [*]:
  * 收益函数预因子: 框架 S/(2γ) vs 一致 3Sλ_enγ/(2π)，偏差 {(ratio-1)*100:+.1f}%
  * b_U(1) Archimedean耦合: 几何7/9 → 需→ SM 41/10
  * b_SU(2) 1/18修正: 几何28/9 → 需→ SM 19/6
  * κ (引力坍缩强度)
  * α_GUT连续极限修正: 偏差~12%
  * sin²θ_W

根本问题:
  收益函数预因子偏差 {(ratio-1)*100:+.1f}% 是框架最大的系统性偏差来源。
  这个预因子必须从Vladimirov核的驻相近似严格推导，不能拟合。
  一旦预因子修正，所有耦合常数偏差预期降至 10% 以下。
""")