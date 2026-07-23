#!/usr/bin/env python3
"""
ρ_m 对 q 参数的敏感度扫描

核心问题: 当前使用的 q_m = λ_m/2 产生的 Mathieu 特征值与 CNT 目标 λ_m 不一致。
需要确定:
1. ρ₂, ρ₃ 对 q_m 的敏感度
2. 存在哪些 q 值使 ρ_m 匹配目标值
3. 这些 q 值是否有物理解释

日期: 2026-07-21
"""

import mpmath as mp
import numpy as np

mp.mp.dps = 60

# ============================================================
# 基础常数
# ============================================================
C = mp.mpf('0.023095708966')
gamma1_val = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + gamma1_val**2
C_theta = C / E1

lambda_c = mp.mpf('1.3160229113')

# CNT 目标 ρ 值
rho_target = {2: 0.198, 3: 0.092}

# ============================================================
# Mathieu 本征函数 (单个 q，固定 n_terms)
# ============================================================

def mathieu_eigenfunction_single(q, m, n_terms=60):
    """返回单个 q 值的 Mathieu 本征函数（最低本征态）"""
    N = n_terms

    if m == 1:
        H = mp.matrix(N, N)
        H[0, 0] = mp.mpf('1') + q
        H[0, 1] = -q
        for k in range(1, N):
            nk = 2*k + 1
            H[k, k] = mp.mpf(nk)**2
            if k + 1 < N:
                H[k, k+1] = -q
            if k - 1 >= 0:
                H[k, k-1] = -q
    elif m == 2:
        H = mp.matrix(N, N)
        H[0, 0] = mp.mpf('1') - q
        H[0, 1] = -q
        for k in range(1, N):
            nk = 2*k + 1
            H[k, k] = mp.mpf(nk)**2
            if k + 1 < N:
                H[k, k+1] = -q
            if k - 1 >= 0:
                H[k, k-1] = -q
    else:
        H = mp.matrix(N, N)
        for k in range(N):
            nk = 2 * (k + 1)
            H[k, k] = mp.mpf(nk)**2
            if k + 1 < N:
                H[k, k+1] = -q
            if k - 1 >= 0:
                H[k, k-1] = -q

    E, V = mp.eig(H)
    eigenvalues = sorted([complex(ev).real for ev in E])
    lowest_idx = eigenvalues.index(min(eigenvalues))

    coeffs_raw = [complex(V[j, lowest_idx]) for j in range(N)]
    coeffs = [c.real for c in coeffs_raw]

    actual_eval = eigenvalues[lowest_idx]

    if m == 1:
        def psi_raw(z_val):
            result = mp.mpf('0')
            zf = mp.mpf(z_val)
            for k in range(N):
                result += coeffs[k] * mp.sin((2*k+1) * zf)
            return result
    elif m == 2:
        def psi_raw(z_val):
            result = mp.mpf('0')
            zf = mp.mpf(z_val)
            for k in range(N):
                result += coeffs[k] * mp.cos((2*k+1) * zf)
            return result
    else:
        def psi_raw(z_val):
            result = mp.mpf('0')
            zf = mp.mpf(z_val)
            for k in range(N):
                result += coeffs[k] * mp.sin(2*(k+1) * zf)
            return result

    # 归一化
    f_norm = lambda z: psi_raw(z)**2
    norm_sq = mp.quad(f_norm, [0, mp.pi/2])
    norm = mp.sqrt(norm_sq)

    def psi(z_val):
        return psi_raw(z_val) / norm

    return psi, actual_eval


# ============================================================
# ρ_m 计算（给定 q₁, q_m, O_m）
# ============================================================

def compute_rho(q1_val, qm_val, m, O_func):
    """计算 ρ_m = |∫ ψ₁(q₁) O ψ_m(q_m) dθ|²"""
    psi1, eval1 = mathieu_eigenfunction_single(q1_val, 1)
    psim, evalm = mathieu_eigenfunction_single(qm_val, m)

    f_int = lambda z: psi1(z) * psim(z) * O_func(z)
    I = mp.quad(f_int, [0, mp.pi/2])
    return float(abs(I)**2), float(eval1), float(evalm)


# ============================================================
# q 扫描: 固定 q₁, 扫描 q_m
# ============================================================

