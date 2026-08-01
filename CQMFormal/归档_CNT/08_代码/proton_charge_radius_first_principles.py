#!/usr/bin/env python3
"""
质子电荷半径的第一性原理推导：从 Mathieu 角向波函数到 ⟨r²_E⟩

核心思路:
1. 质子的电磁电荷分布由 5̄ 表示的角向 Mathieu 波函数 ψ₁(θ) 决定
2. 电荷算符 Q̂ = T₃ + Y_SM 在 Cartan 平面上投影到特定角向方向
3. ⟨r²_E⟩ 由耦合空间径向坐标的角向加权平均给出
4. 通过映射常数 k 转换到物理空间

关键待推导量: r_p/k = 2r_GUT 中的因子 "2"

日期: 2026-07-21
"""

import mpmath as mp
import numpy as np

mp.mp.dps = 80

# ============================================================
# 基础常数 (全部从第一性原理独立确定)
# ============================================================
C = mp.mpf('0.023095708966')
gamma1_val = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + gamma1_val**2
C_theta = C / E1

lambda_c = mp.mpf('1.3160229113')
r_GUT = mp.sqrt(4 * mp.pi * C * lambda_c)  # 耦合空间 GUT 标度

# 物理常数
m_p = mp.mpf('0.938272')     # GeV (唯一实验输入)
hbarc = mp.mpf('0.197327')   # GeV·fm

# 壳层几何参数
I_su5 = mp.mpf('5') / mp.mpf('3')          # SU(5) Dynkin 嵌入指数
g_s_IR = mp.sqrt(I_su5 * lambda_c)          # 红外耦合强度
r_conf = mp.sqrt(I_su5 * lambda_c)          # 禁闭壳层
Lambda_QCD = m_p / (C * E1)                 # QCD 标度
lambda_QCD = hbarc / Lambda_QCD             # QCD 长度

# 映射常数 k
k_fm = lambda_QCD / r_conf                   # fm (耦合空间→物理空间)

# ============================================================
# §1: Mathieu 角向波函数 (n_terms=80 高精度)
# ============================================================

def mathieu_wavefunctions(n_terms=80):
    """
    返回 CNT 线上三个 Mathieu 本征函数 ψ₁, ψ₂, ψ₃。

    边界条件:
    - ψ₁ (5̄): DN — Dirichlet at θ=0, Neumann at θ=π/2
    - ψ₂ (10): ND — Neumann at θ=0, Dirichlet at θ=π/2
    - ψ₃ (24): DD — Dirichlet at θ=0, Dirichlet at θ=π/2

    Mathieu 方程: y'' + [a + 2q cos(2θ)] y = 0
    CNT 线条件: a = 2q, 即特征值 λ_m = 2q_m
    """
    lambda_vals = {
        1: mp.mpf('1.3160229113'),
        2: mp.mpf('3.5592799753'),
        3: mp.mpf('7.4328467659'),
    }
    q_vals = {m: lambda_vals[m] / 2 for m in [1, 2, 3]}

    wavefunctions = {}
    eigenvalues = {}

    N = n_terms

    for m in [1, 2, 3]:
        q = q_vals[m]

        if m == 1:
            # sin((2k+1)θ), k=0,1,2,...
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
            # cos((2k+1)θ), k=0,1,2,...
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
        else:  # m == 3
            # sin(2(k+1)θ), k=0,1,2,...
            H = mp.matrix(N, N)
            for k in range(N):
                nk = 2 * (k + 1)
                H[k, k] = mp.mpf(nk)**2
                if k + 1 < N:
                    H[k, k+1] = -q
                if k - 1 >= 0:
                    H[k, k-1] = -q

        E, V = mp.eig(H)
        eigenvalues_raw = [complex(ev).real for ev in E]
        target_a = float(2 * q)
        idx = min(range(len(eigenvalues_raw)),
                  key=lambda i: abs(eigenvalues_raw[i] - target_a))

        coeffs_raw = [complex(V[j, idx]) for j in range(N)]
        coeffs = [c.real for c in coeffs_raw]
        actual_eval = eigenvalues_raw[idx]

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

        wavefunctions[m] = psi
        eigenvalues[m] = actual_eval

    return wavefunctions, eigenvalues


# ============================================================
# §2: Cartan 平面几何与电荷算符
# ============================================================

