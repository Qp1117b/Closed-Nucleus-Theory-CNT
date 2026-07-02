"""
CNT 端到端 RG 跑动 — 深度分析
==============================
数值结果的关键发现与物理洞察。

运行日期: 2026-07-02
"""

import numpy as np

# ============================================================
# 核心发现1: 点火点耦合常数几乎是普适的
# ============================================================
print("=" * 70)
print("核心发现: 点火点耦合常数几乎普适")
print("=" * 70)

# 从反向跑动得到的点火点耦合常数
alpha_ign = {
    'SU3': 0.020210,  # at k=2, μ=8.81e17 GeV
    'SU2': 0.021065,  # at k=3, μ=2.37e17 GeV
    'U1':  0.026613,  # at k=5, μ=1.71e16 GeV
}

mu_ign = {
    'SU3': 8.81e17,
    'SU2': 2.37e17,
    'U1':  1.71e16,
}

# RG 系数
b = {'SU3': 7.0, 'SU2': 19.0/6, 'U1': -41.0/10}

# 将三个耦合都跑到同一个参考能标 μ_ref = 1e17 GeV
mu_ref = 1e17

def run_rg(alpha_init, mu_init, mu_final, b_val):
    alpha_inv = 1.0 / alpha_init + b_val / (2*np.pi) * np.log(mu_final / mu_init)
    return 1.0 / alpha_inv

print("\n将三个耦合跑到同一个参考能标 μ_ref = 1e17 GeV:")
print("-" * 50)
for key in ['SU3', 'SU2', 'U1']:
    alpha_ref = run_rg(alpha_ign[key], mu_ign[key], mu_ref, b[key])
    print(f"  {key}: α(μ_ref) = {alpha_ref:.6f}  (α⁻¹ = {1.0/alpha_ref:.2f})")

# 计算平均值和离散度
alphas_ref = [run_rg(alpha_ign[key], mu_ign[key], mu_ref, b[key]) for key in ['SU3', 'SU2', 'U1']]
alphas_inv_ref = [1.0/a for a in alphas_ref]
mean_inv = np.mean(alphas_inv_ref)
std_inv = np.std(alphas_inv_ref)
print(f"\n  α⁻¹ 平均值: {mean_inv:.2f}")
print(f"  α⁻¹ 标准差: {std_inv:.2f}  (相对: {std_inv/mean_inv*100:.1f}%)")

print("\n" + "=" * 70)
print("核心发现2: 所有简单假设都失败")
print("=" * 70)

print("""
H1 (α ∝ log(p)):  α_s(M_Z)=0.037 (实验: 0.118) — 偏差 3.2 倍
H2 (α ∝ 1/log(p)): α_s=0.117 接近, 但 α⁻¹=288 (实验: 128) — 偏差 2.3 倍
H3-H5: α_s 跑负 (Landau 奇点), 完全失败
H6: 所有值太小, α_s=0.011 (实验: 0.118) — 偏差 10 倍

结论: 耦合常数不是简单的 log(p) 或 1/log(p) 函数。
      点火点耦合常数几乎是普适的 (~0.02-0.03)。
""")

print("=" * 70)
print("核心发现3: 为什么简单假设失败？")
print("=" * 70)

print("""
原因: 跃迁点火发生在不同能标, 而不是同一个能标。

  k=2 (SU3): μ = 8.81×10¹⁷ GeV  (接近 Planck 尺度)
  k=3 (SU2): μ = 2.37×10¹⁷ GeV  
  k=5 (U1):  μ = 1.71×10¹⁶ GeV  (GUT 尺度)

如果三个力在点火时就有不同的耦合常数, 那么经过 15-17 个数量级
的 RG 跑动后, M_Z 处的值会完全不同。

但实验事实是: M_Z 处的三个耦合常数数量级相近 (α_s≈0.118, 
α_2≈0.034, α_1≈0.017)。这意味着点火时的耦合常数也必须相近。

反向跑动证实了这一点: α₃≈0.020, α₂≈0.021, α₁≈0.027。
""")

print("=" * 70)
print("核心发现4: 规范耦合统一——但不是GUT式的统一")
print("=" * 70)

print("""
标准 GUT: 三个耦合在同一个能标 (~10¹⁶ GeV) 处统一。
CNT:      三个耦合在各自质数对应的能标处"点火", 点火值普适。

     标准 GUT                    CNT 质数动力跃迁
     ─────────                  ─────────────────
     α₁⁻¹                        α₁⁻¹
      \                            \
       \   统一点                   \   U(1)点火 (k=5)
        \  (10¹⁶ GeV)               \  SU(2)点火 (k=3)
         \                           \ SU(3)点火 (k=2)
          \                           \
           \                           \
            \                           \
             +---> log μ                 +---> log μ

CNT 的"统一"不在一个点上, 而是沿着质数序列分布。
这解释了为什么标准 GUT 的统一不完全精确 (Δα⁻¹ ≈ 3-5)。
""")

