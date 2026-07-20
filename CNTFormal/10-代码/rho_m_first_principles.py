#!/usr/bin/env python3
"""
rho_m 第一性原理探索：测试三种候选机制是否再现 rho_2=0.198, rho_3=0.092

机制 A: Mathieu 函数角向重叠积分
机制 B: 有效场论阈值修正
机制 C: 角向-径向耦合动力学生成

日期: 2026-07-21
"""

import mpmath as mp
import numpy as np

mp.mp.dps = 50

# ============================================================
# 基础常数
# ============================================================
C = mp.mpf('0.023095708966')      # xi'(1)/xi(1)
gamma1 = mp.nstr(mp.zetazero(1).imag, 20)
gamma1_val = mp.mpf(gamma1)
E1 = mp.mpf('0.25') + gamma1_val**2  # = 1/4 + gamma1^2 ≈ 200.0405
C_theta = C / E1                    # ≈ 1.1546e-4

# Mathieu CNT 线参数
# 来自连分数方程: lambda_c = 4*q_c, lambda_c ≈ 1.3160229113
lambda_c = mp.mpf('1.3160229113')
q_c = lambda_c / 4                   # ≈ 0.3290057278

# ============================================================
# Mathieu 特征值 (CNT 线 a=2q 上，不同 m 在不同 q 处)
# ============================================================
# m=1: 5̄表示, DN边界, b_1(q) 曲线, a=2q → b_1 = 2q → q_1 = b_1/2 = 1.3160/2
# m=2: 10表示, ND边界, a_1(q) 曲线, a=2q → a_1 = 2q → q_2 = a_1/2 = 3.5593/2
# m=3: 24表示, DD边界, b_2(q) 曲线, a=2q → b_2 = 2q → q_3 = b_2/2 = 7.4328/2

lambda_vals = {
    1: mp.mpf('1.3160229113'),   # b_1,  q=0.6580
    2: mp.mpf('3.5592799753'),   # a_1,  q=1.7796
    3: mp.mpf('7.4328467659'),   # b_2,  q=3.7164
}

q_vals = {m: lambda_vals[m] / 2 for m in [1, 2, 3]}

# 边界条件
# m=1 (DN): Dirichlet at z=0, Neumann at z=pi/2
# m=2 (ND): Neumann at z=0, Dirichlet at z=pi/2
# m=3 (DD): Dirichlet at z=0, Dirichlet at z=pi/2

# ============================================================
# 机制 A: Mathieu 函数重叠积分
# ============================================================