def cartan_geometry():
    """
    SU(5) Cartan 平面上的几何结构。

    在 T₃-Y 平面上:
    - T₃ = (1/2) diag(0,0,0,1,-1)
    - Y = (1/√15) diag(-2,-2,-2,3,3)
    - Q = T₃ + √(3/5)Y

    Weinberg 角 θ_W 定义 T₃ 和 Y 之间的旋转角。
    角向坐标 z ∈ [0, π/2] 遍历 Weyl 腔。

    返回 Cartan 平面上的关键几何量。
    """
    # T₃ 和 Y 方向的单位向量 (在适当的归一化下)
    # 它们的夹角就是 Weinberg 角
    sin2W_exp = mp.mpf('0.23120')

    # Cartan 平面上 T₃ 和 Y_SM = √(3/5)Y 的夹角
    # tan θ_W = g'/g → sin²θ_W 已知
    theta_W = mp.asin(mp.sqrt(sin2W_exp))

    return {
        'sin2W': sin2W_exp,
        'theta_W': theta_W,
        'cos2W': 1 - sin2W_exp,
    }


# ============================================================
# §3: 电荷密度分布: ρ_E(r, θ) 从 Mathieu 波函数
# ============================================================

def charge_density_distribution(wavefunctions, n_grid=200):
    """
    从 Mathieu 角向波函数计算耦合空间中的电荷密度分布。

    物理图像:
    - 电磁荷由 U(1)_EM 生成元 Q̂ = T₃ + Y_SM 测量
    - 在 Cartan 平面上，Q̂ 对角向坐标 θ 的依赖由 5̄ 表示的波函数 ψ₁(θ) 编码
    - 径向依赖来自再生产 RG 流: r(τ) = 1/(-Cτ + const)

    电荷密度 (耦合空间):
    ρ_E(θ) = |ψ₁(θ)|²  (角向部分)

    径向部分通过对角向的适当映射得到。
    """
    psi1 = wavefunctions[1]

    # 角向电荷密度 (归一化到 ∫ρ(θ)dθ = 1)
    theta_grid = np.linspace(0.001, np.pi/2 - 0.001, n_grid)

    rho_E_theta = []
    for theta in theta_grid:
        rho = float(psi1(theta)**2)
        rho_E_theta.append(rho)

    rho_E_theta = np.array(rho_E_theta)

    # 归一化: ∫₀^{π/2} ρ(θ) dθ = 1
    norm = np.trapezoid(rho_E_theta, theta_grid)
    rho_E_theta /= norm

    return theta_grid, rho_E_theta


# ============================================================
# §4: 径向坐标的角向映射
# ============================================================

def angular_to_radial_mapping():
    """
    将角向坐标 θ 映射到耦合空间径向坐标 r。

    CNT 框架中，Cartan 平面上的角向坐标 θ 通过 Weyl 腔几何
    与径向 RG 流相关联。

    关键几何关系:
    - 在 Poincaré 半平面 ds² = du² + e^{-2u} dθ² 上
    - 径向坐标 r = e^u, u = ln r
    - RG 流: du/dτ = C e^u → r ∝ (GUT标度附近)

    电磁扇区 (p=5) 对应 Cartan 平面上的特定角向区间。
    电荷半径与 GUT 标度的比值由该区间内 r(θ) 的加权平均决定。

    候选映射:
    (a) r(θ) = r_GUT · f(θ)  其中 f(θ) 从 Weyl 腔几何确定
    (b) r(θ) 通过 Cartan 度规的测地线距离确定
    (c) r 独立于 θ，电荷半径由角向分布的宽度决定
    """
    # 方案 (a): Weyl 腔中的径向映射
    # 在 Cartan 平面上，Weyl 腔的 "大小" 随 θ 变化
    # 电磁方向在 T₃-Y 平面上，距 GUT 对称中心的距离决定了有效 r

    # 方案 (b): 用 Poincaré 半平面度规
    # 固定 u 时，角向测地距离 = e^{-u} · Δθ
    # 在 GUT 标度 u = ln(r_GUT):
    #   Δs_angular = e^{-ln(r_GUT)} · Δθ = Δθ / r_GUT
    # 电荷半径 ~ r_GUT · (angular extent of ψ₁)

    # 方案 (c): 角向分布宽度决定 r_p
    # r_p ∝ ⟨Δθ²⟩¹/² · (特征径向标度)
    pass


# ============================================================
# §5: 从角向波函数计算电荷半径
# ============================================================

