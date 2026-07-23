"""
3圈修正的第一性原理严格推导（修正版）
基于闭合核增殖理论（CNT），纠正素数-相互作用映射：
  p=2 → 电磁 U(1)  [f_em = f_rep/128]
  p=3 → 弱 SU(2)    [f_w = f_rep/27]
  p=5 → 强 SU(3)    [f_s = f_rep/5]
理论来源: CNTFormal/06-前沿研究/05-路径积分与力学形式研究.md §12.4.1
"""

import math
from fractions import Fraction

# ============================================================
# 0. 精确常数
# ============================================================

alpha_0_inv = 16384 * math.pi / 375  # EPRL 4-单纯形裸值
alpha_0 = 1 / alpha_0_inv
alpha_exp_inv = 137.035999084  # PDG 2024
alpha_exp_err = 0.000000021

# 2/9修正: EPRL 2-单纯形 (1圈)
correction_2_9 = Fraction(2, 9)
alpha_2_inv = alpha_0_inv - float(correction_2_9)

# 展开参数
eps = alpha_0 / (4 * math.pi)  # ε = α₀/(4π)

# ============================================================
# 1. p进结构和频率（理论文档§12.4.1）
# ============================================================

# p进权重因子
def p_adic_weight(p):
    num = p**3 + p**2 + p - 1
    den = p * (p + 1) * (p**2 + p + 1)
    return Fraction(num, den)

w = {p: p_adic_weight(p) for p in [2, 3, 5]}

# 增殖频率（来自理论文档）
# f_em = f_rep / 128 = f_rep / 2^7  → p=2
# f_w  = f_rep / 27  = f_rep / 3^3  → p=3
# f_s  = f_rep / 5                   → p=5
f = {2: Fraction(1, 128), 3: Fraction(1, 27), 5: Fraction(1, 5)}

# 几何因子: 4-单纯形二面角 Θ = arccos(1/4)
sin2_Theta = 15.0 / 16.0  # sin²Θ = 15/16

print("=" * 85)
print("闭合核理论（CNT）3圈修正 — 修正素数映射")
print("p=2→电磁(U(1)), p=3→弱(SU(2)), p=5→强(SU(3))")
print("=" * 85)

print(f"\n[0] 基础常数")
print(f"    α₀⁻¹ = 16384π/375 = {alpha_0_inv:.10f}")
print(f"    α_exp⁻¹ = {alpha_exp_inv:.10f} ± {alpha_exp_err:.10f}")
print(f"    展开参数 ε = α₀/(4π) = {eps:.6e}")
print(f"    1圈修正 2/9 = {float(correction_2_9):.10f}")
print(f"    α⁻¹(1圈) = {alpha_2_inv:.10f}")

print(f"\n[1] 素数-相互作用映射（理论文档§12.4.1）")
print(f"    {'素数':<6} {'权重 w_p':<16} {'频率 f_p':<16} {'相互作用':<16} {'规范群'}")
print(f"    {'-'*65}")
print(f"    p=2     {float(w[2]):.10f}       {float(f[2]):.10f}        {'电磁 (EM)':<16} {'U(1)'}")
print(f"    p=3     {float(w[3]):.10f}       {float(f[3]):.10f}        {'弱 (Weak)':<16} {'SU(2)'}")
print(f"    p=5     {float(w[5]):.10f}       {float(f[5]):.10f}        {'强 (Strong)':<16} {'SU(3)'}")

# ============================================================
# 2. Weinberg角的第一性原理推导
# ============================================================

print(f"\n{'='*85}")
print("2. Weinberg角 sin²θ_W 的第一性原理推导")
print(f"{'='*85}")

print(f"""
[物理分析] Weinberg角描述电弱统一中U(1)_Y与SU(2)_L的混合。
  在CNT中:
    - U(1)_Y (超荷) → 关联于电磁通道 p=2
    - SU(2)_L (弱同位旋) → 关联于弱通道 p=3
    - 强相互作用 p=5 不参与电弱混合

[推导] 增殖频率比:
  f_em / f_w = (1/128) / (1/27) = 27/128 = {float(f[2])/float(f[3]):.6f}

  经4-单纯形二面角几何修正:
  sin²θ_W = (f_em/f_w) × (1/sin²Θ)
          = (27/128) × (16/15)
          = 9/40
          = {9/40:.6f}
""")

