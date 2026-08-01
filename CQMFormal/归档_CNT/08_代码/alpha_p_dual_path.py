#!/usr/bin/env python3
"""
CNT 完整粒子谱 v3 — 第一性原理 α_p + 整数壳层约束
=====================================================
2026-07-23:

α_p 的第一性来源 → 两条约束路径 (数学等价条件):

路径 A [Mathieu 谱比率] —— UV 值 (不动点):
  α_p = ln(Δa_{r(p)}/Δa_{s(p)}) / ln(p)
  来自: RG 变换下 Mathieu 谱闭包条件

路径 B [整数壳层约束] —— IR 值 (观测):
  k ∈ ℤ  ⇒  α_p = 1 - ln(m_j/m_i)/[(k_j-k_i)·ln(p)]
  来自: Vladimirov 本征值 k ∈ ℤ (p进赋值整数性)

两路径的差 = α_p 自身的 RG 运行
"""

import mpmath as mp
from scipy.special import mathieu_a
mp.mp.dps = 60

# ═══════════════════════════════════════════════════════════════
#  基础常数
# ═══════════════════════════════════════════════════════════════
m_p_MeV = mp.mpf('938.27208816')
C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = mp.mpf('0.25') + gamma_1**2

def compute_q_c(depth=50):
    def tail(q, k):
        if k > depth: return mp.mpf('0')
        n = 2*k + 1
        return q**2 / (n**2 - 2*q - tail(q, k+1))
    return mp.findroot(lambda q: 1 - 3*q - tail(q, 1), (29 - mp.sqrt(661))/10)

q_c = compute_q_c(50)
λ_c = 4*q_c
r_GUT_sq = 4*mp.pi * C * λ_c

# ═══════════════════════════════════════════════════════════════
#  Mathieu 谱 → 路径 A: UV α_p
# ═══════════════════════════════════════════════════════════════
a_vals = [mathieu_a(r, float(q_c)) for r in range(20)]
a0 = a_vals[0]
Δa = [a - a0 for a in a_vals]

W_map = {2: 5, 3: 10, 5: 20}
mod_map = {2: 4, 3: 6, 5: 18}
skip_map = {2: 1, 3: 1, 5: 2}

α_UV = {}
for p in [2, 3, 5]:
    mod_p = mod_map[p]
    s = W_map[p] % mod_p
    r = s + skip_map[p]
    α_UV[p] = mp.log(mp.mpf(str(Δa[r])) / mp.mpf(str(Δa[s]))) / mp.log(p)

# ═══════════════════════════════════════════════════════════════
#  整数壳层 → 路径 B: IR α_p
# ═══════════════════════════════════════════════════════════════
#  k ∈ ℤ 固定, 从实验质量反解 α_p
particle_data = {
    5: {'pairs': [('e','μ', -21, 0), ('τ','μ', 11, 0)], 
        'masses': {'e': 0.510998950, 'μ': 105.658375, 'τ': 1776.93}},
    3: {'pairs': [('u','c', -10, 0), ('t','c', 8, 0)],
        'masses': {'u': 2.16, 'c': 1270, 't': 172500}},
    2: {'pairs': [('d','s', 8, 0), ('b','s', -10, 0)],
        'masses': {'d': 4.67, 's': 93.4, 'b': 4180}}
}

α_IR = {}
for p in [2, 3, 5]:
    pd = particle_data[p]
    α_vals = []
    for name1, name2, k1, k2 in pd['pairs']:
        m1 = mp.mpf(str(pd['masses'][name1]))
        m2 = mp.mpf(str(pd['masses'][name2]))
        dk = k1 - k2
        α = 1 - mp.log(m1/m2) / (dk * mp.log(p))
        α_vals.append(α)
    α_IR[p] = sum(α_vals) / len(α_vals)  # average

