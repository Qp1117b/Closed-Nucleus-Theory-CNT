#!/usr/bin/env python3
"""
⚠️ 已过时 (2026-07-23 标记): β-函数不动点路径
=============================================
已被 alpha_p_dual_path.py 替代 (UV: Mathieu 谱比 + IR: 整数壳层双路径)。
保留为推导历史参考。
"""
"""
α_p 第一性推导：RG 不动点自洽方程
=================================
核心方程:
  α_p - 1 = g_GUT² · C₂(p) · Σ_r Σ_{k≥0} 1/(a_r(q_c) + p^{-kα})²

  左边: tree-level 标度维
  右边: Mathieu 谱的一圈量子修正
  不动点: 左右相等时 β(α_p) = 0

  g_GUT² = 4π·C·λ_c (第一性)
  C₂(p) = SU(5) Casimir (群论)
  a_r(q_c) = Mathieu 特征值 (谱)
"""
import numpy as np
from scipy.special import mathieu_a, mathieu_b
import mpmath as mp
mp.mp.dps = 50

# ═══════════════════════════════════════════════════════════════
# PART 1: CNT core constants
# ═══════════════════════════════════════════════════════════════
C = float(1 + mp.euler/2 - mp.log(4*mp.pi)/2)

def tail(q, k, md=50):
    if k > md: return 0.0
    n = 2*k + 1
    return q**2 / (n**2 - 2*q - tail(q, k+1, md))

def q_eq(q): return 1 - 3*q - tail(q, 1, 50)

# Use mpmath for high precision root finding
q_c_mp = mp.findroot(lambda q: float(1 - 3*q - tail(float(q), 1, 50)), (29 - mp.sqrt(661))/10)
q_c = float(q_c_mp)
λ_c = 4*q_c

I = 5/3
I_SU2 = 5/2
N_X = 12
W1, W2, W3 = 5, 10, 20

# GUT coupling (first-principles)
g_GUT2 = 4*np.pi * C * λ_c
g_GUT = np.sqrt(g_GUT2)
print(f'g_GUT² = 4π·C·λ_c = {g_GUT2:.8f}')
print(f'g_GUT = {g_GUT:.6f}')

# β-functions
β3 = λ_c / (N_X * I)
β2 = C / I_SU2
β1 = -C / q_c
print(f'β₁ = {β1:.10f}  β₂ = {β2:.10f}  β₃ = {β3:.10f}')

# SU(5) Casimirs (for RG running)
# For the adjoint representation:
# SU(N): C₂(adj) = N
# For SU(5) broken to SU(3)×SU(2)×U(1):
C2_adj = {3: 3, 2: 2, 1: 0}  # C₂(adj) for SU(3), SU(2), U(1)
# Actually for U(1): C₂ = Y², but we use the combination that matches RG running
# In the spectral framework, the relevant factor is determined by the Dynkin index

# ═══════════════════════════════════════════════════════════════
# PART 2: Mathieu eigenvalues at q_c
# ═══════════════════════════════════════════════════════════════
print(f'\nMathieu eigenvalues at q_c = {q_c:.12f}:')
r_max = 30
a_vals = np.array([mathieu_a(r, q_c) for r in range(r_max)])
b_vals = np.array([mathieu_b(r, q_c) for r in range(1, r_max)])

for r in range(8):
    b_str = f'{b_vals[r]:.10f}' if r < len(b_vals) else ''
    print(f'  a_{r} = {a_vals[r]:.10f}  b_{r+1} = {b_str}')

print(f'\n  b₁(q_c) = {b_vals[0]:.12f}')
print(f'  2q_c    = {2*q_c:.12f}')
print(f'  b₁ == 2q_c? {abs(b_vals[0] - 2*q_c) < 1e-12}')

