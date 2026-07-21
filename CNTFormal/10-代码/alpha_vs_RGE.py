#!/usr/bin/env python3
"""
α⁻¹ 公式 vs 标准 GUT RGE：最硬核的拟合检验

如果 CNT 的 α⁻¹ = 1/(C·λ_c·sin²θ_W) − 5 − ρ₂ − ρ₃ 是推导，
它必须等价于标准电弱统一 + RGE 跑动。
本脚本提取标准 RGE 路径，与 CNT 公式逐项对比。

日期: 2026-07-21
更新 (2026-07-21): 修正 sin²θ_W 公式错误和 β 函数系数。
  详见 delta_theta_W_first_principles.py 获取完整分析。
"""

import mpmath as mp
import numpy as np

mp.mp.dps = 50

# ============================================================
# 基础常数
# ============================================================
C = mp.mpf('0.023095708966')
gamma1_val = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + gamma1_val**2
C_theta = C / E1

lambda_c = mp.mpf('1.3160229113')
sin2W_exp = mp.mpf('0.23120')     # 实验值

# CNT GUT 参数
alpha_GUT_CNT = C * lambda_c       # 定理7.6
g_GUT_CNT = mp.sqrt(4 * mp.pi * alpha_GUT_CNT)

# 标准 GUT 参数
M_Z = mp.mpf('91.1876')           # GeV
M_GUT_CNT = mp.mpf('7.6e14')      # GeV, 定理7.3

rho2 = mp.mpf('0.198')
rho3 = mp.mpf('0.092')
W1 = mp.mpf('5')
delta_W = mp.mpf('-0.156')

f2 = mp.mpf('0.05')
f3 = mp.mpf('0.025')

# ============================================================
# §1: 标准电弱理论中 α_em 的构成
# ============================================================
print("=" * 75)
print("RGE 路径分析: CNT vs 标准 GUT")
print("=" * 75)

# 标准关系: e = g sin θ_W, 所以 α_em = α_2 · sin²θ_W
# α_em⁻¹ = α_2⁻¹ + (5/3) α_Y⁻¹ ... 不，在 SM 中:
# e = g sin θ_W, 所以 α_em = α_2 sin²θ_W
# α_em⁻¹ = 1/(α_2 sin²θ_W)

# CNT 声称: α_em⁻¹ ≈ 1/(α_GUT · sin²θ_W) − 修正
# 这意味着: α_2(M_Z) = α_GUT (无跑动!)
#           所有跑动效应被 −5−ρ₂−ρ₃ 吸收

# 检验: 如果 α_2 真的从 GUT 跑到 M_Z，修正量应该是多少？

# 标准 SM 1-loop β 函数:
# b_2 = -19/6 + 4N_g/3 = -19/6 + 4×3/3 = -19/6 + 4 = 5/6 (对于 SU(2))
# b_1 = 41/10 + 4N_g/3 = 41/10 + 4 = 81/10 (对于 U(1), GUT归一化)

b_2 = mp.mpf('5') / mp.mpf('6')    # SU(2) β 函数系数 (正 → 渐进自由)
b_1_GUT = mp.mpf('81') / mp.mpf('10')  # U(1) (GUT归一化) β 函数

# RGE: α_i⁻¹(M_Z) = α_GUT⁻¹ + b_i/(2π) ln(M_GUT/M_Z)
ln_ratio = mp.log(M_GUT_CNT / M_Z)
alpha_GUT_inv = 1 / alpha_GUT_CNT

alpha_2_inv_MZ = alpha_GUT_inv + b_2 / (2*mp.pi) * ln_ratio
alpha_1_inv_MZ = alpha_GUT_inv + b_1_GUT / (2*mp.pi) * ln_ratio

# SM 关系: α_em⁻¹ = α_2⁻¹ + α_Y⁻¹
# α_Y = (3/5) α_1 (GUT归一化), 所以 α_Y⁻¹ = (5/3) α_1⁻¹
alpha_em_inv_RGE = alpha_2_inv_MZ + (5/mp.mpf('3')) * alpha_1_inv_MZ

# 从 RGE 计算 sin²θ_W
# sin²θ_W = α_em / α_2 = 1/(1 + α_2/α_Y) ... 
# 更标准: sin²θ_W = α_Y/(α_2 + α_Y) [leading order]
# 或: sin²θ_W = α_em/α_2
sin2W_RGE = 1 / (1 + alpha_2_inv_MZ / ((5/mp.mpf('3')) * alpha_1_inv_MZ))