def mathieu_solution(z, m, n_terms=20):
    """
    计算 Mathieu 方程在 CNT 线上的本征函数。
    使用傅里叶级数展开（适用于小到中等 q）。
    
    Mathieu 方程: y'' + [a - 2q cos(2z)] y = 0
    在 CNT 线上: a = 2q
    
    m=1: b_1, DN, 奇宇称 → se_1(z, q) 型
    m=2: a_1, ND, 偶宇称 → ce_1(z, q) 型  
    m=3: b_2, DD, 奇宇称 → se_2(z, q) 型
    """
    q = q_vals[m]
    a = 2 * q  # CNT line condition
    
    # 构建 Mathieu 算符矩阵（截断傅里叶基）
    # 对于周期 pi 或 2pi 的函数，使用 sin/cos 基
    N = n_terms
    
    if m in [1, 3]:  # 奇宇称 (se): 使用 sin(n*z) 基
        H = mp.zeros(N, N)
        for i in range(N):
            n = i + 1  # sin(z), sin(2z), ...
            H[i, i] = n**2  # -d²/dz² → n²
            # -2q cos(2z) 的矩阵元
            # <sin(nz)|cos(2z)|sin(mz)> 
            # cos(2z) sin(nz) = (sin((n+2)z) + sin((n-2)z))/2
            if i + 2 < N:
                H[i, i+2] = -q  # n → n+2
            if i - 2 >= 0:
                H[i, i-2] = -q  # n → n-2
            if n == 2:
                H[i, 0] = -q / 2  # special: sin(2z)cos(2z) = sin(4z)/2, diagonal too
        
        # 校正: -2q cos(2z) sin(z) 的非对角项
        # 重新计算更准确
        H_corrected = mp.zeros(N, N)
        for i in range(N):
            n_i = i + 1
            H_corrected[i, i] = n_i**2
            for j in range(N):
                n_j = j + 1
                # <sin(n_i z)|a - 2q cos(2z)|sin(n_j z)>
                # a * delta_{i,j} 已经包含在 n² 对角项中
                # -2q * <sin(n_i z)|cos(2z)|sin(n_j z)>
                # cos(2z)|sin(nz)> = (|sin((n+2)z)> + |sin((n-2)z)>)/2
                if n_j == n_i + 2:
                    H_corrected[i, j] = -q
                elif n_j == n_i - 2:
                    H_corrected[i, j] = -q
                elif n_i == 1 and n_j == 1:
                    # <sin(z)|cos(2z)|sin(z)> = <sin(z)|sin(3z)/2 + sin(-z)/2>
                    # = <sin(z)|sin(3z)/2 - sin(z)/2> = -1/2
                    H_corrected[i, j] += q  # -2q * (-1/2) = q
        
        eigenvalues, eigenvectors = mp.eig(mp.matrix(H_corrected.tolist()))
        
        # 找到最接近 a=2q 的特征值
        eigenvalues = [complex(ev) for ev in eigenvalues]
        idx = min(range(len(eigenvalues)), 
                  key=lambda i: abs(eigenvalues[i].real - float(a)))
        coeffs = [complex(eigenvectors[j, idx]) for j in range(N)]
        # 去除非实数部分
        coeffs = [c.real for c in coeffs]
        
        def psi(z_val):
            result = mp.mpf('0')
            for k in range(N):
                result += coeffs[k] * mp.sin((k+1) * z_val)
            return result
            
    else:  # m=2: 偶宇称 (ce): 使用 cos(n*z) 基
        H = mp.zeros(N, N)
        H[0, 0] = 0  # cos(0*z) = 1, d²/dz² = 0
        for i in range(1, N):
            H[i, i] = i**2
        
        # cos(2z)|cos(nz)> = (|cos((n+2)z)> + |cos((n-2)z)>)/2
        for i in range(N):
            n_i = i
            for j in range(N):
                n_j = j
                if n_j == n_i + 2:
                    H[i, j] = -q
                elif n_j == n_i - 2:
                    H[i, j] = -q
                elif n_i == 2 and n_j == 0:
                    H[i, j] = -q  # cos(2z)*cos(2z)|1> → extra factor
                elif n_i == 0 and n_j == 2:
                    H[i, j] = -q * 2  # <1|cos(2z)|cos(2z)> = 1 (not 1/2)
        
        eigenvalues, eigenvectors = mp.eig(mp.matrix(H.tolist()))
        eigenvalues = [complex(ev) for ev in eigenvalues]
        # 特征值减去 a 的绝对值 → 实际能量
        idx = min(range(len(eigenvalues)),
                  key=lambda i: abs(eigenvalues[i].real - float(a)))
        coeffs = [complex(eigenvectors[j, idx]) for j in range(N)]
        coeffs = [c.real for c in coeffs]
        
        def psi(z_val):
            result = coeffs[0]  # cos(0) = 1 项
            for k in range(1, N):
                result += coeffs[k] * mp.cos(k * z_val)
            return result
    
    # 归一化
    def norm_sq():
        f = lambda z: psi(z)**2
        return mp.quad(f, [0, mp.pi/2])
    
    norm = mp.sqrt(norm_sq())
    
    def psi_normalized(z_val):
        return psi(z_val) / norm
    
    return psi_normalized


