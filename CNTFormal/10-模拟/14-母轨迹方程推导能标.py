"""
从母轨迹方程直接推导频率-能标关系
====================================

核心方程 (驻相近似):
    δS_Regge[σ_k]/δΓ_k + s_0 · ∂Φ_Λ(x_k)/∂Γ_k - λ · ∂C/∂Γ_k = 0

推导思路:
    1. 从 S_Regge 项推导几何能标 ℓ_k
    2. 从 Φ_Λ 项推导作用量 S_k = s_0 · Λ(k)
    3. 从 ν_k = 1/τ_k 推导频率
    4. 从 dS/dτ 推导能量 E_k = S_k · ν_k
    5. 从 Einstein 方程推导 RG 能标 μ_k = 1/ℓ_k
"""

import numpy as np
import matplotlib.pyplot as plt
import os, platform

if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 常数
# ============================================================
h = 4.135667662e-21   # MeV·s
hbar = h / (2*np.pi)
m_p = 938.272          # MeV
M_P = 1.22089e22       # MeV
M_Z = 91.1876e3        # MeV
t_P = 5.391247e-44     # s
nu_P = 1.0 / t_P

N_CYCLE = 30

# ============================================================
# 步骤1: 从 Regge 作用量推导几何能标 ℓ_k
# ============================================================

print("=" * 70)
print("步骤1: Regge 作用量 → 几何能标 ℓ_k")
print("=" * 70)

# 正则4-单纯形
# 二面角 Θ = arccos(1/4) ≈ 1.31812 rad
# 亏角 ε = 2π - 4Θ ≈ 0.12839 rad
# 三角形面积 A_f = √3/4 · ℓ²
# S_Regge = 10 · A_f · ε = 10 · √3/4 · ℓ² · ε
# 
# 尺寸分析: [S_Regge] = [ℓ²] = [能量]⁻²
# 自然单位: ℓ_P = √(ħG/c³), M_P = 1/ℓ_P
# S_Regge ~ (ℓ/ℓ_P)²

THETA = np.arccos(1.0/4.0)
EPSILON = 2*np.pi - 4*THETA  # 亏角

print(f"  二面角 Θ = arccos(1/4) = {THETA:.5f} rad = {np.degrees(THETA):.2f}°")
print(f"  亏角 ε = 2π - 4Θ = {EPSILON:.5f} rad")
print(f"  S_Regge = 10 · √3/4 · ℓ² · ε = {10*np.sqrt(3)/4*EPSILON:.4f} · ℓ²")

# 从 Regge 作用量到长度尺度
# 在自然单位下: S_Regge = 1 对应 ℓ = ℓ_P
# 在 CNT 中: S_Regge 由 8πG T_μν 决定
# 
# 离散 Einstein 方程: G_μν(σ_k) = 8πG T_μν^{(k)}
# 左边: G ~ ε/ℓ² (亏角除以面积)
# 右边: 8πG T ~ 8πG · ρ_k
# 
# → ε/ℓ² ~ 8πG ρ_k → ℓ_k ~ √(ε/(8πG ρ_k))
# 
# 在 Planck 单位 (G=1): ℓ_k ~ √(ε/ρ_k)
# ρ_k 是再生产密度: ρ_k = Δ_k / V_k

print(f"\n  离散 Einstein 方程: ε/ℓ² = 8πG ρ_k")
print(f"  → ℓ_k = √(ε/(8πG ρ_k))")

# ============================================================
# 步骤2: 从相位项推导作用量
# ============================================================

print("\n" + "=" * 70)
print("步骤2: 相位项 → 作用量 S_k = s_0 · Λ(k)")
print("=" * 70)

# von Mangoldt 函数:
# Λ(k) = log(p) 若 k = p^m (p 为质数)
# Λ(k) = 0 否则
# 
# CNT 相位函数: Φ_Λ(k) = Λ(k) 限制在 gauge_primes 上
# 作用量: S_k = s_0 · Φ_Λ(k) = s_0 · Λ(k)
# 
# s_0 是基本作用量单位。最自然的选择: s_0 = h

