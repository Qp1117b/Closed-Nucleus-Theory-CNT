# -*- coding: utf-8 -*-
"""
T1 数值验证：闭环相容子空间一维性猜想（文档13 §8.1）
=====================================================

验证目标（对应 13 号文档目标定理 T1 与三条证明路线）：
  Part 1  T1(i) 计数检验：在 Δ3×Δ3 上，双线性耦合复制子流的内部不动点
          ——线性代数保证至多一个（非奇异时）；统计其存在（正性）率与
          稳定性分类（路线 A 的双曲性/指标预言）。
  Part 2  动力学行为：对代表性耦合积分 ODE，分类渐近行为
          （收敛到内部不动点 / 振荡 / 趋近边界），与 Jacobian 特征值对照。
  Part 3  C统计 浓度检验：双种群 Moran 过程，测量经验频率围绕联合
          不动点的平稳方差随种群 N 的标度（预言 Var ∝ 1/N，K2）。
  Part 4  共振集扫描：det M(Λ) 沿随机直线的零点分布——验证奇异集
          （一维性退化集）为零测代数超曲面（§6 genericity）。

数学设定（13 号文档 D4）：
  ẋ_i = x_i[(A x)_i + (Λ y)_i - φ_x],  φ_x = x^T(A x + Λ y) = x^T Λ y
  ẏ_j = y_j[(B y)_j + (Λᵀ x)_j - φ_y], φ_y = y^T Λᵀ x = x^T Λ y
  A, B 反对称非传递；内部不动点满足线性方程组 M[x;y] = b。
"""
import json
import time
from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260717)

# ---- CNT 系统扇区博弈矩阵（元RG文档 §3.1）--------------------------------
a0, b0, c0 = np.log(3 / 2), np.log(5 / 3), np.log(5 / 2)
A_SYS = np.array([[0.0, a0, -c0],
                  [-a0, 0.0, b0],
                  [c0, -b0, 0.0]])


def antisym(u, v, w):
    """3x3 反对称矩阵；u,v,w>0 时非传递，核向量 (v,w,u)>0（K1）。"""
    return np.array([[0.0, u, -w],
                     [-u, 0.0, v],
                     [w, -v, 0.0]])


def build_M(A, B, L):
    """内部不动点线性方程的系数矩阵 M（6x6）。"""
    M = np.zeros((6, 6))
    M[0, :3] = A[0] - A[2]; M[0, 3:] = L[0] - L[2]
    M[1, :3] = A[1] - A[2]; M[1, 3:] = L[1] - L[2]
    M[2, :3] = 1.0
    M[3, :3] = L.T[0] - L.T[2]; M[3, 3:] = B[0] - B[2]
    M[4, :3] = L.T[1] - L.T[2]; M[4, 3:] = B[1] - B[2]
    M[5, 3:] = 1.0
    return M


def interior_equilibrium(A, B, L, det_tol=1e-12):
    """解内部不动点线性方程 M[x;y]=b。返回 (x, y, detM)；奇异返回 (None,None,detM)。"""
    M = build_M(A, B, L)
    detM = float(np.linalg.det(M))
    if abs(detM) < det_tol:
        return None, None, detM
    rhs = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 1.0])
    z = np.linalg.solve(M, rhs)
    return z[:3], z[3:], detM


TAN_BASIS = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]])  # Δ3 切空间基
T6 = np.zeros((6, 4))
T6[:3, :2] = TAN_BASIS
T6[3:, 2:] = TAN_BASIS
T6_PINV = np.linalg.pinv(T6)


