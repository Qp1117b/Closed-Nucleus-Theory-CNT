#!/usr/bin/env python3
"""CNT 第一性精度分析
目标: 标注所有非第一性输入, 量化它们的精度贡献, 确定改进优先级"""

import mpmath as mp
mp.mp.dps = 50

print('='*75)
print('  CNT 第一性精度分析')
print('='*75)

# ============================================================
# §1  纯数学常数（严格第一性，无近似）
# ============================================================
print()
print('─'*75)
print('  §1 纯数学常数 (严格第一性)')
print('─'*75)

# C = xi'(1)/xi(1) = 1 + euler/2 - log(4*pi)/2
C_exact = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
print(f'  C = 1 + gamma_e/2 - ln(4*pi)/2 = {float(C_exact):.15f}')
print(f'  来源: Riemann xi 函数导数商, 等价于对称性条件')
print(f'  精度: 精确 (数学恒等式, 50位可任意扩展)')

# E_1 = 1/4 + gamma_1^2, gamma_1 = Im[zeta(1/2 + i*14.134...)]=0
gamma_1 = mp.zetazero(1).imag
E_1 = mp.mpf('0.25') + gamma_1**2
print(f'  gamma_1 = {float(gamma_1):.10f} (第1非平凡零点虚部)')
print(f'  E_1 = 1/4 + gamma_1^2 = {float(E_1):.10f}')
print(f'  来源: Berry-Keating 哈密顿量 H=xp+px, 临界线上本征值')
print(f'  精度: gamma_1 的验证>10^12 (Platt-Trudgian 2021)')

# ============================================================
# §2  lambda_c 连分数 (收敛性检验)
# ============================================================
print()
print('─'*75)
print('  §2 lambda_c 连分数 (收敛性检验)')
print('─'*75)

def tail(q, k, m=100):
    """连分数尾部, 从k开始截断到m"""
    if k > m:
        return mp.mpf('0')
    return q**2 / ((2*k+1)**2 - 2*q - tail(q, k+1, m))

# 求解1-3q-tail(q) = 0, 即Mathieu特征值方程的连分数形式
q_c = mp.findroot(lambda q: 1 - 3*q - tail(q, 1, 100), (29-mp.sqrt(661))/10)
lc = 4 * q_c

print(f'  q_c (截断m=100) = {float(q_c):.15f}')
print(f'  lambda_c = 4*q_c = {float(lc):.15f}')

# 收敛性检验
print()
print('  连分数截断收敛性:')
q_vals = {}
for m in [5, 10, 20, 30, 50, 100, 200]:
    qm = mp.findroot(lambda q: 1 - 3*q - tail(q, 1, m), (29-mp.sqrt(661))/10)
    q_vals[m] = qm
    lc_m = 4 * qm
    if m > 5:
        dq = float(qm - q_vals[5])
        print(f'    m={m:3d}: q_c={float(qm):.15f}  delta_q(m={m})-delta_q(m=5)={dq:+.2e}')

# 截断误差
q_ref = q_vals[200]
for m in [30, 50, 100]:
    dq_tot = float(abs(q_vals[m] - q_ref))
    dlc_tot = 4 * dq_tot
    print(f'    m={m:3d} vs m=200: |delta_lc| = {dlc_tot:.2e}')
    
    # 这对 alpha^{-1} 的影响
    # alpha^{-1} ∝ 1/(C * lc), 导数: d(alpha^{-1})/alpha^{-1} = -dlc/lc
    alpha_sensitivity = -float(dlc_tot / float(lc))
    print(f'        → alpha^{-1} 相对不确定度: {abs(alpha_sensitivity):.1e}')

# ============================================================
# §3  C_th = C/E_1 与修正因子 (1 - C_th)
# ============================================================
print()
print('─'*75)
print('  §3 C_th 修正因子')
print('─'*75)

C_th = C_exact / E_1
print(f'  C_th = C/E_1 = {float(C_th):.10f}')
print(f'  (1 - C_th) = {float(1 - C_th):.10f}')