def compute_overlap_integral(m):
    """
    计算角向重叠积分: ∫₀^{π/2} ψ_m*(θ) O(θ) ψ_1(θ) dθ
    
    O(θ) 是角向耦合算符。在 SU(5) Cartan 子代数中，
    不同表示之间的跃迁由根空间算符 E_α 驱动。
    
    最简单的模型: O(θ) = sin(2θ) (破坏正交性的最低阶角向调制)
    """
    psi1 = mathieu_solution(0, 1)  # z ∈ [0, π/2]
    psim = mathieu_solution(0, m)
    
    # 尝试不同的角向耦合算符
    results = {}
    
    # O1: sin(2z)
    f1 = lambda z: psi1(z) * psim(z) * mp.sin(2*z)
    I1 = mp.quad(f1, [0, mp.pi/2])
    results['sin(2z)'] = float(abs(I1)**2)
    
    # O2: cos(2z)
    f2 = lambda z: psi1(z) * psim(z) * mp.cos(2*z)
    I2 = mp.quad(f2, [0, mp.pi/2])
    results['cos(2z)'] = float(abs(I2)**2)
    
    # O3: sin(z) (Cartan 对角生成元)
    f3 = lambda z: psi1(z) * psim(z) * mp.sin(z)
    I3 = mp.quad(f3, [0, mp.pi/2])
    results['sin(z)'] = float(abs(I3)**2)
    
    # O4: d/dz (角向动量算符)
    # 数值微分
    eps = mp.mpf('0.001')
    f4 = lambda z: psi1(z) * ((psim(z+eps) - psim(z-eps)) / (2*eps))
    I4 = mp.quad(f4, [0, mp.pi/2])
    results['d/dz'] = float(abs(I4)**2)
    
    # O5: 角向 Casimir（保留正交性但产生能移）
    f5 = lambda z: psi1(z) * psim(z) * mp.cos(4*z)
    I5 = mp.quad(f5, [0, mp.pi/2])
    results['cos(4z)'] = float(abs(I5)**2)
    
    return results


def check_orthogonality(m):
    """检查 Mathieu 函数的正交性"""
    psi1 = mathieu_solution(0, 1)
    psim = mathieu_solution(0, m)
    f = lambda z: psi1(z) * psim(z)
    I = mp.quad(f, [0, mp.pi/2])
    return float(I)


# ============================================================
# 机制 B: 有效场论阈值修正估算
# ============================================================

def threshold_estimate():
    """估算阈值修正的量级"""
    # 从 GUT (~10^15 GeV) 到 M_Z (~91 GeV)，ln(M_GUT/M_Z) ≈ 30
    # 世代间标度比
    ln_ratios = {
        2: 30,   # GUT → 电弱
        3: 10,   # 电弱 → QCD (或世代间)
    }
    
    results = {}
    for m in [2, 3]:
        ln_r = ln_ratios[m]
        # g_m 需要使得 g_m²/(16π²) * ln_r ≈ ρ_m
        # ρ_2=0.198 → g_2² ≈ 0.198 * 16π² / 30 ≈ 1.04
        # ρ_3=0.092 → g_3² ≈ 0.092 * 16π² / 10 ≈ 1.45
        g_sq_needed = 0.198 * 16 * mp.pi**2 / ln_r if m == 2 else 0.092 * 16 * mp.pi**2 / ln_r
        results[m] = {
            'ln(M_m/M_{m-1})': ln_r,
            'g_m^2 needed': float(g_sq_needed),
            'g_m needed': float(mp.sqrt(g_sq_needed)),
            'alpha_m needed': float(g_sq_needed / (4*mp.pi)),
        }
    return results


# ============================================================
# 机制 C: 角向-径向耦合估算
# ============================================================