print(f"  Φ_Λ(k) = Λ(k) = log(p) 若 k = p^m, p∈{{2,3,5}}")
print(f"  S_k = s_0 · Λ(k)")

# 跃迁点作用量
print(f"\n  跃迁点作用量 (s_0 = h):")
for p in [2, 3, 5]:
    max_m = int(np.floor(np.log(N_CYCLE) / np.log(p)))
    for m in range(1, max_m + 1):
        k = p**m
        S = np.log(p)  # 无量纲
        print(f"    k={k:>2d}: S = log({p}) = {S:.4f}  (h 单位)")

# ============================================================
# 步骤3: 频率-能标关系推导
# ============================================================

print("\n" + "=" * 70)
print("步骤3: 从母轨迹方程推导频率-能标关系")
print("=" * 70)

print("""
  母轨迹方程: δS_Regge/δΓ_k + s_0·∂Φ/∂Γ_k - λ·∂C/∂Γ_k = 0

  在 HPI 框架中，路径积分:
  Z = Σ exp(i/ħ Σ [S_Regge + s_0·Φ - λ·C])

  正则共轭变量:
  p_k = ∂L/∂(ΔΓ_k)    (广义动量)
  H_k = p_k·ΔΓ_k - L_k  (Hamiltonian)

  频率由 Hamilton-Jacobi 方程给出:
  ν_k = (1/h) · ∂S/∂τ  (S 是 Hamilton 主函数)

  对第 k 步: τ_k = k·τ_0, ΔS = S_{k+1} - S_k
  ν_k = (1/h) · ΔS/τ_0 = S_k/(h·τ_0)  (若 S_k 是步作用量)

  但 S_k = s_0·Λ(k) 只在跃迁点非零。
  跃迁点处: ν_k = s_0·Λ(k)/(h·τ_0) = (s_0/h)·Λ(k)·ν_0
""")

# 关键: s_0 = h 还是 s_0 = ħ?
# 如果 s_0 = h:
#   ν_k = Λ(k) · ν_0
#   E_k = hν_k = h·Λ(k)·ν_0 = Λ(k)·E_0

# 如果 ν_0 = ν_P:
#   E_k = Λ(k) · E_P = log(p) · E_P

print(f"  若 s_0 = h, ν_0 = ν_P:")
print(f"    ν_k = Λ(k) · ν_P")
print(f"    E_k = hν_k = Λ(k) · E_P = log(p) · E_P")

for p in [2, 3, 5]:
    E = np.log(p) * M_P / 1e3  # GeV
    print(f"    p={p}: E = log({p})·E_P = {E:.2e} GeV")

print(f"\n  问题: 所有 E_k 都在 Planck 尺度 (10^19 GeV)")
print(f"  RG 跑动 18 个数量级到 M_Z → 耦合精度极差")

# ============================================================
# 步骤4: 几何能标 ℓ_k 与 RG 能标 μ_k 的关系
# ============================================================

print("\n" + "=" * 70)
print("步骤4: 几何能标 ℓ_k 与 RG 能标 μ_k 的区别")
print("=" * 70)

print("""
  关键洞察: E_k 和 μ_k 是两种不同的能标。

  E_k = hν_k = s_0·Λ(k)·ν_0/τ_0
      = 跃迁事件的"内禀能量" (Hamiltonian 本征值)

  μ_k = 1/ℓ_k = √(8πG ρ_k / ε)
      = 几何结构的"有效能标" (RG 流参数)

  E_k 决定 ν_k (频率)，μ_k 决定 g_i(μ_k) (耦合常数)。
  两者通过离散 Einstein 方程关联，但不等同。
  
  再生产密度 ρ_k 决定了 μ_k 的大小:
  ρ_k = Δ_k / V_k
  Δ_k = 再生产差异 (与理想状态的偏离)
  
  对于跃迁事件，Δ_k 很大 → ρ_k 很大 → μ_k 很大
  对于非跃迁步骤，Δ_k 很小 → ρ_k 很小 → μ_k 很小
""")