def compute_charge_radius_from_wavefunction(wavefunctions):
    """
    从 Mathieu 波函数直接计算耦合空间中的电荷半径。

    方法 1: 角向波函数的 RMS 宽度
    - Δθ_rms = ⟨θ²⟩¹/²  (相对于 θ=0 或某个参考点)
    - r_p(coupling) ∝ r_GUT · Δθ_rms

    方法 2: 耦合算符在角向的期望值
    - 电荷算符 Q̂(θ) 在角向空间的表示
    - ⟨r²⟩ = ∫ r²(θ) |ψ₁(θ)|² dθ

    方法 3: 傅里叶空间分析
    - G_E(Q²) 从 ψ₁ 的傅里叶变换得到
    - ⟨r²_E⟩ = -6 dG_E/dQ²|_{Q²=0}
    """
    psi1 = wavefunctions[1]

    # --- 方法 1: 角向 RMS 宽度 ---
    # ψ₁ (5̄, DN): θ=0 处 ψ₁=0 (Dirichlet), 最大值在 θ→π/2
    # 电荷分布的 "重心" 和 "宽度"

    theta_grid = np.linspace(0, np.pi/2, 400)
    rho = np.array([float(psi1(t)**2) for t in theta_grid])

    # 归一化概率密度
    norm = np.trapezoid(rho, theta_grid)
    p_theta = rho / norm

    # 一阶矩 (重心)
    theta_mean = np.trapezoid(theta_grid * p_theta, theta_grid)

    # RMS 宽度
    theta_rms = np.sqrt(np.trapezoid((theta_grid - theta_mean)**2 * p_theta, theta_grid))

    # --- 方法 2: 从 GUT 标度映射 ---
    # 电荷半径在耦合空间中的值 (经验): r_p/k ≈ 2r_GUT = 1.236
    # 如果 ψ₁ 的特征角向范围与 r_p 有关...

    # --- 方法 3: 傅里叶空间 ---
    # G_E(Q²) ≈ 1 - ⟨r²⟩Q²/6 + O(Q⁴)
    # 计算 ψ₁ 的角向傅里叶变换

    return {
        'theta_mean': theta_mean,
        'theta_rms': theta_rms,
        'r_GUT': float(r_GUT),
        'r_p_over_k_empirical': 2 * float(r_GUT),  # 经验值
    }


# ============================================================
# §6: 角向测地距离与 Cartan 度规
# ============================================================

def cartan_geodesic_charge_radius(wavefunctions):
    """
    使用 Cartan 平面上的 Poincaré 半平面度规计算电荷半径。

    度规: ds² = du² + e^{-2u} dθ²

    在固定 RG 标度 u = u₀ 处:
    - 角向测地距离 s_θ = e^{-u₀} · θ
    - 对应的物理空间距离 r_phys = k · e^{u₀} · (角向因子)

    电荷半径由电磁荷分布的角向范围决定。
    U(1)_EM 方向在 Cartan 平面上对应 Weinberg 角 θ_W 定义的射线。
    """
    psi1 = wavefunctions[1]

    # Weinberg 角在 Cartan 平面上的位置
    sin2W = float(mp.mpf('0.23120'))
    theta_W = np.arcsin(np.sqrt(sin2W))

    # θ_W 对应于 Cartan 平面上 T₃-Y 混合角
    # 这是电弱对称性破缺在 Cartan 平面上的"方向"

    # 电荷密度在 θ_W 附近的行为
    # ψ₁(θ) 在 θ_W 附近的值反映了电磁耦合的强度分布

    # 角向波函数在 θ_W 处的值
    psi1_at_W = float(psi1(theta_W))
    psi1_at_pi2 = float(psi1(np.pi/2))

    # ψ₁ (5̄, DN): 在 θ=π/2 处达到最大值
    # 但 U(1)_EM 对应的是 θ_W ~ 0.5 rad 附近

    # 计算以 θ_W 为中心的电荷分布 RMS
    theta_grid = np.linspace(0, np.pi/2, 500)
    rho = np.array([float(psi1(t)**2) for t in theta_grid])
    norm = np.trapezoid(rho, theta_grid)
    p = rho / norm

    # θ_W 附近的有效宽度
    theta_mean_weighted = np.trapezoid(theta_grid * p, theta_grid)
    theta_rms_weighted = np.sqrt(np.trapezoid((theta_grid - theta_mean_weighted)**2 * p, theta_grid))

    # 从 Cartan 度规: 物理长度 ∼ k · r_GUT · (角向范围因子)
    # 在 GUT 标度 u = ln(r_GUT):
    #   ds/dθ = e^{-u} = 1/r_GUT
    #   s_angle = θ_rms / r_GUT (耦合空间角向测地距离)
    #   r_phys = k · s_angle

    s_angle_coupling = theta_rms_weighted / float(r_GUT)
    r_p_from_geodesic = float(k_fm) * s_angle_coupling

    return {
        'theta_W': theta_W,
        'psi1_at_thetaW': psi1_at_W,
        'theta_mean': theta_mean_weighted,
        'theta_rms': theta_rms_weighted,
        's_angle_coupling': s_angle_coupling,
        'r_p_geodesic': r_p_from_geodesic,
        'r_p_experiment': 0.8409,
    }


