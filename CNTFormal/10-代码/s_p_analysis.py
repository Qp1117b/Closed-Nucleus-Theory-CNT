#!/usr/bin/env python3
"""
s_p 标度因子的第一性模式分析
=============================
探索 s_p = {0.508952, 2.707312, 0.357170} 的数学来源
"""
import mpmath as mp
import itertools
mp.mp.dps = 60

# ═══════════════════════════════════════════════════════════════
# CNT 核心常数
# ═══════════════════════════════════════════════════════════════
C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = mp.mpf('0.25') + gamma_1**2

def compute_q_c(depth=60):
    def tail(q, k):
        if k > depth: return mp.mpf('0')
        n = 2*k + 1
        return q**2 / (n**2 - 2*q - tail(q, k+1))
    return mp.findroot(lambda q: 1 - 3*q - tail(q, 1), (29 - mp.sqrt(661))/10)
q_c = compute_q_c(60)
λ_c = 4*q_c

def Γ_p(p, s):
    """p-adic Gamma function: Γ_p(s) = (1-p^{s-1})/(1-p^{-s})"""
    return (1 - p**(s-1)) / (1 - p**(-s))

# α_p IR values
α = {2: mp.mpf('1.544317'), 3: mp.mpf('0.430377'), 5: mp.mpf('0.841413')}

# Observed s_p (from yukawa_fp.py)
s_obs = {2: mp.mpf('0.357170'), 3: mp.mpf('2.707312'), 5: mp.mpf('0.508952')}

print("="*72)
print("  s_p 标度因子 — 第一性模式分析")
print("="*72)

# ═══════════════════════════════════════════════════════════════
# 1. Γ_p(1-α_p) prefactor
# ═══════════════════════════════════════════════════════════════
print("\n【1】p-adic Gamma Prefactor Γ_p(1-α_p)")
Γ_vals = {}
Γ_abs = {}
for p in [2, 3, 5]:
    g = Γ_p(p, 1-α[p])
    Γ_vals[p] = g
    Γ_abs[p] = abs(g)
    print(f"  Γ_{p}(1-α_{p}) = {float(g):.10f}, |Γ| = {float(abs(g)):.10f}")

# S_p = s_p × Γ_p(1-α_p)
print("\n【2】S_p = s_p × Γ_p(1-α_p)")
S = {}
for p in [2, 3, 5]:
    S[p] = s_obs[p] * Γ_abs[p]
    print(f"  S_{p} = s_{p} × |Γ_{p}| = {float(s_obs[p]):.8f} × {float(Γ_abs[p]):.8f} = {float(S[p]):.10f}")

# Ratios
print("\n【3】S_p 比值")
r32 = S[3]/S[2]
r52 = S[5]/S[2]
r35 = S[3]/S[5]
print(f"  S_3/S_2 = {float(r32):.10f}  (9/2 = 4.5, 偏差 {float((r32-4.5)/4.5*100):+.6f}%)")
print(f"  S_5/S_2 = {float(r52):.10f}  (3/1 = 3.0, 偏差 {float((r52-3)/3*100):+.6f}%)")
print(f"  S_3/S_5 = {float(r35):.10f}  (3/2 = 1.5, 偏差 {float((r35-1.5)/1.5*100):+.6f}%)")

# ═══════════════════════════════════════════════════════════════
# 4. s_3 假设检验: s_3 = 2 + 1/√2
# ═══════════════════════════════════════════════════════════════
print("\n【4】s_3 = 2 + 1/√2 假设检验")
hyp_3 = 2 + 1/mp.sqrt(2)
dev_3 = (s_obs[3] - hyp_3) / s_obs[3] * 100
print(f"  s_3 (观测)     = {float(s_obs[3]):.10f}")
print(f"  2 + 1/√2       = {float(hyp_3):.10f}")
print(f"  偏差           = {float(dev_3):+.6f}%")

# 其他候选
candidates_3 = [
    ("e", mp.e),
    ("√(2π)", mp.sqrt(2*mp.pi)),
    ("2 + 1/√e", 2 + 1/mp.sqrt(mp.e)),
    ("π²/π+1", mp.pi**2/(mp.pi+1)),
    ("(3√2)", 3*mp.sqrt(2)),
    ("ζ(3)+2", mp.zeta(3) + 2),
]
for name, val in candidates_3:
    dev = (s_obs[3] - val) / s_obs[3] * 100
    print(f"  s_3 ≈ {name:<12} = {float(val):.10f}  偏差 {float(dev):+.6f}%")

# ═══════════════════════════════════════════════════════════════
# 5. s_2 假设检验: s_2 = 5/14
# ═══════════════════════════════════════════════════════════════
print("\n【5】s_2 = 5/14 假设检验")
hyp_2_a = mp.mpf(5)/14
dev_2a = (s_obs[2] - hyp_2_a) / s_obs[2] * 100
print(f"  s_2 (观测)     = {float(s_obs[2]):.10f}")
print(f"  5/14            = {float(hyp_2_a):.10f}")
print(f"  偏差           = {float(dev_2a):+.6f}%")

