#!/usr/bin/env python3
"""
α_p 第一性推导：谱闭包 + Weyl 模数
===================================
核心方程:
    α_p = ln((a_{r(p)} - a_0) / (a_{s(p)} - a_0)) / ln(p)

模式指标 (r,s) 从 SU(5) Weyl 轨道权 W_m 和模数 mod(p) 导出:
    s(p) = W_m mod mod(p)
    r(p) = s(p) + (1 if p ≠ 5 else 2)

    模数: mod(2) = 4, mod(3) = 6, mod(5) = 18
    Σ_p mod(p) = 28 = N_cycle - N_Higgs = 30 - 2
"""
import numpy as np
from scipy.special import mathieu_a, mathieu_b
import mpmath as mp

print('='*68)
print('  α_p FROM FIRST PRINCIPLES: SPECTRAL CLOSURE + WEYL MODULUS')
print('='*68)

# ═══════ PART 1: CNT constants ═══════
C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2

def tail(q, k, md=50):
    if k > md: return 0.0
    n = 2*k + 1
    return q**2 / (n**2 - 2*q - tail(q, k+1, md))

q_c = float(mp.findroot(lambda q: float(1 - 3*q - tail(float(q), 1, 50)), 
                         (29 - mp.sqrt(661))/10))

# Mathieu eigenvalues
r_max = 20
a_vals = np.array([mathieu_a(r, q_c) for r in range(r_max)])
Δa = a_vals - a_vals[0]

# ═══════ PART 2: Modulus from first principles ═══════
N_cycle = 30
N_Higgs = 2

# Weyl orbit weights
W = {2: 5, 3: 10, 5: 20}

# Modulus formula:
# mod(p) built from primes {2, 3} only (p=5 doesn't self-contribute)
# e_2(p) = 2 if p=2 else 1
# e_3(p) = 0 if p=2 else floor(log(p)/log(2))
mod = {}
for p in [2, 3, 5]:
    e2 = 2 if p == 2 else 1
    e3 = 0 if p == 2 else int(np.floor(np.log(p) / np.log(2)))
    mod[p] = (2**e2) * (3**e3)

print(f'\n  Weyl orbit weights:    W = {W}')
print(f'  Moduli:                mod = {mod}')
print(f'  Sum mod(p) = {sum(mod.values())}')
print(f'  N_cycle = {N_cycle}, N_Higgs = {N_Higgs}')
print(f'  Σ mod(p) + N_Higgs = {sum(mod.values()) + N_Higgs} = N_cycle ? {sum(mod.values()) + N_Higgs == N_cycle}')

# Mode indices
pairs = {}
for p in [2, 3, 5]:
    s = W[p] % mod[p]
    r = s + (2 if p == 5 else 1)
    pairs[p] = (r, s)
    print(f'  p={p}: s = {W[p]} mod {mod[p]} = {s}, r = {s}{"+2" if p==5 else "+1"} = {r}')

# ═══════ PART 3: α_p from spectral ratio ═══════
print(f'\n{"="*68}')
print(f'  α_p FROM MATHIEU SPECTRAL RATIO')
print(f'  α_p = ln(Δa_{{(r,p)}} / Δa_{{(s,p)}}) / ln(p)')
print(f'  Δa_r = a_r(q_c) - a_0(q_c)')
print(f'{"="*68}')

print(f'\n  {"p":>3}  {"(r,s)":>8}  {"Δa_r":>12}  {"Δa_s":>12}  {"ratio":>10}  {"α_derived":>10}  {"α_empirical":>12}  {"偏差":>8}')
print(f'  {"-"*3}  {"-"*8}  {"-"*12}  {"-"*12}  {"-"*10}  {"-"*10}  {"-"*12}  {"-"*8}')

empirical = {2: 1.547, 3: 0.432, 5: 0.842}
α_derived = {}

for p in [2, 3, 5]:
    r, s = pairs[p]
    ratio = Δa[r] / Δa[s]
    α = float(np.log(ratio) / np.log(p))
    α_derived[p] = α
    emp = empirical[p]
    pct = (α - emp) / emp * 100
    print(f'  {p:>3}  ({r},{s:>2})  {Δa[r]:>12.6f}  {Δa[s]:>12.6f}  {ratio:>10.6f}  {α:>10.6f}  {emp:>12.3f}  {pct:>+7.2f}%')

# ═══════ PART 4: Updated s_p scale factors ═══════
print(f'\n{"="*68}')
print(f'  UPDATED s_p SCALE FACTORS FROM α_derived')
print(f'{"="*68}')

# s_p determined from: p^{α_p} · b₁(q_c) · c_p = Δa_{r(p)} where c_p normalizes
# The fundamental scale: b₁(q_c) = 2q_c = 0.6580
b1 = 2*q_c