def tangent_jacobian_eigs(A, B, L, x, y):
    """内部不动点处，复制子向量场限制在 Δ3×Δ3 切空间（4 维）的 Jacobian 特征值。"""
    J = np.zeros((6, 6))
    Lx = L.T @ x
    Ly = L @ y
    for i in range(3):
        for k in range(3):
            J[i, k] = x[i] * (A[i, k] - Ly[k])          # ∂F_i/∂x_k
            J[3 + i, 3 + k] = y[i] * (B[i, k] - Lx[k])  # ∂G_i/∂y_k
        for l in range(3):
            J[i, 3 + l] = x[i] * (L[i, l] - Lx[l])      # ∂F_i/∂y_l
            J[3 + i, l] = y[i] * (L.T[i, l] - Ly[l])    # ∂G_i/∂x_l
    return np.linalg.eigvals(T6_PINV @ J @ T6)


def classify_stability(eigs, tol=1e-7):
    mr = float(np.max(eigs.real))
    if mr < -tol:
        return "stable"
    if mr > tol:
        return "unstable"
    return "marginal"


# ==========================================================================
# Part 1: T1(i) 计数检验（10^5 组随机耦合 × 6 个耦合强度）
# ==========================================================================
def part1(n_samples=100_000, n_stab=2_000, sigmas=(0.05, 0.1, 0.2, 0.5, 1.0, 2.0)):
    rows = []
    # 基线 sanity：Λ=0 应还原 K1（x*, y* 皆内部）
    B0 = antisym(0.7, 1.1, 0.9)
    x, y, _ = interior_equilibrium(A_SYS, B0, np.zeros((3, 3)))
    base_ok = (x is not None) and np.all(x > 0) and np.all(y > 0)
    xstar = x / x.sum()
    for sigma in sigmas:
        n_int = n_sing = 0
        stab = {"stable": 0, "unstable": 0, "marginal": 0}
        det_abs = []
        n_stab_done = 0
        for _ in range(n_samples):
            u, v, w = np.exp(RNG.normal(0.0, 0.5, 3))      # 随机非传递设备矩阵
            B = antisym(u, v, w)
            L = RNG.normal(0.0, sigma, (3, 3))
            x, y, detM = interior_equilibrium(A_SYS, B, L)
            det_abs.append(abs(detM))
            if x is None:
                n_sing += 1
                continue
            if np.all(x > 1e-9) and np.all(y > 1e-9):
                n_int += 1
                if n_stab_done < n_stab:
                    cls = classify_stability(tangent_jacobian_eigs(A_SYS, B, L, x, y))
                    stab[cls] += 1
                    n_stab_done += 1
        rows.append({
            "sigma": sigma,
            "samples": n_samples,
            "singular": n_sing,
            "interior_frac": n_int / n_samples,
            "stab_subsample": n_stab_done,
            "stable_frac": stab["stable"] / max(n_stab_done, 1),
            "unstable_frac": stab["unstable"] / max(n_stab_done, 1),
            "marginal_frac": stab["marginal"] / max(n_stab_done, 1),
            "min_abs_det": float(np.min(det_abs)),
            "median_abs_det": float(np.median(det_abs)),
        })
    return base_ok, xstar, rows


# ==========================================================================
# Part 2: 代表性耦合的 ODE 渐近行为
# ==========================================================================
def vector_field(A, B, L):
    def f(t, z):
        x, y = z[:3], z[3:]
        fx = A @ x + L @ y
        fy = B @ y + L.T @ x
        dx = x * (fx - x @ fx)
        dy = y * (fy - y @ fy)
        return np.concatenate([dx, dy])
    return f


def rk4_integrate(vf, z0, t_max, dt=0.05, sample_tail=0.2):
    """固定步长 RK4；返回 (z_end, tail_samples)。"""
    n_steps = int(t_max / dt)
    tail_start = n_steps - int(n_steps * sample_tail)
    z = z0.copy()
    tail = []
    for k in range(n_steps):
        k1 = vf(0, z)
        k2 = vf(0, z + 0.5 * dt * k1)
        k3 = vf(0, z + 0.5 * dt * k2)
        k4 = vf(0, z + dt * k3)
        z = z + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        z = np.maximum(z, 0.0)  # 数值保护（复制子流保持单纯形，仅防浮点漂移）
        z[:3] /= z[:3].sum()
        z[3:] /= z[3:].sum()
        if k >= tail_start and k % 20 == 0:
            tail.append(z.copy())
    return z, np.array(tail)