candidates_2 = [
    ("1/(2√2)", 1/(2*mp.sqrt(2))),
    ("√2/4", mp.sqrt(2)/4),
    ("1/(e√2)", 1/(mp.e*mp.sqrt(2))),
    ("2/π²", 2/mp.pi**2),
    ("C/λ_c", C/λ_c),
    ("λ_c/4", λ_c/4),
    ("C*E_1/100", C*E_1/100),
    ("Γ(3/4)/π", mp.gamma(mp.mpf('0.75'))/mp.pi),
]
for name, val in candidates_2:
    dev = (s_obs[2] - val) / s_obs[2] * 100
    print(f"  s_2 ≈ {name:<12} = {float(val):.10f}  偏差 {float(dev):+.6f}%")

# ═══════════════════════════════════════════════════════════════
# 6. s_5 假设检验
# ═══════════════════════════════════════════════════════════════
print("\n【6】s_5 假设检验")
print(f"  s_5 (观测)     = {float(s_obs[5]):.10f}")

candidates_5 = [
    ("e^{-1/√2}", mp.e**(-1/mp.sqrt(2))),
    ("e^{-√2/2}", mp.e**(-mp.sqrt(2)/2)),
    ("e^{-π/4}", mp.e**(-mp.pi/4)),
    ("1/(π√2)", 1/(mp.pi*mp.sqrt(2))),
    ("1/(2√π)", 1/(2*mp.sqrt(mp.pi))),
    ("2/e²", 2/mp.e**2),
    ("ln(2)/√2", mp.log(2)/mp.sqrt(2)),
    ("C/2", C/2),
    ("λ_c/2π", λ_c/(2*mp.pi)),
    ("λ_c/2.58", λ_c/2.58),
    ("1/(1+3C)-1/2", (1/(1+3*C))**2),
]
for name, val in candidates_5:
    dev = (s_obs[5] - val) / s_obs[5] * 100
    print(f"  s_5 ≈ {name:<12} = {float(val):.10f}  偏差 {float(dev):+.6f}%")

# ═══════════════════════════════════════════════════════════════
# 7. 系统搜索: s_p 表示为 CNT 常数的代数组合
# ═══════════════════════════════════════════════════════════════
print("\n【7】系统搜索: s_p 与基本常数的关系")
constants = {
    'C': C, 'E1': E_1, 'λc': λ_c, 'qc': q_c,
    'C/E1': C/E_1, 'C*E1': C*E_1,
    '√(4πCλc)': mp.sqrt(4*mp.pi*C*λ_c),
    '1/(1+3C)': 1/(1+3*C),
    '1/α_cnt': mp.mpf('137.02127778'),
}

import itertools as it
for name, val in constants.items():
    print(f"  {name:<12} = {float(val):.15f}")

# 搜索 s_p 与 Γ_p 乘积的简单有理近似
print("\n【8】S_p = s_p × |Γ_p| 的有理近似")
from fractions import Fraction
for p in [2, 3, 5]:
    sp = s_obs[p]
    gp = Γ_abs[p]
    prod = sp * gp
    frac = Fraction(float(prod)).limit_denominator(100)
    print(f"  S_{p} = {float(prod):.10f} ≈ {frac} = {float(frac):.10f}  (偏差 {float((prod-float(frac))/prod*100):+.6f}%)")

# ═══════════════════════════════════════════════════════════════
# 9. 探索 s_p 是否为 Γ_p(1-α_p)/γ 的简单组合
# ═══════════════════════════════════════════════════════════════
print("\n【9】跨扇区关系")
print("  s_p × Γ_p = S_p 的比值分析:")
print(f"    S_3 : S_5 : S_2 = {float(S[3]/S[2]):.6f} : {float(S[5]/S[2]):.6f} : 1")
print(f"    精确 {9/2}:{3}:{1} = 4.5 : 3 : 1")

# 检查 s_p 与 p-adic 量的关系
for p in [2, 3, 5]:
    sp = s_obs[p]
    gp = Γ_abs[p]
    print(f"\n  p={p}:")
    print(f"    s_p = {float(sp):.10f}")
    print(f"    Γ_p(1-α_p) = {float(gp):.10f}")
    print(f"    s_p × Γ_p = {float(sp*gp):.10f}")
    print(f"    ln(s_p) = {float(mp.log(sp)):.10f}")
    print(f"    ln(Γ_p) = {float(mp.log(gp)):.10f}")
    # 检验是否 s_p = p^{b(1-α_p)} for some base b
    for b in range(-5, 6):
        pred = p ** (b * (1 - α[p]))
        dev = (sp - pred) / sp * 100
        if abs(float(dev)) < 5:
            print(f"    s_p ≈ p^{{{b}(1-α_{p})}} = {float(pred):.10f}  偏差 {float(dev):+.3f}%")
    # 检验 s_p ∝ 1/Γ_p 关系
    inv_g = 1/gp
    dev = (sp - inv_g) / sp * 100
    print(f"    s_p vs 1/Γ_p = {float(inv_g):.10f}  偏差 {float(dev):+.3f}%")