# ═══════════════════════════════════════════════════════════════
# PART 3: Spectral sum S_p(α) for the RG equation
# ═══════════════════════════════════════════════════════════════
def spectral_sum(p, α, a_vals, k_max=30, r_max=30):
    """
    Σ_r Σ_{k=0}^{k_max} 1/(a_r + p^{-k·α})²
    """
    total = 0.0
    for r in range(r_max):
        a_r = a_vals[r]
        # Shift a_r by min to make positive (for convergence)
        # Use raw eigenvalues
        for k in range(k_max + 1):
            denom = a_r + p**(-k * α)
            if abs(denom) > 1e-15:
                total += 1.0 / denom**2
    return total

def rg_eq(α, p, a_vals, g2, C2, k_max=30, r_max=30):
    """
    RG fixed point equation:
    α - 1 = g² · C₂ · Σ_r Σ_k 1/(a_r + p^{-kα})²
    Returns LHS - RHS (zero = fixed point)
    """
    S = spectral_sum(p, α, a_vals, k_max, r_max)
    lhs = α - 1
    rhs = g2 * C2 * S
    return lhs - rhs, lhs, rhs, S

# ═══════════════════════════════════════════════════════════════
# PART 4: Solve RG equation for each sector
# ═══════════════════════════════════════════════════════════════
print('\n' + '='*65)
print('  RG 不动点方程求解')
print('='*65)

# For each sector, we need to determine the effective C₂
# In the spectral framework, C₂ is determined by the SU(5) group structure:
# The Weyl orbit weights W_m define the effective Casimir
# For sector p, the effective C₂ = W_{f(p)} * something

# Let's first scan α for each p and see where the equation is satisfied
empirical = {2: 1.547, 3: 0.432, 5: 0.842}

for p, label in [(2, 'Strong (SU(3))'), (3, 'Weak (SU(2))'), (5, 'EM (U(1))')]:
    print(f'\n--- p={p} [{label}] ---')
    
    # Scan α
    α_scan = np.arange(0.2, 2.1, 0.02)
    results = []
    for α in α_scan:
        diff, lhs, rhs, S = rg_eq(α, p, a_vals, g_GUT2, 1.0, k_max=20, r_max=20)
        results.append((α, float(diff), float(lhs), float(rhs)))
    
    # Find where diff changes sign (RG fixed point candidate)
    results_arr = np.array(results)
    sign_changes = []
    for i in range(len(results_arr)-1):
        if results_arr[i,1] * results_arr[i+1,1] <= 0:
            sign_changes.append((results_arr[i,0], results_arr[i+1,0]))
    
    print(f'  C₂=1 (bare) scan:')
    emp_a = empirical[p]
    print(f'    At α=empirical={emp_a}: diff={float(rg_eq(emp_a, p, a_vals, g_GUT2, 1.0, 20, 20)[0]):.4f}')
    if sign_changes:
        for sc in sign_changes:
            print(f'    Sign change between α={sc[0]:.2f} and α={sc[1]:.2f}')
    else:
        print(f'    No sign change found (equation never crosses zero)')
    
    # Try to find optimal C₂ for each sector
    # The condition is: at α = α_empirical, we need LHS = RHS
    # So C₂ = (α-1) / (g² · S)
    α_test = emp_a
    diff, lhs, rhs, S = rg_eq(α_test, p, a_vals, g_GUT2, 1.0, 20, 20)
    if abs(S) > 1e-15:
        C2_needed = (α_test - 1) / (g_GUT2 * S)
        print(f'  At α_emp={α_test}: S={S:.4f}, needed C₂={C2_needed:.6f}')
    else:
        print(f'  S ≈ 0, no solution')

# ═══════════════════════════════════════════════════════════════
# PART 5: Self-consistent solution
# ═══════════════════════════════════════════════════════════════
print('\n' + '='*65)
print('  自洽解：α_p 同时满足 RG 方程')
print('='*65)

# The RG equation is:
# α - 1 = g_GUT² · C₂_eff(p) · S_p(α)
# where C₂_eff(p) = group theory factor
# 
# The group theory factor should be universal (same structure for all p)
# For SU(3) sector (p=2): C₂ = ?
# For SU(2) sector (p=3): C₂ = ?
# For U(1) sector (p=5): C₂ = ?
#
# In SU(5) GUT: the gauge bosons transform in the adjoint 24
# 24 = (8,1,0) ⊕ (1,3,0) ⊕ (1,1,0) ⊕ (3,2,-5/6) ⊕ (3̅,2,5/6)
# The Casimir for each sector is proportional to the Dynkin index

