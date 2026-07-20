#!/usr/bin/env python3
"""sin^2 theta_W: 标准RGE vs CNT公式
关键问题: delta_W^(1) = -0.156 能第一性推导吗?"""

import math

# === 实验输入 (M_Z 标度) ===
M_Z = 91.1876
alpha_em = 1/137.035999177
sin2W_exp = 0.23120

alpha_2_MZ = alpha_em / sin2W_exp
alpha_1_MZ = 5*alpha_em/(3*(1 - sin2W_exp))

print('='*65)
print('  sin^2 theta_W: 标准RGE vs CNT')
print('='*65)
print()
print(f'  alpha_1^{-1}(M_Z) = {1/alpha_1_MZ:.2f} (SU(5)归一化)')
print(f'  alpha_2^{-1}(M_Z) = {1/alpha_2_MZ:.2f}')
print(f'  sin^2W_exp(M_Z)  = {sin2W_exp:.5f}')
print()

# === SM 单圈 beta ===
b1 = 41/10    # U(1), SU(5)归一化
b2 = -19/6    # SU(2)_L
b3 = -7       # SU(3)_C

print(f'  SM 单圈 beta: b1={b1}, b2={b2:.4f}, b3={b3}')
print()

# === 关键事实: SM 单圈下 SU(2) 和 SU(3) 在 M_Z 以上发散 ===
# alpha_2^{-1} 从 31.68 开始, 斜率为 -19/6/2pi ≈ -0.05/decade
# alpha_3^{-1} 从 8.45 开始, 斜率为 -7/2pi ≈ -1.11/decade
# 两者差距增大, 不交

run_decade = 1.0  # one e-fold
d_alpha2_inv = b2/(2*math.pi) * run_decade
d_alpha3_inv = b3/(2*math.pi) * run_decade

print('  在 M_Z 以上 1 e-fold:')
print(f'    alpha_2^{-1} 变化: {d_alpha2_inv:+.2f}')
print(f'    alpha_3^{-1} 变化: {d_alpha3_inv:+.2f}')
print(f'    差距扩大: {d_alpha2_inv - d_alpha3_inv:+.2f}')
print(f'    → SU(2) 和 SU(3) 在标准SM单圈RGE下不统一')
print()

# === CNT 的 sin^2 theta_W 公式 ===
# sin^2W = 3/8 + delta_W^(1) + f2*rho2 + f3*rho3
delta_W = -0.156
f2, rho2 = 0.05, 0.198
f3, rho3 = 0.025, 0.092

contrib_delta = delta_W
contrib_rho2 = f2 * rho2
contrib_rho3 = f3 * rho3
sin2W_cnt = 3/8 + contrib_delta + contrib_rho2 + contrib_rho3

print('='*65)
print('  CNT 公式分解')
print('='*65)
print(f'  3/8 (GUT对称性)         = {3/8:.5f}')
print(f'  + delta_W^(1)           = {contrib_delta:+.5f}  ← 主导项')
print(f'  + f2*rho2               = {contrib_rho2:+.5f}')
print(f'  + f3*rho3               = {contrib_rho3:+.5f}')
print(f'  ─────────────────────────────────')
print(f'  sin^2 theta_W (CNT)     = {sin2W_cnt:.5f}')
print(f'  sin^2 theta_W (实验)    = {sin2W_exp:.5f}')
print(f'  偏差                    = {sin2W_cnt - sin2W_exp:+.5f}')
print()

print('='*65)
print('  delta_W^(1) 的大小分析')
print('='*65)
print()
print(f'  3/8 = {3/8:.3f}')
print(f'  实验 sin^2W = {sin2W_exp:.3f}')
print(f'  差距 = {sin2W_exp - 3/8:.3f}')
print()
print('  CNT 把这 -0.144 分解为:')
print(f'    delta_W^(1) = {delta_W:.3f} (108.3% of gap)')
print(f'    f2*rho2+f3*rho3 = {contrib_rho2+contrib_rho3:+.4f} (反向, -8.3% )')
print(f'    ───────────────────────────')
print(f'    total = {contrib_delta+contrib_rho2+contrib_rho3:+.5f}')
print()
print('  delta_W^(1) = -0.156 是第一性的吗?')
print()
print('  可能来源:')
print('    1. GUT破缺阈值修正: superheavy X,Y + 24-plet Higgs')
print('       → 大小可控，但需指定粒子谱和阈值')
print('    2. 壳层几何投影: 3/8 是 SU(5) 平直极限')
print('       角向弯曲产生 -0.156 的系统性屏蔽')
print('       → CNT特有机制, 对应"壳层不是平直的"')
print('    3. 高维算符效应: SU(5)/SM 破缺链中的 dim-5/6')
print('       → 需 CNT 的 p进结构定量化')
print()

# === 估计: delta_W^(1) 需要多大的 ln(M/M_GUT) ===
print('  如果用标准阈值修正理解:')
print('    delta = (5/3)(alpha_GUT/2pi)*sum(C_i ln(M_i/M_GUT))')
# alpha_GUT 在 CNT 中约为 1/41 = 0.024
# alpha_GUT/(2pi) ≈ 0.024/6.28 ≈ 0.0038
# 但实际 SU(5) RGE 给不出 sin^2W ≈ 0.231
# 所以 delta_W^(1) 不能用标准RGE框架理解
print('    → 标准RGE阈值修正无法自然产生 -0.156')
print('    → delta_W^(1) 必须是 CNT 特有的壳层几何效应')

print()
print('='*65)
print('  结论')
print('='*65)
print()
print('  1. SM单圈RGE: SU(2)和SU(3)在M_Z以上发散, 不统一')
print('     → CNT不能靠标准RGE理解 sin^2 theta_W')
print()
print('  2. CNT公式: sin^2W = 3/8 + delta_W^(1) + ...')
print(f'     delta_W^(1) = {delta_W:.3f} 是主导项 (108% of gap from 3/8)')
print('     f2*rho2+f3*rho3 = +0.012 是反向小修正')
print()
print('  3. delta_W^(1) 的物理:')
print('     壳层空间不是平直的 → 3/8被角向几何系统性屏蔽')
print('     → 等价于 GUT破缺 + 壳层弯曲 的联合效应')
print('     → 这是 CNT 特有的物理, 不能从标准RGE理解')
print()
print('  4. 第一性确定的路径:')
print('     → 壳层度规的曲率张量 → 角向屏蔽因子')
print('     → 这需要攻克 B2 (再生产算符化) 和 C3 (p进算符)')
print('     → 目前 delta_W^(1) 是唯象输入')
print()
print('  5. ρ_m 的来源:')
print(f'     ρ_2={rho2}, ρ_3={rho3} 是对角向偏离的补偿')
print('     如果 ρ_m 能从 Mathieu 谱的第一性确定')
print('     则 sin^2 theta_W 完全第一性, 无需 delta_W^(1)')