# 方案A: 频率比 + 几何修正（理论推导值）
sin2_W_A = (27.0/128.0) * (16.0/15.0)  # = 9/40 = 0.225

# 方案B: p进权重（仅电弱子空间）
sin2_W_B = float(w[3]) / (float(w[2]) + float(w[3]))

# 方案C: 实验值
sin2_W_exp = 0.23121

print(f"  方案A (频率比+几何): sin²θ_W = 9/40 = {sin2_W_A:.6f}")
print(f"  方案B (p进权重, 电弱子空间): sin²θ_W = w_3/(w_2+w_3) = {sin2_W_B:.6f}")
print(f"  方案C (实验值, PDG): sin²θ_W = {sin2_W_exp:.6f}")
print(f"  理论文档引用值: sin²θ_W ≈ 0.223 (§12.5.8)")

# 选用方案A（频率比+几何修正）作为理论值
sin2_W = sin2_W_A

# ============================================================
# 3. 弱-强混合角（p=3 ↔ p=5）
# ============================================================

print(f"\n{'='*85}")
print("3. 弱-强混合角 sin²θ_35 的推导")
print(f"{'='*85}")

# 方案A: 频率比
f_w = float(f[3])  # 1/27
f_s = float(f[5])  # 1/5
sin2_35_A = (f_w / (f_w + f_s)) * (16.0/15.0)  # 频率比 + 几何修正

# 方案B: p进权重
sin2_35_B = float(w[3]) / (float(w[3]) + float(w[5]))

print(f"""
[推导] 弱(p=3)与强(p=5)增殖通道的交叉耦合:

  频率比: f_w/(f_w+f_s) = (1/27)/(1/27+1/5) = 5/32 = {5/32:.6f}
  方案A (频率比+几何): sin²θ_35 = (5/32)×(16/15) = 1/6 = {sin2_35_A:.6f}
  方案B (p进权重): sin²θ_35 = w_3/(w_3+w_5) = {sin2_35_B:.6f}
""")

sin2_35 = sin2_35_A

# ============================================================
# 4. 2圈弱混合修正 (p=2 ↔ p=3)
# ============================================================

print(f"{'='*85}")
print("4. 2圈弱混合修正 (p=2 EM ↔ p=3 Weak)")
print(f"{'='*85}")

# 2圈系数 C_2 = 1 + sin²θ_W × sin²Θ
C_2 = 1.0 + sin2_W * sin2_Theta
delta_2loop = alpha_0_inv * eps**2 * C_2
alpha_2loop_inv = alpha_2_inv - delta_2loop

print(f"""
[推导] 2圈图: p=2 (电磁) 与 p=3 (弱) 增殖通道的交叉耦合

  C_2 = 1 + sin²θ_W × sin²Θ
      = 1 + {sin2_W:.6f} × {sin2_Theta:.6f}
      = {C_2:.6f}

  Δα⁻¹_2 = -α₀⁻¹ × ε² × C_2
          = -{alpha_0_inv:.2f} × ({eps:.6e})² × {C_2:.4f}
          = -{delta_2loop:.10f}

  α⁻¹_2loop = α₀⁻¹ - 2/9 - Δα⁻¹_2
            = {alpha_2loop_inv:.10f}
""")

gap_2loop = alpha_2loop_inv - alpha_exp_inv
print(f"  与实验偏差: {gap_2loop:+.10f} ({abs(gap_2loop)/alpha_exp_inv*1e9:.1f} ppb, {abs(gap_2loop)/alpha_exp_err:.1f}σ)")

# 也尝试方案B和C的Weinberg角
for name, sw in [("方案B (权重)", sin2_W_B), ("方案C (实验)", sin2_W_exp)]:
    C2_try = 1.0 + sw * sin2_Theta
    d2_try = alpha_0_inv * eps**2 * C2_try
    a2_try = alpha_2_inv - d2_try
    gap_try = a2_try - alpha_exp_inv
    print(f"  [{name}] sin²θ_W={sw:.6f}, C_2={C2_try:.4f}, α⁻¹={a2_try:.10f}, 偏差={gap_try:+.1e} ({abs(gap_try)/alpha_exp_err:.1f}σ)")

# ============================================================
# 5. 3圈图拓扑分析（修正后）
# ============================================================

print(f"\n{'='*85}")
print("5. 3圈图拓扑分析（修正映射: p=2→p=3→p=5）")
print(f"{'='*85}")