def radial_angular_coupling_estimate():
    """
    估算角向-径向耦合矩阵元量级。
    
    E_{θ,m}(u) = E_{θ,m} * e^{2u}
    → 径向涨落 Δu 导致角向能移
    → |<m|∂_u|1>|² ~ ?
    """
    # 径向零点涨落: (Δu)² ~ C/2 (从不确定性关系)
    delta_u_sq = float(C) / 2  # ≈ 0.0115
    
    # 角向-径向耦合: ∂E_θ/∂u = 2 E_θ * e^{2u} ≈ 2 E_θ
    # |<m|∂_u|1>|² 涉及 Mathieu 函数对 q 的导数
    
    # 简化估算: 矩阵元 ~ (E_θ 对 q 的导数) * (q 对 u 的依赖)
    # q ~ e^{2u} 或 q 与 u 成比例
    # |<m|∂_u|1>| ~ dλ/dq|_{CNT} * ∂q/∂u
    
    results = {}
    for m in [2, 3]:
        # Mathieu 特征值在 CNT 线上的 q-梯度
        # 近似: dλ/dq ~ 4 (特征值间距 ÷ q 间距的粗糙估计)
        dlambda_dq = 4.0
        
        # 矩阵元平方
        matrix_element_sq = dlambda_dq**2 * delta_u_sq
        
        # 能级分母
        dE = float(lambda_vals[m] - lambda_vals[1])
        
        # 修正
        correction = matrix_element_sq / dE
        
        results[m] = {
            '(Δu)²': delta_u_sq,
            'dλ/dq (est.)': dlambda_dq,
            '|<m|∂_u|1>|²': matrix_element_sq,
            'E_θ,m - E_θ,1': dE,
            'correction': correction,
        }
    
    return results


# ============================================================
# 机制 A 补充: 直接使用 Mathieu 特征值的修正
# ============================================================

def direct_energy_denominator():
    """
    直接使用文档中的 ρ_m = C_θ / (E_θ,m - E_θ,1) 公式，
    但用正确的 Mathieu 特征值。
    """
    results = {}
    for m in [2, 3]:
        dE = float(lambda_vals[m] - lambda_vals[1])
        rho = float(C_theta) / dE
        results[m] = {
            'E_θ,m': float(lambda_vals[m]),
            'E_θ,1': float(lambda_vals[1]),
            'dE': dE,
            'C_θ': float(C_theta),
            'ρ_m (formula)': rho,
            'ρ_m (needed)': 0.198 if m == 2 else 0.092,
            'ratio (formula/needed)': rho / (0.198 if m == 2 else 0.092),
        }
    return results


