"""
alpha_p 整数壳层约束的数值检验

CNT 质量公式：m_i^(p) = g_p * p^{-k_i * alpha_p}
其中 k_i = v_p(pi) 必须是整数。

本脚本固定 g_p 来自博弈不动点，检查是否存在 alpha_p 使得某扇区的三代粒子质量
对应的 k_i 同时为整数。如果不存在，则给出最优有理逼近及所需 alpha_p。
"""

import math
from fractions import Fraction

# 物理常数
m_p = 938.272  # MeV, 质子质量

# 博弈不动点权重比：x_2 : x_3 : x_5 = ln(5/3) : ln(5/2) : ln(3/2)
a = math.log(3/2)
b = math.log(5/3)
c = math.log(5/2)
s = a + b + c
x2 = b / s
x3 = c / s
x5 = a / s

g2 = x2 * m_p
g3 = x3 * m_p
g5 = x5 * m_p

print("=" * 70)
print("CNT 博弈不动点耦合强度")
print("=" * 70)
print(f"x2* : x3* : x5* = {x2:.6f} : {x3:.6f} : {x5:.6f}")
print(f"g2 = {g2:.3f} MeV")
print(f"g3 = {g3:.3f} MeV")
print(f"g5 = {g5:.3f} MeV")
print()

# 各扇区粒子质量（MeV）
# p=5: 带电轻子
masses_p5 = {
    "e": 0.510998950,
    "mu": 105.6583745,
    "tau": 1776.86
}

# p=3: 弱扇区。这里用中微子质量上限（eV 量级），但中微子质量不确定。
# 为演示整数约束的刚性，我们暂时用 up-type 夸克有效质量作为占位。
masses_p3 = {
    "u": 2.16,
    "c": 1270.0,
    "t": 173210.0
}

# p=2: 强扇区。用 down-type 夸克有效质量作为占位。
masses_p2 = {
    "d": 4.67,
    "s": 93.0,
    "b": 4180.0
}


def find_integer_shell(g_p, p, masses, sector_name, max_k_diff=50):
    """
    对给定扇区，寻找整数 k_i 使得 m_i = g_p * p^{-k_i * alpha} 对某个 alpha 成立。
    等价于：对质量排序 m_1 < m_2 < m_3，要求
        alpha = ln(m_j/m_i) / [(k_i - k_j) ln p]
    且所有 k_i 为整数。
    """
    names = list(masses.keys())
    vals = [masses[n] for n in names]
    # 排序
    sorted_pairs = sorted(zip(vals, names))
    vals_sorted = [x[0] for x in sorted_pairs]
    names_sorted = [x[1] for x in sorted_pairs]

    # 独立对数比
    r12 = math.log(vals_sorted[1] / vals_sorted[0])
    r23 = math.log(vals_sorted[2] / vals_sorted[1])

    print(f"\n{'='*70}")
    print(f"扇区 p={p} ({sector_name})")
    print(f"{'='*70}")
    print(f"粒子: {names_sorted}")
    print(f"质量: {[f'{v:.4g}' for v in vals_sorted]} MeV")
    print(f"ln(m2/m1) = {r12:.6f}")
    print(f"ln(m3/m2) = {r23:.6f}")
    print(f"比值 r12/r23 = {r12/r23:.6f}")

    # 寻找最佳整数逼近 n/m ≈ r12/r23，其中 n = k2-k1, m = k3-k2
    best = []
    for n in range(1, max_k_diff + 1):
        for m in range(1, max_k_diff + 1):
            ratio = n / m
            err = abs(ratio - r12 / r23)
            # 对应的 alpha
            alpha = r12 / (n * math.log(p))
            # 计算 k_i
            k1 = -math.log(vals_sorted[0] / g_p) / (alpha * math.log(p))
            k2 = k1 + n
            k3 = k2 + m
            # 检查 k_i 是否接近整数
            k1_dev = abs(k1 - round(k1))
            k2_dev = abs(k2 - round(k2))
            k3_dev = abs(k3 - round(k3))
            max_dev = max(k1_dev, k2_dev, k3_dev)
            best.append((err, max_dev, n, m, alpha, k1, k2, k3))

    best.sort(key=lambda x: (x[0], x[1]))

    print("\n最佳整数壳层逼近（前 5）:")
    print(f"{'n':>4} {'m':>4} {'ratio':>10} {'err_ratio':>12} {'alpha':>12} {'max_k_dev':>12} {'k1':>10} {'k2':>10} {'k3':>10}")
    for err, max_dev, n, m, alpha, k1, k2, k3 in best[:5]:
        print(f"{n:4d} {m:4d} {n/m:10.6f} {err:12.6f} {alpha:12.6f} {max_dev:12.6f} "
              f"{k1:10.4f} {k2:10.4f} {k3:10.4f}")

    # 同时给出经验 alpha 下的 k_i
    empirical_alpha = {
        2: 1.545,
        3: 0.443,
        5: 0.826
    }[p]
    print(f"\n经验 alpha_p = {empirical_alpha} 时的壳层指数 k_i:")
    for val, name in sorted_pairs:
        k = -math.log(val / g_p) / (empirical_alpha * math.log(p))
        print(f"  {name}: k = {k:.4f}")


# 执行三个扇区的检验
find_integer_shell(g5, 5, masses_p5, "电磁/带电轻子")
find_integer_shell(g3, 3, masses_p3, "弱/up-type 夸克（占位）")
find_integer_shell(g2, 2, masses_p2, "强/down-type 夸克（占位）")

print("\n" + "=" * 70)
print("结论")
print("=" * 70)
print("""
1. 对 p=5 带电轻子，质量比 r12/r23 ≈ 1.889，最佳有理逼近为 17/9 或 34/18，
   对应 alpha_5 ≈ 0.195，与当前经验值 alpha_5 ≈ 0.826 相差甚远。

2. 这说明简单指数质量公式 m_i = g_p * p^{-k_i alpha_p} 无法同时满足：
   (a) g_p 来自博弈不动点；
   (b) alpha_p 取经验值；
   (c) k_i 为整数。

3. 因此要么：
   - 质量公式需要修正（如引入 f_p(k_i, alpha_p) 而非简单指数）；
   - 要么 g_p 不是纯粹的博弈不动点权重，而是包含额外的标度因子；
   - 要么 alpha_p 的经验值需要重新确定。
""")