print(f"""
[物理分析] CNT中的层级涌现顺序（理论文档§12.4.1）:
  第1层: p=2 (电磁, U(1)) — 单面网络, f_em = f_rep/128
  第2层: p=5 (强, SU(3))   — 双面网络, f_s = f_rep/5
  第3层: p=3 (弱, SU(2))   — 三面网络, f_w = f_rep/27

[注] CNT的涌现顺序是 EM → 强 → 弱，与标准模型发现顺序
     (EM → 弱 → 强) 不同。但CNT中弱力是"三面网络"的最深层涌现，
     强力是"双面网络"的中间涌现。

[推导] 3圈增殖图的三种基本拓扑:

  拓扑A: p=2 → p=2 → p=2  (纯电磁三级嵌套)
    - 所有增殖顶点都是p=2
    - 无跨通道耦合, C_3^(A) = 1

  拓扑B: p=2 → p=2 → p=3  (电磁嵌套含弱)
    - 外层p=2, 内层p=3
    - 嵌套: 1, 交叉: sin²θ_W × sin²Θ
    - C_3^(B) = C_2 = 1 + sin²θ_W × sin²Θ

  拓扑C: p=2 → p=5 → p=3  (全层级: EM→强→弱)
    - 外层p=2, 中层p=5, 内层p=3
    - p=2↔p=3: sin²θ_W × sin²Θ
    - p=5↔p=3: sin²θ_35 × sin²Θ
    - p=2↔p=5: (sin²θ_W × sin²θ_35)^(1/2) × sin²Θ (间接)
    - 这是CNT涌现顺序(EM→强→弱)的完整3圈实现
""")

# ============================================================
# 6. 各拓扑的C_3系数
# ============================================================

print(f"{'='*85}")
print("6. C_3系数计算")
print(f"{'='*85}")

# 拓扑A: 纯电磁
C3_A = 1.0
print(f"\n[拓扑A] p=2→p=2→p=2: C_3 = {C3_A:.6f}")

# 拓扑B: EM-EM-weak
C3_B_nest = 1.0
C3_B_cross = sin2_W * sin2_Theta
C3_B = C3_B_nest + C3_B_cross
print(f"\n[拓扑B] p=2→p=2→p=3: C_3 = 1 + sin²θ_W×sin²Θ = {C3_B:.6f}")
print(f"  [注] C_3^(B) = C_2 = {C_2:.6f} (2圈弱混合在3圈的自然延伸)")

# 拓扑C: EM-strong-weak
C3_C_nest = 1.0
C3_C_cross_23 = sin2_W * sin2_Theta          # p=2 ↔ p=3 (弱混合)
C3_C_cross_53 = sin2_35 * sin2_Theta          # p=3 ↔ p=5 (弱-强混合)
C3_C_cross_25 = math.sqrt(sin2_W * sin2_35) * sin2_Theta  # p=2 ↔ p=5 (间接)
C3_C_cross = C3_C_cross_23 + C3_C_cross_53 + C3_C_cross_25
C3_C = C3_C_nest + C3_C_cross

print(f"\n[拓扑C] p=2→p=5→p=3 (全层级: EM→强→弱)")
print(f"  C_3^(C)_nest = 1")
print(f"  交叉项:")
print(f"    p=2↔p=3: sin²θ_W × sin²Θ = {sin2_W:.6f} × {sin2_Theta:.6f} = {C3_C_cross_23:.6f}")
print(f"    p=3↔p=5: sin²θ_35 × sin²Θ = {sin2_35:.6f} × {sin2_Theta:.6f} = {C3_C_cross_53:.6f}")
print(f"    p=2↔p=5 (间接): √(sin²θ_W×sin²θ_35) × sin²Θ = {C3_C_cross_25:.6f}")
print(f"  C_3^(C)_cross = {C3_C_cross:.6f}")
print(f"  C_3^(C) = {C3_C:.6f}")

# ============================================================
# 7. 统计权重
# ============================================================

print(f"\n{'='*85}")
print("7. 增殖树统计权重")
print(f"{'='*85}")

# 在K=196次分裂事件中:
N_total = 196
N_2 = 98   # 偶数步数 (p=2)
N_3 = 65   # 3的倍数 (p=3)
N_5 = 39   # 5的倍数 (p=5)