print("=" * 70)
print("核心发现5: 点火条件应该是普适耦合常数")
print("=" * 70)

print("""
新的候选点火条件:

    α_ignition = α_universal ≈ 0.02-0.03  (对所有三个力)

也就是说, 在各自的跃迁点 k=p 处, 三个规范力以相同的耦合常数"点火"。
然后各自沿着 RG 流跑动到 M_Z, 产生观测到的差异。

这比 α ∝ log(p) 或 α ∝ 1/log(p) 更简单、更自然:
    - 闭合核的再生产结构对三个力是对称的 (只是质数不同)
    - 点火时的耦合强度由闭合核的内在结构决定, 与质数无关
    - 质数只决定点火发生的能标 (k=p 处的 μ_k)
    - 能标的不同导致 RG 跑动量的不同, 产生 M_Z 处的差异

这个假设只有一个自由参数: α_universal。
""")

print("=" * 70)
print("核心发现6: 下一步——从 α_universal 反推闭合核参数")
print("=" * 70)

# 优化 α_universal
print("\n扫描 α_universal 以最佳拟合 SM 实验值:")
print("-" * 50)

M_Z = 91.1876
M_P = 1.22089e19
N_CYCLE = 30

def energy_scale(k):
    return M_P * (M_Z / M_P) ** (k / N_CYCLE)

best_loss = np.inf
best_alpha_u = None

for alpha_u in np.logspace(np.log10(0.01), np.log10(0.05), 200):
    alphas_ign = {'SU3': alpha_u, 'SU2': alpha_u, 'U1': alpha_u}
    
    alphas_MZ = {}
    for key, p, b_val in [('SU3', 2, 7.0), ('SU2', 3, 19.0/6), ('U1', 5, -41.0/10)]:
        mu_ig = energy_scale(p)
        alpha_inv = 1.0/alpha_u + b_val/(2*np.pi) * np.log(M_Z / mu_ig)
        alphas_MZ[key] = 1.0/alpha_inv if alpha_inv > 0 else np.inf
    
    if any(v <= 0 or np.isinf(v) for v in alphas_MZ.values()):
        continue
    
    # 损失
    loss = 0
    loss += ((alphas_MZ['SU3'] - 0.1180) / 0.1180) ** 2
    loss += ((alphas_MZ['SU2'] - 0.033801) / 0.033801) ** 2
    loss += ((alphas_MZ['U1'] - 0.016943) / 0.016943) ** 2
    
    if loss < best_loss:
        best_loss = loss
        best_alpha_u = alpha_u

print(f"  最佳 α_universal = {best_alpha_u:.6f}")
print(f"  损失 = {best_loss:.6e}")

# 用最佳值计算
alphas_MZ_best = {}
for key, p, b_val in [('SU3', 2, 7.0), ('SU2', 3, 19.0/6), ('U1', 5, -41.0/10)]:
    mu_ig = energy_scale(p)
    alpha_inv = 1.0/best_alpha_u + b_val/(2*np.pi) * np.log(M_Z / mu_ig)
    alphas_MZ_best[key] = 1.0/alpha_inv

print(f"\n  预测值 at M_Z:")
print(f"    α_s  = {alphas_MZ_best['SU3']:.6f}  (实验: 0.1180)")
print(f"    α_2  = {alphas_MZ_best['SU2']:.6f}  (实验: 0.0338)")
print(f"    α_1  = {alphas_MZ_best['U1']:.6f}  (实验: 0.0169)")

# 计算 α_em 和 sin²θ_W
alpha_1 = alphas_MZ_best['U1']
alpha_2 = alphas_MZ_best['SU2']
alpha_Y = 3.0/5 * alpha_1
sin2 = alpha_Y / (alpha_2 + alpha_Y)
alpha_em = alpha_2 * sin2

print(f"\n  导出:")
print(f"    α⁻¹   = {1.0/alpha_em:.2f}  (实验: 127.95)")
print(f"    sin²θ_W = {sin2:.6f}  (实验: 0.23122)")

print("\n" + "=" * 70)
print("结论")
print("=" * 70)

print("""
1. 点火点耦合常数几乎是普适的（α ≈ 0.02-0.03），不是简单的 log(p) 函数。
2. 普适点火假设只有一个自由参数 α_universal。
3. 用最佳 α_universal 可以在数量级上重现 SM 耦合常数，但精度不够。
4. 精度不够的可能原因:
   a) 单圈 RG 近似不够 (需要两圈或更高)
   b) 能标对数分布假设可能需要修正
   c) 点火点耦合常数不是完全普适的，可能有 log(p) 的小修正
   d) N_cycle = 30 的对数间距可能不是最优的
5. 最重要的物理洞察: 规范耦合的"统一"不是在一个点上，
   而是沿着质数序列 {2, 3, 5} 分布的"统一序列"。
""")