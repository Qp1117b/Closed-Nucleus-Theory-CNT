"""
统计投影的收敛：从概率坍缩到确定轨迹
========================================

核心问题：
  每次循环的投影是概率性的，但经过足够多次循环，
  统计平均会收敛到一条确定的轨迹。

关键数字：
  ν_M = 2.27×10²³ Hz
  ν_cycle = ν_M/30 = 7.56×10²¹ Hz
  
  在 1 秒内，质子完成 7.56×10²¹ 次完整循环。
  根据大数定律，统计方差 ∝ 1/√N ≈ 10⁻¹¹。
  
  在宏观时间尺度上，统计轨迹是精确确定的。
  
  这与量子力学完全一致：
  - 单次测量：概率性的
  - 期望值：确定性的
  - 宏观观测：由期望值决定
"""

import numpy as np
import matplotlib.pyplot as plt
import os, platform

if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 常数
# ============================================================
m_p = 938.272  # MeV
h = 4.135667696e-21  # MeV·s
nu_M = m_p / h  # Hz
nu_cycle = nu_M / 30  # Hz
N_CYCLE = 30
GAUGE_PRIMES = [2, 3, 5]

# ============================================================
# 收敛分析
# ============================================================

print("=" * 70)
print("统计投影的收敛速度")
print("=" * 70)

# 不同时间尺度下的循环次数
time_scales = {
    '1 ns (10⁻⁹ s)': 1e-9,
    '1 μs (10⁻⁶ s)': 1e-6,
    '1 ms (10⁻³ s)': 1e-3,
    '1 s': 1.0,
    '1 分钟': 60.0,
    '1 小时': 3600.0,
    '1 天': 86400.0,
}

print(f"\n  母轨迹频率: ν_M = {nu_M:.3e} Hz")
print(f"  循环频率: ν_cycle = {nu_cycle:.3e} Hz")
print(f"\n  不同时间尺度下的循环次数和统计精度:")
print(f"  {'时间尺度':<20s} {'循环次数':<15s} {'σ/μ (相对误差)':<20s} {'精度'}")
print(f"  {'-'*70}")

for label, t in time_scales.items():
    n_cycles = nu_cycle * t
    rel_error = 1.0 / np.sqrt(n_cycles)
    if rel_error < 1e-15:
        precision = "精确 (数值极限)"
    elif rel_error < 1e-12:
        precision = "超高精度"
    elif rel_error < 1e-9:
        precision = "极高精度"
    elif rel_error < 1e-6:
        precision = "高精度"
    elif rel_error < 1e-3:
        precision = "中等精度"
    else:
        precision = "低精度"
    print(f"  {label:<20s} {n_cycles:<15.2e} {rel_error:<20.2e} {precision}")

# ============================================================
# 模拟：多次循环的平均轨迹收敛
# ============================================================

def simulate_one_cycle(random_seed=None):
    """模拟一个完整循环的投影过程。"""
    if random_seed is not None:
        np.random.seed(random_seed)
    
    g = np.ones(3)
    g_history = np.zeros((N_CYCLE + 1, 3))
    g_history[0] = g.copy()
    
    prime_to_idx = {2: 0, 3: 1, 5: 2}
    
    for k in range(1, N_CYCLE + 1):
        for p in GAUGE_PRIMES:
            m = 1
            while p**m <= k:
                if p**m == k:
                    prob = np.log(p) / m
                    if np.random.random() < prob:
                        idx = prime_to_idx[p]
                        g[idx] += np.log(p)
                m += 1
        g_history[k] = g.copy()
    
    return g_history

# 模拟 N 次循环，取平均
n_total = 100000
print(f"\n\n  模拟 {n_total} 次循环，观察平均轨迹收敛...")

# 分批计算平均
batch_sizes = [1, 10, 100, 1000, 10000, n_total]
results = {}

for batch_size in batch_sizes:
    # 用 batch_size 次循环计算平均
    avg_traj = np.zeros((N_CYCLE + 1, 3))
    for i in range(batch_size):
        traj = simulate_one_cycle(random_seed=i)
        avg_traj += traj
    avg_traj /= batch_size
    results[batch_size] = avg_traj

# 计算最终收敛轨迹 (n_total 次平均)
final_traj = results[n_total]

# 计算不同 batch_size 下与最终轨迹的偏差
print(f"\n  {'循环次数':<12s} {'与最终轨迹的偏差':<20s} {'相对误差'}")
print(f"  {'-'*55}")
for batch_size in batch_sizes:
    if batch_size == n_total:
        continue
    diff = np.mean(np.abs(results[batch_size] - final_traj))
    rel = diff / np.mean(np.abs(final_traj - 1.0))  # 相对于总变化量
    print(f"  {batch_size:<12d} {diff:<20.6e} {rel:<15.6e}")

# 最终轨迹
print(f"\n  最终收敛轨迹 (k=30处的耦合常数):")
print(f"    SU(3) (p=2): g = {final_traj[30, 0]:.6f}")
print(f"    SU(2) (p=3): g = {final_traj[30, 1]:.6f}")
print(f"    U(1)  (p=5): g = {final_traj[30, 2]:.6f}")

# 理论期望值
expected = np.ones(3)
for p in GAUGE_PRIMES:
    idx = {2: 0, 3: 1, 5: 2}[p]
    expected_collapse = 0
    m = 1
    while p**m <= N_CYCLE:
        expected_collapse += np.log(p)**2 / m  # 期望坍缩量 = 概率 × 强度
        m += 1
    expected[idx] += expected_collapse