# ═══════════════════════════════════════════════════════════════
#  粒子谱计算 (用 UV α_p, 但 k 从整数性固定)
# ═══════════════════════════════════════════════════════════════
sectors = {
    5: {'name': 'p=5 轻子', 'g_p': mp.mpf('207.6'),
        'particles': [('e', -21, 0.510998950), ('μ', 0, 105.658375), ('τ', 11, 1776.93)]},
    3: {'name': 'p=3 up型夸克', 'g_p': mp.mpf('469.1'),
        'particles': [('u', -10, 2.16), ('c', 0, 1270), ('t', 8, 172500)]},
    2: {'name': 'p=2 down型夸克', 'g_p': mp.mpf('261.5'),
        'particles': [('d', 8, 4.67), ('s', 0, 93.4), ('b', -10, 4180)]}
}

print('='*72)
print('  CNT 粒子谱 — 双路径 α_p 比较')
print('='*72)
print(f'\n  基础常数: C={float(C):.6f}, q_c={float(q_c):.12f}, λ_c={float(λ_c):.12f}')

print(f'\n{"="*72}')
print(f'  α_p: UV (Mathieu 谱) vs IR (整数壳层)')
print(f'{"="*72}')
print(f'\n  {"p":>3}  {"UV α":>10}  {"IR α":>10}  {"Δα":>10}  {"模式":>12}  {"说明":>25}')
print(f'  {"---":>3}  {"-----":>10}  {"-----":>10}  {"---":>10}  {"----":>12}  {"----":>25}')

for p in [2, 3, 5]:
    r, s = W_map[p] % mod_map[p], (W_map[p] % mod_map[p]) + skip_map[p]
    s_idx = W_map[p] % mod_map[p]
    r_idx = s_idx + skip_map[p]
    diff = (α_UV[p] / α_IR[p] - 1) * 100
    desc = {2: 'UV>IR (超扩散减弱)', 3: 'UV<IR (次扩散增强)', 
            5: 'UV>IR (近乎一致)'}[p]
    print(f'  {p:>3}  {float(α_UV[p]):>10.6f}  {float(α_IR[p]):>10.6f}  {float(diff):>+9.4f}%  Δa_{{{r_idx}}}/Δa_{{{s_idx}}}  {desc}')

print(f'\n  差 = α_p 自身的 RG 运行 (从 GUT 标度到粒子质量标度)')

# ═══════════════════════════════════════════════════════════════
#  Green 函数质量公式 (用 UV α_p)
# ═══════════════════════════════════════════════════════════════
print(f'\n{"="*72}')
print(f'  [路径 A: UV α_p] 全粒子谱')
print(f'  m_k^(p) = g_p · s_p · p^(k(1-α_UV_p)),  s_p = m_0/g_p')
print(f'{"="*72}')

print(f'\n  {"扇区":<16} {"粒子":<6} {"k":<4} {"m_UV (MeV)":<14} {"m_exp (MeV)":<14} {"偏差%":<8}')
print(f'  {"-"*66}')

total_rms_UV = mp.mpf('0')
n_UV = 0

for p in sorted(sectors.keys(), reverse=True):
    sec = sectors[p]
    g_p = sec['g_p']
    m0 = mp.mpf(str(sec['particles'][1][2]))  # k=0 mass
    s_p = m0 / g_p

    for name, k, m_exp_val in sec['particles']:
        m_exp = mp.mpf(str(m_exp_val))
        factor = p ** (k * (1 - α_UV[p]))
        m_cnt = g_p * s_p * factor

        if m_exp > 0 and m_cnt > 0:
            dev = (m_cnt - m_exp) / m_exp * 100
            total_rms_UV += dev**2
            n_UV += 1
        else:
            dev = mp.mpf('0')

        print(f'  {sec["name"]:<16} {name:<6} {k:<4} {float(m_cnt):<14.6f} {float(m_exp):<14.6f} {float(dev):+.2f}%')

rms_UV = mp.sqrt(total_rms_UV / n_UV) if n_UV > 0 else mp.mpf('0')
print(f'\n  RMS = {float(rms_UV):.2f}%')

# ═══════════════════════════════════════════════════════════════
#  k 的整数性检验
# ═══════════════════════════════════════════════════════════════
print(f'\n{"="*72}')
print(f'  整数壳层检验: k 必须为整数 → α_UV 要求非整数 k 的程度')
print(f'{"="*72}')

print(f'\n  {"扇区":<16} {"粒子对":<10} {"m_ratio(exp)":<14} {"k_needed":<10} {"整数?":<8}')
print(f'  {"-"*62}')