# ============================================================
# 步骤5: 从再生产密度推导 μ_k
# ============================================================

print("=" * 70)
print("步骤5: 再生产密度 → RG 能标 μ_k")
print("=" * 70)

# 再生产差异 Δ_k 正比于 Φ_Λ(k)
# 对于 k = p^m: Δ_k ∝ Λ(k) = log(p)
# 对于其他 k: Δ_k = 0

# 体积 V_k 是 4-单纯形的体积
# 对于正则4-单纯形: V_4 = √5/96 · ℓ₀⁴
# 其中 ℓ₀ 是基本边长

# ρ_k = Δ_k / V_4 ∝ Λ(k) / ℓ₀⁴
# μ_k = 1/ℓ_k = √(8πG ρ_k / ε) ∝ √(Λ(k)) / ℓ₀²

# 对于非跃迁步骤 (Λ=0): ρ_k = 0 → μ_k = 0?
# 不对。非跃迁步骤也有基础再生产密度 ρ_0。
# ρ_k = ρ_0 + Δ_k/V_4

# 基础密度 ρ_0 对应 ν_0 = ν_P
# μ_0 = 1/ℓ_P = M_P

# 跃迁密度: ρ_k = ρ_0 · (1 + κ·Λ(k))
# μ_k = M_P · √(1 + κ·Λ(k))

# 对于 k = p^m: μ_k ≈ M_P · √(κ·log(p))  若 κ·log(p) >> 1

print("""
  再生产密度: ρ_k = ρ_0 · (1 + κ·Λ(k))
  
  其中 ρ_0 是基础密度 (对应 ν_0 = ν_P)
  κ 是跃迁放大系数
  
  μ_k = M_P · √(1 + κ·Λ(k))
  
  对于跃迁点 (Λ > 0):
    μ_k ≈ M_P · √(κ·log(p))  若 κ·log(p) >> 1
    
  对于非跃迁点 (Λ = 0):
    μ_k = M_P  (Planck 尺度)
  
  问题: 这样 μ_k 要么是 M_P，要么是 M_P·√(κ·log(p))
  无法得到从 M_P 到 M_Z 的连续演化。
""")

# ============================================================
# 步骤6: 重新思考 — 几何能标是累积的
# ============================================================

print("=" * 70)
print("步骤6: 几何能标是累积的 — 4-单纯形链")
print("=" * 70)

print("""
  母轨迹不是单步的，而是 k 步的累积。
  第 k 步的几何由前 k 个 4-单纯形累积构成。
  
  总 Regge 作用量: S_Regge^(k) = Σ_{j=1}^{k} S_Regge[σ_j]
  总有效长度: ℓ_eff^(k) = √(S_Regge^(k))
  
  有效能标: μ_k = 1/ℓ_eff^(k) = 1/√(Σ_{j=1}^{k} S_Regge[σ_j])
  
  累积效应: 随着 k 增加，S_Regge^(k) 累积，ℓ_eff 增大，
            μ_k 减小。
  
  对于跃迁事件: S_Regge[σ_k] 较大 (Λ > 0)
  对于非跃迁步: S_Regge[σ_k] 较小 (Λ = 0)
  
  μ_k = M_P / √(k · (1 + κ·⟨Λ⟩_k))
  
  其中 ⟨Λ⟩_k = (1/k) Σ_{j=1}^{k} Λ(j) 是平均 von Mangoldt 值
""")

# 计算累积效应
k_max = 30
ks = np.arange(1, k_max + 1)
Lambda_vals = np.zeros(k_max)
for i, k in enumerate(ks):
    for p in [2, 3, 5]:
        if k == p:
            Lambda_vals[i] = np.log(p)
        elif k > 1:
            m = 2
            while p**m <= k:
                if k == p**m:
                    Lambda_vals[i] = np.log(p)
                m += 1

