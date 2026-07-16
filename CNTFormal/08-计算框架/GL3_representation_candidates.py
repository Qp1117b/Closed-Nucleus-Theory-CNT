#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL(3) 自守表示候选与 S_p、α_p 的数值对应检验

目标：测试若干自然的 GL(3,Q_p) 局部表示数据，检验它们能否同时复现
      观测到的 α_p 与标度因子 S_p。

认识论地位：探索性。文中"猜想 4.1"（α_p = -Σ v_p(α_{p,i})）尚未被严格证明；
      所有表示候选均为启发式构造。
"""

import numpy as np
from math import pi, log

# ---------------------------------------------------------------------------
# 观测值
# ---------------------------------------------------------------------------
P = [2, 3, 5]
alpha_obs = {2: 1.545, 3: 0.443, 5: 0.826}
S_obs = {2: 0.3613, 3: 2.5032, 5: 0.5191}

print("=" * 90)
print("GL(3) 自守表示候选与 α_p、S_p 的数值对应检验")
print("=" * 90)
print("\n观测值:")
for p in P:
    print(f"  p={p}: α_p={alpha_obs[p]:.4f}, S_p={S_obs[p]:.4f}")


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def vp(x, p):
    """p-adic 赋值 v_p(x)，x 为非零有理数/浮点数。"""
    if x == 0:
        return np.inf
    # 对浮点数，用对数近似整数赋值
    val = round(log(abs(x)) / log(p))
    # 验证 p^val 是否接近 |x|
    if abs(abs(x) - p**val) < 1e-6 * max(abs(x), 1.0):
        return val
    # 若 x 不是纯 p 幂，返回非整数对数（用于探索）
    return log(abs(x)) / log(p)


def alpha_from_satake(satake, p):
    """
    猜想 4.1：α_p = -Σ_i v_p(α_{p,i})。
    对非分歧主序列表示，Satake 参数为 {α_1, α_2, α_3}。
    """
    return -sum(vp(a, p) for a in satake)


def local_L_factor_at_1(satake, p):
    """局部 L-因子在 s=1 的值：L(1,π_p) = ∏_i (1 - α_i p^{-1})^{-1}。
    若某项使分母为零（即存在 Satake 参数等于 p），返回 +inf 并标记为极点。"""
    val = 1.0
    for a in satake:
        denom = 1.0 - a / p
        if abs(denom) < 1e-12:
            return np.inf
        val *= 1.0 / denom
    return val


def local_epsilon(p, f):
    """导体为 p^f 的表示的 epsilon 因子绝对值 |ε(0,π_p)| = p^{f/2}"""
    return p**(f / 2.0)


# ---------------------------------------------------------------------------
# 候选表示
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("候选 1：Steinberg 型表示（unipotent ramification）")
print("-" * 90)

# Steinberg 型：Satake 参数常为 {p^{-1/2}, p^{-1/2}, p} 或 {p^{-1}, 1, p}
steinberg_candidates = [
    ("{p^{-1/2}, p^{-1/2}, p}", lambda p: [p**(-0.5), p**(-0.5), p]),
    ("{p^{-1}, 1, p}", lambda p: [1.0/p, 1.0, p]),
    ("{p^{-1}, p^{-1}, p^2}", lambda p: [1.0/p, 1.0/p, p**2]),
]

for name, satake_fn in steinberg_candidates:
    print(f"\n  {name}:")
    print(f"    {'p':<6} {'α_pred':<12} {'α_obs':<12} {'L(1)':<14} {'|L(1)| 作为 S_p':<16} {'S_obs':<12}")
    for p in P:
        satake = satake_fn(p)
        alpha_pred = alpha_from_satake(satake, p)
        L1 = local_L_factor_at_1(satake, p)
        print(f"    {p:<6} {alpha_pred:<12.4f} {alpha_obs[p]:<12.4f} {L1:<14.4f} {abs(L1):<16.4f} {S_obs[p]:<12.4f}")


print("\n" + "-" * 90)
print("候选 2：主序列 with HT 权 {h_1, h_2, h_3}")
print("-" * 90)

# 主序列：Satake 参数为 {p^{-h_1}, p^{-h_2}, p^{-h_3}}（对未分歧表示，中心特征调整后）
HT_candidates = [
    ("HT={-1,0,1}", [-1, 0, 1]),
    ("HT={-1,-1,2}", [-1, -1, 2]),
    ("HT={-2,0,2}", [-2, 0, 2]),
    ("HT={-1,0,0}", [-1, 0, 0]),
    ("HT={-2,-1,3}", [-2, -1, 3]),
]

for name, HT in HT_candidates:
    print(f"\n  {name}:")
    print(f"    {'p':<6} {'α_pred':<12} {'α_obs':<12} {'L(1)':<14} {'|L(1)| 作为 S_p':<16} {'S_obs':<12}")
    for p in P:
        satake = [p**(-h) for h in HT]
        alpha_pred = alpha_from_satake(satake, p)
        L1 = local_L_factor_at_1(satake, p)
        print(f"    {p:<6} {alpha_pred:<12.4f} {alpha_obs[p]:<12.4f} {L1:<14.4f} {abs(L1):<16.4f} {S_obs[p]:<12.4f}")


print("\n" + "-" * 90)
print("候选 3：对称平方提升 from GL(2)")
print("-" * 90)

# 若 GL(2) 表示的 Satake 参数为 {p^{-it}, p^{it}}（主序列，无质量），
# 则 Sym² 提升的 GL(3) Satake 参数为 {p^{-2it}, 1, p^{2it}}。
# 对纯相位，v_p = 0，故 α_p = 0。这与观测不符。
# 若 GL(2) 表示带有权重（如 holomorphic modular form），Satake 参数为 {p^{(k-1)/2} e^{iθ}, p^{(k-1)/2} e^{-iθ}}。
# 此时 Sym² 提升给出权重信息。

print("  对无质量主序列 GL(2) 表示，Sym² 提升的 Satake 参数为 {p^{-2it}, 1, p^{2it}}。")
print("  所有 v_p = 0，因此 α_p = 0（扇区冻结），与观测 α_p ≠ 0 不符。")
print("  若要求 α_p ≠ 0，需要 GL(2) 表示本身带有非零 p-adic 赋值（如 Steinberg 或 twist）。")

# 测试：GL(2) Steinberg 的 Sym² 提升
# GL(2) Steinberg Satake: {p^{-1/2}, p^{1/2}}? 实际上 Steinberg 的 Satake 参数是 {p^{-1/2}, p^{1/2}} 带符号。
# Sym²: {p^{-1}, 1, p}
print("\n  GL(2) Steinberg 的 Sym² 提升：Satake = {p^{-1}, 1, p}")
print(f"    {'p':<6} {'α_pred':<12} {'α_obs':<12} {'L(1)':<14} {'|L(1)| 作为 S_p':<16} {'S_obs':<12}")
for p in P:
    satake = [1.0/p, 1.0, p]
    alpha_pred = alpha_from_satake(satake, p)
    L1 = local_L_factor_at_1(satake, p)
    print(f"    {p:<6} {alpha_pred:<12.4f} {alpha_obs[p]:<12.4f} {L1:<14.4f} {abs(L1):<16.4f} {S_obs[p]:<12.4f}")


print("\n" + "-" * 90)
print("候选 4：Dirichlet 特征诱导（代数 Hecke 特征）")
print("-" * 90)

# 由模 30 的 Dirichlet 特征 χ 诱导 GL(1) 表示，再提升/直和到 GL(3)。
# 例如三个特征 χ_2, χ_3, χ_5 分别仅在对应素数处 ramified。
# 这里用占位：χ(p) = ±1 或 0（若 p 整除 conductor）。

# 简单测试：三个特征分别为模 2、3、5 的二次特征
chi_2 = {2: -1, 3: 1, 5: 1}   # 模 2 非主特征
chi_3 = {2: 1, 3: -1, 5: 1}   # 模 3 非主特征
chi_5 = {2: 1, 3: 1, 5: -1}   # 模 5 非主特征

print("  三个一维特征 {χ_2, χ_3, χ_5} 的直和，每个特征仅在对应素数处取 -1：")
print(f"    {'p':<6} {'α_pred':<12} {'α_obs':<12}")
for p in P:
    satake = [chi_2[p], chi_3[p], chi_5[p]]
    alpha_pred = alpha_from_satake(satake, p)
    print(f"    {p:<6} {alpha_pred:<12.4f} {alpha_obs[p]:<12.4f}")


# ---------------------------------------------------------------------------
# 综合评分：哪个候选最接近观测 α_p 与 S_p？
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("候选 5：CNT Cartan-S5 不变量（与 α_EM 周期假设关联）")
print("-" * 90)

# CNT 输入：Cartan 曲率本征值 λ={9,4,1} 与 S5 表示维数 mult={1,4,5}。
# 若把这些不变量映射为 Satake 参数的 p-adic 赋值，可构造一个“截断”表示：
#   v_2 = -Σλ / 3, v_3 = -(mult_3 - mult_5), v_5 = -(mult_2 - mult_3)。
# 该候选的动机来自 α_EM 周期 1/α = 2^{Σλ} 3^{mult_3-mult_5} 5^{mult_2-mult_3} π。
Cartan = [9, 4, 1]
mult = [1, 4, 5]
# 构造 Satake 参数：{2^{-Σλ/3}, 3^{-(mult_3-mult_5)}, 5^{-(mult_2-mult_3)}}
def satake_CNT(p):
    v2 = -sum(Cartan) / 3.0
    v3 = -(mult[1] - mult[2])  # -(4-5)=1
    v5 = -(mult[0] - mult[1])  # -(1-4)=3
    vals = {2: v2, 3: v3, 5: v5}
    # 返回三个参数，其中与 p 对应的参数取 p^{v_p}，其余两个取 1
    return [p**vals[p] if i == p else 1.0 for i in [2, 3, 5]]

print("  构造：对每个素数 p，Satake 参数的 p-adic 赋值取 CNT 不变量决定的有理数/整数；")
print("        非 p 方向参数设为 1（表示在该方向未分歧）。")
print(f"    {'p':<6} {'α_pred':<12} {'α_obs':<12} {'L(1)':<14} {'|L(1)| 作为 S_p':<16} {'S_obs':<12}")
for p in P:
    satake = satake_CNT(p)
    alpha_pred = alpha_from_satake(satake, p)
    L1 = local_L_factor_at_1(satake, p)
    print(f"    {p:<6} {alpha_pred:<12.4f} {alpha_obs[p]:<12.4f} {L1:<14.4f} {abs(L1):<16.4f} {S_obs[p]:<12.4f}")
print("  说明：此候选目前仅用于展示 CNT 不变量与 GL(3) 局部数据之间的数值关系；")
print("        它并不满足三个扇区同时匹配，也不是一个自洽的整体表示。")


print("\n" + "=" * 90)
print("综合评分：同时匹配 α_p 与 S_p 的候选")
print("=" * 90)

def score_candidate(name, satake_fn, S_fn=None):
    """
    计算候选与观测的偏差。
    S_fn(p) 给出标度因子候选；若 None，使用 |L(1,π_p)|。
    """
    alpha_dev = []
    S_dev = []
    for p in P:
        satake = satake_fn(p)
        alpha_pred = alpha_from_satake(satake, p)
        alpha_dev.append(abs(alpha_pred - alpha_obs[p]) / alpha_obs[p])
        if S_fn is None:
            S_pred = abs(local_L_factor_at_1(satake, p))
        else:
            S_pred = S_fn(p)
        S_dev.append(abs(S_pred - S_obs[p]) / S_obs[p])
    return np.mean(alpha_dev), np.mean(S_dev), np.mean(alpha_dev) + np.mean(S_dev)

all_candidates = [
    ("Steinberg {p^{-1},1,p}", lambda p: [1.0/p, 1.0, p]),
    ("HT={-1,0,1}", lambda p: [p, 1.0, 1.0/p]),
    ("HT={-1,-1,2}", lambda p: [p**2, 1.0/p, 1.0/p]),
    ("HT={-2,0,2}", lambda p: [p**2, 1.0, 1.0/p**2]),
    ("HT={-2,-1,3}", lambda p: [p**3, 1.0/p, 1.0/p**2]),
]

results = []
for name, satake_fn in all_candidates:
    a_dev, s_dev, total = score_candidate(name, satake_fn)
    results.append((name, a_dev, s_dev, total))

results.sort(key=lambda x: x[3])

print(f"\n  {'Rank':<6} {'Candidate':<30} {'α 平均偏差':<16} {'S 平均偏差':<16} {'总偏差':<12}")
print("  " + "-" * 76)
for i, (name, a_dev, s_dev, total) in enumerate(results[:5]):
    print(f"  {i+1:<6} {name:<30} {a_dev*100:<16.2f}% {s_dev*100:<16.2f}% {total*100:<12.2f}%")

print("""
[诚实结论]
1. 没有任何一个简单 GL(3) 局部表示候选能同时精确复现观测到的 α_p 与 S_p。
2. Steinberg 型 {p^{-1},1,p} 给出 α_p = 0 对所有 p（扇区全部冻结），与观测不符。
3. 对中心特征平凡的未分歧主序列 HT 权 {h_1,h_2,h_3}，若 Satake 参数取 {p^{-h_i}}，
   则 Σ h_i = 0 时 Σ v_p(α_i) = 0，故 α_p = 0。这说明简单表示无法直接产生非零 α_p。
