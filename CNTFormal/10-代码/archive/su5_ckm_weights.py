#!/usr/bin/env python3
"""
⚠️ 关键负结果: SU(5) 权重内积 = 单位矩阵 (纯群论无 CKM 混合)
=============================================================
CKM 混合必须来自 SU(5) 破缺效应 (24_H 混合 + RG 运行)，
非纯 SU(5) 表示论。保留为群论证据。
"""
"""
CNT CKM 从 SU(5) × SU(5) 双卷积：正确权重映射
================================================
核心结构:
  (10,1)_L ⊗ (1,10)_R → 5_H   (上型)
  (10,1)_L ⊗ (1,5̅)_R → 5_H   (下型)
  
  CKM = V_u^† V_d, 其中 V_u, V_d 来自左-handed 扇区 (10,1) 的权重交叠。
  
  三世代对应 10 表示中 (3,2)(1/6) 子空间的三个权重。

SU(5) 10 表示的 (3,2)(1/6) 分量:
  w2 = e₁+e₄ = (3,2)(1/6)  ← gen1 (prime 2)
  w3 = e₁+e₅ = (3,2)(1/6)  ← not used (对应 5→1 分支)
  w5 = e₂+e₄ = (3,2)(1/6)  ← gen2 (prime 3)
  w6 = e₂+e₅ = (3,2)(1/6)
  w7 = e₃+e₄ = (3,2)(1/6)  ← gen3 (prime 5)
  w8 = e₃+e₅ = (3,2)(1/6)
"""
import numpy as np

# 10 表示的权重 (在 eᵢ 基中)
weights_10 = []
for i in range(4):
    for j in range(i+1, 5):
        w = np.zeros(5)
        w[i] = 1
        w[j] = 1
        weights_10.append(w)

# 5̅ 表示的权重
weights_5bar = []
for i in range(5):
    w = np.zeros(5)
    w[i] = -1
    weights_5bar.append(w)

def Y(w):
    return -(w[0]+w[1]+w[2])/3 + (w[3]+w[4])/2

print("="*65)
print("SU(5) 10 表示: (3,2)(1/6) 子空间 = 左-handed 夸克")
print("="*65)
print(f"  {'idx':<4} {'权重':<24} {'SU(3)':<6} {'SU(2)':<6} {'U(1)':<8}")
for i, w in enumerate(weights_10):
    w_str = f"({w[0]:+.0f},{w[1]:+.0f},{w[2]:+.0f},{w[3]:+.0f},{w[4]:+.0f})"
    # SU(3) 标签
    su3_ones = sum(w[:3])
    if su3_ones == 2: su3_l = "3̅"
    elif su3_ones == 1: su3_l = "3"
    else: su3_l = "1"
    su2_ones = sum(w[3:])
    su2_l = f"{int(su2_ones+1)}" if su2_ones > 0 else "1"
    y_val = Y(w)
    print(f"  w{i:<2} {w_str:<24} {su3_l:<6} {su2_l:<6} {y_val:+.3f}")

# 世代到权重的正确映射
# 三世代对应三个不同 prime: gen1→p=2, gen2→p=3, gen3→p=5
# 权重选择: 用前三个 eᵢ 中的两个 e_idx_i + e_4 (SU(2) 上分量)
# 使得 SU(3) 量子数区分三代

# 映射规则: gen_i → w = e_i + e₄ (i=1,2,3)
gen_weights_10 = {
    'u': 2,  # gen1 (p=2): e₁+e₄ = w2
    'c': 5,  # gen2 (p=3): e₂+e₄ = w5
    't': 7,  # gen3 (p=5): e₃+e₄ = w7
}

gen_weights_5bar = {
    'd': 0,  # gen1 (p=2): -e₁
    's': 1,  # gen2 (p=3): -e₂
    'b': 2,  # gen3 (p=5): -e₃
}

print("\n" + "="*65)
print("世代 → SU(5) 权重映射")
print("="*65)
print(f"\n  上型 (在 10 的 (3,2) 分量中):")
for name, wi in gen_weights_10.items():
    w = weights_10[wi]
    print(f"    {name}: gen{['u','c','t'].index(name)+1} → w{wi} = {w} (Y={Y(w):+.3f})")

print(f"\n  下型 (在 5̅ 的 (3̅,1) 分量中, 右手):")
for name, wi in gen_weights_5bar.items():
    w = weights_5bar[wi]
    print(f"    {name}: gen{['d','s','b'].index(name)+1} → w{wi} = {w} (Y={Y(w):+.3f})")

# ═══════════════════════════════════════════════════════════════
# CKM 从左-handed 扇区的权重交叠
# ═══════════════════════════════════════════════════════════════
# 左-handed 上型和下型夸克在同一 10 表示中
# CKM_{ij} = (10 中上型 gen i 的权重) · (10 中下型 gen j 的权重)
# 但下型左-handed 夸克 = 10 表示中与上型不同的权重

# 实际上在 10 的 (3,2)(1/6) 中有 6 个权重
# 3 个给上型 (+2/3 电荷), 3 个给下型 (-1/3 电荷)
# 它们由 SU(3) 色量子数和 SU(2) 同位旋量子数的组合区分

print("\n" + "="*65)
print("CKM = 上型 · 下型 权重内积矩阵")
print("="*65)