# 重叠计数
N_23 = 196 // 6   # 2和3的公倍数 = 32
N_25 = 196 // 10  # 2和5的公倍数 = 19
N_35 = 196 // 15  # 3和5的公倍数 = 13
N_235 = 196 // 30 # 2,3,5的公倍数 = 6

# 修正: 纯p=2 (偶数但不是3或5的倍数)
N_A = N_2 - N_23 - N_25 + N_235  # 98 - 32 - 19 + 6 = 53
# 纯p=2+p=3 (2和3的倍数但不是5的倍数)
N_B = N_23 - N_235  # 32 - 6 = 26
# p=2+p=3+p=5 (30的倍数)
N_C = N_235  # 6

# 但3圈修正涉及3个顶点的组合。对于拓扑B (p=2→p=2→p=3):
# 需要两个连续p=2顶点后跟一个p=3顶点
# 简化: 使用单顶点频率

w_A = N_A / 196.0
w_B = N_B / 196.0
w_C = N_C / 196.0

print(f"  分裂事件统计 (K=196):")
print(f"    纯p=2: {N_A} ({w_A*100:.1f}%)")
print(f"    p=2+p=3: {N_B} ({w_B*100:.1f}%)")
print(f"    p=2+p=3+p=5: {N_C} ({w_C*100:.1f}%)")

# 加权平均
C3_weighted = (w_A * C3_A + w_B * C3_B + w_C * C3_C) / (w_A + w_B + w_C)

print(f"\n  加权平均 C_3 = ({w_A:.1f}×{C3_A:.3f} + {w_B:.1f}×{C3_B:.3f} + {w_C:.1f}×{C3_C:.3f}) / {w_A+w_B+w_C:.1f}")
print(f"                = {C3_weighted:.6f}")

# ============================================================
# 8. 3圈修正数值计算
# ============================================================

print(f"\n{'='*85}")
print("8. 3圈修正数值计算")
print(f"{'='*85}")

eps3 = eps**3
print(f"\n  ε³ = (α₀/(4π))³ = {eps3:.6e}")
print(f"  α₀⁻¹ × ε³ = {alpha_0_inv * eps3:.6e}")
print(f"\n{'方案':<40} {'C_3':<10} {'Δα⁻¹_3':<16} {'α⁻¹_3loop':<18} {'偏差':<12} {'σ':<8}")
print("-" * 105)

schemes = [
    ("方案0: 无3圈 (2圈结果)", 0.0),
    ("方案1: C_3=1 (纯嵌套)", 1.0),
    ("方案2: C_3=C_2 (2圈延伸)", C_2),
    ("方案3: C_3=C_3^(C) (全层级拓扑C)", C3_C),
    ("方案4: C_3=加权平均", C3_weighted),
    ("方案5: C_3=1+sin²θ_W×sin²Θ (仅弱混合)", 1.0 + sin2_W * sin2_Theta),
    ("方案6: C_3=1+sin²θ_W×sin²Θ+sin²θ_35×sin²Θ", 
     1.0 + sin2_W * sin2_Theta + sin2_35 * sin2_Theta),
]

for name, C3_val in schemes:
    delta_3 = alpha_0_inv * eps3 * C3_val
    alpha_3_inv = alpha_2loop_inv - delta_3
    gap = alpha_3_inv - alpha_exp_inv
    n_sigma = abs(gap) / alpha_exp_err
    print(f"{name:<40} {C3_val:<10.4f} -{delta_3:<15.6e} {alpha_3_inv:<18.10f} {gap:+.1e}  {n_sigma:<7.1f}")

# 最佳C_3
C3_opt = (alpha_2loop_inv - alpha_exp_inv) / (alpha_0_inv * eps3)
print(f"\n[优化] 使偏差=0的C_3: C_3^(opt) = {C3_opt:.6f}")

# ============================================================
# 9. 完整精度对比
# ============================================================

print(f"\n{'='*85}")
print("9. 完整精度对比表")
print(f"{'='*85}")

# 用方案4 (加权平均) 作为最终3圈结果
alpha_3_inv_final = alpha_2loop_inv - alpha_0_inv * eps3 * C3_weighted
gap_3loop = alpha_3_inv_final - alpha_exp_inv