def part2(sigma=0.5, n_traj=24, t_max=200.0):
    results = {"converged": 0, "boundary": 0, "oscillating": 0}
    example = None
    attempts = 0
    while example is None and attempts < 200:   # 取第一个内部不动点（不限稳定性类别）
        attempts += 1
        u, v, w = np.exp(RNG.normal(0.0, 0.5, 3))
        B = antisym(u, v, w)
        L = RNG.normal(0.0, sigma, (3, 3))
        x, y, _ = interior_equilibrium(A_SYS, B, L)
        if x is None or not (np.all(x > 1e-9) and np.all(y > 1e-9)):
            continue
        eigs = tangent_jacobian_eigs(A_SYS, B, L, x, y)
        cls = classify_stability(eigs)
        if cls != "marginal":   # 选中心型（CNT 闭环条件一：不动点须为中心）
            continue
        vf = vector_field(A_SYS, B, L)
        fp = np.concatenate([x, y])
        for _ in range(n_traj):
            z0 = np.concatenate([RNG.dirichlet(np.ones(3)), RNG.dirichlet(np.ones(3))])
            zend, tail = rk4_integrate(vf, z0, t_max)
            if np.min(zend) < 1e-3:
                results["boundary"] += 1
            elif np.linalg.norm(zend - fp) < 1e-4:
                results["converged"] += 1
            else:
                results["oscillating" if tail.std(axis=0).max() > 1e-3 else "converged"] += 1
        example = {"B_uvw": [float(u), float(v), float(w)],
                   "stability_class": cls,
                   "fp_x": x.tolist(), "fp_y": y.tolist(),
                   "eigs": [[float(e.real), float(e.imag)] for e in eigs]}
    return results, example


# ==========================================================================
# Part 3: 浓度检验（Var ∝ 1/N）——Wright-Fisher 多项抽样
# （与事件级 Moran 共享同一扩散极限，09 文档 §3.3；代际更新使计算可行）
# ==========================================================================
def wf_run_batch(A, B, L, fp_x, fp_y, N, generations, replicates, beta=1.0, burn_frac=0.5):
    """R 个双种群 Wright-Fisher 复制并行；返回烧入后 x̂_1 时间序列（R, T）。"""
    nx = np.tile(np.round(np.array(fp_x) * N).astype(int), (replicates, 1)).astype(np.int64)
    ny = np.tile(np.round(np.array(fp_y) * N).astype(int), (replicates, 1)).astype(np.int64)
    nx[:, 0] += N - nx.sum(axis=1)
    ny[:, 0] += N - ny.sum(axis=1)
    cut = int(generations * burn_frac)
    series = np.empty((replicates, generations - cut))
    for g in range(generations):
        for pop in (0, 1):
            n = nx if pop == 0 else ny
            other = (ny / N) if pop == 0 else (nx / N)
            freq = n / N
            fitv = freq @ A.T + other @ L.T if pop == 0 else freq @ B.T + other @ L
            fitv = np.exp(beta * (fitv - fitv.max(axis=1, keepdims=True)))
            w = n * fitv
            p = w / w.sum(axis=1, keepdims=True)
            for r in range(replicates):
                n[r] = RNG.multinomial(N, p[r])
        if g >= cut:
            series[:, g - cut] = nx[:, 0] / N
    return series


