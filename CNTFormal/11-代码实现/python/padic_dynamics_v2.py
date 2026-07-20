"""
CNT p进动力学研究 - 第二版 (v2)
=======================
按最终本体论: 生成连续(再生产持续进行->tau连续), 离散是读数(k)与自守筛选产出(gamma_n).
放弃 v1 的"有限离散树直接对应gamma_n"朴素路线.

v2 做结构验证(非完备推导, 对接 v3 开放问题A):
  1. 有限(较大) Bruhat-Tits 树的 Vladimirov 谱 = 连续谱 [p^alpha,inf) 的离散采样
  2. 施加自守型边界约束(根-叶周期/对称筛选) 模拟定理5.1, 筛选"允许"本征模
  3. 对比筛选后离散模的统计分布 与 黎曼零点分布 (累积计数 N(T), 相邻间距)
  4. 输出分布对比图 (本地 png, 非 sandbox)

注意: alpha_p 与 自守约束形式为待严格化参数; 本脚本做结构探索.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpmath as mp

def riemann_zeros(n=50):
    mp.mp.dps = 50
    return np.array([float(mp.zetazero(k+1).imag) for k in range(n)])

def bruhat_tits_adjacency(p, depth):
    n_nodes = (p**(depth+1) - 1) // (p - 1)
    rows, cols = [], []
    def node_at(level, idx):
        return (p**level - 1)//(p-1) + idx
    for level in range(depth):
        for idx in range(p**level):
            parent = node_at(level, idx)
            for c in range(p):
                child = node_at(level+1, idx*p + c)
                rows += [parent, child]; cols += [child, parent]
    A = np.zeros((n_nodes, n_nodes))
    for r, c in zip(rows, cols):
        A[r, c] = 1.0
    return A

def vladimirov_spectrum(p, depth, alpha):
    """Vladimirov 特征值近似: lambda_V = p^alpha - p^(alpha-1)*mu, mu=归一化邻接谱"""
    A = bruhat_tits_adjacency(p, depth)
    mu = np.linalg.eigvalsh(A / p)
    lambda_V = p**alpha - p**(alpha-1) * mu
    return np.sort(lambda_V)  # 连续谱 [p^alpha, ~p^alpha+p^(alpha-1)*2sqrt(p)] 的离散采样

def automorphic_filter(eigs, p, keep_frac=0.15):
    """
    模拟定理5.1自守约束: 仅保留"对称/低动量"模(类 Psi(qx)=Psi(x) 的周期筛选).
    这里用启发式: 保留谱低端(近 p^alpha 本底)的 keep_frac 部分作为"被允许的临界线模式".
    注: 这是数值近似, 非定理5.1的严格实现(严格实现是开放问题A).
    """
    n_keep = max(1, int(len(eigs)*keep_frac))
    return eigs[:n_keep]

def cumulative_count(values, xs):
    """N(x) = #{v <= x}"""
    return np.array([np.sum(values <= x) for x in xs])

def main():
    mp.mp.dps = 50
    gammas = riemann_zeros(50)
    print("=== 黎曼零点 gamma_n (前10) ===")
    print(np.round(gammas[:10], 4))
    # 黎曼零点累积计数 (von Mangoldt 近似 N(T)~T/(2pi) ln(T/2pi e))
    T_grid = np.linspace(10, 125, 200)
    N_gamma = cumulative_count(gammas, T_grid)
    N_rf = T_grid/(2*np.pi) * np.log(T_grid/(2*np.pi*np.e))

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(T_grid, N_gamma, 'k-', lw=2, label='actual zeros N(T)')
    plt.plot(T_grid, N_rf, 'r--', label='von Mangoldt ~T/2pi ln(T/2pi e)')
    plt.xlabel('T'); plt.ylabel('N(T)'); plt.title('Riemann zeros cumulative')
    plt.legend(); plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    colors = {2: 'b', 3: 'g', 5: 'm'}
    for (p, alpha) in [(2, 2.0), (3, 1.5), (5, 1.0)]:
        eigs = vladimirov_spectrum(p, depth=5, alpha=alpha)
        filt = automorphic_filter(eigs, p, keep_frac=0.12)
        # 把筛选模映射到 [0,125] 量级做分布对比 (仅形态, 非数值等号)
        xs = np.linspace(filt.min(), filt.max(), 200)
        N_f = cumulative_count(filt, xs)
        plt.plot(xs, N_f, color=colors[p], label=f'p={p} filtered (mapped)')
    plt.xlabel('mapped eigenvalue'); plt.ylabel('N')
    plt.title('p-adic filtered spectrum cumulative (shape compare)')
    plt.legend(); plt.grid(alpha=0.3)
    plt.tight_layout()
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'padic_v2_spectrum_compare.png')
    plt.savefig(out, dpi=120)
    print(f"图已存: {out}")

    # 相邻间距统计 (离散残差结构)
    print("\n=== 筛选后离散模相邻间距 (p=2, alpha=2) ===")
    eigs = vladimirov_spectrum(2, depth=5, alpha=2.0)
    filt = np.diff(automorphic_filter(eigs, 2, 0.12))
    print("p=2 间距:", np.round(filt[:10], 4))
    print("gamma 间距:", np.round(np.diff(gammas[:10]), 4))
    print("\n观察: p进筛选模有零间距(简并), gamma_n 近无简并 -> 朴素等号不成立,")
    print("但累积计数形态(幂律增长)可对比 -> 需自守约束更严格实现(开放问题A)")

if __name__ == "__main__":
    main()
