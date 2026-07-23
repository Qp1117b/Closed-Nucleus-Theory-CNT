#!/usr/bin/env python3
"""
⚠️ 已过时 (2026-07-23 标记): Mathieu-only α_p 路径
===================================================
已被 alpha_p_dual_path.py 替代 (UV: Mathieu 谱比 + IR: 整数壳层双路径)。
保留为推导历史参考。
"""
"""
α_p 第一性推导：从 Mathieu 特征值出发
====================================
核心逻辑链:
  1. CNT 角向 Hamilton = Mathieu 方程: -d²ψ/dθ² + 2q·cos(2θ)ψ = aψ
  2. q_c 由连分数定义 → Mathieu 特征值 a_r(q_c), b_r(q_c) 
  3. 冻结点条件 = 特定谱关系成立
  4. α_p 是谱关系的直接代数推论，非拟合参数
"""
import numpy as np
from scipy.special import mathieu_a, mathieu_b
import mpmath as mp
mp.mp.dps = 50

# ═══ CNT 核心常数 ═══
C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
gamma_1 = mp.zetazero(1).imag
E_1 = 0.25 + gamma_1**2

def tail(q, k, max_depth=50):
    if k > max_depth: return mp.mpf('0')
    n_k = 2*k + 1
    return q**2 / (n_k**2 - 2*q - tail(q, k+1, max_depth))

q_c = float(mp.findroot(lambda q: 1 - 3*q - tail(q, 1, 50), (29 - mp.sqrt(661))/10))
I = 5/3
I_SU2 = 5/2

print('='*67)
print('  α_p 第一性推导: Mathieu 特征值谱分析')
print('='*67)

print(f'\n  q_c = {q_c:.12f}  (冻结点)')
print(f'  2q_c = {2*q_c:.12f}')

# ═══ Mathieu 特征值计算 ═══
print(f'\n  Mathieu 特征值 a_r(q_c) 和 b_r(q_c):')
print(f'  {"r":<4} {"a_r":<16} {"b_{r+1}":<16} {"a_r - b_{r+1}":<16}')
print(f'  {"-"*52}')

# 高精度计算特征值
a_vals = {}
b_vals = {}
for r in range(8):
    a_r = mathieu_a(r, q_c)
    b_r = mathieu_b(r+1, q_c) if r < 7 else 0
    a_vals[r] = a_r
    b_vals[r+1] = b_r
    diff = a_r - b_r if r > 0 else a_r - b_vals[1]
    print(f'  {r:<4} {a_r:<16.10f} {b_r if r<7 else 0:<16.10f} {diff if r<7 else 0:<16.10f}')

# ═══ 关键识别 ═══
print(f'\n{"="*67}')
print(f'  冻结点条件验证')
print(f'='*67)

print(f'\n  b₁(q_c) = {b_vals[1]:.12f}')
print(f'  2·q_c   = {2*q_c:.12f}')
print(f'  b₁ = 2q_c? {(abs(b_vals[1] - 2*q_c) < 1e-10)}')

print(f'\n  a₀(q_c) = {a_vals[0]:.12f}')
print(f'  -q_c²/2 = {-q_c**2/2:.12f}')
print(f'  差       = {abs(a_vals[0] + q_c**2/2):.12f}')

print(f'\n  a₁(q_c) - b₁(q_c) = {a_vals[1] - b_vals[1]:.12f}')
print(f'  b₂(q_c) - a₁(q_c) = {b_vals[2] - a_vals[1]:.12f}')

# ═══ 探索 α_p 与特征值的刚性关系 ═══
emp = {2: 1.547, 3: 0.432, 5: 0.842}

print(f'\n{"="*67}')
print(f'  探索 α_p 的 Mathieu 谱来源')
print(f'='*67)

# α_p 偏差量
print(f'\n  经验 α_p:')
for p, val in emp.items():
    print(f'    α_{p} = {val:.4f}  (偏离 1: {val-1:+.4f})')

# 候选: α_p = 1 + r_p · a_0(q_c)  (r_p 依赖于 p)
print(f'\n  --- 候选 1: α_p = 1 + c_p × a₀ ---')
for p, label in [(2, 'p=2'), (3, 'p=3'), (5, 'p=5')]:
    c_p = (emp[p] - 1) / a_vals[0]
    print(f'    α_{p} = 1 + {c_p:.4f} × a₀  (a₀={a_vals[0]:.6f})  [{label}]')

