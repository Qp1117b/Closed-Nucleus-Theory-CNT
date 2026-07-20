#!/usr/bin/env python3
"""g_s 完整对照：CNT 预言 vs 实验"""
import mpmath as mp; mp.mp.dps = 30
import math

C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = 0.25 + gamma_1**2

def tail(q, k, m=30):
    if k > m: return 0
    return q**2/((2*k+1)**2 - 2*q - tail(q, k+1, m))

q_c = mp.findroot(lambda q: 1-3*q-tail(q, 1, 30), (29-mp.sqrt(661))/10)
lc = 4*q_c; I = mp.mpf(5)/3
m_p = 938.27208943; hbar_c = 197.3269804

g_s_theorem = float(mp.sqrt(I*lc))
g_s_k_formula = float(hbar_c * C * E_1 / (m_p * 0.6805))

g_s_MZ_FLAG = math.sqrt(4*math.pi*0.1183)
g_s_MZ_PDG  = math.sqrt(4*math.pi*0.1179)
g_s_IR_approx = math.sqrt(4*math.pi*0.5)

print('='*60)
print('  g_s 完整对照')
print('='*60)
print()
print('  CNT 内部值:')
print(f'    定理 10.4: sqrt(I*lambda_c)         = {g_s_theorem:.4f}')
print(f'    k 公式反推: hbar*C*E1/(m_p*k)       = {g_s_k_formula:.4f} (k=0.6805 fm)')
print(f'    读者入门:   (伪造值)                = 1.2140')
print()
print('  实验值:')
print(f'    g_s(M_Z) [FLAG 2024]:  alpha_s=0.1183(7) -> g_s = {g_s_MZ_FLAG:.4f}')
print(f'    g_s(M_Z) [PDG 2024]:   alpha_s=0.1179(9) -> g_s = {g_s_MZ_PDG:.4f}')
print(f'    g_s(1 GeV) [非微扰估计]: alpha_s~0.5      -> g_s ~ {g_s_IR_approx:.1f}')
print()
print('='*60)
print('  g_s 能和实验比吗?')
print('='*60)
print()
print(f'  场景 A: CNT g_s=1.481 是红外(hadronic scale)值')
print(f'    实验: g_s(1 GeV) ~ 2.5 (大不确定, 非微扰)')
print(f'    偏差: ~ {(1.481-2.5)/2.5*100:+.0f}%')
print(f'    判定: 比较无意义 -- 实验红外 g_s 定义依赖强')
print()
print(f'  场景 B: CNT g_s=1.481 是 M_Z 标度值')
print(f'    实验: g_s(M_Z) = {g_s_MZ_PDG:.4f}')
print(f'    偏差: {(1.481-g_s_MZ_PDG)/g_s_MZ_PDG*100:+.1f}%')
print(f'    判定: CNT g_s^IR 不是 M_Z 标度值, 不能直接比')
print()
print(f'  场景 C: CNT g_s=1.428 (从 k 公式反推)')
print(f'    这是内部自洽需要的值, 不是对实验的独立预言')
print()
print('='*60)
print('  结论')
print('='*60)
print()
print('  g_s 不能和实验做有意义的直接对比:')
print('    1. CNT 的 g_s^IR 标度不明确')
print('    2. 实验红外 g_s 非微扰, 定义依赖')
print('    3. M_Z 标度值不能和 IR 值直接比较')
print()
print('  诚实处理:')
print('    - 对比表中移除 g_s (无意义比较)')
print('    - 保留 g_s^IR = 1.481 作为 CNT 内部量')
print('    - 将来若 CNT 能跑动 g_s(scale), 再和实验对比')