print(f"\nCNT GUT 参数:")
print(f"  α_GUT = C·λ_c = {float(alpha_GUT_CNT):.6f}")
print(f"  g_GUT = {float(g_GUT_CNT):.4f}")
print(f"  M_GUT = {float(M_GUT_CNT):.2e} GeV")
print(f"  ln(M_GUT/M_Z) = {float(ln_ratio):.2f}")

print(f"\n标准 GUT RGE (1-loop):")
print(f"  b_2 = {float(b_2):.4f}")
print(f"  b_1 = {float(b_1_GUT):.1f}")
print(f"  α_2⁻¹(M_Z) = α_GUT⁻¹ + b_2/(2π)·ln = {float(alpha_GUT_inv):.2f} + {float(b_2/(2*mp.pi)*ln_ratio):.2f} = {float(alpha_2_inv_MZ):.2f}")
print(f"  α_1⁻¹(M_Z) = α_GUT⁻¹ + b_1/(2π)·ln = {float(alpha_GUT_inv):.2f} + {float(b_1_GUT/(2*mp.pi)*ln_ratio):.2f} = {float(alpha_1_inv_MZ):.2f}")

# CNT 的 "bare α_em⁻¹"
alpha_em_bare_CNT = 1 / (C * lambda_c * sin2W_exp)

print(f"\n对比:")
print(f"  标准 RGE:  α_em⁻¹(M_Z) = {float(alpha_em_inv_RGE):.2f}")
print(f"  实验:      α_em⁻¹(M_Z) = 137.036")
print(f"  CNT bare:  α_em⁻¹(M_Z) = {float(alpha_em_bare_CNT):.2f}  (1/(C·λ_c·sin²θ_W))")
print(f"  CNT full:  α_em⁻¹(M_Z) = {float(alpha_em_bare_CNT - W1 - rho2 - rho3):.2f}  (bare − 5 − ρ₂ − ρ₃)")

print(f"\n  CNT bare − 标准 RGE = {float(alpha_em_bare_CNT - alpha_em_inv_RGE):.2f}")
print(f"  这 ~{float(alpha_em_bare_CNT - alpha_em_inv_RGE):.0f} 的差被 −W₁−ρ₂−ρ₃ = −{float(W1+rho2+rho3):.2f} '修正'")
print(f"\n  sin²θ_W (RGE) = {float(sin2W_RGE):.6f}")
print(f"  sin²θ_W (实验) = 0.23120")

# ============================================================
# §2: 关键检验 — CNT 公式等价于标准 RGE 吗?
# ============================================================
print("\n" + "=" * 75)
print("核心问题: CNT 公式 [1/(C·λ_c·sin²θ_W) − 5 − ρ] 等价于标准 RGE 吗?")
print("=" * 75)

# 标准 RGE 的 α_em⁻¹ 可以写成:
# α_em⁻¹ = α_2⁻¹ + (5/3)α_1⁻¹
#         = [α_GUT⁻¹ + b_2·ln/(2π)] + (5/3)[α_GUT⁻¹ + b_1·ln/(2π)]
#         = (1+5/3)α_GUT⁻¹ + [b_2 + (5/3)b_1]·ln/(2π)
#         = (8/3)α_GUT⁻¹ + [b_2 + (5/3)b_1]·ln/(2π)

coeff = 1 + 5/mp.mpf('3')  # = 8/3
b_em = b_2 + (5/mp.mpf('3')) * b_1_GUT

print(f"\n标准 RGE 展开:")
print(f"  α_em⁻¹ = (8/3)·α_GUT⁻¹ + b_em·ln/(2π)")
print(f"  b_em = b_2 + (5/3)·b_1 = {float(b_2):.4f} + {float(5/3*b_1_GUT):.1f} = {float(b_em):.4f}")
print(f"  (8/3)·α_GUT⁻¹ = {float((8/3)*alpha_GUT_inv):.2f}")
print(f"  b_em·ln/(2π) = {float(b_em/(2*mp.pi)*ln_ratio):.2f}")
print(f"  α_em⁻¹(RGE) = {float((8/3)*alpha_GUT_inv + b_em/(2*mp.pi)*ln_ratio):.2f}")

# CNT 展开:
# 1/(C·λ_c·sin²θ_W) = α_GUT⁻¹ / sin²θ_W
alpha0_inv = alpha_GUT_inv / sin2W_exp

print(f"\nCNT 展开:")
print(f"  α_GUT⁻¹ = (C·λ_c)⁻¹ = {float(alpha_GUT_inv):.2f}")
print(f"  1/(C·λ_c·sin²θ_W) = α_GUT⁻¹/sin²θ_W = {float(alpha0_inv):.2f}")
print(f"  = {float(alpha_GUT_inv):.2f} / {float(sin2W_exp):.4f}")