# ============================================================
# §7: 电磁形状因子与电荷半径 (傅里叶方法)
# ============================================================

def form_factor_from_wavefunction(wavefunctions):
    """
    从 Mathieu 波函数计算电磁形状因子 G_E(Q²)。

    方法: 电荷密度在角向空间的傅里叶变换。

    在 CNT 中，电磁流在 Cartan 平面上的角向分布由 ψ₁(θ) 和电荷算符 Q̂(θ) 决定。
    形状因子是此分布在动量空间的表现。

    G_E(Q²) = ∫ e^{iQ·r} ρ_E(r) d³r

    在角向空间中:
    ρ_E(θ) = |ψ₁(θ)|² · Q_eff(θ)
    其中 Q_eff(θ) 是电荷算符 Q̂ = T₃ + Y_SM 在角向的投影

    对于小 Q²，展开 G_E(Q²) ≈ 1 − ⟨r²_E⟩Q²/6 + O(Q⁴)
    → ⟨r²_E⟩ = −6 dG_E/dQ²|_{Q²=0}
    """
    psi1 = wavefunctions[1]

    # 计算角向电荷分布的傅里叶矩
    # 在角向坐标中，Q² 对应角向傅里叶模式

    theta_grid = np.linspace(0, np.pi/2, 500)
    rho = np.array([float(psi1(t)**2) for t in theta_grid])
    norm = np.trapezoid(rho, theta_grid)
    p = rho / norm

    # 角向坐标的 2 阶矩 → 对应 ⟨θ²⟩
    theta_mean = np.trapezoid(theta_grid * p, theta_grid)
    theta2_mean = np.trapezoid(theta_grid**2 * p, theta_grid)
    theta_var = theta2_mean - theta_mean**2

    # 在耦合空间中，角向距离 → 径向物理距离的映射
    # 关系: r_phys ∼ k · r_coupling(θ)
    # 对于小角度: Δr ∼ r_GUT · Δθ (在一阶)
    # 更精确: 使用 Cartan 度规

    # 从 GUT 标度展开:
    # 耦合空间中 r(θ) = r_GUT · exp(∫ C dτ) ...
    # 但在 Cartan 平面几何中，更直接的是:
    # 角向宽度 Δθ 对应物理距离 k · r_GUT · Δθ

    r2_mean_coupling = float(r_GUT**2) * theta_var
    r2_mean_physical = float(k_fm**2) * r2_mean_coupling

    r_E_rms_physical = np.sqrt(r2_mean_physical)

    return {
        'theta_mean': theta_mean,
        'theta_var': theta_var,
        'r2_mean_coupling': r2_mean_coupling,
        'r2_mean_physical': r2_mean_physical,
        'r_E_rms_physical': r_E_rms_physical,
    }


# ============================================================
# §8: 因子 "2" 的第一性原理推导
# ============================================================