def scan_qm(q1_val, m, O_func, O_name, q_range, n_points=30):
    """扫描 q_m 找到使 ρ_m 匹配目标的值"""
    print(f"\n--- m={m}, O={O_name} ---")
    print(f"  固定 q₁ = {float(q1_val):.6f}, 目标 ρ_{m} = {rho_target[m]:.4f}")
    print(f"  {'q_m':>10s}  {'λ_{m}':>10s}  {'ρ_m':>10s}  {'ratio':>8s}")
    print(f"  {'-'*45}")

    q_vals_scan = np.linspace(q_range[0], q_range[1], n_points)
    results = []

    for qm in q_vals_scan:
        qm_mp = mp.mpf(str(qm))
        rho, eval1, evalm = compute_rho(q1_val, qm_mp, m, O_func)
        ratio = rho / rho_target[m]
        results.append((qm, evalm, rho, ratio))

        marker = ""
        if 0.9 < ratio < 1.1:
            marker = " ← "
        elif 0.8 < ratio < 1.25:
            marker = " ~ "
        print(f"  {qm:10.4f}  {evalm:10.4f}  {rho:10.6f}  {ratio:8.3f}{marker}")

    # 找到最佳匹配
    best = min(results, key=lambda x: abs(x[2] - rho_target[m]))
    print(f"\n  最佳匹配: q_{m} = {best[0]:.6f}, λ_{m} = {best[1]:.4f}, ρ_{m} = {best[2]:.6f} (×{best[3]:.3f})")

    return best


def scan_both_q(q1_range, qm_range, m, O_func, O_name, n_q1=10, n_qm=20):
    """同时扫描 q₁ 和 q_m"""
    print(f"\n--- 二维扫描 m={m}, O={O_name} ---")

    q1_vals = np.linspace(q1_range[0], q1_range[1], n_q1)
    qm_vals = np.linspace(qm_range[0], qm_range[1], n_qm)

    best_dev = float('inf')
    best_pair = None

    print(f"  扫描 {n_q1}×{n_qm} = {n_q1*n_qm} 个点...")

    for q1 in q1_vals:
        for qm in qm_vals:
            q1_mp = mp.mpf(str(q1))
            qm_mp = mp.mpf(str(qm))
            rho, _, _ = compute_rho(q1_mp, qm_mp, m, O_func)
            dev = abs(rho - rho_target[m])
            if dev < best_dev:
                best_dev = dev
                best_pair = (q1, qm, rho)

    q1_best, qm_best, rho_best = best_pair
    print(f"  最佳: q₁ = {q1_best:.6f}, q_{m} = {qm_best:.4f}, ρ_{m} = {rho_best:.6f} (×{rho_best/rho_target[m]:.3f})")
    print(f"  偏差: {abs(rho_best - rho_target[m]):.6f}")

    return best_pair


# ============================================================
# 主程序
# ============================================================

if __name__ == '__main__':
    print("=" * 75)
    print("ρ_m 对 q 参数的敏感度分析")
    print("=" * 75)

    q1_current = mp.mpf('0.658011')

    # --- m=2: sin(2θ), 窄范围精扫 ---
    print("\n" + "=" * 75)
    print("§1: m=2, sin(2θ) — q₂ 对 ρ₂ 的敏感度")
    print("=" * 75)

    O2 = lambda z: mp.sin(2 * mp.mpf(z))
    scan_qm(q1_current, 2, O2, 'sin(2θ)', [0.3, 3.0], n_points=30)

    # --- m=3: cos(4θ), 扫描 ---
    print("\n" + "=" * 75)
    print("§2: m=3, cos(4θ) — q₃ 对 ρ₃ 的敏感度")
    print("=" * 75)

    O3 = lambda z: mp.cos(4 * mp.mpf(z))
    scan_qm(q1_current, 3, O3, 'cos(4θ)', [0.5, 6.0], n_points=30)

    # --- 二维扫描: m=3 ---
    print("\n" + "=" * 75)
    print("§3: m=3, cos(4θ) — 同时扫描 q₁ 和 q₃")
    print("=" * 75)

    scan_both_q([0.3, 1.5], [0.5, 6.0], 3, O3, 'cos(4θ)', n_q1=12, n_qm=20)

    # --- 自洽性检查 ---
    print("\n" + "=" * 75)
    print("§4: 自洽性诊断")
    print("=" * 75)

    # 检查 CNT 线交叉条件: λ_m = 2q_m 是否在某个 q 成立
    print("\n检查 Mathieu 特征值是否满足 CNT 线条件 λ = 2q:")
    for m, label in [(1, 'DN'), (2, 'ND'), (3, 'DD')]:
        for q_test in [0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0]:
            q_mp = mp.mpf(str(q_test))
            _, eval_val = mathieu_eigenfunction_single(q_mp, m, n_terms=60)
            ratio_val = float(eval_val) / q_test if q_test > 0 else float('inf')
            marker = " ← CNT线" if abs(ratio_val - 2.0) < 0.3 else ""
            if abs(ratio_val - 2.0) < 0.5:
                print(f"  m={m} ({label}): q={q_test:.3f}, λ={float(eval_val):.4f}, λ/q={ratio_val:.3f}{marker}")

    print("\n" + "=" * 75)
    print("结论")
    print("=" * 75)
