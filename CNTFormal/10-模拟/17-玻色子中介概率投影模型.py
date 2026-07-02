"""
玻色子中介概率投影模型
========================

核心洞察：
  1. 支撑母轨迹投影的再生产中介——玻色子——具有概率性
  2. 玻色子的量子本性导致 RG 投影是概率性的"测量"，而非确定性的连续演化
  3. 母轨迹再生产频率 ν_M = m_p/h ≈ 2.27×10²³ Hz（质子 Compton 频率）
  
物理图像：
  母轨迹 → 玻色子中介 → 规范力投影
  
  - 玻色子是"测量仪器"：胶子、W/Z、光子
  - 母轨迹是"量子态"：在 3 维规范空间中演化
  - 投影是"测量结果"：在质数幂处，特定玻色子"测量"母轨迹
  
  玻色子概率性 → 投影概率性 → 耦合常数的统计本质
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, platform

if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 物理常数
# ============================================================
m_p = 938.272  # MeV
h = 4.135667696e-21  # MeV·s
c = 2.99792458e8  # m/s

nu_M = m_p / h  # Hz
T_M = 1.0 / nu_M  # s
T_cycle = 30 * T_M  # s

N_CYCLE = 30
GAUGE_PRIMES = [2, 3, 5]

# ============================================================
# 第一部分：母轨迹频率
# ============================================================

print("=" * 70)
print("母轨迹再生产频率")
print("=" * 70)

print(f"""
  质子质量: m_p = {m_p} MeV
  普朗克常数: h = {h} MeV·s
  
  母轨迹频率: ν_M = m_p/h = {nu_M:.3e} Hz
  母轨迹周期: T_M = 1/ν_M = {T_M:.3e} s
  完整循环周期: T_cycle = 30 × T_M = {T_cycle:.3e} s
  
  对应能量: E_M = hν_M = m_p = {m_p} MeV (质子静能)
  
  物理意义: 质子每 T_M ≈ 4.4×10⁻²⁴ s 完成一次再生产
           30 次再生产 = 一个完整规范力循环
           循环频率 ν_cycle = ν_M/30 = {nu_M/30:.3e} Hz