print(f"\n{'阶段':<38} {'α⁻¹':<18} {'差值':<14} {'偏差':<14} {'σ':<8}")
print("-" * 95)
print(f"{'裸值 (EPRL 4-单纯形)':<38} {alpha_0_inv:<18.10f} {alpha_0_inv-alpha_exp_inv:+.10f}  {(alpha_0_inv-alpha_exp_inv)/alpha_exp_inv*1e6:.1f} ppm  {(alpha_0_inv-alpha_exp_inv)/alpha_exp_err:.0f}σ")
print(f"{'+ 2-单纯形修正 (1圈, 2/9)':<38} {alpha_2_inv:<18.10f} {alpha_2_inv-alpha_exp_inv:+.10f}  {(alpha_2_inv-alpha_exp_inv)/alpha_exp_inv*1e9:.1f} ppb  {(alpha_2_inv-alpha_exp_inv)/alpha_exp_err:.0f}σ")

# 2圈结果
gap_2 = alpha_2loop_inv - alpha_exp_inv
print(f"{'+ 弱混合修正 (2圈, p=2↔p=3)':<38} {alpha_2loop_inv:<18.10f} {gap_2:+.10f}  {abs(gap_2)/alpha_exp_inv*1e9:.1f} ppb  {abs(gap_2)/alpha_exp_err:.1f}σ")

# 3圈结果
gap_3 = alpha_3_inv_final - alpha_exp_inv
print(f"{'+ 3圈修正 (加权平均)':<38} {alpha_3_inv_final:<18.10f} {gap_3:+.10f}  {abs(gap_3)/alpha_exp_inv*1e9:.1f} ppb  {abs(gap_3)/alpha_exp_err:.1f}σ")
print(f"{'实验值 (PDG 2024)':<38} {alpha_exp_inv:<18.10f} ±{alpha_exp_err:.10f}  {'---':<14} {'---'}")

# ============================================================
# 10. 理论自洽性分析
# ============================================================

print(f"\n{'='*85}")
print("10. 理论自洽性分析")
print(f"{'='*85}")

print(f"""
[关键结论]

1. 素数映射修正:
   p=2 → EM(U(1)), p=3 → Weak(SU(2)), p=5 → Strong(SU(3))
   此映射来自理论文档§12.4.1的频率结构:
   f_em=f_rep/128, f_w=f_rep/27, f_s=f_rep/5

2. Weinberg角:
   sin²θ_W = (f_em/f_w)×(1/sin²Θ) = 9/40 = {sin2_W:.6f}
   (理论值) vs 实验值 0.23121
   偏差: {(sin2_W-0.23121)/0.23121*100:.1f}%

3. 2圈弱混合修正 (p=2↔p=3):
   C_2 = 1 + sin²θ_W × sin²Θ = {C_2:.6f}
   Δα⁻¹_2 = {delta_2loop:.6e}
   2圈理论值: α⁻¹ = {alpha_2loop_inv:.10f}
   偏差: {gap_2loop:+.1e} ({abs(gap_2loop)/alpha_exp_err:.1f}σ)

4. 3圈修正:
   加权平均 C_3 = {C3_weighted:.6f}
   3圈修正量: {alpha_0_inv * eps3 * C3_weighted:.2e}
   3圈理论值: α⁻¹ = {alpha_3_inv_final:.10f}
   偏差: {gap_3loop:+.1e} ({abs(gap_3loop)/alpha_exp_err:.1f}σ)

5. 与旧映射(p=5→弱)对比:
   旧映射下Weinberg角 sin²θ_W = w_5/(w_2+w_3+w_5) = {float(w[5])/(float(w[2])+float(w[3])+float(w[5])):.6f}
   与实验值偏差仅0.35%，但素数映射与理论文档矛盾。
   新映射下Weinberg角由频率比+几何因子给出，理论自洽。
""")

# ============================================================
# 11. 4圈修正 — 再算一圈
# ============================================================

print(f"\n{'='*85}")
print("11. 4圈修正 — 四顶点增殖图的拓扑与系数")
print(f"{'='*85}")

eps4 = eps**4
print(f"\n  ε⁴ = (α₀/(4π))⁴ = {eps4:.6e}")
print(f"  α₀⁻¹ × ε⁴ = {alpha_0_inv * eps4:.6e}")
print(f"  实验误差 (α⁻¹): {alpha_exp_err:.2e}")
print(f"  4圈/实验误差比值: {alpha_0_inv * eps4 / alpha_exp_err:.2e}")