# 在 SU(5) 双卷积中, CKM 来自左-handed (10,1) 的权重交叠
# 上型 gen i 对应权重 w_i^{(up)} = e_i + e₄
# 下型 gen j 对应权重 w_j^{(down)} = e_j + e₅
# 
# 权重内积: ⟨w_i|w_j⟩ = w_i · w_j (在 ℝ⁵ 中)
# CKM_{ij} ∝ w_i · w_j 的归一化

# 下型在 10 表示中的左-handed 权重
down_weights_10 = {
    'd': 3,  # gen1: e₁+e₅ = w3
    's': 6,  # gen2: e₂+e₅ = w6
    'b': 8,  # gen3: e₃+e₅ = w8
}

print(f"\n  左-handed 下型 (在 10 的 (3,2) 分量中):")
for name, wi in down_weights_10.items():
    w = weights_10[wi]
    print(f"    {name}: gen{['d','s','b'].index(name)+1} → w{wi} = {w} (Y={Y(w):+.3f})")

# CKM 矩阵
up_names = ['u', 'c', 't']
down_names = ['d', 's', 'b']

print(f"\n  权重内积矩阵 M_ij = w_u(i) · w_d(j):")
M = np.zeros((3, 3))
for i, name_u in enumerate(up_names):
    for j, name_d in enumerate(down_names):
        w_u = weights_10[gen_weights_10[name_u]]
        w_d = weights_10[down_weights_10[name_d]]
        M[i,j] = np.dot(w_u, w_d)

# 打印
header = "  " + "".join([f"  {name:<8}" for name in down_names])
print(header)
for i, name_u in enumerate(up_names):
    row = f"  {name_u:<4}"
    for j in range(3):
        row += f"  {M[i,j]:+.0f}      "
    print(row)

# 归一化: 使最大元素为 1
print(f"\n  归一化后 (最大元素 = 1):")
M_norm = M / np.max(np.abs(M))
print(header)
for i, name_u in enumerate(up_names):
    row = f"  {name_u:<4}"
    for j in range(3):
        row += f"  {M_norm[i,j]:+.3f}   "
    print(row)

# 加入 p-adic 壳层因子
print(f"\n{'='*65}")
print("加入 p-adic 壳层因子")
print("壳层因子 = p^{k_i(1-α_p)} / normalization")
print('='*65)

# 壳层数据
k_up = {'u': -10, 'c': 0, 't': 8}
k_down = {'d': 8, 's': 0, 'b': -10}
k_down_L = {'d': 0, 's': 0, 'b': 0}  # 左-handed 下型壳层待定

α3 = 0.430377  # IR α₃ (上型)
α2 = 1.544317  # IR α₂ (下型)

# 壳层权重因子
def w_p(k, alpha):
    return 2**(k*(1-alpha))  # p=2 为主, 也可用 3-adic

print(f"\n  壳层因子 = 2^{{k(1-α)}}:")
print(f"  {'':<8} {'k_u':<8} {'2^{k(1-α₃)}':<14} {'k_d':<8} {'2^{k(1-α₂)}':<14}")
for i, name_u in enumerate(up_names):
    ku = k_up[name_u]
    fu = 2**(ku*(1-α3))
    kd = k_down[down_names[i]]
    fd = 2**(kd*(1-α2))
    print(f"  gen{i+1}: {ku:<+4}     {fu:<14.6e} {kd:<+4}     {fd:<14.6e}")

# 完整 CKM: 权重内积 + 壳层因子
# V_{ij} = M_{ij} · sqrt(shell_factor_i · shell_factor_j) / normalization
print(f"\n  完整 CKM 模型 (内积 × 壳层):")
V = np.zeros((3, 3))
for i, name_u in enumerate(up_names):
    for j, name_d in enumerate(down_names):
        w_u = weights_10[gen_weights_10[name_u]]
        w_d = weights_10[down_weights_10[name_d]]
        overlap = np.dot(w_u, w_d)
        # 壳层: 用上下壳层的 p-adic 调和平均
        ku = k_up[name_u]
        kd = k_down[down_names[j]]
        shell_factor = 2**(-abs(ku-kd)/10)  # 壳层差的 p-adic 抑制
        V[i,j] = overlap * shell_factor

# 归一化
V_norm = np.abs(V) / np.max(np.abs(V))

print(header)
for i, name_u in enumerate(up_names):
    row = f"  {name_u:<4}"
    for j in range(3):
        row += f"  {V_norm[i,j]:.4f}   "
    print(row)

# 与实验对比
V_exp = {
    'ud': 0.974, 'us': 0.225, 'ub': 0.0037,
    'cd': 0.225, 'cs': 0.973, 'cb': 0.041,
    'td': 0.009, 'ts': 0.040, 'tb': 0.999
}
print(f"\n  与实验对比:")
print(f"  {'|V_{ij}|':<10} {'CNT':<10} {'实验':<10} {'偏差':<10}")
for i, nu in enumerate(up_names):
    for j, nd in enumerate(down_names):
        key = nu+nd
        cnt = V_norm[i,j]
        exp = V_exp[key]
        dev = (cnt/exp - 1)*100
        print(f"  |V_{nu}{nd}|     {cnt:.4f}    {exp:.4f}    {dev:+.1f}%")
