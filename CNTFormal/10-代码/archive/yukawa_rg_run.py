#!/usr/bin/env python3
"""
CNT Yukawa RG 运行验证
======================
从 CNT 值 Y_f(m_f) 用 1-圈 SM RGE 运行到 M_Z，
与 SM 预期值比较。

SM 参考值 (M_Z, MSbar):
  m_t(M_Z) ≈ 172.5 GeV (pole), Y_t(M_Z) ≈ 0.995
  m_b(M_Z) ≈ 2.82 GeV,       Y_b(M_Z) ≈ √2·2.82/246.22 ≈ 0.0162
  m_τ(M_Z) ≈ 1.746 GeV,      Y_τ(M_Z) ≈ √2·1.746/246.22 ≈ 0.01003
"""
import numpy as np
from scipy.integrate import solve_ivp
import mpmath as mp

mp.mp.dps = 30

print("="*65)
print("CNT Yukawa RG 运行: 从 m_f → M_Z")
print("1-圈 SM RGE")
print("="*65)

# 常数
M_Z = 91.1876  # GeV
v_SM = 246.22  # GeV

# CNT Yukawa 在粒子质量标度
CNT = {
    't': {'Y': 1.004073, 'm': 172.5},
    'b': {'Y': 0.0235148, 'm': 4.18},
    'τ': {'Y': 0.0102217, 'm': 1.777},
}

# SM 参考值 (在 M_Z, MSbar)
SM = {
    't': {'Y': 0.995,   'm': 172.5},
    'b': {'Y': 0.0162,  'm': 2.82},
    'τ': {'Y': 0.01003, 'm': 1.746},
}

# 规范耦合在 M_Z (MSbar)
# g₁ = sqrt(4π·α₁), α₁ = 5α_EM/(3cos²θ_W)
# g₂ = sqrt(4π·α₂), α₂ = α_EM/sin²θ_W
# g₃ = sqrt(4π·α₃), α₃ = 0.118
α_EM = 1/127.955
sin2θ = 0.23122
α1 = 5*α_EM/(3*(1-sin2θ))
α2 = α_EM/sin2θ
α3 = 0.1180

g1_MZ = np.sqrt(4*np.pi*α1)
g2_MZ = np.sqrt(4*np.pi*α2)
g3_MZ = np.sqrt(4*np.pi*α3)

print(f"\n  规范耦合 (M_Z):")
print(f"    g₁²/(4π) = α₁ = {α1:.6f}")
print(f"    g₂²/(4π) = α₂ = {α2:.6f}")
print(f"    g₃²/(4π) = α₃ = {α3:.4f}")

def rge_system_sm(t, y):
    """SM 1-圈 RGE, t = ln(μ/M_Z)"""
    Yt, Yb, Yτ, g1, g2, g3 = y
    C = 1 / (16*np.pi**2)
    # Traces: T = Tr(3Y_u†Y_u + 3Y_d†Y_d + Y_e†Y_e)
    T = 3*Yt**2 + 3*Yb**2 + Yτ**2
    
    # 标准 SM 1-圈 RGE (Machacek-Vaughn '83, Arason '93)
    dYt = Yt * (9/2*Yt**2 + 3/2*Yb**2 + T - 8*g3**2 - 9/4*g2**2 - 17/20*g1**2) * C
    dYb = Yb * (9/2*Yb**2 + 3/2*Yt**2 + T - 8*g3**2 - 9/4*g2**2 - 1/4*g1**2) * C
    dYτ = Yτ * (5/2*Yτ**2 + T - 9/4*g2**2 - 9/4*g1**2) * C
    
    dg1 = 41/6 * g1**3 * C
    dg2 = -19/6 * g2**3 * C
    dg3 = -7 * g3**3 * C
    
    return [dYt, dYb, dYτ, dg1, dg2, dg3]