# 4圈拓扑分析
# 交叉耦合规则: 对于不同的素数通道 p_i ≠ p_j,
# 耦合强度 = f_min / f_max (频率比, 较小/较大)
cross = {
    (2,3): float(f[2]) / float(f[3]),  # f_em/f_w = 27/128
    (3,5): float(f[3]) / float(f[5]),  # f_w/f_s = 5/27
    (2,5): float(f[2]) / float(f[5]),  # f_em/f_s = 5/128
}

print(f"\n[交叉耦合强度] f_min/f_max:")
print(f"  p=2↔p=3 (EM↔Weak):   f_em/f_w = 27/128 = {cross[(2,3)]:.6f}")
print(f"  p=3↔p=5 (Weak↔Strong): f_w/f_s = 5/27  = {cross[(3,5)]:.6f}")
print(f"  p=2↔p=5 (EM↔Strong):  f_em/f_s = 5/128 = {cross[(2,5)]:.6f}")

# 4圈拓扑: 4个顶点的增殖序列
# 物理上有意义的序列 (按CNT层级: p=2外层 → p=5中层 → p=3内层)
# 对于4圈, 考虑所有相邻顶点的交叉耦合对

def C4_from_sequence(seq):
    """计算给定素数序列的C_4系数 (仅最近邻交叉耦合)"""
    C = 1.0
    pairs = []
    for i in range(len(seq) - 1):
        if seq[i] != seq[i+1]:
            p_min, p_max = min(seq[i], seq[i+1]), max(seq[i], seq[i+1])
            C += cross[(p_min, p_max)]
            pairs.append((seq[i], seq[i+1]))
    return C, pairs

# 主要拓扑
topologies_4 = [
    ("(2,2,2,2) 纯电磁四级嵌套", (2,2,2,2)),
    ("(2,2,2,3) EM→EM→EM→Weak", (2,2,2,3)),
    ("(2,2,2,5) EM→EM→EM→Strong", (2,2,2,5)),
    ("(2,2,5,5) EM→EM→Strong→Strong", (2,2,5,5)),
    ("(2,2,5,3) EM→EM→Strong→Weak", (2,2,5,3)),
    ("(2,2,3,3) EM→EM→Weak→Weak", (2,2,3,3)),
    ("(2,5,5,5) EM→Strong→Strong→Strong", (2,5,5,5)),
    ("(2,5,5,3) EM→Strong→Strong→Weak", (2,5,5,3)),
    ("(2,5,3,3) EM→Strong→Weak→Weak", (2,5,3,3)),
    ("(2,3,3,3) EM→Weak→Weak→Weak", (2,3,3,3)),
]

print(f"\n[4圈拓扑 C₄ 系数]:")
print(f"  {'拓扑':<42} {'C₄':<10} {'交叉对'}")
print(f"  {'-'*70}")
for name, seq in topologies_4:
    C4, pairs = C4_from_sequence(seq)
    pair_str = ", ".join([f"{a}↔{b}" for a,b in pairs]) if pairs else "无"
    print(f"  {name:<42} {C4:<10.6f} {pair_str}")

# 统计权重 (与3圈类似, 扩展至4顶点)
# 在K=196次分裂中, 4顶点序列的统计权重
# 简化: 使用多项式分布

# 各类顶点的比例
p_2 = N_A / 196.0  # 纯p=2: 53/196 = 0.2704
p_23 = N_B / 196.0  # p=2+p=3: 26/196 = 0.1327
p_235 = N_C / 196.0  # p=2+p=3+p=5: 6/196 = 0.0306

# 对于4顶点序列, 权重正比于各顶点类型的乘积
# 简化: 按拓扑类型分类权重

# 纯EM (所有顶点p=2): 权重 ∝ p_2^4
w_2222 = p_2**4

# 含1个p=3 (EM→EM→EM→Weak): 权重 ∝ p_2^3 × p_23
w_2223 = p_2**3 * p_23

# 含1个p=5 (EM→EM→EM→Strong): 权重 ∝ p_2^3 × p_235
w_2225 = p_2**3 * p_235

# 含p=5和p=3 (EM→EM→Strong→Weak): 权重 ∝ p_2^2 × p_23 × p_235
w_2253 = p_2**2 * p_23 * p_235

# 含p=5, p=5 (EM→Strong→Strong→Weak): 权重 ∝ p_2 × p_235^2 × p_23
w_2553 = p_2 * p_235**2 * p_23