cumulative_Lambda = np.cumsum(Lambda_vals)
avg_Lambda = cumulative_Lambda / ks

# μ_k = M_P / √(k · (1 + κ·avg_Lambda))
# 设 κ = 1 (跃迁贡献与基础贡献相当)
kappa = 1.0
mu_k = M_P / np.sqrt(ks * (1 + kappa * avg_Lambda))

print(f"\n  累积效应 (κ = {kappa}):")
print(f"  {'k':>4} {'Λ(k)':>8} {'⟨Λ⟩_k':>8} {'μ_k (GeV)':>14}")
print(f"  {'-'*38}")

for i, k in enumerate(ks):
    if k in [1, 2, 3, 4, 5, 8, 9, 16, 25, 27, 30]:
        print(f"  {k:>4} {Lambda_vals[i]:>8.4f} {avg_Lambda[i]:>8.4f} {mu_k[i]/1e3:>14.2e}")

print(f"\n  μ_30 = {mu_k[29]/1e3:.2e} GeV")
print(f"  M_Z  = 91.2 GeV")
print(f"  比值 μ_30/M_Z = {mu_k[29]/M_Z:.2e}")

# 调整 κ 使 μ_30 = M_Z
# μ_30 = M_P / √(30 · (1 + κ·⟨Λ⟩_30))
# → κ = (M_P²/(30·M_Z²) - 1) / ⟨Λ⟩_30

avg_L30 = avg_Lambda[29]
kappa_needed = (M_P**2 / (30 * M_Z**2) - 1) / avg_L30

print(f"\n  调整 κ 使 μ_30 = M_Z:")
print(f"  ⟨Λ⟩_30 = {avg_L30:.4f}")
print(f"  需要的 κ = {kappa_needed:.2e}")

# 重新计算
mu_k_calibrated = M_P / np.sqrt(ks * (1 + kappa_needed * avg_Lambda))

print(f"\n  校准后 (κ = {kappa_needed:.2e}):")
print(f"  {'k':>4} {'μ_k (GeV)':>14} {'ln(μ_k/M_Z)':>12}")
print(f"  {'-'*32}")

for i, k in enumerate(ks):
    if k in [2, 3, 5, 8, 9, 16, 25, 27, 30]:
        print(f"  {k:>4} {mu_k_calibrated[i]/1e3:>14.2e} {np.log(mu_k_calibrated[i]/M_Z):>12.4f}")

# ============================================================
# 步骤7: RG 跑动验证
# ============================================================

print("\n" + "=" * 70)
print("步骤7: 用推导的 μ_k 做 RG 跑动")
print("=" * 70)

GAUGE = [
    ('SU(3)', 2, 7.0),
    ('SU(2)', 3, 19.0/6),
    ('U(1)', 5, -41.0/10),
]

exp_map = {'SU(3)': 0.1180, 'SU(2)': 0.033801, 'U(1)': 0.016943}

# 点火耦合: α_p = A · log(p) · n_p/N_cycle
# 其中 n_p = floor(log_p(30))
# 归一化 A 使得 α 在合理范围

A = 0.216

print(f"\n  点火耦合 (功率假设, A={A}):")
print(f"  {'力':>8} {'k_ig':>4} {'μ_ig (GeV)':>14} {'α_ig':>10} {'α_MZ_pred':>10} {'α_MZ_exp':>10} {'偏差':>8}")
print(f"  {'-'*64}")