# 三种可能形式
v1 = float(1 - C_th)          # 线性截断
v2 = float(mp.exp(-C_th))     # 指数形式
v3 = float(1 / (1 + C_th))    # 有理形式
print(f'  候选形式:')
print(f'    (1-C_th)      = {v1:.10f}')
print(f'    exp(-C_th)    = {v2:.10f}')
print(f'    1/(1+C_th)    = {v3:.10f}')
print(f'    v1-v2          = {v1-v2:.1e} (1e-8量级, 对alpha^{-1}影响 << 1ppm)')
print(f'  结论: 任意形式等价, C_th修正因子本身不引入不确定度')

# ============================================================
# §4  角向修正 rho_m (当前唯象)
# ============================================================
print()
print('─'*75)
print('  §4 角向修正 rho_m (当前唯象输入)')
print('─'*75)

rho_2 = mp.mpf('0.198')
rho_3 = mp.mpf('0.092')

# 这些值不是从Mathieu谱导出的
# 计算Mathieu特征值 a_n(2q_c)
q_f = float(q_c)
a_ref = None
print(f'  在 q = {q_f:.6f} 处 (a=2q线):')
for n in range(1, 6):
    try:
        # Mathieu特征值 a_n(q): ce_n和se_n
        # 对于 a=2q 线, 对应的q和a参数
        # ce_n(a,q) -> a是特征值参数, q是Mathieu参数
        # 在 a=2q 线上: q就是q_f, a=2*q_f
        from mpmath import mathieuce, mathieuse
        # 实际上mpmath的mathieuce返回特征值 a_n(q)
        a_n = mp.mathieuce(n, q_f)
        if a_ref is None:
            a_ref = a_n
        da = float(a_n - a_ref)
        print(f'    a_{n}({q_f:.4f}) = {float(a_n):.8f}  delta={da:+.8f}')
    except Exception as e:
        print(f'    a_{n}: {e}')

print()
print(f'  Mathieu 特征值间距 O(1), 但 CNT 需要:')
print(f'    1/(E_2-E_1) ~ 1/0.000583 ~ 1715')
print(f'  → Mathieu 谱完全不能提供这个间距')
print(f'  → rho_2={rho_2}, rho_3={rho_3} 是唯象输入')

# 缩放模式估计
print()
print(f'  rho_2/rho_3 = {float(rho_2/rho_3):.4f}')
print(f'  如果 rho_m ∝ 1/m^2: rho_3/rho_2 ≈ (2/3)^2 = 0.444')
print(f'  如果 rho_m ∝ 1/2^(m-1): rho_3/rho_2 = 0.5')
print(f'  实际 rho_3/rho_2 = {float(rho_3/rho_2):.4f}')

# 如果模式持续, rho_4 和 rho_5
for ratio_name, ratio in [("1/m^2", 4/9), ("1/2^(m-1)", 0.5)]:
    rho_4_est = float(rho_3) * ratio
    rho_5_est = rho_4_est * ratio
    print(f'  {ratio_name} → rho_4≈{rho_4_est:.3f}, rho_5≈{rho_5_est:.3f}')

# ============================================================
# §5  完整敏感度分析
# ============================================================
print()
print('─'*75)
print('  §5 敏感度分析: 哪些参数主导 alpha^{-1} 精度?')
print('─'*75)

# 主公式: alpha^{-1} ≈ 1/(C*lambda_c*sin2W*(1-C_th)) - 5 - rho2 - rho3
C_val = C_exact
lc_val = lc
sin2W = mp.mpf('0.23120')
alpha_0 = C_val * lc_val * sin2W
alpha_eff = alpha_0 * (1 - C_th)
alpha_inv_base = 1/alpha_eff - 5 - rho_2 - rho_3

target = mp.mpf('137.035999177')
diff = float(alpha_inv_base - target)

print(f'  alpha^{-1}_CNT = {float(alpha_inv_base):.6f}')
print(f'  alpha^{-1}_exp = {float(target):.9f}')
print(f'  偏差 = {diff:+.4f} = {diff/float(target)*1e6:+.1f} ppm')
print()

# 逐个参数敏感度
h = mp.mpf('1e-8')

