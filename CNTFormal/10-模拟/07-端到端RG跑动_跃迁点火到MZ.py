"""
CNT 端到端 RG 跑动：从质数动力跃迁点火到 M_Z
==============================================

核心问题：给定 N_cycle=30, k=30↔M_Z, 跃迁点 k=2,3,5,
能否从第一性原理计算 α_s(M_Z), α(M_Z), sin²θ_W？

框架：
    1. N_cycle = 30 (adelic 约束确定)
    2. 能标对数分布: μ_k = M_P · (M_Z/M_P)^{k/30}
    3. 跃迁点火: k=2→SU(3), k=3→SU(2), k=5→U(1)
    4. 点火条件: 耦合常数由 S_p = log(p) 决定
    5. RG 跑动: SM 单圈 β 函数
    6. 输出: M_Z 处的三个耦合常数

认识论地位: [数值探索] + [候选假设]
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import os
import platform

if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 物理常数
# ============================================================
M_P = 1.22089e19   # Planck 质量 (GeV)
M_Z = 91.1876       # Z 玻色子质量 (GeV)
N_CYCLE = 30
GAUGE_PRIMES = [2, 3, 5]

# SM 单圈 β 函数系数 (MS-bar)
# dα_i/d(ln μ) = -b_i · α_i²/(2π)
# 或等价地: d(α_i^{-1})/d(ln μ) = b_i/(2π)
B_SM = {
    'SU3':  7.0,      # b_3 = 11 - 4n_f/3, n_f=6
    'SU2':  19.0/6,   # b_2 = 22/3 - 4n_f/3 - 1/6, n_f=6, n_H=1
    'U1':  -41.0/10,  # b_1 = -4n_f/3 - 1/10, n_f=6 (GUT归一化)
}

# SM 实测值 at M_Z (PDG 2024)
EXP = {
    'alpha_s_MZ': 0.1180,
    'alpha_s_MZ_err': 0.0009,
    'alpha_inv_MZ': 127.952,
    'alpha_inv_MZ_err': 0.009,
    'sin2_thetaW_MZ': 0.23122,
    'sin2_thetaW_MZ_err': 0.00003,
}

# 从实测值推导的 α_2, α_1 at M_Z
EXP['alpha_em_MZ'] = 1.0 / EXP['alpha_inv_MZ']
EXP['alpha_2_MZ'] = EXP['alpha_em_MZ'] / EXP['sin2_thetaW_MZ']
EXP['alpha_1_MZ'] = (5.0/3) * EXP['alpha_em_MZ'] / (1 - EXP['sin2_thetaW_MZ'])

# ============================================================
# 第1部分: 能标确定
# ============================================================

def energy_scale(k: int) -> float:
    """
    对数分布能标: μ_k = M_P · (M_Z/M_P)^{k/N_cycle}
    
    性质:
    - μ_30 = M_Z
    - μ_1 = M_P · (M_Z/M_P)^{1/30} ≈ 2.8×10^{18} GeV
    - μ_2 = M_P · (M_Z/M_P)^{2/30} ≈ 1.1×10^{19} GeV (> M_P, 需要截断)
    """
    return M_P * (M_Z / M_P) ** (k / N_CYCLE)

def print_energy_scales():
    """打印跃迁点能标。"""
    print("=" * 60)
    print("能标分布 (对数分布)")
    print("=" * 60)
    for k in range(1, 31):
        mu = energy_scale(k)
        markers = []
        if k in GAUGE_PRIMES:
            markers.append(f"← 跃迁点火 (p={k})")
        if k == 30:
            markers.append("← M_Z")
        if k in [4, 8, 9, 16, 25, 27, 32]:
            markers.append("← Φ_Λ>0")
        marker_str = " ".join(markers) if markers else ""
        print(f"  k={k:2d}: μ = {mu:.2e} GeV  {marker_str}")

# ============================================================
# 第2部分: RG 跑动方程
# ============================================================

def run_single_rg(alpha_initial: float, mu_initial: float, mu_final: float, 
                  b: float) -> float:
    """
    单圈 RG 跑动。
    
    α^{-1}(μ_final) = α^{-1}(μ_initial) + b/(2π) · ln(μ_final/μ_initial)
    
    参数:
        alpha_initial: 初始能标处的耦合常数
        mu_initial: 初始能标 (GeV)
        mu_final: 目标能标 (GeV)
        b: β 函数系数
    
    返回:
        alpha_final: 目标能标处的耦合常数
    """
    alpha_inv_initial = 1.0 / alpha_initial
    alpha_inv_final = alpha_inv_initial + b / (2 * np.pi) * np.log(mu_final / mu_initial)
    return 1.0 / alpha_inv_final

def run_rg_from_ignition_to_MZ(alphas_ignition: dict) -> dict:
    """
    从跃迁点火点跑动到 M_Z。
    
    参数:
        alphas_ignition: {'SU3': α_3, 'SU2': α_2, 'U1': α_1} at ignition points
    
    返回:
        alphas_MZ: 跑动到 M_Z 后的耦合常数
    """
    mu_30 = M_Z
    mu_ignition = {
        'SU3': energy_scale(2),  # k=2
        'SU2': energy_scale(3),  # k=3
        'U1':  energy_scale(5),  # k=5
    }
    
    alphas_MZ = {}
    for key, b in [('SU3', B_SM['SU3']), ('SU2', B_SM['SU2']), ('U1', B_SM['U1'])]:
        alpha = run_single_rg(
            alphas_ignition[key], mu_ignition[key], mu_30, b
        )
        alphas_MZ[key] = alpha
    
    return alphas_MZ

def run_rg_from_MZ_to_ignition() -> dict:
    """
    反向跑动: 从 M_Z 实测值反推跃迁点火点的耦合常数。
    
    这是"上帝视角"——如果 SM 是正确的，点火点耦合常数应该是多少？
    """
    mu_30 = M_Z
    mu_ignition = {
        'SU3': energy_scale(2),
        'SU2': energy_scale(3),
        'U1':  energy_scale(5),
    }
    
    alphas_ignition = {}
    alphas_MZ = {
        'SU3': EXP['alpha_s_MZ'],
        'SU2': EXP['alpha_2_MZ'],
        'U1':  EXP['alpha_1_MZ'],
    }
    
    for key, b in [('SU3', B_SM['SU3']), ('SU2', B_SM['SU2']), ('U1', B_SM['U1'])]:
        # 反向跑动: α^{-1}(μ_ign) = α^{-1}(M_Z) + b/(2π) · ln(μ_ign/M_Z)
        alpha = run_single_rg(
            alphas_MZ[key], mu_30, mu_ignition[key], b
        )
        alphas_ignition[key] = alpha
    
    return alphas_ignition, mu_ignition

# ============================================================
# 第3部分: 点火条件假设
# ============================================================

def hypothesis_direct(scale: float = 1.0) -> dict:
    """H1: α_i(k=p) = scale · log(p)  (直接比例)"""
    return {
        'SU3': scale * np.log(2),
        'SU2': scale * np.log(3),
        'U1':  scale * np.log(5),
    }

def hypothesis_inverse(scale: float = 1.0) -> dict:
    """H2: α_i(k=p) = scale / log(p)  (反比例)"""
    return {
        'SU3': scale / np.log(2),
        'SU2': scale / np.log(3),
        'U1':  scale / np.log(5),
    }

def hypothesis_natural() -> dict:
    """H3: α_i(k=p) = log(p) / (2π)  (自然量子归一化)"""
    return {
        'SU3': np.log(2) / (2 * np.pi),
        'SU2': np.log(3) / (2 * np.pi),
        'U1':  np.log(5) / (2 * np.pi),
    }

def hypothesis_action_share() -> dict:
    """H4: α_i(k=p) = α_0 · log(p) / log(30)  (作用量份额)"""
    # 假设 α_0 是 Planck 尺度耦合 ≈ 1
    alpha_0 = 1.0
    return {
        'SU3': alpha_0 * np.log(2) / np.log(30),
        'SU2': alpha_0 * np.log(3) / np.log(30),
        'U1':  alpha_0 * np.log(5) / np.log(30),
    }

def hypothesis_inverse_natural() -> dict:
    """H5: α_i(k=p) = 1 / (2π · log(p))  (反比例自然归一化)"""
    return {
        'SU3': 1.0 / (2 * np.pi * np.log(2)),
        'SU2': 1.0 / (2 * np.pi * np.log(3)),
        'U1':  1.0 / (2 * np.pi * np.log(5)),
    }

def hypothesis_inverse_2pi_ncycle() -> dict:
    """H6: α_i(k=p) = 1 / (2π · N_cycle · log(p))"""
    return {
        'SU3': 1.0 / (2 * np.pi * N_CYCLE * np.log(2)),
        'SU2': 1.0 / (2 * np.pi * N_CYCLE * np.log(3)),
        'U1':  1.0 / (2 * np.pi * N_CYCLE * np.log(5)),
    }

# ============================================================
# 第4部分: 扫描与拟合
# ============================================================

def scan_hypothesis(hypothesis_name: str, 
                    ignition_func,
                    scale_range: tuple = None) -> dict:
    """
    对可调参数的假设进行扫描，找到最佳拟合 SM 实测值的参数。
    """
    best_result = None
    best_loss = np.inf
    
    if scale_range is not None:
        scales = np.logspace(np.log10(scale_range[0]), np.log10(scale_range[1]), 200)
    else:
        scales = [1.0]
    
    for scale in scales:
        if scale_range is not None:
            alphas_ignition = ignition_func(scale)
        else:
            alphas_ignition = ignition_func()
        
        alphas_MZ = run_rg_from_ignition_to_MZ(alphas_ignition)
        
        # 损失函数: 相对误差平方和
        loss = 0.0
        loss += ((alphas_MZ['SU3'] - EXP['alpha_s_MZ']) / EXP['alpha_s_MZ']) ** 2
        loss += ((alphas_MZ['SU2'] - EXP['alpha_2_MZ']) / EXP['alpha_2_MZ']) ** 2
        loss += ((alphas_MZ['U1'] - EXP['alpha_1_MZ']) / EXP['alpha_1_MZ']) ** 2
        
        if loss < best_loss:
            best_loss = loss
            best_result = {
                'hypothesis': hypothesis_name,
                'scale': float(scale) if scale_range else None,
                'alphas_ignition': alphas_ignition,
                'alphas_MZ': alphas_MZ,
                'loss': float(loss),
                'alpha_s_MZ': float(alphas_MZ['SU3']),
                'alpha_2_MZ': float(alphas_MZ['SU2']),
                'alpha_1_MZ': float(alphas_MZ['U1']),
            }
    
    return best_result

def compute_derived_quantities(alphas_MZ: dict) -> dict:
    """从 SU3, SU2, U1 耦合计算 α_em 和 sin²θ_W。"""
    alpha_1 = alphas_MZ['U1']
    alpha_2 = alphas_MZ['SU2']
    
    # GUT 归一化: α_Y = (3/5)α_1
    alpha_Y = (3.0/5) * alpha_1
    
    # sin²θ_W = α_Y / (α_2 + α_Y) = g'²/(g² + g'²)
    sin2_thetaW = alpha_Y / (alpha_2 + alpha_Y)
    
    # α_em = α_2 · sin²θ_W = α_2 · α_Y / (α_2 + α_Y)
    alpha_em = alpha_2 * sin2_thetaW
    
    return {
        'alpha_em': float(alpha_em),
        'alpha_em_inv': float(1.0 / alpha_em),
        'sin2_thetaW': float(sin2_thetaW),
    }

# ============================================================
# 第5部分: 综合分析
# ============================================================

def run_full_analysis():
    """运行完整分析。"""
    results = {}
    
    # 1. 能标分布
    print_energy_scales()
    
    # 2. 反向跑动: 从 M_Z 实测值反推点火点
    print("\n" + "=" * 60)
    print("反向跑动: M_Z 实测值 → 跃迁点火点")
    print("=" * 60)
    alphas_ignition_from_SM, mu_ignition = run_rg_from_MZ_to_ignition()
    for key, val in alphas_ignition_from_SM.items():
        print(f"  {key}: α(k=p) = {val:.6f}  at μ = {mu_ignition[key]:.2e} GeV")
        print(f"        α^{-1} = {1.0/val:.4f}")
    
    results['reverse_ignition'] = {
        key: float(val) for key, val in alphas_ignition_from_SM.items()
    }
    results['ignition_energies'] = {
        key: float(val) for key, val in mu_ignition.items()
    }
    
    # 3. 计算 ignition 处的 action 比值
    print("\n--- 点火点耦合常数与 log(p) 的关系 ---")
    for key, p in [('SU3', 2), ('SU2', 3), ('U1', 5)]:
        alpha = alphas_ignition_from_SM[key]
        ratio = alpha / np.log(p)
        inv_ratio = alpha * np.log(p)
        print(f"  {key} (p={p}): α/log(p) = {ratio:.6f},  α·log(p) = {inv_ratio:.6f}")
    
    # 4. 正向假设扫描
    print("\n" + "=" * 60)
    print("正向假设: 跃迁点火 → M_Z")
    print("=" * 60)
    
    hypotheses = [
        ('H1: α ∝ log(p)', lambda s: hypothesis_direct(s), (1e-3, 10)),
        ('H2: α ∝ 1/log(p)', lambda s: hypothesis_inverse(s), (1e-3, 10)),
        ('H3: α = log(p)/(2π)', hypothesis_natural, None),
        ('H4: α = α₀·log(p)/log(30)', hypothesis_action_share, None),
        ('H5: α = 1/(2π·log(p))', hypothesis_inverse_natural, None),
        ('H6: α = 1/(2π·N·log(p))', hypothesis_inverse_2pi_ncycle, None),
    ]
    
    all_hypothesis_results = []
    for name, func, srange in hypotheses:
        result = scan_hypothesis(name, func, srange)
        if result:
            derived = compute_derived_quantities(result['alphas_MZ'])
            result.update(derived)
            all_hypothesis_results.append(result)
            
            print(f"\n  {name}")
            if result['scale'] is not None:
                print(f"    最佳 scale = {result['scale']:.4f}")
            print(f"    点火: α₃={result['alphas_ignition']['SU3']:.6f}, "
                  f"α₂={result['alphas_ignition']['SU2']:.6f}, "
                  f"α₁={result['alphas_ignition']['U1']:.6f}")
            print(f"    M_Z:  α₃={result['alpha_s_MZ']:.6f}, "
                  f"α₂={result['alpha_2_MZ']:.6f}, "
                  f"α₁={result['alpha_1_MZ']:.6f}")
            print(f"    导出: α_em={result['alpha_em']:.6f} "
                  f"(α⁻¹={result['alpha_em_inv']:.2f}), "
                  f"sin²θ_W={result['sin2_thetaW']:.6f}")
            print(f"    损失: {result['loss']:.6e}")
    
    results['hypotheses'] = all_hypothesis_results
    
    # 5. 实验对比
    print("\n" + "=" * 60)
    print("实验值对比")
    print("=" * 60)
    print(f"  α_s(M_Z)   = {EXP['alpha_s_MZ']:.4f} ± {EXP['alpha_s_MZ_err']:.4f}")
    print(f"  α⁻¹(M_Z)   = {EXP['alpha_inv_MZ']:.3f} ± {EXP['alpha_inv_MZ_err']:.3f}")
    print(f"  sin²θ_W    = {EXP['sin2_thetaW_MZ']:.5f} ± {EXP['sin2_thetaW_MZ_err']:.5f}")
    print(f"  α_2(M_Z)   = {EXP['alpha_2_MZ']:.6f}")
    print(f"  α_1(M_Z)   = {EXP['alpha_1_MZ']:.6f}")
    
    return results, alphas_ignition_from_SM, mu_ignition

# ============================================================
# 第6部分: 可视化
# ============================================================

def plot_results(results, alphas_ignition_from_SM, mu_ignition):
    """生成综合分析可视化。"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 图1: 能标分布
    ax = axes[0, 0]
    ks = np.arange(1, 31)
    mus = [energy_scale(k) for k in ks]
    ax.semilogy(ks, mus, 'b-', linewidth=2)
    # 标注跃迁点
    for i, p in enumerate(GAUGE_PRIMES):
        ax.scatter([p], [energy_scale(p)], s=100, c=['red', 'green', 'orange'][i], 
                  zorder=5, label=f'p={p} (跃迁点火)')
    ax.scatter([30], [M_Z], s=100, c='blue', marker='s', zorder=5, label='M_Z')
    ax.axhline(y=M_P, color='gray', linestyle='--', alpha=0.5, label='M_P')
    ax.set_xlabel('再生产计数 k')
    ax.set_ylabel('能标 μ (GeV)')
    ax.set_title('能标对数分布: μ_k = M_P·(M_Z/M_P)^{k/30}')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # 图2: RG 跑动曲线
    ax = axes[0, 1]
    mu_range = np.logspace(np.log10(M_Z), np.log10(energy_scale(1)), 300)
    
    for key, p, color, b in [('SU3', 2, 'red', B_SM['SU3']), 
                               ('SU2', 3, 'green', B_SM['SU2']),
                               ('U1', 5, 'orange', B_SM['U1'])]:
        mu_ign = energy_scale(p)
        alpha_ign = alphas_ignition_from_SM[key]
        alphas = []
        for mu in mu_range:
            alpha = run_single_rg(alpha_ign, mu_ign, mu, b)
            alphas.append(1.0 / alpha)
        ax.semilogx(mu_range, alphas, color=color, linewidth=2, 
                   label=f'{key} (p={p})')
    
    ax.set_xlabel('能标 μ (GeV)')
    ax.set_ylabel('α⁻¹')
    ax.set_title('RG 跑动: α⁻¹(μ) (从SM反推点火点)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.invert_xaxis()
    
    # 图3: 点火点耦合常数 vs log(p)
    ax = axes[0, 2]
    primes = [2, 3, 5]
    log_primes = [np.log(p) for p in primes]
    alphas = [alphas_ignition_from_SM[key] for key in ['SU3', 'SU2', 'U1']]
    alphas_inv = [1.0/a for a in alphas]
    
    colors = ['red', 'green', 'orange']
    labels = ['SU(3)', 'SU(2)', 'U(1)']
    
    ax.scatter(log_primes, alphas_inv, c=colors, s=100, zorder=5)
    for i in range(3):
        ax.annotate(f'{labels[i]}\nα⁻¹={alphas_inv[i]:.1f}', 
                   (log_primes[i], alphas_inv[i]),
                   textcoords="offset points", xytext=(10, 10), fontsize=8)
    
    # 线性拟合
    coeffs = np.polyfit(log_primes, alphas_inv, 1)
    x_fit = np.linspace(min(log_primes)*0.9, max(log_primes)*1.1, 100)
    y_fit = np.polyval(coeffs, x_fit)
    ax.plot(x_fit, y_fit, 'k--', alpha=0.5, 
           label=f'α⁻¹ = {coeffs[0]:.1f}·log(p) + {coeffs[1]:.1f}')
    
    ax.set_xlabel('log(p)')
    ax.set_ylabel('α⁻¹ (点火点)')
    ax.set_title('点火点耦合常数 vs log(p)\n(从SM实验值反推)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # 图4: 各假设的 M_Z 预测 vs 实验
    ax = axes[1, 0]
    hyps = results['hypotheses']
    if hyps:
        names = [h['hypothesis'] for h in hyps]
        losses = [h['loss'] for h in hyps]
        ax.barh(range(len(names)), losses, color='steelblue', alpha=0.7)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels([n.split(':')[0] for n in names], fontsize=8)
        ax.set_xlabel('损失 (相对误差平方和)')
        ax.set_title('各假设的拟合质量')
        ax.set_xscale('log')
    
    # 图5: 最佳假设的耦合常数对比
    ax = axes[1, 1]
    if hyps:
        best = min(hyps, key=lambda h: h['loss'])
        groups = ['SU(3)', 'SU(2)', 'U(1)']
        exp_vals = [EXP['alpha_s_MZ'], EXP['alpha_2_MZ'], EXP['alpha_1_MZ']]
        pred_vals = [best['alpha_s_MZ'], best['alpha_2_MZ'], best['alpha_1_MZ']]
        
        x = np.arange(len(groups))
        width = 0.35
        ax.bar(x - width/2, exp_vals, width, color='gray', alpha=0.7, label='实验值')
        ax.bar(x + width/2, pred_vals, width, color='steelblue', alpha=0.7, label=f'{best["hypothesis"].split(":")[0]}')
        ax.set_xticks(x)
        ax.set_xticklabels(groups)
        ax.set_ylabel('α')
        ax.set_title('最佳假设 vs 实验值')
        ax.legend(fontsize=8)
    
    # 图6: α_em 和 sin²θ_W 的预测
    ax = axes[1, 2]
    if hyps:
        h_names = [h['hypothesis'].split(':')[0] for h in hyps]
        sin2_pred = [h['sin2_thetaW'] for h in hyps]
        alpha_inv_pred = [h['alpha_em_inv'] for h in hyps]
        
        x = np.arange(len(hyps))
        # 归一化偏差
        sin2_dev = [(s - EXP['sin2_thetaW_MZ']) / EXP['sin2_thetaW_MZ_err'] for s in sin2_pred]
        alpha_dev = [(a - EXP['alpha_inv_MZ']) / EXP['alpha_inv_MZ_err'] for a in alpha_inv_pred]
        
        width = 0.35
        ax.bar(x - width/2, sin2_dev, width, color='coral', alpha=0.7, label='sin²θ_W 偏差/σ')
        ax.bar(x + width/2, alpha_dev, width, color='steelblue', alpha=0.7, label='α⁻¹ 偏差/σ')
        ax.set_xticks(x)
        ax.set_xticklabels(h_names, fontsize=7)
        ax.axhline(y=0, color='black', linestyle='-')
        ax.set_ylabel('偏差 / 实验误差')
        ax.set_title('sin²θ_W 和 α⁻¹ 的预测偏差')
        ax.legend(fontsize=8)
    
    plt.tight_layout()
    output_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(output_dir, '07-端到端RG跑动.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: 07-端到端RG跑动.png")

# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    results, alphas_ignition_from_SM, mu_ignition = run_full_analysis()
    plot_results(results, alphas_ignition_from_SM, mu_ignition)
    
    # 保存结果
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, '07-端到端RG跑动_结果.json')
    
    # 清理不可序列化的对象
    serializable = {
        'reverse_ignition': results['reverse_ignition'],
        'ignition_energies': results['ignition_energies'],
        'hypotheses': results['hypotheses'],
        'experiment': {
            'alpha_s_MZ': EXP['alpha_s_MZ'],
            'alpha_2_MZ': EXP['alpha_2_MZ'],
            'alpha_1_MZ': EXP['alpha_1_MZ'],
            'alpha_em_MZ': EXP['alpha_em_MZ'],
            'alpha_inv_MZ': EXP['alpha_inv_MZ'],
            'sin2_thetaW_MZ': EXP['sin2_thetaW_MZ'],
        },
        'key_finding': ''  # 将在分析后填充
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存: 07-端到端RG跑动_结果.json")