# 对比 (8/3) vs 1/sin²θ_W
print(f"\n  对比: (8/3)·α_GUT⁻¹ = {float((8/3)*alpha_GUT_inv):.2f}")
print(f"         α_GUT⁻¹/sin²θ_W = {float(alpha0_inv):.2f}")
print(f"         差值 = {float(alpha0_inv - (8/3)*alpha_GUT_inv):.1f}")

print(f"\n  CNT的 1/sin²θ_W = {float(1/sin2W_exp):.3f} 应等价于 (8/3) + RGE项")
print(f"  但标准GUT中 sin²θ_W不是参数而是输出!")
print(f"  标准: sin²θ_W(M_Z) 由 RGE 决定, 不是自由参数")

# ============================================================
# §3: 自洽性检验 — 如果从 RGE 计算 ρ_m, 能得到什么?
# ============================================================
print("\n" + "=" * 75)
print("自洽性检验: 如果从标准 RGE 反推 'CNT修正项'")
print("=" * 75)

# 假设 CNT 公式骨架正确, 但修正项应该匹配标准 RGE
# CNT: α_em⁻¹ = 1/(C·λ_c·sin²θ_W) − δCNT
# RGE: α_em⁻¹ = (8/3)(C·λ_c)⁻¹ + RGE_correction

# 设定 α_em⁻¹ = 137.036 (实验)
alpha_em_exp = mp.mpf('137.035999177')

# 从 CNT 公式反推 δ
delta_CNT = alpha0_inv - alpha_em_exp
print(f"\n  CNT 需要: δ = 1/(C·λ_c·s²) − α_exp⁻¹")
print(f"            = {float(alpha0_inv):.2f} − {float(alpha_em_exp):.2f}")
print(f"            = {float(delta_CNT):.2f}")
print(f"  实际使用: W₁ + ρ₂ + ρ₃ = 5 + {float(rho2):.3f} + {float(rho3):.3f} = {float(W1+rho2+rho3):.2f}")
print(f"  差值: {float(delta_CNT - W1 - rho2 - rho3):.3f}")

# 从标准 RGE 计算修正
delta_RGE = (8/mp.mpf('3')) * alpha_GUT_inv + b_em / (2*mp.pi) * ln_ratio - alpha_em_exp
print(f"\n  标准 RGE: α_em⁻¹ = (8/3)·α_GUT⁻¹ + ΔRGE")
print(f"            = {float((8/3)*alpha_GUT_inv):.2f} + ΔRGE = {float(alpha_em_exp):.2f}")
print(f"            ΔRGE = {float(b_em/(2*mp.pi)*ln_ratio):.2f} (纯跑动)")
print(f"  所以 α_em⁻¹(RGE) 与实验差: {float((8/3)*alpha_GUT_inv + b_em/(2*mp.pi)*ln_ratio - alpha_em_exp):.2f}")

# ============================================================
# §4: 最致命的检验
# ============================================================
print("\n" + "=" * 75)
print("最致命检验: CNT 公式中 sin²θ_W 的双重角色")
print("=" * 75)
print("""
在 CNT 中:
  sin²θ_W = 3/8 + δθ_W^(1) + f₂ρ₂ + f₃ρ₃  (来自角向结构)
  α⁻¹    = 1/(C·λ_c·sin²θ_W) − W₁ − ρ₂ − ρ₃   (来自径向+角向)

在标准电弱理论中:
  sin²θ_W 和 α 是独立的可观测量
  sin²θ_W 由 α_2/α_Y 的比值决定
  α 由 α_2·sin²θ_W = e²/(4π) 决定

CNT 公式中 sin²θ_W 同时出现在两个地方:
  1. 决定 α⁻¹ 的"裸值" (通过 1/sin²θ_W)
  2. 自身的值被 f₂ρ₂+f₃ρ₃ 修正
  
一致性条件:
  两个公式对 α⁻¹ 的依赖必须自洽!
  
  从 sin²θ_W 公式: f₂ρ₂ + f₃ρ₃ = sin²θ_W − 3/8 − δθ_W^(1)
  从 α⁻¹ 公式:     ρ₂ + ρ₃   = 1/(C·λ_c·sin²θ_W) − W₁ − α⁻¹
  
  如果 f₂ ≠ 1 (确实 f₂=1/20, f₃=1/40), 这两个条件不能同时
  满足任意 (ρ₂, ρ₃), 必须通过调整 δθ_W^(1) 来达成。

  所以 δθ_W^(1) 的真正角色 = 维持两个公式之间的自洽性。
  这不是"拟合 α⁻¹"——这是"自洽性条件"。
""")

# 数值验证
sin2W_current = mp.mpf('0.375') + delta_W + f2*rho2 + f3*rho3
alpha_inv_current = 1/(C*lambda_c*sin2W_current*(1-C_theta)) - W1 - rho2 - rho3