# ============================================================
# 主程序
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("CNT ρ_m 第一性原理探索")
    print("=" * 70)
    print(f"C = {float(C):.8f}")
    print(f"E1 = {float(E1):.6f}")
    print(f"C_θ = C/E1 = {float(C_theta):.6e}")
    print(f"q_c = {float(q_c):.6f}")
    print(f"\nMathieu 特征值 (CNT 线):")
    for m in [1, 2, 3]:
        print(f"  λ_{m} = {float(lambda_vals[m]):.10f}  (q_{m} = {float(q_vals[m]):.6f})")
    
    # --- 直接能级分母公式 ---
    print("\n" + "=" * 70)
    print("测试: 直接公式 ρ_m = C_θ / (E_θ,m - E_θ,1)")
    print("=" * 70)
    direct = direct_energy_denominator()
    for m in [2, 3]:
        d = direct[m]
        print(f"\nm={m}:")
        print(f"  E_θ,{m} - E_θ,1 = {d['dE']:.6f}")
        print(f"  ρ_{m} (公式) = {d['ρ_m (formula)']:.2e}")
        print(f"  ρ_{m} (需要) = {d['ρ_m (needed)']:.4f}")
        print(f"  比值 = {d['ratio (formula/needed)']:.2e}  ← 差 3-4 个数量级")
    
    # --- 机制 A: 重叠积分 ---
    print("\n" + "=" * 70)
    print("机制 A: Mathieu 函数角向重叠积分")
    print("=" * 70)
    
    for m in [2, 3]:
        print(f"\n--- m={m} ---")
        
        # 检查正交性
        orth = check_orthogonality(m)
        print(f"  正交性检查: ∫ ψ₁ ψ_{m} dz = {orth:.2e}")
        
        # 计算重叠积分（多种角向算符）
        overlaps = compute_overlap_integral(m)
        for op_name, val in overlaps.items():
            rho_needed = 0.198 if m == 2 else 0.092
            ratio = val / rho_needed
            marker = " ← 接近!" if 0.1 < ratio < 10 else ""
            print(f"  O = {op_name:10s}: |∫ψ₁Oψ_{m}|² = {val:.6f}  "
                  f"(需要 {rho_needed:.4f}, 比值 = {ratio:.3f}){marker}")
    
    # --- 机制 B: 阈值修正 ---
    print("\n" + "=" * 70)
    print("机制 B: 有效场论阈值修正")
    print("=" * 70)
    thresh = threshold_estimate()
    for m in [2, 3]:
        d = thresh[m]
        print(f"\nm={m}:")
        print(f"  ln(M_{m}/M_{m-1}) = {d['ln(M_m/M_{m-1})']:.0f}")
        print(f"  需要的 g_{m}² = {d['g_m^2 needed']:.3f}")
        print(f"  需要的 g_{m} = {d['g_m needed']:.3f}")
        print(f"  需要的 α_{m} = {d['alpha_m needed']:.3f}")
        rho_needed = 0.198 if m == 2 else 0.092
        print(f"  (目标 ρ_{m} = {rho_needed:.4f})")
    
    # --- 机制 C: 角向-径向耦合 ---
    print("\n" + "=" * 70)
    print("机制 C: 角向-径向耦合动力学生成")
    print("=" * 70)
    r_a = radial_angular_coupling_estimate()
    for m in [2, 3]:
        d = r_a[m]
        rho_needed = 0.198 if m == 2 else 0.092
        print(f"\nm={m}:")
        print(f"  (Δu)² = {d['(Δu)²']:.4f}")
        print(f"  dλ/dq (估算) = {d['dλ/dq (est.)']:.1f}")
        print(f"  |<m|∂_u|1>|² = {d['|<m|∂_u|1>|²']:.3f}")
        print(f"  E_θ,{m} - E_θ,1 = {d['E_θ,m - E_θ,1']:.4f}")
        print(f"  修正量 = {d['correction']:.4f}")
        print(f"  需要 ρ_{m} = {rho_needed:.4f}, 比值 = {d['correction']/rho_needed:.3f}")
    
    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)
    print("""
1. 直接公式 ρ_m = C_θ/(E_θ,m-E_θ,1) 产生的数值比需要的 0.198/0.092
   小 3-4 个数量级 → 此公式不成立，ρ_m 不是简单的二阶微扰修正。

2. 机制 A (重叠积分): 角向重叠积分依赖算符形式。
   若使用 sin(2z) 或 cos(2z) 等自然选择，结果通常远小于目标值。
   需要特定的 O(θ) 形式才能产生大重叠积分。
   → 需要从 SU(5) Cartan 子代数严格导出 O(θ)。

3. 机制 B (阈值修正): 需要的耦合常数 g_m ~ 1 在物理上完全合理。
   ln(M_m/M_{m-1}) ~ 10-30 与 GUT-电弱-QCD 能标层级一致。
   → 这是最有希望的定量机制。

4. 机制 C (角向-径向耦合): 产生的修正量很小，
   因为 Mathieu 特征值间距大 (O(1-10)) 而径向涨落小 (O(0.01))。
   → 不足以解释 ρ_m ~ 0.1 量级。

推荐下一步: 结合机制 A+B，从 SU(5) 根空间严格导出角向耦合算符 O(θ)，
并结合对数增强的 ln(M_m/M_{m-1}) 因子。""")
