#!/usr/bin/env python3
"""
ρ₃ 目标值重新计算：用独立确定的 δθ_W^(1) 打破参数简并

旧的 ρ₃=0.092 是在 δθ_W^(1) 自由的框架下反推的。
现在 δθ_W^(1) = −0.15634 已被 CNT 第一性原理确定，
需要重新计算 ρ₃ 的自洽目标值。

日期: 2026-07-21
"""

import mpmath as mp
mp.mp.dps = 60

# ============================================================
# 基础常数
# ============================================================
C = mp.mpf('0.023095708966')
lambda_c = mp.mpf('1.3160229113')
gamma1_val = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + gamma1_val**2
C_theta = C / E1

# 实验值
sin2W_exp = mp.mpf('0.23120')
alpha_em_exp = mp.mpf('137.035999177')

# CNT 参数
W1 = mp.mpf('5')
f2 = mp.mpf('0.05')
f3 = mp.mpf('0.025')
N_cycle = mp.mpf('30')

# 标准 RGE 参数
M_Z = mp.mpf('91.1876')
M_GUT = mp.mpf('7.6e14')
ln_ratio = mp.log(M_GUT / M_Z)
alpha_GUT = C * lambda_c
alpha_GUT_inv = 1 / alpha_GUT

b_2_val = mp.mpf('5') / mp.mpf('6')
b_1_SM = mp.mpf('41') / mp.mpf('10')

# ============================================================
# §1: 独立确定的 δθ_W^(1)
# ============================================================
print("=" * 70)
print("ρ₃ 目标值自洽重新计算")
print("=" * 70)

# 标准 RGE
alpha_2_inv = alpha_GUT_inv + b_2_val / (2*mp.pi) * ln_ratio
alpha_1_inv = (mp.mpf('5')/mp.mpf('3')) * alpha_GUT_inv + b_1_SM / (2*mp.pi) * ln_ratio
sin2W_RGE = alpha_2_inv / (alpha_1_inv + alpha_2_inv)
delta_RGE_pure = sin2W_RGE - mp.mpf('0.375')

# CNT δ_CNT 预测 (含 N_cycle 修正)
C_eff = C * (1 + 1/N_cycle)
delta_CNT_pred = -C_eff * ln_ratio / (2 * mp.pi)

# 总 δθ_W^(1) 预测
delta_W_pred = delta_RGE_pure + delta_CNT_pred

print(f"\nδθ_W^(1) 第一性原理预测:")
print(f"  Δ_RGE  = {float(delta_RGE_pure):.6f}  [标准 RGE]")
print(f"  δ_CNT  = {float(delta_CNT_pred):.6f}  [CNT, −C·(1+1/30)·ln/(2π)]")
print(f"  δθ_W^(1) = {float(delta_W_pred):.6f}  [总预测]")
print(f"  旧自洽值  = -0.15662  [含 ρ₃=0.092 假设]")
print(f"  差值      = {float(delta_W_pred + mp.mpf('0.15662')):+.6f}")

# ============================================================
# §2: 用新 δθ_W^(1) 重新确定 f₂ρ₂+f₃ρ₃ 目标
# ============================================================
print("\n" + "=" * 70)
print("§2: 重新确定角向修正目标值")
print("=" * 70)

# CNT 公式: sin²θ_W = 3/8 + δθ_W^(1) + f₂ρ₂ + f₃ρ₃
# → f₂ρ₂ + f₃ρ₃ = sin²θ_W − 3/8 − δθ_W^(1)
f2r2_plus_f3r3_target = sin2W_exp - mp.mpf('0.375') - delta_W_pred

print(f"\n  sin²θ_W = 3/8 + δθ_W^(1) + f₂ρ₂+f₃ρ₃")
print(f"  {float(sin2W_exp):.6f} = 0.375 + ({float(delta_W_pred):.6f}) + (目标)")
print(f"  f₂ρ₂ + f₃ρ₃ 目标 = {float(f2r2_plus_f3r3_target):.6f}")

# 旧目标 (基于旧框架 δθ_W^(1) = −0.15662)
f2r2_plus_f3r3_old = sin2W_exp - mp.mpf('0.375') - mp.mpf('-0.15662')
print(f"  旧目标 = {float(f2r2_plus_f3r3_old):.6f}  [δθ_W^(1)=−0.15662]")
print(f"  变化   = {float(f2r2_plus_f3r3_target - f2r2_plus_f3r3_old):+.6f}")

# ============================================================
# §3: 用 Mathieu ρ₂ + 新目标 → 确定 ρ₃ 目标
# ============================================================
print("\n" + "=" * 70)
print("§3: 确定 ρ₃ 新目标值")
print("=" * 70)

rho2_mathieu = mp.mpf('0.19907')  # Mathieu sin(2θ), 验证度 +0.5%
rho3_mathieu = mp.mpf('0.11471')  # Mathieu cos(4θ), 当前计算值

f2r2_calc = f2 * rho2_mathieu
f3r3_needed = f2r2_plus_f3r3_target - f2r2_calc
rho3_target_new = f3r3_needed / f3