# Dynkin indices (normalized to SU(5) fundamental = 1):
# SU(3) adjoint: I₂(8) = 2N = 6 (in SU(N) normalization)
# SU(2) adjoint: I₂(3) = 2N = 4
# U(1) charge: I₂(1) = Y² summed over states

# In the SU(5) normalization, the embedding indices are:
I_SU3_in_SU5 = 5/3  # for SU(3) ⊂ SU(5)
I_SU2_in_SU5 = 5/2  # for SU(2) ⊂ SU(5)
# For U(1): need to determine from the 24 representation

# The effective C₂ in the RG equation should be proportional to these:
C2_eff = {2: I_SU3_in_SU5, 3: I_SU2_in_SU5, 5: (3/5) * I_SU3_in_SU5}

for p in [2, 3, 5]:
    print(f'\n  p={p}: searching self-consistent α_p...')
    
    # Iterative solution
    α_guess = 1.0
    for iteration in range(50):
        diff, lhs, rhs, S = rg_eq(α_guess, p, a_vals, g_GUT2, C2_eff[p], 20, 20)
        if abs(diff) < 1e-8:
            break
        # Newton step: d(diff)/dα = 1 - g²·C₂·dS/dα
        # Approximate: dS/dα ≈ S/α
        dS_dα = S / max(α_guess, 0.1)
        ddiff_dα = 1 - g_GUT2 * C2_eff[p] * dS_dα
        if abs(ddiff_dα) > 1e-10:
            α_guess -= diff / ddiff_dα
        else:
            α_guess += 0.01
        α_guess = max(0.1, min(3.0, α_guess))
    
    emp = empirical[p]
    print(f'    解: α = {α_guess:.6f}  (经验 {emp}, 偏差 {(α_guess-emp)/emp*100:.3f}%)')

# ═══════════════════════════════════════════════════════════════
# PART 6: Alternative - solve directly from RG flow rate
# ═══════════════════════════════════════════════════════════════
print('\n' + '='*65)
print('  Alternative: α_p from β-function matching')
print('='*65)
print('''
  In CNT, the β-functions are known first-principles numbers.
  For the RG flow to be consistent:
    β_p = (α_{f(p)} - 1) × (group theory factor)
  
  where f(p) maps force sector → α sector.
  
  For SU(3)β → α₂: β₃ = (α₂ - 1) × G₃
  For SU(2)β → α₃: β₂ = (α₃ - 1) × G₂
  For U(1)β  → α₅: β₁ = (α₅ - 1) × G₁
  
  G_p are group theory factors from SU(5) to be determined.
''')

# Try: G_p = C₂(p) * spectral_ratio
# where spectral_ratio = Σ_r 1/(a_r + something)

for p, β_val, label in [(2, β3, 'β₃→α₂'), (3, β2, 'β₂→α₃'), (5, abs(β1), '|β₁|→α₅')]:
    print(f'\n  {label}:')
    # β = (α-1) × G → G = β/(α-1)
    emp_a = empirical[p]
    if p == 2:
        G_needed = β_val / (emp_a - 1)
    else:
        G_needed = β_val / (1 - emp_a)
    
    # Spectral sum as G_p
    S_base = spectral_sum(p, emp_a, a_vals, 20, 20)
    print(f'    Needed G = {G_needed:.6f}')
    print(f'    Spectral sum S = {S_base:.6f}')
    print(f'    G/S = {G_needed/S_base:.6f}')
    
    # What combination of group theory gives G?
    # G ∝ W_m · I · (spectral factor)
    for name, val in [('W₁·I', W1*I), ('W₂·I', W2*I), ('W₃·I', W3*I),
                       ('W₁·I·(1-C)', W1*I*(1-C)), ('W₂·I/2', W2*I/2)]:
        ratio = val / G_needed
        if abs(ratio - 1) < 0.5:
            print(f'    {name} = {val:.4f} ≈ G (ratio {ratio:.4f})')
