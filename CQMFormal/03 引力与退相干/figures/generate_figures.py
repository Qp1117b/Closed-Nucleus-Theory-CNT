import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set style
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def save_fig(fig, name):
    fig.savefig(f'D:/WorkSpace/物理/闭合核理论/CQMFormal/03 引力与退相干/figures/{name}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


# Figure 1: Decoherence as continuous spectrum
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 3)
ax.set_ylim(0, 1)
ax.set_xlabel('耦合深度 d', fontsize=12)
ax.set_ylabel('相干性 / 唯一性', fontsize=12)
ax.set_title('退相干连续谱', fontsize=14, fontweight='bold')

# Regions
ax.axvspan(0, 1, alpha=0.2, color='blue', label='叠加态')
ax.axvspan(1, 1.5, alpha=0.2, color='orange', label='经典概率')
ax.axvspan(1.5, 3, alpha=0.2, color='green', label='确定结果')

# Curves
d = np.linspace(0.01, 3, 300)
coherence = np.exp(-2 * d)
uniqueness = 1 - np.exp(-2 * (d - 1))
uniqueness = np.where(d > 1, uniqueness, 0)

ax.plot(d, coherence, 'b-', linewidth=2, label='相干度')
ax.plot(d, uniqueness, 'g-', linewidth=2, label='唯一性')
ax.axvline(x=1, color='red', linestyle='--', linewidth=1.5, label='经典阈值 d_c')

ax.text(0.5, 0.85, '叠加态', fontsize=11, ha='center', color='blue', fontweight='bold')
ax.text(1.25, 0.5, '经典概率', fontsize=11, ha='center', color='darkorange', fontweight='bold')
ax.text(2.25, 0.85, '确定结果', fontsize=11, ha='center', color='green', fontweight='bold')

ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
save_fig(fig, '01_decoherence_spectrum')


# Figure 2: Cross-layer deep coupling
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('跨层级深耦合机制', fontsize=14, fontweight='bold')

# Base layer
base = mpatches.FancyBboxPatch((1, 1), 8, 2, boxstyle="round,pad=0.1",
                                edgecolor='black', facecolor='lightblue', linewidth=2)
ax.add_patch(base)
ax.text(5, 2, '基础层级（约束/条件/原料）', ha='center', va='center', fontsize=12, fontweight='bold')

# Upper layer
upper = mpatches.FancyBboxPatch((2.5, 5.5), 5, 2, boxstyle="round,pad=0.1",
                                 edgecolor='black', facecolor='lightgreen', linewidth=2)
ax.add_patch(upper)
ax.text(5, 6.5, '上层（能动系统/测量装置）', ha='center', va='center', fontsize=12, fontweight='bold')

# Arrows
ax.annotate('', xy=(5, 5.5), xytext=(5, 3),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(5.5, 4.2, '深耦合', fontsize=11, color='red', fontweight='bold')

ax.annotate('', xy=(3, 5.5), xytext=(3, 3),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.5, ls='--'))
ax.text(3.3, 4.2, '约束/条件/原料', fontsize=10, color='purple')

# Quantum system
system = mpatches.Circle((5, 8.2), 0.6, color='gold', ec='black', linewidth=2)
ax.add_patch(system)
ax.text(5, 8.2, '量子\n系统', ha='center', va='center', fontsize=10, fontweight='bold')

ax.annotate('', xy=(5, 7.6), xytext=(5, 7.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
ax.text(6.2, 8.2, '唯一结果', fontsize=11, color='green', fontweight='bold')

save_fig(fig, '02_cross_layer_coupling')


# Figure 3: Reductionism vs CQM
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Reductionism
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('层级还原论', fontsize=14, fontweight='bold')

layers1 = ['上层（现象）', '经典层', '量子层', '引力层', '…无限上承']
colors1 = plt.cm.Reds(np.linspace(0.3, 0.9, 5))
for i, (layer, color) in enumerate(zip(layers1, colors1)):
    y = 8 - i * 1.5
    rect = mpatches.FancyBboxPatch((2, y), 6, 1, boxstyle="round,pad=0.05",
                                    edgecolor='black', facecolor=color, linewidth=1.5)
    ax1.add_patch(rect)
    ax1.text(5, y + 0.5, layer, ha='center', va='center', fontsize=10, fontweight='bold')
    if i < 4:
        ax1.annotate('', xy=(5, y - 0.1), xytext=(5, y - 0.4),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax1.text(5, 0.8, '无法推出唯一性 → 多世界保底', ha='center', fontsize=11,
         color='darkred', fontweight='bold')

# CQM
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('CQM 层级非还原论', fontsize=14, fontweight='bold')

layers2 = ['上层（能动/经典）', '量子层', '引力层']
colors2 = ['lightgreen', 'lightyellow', 'lightblue']
positions = [7, 4.5, 2]
for layer, color, y in zip(layers2, colors2, positions):
    rect = mpatches.FancyBboxPatch((2, y), 6, 1.2, boxstyle="round,pad=0.05",
                                    edgecolor='black', facecolor=color, linewidth=1.5)
    ax2.add_patch(rect)
    ax2.text(5, y + 0.6, layer, ha='center', va='center', fontsize=10, fontweight='bold')

# Constraint arrows
for y in positions[1:]:
    ax2.annotate('', xy=(5, y + 1.3), xytext=(5, y + 1.6),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax2.text(6.5, 5.8, '约束/条件/原料', fontsize=10, color='blue', rotation=90, va='center')

# Deep coupling arrow
ax2.annotate('', xy=(8.5, 7.6), xytext=(8.5, 2.6),
            arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
ax2.text(9.1, 5, '深耦合\n筛出唯一性', fontsize=11, color='red', fontweight='bold',
         rotation=90, va='center')

ax2.text(5, 0.8, '退相干贯穿到底，无需多世界', ha='center', fontsize=11,
         color='darkgreen', fontweight='bold')

save_fig(fig, '03_reductionism_vs_CQM')


# Figure 4: Agency and coupling depth
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 3)
ax.set_ylim(0, 1.2)
ax.set_xlabel('耦合深度 d', fontsize=12)
ax.set_ylabel('能动作用效果', fontsize=12)
ax.set_title('能动性调节耦合深度', fontsize=14, fontweight='bold')

d = np.linspace(0.1, 3, 300)
# Different agency choices
depths = [0.5, 1.0, 1.8, 2.5]
labels = ['浅耦合：维持叠加', '经典耦合：概率分布', '深耦合：开始确定', '更深耦合：唯一结果']
colors = ['blue', 'orange', 'green', 'darkgreen']

for depth, label, color in zip(depths, labels, colors):
    effect = np.exp(-((d - depth) ** 2) / 0.1)
    ax.plot(d, effect, color=color, linewidth=2, label=label)
    ax.axvline(x=depth, color=color, linestyle='--', alpha=0.5)

ax.axvline(x=1, color='red', linestyle='--', linewidth=1.5, label='经典阈值 d_c')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
save_fig(fig, '04_agency_coupling_depth')


print("All figures generated successfully.")