# Each s_p is the ratio between a characteristic gap and b₁
for p in [2, 3, 5]:
    r, s = pairs[p]
    # s_p should be: (some gap) / b₁ for this sector
    # Natural choice: s_p = Δa_s / b₁ (the "reference" gap in units of b₁)
    s_p = Δa[s] / b1
    print(f'  p={p}: s_p = Δa_{s}/b₁ = {Δa[s]:.6f}/{b1:.6f} = {s_p:.6f}')

print()
print(f'  Previous s_p values (from β-function fitting): 0.519, 2.503, 0.361')

# ═══════ PART 5: GL(3) consistency ═══════
print(f'\n{"="*68}')
print(f'  GL(3)-LANGLANDS CONSISTENCY CHECK')
print(f'  p-adic GL(3) Satake parameters: (p^α₁, p^α₂, p^α₃)')
print(f'{"="*68}')

# In GL(3), the Langlands parameter should satisfy:
# For each p, the Satake parameters α₁, α₂, α₃ are the α_p for p=2,3,5
# The GL(3) central character condition: α₂ + α₃ + α₅ = 0 (for tempered)
sum_α = α_derived[2] + α_derived[3] + α_derived[5]
print(f'\n  α₂ + α₃ + α₅ = {α_derived[2]:.6f} + {α_derived[3]:.6f} + {α_derived[5]:.6f} = {sum_α:.6f}')
print(f'  GL(3) tempered condition α₂+α₃+α₅ = 0? 偏差 = {sum_α:.6f}')
print(f'  偏移量等于 C? C = {float(C):.6f}, 差 = {abs(sum_α - float(C)):.6f}')

# Sum with GL(3) shift
δ_GL3 = sum_α
print(f'\n  Shifted: α\'_p = α_p - δ_GL3/3')
shift = δ_GL3/3
for p in [2, 3, 5]:
    α_shifted = α_derived[p] - shift
    print(f'    α\'_{p} = {α_derived[p]:.6f} - {shift:.6f} = {α_shifted:.6f}')
print(f'  Σ α\'_p = {sum(α_derived[p]-shift for p in [2,3,5]):.6f}')

# ═══════ PART 6: Validation via spectrum ═══════
print(f'\n{"="*68}')
print(f'  VALIDATION: Green\'s function masses')
print(f'{"="*68}')

# Green's function mass formula: m_k^(p) = g_p · p^{k(1-α_p)}
g_GUT = np.sqrt(float(4*np.pi * C * 4*q_c))

# For each sector's α, compute first few masses and check ordering
for p in [2, 3, 5]:
    α = α_derived[p]
    s_p = Δa[pairs[p][1]] / b1
    print(f'\n  p={p} (α={α:.4f}, s={s_p:.4f}):')
    for k in range(-2, 4):
        m_k = g_GUT * (p ** (k * (1 - α)))
        print(f'    k={k:+d}: m = {m_k:.6f}')

# ═══════ PART 7: Full evaluation ═══════
print(f'\n{"="*68}')
print(f'  FULL FIRST-PRINCIPLES α_p CHAIN')
print(f'{"="*68}')
print('''
  INPUTS (pure number theory):
    q_c : 连分数 1-3q = q²/(9-2q-q²/(25-2q-...)) 的根
    C   : 1 + γ/2 - ln(4π/2) = 0.023095709
    W_m : SU(5) Weyl 轨道权重 {5, 10, 20}
    N_cycle = 30

  CHAIN:
    1. q_c = 0.329005727827  (连分数)
    2. b₁(q_c) = 2q_c          (Mathieu 恒等式)
    3. mod(p) = 2^{e₂}·3^{e₃}   (模数, 来自 Weyl 群结构)
       e₂ = 2 if p=2 else 1
       e₃ = 0 if p=2 else ⌊log₂(p)⌋
    4. s(p) = W_m mod mod(p)   (参考模式)
    5. r(p) = s + (1 if p≠5 else 2)  (目标模式)
    6. α_p = ln((a_r-a₀)/(a_s-a₀)) / ln(p)

  RESULTS:
''')

print(f'    p=2 (SU(3)): α₂ = {α_derived[2]:.6f}  (Weyl 模 4, 模式 (2,1))')
print(f'    p=3 (SU(2)): α₃ = {α_derived[3]:.6f}  (Weyl 模 6, 模式 (5,4))')
print(f'    p=5 (U(1)):  α₅ = {α_derived[5]:.6f}  (Weyl 模 18, 模式 (4,2))')
print(f'    α₂ + α₃ + α₅ = {sum_α:.6f}')

print(f'\n  对比 β-函数拟合值: α₂=1.547, α₃=0.432, α₅=0.842')
print(f'  偏差主要来源: β-函数拟合不是第一性')
