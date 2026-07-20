"""
CNT p进动力学研究 - 第一版
=======================
作者: Hermes (按用户猜测展开)
日期: 2026-07-20
对接: v3 定理3.4 (p进RG/离散再生产周期), 定理4.1/4.3 (xi函数谱),
      公理9.1/定理9.2 (代数能动张量), 候选链第3份 p进薛定谔

核心猜测 (用户):
  固有时 tau 量子化为离散再生产计数 n
  -> p进赋值 k (定理3.4: k->k-1 当 Delta tau = ln(p)/C)
  -> p进薛定谔 D_p^alpha psi + V_p psi = E psi 的谱应与黎曼零点 gamma_n 对应

本脚本验证: Bruhat-Tits 树上 Vladimirov 导数的谱结构, 对比黎曼零点密度。

注意: alpha_p 与 V_p 为待严格化参数 (候选链给 alpha_2=2,alpha_3=3/2,alpha_5=1),
       本脚本先数值探索, 不宣称已证明对应。
"""

import numpy as np
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import eigs
from sympy import nfloat, zeta, polylog, N
import mpmath as mp

# ---------- 0. 黎曼零点 (v3 定理4.1 的 gamma_n) ----------
def riemann_zeros(n=20):
    """前 n 个黎曼零点虚部 gamma_n (v3 用 RH)"""
    mp.mp.dps = 50
    return [float(mp.zetazero(k+1).imag) for k in range(n)]

# ---------- 1. Bruhat-Tits 树 (p进齐次树) ----------
def bruhat_tits_adjacency(p, depth):
    """
    构建 p进齐次树 (Bruhat-Tits) 的邻接矩阵。
    root=0, 每个非叶节点有 p 个子节点。
    depth: 树深 (节点数 = (p^(depth+1)-1)/(p-1))
    """
    n_nodes = (p**(depth+1) - 1) // (p - 1)
    rows, cols = [], []
    def node_at(level, idx):
        return (p**level - 1)//(p-1) + idx
    for level in range(depth):
        nodes_here = p**level
        for idx in range(nodes_here):
            parent = node_at(level, idx)
            for c in range(p):
                child = node_at(level+1, idx*p + c)
                rows += [parent, child]
                cols += [child, parent]
    N = n_nodes
    A = np.zeros((N, N))
    for r, c in zip(rows, cols):
        A[r, c] = 1.0
    return A

# ---------- 2. Vladimirov 导数 (p进拉普拉斯) ----------
def vladimirov_laplacian(p, depth, alpha):
    """
    Vladimirov 导数算子 D_p^alpha 在 Bruhat-Tits 树上的离散实现。
    参考: 树上 Vladimirov = p^alpha * (I - p^{-1} A) 的 alpha 次幂近似,
          或直接用 p进拉普拉斯 L_p = p^{-1} A - I。
    这里用 p进拉普拉斯 L_p = p^{-1} A (邻接) - I，对应 D_p^alpha ~ (-L_p)^{alpha/2} 的谱。
    简化: 取 L_p 的特征值 lambda，Vladimirov 特征值 = p^{alpha} * (1 - p^{-1} lambda) 形式。
    """
    A = bruhat_tits_adjacency(p, depth)
    Lp = A / p - np.eye(A.shape[0])
    # 特征值 (小规模树可全对角化)
    w = np.linalg.eigvalsh(Lp)
    return Lp, w

# ---------- 3. p进薛定谔 本征值 ----------
def padeic_spectrum(p, depth, alpha, V_const=0.0, n_eval=15):
    """
    求解 D_p^alpha psi + V_p psi = E psi 在树上的本征值。
    离散化: H_p = -D_p^alpha + V_const * I  (势能先用常数)
    D_p^alpha 谱用 Vladimirov 特征值近似。
    """
    Lp, w = vladimirov_laplacian(p, depth, alpha)
    # Vladimirov 特征值近似: lambda_V = p^alpha * (-w)^? 
    # 树上标准: D_p^alpha 特征值 = p^{alpha} - p^{alpha-1} * mu, mu 为邻接谱
    # 邻接谱 mu in [-2*sqrt(p), 2*sqrt(p)] (无穷树); 有限树用实际 w*A
    A = bruhat_tits_adjacency(p, depth)
    mu = np.linalg.eigvalsh(A / p)  # 归一化邻接谱
    lambda_V = p**alpha - p**(alpha-1) * mu
    # H_p 本征值 = -lambda_V + V_const (符号约定)
    E = -lambda_V + V_const
    E = np.sort(E)
    return E[:n_eval], mu

# ---------- 4. 密度对比 ----------
def spectral_density_compare():
    """对比 p进谱渐近密度 与 黎曼零点密度"""
    gammas = np.array(riemann_zeros(20))
    print("前10个黎曼零点 gamma_n:")
    print(np.round(gammas[:10], 4))
    print("黎曼零点密度 (相邻差):")
    print(np.round(np.diff(gammas[:10]), 4))

    for p, alpha in [(2, 2.0), (3, 1.5), (5, 1.0)]:
        E, mu = padeic_spectrum(p, depth=4, alpha=alpha, n_eval=20)
        print(f"\np={p}, alpha={alpha}: 前10个p进本征值 E")
        print(np.round(E[:10], 4))
        print(f"p={p}: 本征值间距 (近似谱密度):")
        print(np.round(np.diff(E[:10]), 4))

if __name__ == "__main__":
    mp.mp.dps = 50
    spectral_density_compare()
