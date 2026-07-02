"""
从母轨迹方程直接推导耦合常数
==============================

放弃频率假设，直接从母轨迹 HPI 出发。

母轨迹 HPI:
    Z = Sigma exp(i/hbar * Sigma [S_Regge + s0*Phi - lambda*C])

驻相方程:
    dS_Regge/dGamma_k + s0 * dPhi/dGamma_k - lambda * dC/dGamma_k = 0

其中 Gamma_k = (g1, g2, g3) 是三个耦合常数。

关键: 耦合常数不是从频率导出的，而是母轨迹在相空间中的坐标。
      频率决定"节奏"，耦合常数是"位置"。
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
M_P = 1.22089e22       # MeV
M_Z = 91.1876e3        # MeV
N_CYCLE = 30

# ============================================================
# 路径1: 从 Cartan 曲率通道推导耦合常数比值
# ============================================================

print("=" * 70)
print("路径1: Cartan 曲率通道 → 耦合常数比值")
print("=" * 70)

# 正则4-单纯形, 10个bivector
# Cartan曲率算子本征值: {9, 4, 4, 4, 4, 1, 1, 1, 1, 1}
# 不可约表示: 1 (dim 1, eigenvalue 9), 4 (dim 4, eigenvalue 4), 5 (dim 5, eigenvalue 1)

# 曲率 = eigenvalue * deficit_angle
# 耦合常数 = 1 / 曲率 (类比: alpha = 1 / (4pi * 曲率) 在规范理论中)

# 但哪一个通道对应哪一个规范力?
# 这需要额外的物理输入。

# 假设: 耦合强度正比于通道维度 (更多的bivector = 更强的耦合)
# dim(1) = 1, dim(4) = 4, dim(5) = 5
# 比例: 1 : 4 : 5

# 或者: 耦合强度反比于本征值 (更大的本征值 = 更大的曲率 = 更弱的耦合)
# 1/9 : 1/4 : 1 = 1 : 2.25 : 9

# 或者: 耦合强度正比于本征值 (更大的本征值 = 更大的曲率 = 更强的耦合?)
# 9 : 4 : 1

print("""
Cartan 曲率算子本征值: {9, 4, 4, 4, 4, 1, 1, 1, 1, 1}
不可约表示: 1 (dim 1, eval 9), 4 (dim 4, eval 4), 5 (dim 5, eval 1)

候选映射:
  A: alpha ∝ dim → 1:4:5
  B: alpha ∝ 1/eval → 1/9:1/4:1 = 1:2.25:9
  C: alpha ∝ eval → 9:4:1
  D: alpha ∝ 1/dim → 1:1/4:1/5 = 20:5:4
""")

# 从 SM 反推 GUT 尺度的耦合比值
# 对数方案: mu_k = M_P * (M_Z/M_P)^(k/30)
# mu_2 = M_P*(M_Z/M_P)^(2/30), mu_3 = M_P*(M_Z/M_P)^(3/30), mu_5 = M_P*(M_Z/M_P)^(5/30)

b_vals = {'SU(3)': 7.0, 'SU(2)': 19.0/6, 'U(1)': -41.0/10}
alpha_MZ = {'SU(3)': 0.1180, 'SU(2)': 0.033801, 'U(1)': 0.016943}

# 反推点火耦合
alpha_ig = {}
for name, p in [('SU(3)', 2), ('SU(2)', 3), ('U(1)', 5)]:
    mu_ig = M_P * (M_Z/M_P)**(p/N_CYCLE) / 1e3  # GeV
    b = b_vals[name]
    t = np.log(mu_ig * 1e3 / M_Z)  # ln(mu_ig/M_Z)
    inv = 1.0/alpha_MZ[name] + b*t/(2*np.pi)
    alpha_ig[name] = 1.0/inv

print(f"\nSM 反推的 GUT 尺度点火耦合:")
print(f"  SU(3): alpha_ig = {alpha_ig['SU(3)']:.6f}")
print(f"  SU(2): alpha_ig = {alpha_ig['SU(2)']:.6f}")
print(f"  U(1): alpha_ig = {alpha_ig['U(1)']:.6f}")

# 比值
ref = alpha_ig['SU(3)']
ratios = {name: alpha_ig[name]/ref for name in alpha_ig}
print(f"\n  比值 (SU(3)=1): {ratios['SU(3)']:.3f} : {ratios['SU(2)']:.3f} : {ratios['U(1)']:.3f}")

# 与候选对比
candidates = {
    'A: dim': [1, 4, 5],
    'B: 1/eval': [1/9, 1/4, 1],
    'C: eval': [9, 4, 1],
    'D: 1/dim': [1, 1/4, 1/5],
}
print(f"\n  候选比值:")
for name, vals in candidates.items():
    norm = vals[0]
    r = [v/norm for v in vals]
    print(f"    {name}: {r[0]:.3f} : {r[1]:.3f} : {r[2]:.3f}")

# ============================================================
# 路径2: 从 p进赋值推导耦合常数
# ============================================================

print("\n" + "=" * 70)
print("路径2: p进赋值 → 耦合常数")
print("=" * 70)

# 合成p进数编码: x = Sigma S_k * P_k
# p进赋值: nu_p(x) = max{nu : p^nu | x}
# 
# 对于 gauge_primes = {2,3,5}, P_3 = 30:
# nu_2(30) = 1, nu_3(30) = 1, nu_5(30) = 1
# 
# 如果耦合常数 mu_p ∝ p^{nu_p(x)}:
# g_2 : g_3 : g_5 = 2^1 : 3^1 : 5^1 = 2:3:5

# 如果耦合常数 ∝ nu_p(x):
# g_2 : g_3 : g_5 = 1:1:1 (统一)

# 如果耦合常数 ∝ 1/nu_p(x):
# 也是 1:1:1

print("""
合成p进数编码 x = Sigma S_k * P_k, P_3 = 30