def run_CNT_to_MZ(particle):
    """从 m_f 运行到 M_Z"""
    m_f = CNT[particle]['m']
    t_start = np.log(m_f / M_Z)
    t_stop = 0.0
    
    y0 = [CNT['t']['Y'], CNT['b']['Y'], CNT['τ']['Y'], g1_MZ, g2_MZ, g3_MZ]
    idx = {'t': 0, 'b': 1, 'τ': 2}[particle]
    
    sol = solve_ivp(rge_system_sm, [t_start, t_stop], y0, 
                    method='RK45', max_step=0.005, rtol=1e-10, atol=1e-12)
    
    return sol.y[idx, -1], sol

for p in ['t', 'b', 'τ']:
    Y_CNT_mf = CNT[p]['Y']
    m_f = CNT[p]['m']
    Y_RG_MZ, sol = run_CNT_to_MZ(p)
    Y_SM_MZ = SM[p]['Y']
    
    # 也给出 SM 预期的 m_f 值
    Y_SM_mf = SM[p]['Y']  # 近似
    
    print(f"\n  {p}:")
    print(f"    m_f = {m_f:.1f} GeV")
    print(f"    Y_CNT(m_f)     = {Y_CNT_mf:.6f}")
    print(f"    Y_RG(M_Z)      = {Y_RG_MZ:.6f}  (从 CNT 运行)")
    print(f"    Y_SM(M_Z)      = {Y_SM_MZ:.6f}")
    print(f"    偏差(在 M_Z)  = {(Y_RG_MZ/Y_SM_MZ - 1)*100:+.2f}%")

# 完整 Y_t 轨迹
print(f"\n{'='*65}")
print("Y_t 运行轨迹: m_t → M_Z")
print('='*65)

t_vals = np.linspace(np.log(172.5/M_Z), 0, 30)
sol = solve_ivp(rge_system_sm, [t_vals[0], t_vals[-1]],
                [CNT['t']['Y'], CNT['b']['Y'], CNT['τ']['Y'], g1_MZ, g2_MZ, g3_MZ],
                method='RK45', t_eval=t_vals, max_step=0.005, rtol=1e-10, atol=1e-12)

mu_vals = M_Z * np.exp(sol.t)
print(f"  {'μ (GeV)':<12} {'Y_t':<12} {'Y_b':<12} {'Y_τ':<12}")
print(f"  {'-'*48}")
for i in range(0, len(mu_vals), 3):
    print(f"  {mu_vals[i]:<12.1f} {sol.y[0,i]:<12.6f} {sol.y[1,i]:<12.6f} {sol.y[2,i]:<12.6f}")

# 反向运行验证: 从 Y_SM(M_Z) → m_f
print(f"\n{'='*65}")
print("反向验证: 从 Y_SM(M_Z) 运行到 m_f")
print('='*65)

for p in ['t', 'b', 'τ']:
    m_f = CNT[p]['m']
    Y_SM_MZ = SM[p]['Y']
    t_start = 0.0
    t_stop = np.log(m_f / M_Z)
    
    y0 = [SM['t']['Y'], SM['b']['Y'], SM['τ']['Y'], g1_MZ, g2_MZ, g3_MZ]
    idx = {'t': 0, 'b': 1, 'τ': 2}[p]
    
    sol = solve_ivp(rge_system_sm, [t_start, t_stop], y0,
                    method='RK45', max_step=0.005, rtol=1e-10, atol=1e-12)
    
    Y_SM_at_mf = sol.y[idx, -1]
    Y_CNT_mf = CNT[p]['Y']
    
    print(f"\n  {p}: m_f = {m_f:.1f} GeV")
    print(f"    Y_SM(M_Z)      = {Y_SM_MZ:.6f}")
    print(f"    Y_SM→m_f       = {Y_SM_at_mf:.6f}")
    print(f"    Y_CNT(m_f)     = {Y_CNT_mf:.6f}")
    print(f"    偏差(在 m_f)  = {(Y_CNT_mf/Y_SM_at_mf - 1)*100:+.2f}%")