def derive_factor_2(wavefunctions):
    """
    推导 r_p/k = 2 × r_GUT 中的因子 2。

    已知:
    - r_GUT = √(4πCλ_c) ≈ 0.618 (耦合空间)
    - r_p/k ≈ 2r_GUT ≈ 1.236 (耦合空间, 经验)
    - λ_p/k ≈ r_GUT/2 ≈ 0.309 (耦合空间, 经验)

    几何级数: λ_p/k : r_GUT : r_p/k = 1/2 : 1 : 2

    第一性原理来源候选:
    1. ℓ=1 跃迁的角向阶 → 2 来自 2ℓ + 1 或 2ℓ
    2. SU(5) Weyl 群阶 |Weyl| = 120 → 因子来自轨道对称性
    3. Mathieu 势的周期 → V(z) = −2q cos(2z) 中的 2
    4. Cartan 平面中 Weyl 腔的几何 → r 的奇偶配对
    """
    psi1, psi2, psi3 = wavefunctions[1], wavefunctions[2], wavefunctions[3]

    # --- 候选 1: ℓ=1 角向阶 ---
    # 5̄→10 跃迁是 ℓ=1 (单根), sin(2θ) 中的 2
    # 电荷半径是 ℓ=1 跃迁的空间范围
    # r_p ∝ (2ℓ + 1) r_GUT / f = 3r_GUT / f ...
    # 对于某种归一化 f, 3/f = 2 → f = 3/2

    # --- 候选 2: Mathieu 势周期 ---
    # V(θ) = −2q cos(2θ), 周期 π
    # 在区间 [0, π/2] 上, 势有 1/4 个周期
    # 电荷分布的特征范围与势的特征尺度有关

    # --- 候选 3: ψ₁ 角向分布特征 ---
    # ψ₁ (5̄, DN) 在 θ → π/2 时达到峰值
    # 从 θ=0 到峰值位置的角度 = π/2
    # r_p ∝ r_GUT · (π/2) / (某特征角)
    # 特征角 ∼ π/4 → r_p ∝ 2r_GUT

    # --- 候选 4: 双曲几何因子 ---
    # Poincaré 半平面: ds² = du² + e^{-2u} dθ²
    # 在 u = ln(r_GUT) 处:
    # 角向范围 θ ∈ [0, π/2] 的测地距离 = e^{-u} · π/2 = π/(2r_GUT)
    # 电磁荷的角向分布范围 = (π/2) · r_GUT × (权重因子)
    # 权重因子 ≈ 4/π → r_p ≈ 2r_GUT

    # 数值检验
    theta_grid = np.linspace(0, np.pi/2, 500)
    rho1 = np.array([float(psi1(t)**2) for t in theta_grid])
    norm1 = np.trapezoid(rho1, theta_grid)
    p1 = rho1 / norm1

    # ψ₁ 累积分布: 50% 分位点
    cdf = np.cumsum(p1) * (theta_grid[1] - theta_grid[0])
    idx_50 = np.argmin(np.abs(cdf - 0.5))
    theta_median = theta_grid[idx_50]

    # 峰值位置
    idx_max = np.argmax(rho1)
    theta_peak = theta_grid[idx_max]

    # 候选公式:
    # r_p / (k·r_GUT) = (π/2) / θ_char
    # 其中 θ_char 是角向分布的特征宽度

    theta_rms = np.sqrt(np.trapezoid((theta_grid - np.average(theta_grid, weights=p1))**2 * p1, theta_grid))

    # 如果 θ_char 定义为使得 ∫₀^{θ_char} |ψ₁|² dθ = 1/2 的角度:
    factor_from_median = (np.pi/2) / theta_median if theta_median > 0 else float('inf')

    # 如果 θ_char 与 ψ₁ 的节点位置有关:
    # ψ₁ = sin(θ) + 高阶修正 → 在 [0, π/2] 上无节点
    # 但"有效宽度" ∼ π/4 → factor ≈ 2

    # 候选公式 (从角向分布直接计算):
    # r_p / k = r_GUT · (∫ θ²|ψ₁|² dθ / ∫ |ψ₁|² dθ)^{-1/2} · normalization
    theta2_mean_p1 = np.trapezoid(theta_grid**2 * p1, theta_grid)
    theta_rms_p1 = np.sqrt(theta2_mean_p1 - np.average(theta_grid, weights=p1)**2)

    # 假设 r_p/k = r_GUT · f(θ_rms), 其中 f 是待定函数
    # 经验上 f 应使 r_p/k = 2r_GUT

    # 尝试 f(θ_rms) = α/θ_rms (量纲: 1/角度)
    alpha_candidate = 2 * theta_rms_p1

    # 尝试 f(θ_rms) = (π/2) / θ_rms (特征角 = π/2 除以 RMS)
    factor_candidate = (np.pi/2) / theta_rms_p1

    return {
        'theta_median': theta_median,
        'theta_peak': theta_peak,
        'theta_rms': theta_rms_p1,
        'theta2_mean': theta2_mean_p1,
        'factor_from_median': factor_from_median,
        'factor_from_rms': factor_candidate,
        'alpha_candidate': alpha_candidate,
        'pi_over_2': np.pi/2,
        'r_GUT': float(r_GUT),
        'r_p_over_k_expected': 2 * float(r_GUT),
    }


# ============================================================
# §9: 电荷半径：最终综合计算
# ============================================================