nu_2(x) = 1, nu_3(x) = 1, nu_5(x) = 1 (所有 S_k 与 gauge_primes 互质)

候选:
  E: alpha ∝ p^{nu_p} → 2:3:5
  F: alpha ∝ nu_p → 1:1:1 (统一)
  
比值 1:1:1 意味着三个规范力在编码层面统一。
分裂发生在 RG 跑动过程中。
""")

# ============================================================
# 路径3: 从母轨迹闭合条件推导
# ============================================================

print("=" * 70)
print("路径3: 母轨迹闭合条件 → 耦合常数约束")
print("=" * 70)

# 母轨迹是闭合环: Gamma_{N_cycle} = Gamma_0
# 这意味着经过一个完整周期，耦合常数必须回到初始值。
# 
# RG 方程: d(alpha^{-1})/d(ln mu) = b/(2pi)
# 积分: alpha^{-1}(mu_2) - alpha^{-1}(mu_1) = b/(2pi) * ln(mu_2/mu_1)
# 
# 闭合条件: alpha^{-1}(mu_N) = alpha^{-1}(mu_0)
# → b/(2pi) * ln(mu_N/mu_0) = 0 (mod 2pi)
# → 如果 mu_N = mu_0，自动满足。
# 
# 但如果 mu_N != mu_0 (周期结束时的能标不等于起始能标):
# b/(2pi) * ln(mu_N/mu_0) = 0 mod (某个值)
# 这给出了 b 的量子化条件。

print("""
闭合条件: Gamma_{N_cycle} = Gamma_0

对于第 i 个规范力:
  alpha_i^{-1}(mu_N) - alpha_i^{-1}(mu_0) = b_i/(2pi) * ln(mu_N/mu_0)

如果 mu_N = mu_0 (能标也闭合): 自动满足。
如果 mu_N != mu_0: 需要 b_i * ln(mu_N/mu_0) = 0 mod (2pi*整数)

这在 b_i 上施加了量子化条件。
但 b_i 由标准模型决定，不是 CNT 的自由参数。
""")

# ============================================================
# 路径4: 直接用 RG 反推（最可靠）
# ============================================================

print("=" * 70)
print("路径4: RG 反推 (最可靠，但需要实验输入)")
print("=" * 70)

# 唯一的可靠方法: 用 SM 实验值反推。
# 需要假设 mu_ig 的值。

# 对数方案
print("\n  对数方案 (mu_k = M_P * (M_Z/M_P)^(k/30)):")
for name, p in [('SU(3)', 2), ('SU(2)', 3), ('U(1)', 5)]:
    mu_ig = M_P * (M_Z/M_P)**(p/N_CYCLE) / 1e3
    b = b_vals[name]
    t = np.log(mu_ig * 1e3 / M_Z)
    inv = 1.0/alpha_MZ[name] + b*t/(2*np.pi)
    a_ig = 1.0/inv
    print(f"    {name}: mu_ig = {mu_ig:.2e} GeV, alpha_ig = {a_ig:.6f}")

# 逆 p进方案: mu_p = M_P / p
print("\n  逆 p进方案 (mu_p = M_P/p):")
for name, p in [('SU(3)', 2), ('SU(2)', 3), ('U(1)', 5)]:
    mu_ig = M_P / p / 1e3
    b = b_vals[name]
    t = np.log(mu_ig * 1e3 / M_Z)
    inv = 1.0/alpha_MZ[name] + b*t/(2*np.pi)
    a_ig = 1.0/inv
    print(f"    {name}: mu_ig = {mu_ig:.2e} GeV, alpha_ig = {a_ig:.6f}")

# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 70)
print("诚实结论")
print("=" * 70)

print("""
  母轨迹方程 δS/δΓ + s0·∂Φ/∂Γ - λ·∂C/∂Γ = 0 是 1 个方程,
  3 个未知数 (g1, g2, g3) 在每一步。方程本身欠定。

  耦合常数不能从母轨迹方程唯一确定，需要额外输入:
  1. 能标函数 mu(k) — 决定 RG 跑动长度
  2. 边界条件 — 决定初值

  四种候选路径:
  A-D: Cartan 曲率通道 → 比值不对
  E-F: p进赋值 → 只能给出统一 (1:1:1) 或 2:3:5
  逆 RG: 需要 mu(k) 假设

  最诚实的结论:
  1. 母轨迹方程给出的是"框架"，不是"数值"
  2. 耦合常数的精确数值需要实验输入 (SM beta 函数 + alpha_MZ)
  3. CNT 的贡献是解释"为什么有三个力"和"为什么周期=30"
  4. 精细结构常数等具体数值仍需从 SM 实验反推

  但这不意味着 CNT 没有预测力:
  - N_cycle = 30 是刚性预测
  - 质数动力跃迁在 p^m 处是刚性预测
  - 三力统一于 p进编码 (nu_2=nu_3=nu_5=1) 是刚性预测
  - 频率层级结构是刚性预测
""")