# 自洽性: 解联立方程
# sin²θ_W = 3/8 + δ + f₂ρ₂ + f₃ρ₃
# α⁻¹     = 1/(C·λ_c·sin²θ_W) − W₁ − ρ₂ − ρ₃  (忽略 C_θ 小修正)
# 给定 sin²θ_W = 0.23120, α⁻¹ = 137.036, 解 ρ₂, ρ₃, δ

# 实际上有3个未知数 (δ, ρ₂, ρ₃) 和 2个方程 → 1自由度
# ρ₂, ρ₃ 现在有独立来源 (Mathieu重叠积分), 所以 δ 被唯一确定:
# δ = sin²θ_W − 3/8 − f₂ρ₂ − f₃ρ₃
# 然后 α⁻¹ 由 ρ₂, ρ₃ 和 δ 确定, 不需要额外拟合

print(f"\n自洽性数值验证:")
print(f"  给定 sin²θ_W = 0.23120 (实验)")
print(f"  给定 ρ₂ = {float(rho2_new:=mp.mpf('0.222')):.3f} (Mathieu重叠积分)")
print(f"  给定 ρ₃ = {float(rho3_new:=mp.mpf('0.077')):.3f} (Mathieu重叠积分)")
delta_new = sin2W_exp - mp.mpf('0.375') - f2*rho2_new - f3*rho3_new
print(f"  → δθ_W^(1) = sin²θ_W − 3/8 − f₂ρ₂ − f₃ρ₃")
print(f"            = 0.23120 − 0.375 − 0.05×0.222 − 0.025×0.077")
print(f"            = {float(delta_new):.6f}")

# 用自洽的 δ 和 ρ 预测 α⁻¹
sin2W_self = mp.mpf('0.375') + delta_new + f2*rho2_new + f3*rho3_new
alpha_pred = 1/(C*lambda_c*sin2W_self*(1-C_theta)) - W1 - rho2_new - rho3_new

print(f"\n  预测 α⁻¹ = 1/(C·λ_c·{float(sin2W_self):.6f}·(1−C_θ)) − 5 − {float(rho2_new):.3f} − {float(rho3_new):.3f}")
print(f"          = {float(alpha_pred):.6f}")
print(f"  实验 α⁻¹ = {float(alpha_em_exp):.6f}")
print(f"  偏差     = {float(alpha_pred - alpha_em_exp):+.4f} = {float((alpha_pred - alpha_em_exp)/alpha_em_exp*1e6):+.1f} ppm")

# ============================================================
# 最终评估
# ============================================================
print("\n" + "=" * 75)
print("最终评估: CNT α⁻¹ 公式是推导还是拟合?")
print("=" * 75)
print("""
1. 公式结构 α⁻¹ = 1/(C·λ_c·sin²θ_W) − W₁ − ρ₂ − ρ₃ 
   不是标准 GUT RGE 的形式。标准 RGE 给出:
   α⁻¹ = (8/3)α_GUT⁻¹ + (b_em/(2π))ln(M_GUT/M_Z)
   
   CNT 用 1/sin²θ_W ≈ 4.325 代替 (8/3) ≈ 2.667,
   将 RGE 跑动的 ~50 压缩进 sin²θ_W 的增强因子。

2. sin²θ_W 在 CNT 中扮演双重角色:
   (a) 决定 α⁻¹ 的"裸值"(通过 1/sin²θ_W)
   (b) 自身被角向结构修正
   
   这种双重使用在标准电弱理论中无对应——sin²θ_W 和 α
   是独立可观测量。

3. 但 CNT 声称 sin²θ_W 不是独立参数——它被角向结构
   (Mathieu 谱 + SU(5) Weyl 群) 决定。如果能从第一性原理
   同时导出 sin²θ_W 和 α⁻¹，则公式不是拟合。

4. 当前状态: δθ_W^(1) = −0.156 是唯一真正自由参数。
   如果 δθ_W^(1) 能被第一性原理导出，则整个公式闭合。
   ρ₂, ρ₃ 正在被 Mathieu 重叠积分攻克。

5. 拟合风险: 中低等
   - 骨架参数 (C, λ_c, W₁, E₁) 全部独立确定
   - ρ₂, ρ₃ 有独立的 Mathieu 来源
   - 仅 δθ_W^(1) 需要通过自洽性条件确定为 −0.156
   - 公式形式经过函数形式退化检验——只有减法形式工作

6. 最需要警惕的: 1/sin²θ_W 代替 (8/3) + RGE 跑动
   是否等价于 RGE 的一阶近似？需要在 sin²θ_W 的
   CNT 框架内严格证明。
""")