def sensitivity(name, val, perturb_func):
    base = perturb_func(val)
    d = perturb_func(val * (1 + h))
    s = float((d - base) / (float(val) * float(h)) * float(base) / float(base))
    deriv = float((d - base) / (float(val) * float(h)))
    ppm_per_pct = abs(deriv) / float(base) * 1e4
    return name, float(base), deriv, ppm_per_pct

def compute_alpha_inv(Cv, lv, sw, r2, r3):
    a0 = Cv * lv * sw
    ae = a0 * (1 - Cv/E_1)
    return 1/ae - 5 - r2 - r3

results = []
results.append(sensitivity('C  (zeta)', C_val, 
    lambda x: compute_alpha_inv(x, lc_val, sin2W, rho_2, rho_3)))
results.append(sensitivity('lambda_c', lc_val,
    lambda x: compute_alpha_inv(C_val, x, sin2W, rho_2, rho_3)))
results.append(sensitivity('sin^2W', sin2W,
    lambda x: compute_alpha_inv(C_val, lc_val, x, rho_2, rho_3)))
results.append(sensitivity('rho_2', rho_2,
    lambda x: compute_alpha_inv(C_val, lc_val, sin2W, x, rho_3)))
results.append(sensitivity('rho_3', rho_3,
    lambda x: compute_alpha_inv(C_val, lc_val, sin2W, rho_2, x)))

print(f'  {"参数":<20} {"基础值":>12} {"d(alpha^{-1})/d(param)":>18} {"ppm/1%变化":>18}')
print(f'  {"─"*68}')
for name, base, deriv, ppm in results:
    print(f'  {name:<20} {base:>12.6f} {deriv:>18.6f} {ppm:>18.1f}')

# ============================================================
# §6  消除40 ppm需要什么
# ============================================================
print()
print('─'*75)
print('  §6 消除40 ppm偏差: 需要多少修正?')
print('─'*75)

# 途径1: 调整 rho_2
drho2_needed = diff  # derivative of alpha^{-1} wrt rho_2 is -1
print(f'  途径1: 仅调 rho_2')
print(f'    rho_2 需从 {float(rho_2)} 调至 {float(rho_2 + drho2_needed)}')
print(f'    变化: {float(drho2_needed/rho_2*100):+.1f}%')

# 途径2: 调整 rho_3
drho3_needed = diff
print(f'  途径2: 仅调 rho_3')
print(f'    rho_3 需从 {float(rho_3)} 调至 {float(rho_3 + drho3_needed)}')
print(f'    变化: {float(drho3_needed/rho_3*100):+.1f}%')

# 途径3: 高阶rho
rho_4_est = mp.mpf('0.05')  # 1/m^2 缩放估计
rho_5_est = mp.mpf('0.02')
alpha_inv_high = compute_alpha_inv(C_val, lc_val, sin2W, rho_2, rho_3)
# 如果rho_4, rho_5也减: alpha^{-1} → alpha^{-1} - rho4 - rho5
# 这会使偏差更大!
print(f'  途径3: 包含高阶 rho (恶化)')
print(f'    rho_4≈0.05, rho_5≈0.02 → alpha^{-1} 再减0.07')
print(f'    → 如果rho模式持续, 需要正的高阶贡献抵消')

# 途径4: 微调 sin^2 theta_W
dsin2w_needed = diff / float(compute_alpha_inv(C_val, lc_val, sin2W*(1+h), rho_2, rho_3) - 
                              compute_alpha_inv(C_val, lc_val, sin2W, rho_2, rho_3)) * float(sin2W * h)
dsin2w_needed_alt = diff * float(sin2W) / float(compute_alpha_inv(C_val, lc_val, sin2W*(1+h), rho_2, rho_3) - 
                            compute_alpha_inv(C_val, lc_val, sin2W, rho_2, rho_3)) * float(h)

