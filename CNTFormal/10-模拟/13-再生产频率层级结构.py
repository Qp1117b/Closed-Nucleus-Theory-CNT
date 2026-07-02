"""
CNT 再生产频率层级结构
======================

四个层级:
  1. 基础再生产频率 ν_0 = ν_P (Planck) → 闭合核结构的最基本时钟
  2. 母轨迹再生产频率 ν_M = m_p/h (质子) → 具体闭合核的周期
  3. 三种规范力再生产频率 ν_p → 从 ν_0 导出
  4. 耦合常数 → 从频率和p进结构导出

关键: ν_M 和 ν_0 的比值 = m_p/M_P — 层次问题在频率空间
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
h_MeVs = 4.135667662e-21  # MeV·s
m_p = 938.272              # MeV
M_P = 1.22089e22           # MeV
M_Z = 91.1876e3            # MeV
t_P = 5.391247e-44         # s

nu_P = 1.0 / t_P           # Planck 频率
nu_M = m_p / h_MeVs        # 母轨迹(质子) 频率

N_CYCLE = 30
GAUGE = [
    ('SU(3)', 2, 4, 7.0, '#E74C3C'),
    ('SU(2)', 3, 3, 19.0/6, '#27AE60'),
    ('U(1)', 5, 2, -41.0/10, '#F39C12'),
]

# ============================================================
# 主计算
# ============================================================

print("=" * 75)
print("CNT 再生产频率层级结构")
print("=" * 75)

# 层级1: 基础频率
print("\n[层级1] 基础再生产频率 ν_0 = ν_P (Planck 时钟)")
print(f"  ν_0 = 1/t_P = {nu_P:.3e} Hz")
print(f"  E_0 = hν_0 = M_P = {M_P/1e6:.2e} GeV")

# 层级2: 母轨迹频率
print(f"\n[层级2] 母轨迹再生产频率 ν_M = m_p/h (质子时钟)")
print(f"  ν_M = {nu_M:.3e} Hz")
print(f"  E_M = hν_M = m_p = {m_p/1e3:.3f} GeV")
print(f"  ν_M/ν_0 = m_p/M_P = {m_p/M_P:.2e}")

# 层级3: 规范力频率
print(f"\n[层级3] 三种规范力再生产频率 (从 ν_0 导出)")
print(f"  ν_p = (n_p/N_cycle) · ν_0,  N_cycle = {N_CYCLE}")
print()
print(f"  {'力':>8} {'n_p':>4}   {'ν_p (Hz)':>16}  {'E_p = hν_p (GeV)':>18}  {'ν_p/ν_0':>10}  {'ν_p/ν_M':>10}")
print(f"  {'-'*68}")

for name, p, n, b, color in GAUGE:
    nu_p = n / N_CYCLE * nu_P
    E_p = nu_p * h_MeVs / 1e3  # GeV
    print(f"  {name:>5}  {n:>4}   {nu_p:>16.3e}  {E_p:>18.2e}  {n/N_CYCLE:>10.4f}  {nu_p/nu_M:>10.2e}")

print(f"\n  ν_p/ν_M ≈ 10^19 — 规范力频率是母轨迹频率的 10^19 倍")

# ============================================================
# 物理图像
# ============================================================

print("\n" + "=" * 75)
print("物理图像: 嵌套时钟")
print("=" * 75)

print(f"""
  ν_0 (Planck)  = {nu_P:.1e} Hz  ─── 闭合核结构的最基本时钟
  │                                        (时空本身的量子涨落频率)
  │
  ├─ ν_SU3 = {4/30*nu_P:.1e} Hz  ─── 强相互作用点火频率
  ├─ ν_SU2 = {3/30*nu_P:.1e} Hz  ─── 弱相互作用点火频率
  └─ ν_U1  = {2/30*nu_P:.1e} Hz  ─── 电磁相互作用点火频率
  │
  └─ ν_M (质子) = {nu_M:.1e} Hz  ─── 母轨迹/质子再生产频率
                                        (规范力粗粒化后的宏观表现)

  母轨迹的频率是 ν_M (质子的"心跳")。
  规范力事件发生在 Planck 频率下，但母轨迹以低得多的频率
  整合这些事件，形成质子的宏观再生产周期。
  
  类比: 母轨迹是"包络" (envelope)，规范力是"载波" (carrier)。
  包络频率 = ν_M，载波频率 = ν_P。
  载波/包络比 = {nu_P/nu_M:.1e} = 层次问题。