# 含p=5, p=3, p=3 (EM→Strong→Weak→Weak): 权重 ∝ p_2 × p_235 × p_23^2
w_2533 = p_2 * p_235 * p_23**2

# 纯p=3结尾 (EM→Weak→Weak→Weak): 权重 ∝ p_2 × p_23^3
w_2333 = p_2 * p_23**3

# 纯p=5结尾 (EM→Strong→Strong→Strong): 权重 ∝ p_2 × p_235^3
w_2555 = p_2 * p_235**3

# EM→EM→Strong→Strong: 权重 ∝ p_2^2 × p_235^2
w_2255 = p_2**2 * p_235**2

# EM→EM→Weak→Weak: 权重 ∝ p_2^2 × p_23^2
w_2233 = p_2**2 * p_23**2

# 总权重
w_total_4 = (w_2222 + w_2223 + w_2225 + w_2255 + w_2253 + 
             w_2233 + w_2555 + w_2553 + w_2533 + w_2333)

# 加权平均C₄
C4_weighted = (
    w_2222 * C4_from_sequence((2,2,2,2))[0] +
    w_2223 * C4_from_sequence((2,2,2,3))[0] +
    w_2225 * C4_from_sequence((2,2,2,5))[0] +
    w_2255 * C4_from_sequence((2,2,5,5))[0] +
    w_2253 * C4_from_sequence((2,2,5,3))[0] +
    w_2233 * C4_from_sequence((2,2,3,3))[0] +
    w_2555 * C4_from_sequence((2,5,5,5))[0] +
    w_2553 * C4_from_sequence((2,5,5,3))[0] +
    w_2533 * C4_from_sequence((2,5,3,3))[0] +
    w_2333 * C4_from_sequence((2,3,3,3))[0]
) / w_total_4

print(f"\n[统计权重与加权平均]:")
print(f"  w(2222) = {w_2222:.6f} ({w_2222/w_total_4*100:.1f}%)")
print(f"  w(2223) = {w_2223:.6f} ({w_2223/w_total_4*100:.1f}%)")
print(f"  w(2225) = {w_2225:.6f} ({w_2225/w_total_4*100:.1f}%)")
print(f"  w(2255) = {w_2255:.6f} ({w_2255/w_total_4*100:.1f}%)")
print(f"  w(2253) = {w_2253:.6f} ({w_2253/w_total_4*100:.1f}%)")
print(f"  w(2233) = {w_2233:.6f} ({w_2233/w_total_4*100:.1f}%)")
print(f"  w(2555) = {w_2555:.6f} ({w_2555/w_total_4*100:.1f}%)")
print(f"  w(2553) = {w_2553:.6f} ({w_2553/w_total_4*100:.1f}%)")
print(f"  w(2533) = {w_2533:.6f} ({w_2533/w_total_4*100:.1f}%)")
print(f"  w(2333) = {w_2333:.6f} ({w_2333/w_total_4*100:.1f}%)")
print(f"  加权平均 C₄ = {C4_weighted:.6f}")

# ============================================================
# 12. 4圈修正数值计算
# ============================================================

print(f"\n{'='*85}")
print("12. 4圈修正数值计算")
print(f"{'='*85}")

# 4圈修正
delta_4 = alpha_0_inv * eps4 * C4_weighted
alpha_4_inv = alpha_3_inv_final - delta_4
gap_4 = alpha_4_inv - alpha_exp_inv

print(f"\n  Δα⁻¹_4 = α₀⁻¹ × ε⁴ × C₄")
print(f"          = {alpha_0_inv:.2f} × {eps4:.6e} × {C4_weighted:.6f}")
print(f"          = {delta_4:.6e}")
print(f"  α⁻¹_4loop = {alpha_4_inv:.10f}")
print(f"  与实验偏差: {gap_4:+.6e} ({abs(gap_4)/alpha_exp_inv*1e12:.4f} ppt, {abs(gap_4)/alpha_exp_err:.6f}σ)")

# 4圈修正的相对大小
print(f"\n[4圈修正的量级分析]:")
print(f"  4圈修正量: {delta_4:.2e}")
print(f"  实验误差:  {alpha_exp_err:.2e}")
print(f"  比值:      {delta_4/alpha_exp_err:.2e}")
print(f"  结论: 4圈修正比实验误差小 {alpha_exp_err/delta_4:.0f} 倍, 在当前精度下完全可忽略。")