""")

# ============================================================
# 第二部分：玻色子作为测量中介
# ============================================================

print("=" * 70)
print("玻色子中介：规范力的概率性根源")
print("=" * 70)

# 玻色子属性
bosons = {
    'SU(3)': {
        'name': '胶子 (gluon)',
        'count': 8,
        'mass': 0.0,  # MeV
        'prime': 2,
        'color': '#2196F3',
        'description': '8种无质量色荷载体，自相互作用 → 渐近自由'
    },
    'SU(2)': {
        'name': 'W±, Z',
        'count': 3,
        'mass': 80.4e3,  # MeV (W质量)
        'prime': 3,
        'color': '#4CAF50',
        'description': '3种有质量弱荷载体，自发破缺 → 短程力'
    },
    'U(1)': {
        'name': '光子 (photon)',
        'count': 1,
        'mass': 0.0,  # MeV
        'prime': 5,
        'color': '#FF9800',
        'description': '1种无质量电荷载体，无自相互作用 → 长程力'
    }
}

for key, b in bosons.items():
    print(f"  {key} (p={b['prime']}): {b['name']}")
    print(f"    数量: {b['count']} 种  质量: {b['mass']} MeV")
    print(f"    {b['description']}")
    print()

# 关键洞察：玻色子数量与坍缩次数的关系
print("  玻色子数量与坍缩次数的对应:")
print(f"    SU(3): 8 种胶子 ↔ 4 次坍缩 (k=2,4,8,16)")
print(f"    SU(2): 3 种玻色子 ↔ 3 次坍缩 (k=3,9,27)")
print(f"    U(1): 1 种光子   ↔ 2 次坍缩 (k=5,25)")
print(f"    比值: 8:3:1 ≈ 坍缩次数比 4:3:2")
print(f"    注意: 不是精确对应，但方向一致——更多玻色子 → 更多坍缩")


# ============================================================
# 第三部分：概率投影模型
# ============================================================

print("\n" + "=" * 70)
print("概率投影模型：玻色子测量母轨迹")
print("=" * 70)

# 每次坍缩的概率由 von Mangoldt 相位决定
# 在 k = p^m 处，玻色子类型 p 以概率 P(p,m) 测量母轨迹

def projection_probability(p, m, n_bosons):
    """
    玻色子 p 在第 m 阶坍缩处的测量概率。
    
    概率 = 基础概率 + 玻色子数量修正
    
    基础概率 ∝ log(p) (von Mangoldt 相位)
    修正: 正比于玻色子数量 n_bosons
    """
    base = np.log(p)  # 基础概率 = von Mangoldt 相位
    # 高阶泛音概率递减: 1/m
    # 玻色子数量修正: 玻色子越多，测量越频繁
    return base / m

def simulate_one_cycle(random_seed=None):
    """
    模拟一个完整循环 (k=1 到 30) 的投影过程。
    
    每一步非零 von Mangoldt 相位处，玻色子以概率
    P = log(p)/m 测量母轨迹，导致该方向的投影坍缩。
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # 轨迹状态: [g_SU3, g_SU2, g_U1]
    g = np.ones(3)  # 统一初始值
    g_history = [g.copy()]
    
    # 玻色子类型映射
    prime_to_idx = {2: 0, 3: 1, 5: 2}
    
    # 累积测量次数
    measurements = {2: 0, 3: 0, 5: 0}
    
    for k in range(1, N_CYCLE + 1):
        g_new = g.copy()
        
        # 检查是否为质数幂
        for p in GAUGE_PRIMES:
            m = 1
            while p**m <= k:
                if p**m == k:
                    # 玻色子 p 以概率 log(p)/m 测量
                    prob = np.log(p) / m
                    if np.random.random() < prob:
                        # 测量成功：该方向坍缩
                        idx = prime_to_idx[p]
                        g_new[idx] += np.log(p)  # 坍缩强度 = log(p)
                        measurements[p] += 1
                m += 1
        
        g = g_new
        g_history.append(g.copy())
    
    return np.array(g_history), measurements

# 多次模拟
n_simulations = 10000
all_measurements = {2: [], 3: [], 5: []}
all_final = []

for i in range(n_simulations):
    g_hist, meas = simulate_one_cycle(random_seed=i)
    for p in GAUGE_PRIMES:
        all_measurements[p].append(meas[p])
    all_final.append(g_hist[-1])

all_final = np.array(all_final)

print(f"  {n_simulations} 次模拟的结果:")
print(f"\n  期望测量次数 (理论值):")
for p in GAUGE_PRIMES:
    expected = 0
    m = 1
    terms = []
    while p**m <= N_CYCLE:
        prob = np.log(p) / m
        expected += prob
        terms.append(f"log({p})/{m}={prob:.4f}")
        m += 1
    print(f"    p={p}: E[测量次数] = {' + '.join(terms)} = {expected:.4f}")

print(f"\n  模拟测量次数 (n={n_simulations}):")
for p in GAUGE_PRIMES:
    avg = np.mean(all_measurements[p])
    std = np.std(all_measurements[p])
    print(f"    p={p}: {avg:.4f} ± {std:.4f}")

print(f"\n  最终耦合常数 (模拟平均):")
print(f"    SU(3): g = {np.mean(all_final[:, 0]):.4f} ± {np.std(all_final[:, 0]):.4f}")
print(f"    SU(2): g = {np.mean(all_final[:, 1]):.4f} ± {np.std(all_final[:, 1]):.4f}")
print(f"    U(1):  g = {np.mean(all_final[:, 2]):.4f} ± {np.std(all_final[:, 2]):.4f}")

# 耦合常数比值
g_mean = np.mean(all_final, axis=0)
ratio = g_mean / g_mean[0]
print(f"\n  耦合常数比值 (SU(3)=1):")
print(f"    SU(3):SU(2):U(1) = 1:{ratio[1]:.4f}:{ratio[2]:.4f}")