for p in sorted(sectors.keys(), reverse=True):
    sec = sectors[p]
    parts = sec['particles']
    g_p = sec['g_p']
    m0 = mp.mpf(str(parts[1][2]))
    s_p = m0 / g_p

    for name, k_assumed, m_exp_val in parts:
        if k_assumed == 0:
            continue
        m_exp = mp.mpf(str(m_exp_val))
        # What k would give exact mass with UV α?
        # m = g_p · s_p · p^(k(1-α))
        # k = ln(m/(g_p·s_p)) / ((1-α)·ln(p))
        k_from_UV = mp.log(m_exp / (g_p * s_p)) / ((1 - α_UV[p]) * mp.log(p))
        is_int = abs(k_from_UV - round(float(k_from_UV))) < 0.05
        marker = '✓' if is_int else '✗'
        print(f'  {sec["name"]:<16} {name:<10} {float(m_exp/m0):<14.6f} {float(k_from_UV):<10.4f} {marker}')

# ═══════════════════════════════════════════════════════════════
#  α_p 运行: UV → IR
# ═══════════════════════════════════════════════════════════════
print(f'\n{"="*72}')
print(f'  α_p 的 RG 运行: Δα_p = α_IR_p - α_UV_p')
print(f'{"="*72}')

print(f'\n  {"p":>3}  {"α_UV":>10}  {"α_IR":>10}  {"Δα":>10}  {"β(α_p)":>10}  {"物理解释":>30}')
print(f'  {"---":>3}  {"----":>10}  {"----":>10}  {"---":>10}  {"------":>10}  {"----":>30}')

for p in [2, 3, 5]:
    Δα = α_IR[p] - α_UV[p]
    sec_name = {2: 'SU(3) 超扩散', 3: 'SU(2) 次扩散', 5: 'U(1) 近临界'}[p]
    direction = {2: 'IR 降低 (禁闭驱动)', 3: 'IR 升高 (弱作用减弱)', 
                 5: 'IR 降低 (电磁精细化)'}[p]
    print(f'  {p:>3}  {float(α_UV[p]):>10.6f}  {float(α_IR[p]):>10.6f}  {float(Δα):>+10.6f}  {"":>10}  {direction}')

# ═══════════════════════════════════════════════════════════════
#  最终决策: 推荐 α_p
# ═══════════════════════════════════════════════════════════════
print(f'\n{"="*72}')
print(f'  推荐: 数学谱 = α_UV, 观测谱校正 = α_IR 时的质量')
print(f'{"="*72}')

print(f'''
  α_p 的双重角色:
    UV (Mathieu 谱固定点):  α_UV_p = α_p 的裸值
    IR (整数壳层约束):     α_IR_p = α_p 的红外值
    RG 运行:               Δα_p = α_IR_p - α_UV_p

  推荐: 在数学推导中用 α_UV, 在粒子谱计算中用 α_IR。
  两者之差 = α_p 跑动效应, 是未来的严格推导方向。
''')

# 用 IR α_p 再算一遍 RMS
total_rms_IR = mp.mpf('0')
n_IR = 0
print(f'\n  [路径 B: IR α_p] 全粒子谱')

for p in sorted(sectors.keys(), reverse=True):
    sec = sectors[p]
    g_p = sec['g_p']
    m0 = mp.mpf(str(sec['particles'][1][2]))
    s_p = m0 / g_p

    for name, k, m_exp_val in sec['particles']:
        m_exp = mp.mpf(str(m_exp_val))
        factor = p ** (k * (1 - α_IR[p]))
        m_cnt = g_p * s_p * factor

        dev = (m_cnt - m_exp) / m_exp * 100 if m_exp > 0 else mp.mpf('0')
        total_rms_IR += dev**2
        n_IR += 1

rms_IR = mp.sqrt(total_rms_IR / n_IR) if n_IR > 0 else mp.mpf('0')
print(f'  RMS = {float(rms_IR):.2f}%  (α_IR, 整数壳层)')
print(f'  RMS = {float(rms_UV):.2f}%  (α_UV, Mathieu 谱)')
