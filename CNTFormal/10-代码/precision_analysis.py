#!/usr/bin/env python3
"""CNT 精度瓶颈追踪: 40 ppm α⁻¹ 偏差的逐项分解"""

import mpmath as mp
mp.mp.dps = 60

# === 数论核心 ===
gamma_euler = mp.euler
C = 1 + gamma_euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = mp.mpf('0.25') + gamma_1**2
C_th = C / E_1

# === 连分数 ===
def tail(q, k, max_d=30):
    if k > max_d: return mp.mpf('0')
    n_k = 2*k + 1
    return q**2/(n_k**2 - 2*q - tail(q, k+1, max_d))

q_c = mp.findroot(lambda q: 1-3*q-tail(q,1,30), (29-mp.sqrt(661))/10)
lambda_c = 4 * q_c
I = mp.mpf(5)/3

# === 角向修正 ===
f2, f3 = mp.mpf('0.05'), mp.mpf('0.025')
rho2, rho3 = mp.mpf('0.198'), mp.mpf('0.092')
delta_W = mp.mpf('-0.156')

sin2W_GUT = mp.mpf(3)/8
sin2W_MZ = sin2W_GUT + delta_W + f2*rho2 + f3*rho3

# === α⁻¹ 分步追踪 ===
alpha_0 = C * lambda_c * sin2W_MZ
alpha_0_eff = alpha_0 * (1 - C_th)
alpha_0_inv = 1/alpha_0_eff
alpha_inv = alpha_0_inv - 5 - rho2 - rho3

print("="*60)
print("  CNT α⁻¹ = 40 ppm 偏差 → 逐项追踪")
print("="*60)

items = [
    ("C = ξ'(1)/ξ(1)", C),
    ("λ_c = 4·q_c", lambda_c),
    ("E_1 = 1/4+γ₁²", E_1),
    ("C_th = C/E_1", C_th),
    ("sin²θ_W(GUT) = 3/8", sin2W_GUT),
    ("δθ_W^(1) [唯象]", delta_W),
    ("f₂·ρ₂", f2*rho2),
    ("f₃·ρ₃", f3*rho3),
    ("sin²θ_W(M_Z)", sin2W_MZ),
    ("α₀ = C·λ_c·sin²θ_W", alpha_0),
    ("α₀^eff = α₀·(1-C_th)", alpha_0_eff),
    ("1/α₀^eff", alpha_0_inv),
    ("-5 - ρ₂ - ρ₃", -5 - rho2 - rho3),
    ("α⁻¹ (CNT)", alpha_inv),
]

for name, val in items:
    print(f"  {name:<30} = {float(val):.12f}")

target = mp.mpf('137.035999084')
dev = float(alpha_inv - target)
print(f"\n  实验 α⁻¹            = 137.035999084")
print(f"  CNT α⁻¹             = {float(alpha_inv):.8f}")
print(f"  偏差                 = {dev:.8f}")
print(f"  偏差 (ppm)           = {float(dev/target*1e6):.1f}")

# === 灵敏度分析 ===
print("\n" + "="*60)
print("  灵敏度分析：要消掉40 ppm，各参数需变多少？")
print("="*60)

# δ/δC
d_alpha_dC = lambda_c * sin2W_MZ * (1 - C_th) - alpha_0 * (-1/E_1)
delta_C_needed = -dev / float(d_alpha_dC)
print(f"  仅调 C：         ΔC = {float(delta_C_needed):.2e}  ({float(delta_C_needed/C*1e6):.1f} ppm)")

# δ/δλ_c
d_alpha_dlc = C * sin2W_MZ * (1 - C_th)
delta_lc_needed = -dev / float(d_alpha_dlc)
print(f"  仅调 λ_c：       Δλ_c = {float(delta_lc_needed):.2e}  ({float(delta_lc_needed/lambda_c*1e6):.1f} ppm)")

# δ/δ rho2 (if rho2 shifts α by ~1)
# α_inv ≈ 1/(α₀_eff) - const - rho_2 - rho_3
# ∂α⁻¹/∂ρ₂ = -1
delta_rho2 = float(target - alpha_inv)  # sign: need to increase rho2 slightly
print(f"  仅调 ρ₂：        Δρ₂ = {delta_rho2:.4f}  ({delta_rho2/float(rho2)*100:.2f}%)")