# 方差分析：耦合常数的概率分布
print(f"\n  耦合常数方差 (概率性度量):")
print(f"    SU(3): σ² = {np.var(all_final[:, 0]):.6f}")
print(f"    SU(2): σ² = {np.var(all_final[:, 1]):.6f}")
print(f"    U(1):  σ² = {np.var(all_final[:, 2]):.6f}")

# ============================================================
# 第四部分：玻色子属性与耦合常数的关系
# ============================================================

print("\n" + "=" * 70)
print("玻色子属性与耦合常数")
print("=" * 70)

# 玻色子维度: SU(3)=8, SU(2)=3, U(1)=1
# 玻色子质量: 胶子=0, W/Z=80.4GeV, 光子=0
# 玻色子自相互作用: 胶子有, W/Z有, 光子无

print("""
  三层结构:
  
  1. 质数层级: p=2,3,5 决定"何时"坍缩
  2. 玻色子层级: 胶子/W/Z/光子 决定"如何"坍缩  
  3. 耦合常数: 坍缩的统计平均 决定"强度"
  
  核心关系:
    耦合常数 = f(质数, 玻色子数量, 玻色子质量)
    
  候选假说:
    α_p ∝ (玻色子数量 × 坍缩次数) / (质数 × 总坍缩强度)
    
    SU(3): 8 × 4 / (2 × 1.444) = 11.09
    SU(2): 3 × 3 / (3 × 2.014) = 1.49
    U(1):  1 × 2 / (5 × 2.414) = 0.166
    
    比值: 11.09 : 1.49 : 0.166 ≈ 66.8 : 8.98 : 1
    
    与 SM 比值 (6.97 : 2.00 : 1) 比较:
    - SU(3) 过大 (66.8 vs 6.97)
    - 说明玻色子数量的影响是亚线性的
    
  修正: α_p ∝ (log(玻色子数量) × 坍缩次数) / (质数 × 总坍缩强度)
    
    SU(3): log(8) × 4 / (2 × 1.444) = 2.079 × 4 / 2.888 = 2.879
    SU(2): log(3) × 3 / (3 × 2.014) = 1.099 × 3 / 6.042 = 0.545
    U(1):  log(1) × 2 / (5 × 2.414) = 0
    
    比值: 2.879 : 0.545 : 0 → 玻色子数量为1时为零，不合理

  问题: 玻色子数量与耦合常数的关系不是简单的线性或对数关系。
       需要更深入的理论（可能涉及表示论中的 Casimir 不变量）。
""")


# ============================================================
# 可视化
# ============================================================

fig = plt.figure(figsize=(16, 10))

# 图1: 母轨迹频率层级
ax1 = fig.add_subplot(2, 3, 1)
freqs = [nu_M, nu_M/N_CYCLE]
labels = ['ν_M (母轨迹)', 'ν_cycle (循环)']
colors = ['#2196F3', '#FF5722']
bars = ax1.bar(labels, freqs, color=colors, alpha=0.7)
ax1.set_yscale('log')
ax1.set_ylabel('频率 (Hz)')
ax1.set_title('再生产频率层级')
for bar, val in zip(bars, freqs):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.2,
             f'{val:.2e}', ha='center', fontsize=8)

# 图2: 玻色子属性
ax2 = fig.add_subplot(2, 3, 2)
boson_counts = [8, 3, 1]
boson_labels = ['SU(3)\n胶子×8', 'SU(2)\nW/Z×3', 'U(1)\n光子×1']
boson_colors = ['#2196F3', '#4CAF50', '#FF9800']
bars = ax2.bar(boson_labels, boson_counts, color=boson_colors, alpha=0.7)
ax2.set_ylabel('玻色子种类数')
ax2.set_title('规范玻色子')
for bar, val in zip(bars, boson_counts):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             str(val), ha='center', fontsize=12)