# ═══════════════════════════════════════════════════════════════
# 10. 关键模式: s_p / s_q 与 mod(p)/mod(q) 关系
# ═══════════════════════════════════════════════════════════════
print("\n【10】s_p 与 mod(p) 等 SU(5) 量的关系")
mod_p = {2: 4, 3: 6, 5: 18}
W_m = {2: 5, 3: 10, 5: 20}
Cartan = {2: 1, 3: 4, 5: 9}  # 注意: p=2→1, p=3→4, p=5→9 但扇区映射不同

for p in [2, 3, 5]:
    print(f"  p={p}: s_p={float(s_obs[p]):.6f}, mod(p)={mod_p[p]}, W_m={W_m[p]}, Cartan={Cartan[p]}")

# 检查 s_p/s_q ≈ mod(p)/mod(q) 等
print()
for (p,q) in [(2,3), (2,5), (3,5)]:
    print(f"  s_{p}/s_{q} = {float(s_obs[p]/s_obs[q]):.6f}, mod({p})/mod({q}) = {mod_p[p]/mod_p[q]:.6f}")
    print(f"  W_{p}/W_{q} = {W_m[p]/W_m[q]:.6f}")
    print(f"  Cartan_{p}/Cartan_{q} = {Cartan[p]/Cartan[q]:.6f}")

# ═══════════════════════════════════════════════════════════════
# 11. 探索 S_p 与 CNT 常数的直接关系
# ═══════════════════════════════════════════════════════════════
print("\n【11】搜索 S_p 与 CNT 常数的代数关系")
# 尝试 S_2 = 1/2?  S_5 = 3/2?  S_3 = 9/4?
print(f"  1/2  = {float(mp.mpf('0.5')):8f}   S_2 = {float(S[2]):.8f}  偏差 {(S[2]/mp.mpf('0.5')-1)*100:+.6f}%")
print(f"  3/2  = {float(mp.mpf('1.5')):8f}   S_5 = {float(S[5]):.8f}  偏差 {(S[5]/mp.mpf('1.5')-1)*100:+.6f}%")
print(f"  9/4  = {float(mp.mpf('2.25')):8f}   S_3 = {float(S[3]):.8f}  偏差 {(S[3]/mp.mpf('2.25')-1)*100:+.6f}%")

# 尝试 S_2 = π/2π?  S_2 = (C·E₁/λ_c)/something
candidates_S = [
    ("S_2 = π/6", mp.pi/6),
    ("S_2 = 1/√π", 1/mp.sqrt(mp.pi)),
    ("S_2 = Γ(5/4)/Γ(3/4)", mp.gamma(mp.mpf('1.25'))/mp.gamma(mp.mpf('0.75'))),
]
for name, val in candidates_S:
    dev = (S[2] - val)/S[2]*100
    print(f"  {name} = {float(val):.8f}  偏差 {float(dev):+.6f}%")

# ═══════════════════════════════════════════════════════════════
# 12. 核心发现总结
# ═══════════════════════════════════════════════════════════════
print("\n" + "="*72)
print("  核心发现总结")
print("="*72)

# S_p ratio to {9/2, 3, 1}
target = {3: mp.mpf('4.5'), 5: mp.mpf('3'), 2: mp.mpf('1')}
print(f"\n  S_p = s_p × Γ_p(1-α_p) 的比值:")
for p in [3, 5, 2]:
    predicted = S[2] * target[p]
    deviation = (S[p] - predicted) / predicted * 100
    print(f"    S_{p} = {S[p]:.8f} 期望 = {target[p]}×S_2 = {predicted:.8f} 偏差 {deviation:+.6f}%")

# s_3 = 2 + 1/√2 precision
print(f"\n  s_3 = 2 + 1/√2 偏差: {float(dev_3):+.6f}%")
print(f"  s_2 = 5/14    偏差: {float(dev_2a):+.6f}%")

# Is s_3 exactly 2 + 1/√2? Compute s_3 - (2 + 1/√2)
diff_3 = s_obs[3] - (2 + 1/mp.sqrt(2))
print(f"\n  s_3 - (2 + 1/√2) = {float(diff_3):.2e}")

# The difference is 2.05e-4. What is this?
# Compare to C = 0.023, C² = 5.34e-4, C²/2 = 2.67e-4
print(f"  C             = {float(C):.6e}")
print(f"  C²            = {float(C**2):.6e}")
print(f"  C²/2          = {float(C**2/2):.6e}")
print(f"  C/100         = {float(C/100):.6e}")
# Maybe the residual is related to the RG running correction?
delta_α_p = {2: -0.0381, 3: 0.0254, 5: -0.0071}
for p in [3]:
    corr = delta_α_p[p] * mp.log(p)
    print(f"  Δα_{p}·ln({p}) = {float(corr):.6e}")