# 候选: α_p = a_r / s_p  (特征值比值)
print(f'\n  --- 候选 2: 特征值比 ---')
for r in range(1, 6):
    ratio_a = a_vals[r] / a_vals[0] if a_vals[0] != 0 else float('inf')
    print(f'    a_{r}/a₀ = {ratio_a:.4f}')
    print(f'    1 - a₀/a_{r} = {1 - a_vals[0]/a_vals[r]:.4f}')

# 候选: α_p = 1 + β_p × (Mathieu 特征值比)
beta3 = float(mp.mpf(str(lambda_c)) / (12 * mp.mpf(str(I)))) if False else 0.0658011456
print(f'\n  --- 候选 3: 特征指数 ν = √a ---')
for r in range(1, 6):
    nu = np.sqrt(max(0, a_vals[r]))
    print(f'    ν_{r} = √a_{r} = {nu:.6f}')
    print(f'      ν_{r}/p(r) ∝ ?')

# 候选: 从 N_cycle = 30 的结构
print(f'\n  --- 候选 4: N_cycle = 30 结构 ---')
Nc = 30
for d in [2, 3, 5, 6, 10, 15]:
    val = 30/d
    print(f'    30/{d} = {val:.4f}, 1-1/(30/{d}) = {1-1/val:.4f}')

# ═══ 完整谱分析 ═══
print(f'\n{"="*67}')
print(f'  特征值间距分析: 寻找与 α_p 匹配的模式')
print(f'='*67)

# 相邻特征值间距
print(f'\n  a-谱间距:')
deltas_a = [a_vals[r+1] - a_vals[r] for r in range(5)]
for r, d in enumerate(deltas_a):
    print(f'    a_{r+1} - a_{r} = {d:.8f}')

print(f'\n  b-谱间距:')
deltas_b = [b_vals[r+1] - b_vals[r] for r in range(1, 5)]
for r, d in enumerate(deltas_b):
    print(f'    b_{r+2} - b_{r+1} = {d:.8f}')

# 特征值差的对数
print(f'\n  特征值间距/2q_c 比:')
for r, d in enumerate(deltas_a):
    ratio = d / (2*q_c)
    print(f'    (a_{r+1}-a_{r})/(2q_c) = {ratio:.6f}')

# ═══ 稳定带宽度与 β-函数的连接 ═══
print(f'\n{"="*67}')
print(f'  Mathieu 谱 → CNT β-函数的关系')
print(f'='*67)

beta3 = float(mp.mpf('1.316022911308') / (12 * mp.mpf('1.6666666666667')))
beta2 = float(mp.mpf('0.023095708966121') / mp.mpf('2.5'))
beta1 = -float(mp.mpf('0.023095708966121') / mp.mpf('0.329005727827'))

print(f'\n  CNT β-函数:')
print(f'    β₁ = {beta1:.10f}')
print(f'    β₂ = {beta2:.10f}')
print(f'    β₃ = {beta3:.10f}')

# 稳定带宽度
print(f'\n  稳定带/不稳定带宽度:')
bands = []
for r in range(4):
    if r == 0:
        w = abs(a_vals[0] - b_vals[1])  # instability band 1
        print(f'    不稳定带 1: |a₀ - b₁| = {w:.8f}')
    else:
        w1 = abs(b_vals[r] - a_vals[r-1])  # stability band
        w2 = abs(a_vals[r] - b_vals[r])    # instability band
        print(f'    稳定带 {r}: |b_{r} - a_{r-1}| = {w1:.8f}')
        print(f'    不稳定带 {r+1}: |a_{r} - b_{r+1}| = {w2:.8f}')

# 关键检查: 带宽与 β 的关系
print(f'\n  带宽/β 比:')
for r in range(4):
    w_a = abs(a_vals[r+1] - b_vals[r+1]) if r < 3 else 0
    w_b_raw = abs(b_vals[r+1] - a_vals[r]) if r < 4 else 0
    if w_a > 0:
        print(f'    |a_{r+1}-b_{r+1}|/|β₁| = {w_a/abs(beta1):.4f}')
        print(f'    |a_{r+1}-b_{r+1}|/|β₃| = {w_a/beta3:.4f}')