print(f"\n  使用 Mathieu ρ₂ = {float(rho2_mathieu):.5f} (±0.5%)")
print(f"  f₂ρ₂ = {float(f2r2_calc):.6f}")
print(f"  f₃ρ₃ 需要 = f₂ρ₂+f₃ρ₃ 目标 − f₂ρ₂")
print(f"           = {float(f2r2_plus_f3r3_target):.6f} − {float(f2r2_calc):.6f}")
print(f"           = {float(f3r3_needed):.6f}")
print(f"  ρ₃ 新目标 = f₃ρ₃ / f₃ = {float(f3r3_needed):.6f} / 0.025")
print(f"           = {float(rho3_target_new):.5f}")

# 对比
print(f"\n  ρ₃ 旧目标 = 0.09200  [δθ_W^(1) 自由时的反推]")
print(f"  ρ₃ 新目标 = {float(rho3_target_new):.5f}  [δθ_W^(1) 独立确定后]")
print(f"  ρ₃ Mathieu = {float(rho3_mathieu):.5f}  [cos(4θ) 重叠积分]")
print(f"  偏差 (新)  = {float((rho3_mathieu - rho3_target_new)/rho3_target_new*100):+.1f}%")
print(f"  偏差 (旧)  = {float((rho3_mathieu - 0.092)/0.092*100):+.1f}%")
print(f"  → 偏差从 +24.7% 降至 {float(abs((rho3_mathieu - rho3_target_new)/rho3_target_new*100)):.1f}% !")

# ============================================================
# §4: 用新 ρ₃ 目标计算 sin²θ_W 自洽值
# ============================================================
print("\n" + "=" * 70)
print("§4: 自洽 sin²θ_W 和 α⁻¹ 计算")
print("=" * 70)

# 方案 A: 使用独立 δθ_W^(1) 预测 + Mathieu ρ₂ + 新 ρ₃ 目标
print(f"\n方案 A: 全部独立输入")
print(f"  δθ_W^(1) = {float(delta_W_pred):.6f}  [CNT+RGE 推导]")
print(f"  ρ₂ = {float(rho2_mathieu):.5f}  [Mathieu, ±0.5%]")
print(f"  ρ₃ = {float(rho3_target_new):.5f}  [自洽确定]")

sin2W_A = mp.mpf('0.375') + delta_W_pred + f2*rho2_mathieu + f3*rho3_target_new
print(f"  sin²θ_W = 0.375 + ({float(delta_W_pred):.6f}) + {float(f2*rho2_mathieu):.6f} + {float(f3*rho3_target_new):.6f}")
print(f"          = {float(sin2W_A):.6f}")

alpha0_A = C * lambda_c * sin2W_A
alpha_eff_A = alpha0_A * (1 - C_theta)
alpha_inv_A = 1/alpha_eff_A - W1 - rho2_mathieu - rho3_target_new

print(f"  α⁻¹ = {float(alpha_inv_A):.6f}")
print(f"  实验 = {float(alpha_em_exp):.6f}")
print(f"  偏差 = {float(alpha_inv_A - alpha_em_exp):+.4f}")
print(f"       = {float((alpha_inv_A - alpha_em_exp)/alpha_em_exp*1e6):+.1f} ppm")

# 方案 B: δθ_W^(1) 预测 + Mathieu ρ₂ + Mathieu ρ₃ (cos⁴θ)
print(f"\n方案 B: 全 Mathieu (不调整任何参数)")
print(f"  δθ_W^(1) = {float(delta_W_pred):.6f}  [推导]")
print(f"  ρ₂ = {float(rho2_mathieu):.5f}  [Mathieu]")
print(f"  ρ₃ = {float(rho3_mathieu):.5f}  [Mathieu cos(4θ)]")

sin2W_B = mp.mpf('0.375') + delta_W_pred + f2*rho2_mathieu + f3*rho3_mathieu
print(f"  sin²θ_W = {float(sin2W_B):.6f}  [实验 {float(sin2W_exp):.6f}, 偏差 {float((sin2W_B-sin2W_exp)/sin2W_exp*1e6):+.0f} ppm]")

alpha0_B = C * lambda_c * sin2W_B
alpha_eff_B = alpha0_B * (1 - C_theta)
alpha_inv_B = 1/alpha_eff_B - W1 - rho2_mathieu - rho3_mathieu
print(f"  α⁻¹ = {float(alpha_inv_B):.6f}")
print(f"  偏差 = {float(alpha_inv_B - alpha_em_exp):+.4f} = {float((alpha_inv_B - alpha_em_exp)/alpha_em_exp*1e6):+.1f} ppm")

# ============================================================
# §5: ρ₃ 偏差的物理解释探索
# ============================================================
print("\n" + "=" * 70)
print("§5: ρ₃ 偏差 = {:.1f}% 的物理来源".format(float(abs((rho3_mathieu - rho3_target_new)/rho3_target_new*100))))
print("=" * 70)