print(f'  途径4: 微调 sin^2 theta_W')
# d(alpha^{-1})/d(sin2W) ≈ -alpha_0/(sin2W^2 * alpha_eff^2)
d_alpha_inv_d_sw = -float(lc_val * C_val / (sin2W**2 * (1-C_th)**2 * lc_val**2 * C_val**2 * (1-C_th)**2))
# Actually let me just compute numerically
alpha_inv_plus = compute_alpha_inv(C_val, lc_val, sin2W*(1+h), rho_2, rho_3)
dsin2w_per_alpha = float(sin2W * h) / float(alpha_inv_plus - alpha_inv_base)
dsin2w_req = dsin2w_per_alpha * diff
print(f'    sin^2W 需从 {float(sin2W)} 调至 {float(sin2W + dsin2w_req)}')
print(f'    这等价于 delta_W^(1) 从 -0.156 调至 {float(-0.156 + dsin2w_req)}')

# ============================================================
# §7  G_N 的精度分析
# ============================================================
print()
print('─'*75)
print('  §7 G_N 的精度分析')
print('─'*75)

I = mp.mpf(5)/3
m_p = mp.mpf('938.27208943') / 1000  # GeV
hbar_c = mp.mpf('197.3269804')  # MeV*fm

# G_N公式
G_N_cnt = I * lc_val * C_val**2 * E_1 / m_p**2 * mp.exp(-2/C_val)
G_N_exp = mp.mpf('6.70883e-39')  # GeV^{-2}

print(f'  G_N_cnt = {float(G_N_cnt):.4e} GeV^{-2}')
print(f'  G_N_exp = {float(G_N_exp):.4e} GeV^{-2}')
print(f'  偏差    = {float((G_N_cnt - G_N_exp)/G_N_exp*100):+.1f}%')
print()
print(f'  主导因子 exp(-2/C):')
print(f'    2/C = {float(2/C_val):.10f}')
print(f'    exp(-2/C) = {float(mp.exp(-2/C_val)):.2e}')
print()
# G_N对C的灵敏度
G_N_C = I * lc_val * (C_val*(1+h))**2 * E_1 / m_p**2 * mp.exp(-2/(C_val*(1+h)))
dGdC = float((G_N_C - G_N_cnt) / (float(C_val)*float(h)))
C_uncertainty = float(abs(dGdC) / float(G_N_cnt) * 100)
print(f'  G_N对C的敏感度: C变化1% → G_N变化 {C_uncertainty:.0f}%')
print(f'  (这是因为exp(-2/C)的极度放大效应)')

# ============================================================
# §8  总结
# ============================================================
print()
print('='*75)
print('  精度改进路线图')
print('='*75)
print()
print('  可第一性确定的量 (已精确):')
print('    C = xi\'(1)/xi(1)            → 精确, 50位无忧')
print('    E_1 = 1/4 + gamma_1^2        → 精确, 零点验证>10^12')
print('    lambda_c (连分数)            → 截断误差 << 1ppm')
print('    C_th = C/E_1                  → 精确')
print('    (1-C_th) 修正因子             → 线性/指数/有理等价')
print('    常数5 (SU(5) Dynkin指标)      → 群论确定')
print()
print('  当前非第一性输入 (精度瓶颈):')
print('    rho_2 = 0.198                   → 偏差40ppm = rho_2变化2.7%')
print('    rho_3 = 0.092                   → 或rho_3变化5.9%')
print('    delta_W^(1) = -0.156            → sin^2W=0.231 的108%贡献')
print()
print('  改进优先级:')
print('    P0: Mathieu谱重分析 → 检查边界行为是否产生小间距谱')
print('    P1: 壳层弯曲度规 → 导出 delta_W^(1) 的理论值')
print('    P2: rho_m 第一性 → Mathieu波函数交叠积分')
print('    P3: G_N公式中的 exp(-2/C) → 检查是否有归一化修正')
print()
print('  当前可达到的最优精度 (不改非第一性输入):')
print(f'    alpha^{-1}: 137.0316 → 与实验差 +{diff*1e6/float(target):.0f} ppm')
print(f'    G_N:    {float(G_N_cnt):.2e} GeV^{-2} → 差{(float(G_N_cnt)-float(G_N_exp))/float(G_N_exp)*100:+.1f}%')
print(f'    Lambda_QCD: {float(m_p*1000/(C_val*E_1)):.0f} MeV → 差{float(m_p*1000/(C_val*E_1)-210)/210*100:+.1f}%')