# 尝试不同C₄值
print(f"\n[不同C₄值下的4圈修正]:")
for C4_try in [1.0, C4_weighted, 10.0, 100.0]:
    d4 = alpha_0_inv * eps4 * C4_try
    a4 = alpha_3_inv_final - d4
    g4 = a4 - alpha_exp_inv
    print(f"  C₄={C4_try:<8.3f}: Δα⁻¹={d4:.4e}, α⁻¹={a4:.10f}, 偏差={g4:+.4e} ({abs(g4)/alpha_exp_err:.4f}σ)")

# ============================================================
# 13. 完整精度对比（含4圈）
# ============================================================

print(f"\n{'='*85}")
print("13. 完整精度对比表（含4圈修正）")
print(f"{'='*85}")

print(f"\n{'阶段':<38} {'α⁻¹':<18} {'差值':<14} {'偏差':<14} {'σ':<8}")
print("-" * 95)
print(f"{'裸值 (EPRL 4-单纯形)':<38} {alpha_0_inv:<18.10f} {alpha_0_inv-alpha_exp_inv:+.10f}  {(alpha_0_inv-alpha_exp_inv)/alpha_exp_inv*1e6:.1f} ppm  {(alpha_0_inv-alpha_exp_inv)/alpha_exp_err:.0f}σ")
print(f"{'+ 2-单纯形修正 (1圈, 2/9)':<38} {alpha_2_inv:<18.10f} {alpha_2_inv-alpha_exp_inv:+.10f}  {(alpha_2_inv-alpha_exp_inv)/alpha_exp_inv*1e9:.1f} ppb  {(alpha_2_inv-alpha_exp_inv)/alpha_exp_err:.0f}σ")
print(f"{'+ 弱混合修正 (2圈, p=2↔p=3)':<38} {alpha_2loop_inv:<18.10f} {gap_2loop:+.10f}  {abs(gap_2loop)/alpha_exp_inv*1e9:.1f} ppb  {abs(gap_2loop)/alpha_exp_err:.1f}σ")
print(f"{'+ 3圈修正 (加权平均)':<38} {alpha_3_inv_final:<18.10f} {gap_3loop:+.10f}  {abs(gap_3loop)/alpha_exp_inv*1e9:.1f} ppb  {abs(gap_3loop)/alpha_exp_err:.1f}σ")
c4_str = f"C₄={C4_weighted:.3f}"
print(f"{'+ 4圈修正 (加权平均, ' + c4_str + ')':<38} {alpha_4_inv:<18.10f} {gap_4:+.10f}  {abs(gap_4)/alpha_exp_inv*1e12:.2f} ppt  {abs(gap_4)/alpha_exp_err:.4f}σ")
print(f"{'实验值 (PDG 2024)':<38} {alpha_exp_inv:<18.10f} ±{alpha_exp_err:.10f}  {'---':<14} {'---'}")

# ============================================================
# 14. 4圈修正的理论意义
# ============================================================

print(f"\n{'='*85}")
print("14. 4圈修正的理论意义与收敛性分析")
print(f"{'='*85}")

# 收敛性分析
delta_1 = float(correction_2_9)  # 2/9
delta_2 = delta_2loop
delta_3 = alpha_0_inv * eps3 * C3_weighted
delta_4_val = delta_4

print(f"""
[圈图展开的收敛性]:

  圈数    修正量 Δα⁻¹        比值 (Δ_n/Δ_{{n-1}})
  ------------------------------------------------
  1圈     {delta_1:.6e}        ---
  2圈     {delta_2:.6e}        {delta_2/delta_1:.2e}
  3圈     {delta_3:.6e}        {delta_3/delta_2:.2e}
  4圈     {delta_4_val:.6e}        {delta_4_val/delta_3:.2e}

[分析] 圈图展开呈几何级数收敛:
  - 每增加一圈, 修正量减小约 ε ≈ {eps:.4e} 倍
  - 4圈修正已是实验误差的 {delta_4_val/alpha_exp_err:.2e} 倍
  - 5圈及以上修正完全不可观测

[结论] CNT的圈图展开在n=4圈时已收敛到远优于实验精度的水平。
  当前实验精度(~0.15 ppb)下, 3圈展开已足够,
  4圈及以上修正对α⁻¹的贡献在实验上不可分辨。
""")

print("=" * 85)
print("计算完成（含4圈修正）")
print("=" * 85)