# 需要多少 sin²θ_W 变化？
sin2W_needed = 1/(C*lambda_c*(1-C_th)*(target + 5 + rho2 + rho3))
delta_sin2W = float(sin2W_needed - sin2W_MZ)
print(f"  仅调 sin²θ_W：   Δsin²θ_W = {delta_sin2W:.2e}  ({delta_sin2W/float(sin2W_MZ)*1e6:.1f} ppm)")
print(f"    → 需 δθ_W^(1) = {float(sin2W_needed - sin2W_GUT - f2*rho2 - f3*rho3):.6f}")
print(f"    → 当前 δθ_W^(1) = {float(delta_W):.4f}, 差 = {float(sin2W_needed - sin2W_MZ):.2e}")

# 高阶角向贡献
print(f"\n  rho4=0.058, f4=0.0125 → f4·rho4 = {0.058*0.0125:.6f}")
print(f"  进入 sin2W 后 α⁻¹ 变化 ≈ {0.058*0.0125/float(C*lambda_c*(1-C_th)):.2f}")

# === G_N 偏差追踪 ===
print("\n" + "="*60)
print("  G_N 偏差追踪")
print("="*60)
m_p = mp.mpf('0.93827208816')
pre_exp = I*lambda_c*C**2*E_1 / m_p**2
exp_factor = mp.exp(-2/C)
G_N = pre_exp * exp_factor
G_N_exp = mp.mpf('6.70883e-39')

print(f"  前置因子 I·λ_c·C²·E₁/m_p² = {float(pre_exp):.6e}")
print(f"  指数因子 exp(-2/C)          = {float(exp_factor):.6e}")
print(f"  G_N (CNT)  = {float(G_N):.4e}")
print(f"  G_N (exp)  = {float(G_N_exp):.4e}")
print(f"  偏差        = {(float(G_N)-float(G_N_exp))/float(G_N_exp)*100:.2f}%")

# 对指数敏感度
delta_ln_G = 2/C**2  # d(ln G_N)/dC = d/dC(-2/C + ln(pre_exp))
# ∂G_N/∂C: G_N ∝ C²·exp(-2/C)
# ln G_N = const + 2ln(C) - 2/C
# dlnG_N/dC = 2/C + 2/C² = 2(C+1)/C²
print(f"  ∂ln(G_N)/∂C = {float(2*(C+1)/C**2):.2f}")
print(f"  → C 变动 1% 约使 G_N 变动 {float(2*(C+1)/C**2)/100:.1f}%")

# === 精度瓶颈总结 ===
print("\n" + "="*60)
print("  精度瓶颈总结")
print("="*60)
print(f"""
  1. α⁻¹ 的 40 ppm 偏差等价于:
     - sin²θ_W 需变 {float(delta_sin2W):.1e} ({float(delta_sin2W/float(sin2W_MZ)*1e6):.0f} ppm)
     - 或 ρ₂ 需变 {delta_rho2:.4f} ({delta_rho2/float(rho2)*100:.2f}%)  
     - 或 ρ₃ 需变 {delta_rho2:.4f} ({delta_rho2/float(rho3)*100:.2f}%)

  2. 物理来源 (按可能重要性排序):
     (a) 角向谱的精确计算 — ρ₂,ρ₃ 需从 Mathieu 方程第一性导出
     (b) 高阶角向修正 — ρ₄,ρ₅,... 的累积效应
     (c) C_th 修正因子 — (1-C_th) 是一阶近似, 可能漏高阶项
     (d) 费米子质量分裂效应 — SU(5) 破缺后的质量修正

  3. G_N 的 -2.3% 偏差等价于 C 变动 ~{float(-0.023/float(2*(C+1)/C**2)*100):.1f}%
     - 主要来源: exp(-2/C) 指数严重放大 C 的微小不确定度
     - 如果 C 的精密度是 1 ppm, G_N 不确定度约 {float(2*(C+1)/C**2)*1e-6*100:.2f}%

  4. 关键路径:
     - 攻克 Mathieu 角向谱 → 消除 ρ_m 的非第一性
     - 严格证明 C = ∏c_p → 消除 p进不确定度
     - 这两步补上, 其余 40 ppm 可能自动消失
""")