""")

# ============================================================
# RG 跑动: 从 ν_0 到 ν_M
# ============================================================

print("=" * 75)
print("RG 跑动: 从 ν_0 到 ν_M 的耦合常数演化")
print("=" * 75)

# 点火耦合: α_p ∝ log(p)·n_p/N_cycle (功率假设)
# 归一化: 使 α 在合理范围
# α_p = A · log(p) · n_p/N_cycle
# 用 A = 0.216 (之前确定的最佳值)

A = 0.216  # 归一化常数

print(f"\n  点火耦合 (功率假设 α_p = A·log(p)·n_p/30, A={A}):")
print(f"  {'力':>8} {'功率':>10} {'α_ig':>10} {'μ_ig (GeV)':>14}")
print(f"  {'-'*46}")

for name, p, n, b, color in GAUGE:
    power = np.log(p) * n / N_CYCLE
    alpha_ig = A * power
    mu_ig = n / N_CYCLE * M_P / 1e3  # GeV
    print(f"  {name:>5}  {power:>10.4f}  {alpha_ig:>10.6f}  {mu_ig:>14.2e}")

# 单圈 RG 跑动到 ν_M 对应的能标 (m_p)
print(f"\n  RG 跑动到 μ_M = m_p = {m_p/1e3:.3f} GeV:")
print(f"  {'力':>8} {'α_ig':>10} {'α(m_p)':>10} {'α_MZ_pred':>10} {'α_MZ_exp':>10} {'偏差':>8}")
print(f"  {'-'*60}")

exp_map = {'SU(3)': 0.1180, 'SU(2)': 0.033801, 'U(1)': 0.016943}

for name, p, n, b, color in GAUGE:
    alpha_ig = A * np.log(p) * n / N_CYCLE
    mu_ig = n / N_CYCLE * M_P / 1e3  # GeV
    
    # 跑动到 m_p
    t1 = np.log(m_p / (mu_ig * 1e3))
    inv1 = 1.0/alpha_ig - b*t1/(2*np.pi)
    alpha_at_mp = 1.0/inv1 if inv1 > 0 else 0
    
    # 跑动到 M_Z
    t2 = np.log(M_Z / m_p)
    inv2 = 1.0/alpha_at_mp - b*t2/(2*np.pi)
    alpha_MZ = 1.0/inv2 if inv2 > 0 else 0
    
    exp_val = exp_map[name]
    dev = (alpha_MZ - exp_val) / exp_val * 100
    print(f"  {name:>5}  {alpha_ig:>10.6f}  {alpha_at_mp:>10.6f}  {alpha_MZ:>10.6f}  {exp_val:>10.6f}  {dev:>+7.1f}%")

# ============================================================
# 关键发现
# ============================================================

print("\n" + "=" * 75)
print("关键发现")
print("=" * 75)

# 计算 α_at_mp 更精确的值
results_at_mp = {}
for name, p, n, b, color in GAUGE:
    alpha_ig = A * np.log(p) * n / N_CYCLE
    mu_ig = n / N_CYCLE * M_P / 1e3  # GeV
    t1 = np.log(m_p / (mu_ig * 1e3))
    inv1 = 1.0/alpha_ig - b*t1/(2*np.pi)
    alpha_at_mp = 1.0/inv1 if inv1 > 0 else 0
    results_at_mp[name] = alpha_at_mp

# U(1) 的负 b 导致反向跑动
# 在 Planck 到 m_p 之间，U(1) 耦合减小

print(f"""
  1. ν_0 = ν_P = {nu_P:.1e} Hz
     基础时钟: 闭合核结构的最基本再生产频率

  2. ν_M = m_p/h = {nu_M:.1e} Hz
     母轨迹(质子)频率: 规范力粗粒化后的宏观表现

  3. ν_p = (n_p/30)·ν_P
     规范力频率在 Planck 量级
     ν_p/ν_M ≈ {nu_P/nu_M:.1e} → 层次问题在频率空间

  4. 耦合常数在 m_p 处的值:
     α_SU3(m_p) = {results_at_mp['SU(3)']:.6f}
     α_SU2(m_p) = {results_at_mp['SU(2)']:.6f}
     α_U1(m_p)  = {results_at_mp['U(1)']:.6f}

  5. 从 m_p 到 M_Z 的跑动:
     SU(3): 渐近自由 (b>0) → α ↓
     SU(2): 渐近自由 (b>0) → α ↓
     U(1): 非渐近自由 (b<0) → α ↑
""")

# ============================================================
# 可视化
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# 图1: 频率层级
ax = axes[0]
freqs = [nu_P, nu_M]
freqs += [n/N_CYCLE*nu_P for _, _, n, _, _ in GAUGE]
labels = ['ν_0 (Planck)', 'ν_M (质子)']
labels += [f'ν_{name} ({name})' for name, _, _, _, _ in GAUGE]
colors = ['#2C3E50', '#8E44AD', '#E74C3C', '#27AE60', '#F39C12']

y = np.arange(len(freqs))
ax.barh(y, freqs, color=colors, alpha=0.7, edgecolor='white')
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xscale('log')
ax.set_xlabel('频率 (Hz)')
ax.set_title('再生产频率层级')

# 图2: 能量对比
ax = axes[1]
energies = [M_P/1e3, m_p/1e3]
energies += [n/N_CYCLE*M_P/1e3 for _, _, n, _, _ in GAUGE]
y = np.arange(len(energies))
ax.barh(y, energies, color=colors, alpha=0.7, edgecolor='white')
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xscale('log')
ax.set_xlabel('能量 (GeV)')
ax.set_title('对应能量')

# 图3: 母轨迹与规范力的关系
ax = axes[2]
ax.text(0.5, 0.95, '母轨迹 (ν_M = m_p/h)', transform=ax.transAxes,
        ha='center', fontsize=12, fontweight='bold', color='#8E44AD',
        bbox=dict(boxstyle='round', facecolor='#F3E5F5', alpha=0.5))
ax.text(0.5, 0.75, '├── SU(3) 投影: ν_2 = 4/30·ν_P', transform=ax.transAxes,
        ha='center', fontsize=10, color='#E74C3C')
ax.text(0.5, 0.60, '├── SU(2) 投影: ν_3 = 3/30·ν_P', transform=ax.transAxes,
        ha='center', fontsize=10, color='#27AE60')
ax.text(0.5, 0.45, '└── U(1) 投影: ν_5 = 2/30·ν_P', transform=ax.transAxes,
        ha='center', fontsize=10, color='#F39C12')
ax.text(0.5, 0.25, f'ν_M/ν_0 = m_p/M_P = {m_p/M_P:.1e}', transform=ax.transAxes,
        ha='center', fontsize=9, color='gray', style='italic')
ax.text(0.5, 0.10, '母轨迹 = 包络 | 规范力 = 载波', transform=ax.transAxes,
        ha='center', fontsize=9, color='gray')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('频率结构')

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, '13-再生产频率层级.png'), dpi=150, bbox_inches='tight')
plt.close()
print("\n图表已保存: 13-再生产频率层级.png")