print(f"\n  理论期望值:")
print(f"    SU(3): g = {expected[0]:.6f}")
print(f"    SU(2): g = {expected[1]:.6f}")
print(f"    U(1):  g = {expected[2]:.6f}")

print(f"\n  模拟 vs 理论偏差:")
print(f"    SU(3): {abs(final_traj[30,0]-expected[0])/expected[0]*100:.4f}%")
print(f"    SU(2): {abs(final_traj[30,1]-expected[1])/expected[1]*100:.4f}%")
print(f"    U(1):  {abs(final_traj[30,2]-expected[2])/expected[2]*100:.4f}%")


# ============================================================
# 可视化：收敛过程
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ks = np.arange(N_CYCLE + 1)
colors = ['#2196F3', '#4CAF50', '#FF9800']
labels = ['SU(3)', 'SU(2)', 'U(1)']

# 图1: 不同循环次数的平均轨迹 (SU(3) 方向)
ax = axes[0, 0]
for batch_size in batch_sizes:
    traj = results[batch_size]
    alpha = 0.2 + 0.8 * (batch_size / n_total)
    ax.plot(ks, traj[:, 0], alpha=alpha, linewidth=1.5,
            label=f'N={batch_size}' if batch_size <= 1000 else f'N={batch_size//1000}k')
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('再生产计数 k')
ax.set_ylabel('g (SU(3))')
ax.set_title('SU(3) 方向: 平均轨迹收敛')
ax.legend(fontsize=7)
ax.set_xlim(0, N_CYCLE)
ax.grid(True, alpha=0.3)

# 图2: 偏差随循环次数衰减
ax = axes[0, 1]
batch_sizes_for_plot = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
# 只取存在的
existing = [b for b in batch_sizes_for_plot if b <= n_total]
deviations = []
for b in existing:
    if b in results:
        diff = np.mean(np.abs(results[b] - final_traj))
    else:
        # 计算该 batch_size
        avg_traj = np.zeros((N_CYCLE + 1, 3))
        for i in range(b):
            traj = simulate_one_cycle(random_seed=i + 100000)
            avg_traj += traj
        avg_traj /= b
        diff = np.mean(np.abs(avg_traj - final_traj))
    deviations.append(diff)

ax.loglog(existing, deviations, 'b-o', markersize=4)
# 拟合 1/√N 线
n_ref = np.array([1, n_total])
ref_line = deviations[0] * np.sqrt(n_ref[0]) / np.sqrt(n_ref)
ax.loglog(n_ref, ref_line, 'r--', alpha=0.5, label='∝ 1/√N')
ax.set_xlabel('循环次数 N')
ax.set_ylabel('与最终轨迹的偏差')
ax.set_title('偏差 ∝ 1/√N (大数定律)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 图3: 最终收敛轨迹 (三个方向)
ax = axes[1, 0]
for i in range(3):
    ax.plot(ks, final_traj[:, i], color=colors[i], label=labels[i], linewidth=2)
    ax.plot(ks, expected[i] * np.ones(N_CYCLE+1), '--', color=colors[i], alpha=0.5, linewidth=1)
ax.set_xlabel('再生产计数 k')
ax.set_ylabel('耦合常数 g')
ax.set_title('最终收敛轨迹 (N=100,000)')
ax.legend(fontsize=8)
ax.set_xlim(0, N_CYCLE)
ax.grid(True, alpha=0.3)

# 图4: 单次 vs 平均
ax = axes[1, 1]
# 单次轨迹
single_traj = simulate_one_cycle(random_seed=42)
for i in range(3):
    ax.plot(ks, single_traj[:, i], color=colors[i], alpha=0.3, linewidth=1, linestyle=':')
    ax.plot(ks, final_traj[:, i], color=colors[i], linewidth=2, label=f'{labels[i]} (平均)')
ax.set_xlabel('再生产计数 k')
ax.set_ylabel('耦合常数 g')
ax.set_title('单次轨迹(虚线) vs 平均轨迹(实线)')
ax.legend(fontsize=8)
ax.set_xlim(0, N_CYCLE)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, '18-统计投影收敛.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n图表已保存: 18-统计投影收敛.png")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 70)
print("核心结论: 统计投影 → 确定轨迹")
print("=" * 70)

print(f"""
1. 单次循环: 投影是概率性的
   - 玻色子以概率 log(p)/m 测量母轨迹
   - 每次循环的坍缩点不同 → 轨迹有方差
   
2. 多次循环: 统计平均收敛
   - 在 1 ns 内: {nu_cycle*1e-9:.1f} 次循环 → 相对误差 ~{1/np.sqrt(nu_cycle*1e-9):.2e}
   - 在 1 s 内:  {nu_cycle:.1e} 次循环 → 相对误差 ~{1/np.sqrt(nu_cycle):.2e}
   - 收敛速度 ∝ 1/√N (大数定律)
   
3. 宏观观测: 轨迹是确定的
   - 我们观测到的耦合常数是极限期望值
   - 就像量子力学的期望值——单次随机，平均确定
   - α_s(M_Z) = 0.1180 是统计极限，不是精确值
   
4. 根本图景:
   微观: 概率性坍缩 (玻色子测量)
   宏观: 确定性轨迹 (统计极限)
   
   这与量子力学的测量理论完全同构。
""")