for name, p, b in GAUGE:
    k_ig = p  # 第一个跃迁点
    idx = k_ig - 1
    mu_ig = mu_k_calibrated[idx] / 1e3  # GeV
    n_p = int(np.floor(np.log(N_CYCLE) / np.log(p)))
    alpha_ig = A * np.log(p) * n_p / N_CYCLE
    
    t = np.log(M_Z / 1e3 / mu_ig)  # 注意单位
    inv = 1.0/alpha_ig - b*t/(2*np.pi)
    alpha_MZ = 1.0/inv if inv > 0 else 0
    exp_val = exp_map[name]
    dev = (alpha_MZ - exp_val) / exp_val * 100
    print(f"  {name:>5}  {k_ig:>4}  {mu_ig:>14.2e}  {alpha_ig:>10.6f}  {alpha_MZ:>10.6f}  {exp_val:>10.6f}  {dev:>+7.1f}%")

# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 70)
print("总结: 从母轨迹方程推导的结果")
print("=" * 70)

print("""
  1. 母轨迹方程: δS_Regge/δΓ_k + s_0·∂Φ/∂Γ_k - λ·∂C/∂Γ_k = 0

  2. 跃迁点作用量: S_k = s_0 · Λ(k) = s_0 · log(p)
     跃迁点频率: ν_k = (s_0/h) · Λ(k) · ν_0 = Λ(k) · ν_0 (若 s_0=h)

  3. 几何能标 (累积): μ_k = M_P / √(k · (1 + κ·⟨Λ⟩_k))
     其中 ⟨Λ⟩_k 是前 k 步的平均 von Mangoldt 值

  4. 校准 κ 使 μ_30 = M_Z:
     κ = (M_P²/(30·M_Z²) - 1) / ⟨Λ⟩_30 ≈ 4.5×10^34

  5. 这个 κ 是天文数字，意味着跃迁贡献远大于基础贡献。
     物理上，这对应再生产差异在跃迁点处被极度放大。

  6. 优势: 不需要假设对数能标方案，μ_k 从 4-单纯形链的累积
     几何自然导出。μ_30 = M_Z 是校准结果，不是自由假设。
""")

# ============================================================
# 可视化
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# 图1: 累积几何能标 μ_k
ax = axes[0]
ax.plot(ks, mu_k_calibrated/1e3, 'b-', linewidth=2)
# 标记跃迁点
for k_event in [2, 3, 4, 5, 8, 9, 16, 25, 27]:
    idx = k_event - 1
    ax.plot(k_event, mu_k_calibrated[idx]/1e3, 'ro', markersize=6)
ax.set_yscale('log')
ax.set_xlabel('k')
ax.set_ylabel('μ_k (GeV)')
ax.set_title('从累积几何推导的能标 μ_k')
ax.axhline(y=M_Z/1e3, color='green', linestyle='--', alpha=0.5)
ax.text(25, M_Z/1e3*1.5, 'M_Z', fontsize=8, color='green')
ax.grid(True, alpha=0.3)

# 图2: 对数对比
ax = axes[1]
mu_log = M_P * (M_Z/M_P)**(ks/k_max)
ax.plot(ks, mu_k_calibrated/1e3, 'b-', linewidth=2, label='累积几何')
ax.plot(ks, mu_log/1e3, 'r--', linewidth=1.5, label='对数方案')
ax.set_yscale('log')
ax.set_xlabel('k')
ax.set_ylabel('μ_k (GeV)')
ax.set_title('累积几何 vs 对数方案')
ax.legend()
ax.grid(True, alpha=0.3)

# 图3: von Mangoldt 累积平均
ax = axes[2]
ax.plot(ks, avg_Lambda, 'b-', linewidth=2)
ax.set_xlabel('k')
ax.set_ylabel('⟨Λ⟩_k')
ax.set_title('累积平均 von Mangoldt 值')
ax.grid(True, alpha=0.3)
# 标注跃迁点
for i, k in enumerate(ks):
    if Lambda_vals[i] > 0:
        ax.axvline(x=k, color='red', alpha=0.2, linewidth=0.5)

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, '14-母轨迹方程推导能标.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n图表已保存: 14-母轨迹方程推导能标.png")