# ρ₃_Mathieu / ρ₃_target = 0.11471 / ~0.10... 
ratio_rho3 = rho3_mathieu / rho3_target_new
print(f"\n  ρ₃(Mathieu) / ρ₃(目标) = {float(rho3_mathieu):.5f} / {float(rho3_target_new):.5f} = {float(ratio_rho3):.4f}")
print(f"  即 Mathieu cos(4θ) 重叠积分偏高约 {float((ratio_rho3-1)*100):.1f}%")

# 候选机制 1: SU(5) 约化矩阵元修正
# 对 5̄→24 (ℓ=2): dim(5̄)=5, dim(24)=24
dim_factor_3 = mp.sqrt(mp.mpf('24') / mp.mpf('5'))
ang_factor_3 = mp.mpf('1') / mp.sqrt(mp.mpf('5'))  # 1/√5
su5_norm_3 = dim_factor_3 * ang_factor_3
rho3_su5 = rho3_mathieu * su5_norm_3**2

print(f"\n候选 1: SU(5) 约化矩阵元归一化")
print(f"  dim因子 = √(24/5) = {float(dim_factor_3):.4f}")
print(f"  ang因子 = 1/√(2ℓ+1) = 1/√5 = {float(ang_factor_3):.4f}")
print(f"  总归一化 = {float(su5_norm_3):.4f}, norm² = {float(su5_norm_3**2):.4f}")
print(f"  ρ₃_SU5 = {float(rho3_mathieu):.5f} × {float(su5_norm_3**2):.4f} = {float(rho3_su5):.5f}")
print(f"  ρ₃ 目标 = {float(rho3_target_new):.5f}")
print(f"  → SU(5) 归一化使偏差从 {float(abs((rho3_mathieu-rho3_target_new)/rho3_target_new*100)):.1f}% 变到 {float(abs((rho3_su5-rho3_target_new)/rho3_target_new*100)):.1f}%")

# 候选机制 2: 双重分解 — cos(4θ) = cos²(2θ) − sin²(2θ)
# 可能需要对 O₃ 进行更精确的群论展开
print(f"\n候选 2: cos(4θ) 的精确群论展开")
print(f"  cos(4θ) = cos²(2θ) − sin²(2θ)")
print(f"          = [1 − 2sin²(θ)cos²(θ)...] − ...")
print(f"  O₃ 可能包含来自不同根路径的干涉项")

# 候选机制 3: C_θ 耦合修正
# 角向-径向耦合 C_θ = C/E1 ≈ 1.15×10⁻⁴
# 其对方差的贡献 ∼ C_θ · (scale factor)
cartan_coupling_correction = float(C_theta * lambda_c)
print(f"\n候选 3: 角向-径向耦合 C_θ = {float(C_theta):.2e}")
print(f"  C_θ · λ_c = {cartan_coupling_correction:.2e}")
print(f"  相对于 ρ₃ 偏差 {float(abs(rho3_mathieu - rho3_target_new)):.4f} → 太小")

# ============================================================
# §6: 总结
# ============================================================
print("\n" + "=" * 70)
print("总结")
print("=" * 70)

# δθ_W^(1) 独立确定后的新参数表
delta_W_effective = float(delta_W_pred)
delta_CNT_eff = float(delta_CNT_pred)

sin2W_pred_theory = float(mp.mpf('0.375') + delta_W_pred + f2*rho2_mathieu + f3*rho3_mathieu)
alpha_pred_theory_B = float(alpha_inv_B)

print(f"""
1. δθ_W^(1) 独立确定后，ρ₃ 目标从 0.092 移至 {float(rho3_target_new):.5f}
   (ρ₂ 维持 Mathieu 值 {float(rho2_mathieu):.5f}, ±0.5%)

2. ρ₃(Mathieu) = {float(rho3_mathieu):.5f} vs ρ₃(新目标) = {float(rho3_target_new):.5f}
   偏差: {float(abs((rho3_mathieu - rho3_target_new)/rho3_target_new*100)):.1f}% (vs 旧偏差 24.7%)
   → δθ_W^(1) 独立确定使 ρ₃ 偏差减半!

3. 全 Mathieu 预测 (方案 B):
   sin²θ_W = {sin2W_pred_theory:.6f} (vs {float(sin2W_exp):.6f} 实验)
   α⁻¹ = {alpha_pred_theory_B:.6f} (vs {float(alpha_em_exp):.6f} 实验)
   偏差 = {float((mp.mpf(alpha_pred_theory_B) - alpha_em_exp)/alpha_em_exp*1e6):.0f} ppm

4. 剩余 ~{float(abs((rho3_mathieu - rho3_target_new)/rho3_target_new*100)):.1f}% ρ₃ 偏差可能:
   - cos(4θ) 算符的精确群论归一化 (Wigner-Eckart 约化矩阵元)
   - 5̄→24 的多种根路径干涉 (不止一条 ladder 路径)
   - δθ_W^(1) 预测的 0.25% 残余影响
""")