def part3(Ns=(100, 200, 400, 800, 1600), replicates=32, generations=600, sigma=0.3):
    # 固定一个具有内部不动点的代表性耦合（类别不限，记录之）
    while True:
        u, v, w = np.exp(RNG.normal(0.0, 0.5, 3))
        B = antisym(u, v, w)
        L = RNG.normal(0.0, sigma, (3, 3))
        x, y, _ = interior_equilibrium(A_SYS, B, L)
        if x is None or not (np.all(x > 1e-9) and np.all(y > 1e-9)):
            continue
        cls = classify_stability(tangent_jacobian_eigs(A_SYS, B, L, x, y))
        if cls != "marginal":   # 中心型耦合（闭环条件一）
            continue
        break
    rows = []
    for N in Ns:
        s = wf_run_batch(A_SYS, B, L, x, y, N, generations, replicates)
        rows.append({"N": N,
                     "var_x1": float(s.var(axis=1).mean()),
                     "mean_x1": float(s.mean()),
                     "fp_x1": float(x[0])})
    logN = np.log([r["N"] for r in rows])
    logV = np.log([r["var_x1"] for r in rows])
    slope = float(np.polyfit(logN, logV, 1)[0])
    return rows, slope, {"B_uvw": [float(u), float(v), float(w)],
                         "stability_class": cls,
                         "fp_x": x.tolist(), "fp_y": y.tolist()}


# ==========================================================================
# Part 4: 共振集扫描（det M 沿随机直线的零点）
# ==========================================================================
def part4(n_lines=6, n_points=4001, t_range=(-2.0, 2.0)):
    B = antisym(0.7, 1.1, 0.9)
    lines = []
    total_zeros = 0
    ts = np.linspace(*t_range, n_points)
    for _ in range(n_lines):
        L1 = RNG.normal(0.0, 1.0, (3, 3))
        L2 = RNG.normal(0.0, 1.0, (3, 3))
        dets = np.empty(n_points)
        for i, t in enumerate(ts):
            L = t * L1 + (1.0 - t) * L2
            dets[i] = np.linalg.det(build_M(A_SYS, B, L))
        sign_changes = int(np.sum(dets[:-1] * dets[1:] < 0))
        total_zeros += sign_changes
        lines.append({"n_sign_changes": sign_changes,
                      "min_abs_det": float(np.min(np.abs(dets))),
                      "det_profile_sample": [float(v) for v in dets[::200]]})
    return {"lines": lines, "total_isolated_zeros": total_zeros,
            "n_points_per_line": n_points, "t_range": list(t_range)}


# ==========================================================================
def main():
    t0 = time.time()
    print("[Part 1] T1(i) 计数检验 ...", flush=True)
    base_ok, xstar, p1 = part1()
    print(f"  基线 Λ=0 还原 K1: {base_ok}, x* = {np.round(xstar, 4)}", flush=True)
    for r in p1:
        print(f"  σ={r['sigma']:<4} 内部不动点率={r['interior_frac']:.3f} "
              f"奇异={r['singular']} 稳定={r['stable_frac']:.2f} "
              f"不稳={r['unstable_frac']:.2f} 临界={r['marginal_frac']:.2f}", flush=True)

    print("[Part 2] ODE 渐近行为 ...", flush=True)
    p2, p2ex = part2()
    print(f"  轨迹分类: {p2}", flush=True)

    print("[Part 3] Moran 浓度检验 ...", flush=True)
    p3, slope, p3cfg = part3()
    print(f"  Var ~ N^slope, slope = {slope:.3f}（预言 -1）", flush=True)

    print("[Part 4] 共振集扫描 ...", flush=True)
    p4 = part4()
    print(f"  6 条直线共 {p4['total_isolated_zeros']} 个孤立零点", flush=True)

    results = {
        "meta": {"date": "2026-07-17", "doc": "13号文档 §8.1",
                 "A_SYS": "CNT 元RG 矩阵 a=ln(3/2), b=ln(5/3), c=ln(5/2)"},
        "baseline_L0_recovers_K1": base_ok,
        "xstar_K1": xstar.tolist(),
        "part1": p1,
        "part2": p2, "part2_example": p2ex,
        "part3": p3, "part3_slope": slope, "part3_config": p3cfg,
        "part4": p4,
        "runtime_sec": time.time() - t0,
    }
    out = OUT_DIR / "t1_verification_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完成，用时 {time.time() - t0:.1f}s，结果写入 {out.name}", flush=True)
    return results


if __name__ == "__main__":
    main()
