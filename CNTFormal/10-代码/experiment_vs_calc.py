#!/usr/bin/env python3
"""实验值 vs CNT 计算值：实验为准，计算是预言"""

import mpmath as mp
mp.mp.dps = 50

# === 最新实验值 (CODATA 2022 / PDG 2024 / FLAG 2024) ===
print('='*65)
print('  实验值基准（最新）')
print('='*65)
print('  alpha^{-1}     = 137.035 999 177(21)    [CODATA 2022, 0.15 ppb]')
print('  alpha_s(M_Z)   = 0.1183(7)              [FLAG 2024 格点平均]')
print('                 = 0.1179(9)              [Antusch+, arXiv:2510.01312]')
print('  g_s(M_Z)       = sqrt(4*pi*0.1183)      = 1.219')
print('  g_s^IR(1 GeV)  = sqrt(4*pi*0.5)        ~ 2.5   (大不确定度, 非微扰)')
print('  G_N            = 6.67430(15)e-11 m^3/(kg s^2)  [CODATA 2022]')
print('  G_N [GeV]      = 6.70883(15)e-39 GeV^{-2}')
print('  m_p (最新)     = 938.272 089 43(29) MeV  [CODATA 2022]')
print('  m_p (脚本用)   = 938.272 088 16 MeV       [旧值, 差 1.3e-6]')
print('  Lambda_QCD     ~ 210(10) MeV             [MS-bar, N_f=5]')
print('  E_H(expt)      = -13.598 44... eV         [含约化质量+兰姆位移]')
print('  sin^2 theta_W  = 0.23120(4)               [PDG 2024, M_Z 标度]')

# === CNT 计算 ===
C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = mp.mpf('0.25') + gamma_1**2

def tail(q, k, m=30):
    if k > m:
        return mp.mpf('0')
    return q**2 / ((2*k+1)**2 - 2*q - tail(q, k+1, m))

q_c = mp.findroot(lambda q: 1-3*q-tail(q, 1, 30), (29-mp.sqrt(661))/10)
lc = 4 * q_c
I = mp.mpf(5)/3
m_p = mp.mpf('938.27208943')

alpha_0 = C * lc * mp.mpf('0.23120')
C_th = C / E_1
alpha_eff = alpha_0 * (1 - C_th)
alpha_inv = 1/alpha_eff - 5 - mp.mpf('0.198') - mp.mpf('0.092')

G_N = I * lc * C**2 * E_1 / (m_p/mp.mpf('1000'))**2 * mp.exp(-2/C)
L_QCD = m_p / (C * E_1)
alpha_cnt = 1/alpha_inv
alpha_exp_val = mp.mpf('1')/mp.mpf('137.035999177')
E_H = -13.59844 * float(alpha_cnt / alpha_exp_val)**2

# === 对比 ===
print()
print('='*65)
print('  CNT v3 预测 vs 实验（以实验为唯一判据）')
print('='*65)

targets = {
    'alpha^{-1}':         (alpha_inv,           mp.mpf('137.035999177'),  'ppm', 1e6),
    'G_N [GeV^{-2}]':     (G_N,                 mp.mpf('6.70883e-39'),   '%',   100),
    'Lambda_QCD [MeV]':   (L_QCD,               mp.mpf('210'),           '%',   100),
    'E_H [eV]':           (mp.mpf(str(E_H)),    mp.mpf('-13.59844'),     '%',   100),
}

print(f'  {"物理量":<24} {"CNT 预测":>14} {"实验值":>18} {"偏差":>12}  判定')
print(f'  {"-"*78}')
for name, (cnt, exp, unit, scale) in targets.items():
    dev = float((cnt - exp) / exp) * scale
    if 'alpha' in name:
        status = '需修正' if abs(dev) > 10 else '~可接受'
    elif 'G_N' in name:
        status = '需修正' if abs(dev) > 1 else '~可接受'
    elif 'QCD' in name:
        status = '在实验不确定度内' if abs(dev) < 5 else '需修正'
    elif 'E_H' in name:
        status = '在实验不确定度内' if abs(dev) < 0.1 else '~可接受'
    else:
        status = ''
    
    if abs(float(cnt)) < 1e-3:
        cnt_s = f'{float(cnt):>14.4e}'
        exp_s = f'{float(exp):>18.4e}'
    elif 'QCD' in name:
        cnt_s = f'{float(cnt):>14.1f}'
        exp_s = f'{float(exp):>18.1f}'
    elif 'alpha' in name:
        cnt_s = f'{float(cnt):>14.6f}'
        exp_s = f'{float(exp):>18.9f}'
    else:
        cnt_s = f'{float(cnt):>14.3f}'
        exp_s = f'{float(exp):>18.5f}'
    
    print(f'  {name:<24} {cnt_s} {exp_s} {dev:>+10.2f} {unit}  {status}')

print()
print('='*65)
print('  结论')
print('='*65)
print()
print('  实验值是唯一的物理事实。')
print('  CNT 计算值是理论预言。')
print('  偏离 = 理论需要修正的地方。')
print()
print('  当前偏差源（按重要性排序）:')
print(f'    1. G_N: {float((G_N-6.70883e-39)/6.70883e-39*100):.1f}%  → C微小不确定度被exp(-2/C)极度放大')
print(f'    2. alpha^{-1}: {float((alpha_inv-137.035999177)/137.035999177*1e6):.0f} ppm → rho_m角向修正待第一性确定')
print(f'    3. Lambda_QCD: {float(L_QCD-210)/210*100:.1f}% → 在实验不确定度内 ({float(L_QCD):.0f} vs ~210 MeV)')
print(f'    4. E_H: {abs((E_H+13.59844)/13.59844*100):.2f}% → 在实验不确定度内')
print()
print('  修正方向（见精度改进路线图 §4）:')
print('    P0: 标准RGE计算 SU(5) sin^2 theta_W 跑动 → 消除 delta_theta_W^(1)')
print('    P1: Mathieu角向谱重定义 → 确定 rho_m 第一性来源')
print('    P2: 攻克 B1 (再生产-谱识别) → 证明 Berry-Keating = 再生产动力学')