# 图3: 坍缩次数 vs 玻色子数量
ax3 = fig.add_subplot(2, 3, 3)
collapse_counts = [4, 3, 2]  # SU(3), SU(2), U(1) 的坍缩次数
ax3.scatter(boson_counts, collapse_counts, c=boson_colors, s=200, zorder=5)
ax3.set_xlabel('玻色子种类数')
ax3.set_ylabel('坍缩次数 (k≤30)')
ax3.set_title('玻色子数量 vs 坍缩次数')
for i, (x, y) in enumerate(zip(boson_counts, collapse_counts)):
    ax3.annotate(boson_labels[i].replace('\n', ' '), (x, y),
                textcoords="offset points", xytext=(10, 10), fontsize=8)
ax3.grid(True, alpha=0.3)

# 图4: 概率投影 — 多次模拟的最终耦合分布
ax4 = fig.add_subplot(2, 3, 4)
for i, (label, color) in enumerate(zip(
    ['SU(3) (p=2)', 'SU(2) (p=3)', 'U(1) (p=5)'],
    ['#2196F3', '#4CAF50', '#FF9800']
)):
    ax4.hist(all_final[:, i], bins=50, alpha=0.5, color=color, label=label, density=True)
ax4.set_xlabel('耦合常数 g')
ax4.set_ylabel('概率密度')
ax4.set_title(f'耦合常数概率分布 (n={n_simulations})')
ax4.legend(fontsize=8)

# 图5: 测量次数分布
ax5 = fig.add_subplot(2, 3, 5)
for p, color in zip(GAUGE_PRIMES, ['#2196F3', '#4CAF50', '#FF9800']):
    meas = np.array(all_measurements[p])
    # 计算每个可能值的频率
    values, counts = np.unique(meas, return_counts=True)
    ax5.bar(values + (p-3)*0.1, counts/n_simulations, width=0.2, 
            color=color, alpha=0.7, label=f'p={p}')
ax5.set_xlabel('测量次数')
ax5.set_ylabel('频率')
ax5.set_title('玻色子测量次数分布')
ax5.legend(fontsize=8)

# 图6: 3D 轨迹 (单次模拟)
ax6 = fig.add_subplot(2, 3, 6, projection='3d')
g_single, _ = simulate_one_cycle(random_seed=42)
ax6.plot(g_single[:, 0], g_single[:, 1], g_single[:, 2], 'k-', linewidth=1, alpha=0.7)
ax6.scatter([g_single[0, 0]], [g_single[0, 1]], [g_single[0, 2]], 
           c='green', s=100, marker='o', label='k=0')
ax6.scatter([g_single[-1, 0]], [g_single[-1, 1]], [g_single[-1, 2]], 
           c='red', s=100, marker='s', label='k=30')
ax6.set_xlabel('SU(3)')
ax6.set_ylabel('SU(2)')
ax6.set_zlabel('U(1)')
ax6.set_title('单次模拟的3D轨迹')
ax6.legend(fontsize=8)

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, '17-玻色子中介概率投影.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n图表已保存: 17-玻色子中介概率投影.png")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 70)
print("核心结论")
print("=" * 70)

print(f"""
1. 母轨迹频率
   ν_M = m_p/h = {nu_M:.3e} Hz
   T_M = 1/ν_M = {T_M:.3e} s
   T_cycle = 30 × T_M = {T_cycle:.3e} s
   
   这是质子的 Compton 频率。质子每 4.4×10⁻²⁴ s 完成一次再生产，
   30 次再生产 = 一个完整规范力循环。

2. 玻色子中介 → 概率性投影
   三种规范力的玻色子（胶子×8, W/Z×3, 光子×1）是母轨迹的"测量仪器"。
   玻色子的量子本性 → 投影是概率性的 → 耦合常数是统计量。
   
   在质数幂 k = p^m 处，玻色子类型 p 以概率 P = log(p)/m 测量母轨迹。
   测量成功 → 该方向的耦合常数发生坍缩跳跃。

3. 为什么耦合常数有统计方差？
   因为每次循环的坍缩次数是随机的（概率性测量）。
   耦合常数是多次循环的统计平均，具有固有的量子不确定性。
   
4. 连续 RG 流的本质
   连续 RG 流 = 离散坍缩在多次循环平均下的粗粒化极限。
   β 函数描述的是"平均坍缩速率"，不是确定性的微分方程。
""")