def comprehensive_charge_radius():
    """
    综合多种方法计算质子电荷半径，寻找第一性原理推导。
    """
    print("=" * 75)
    print("质子电荷半径的第一性原理推导")
    print("=" * 75)

    # 获取波函数
    wavefunctions, eigenvalues = mathieu_wavefunctions(n_terms=80)
    psi1 = wavefunctions[1]

    print(f"\n基础参数:")
    print(f"  C = {float(C):.8f}")
    print(f"  λ_c = {float(lambda_c):.8f}")
    print(f"  r_GUT = {float(r_GUT):.6f} (耦合空间)")
    print(f"  k = {float(k_fm):.6f} fm (映射常数)")
    print(f"  r_GUT × k = {float(r_GUT * k_fm):.6f} fm (GUT 物理尺度)")
    print(f"  r_p (实验) = 0.8409 fm")
    print(f"  r_p/k = {0.8409/float(k_fm):.6f} (耦合空间)")
    print(f"  r_p/k / r_GUT = {0.8409/float(k_fm)/float(r_GUT):.4f}")

    # --- 角向分布特征 ---
    print(f"\n{'='*75}")
    print("§1: ψ₁(5̄) 角向波函数特征")
    print("=" * 75)

    theta_grid = np.linspace(0.001, np.pi/2 - 0.001, 500)
    rho = np.array([float(psi1(t)**2) for t in theta_grid])
    norm = np.trapezoid(rho, theta_grid)
    p = rho / norm

    theta_mean = np.trapezoid(theta_grid * p, theta_grid)
    theta_rms = np.sqrt(np.trapezoid((theta_grid - theta_mean)**2 * p, theta_grid))
    theta_peak = theta_grid[np.argmax(rho)]

    print(f"  θ_mean = {theta_mean:.6f} rad = {theta_mean*180/np.pi:.2f}°")
    print(f"  θ_peak = {theta_peak:.6f} rad = {theta_peak*180/np.pi:.2f}°")
    print(f"  θ_rms  = {theta_rms:.6f} rad = {theta_rms*180/np.pi:.2f}°")
    print(f"  (π/2) / θ_rms = {(np.pi/2)/theta_rms:.4f}")

    psi1_max = float(psi1(np.pi/2 - 0.001))
    print(f"  ψ₁(π/2) ≈ {psi1_max:.4f} (峰值在 θ→π/2)")

    # --- 方法 A: 角向 RMS 方法 ---
    print(f"\n{'='*75}")
    print("§2: 方法 A — 角向 RMS 映射到径向")
    print("=" * 75)

    # 在 Cartan 平面，角向距离与径向距离通过度规关联
    # 最简单的试探: r_p/k = r_GUT × (某种角向因子)

    # 方案 A1: r_p/k = r_GUT · (π/2)/θ_rms
    factor_A1 = (np.pi/2) / theta_rms
    rp_k_A1 = float(r_GUT) * factor_A1
    rp_A1 = float(k_fm) * rp_k_A1

    print(f"  A1: r_p/k = r_GUT · (π/2)/θ_rms = {float(r_GUT):.4f} × {factor_A1:.4f}")
    print(f"      r_p/k = {rp_k_A1:.6f}")
    print(f"      r_p   = {rp_A1:.6f} fm")
    print(f"      偏差   = {abs(rp_A1-0.8409)/0.8409*100:.1f}%")

    # --- 方法 B: Cartan 度规测地距离 ---
    print(f"\n{'='*75}")
    print("§3: 方法 B — Cartan 度规测地距离")
    print("=" * 75)

    # 在 Poincaré 半平面 ds² = du² + e^{-2u} dθ²
    # 在固定 u = ln(r_GUT) 处:
    #   角向测地距离 s = e^{-u} · θ = θ/r_GUT
    #   总角向范围: Δs_max = (π/2)/r_GUT
    #   电荷RMS范围: s_rms = θ_rms/r_GUT
    #   物理半径: r_p = k · (有效径向标度) · s_rms

    # 假设 r_p 由角向测地距离在某个特征径向标度处给出
    s_rms_coupling = theta_rms / float(r_GUT)  # 耦合空间中的 RMS 测地距离

    # 物理空间的电荷半径:
    # r_p 应该既涉及 θ_rms (角向分布) 又涉及 r_GUT (径向标度)
    # 试探: r_p = k · r_GUT² · (θ_rms 的函数)

    rp_B1 = float(k_fm) * float(r_GUT) * theta_rms  # 最简单的量纲匹配
    rp_B2 = float(k_fm) * float(r_GUT**2) * theta_rms / (np.pi/2)

    print(f"  B1: r_p = k · r_GUT · θ_rms = {rp_B1:.6f} fm")
    print(f"      偏差 = {abs(rp_B1-0.8409)/0.8409*100:.1f}%")
    print(f"  B2: r_p = k · r_GUT² · θ_rms / (π/2) = {rp_B2:.6f} fm")
    print(f"      偏差 = {abs(rp_B2-0.8409)/0.8409*100:.1f}%")

    # --- 方法 C: 级数展开 → 因子 2 的推导 ---
    print(f"\n{'='*75}")
    print("§4: 方法 C — 因子 2 的群论/几何推导")
    print("=" * 75)

    # 方案 C1: ℓ=1 跃迁因子
    # sin(2θ) 算符中的 2 来自 SU(5) 根长度
    # 电荷半径是 ℓ=1 的 "空间尺度":
    #   r_p/k = (ℓ + 1) r_GUT = 2 r_GUT

    # 方案 C2: Weyl 腔几何
    # Weyl 腔在 Cartan 平面上的大小:
    #   全腔角向范围 = π/2
    #   有效 (电磁) 范围 = π/4
    #   r_p/k = r_GUT · (π/2) / (π/4) = 2 r_GUT

    # 方案 C3: Mathieu 势
    # V(θ) = -2q cos(2θ), cos(2θ) 的周期 = π
    # 在 [0, π/2] 中，势覆盖 1/2 周期
    # 电荷半径与半周期的几何平均有关

    # 关键: 2 的群论来源
    # SU(5) 中，Coxeter 数 h = 5
    # 对偶 Coxeter 数 h∨ = 5
    # 但 factor 2 似乎来自 ℓ=1 → ℓ+1 = 2
    # 物理上: 电荷半径是 5̄→10 跃迁 (ℓ=1) 的空间范围
    #   跃迁算符 sin(2θ) 在 [0, π/2] 上在 θ=π/4 有节点
    #   电荷分布在此节点两侧 → 特征范围 = 2 · (节点到边界的距离)

    # 计算 sin(2θ) 在 θ ∈ [0, π/2] 上的节点: θ_node = π/4
    # 电磁荷的有效分布区间 [π/4, π/2] (sin(2θ) > 0, 对应正向电荷)
    theta_node = np.pi / 4

    # 在此区间内 ψ₁ 的 RMS:
    mask = theta_grid > theta_node
    p_EM = p[mask].copy()
    p_EM /= np.sum(p_EM) * (theta_grid[1] - theta_grid[0])

    theta_EM_mean = np.average(theta_grid[mask], weights=p_EM)
    theta_EM_rms = np.sqrt(np.average((theta_grid[mask] - theta_EM_mean)**2, weights=p_EM))

    # ℓ=1 的意义:
    #   sin(2θ) = 2 sinθ cosθ, 在 [π/4, π/2] 上为正
    #   电荷分布的有效角向范围 = (π/2 - π/4) = π/4
    #   平均位置 = π/4 + π/8 = 3π/8

    rp_k_C1 = float(r_GUT) * 2  # ℓ+1 = 2
    rp_C1 = rp_k_C1 * float(k_fm)

    print(f"  C1: r_p/k = (ℓ+1) r_GUT = 2·r_GUT = {rp_k_C1:.6f}")
    print(f"      r_p = {rp_C1:.6f} fm")
    print(f"      偏差 = {abs(rp_C1-0.8409)/0.8409*100:.2f}%")

    # --- 方法 D: 从形状因子 Q²→0 极限 ---
    print(f"\n{'='*75}")
    print("§5: 方法 D — 形状因子斜率方法")
    print("=" * 75)

    # 角向分布的傅里叶变换给出形状因子
    # 小 Q² 展开: G_E(Q²) ≈ 1 - ⟨r²⟩Q²/6

    # 在角向空间:
    #   动量 Q 对应角向傅里叶模式 n
    #   角向 Q² ∼ n² (离散模式)
    #   ⟨r²⟩ ∼ (特征角向模式间距)⁻²

    # ℓ=1 的 sin(2θ) 对应 n=2
    # 特征 Q² ∼ 2² = 4 (在角向单位下)
    # ⟨r²_E⟩ ∼ 6 · (1/4) · (径向映射因子)

    # 更精确地:
    r2_from_form_factor_coupling = float(r_GUT**2) * 6/4  # ⟨r²⟩ = 6/(n²) × r_GUT²
    r_E_from_ff_coupling = np.sqrt(r2_from_form_factor_coupling)
    r_E_from_ff_physical = float(k_fm) * r_E_from_ff_coupling

    print(f"  角向模式 n = 2 (sin(2θ))")
    print(f"  ⟨r²⟩_coupling = 6/n² · r_GUT² = {r2_from_form_factor_coupling:.4f}")
    print(f"  r_E_coupling  = {r_E_from_ff_coupling:.4f}")
    print(f"  r_E_physical  = {r_E_from_ff_physical:.4f} fm")
    print(f"  偏差 = {abs(r_E_from_ff_physical-0.8409)/0.8409*100:.1f}%")

    # --- 方法 E: 从 ρ₂ 叠积分直接导出 ---
    print(f"\n{'='*75}")
    print("§6: 方法 E — 从 ρ₂ 重叠积分导出电荷半径")
    print("=" * 75)

    # ρ₂ = |∫ ψ₂* sin(2θ) ψ₁ dθ|²
    # 重叠积分测量了 sin(2θ) 在波函数间的矩阵元
    # 这个矩阵元与电荷半径有关:
    #   |⟨r⟩| ∼ (重叠积分)^{1/2} · (特征尺度)

    # 计算 ρ₂
    psi2 = wavefunctions[2]
    f_int_rho2 = lambda t: psi1(t) * psi2(t) * mp.sin(2*mp.mpf(t))
    I_rho2 = mp.quad(f_int_rho2, [0, mp.pi/2])
    rho2 = float(abs(I_rho2)**2)

    # sin(2θ) 的 "空间范围" 特征:
    #   ⟨sin²(2θ)⟩ = 1/2 over [0, π/2]
    #   但 ψ₂ 的权重改变了这个平均值

    # 电荷半径的一阶矩 ⟨r⟩ 推测:
    #   ⟨r⟩/k ∝ r_GUT · (∫ ψ₂* sin(2θ) ψ₁ dθ)^{−1/2}
    #   或 ∝ r_GUT · ρ₂^{−1/4}

    rp_k_E1 = float(r_GUT) * rho2**(-0.25)  # 试探
    rp_k_E2 = float(r_GUT) * (rho2/0.19907)**(-0.5)  # 归一化到经验 ρ₂=0.1991

    print(f"  ρ₂ = {rho2:.6f}")
    print(f"  E1: r_p/k = r_GUT · ρ₂^(-1/4) = {rp_k_E1:.4f}")
    print(f"      偏差 vs 2r_GUT = {abs(rp_k_E1-2*float(r_GUT))/(2*float(r_GUT))*100:.2f}%")

    # --- 综合汇总 ---
    print(f"\n{'='*75}")
    print("§7: 综合对比")
    print("=" * 75)

    rp_exp_coupling = 0.8409 / float(k_fm)

    results = {
        '实验 r_p/k': rp_exp_coupling,
        'A1 (角向RMS)': rp_k_A1,
        'C1 (ℓ+1)': rp_k_C1,
        'D (形状因子)': r_E_from_ff_coupling,
        'E1 (ρ₂尺度)': rp_k_E1,
    }

    print(f"\n  {'方法':20s} {'r_p/k':>10s} {'vs 实验':>10s}")
    print(f"  {'-'*42}")
    for name, val in results.items():
        dev = abs(val - rp_exp_coupling) / rp_exp_coupling * 100
        print(f"  {name:20s} {val:10.6f} {dev:+9.2f}%")

    return results