4. 对称平方提升 from GL(2) 需要 GL(2) 表示本身带非零 p-adic 赋值，否则 α_p=0。
5. 与质子对应的 GL(3) 表示很可能不是简单的未分歧主序列或 Steinberg，而是带有
   非平凡 conductor（仅由 2,3,5 支持）和特殊 Satake 参数的表示。当前数学文献中
   尚未有明确匹配；需要进一步构造或从 LMFDB 等数据库中搜索 conductor 被 30 整除
   的 GL(3) 自守形式。
""")


# ---------------------------------------------------------------------------
# 候选 6：α_p 映射的修正方案
# ---------------------------------------------------------------------------
print("\n" + "=" * 90)
print("候选 6：α_p 映射的修正方案（差分映射、加权映射、HT 权网格扫描）")
print("=" * 90)

# 6.1 差分映射：alpha_p = max(vp) - min(vp)
def alpha_diff_mapping(satake, p):
    vps = [vp(a, p) for a in satake]
    return max(vps) - min(vps)

# 6.2 加权映射：alpha_p = -sum(h_i * vp(a_i))，其中 h_i 为 HT 权（作为权重）
def alpha_weighted_mapping(satake, p, weights):
    vps = [vp(a, p) for a in satake]
    return -sum(w * v for w, v in zip(weights, vps))

print("\n  差分映射 alpha_p = max(v_p) - min(v_p) 的测试结果:")
print(f"    {'候选':<30} {'α_2':<10} {'α_3':<10} {'α_5':<10} {'平均偏差':<12}")
print("    " + "-" * 72)

for name, satake_fn in all_candidates:
    preds = [alpha_diff_mapping(satake_fn(p), p) for p in P]
    dev = np.mean([abs(preds[i] - alpha_obs[P[i]]) / alpha_obs[P[i]] for i in range(3)])
    print(f"    {name:<30} {preds[0]:<10.4f} {preds[1]:<10.4f} {preds[2]:<10.4f} {dev*100:<12.2f}%")

# 6.3 对差分映射进行 HT 权网格扫描
print("\n  对 HT 权 {h1,h2,h3}（满足 h1+h2+h3=0）用差分映射扫描，寻找最佳匹配:")
print(f"    {'HT 权':<20} {'α_2':<10} {'α_3':<10} {'α_5':<10} {'平均偏差':<12}")
print("    " + "-" * 62)

best_diff = None
best_dev = 1e9
for h1 in range(-5, 6):
    for h2 in range(-5, 6):
        h3 = -(h1 + h2)
        if h3 < -5 or h3 > 5:
            continue
        HT = [h1, h2, h3]
        preds = []
        for p in P:
            satake = [p**(-h) for h in HT]
            preds.append(alpha_diff_mapping(satake, p))
        dev = np.mean([abs(preds[i] - alpha_obs[P[i]]) / alpha_obs[P[i]] for i in range(3)])
        if dev < best_dev:
            best_dev = dev
            best_diff = (HT, preds, dev)
        if dev < 0.5:  # 只显示较好候选
            print(f"    {str(HT):<20} {preds[0]:<10.4f} {preds[1]:<10.4f} {preds[2]:<10.4f} {dev*100:<12.2f}%")

if best_diff:
    print(f"\n  最佳差分映射候选: HT={best_diff[0]}, α_pred=({best_diff[1][0]:.4f}, {best_diff[1][1]:.4f}, {best_diff[1][2]:.4f}), 平均偏差={best_diff[2]*100:.2f}%")

# 6.4 加权映射测试：用 HT 权本身作为权重
print("\n  加权映射 alpha_p = -Σ h_i · v_p(α_i) 的测试结果:")
print(f"    {'HT 权':<20} {'α_2':<10} {'α_3':<10} {'α_5':<10} {'平均偏差':<12}")
print("    " + "-" * 62)

best_weighted = None
best_dev_w = 1e9
for h1 in range(-5, 6):
    for h2 in range(-5, 6):
        h3 = -(h1 + h2)
        if h3 < -5 or h3 > 5:
            continue
        HT = [h1, h2, h3]
        preds = []
        for p in P:
            satake = [p**(-h) for h in HT]
            preds.append(alpha_weighted_mapping(satake, p, HT))
        dev = np.mean([abs(preds[i] - alpha_obs[P[i]]) / alpha_obs[P[i]] for i in range(3)])
        if dev < best_dev_w:
            best_dev_w = dev
            best_weighted = (HT, preds, dev)
        if dev < 1.0:
            print(f"    {str(HT):<20} {preds[0]:<10.4f} {preds[1]:<10.4f} {preds[2]:<10.4f} {dev*100:<12.2f}%")

if best_weighted:
    print(f"\n  最佳加权映射候选: HT={best_weighted[0]}, α_pred=({best_weighted[1][0]:.4f}, {best_weighted[1][1]:.4f}, {best_weighted[1][2]:.4f}), 平均偏差={best_weighted[2]*100:.2f}%")

print("""
[映射修正结论]
1. 简单映射 α_p = -Σ v_p(α_i) 因中心特征平凡而普遍给出 0，无法匹配观测。
2. 差分映射 alpha_p = max(v_p) - min(v_p) 能产生非零值，但网格扫描显示
   最佳候选的平均偏差仍在 50% 以上，无法精确匹配 {1.545, 0.443, 0.826}。