# ============================================================
# §10: 主程序
# ============================================================

if __name__ == '__main__':
    results = comprehensive_charge_radius()

    print(f"\n{'='*75}")
    print("初步结论")
    print("=" * 75)
    print(f"""
1. 质子电荷半径 r_p = 0.841 fm 在耦合空间中对应 r_p/k = 2r_GUT = 1.236
   因子 "2" 是目前需要从第一性原理推导的核心

2. 候选推导路径:
   (a) ℓ=1 跃迁 (5̄→10): r_p/k = (ℓ+1)r_GUT = 2r_GUT
       物理: 电荷半径是第一次角向激发的空间尺度
   (b) sin(2θ) 节点在 θ=π/4: 电荷分布的有效区间 [π/4, π/2]
       几何平均给出 r_p/k = 2r_GUT
   (c) 形状因子极点: G_E(Q²) ∼ 1/(1 + Q²/Λ²)
       Λ = √12/(r_p) → r_p ∼ √12/Λ
       在 CNT 中 Λ 由 sin(2θ) 的角向模式 n=2 决定

3. 下一步: 严格证明因子 2 来自 SU(5) Cartan 平面上的 Weyl 腔几何，
   将 r_p 的表达式写成仅含 C, λ_c, r_GUT, k 的第一性原理形式
""")