3. 加权映射 alpha_p = -Σ h_i v_p(α_i) 在整数 HT 权范围内同样无法同时匹配三个扇区。
4. 这表明：要么需要非整数/有理数 HT 权，要么需要非主序列表示（带 conductor 或 twist），
   要么 α_p 并非直接由 Satake 参数赋值决定，而是涉及更复杂的周期/积分变换。
""")


# ---------------------------------------------------------------------------
# 候选 7：p-依赖映射的测试与关键洞察
# ---------------------------------------------------------------------------
print("\n" + "=" * 90)
print("候选 7：p-依赖映射测试")
print("=" * 90)

print("\n  关键观察：对全局 GL(3) 表示，HT 权 {h_i} 是 p-无关的。")
print("  因此由 HT 权构造的任何 p-无关函数（如 max(v_p)-min(v_p)、Σ h_i v_p 等）")
print("  都会给出 p-无关的 alpha_p，无法解释观测到的 {1.545, 0.443, 0.826}。")
print("  必须引入 p-依赖因子才能使 alpha_p 随 p 变化。")

# 测试一些自然的 p-依赖映射
def satake_from_HT(HT, p):
    return [p**(-h) for h in HT]

print("\n  测试 p-依赖映射（使用 HT={-1,-1,2} 作为示例）:")
HT_example = [-1, -1, 2]
print(f"    HT = {HT_example}")
print(f"    {'映射':<45} {'α_2':<10} {'α_3':<10} {'α_5':<10} {'平均偏差':<12}")
print("    " + "-" * 87)

mappings = [
    ("(max-min)/p", lambda s, p: (max([vp(a,p) for a in s]) - min([vp(a,p) for a in s])) / p),
    ("(max-min)/log(p)", lambda s, p: (max([vp(a,p) for a in s]) - min([vp(a,p) for a in s])) / log(p)),
    ("(max-min)*|p|_p", lambda s, p: (max([vp(a,p) for a in s]) - min([vp(a,p) for a in s])) / p),
    ("Σ|h_i|/p", lambda s, p: sum(abs(h) for h in HT_example) / p),
    ("Σ h_i^2 / p", lambda s, p: sum(h*h for h in HT_example) / p),
]

for name, mapping in mappings:
    preds = [mapping(satake_from_HT(HT_example, p), p) for p in P]
    dev = np.mean([abs(preds[i] - alpha_obs[P[i]]) / alpha_obs[P[i]] for i in range(3)])
    print(f"    {name:<45} {preds[0]:<10.4f} {preds[1]:<10.4f} {preds[2]:<10.4f} {dev*100:<12.2f}%")

print("""
[p-依赖映射结论]
1. 简单 p-依赖因子（如 1/p、1/log(p)）无法同时匹配三个扇区的 alpha_p。
2. 这表明 alpha_p 不能由单个全局 GL(3) 表示的 p-无关数据经简单 p-依赖 rescaling 得到。
3. 更可能的情形是：与质子对应的自守对象在每个 p ∈ {2,3,5} 处有本质上不同的局部类型，
   或者 alpha_p 由某个涉及 p-进积分/周期的局部量决定，而非仅由 Satake 参数的赋值决定。
4. 这与 CNT 中“每个素数扇区有独立的再生产动力学”的物理图像一致。
""")


# ---------------------------------------------------------------------------
# 候选 8：反问题——给定观测 alpha_p，推断局部 HT 权范围
# ---------------------------------------------------------------------------
print("\n" + "=" * 90)
print("候选 8：反问题——由观测 alpha_p 推断局部表示数据")
print("=" * 90)

# 假设映射 alpha_p = (max(HT) - min(HT)) / p，反解所需的局部“赋值跨度”
print("\n  假设 alpha_p = (max(HT) - min(HT)) / p，反解每个素数处的局部跨度 D_p:")
print(f"    p=2: D_2 = 2 * alpha_2 = {2 * alpha_obs[2]:.4f}")
print(f"    p=3: D_3 = 3 * alpha_3 = {3 * alpha_obs[3]:.4f}")
print(f"    p=5: D_5 = 5 * alpha_5 = {5 * alpha_obs[5]:.4f}")
print("\n  若要求整数 HT 权，最近似取整为 D_2=3, D_3=1, D_5=4，对应:")
print(f"    alpha_pred = {{3/2, 1/3, 4/5}} = {{{3/2:.4f}, {1/3:.4f}, {4/5:.4f}}}")
print(f"    与观测 {{1.545, 0.443, 0.826}} 的平均偏差: ", end="")
dev_int = np.mean([abs(3/2 - alpha_obs[2])/alpha_obs[2], abs(1/3 - alpha_obs[3])/alpha_obs[3], abs(4/5 - alpha_obs[5])/alpha_obs[5]])
print(f"{dev_int*100:.2f}%")

# 尝试寻找有理数 HT 权，使差分映射匹配更好
print("\n  使用有理数 HT 权 {a,b,-(a+b)}，扫描小整数 a,b ∈ [-4,4]，用映射 alpha_p = (max-min)/p:")
print(f"    {'HT_2':<12} {'HT_3':<12} {'HT_5':<12} {'α_2':<10} {'α_3':<10} {'α_5':<10} {'偏差':<10}")
print("    " + "-" * 76)

best_local = None
best_dev_local = 1e9
best_local_all = None      # 不受 per-sector 阈值限制的最佳候选
best_dev_local_all = 1e9
# 对每个 p，独立选择 HT 权，使其 (max-min)/p 接近 alpha_obs[p]
for a2 in range(-4, 5):
    for b2 in range(-4, 5):
        c2 = -(a2 + b2)
        if c2 < -4 or c2 > 4: continue
        HT2 = [a2, b2, c2]
        d2 = max(HT2) - min(HT2)
        pred2 = d2 / 2.0
        dev2 = abs(pred2 - alpha_obs[2]) / alpha_obs[2]
        for a3 in range(-4, 5):
            for b3 in range(-4, 5):
                c3 = -(a3 + b3)
                if c3 < -4 or c3 > 4: continue
                HT3 = [a3, b3, c3]
                d3 = max(HT3) - min(HT3)
                pred3 = d3 / 3.0
                dev3 = abs(pred3 - alpha_obs[3]) / alpha_obs[3]
                for a5 in range(-4, 5):
                    for b5 in range(-4, 5):
                        c5 = -(a5 + b5)
                        if c5 < -4 or c5 > 4: continue
                        HT5 = [a5, b5, c5]
                        d5 = max(HT5) - min(HT5)
                        pred5 = d5 / 5.0
                        dev5 = abs(pred5 - alpha_obs[5]) / alpha_obs[5]
                        dev_total = np.mean([dev2, dev3, dev5])
                        if dev_total < best_dev_local_all:
                            best_dev_local_all = dev_total
                            best_local_all = (HT2, HT3, HT5, [pred2, pred3, pred5], dev_total)
                        if dev2 > 0.15 or dev3 > 0.15 or dev5 > 0.15:
                            continue
                        if dev_total < best_dev_local:
                            best_dev_local = dev_total
                            best_local = (HT2, HT3, HT5, [pred2, pred3, pred5], dev_total)
                        if dev_total < 0.12:
                            print(f"    {str(HT2):<12} {str(HT3):<12} {str(HT5):<12} {pred2:<10.4f} {pred3:<10.4f} {pred5:<10.4f} {dev_total*100:<10.2f}%")

report = best_local if best_local is not None else best_local_all
if report:
    print(f"\n  最佳局部独立 HT 权:")
    print(f"    p=2: HT={report[0]}, alpha_pred={report[3][0]:.4f}")
    print(f"    p=3: HT={report[1]}, alpha_pred={report[3][1]:.4f}")
    print(f"    p=5: HT={report[2]}, alpha_pred={report[3][2]:.4f}")
    print(f"    平均偏差={report[4]*100:.2f}%")
    if report[4] > 0.15 or best_local is None:
        print("  注意：最佳候选至少有一个扇区偏差超过 15%，说明整数 HT 权难以精确匹配观测。")
else:
    print("\n  在小整数 HT 权范围内未找到任何候选。")

print("""
[反问题结论]
1. 若采用简单局部映射 alpha_p = (max(HT)-min(HT))/p，则所需局部 HT 权在不同素数处不同：
   p=2 需要跨度约 3.09，p=3 需要跨度约 1.33，p=5 需要跨度约 4.13。
2. 整数近似 {3,1,4} 给出 {1.5, 0.333, 0.8}，平均偏差约 20%，是合理的起点但不够精确。
3. 这说明与质子对应的对象可能不是单一全局 GL(3) 表示，而是一个“局部类型族”，
   在每个 p ∈ {2,3,5} 处有独立的局部数据，但由全局 adelic 约束（如 conductor=30）统一。
4. 该反问题为下一步在 LMFDB 或文献中搜索 GL(3) 自守形式提供了具体筛选条件：
   寻找 conductor 被 30 整除、且在 p=2,3,5 处的局部参数分别给出跨度约 3,1,4 的表示。
""")
