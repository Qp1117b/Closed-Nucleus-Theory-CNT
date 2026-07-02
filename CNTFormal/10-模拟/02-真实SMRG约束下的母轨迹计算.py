"""
CNT 母轨迹真实计算：标准模型 RG 约束下的反推

目标：
    1. 使用标准模型一阶 RG β 函数生成真实的耦合常数跑动曲线；
    2. 通过 μ_k = μ0 · k 映射，把再生产计数 k 与能标联系起来；
    3. 在 k = 2, 3, 5（以及更多质数）处，用真实 RG 值作为母轨迹的硬约束；
    4. 数值求解满足约束、平滑、闭合的母轨迹；
    5. 比较母轨迹投影与完整 SM RG 曲线，扫描 μ0 寻找最佳标度。

关键假设（认识论地位：工作假设）：
    - SM 一阶 RG 在 μ ∈ [μ0, 30 μ0] 范围内足够准确；
    - 能标映射关系为 μ_k = μ0 · k（即再生产计数越高，能标越高）；
    - 母轨迹在循环论相空间中为离散环；
    - 三种规范力对应坐标 g_i = α_i（SM 归一化耦合常数）。

依赖：
    numpy, scipy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from typing import Dict, Tuple, Optional
import json
import os
import platform

# 配置中文字体支持
if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ---------------------------
# 1. 标准模型一阶 RG
# ---------------------------

class SMRGRunning:
    """
    标准模型规范耦合的一阶跑动。

    使用 SM 归一化：
        g_1 = α_1, g_2 = α_2, g_3 = α_3
    一阶 RG 方程：
        d(1/α_i)/d(ln μ) = - b_i / (2π)
    解：
        1/α_i(μ) = 1/α_i(m_Z) - (b_i / 2π) ln(μ / m_Z)
    """

    # 一阶 beta 函数系数（SM 归一化）
    B1 = 41.0 / 10.0
    B2 = -19.0 / 6.0
    B3 = -7.0

    # m_Z 处参考值（PDG 近似）
    M_Z = 91.1876  # GeV
    ALPHA_1_MZ = 0.01017  # SM normalization
    ALPHA_2_MZ = 0.0338
    ALPHA_3_MZ = 0.1179

    def __init__(self):
        self.b = np.array([self.B1, self.B2, self.B3])
        self.alpha_mz = np.array([self.ALPHA_1_MZ, self.ALPHA_2_MZ, self.ALPHA_3_MZ])

    def alpha(self, mu: float) -> np.ndarray:
        """计算在能标 mu（GeV）处的三个 α_i 值。"""
        if mu <= 0:
            raise ValueError("能标必须为正")
        log_ratio = np.log(mu / self.M_Z)
        inv_alpha = 1.0 / self.alpha_mz - (self.b / (2.0 * np.pi)) * log_ratio
        return 1.0 / inv_alpha

    def alpha_i(self, mu: float, i: int) -> float:
        """计算第 i 个耦合在能标 mu 处的值（i=0,1,2）。"""
        return self.alpha(mu)[i]


# ---------------------------
# 2. 母轨迹优化器
# ---------------------------

class RealMotherTrajectory:
    """
    在真实 SM RG 约束下反推母轨迹。
    """

    def __init__(
        self,
        mu0: float,
        N_cycle: int = 30,
        sm_rg: Optional[SMRGRunning] = None,
        lambda_loop: float = 10.0,
        lambda_split: float = 1000.0,
        lambda_rg: float = 1.0,
        lambda_smooth: float = 1.0,
    ):
        self.mu0 = mu0
        self.N_cycle = N_cycle
        self.sm = sm_rg if sm_rg is not None else SMRGRunning()
        self.lambda_loop = lambda_loop
        self.lambda_split = lambda_split
        self.lambda_rg = lambda_rg
        self.lambda_smooth = lambda_smooth

        # 生成真实 RG 约束：g_i^(k) = α_i(μ0 * k)
        self.rg_values = self._generate_rg_constraints()

        # 初猜：真实 RG 曲线本身
        self.Gamma = self.rg_values.copy()

    def _generate_rg_constraints(self) -> np.ndarray:
        """生成每个 k 对应的真实 SM RG 值。"""
        Gamma = np.zeros((self.N_cycle, 3))
        for k in range(1, self.N_cycle):
            mu_k = self.mu0 * k
            Gamma[k, :] = self.sm.alpha(mu_k)
        # 闭合条件：起点复制终点
        Gamma[0, :] = Gamma[-1, :]
        return Gamma

    def _prime_indices(self) -> np.ndarray:
        """返回 [2, N_cycle) 内的质数索引。"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(np.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        return np.array([k for k in range(2, self.N_cycle) if is_prime(k)])

    def action(self, Gamma_flat: np.ndarray) -> float:
        """
        实数值损失函数。

        包含：
        1. 离散环闭合条件（Gamma[0] ≈ Gamma[-1]）
        2. 质数处硬约束（Gamma[p] = α_i(μ0·p)）
        3. RG 平滑性（轨迹不要剧烈抖动）
        4. 二阶平滑性（离散二阶导数小）
        """
        Gamma = Gamma_flat.reshape((self.N_cycle, 3))

        # 1. 闭合条件
        loop_penalty = np.sum((Gamma[-1, :] - Gamma[0, :]) ** 2)

        # 2. 质数处投影约束（硬约束）
        split_penalty = 0.0
        for p in self._prime_indices():
            target = self.sm.alpha(self.mu0 * p)
            split_penalty += np.sum((Gamma[p, :] - target) ** 2)

        # 3. 一阶平滑性
        rg_penalty = 0.0
        for k in range(self.N_cycle - 1):
            rg_penalty += np.sum((Gamma[k + 1, :] - Gamma[k, :]) ** 2)

        # 4. 二阶平滑性
        smooth_penalty = 0.0
        for k in range(1, self.N_cycle - 1):
            smooth_penalty += np.sum(
                (Gamma[k + 1, :] - 2 * Gamma[k, :] + Gamma[k - 1, :]) ** 2
            )

        return (
            self.lambda_loop * loop_penalty
            + self.lambda_split * split_penalty
            + self.lambda_rg * rg_penalty
            + self.lambda_smooth * smooth_penalty
        )

    def optimize(self, method: str = "L-BFGS-B", max_iter: int = 5000) -> np.ndarray:
        """优化母轨迹。"""
        result = minimize(
            self.action,
            self.Gamma.flatten(),
            method=method,
            options={"maxiter": max_iter},
        )
        self.Gamma = result.x.reshape((self.N_cycle, 3))
        return self.Gamma

    def reconstruction_error(self) -> float:
        """母轨迹投影与真实 RG 曲线的均方误差。"""
        return np.mean((self.Gamma - self.rg_values) ** 2)


# ---------------------------
# 3. μ0 扫描
# ---------------------------

def scan_mu0(mu0_list: np.ndarray, N_cycle: int = 30) -> Dict:
    """扫描不同 μ0，比较母轨迹与真实 RG 曲线的拟合质量。"""
    results = {
        "mu0": [],
        "action_initial": [],
        "action_final": [],
        "reconstruction_error": [],
        "Gamma": [],
        "rg_values": [],
    }

    for mu0 in mu0_list:
        model = RealMotherTrajectory(mu0=mu0, N_cycle=N_cycle)
        S_initial = model.action(model.Gamma.flatten())
        model.optimize()
        S_final = model.action(model.Gamma.flatten())
        err = model.reconstruction_error()

        results["mu0"].append(float(mu0))
        results["action_initial"].append(float(S_initial))
        results["action_final"].append(float(S_final))
        results["reconstruction_error"].append(float(err))
        results["Gamma"].append(model.Gamma.tolist())
        results["rg_values"].append(model.rg_values.tolist())

    return results


# ---------------------------
# 4. 可视化
# ---------------------------

def plot_scan_results(results: Dict, save_path: Optional[str] = None):
    """绘制 μ0 扫描结果。"""
    mu0 = np.array(results["mu0"])
    err = np.array(results["reconstruction_error"])
    action_final = np.array(results["action_final"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ax.plot(mu0, err, "-o", color="darkblue")
    ax.set_xlabel(r"基本能标 $\mu_0$ (GeV)")
    ax.set_ylabel("母轨迹-RG 重建误差")
    ax.set_title(r"不同 $\mu_0$ 下的重建误差")
    ax.grid(True, alpha=0.3)
    if len(err) > 0:
        best_idx = np.argmin(err)
        ax.axvline(mu0[best_idx], color="red", linestyle="--", alpha=0.7, label=f"最佳 μ0={mu0[best_idx]:.2f} GeV")
        ax.legend()

    ax = axes[1]
    ax.plot(mu0, action_final, "-o", color="darkgreen")
    ax.set_xlabel(r"基本能标 $\mu_0$ (GeV)")
    ax.set_ylabel("优化后损失函数")
    ax.set_title(r"不同 $\mu_0$ 下的损失函数")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"扫描图已保存: {save_path}")
    else:
        plt.show()


def plot_best_trajectory(results: Dict, save_path: Optional[str] = None):
    """绘制最佳 μ0 对应的母轨迹与 RG 曲线对比。"""
    best_idx = np.argmin(results["reconstruction_error"])
    mu0 = results["mu0"][best_idx]
    Gamma = np.array(results["Gamma"][best_idx])
    rg = np.array(results["rg_values"][best_idx])
    N = Gamma.shape[0]
    k = np.arange(N)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    labels = [r"$\alpha_1$ (U(1), SM norm)", r"$\alpha_2$ (SU(2))", r"$\alpha_3$ (SU(3))"]
    colors = ["red", "green", "blue"]

    # 子图 1：三个耦合随 k 演化
    ax = axes[0, 0]
    for i in range(3):
        ax.plot(k, rg[:, i], "--", color=colors[i], alpha=0.7, label=f"SM RG: {labels[i]}")
        ax.plot(k, Gamma[:, i], "-o", color=colors[i], markersize=3, label=f"母轨迹: {labels[i]}")
    ax.set_xlabel(r"再生产计数 $k$")
    ax.set_ylabel(r"耦合常数 $\alpha_i$")
    ax.set_title(rf"母轨迹 vs SM RG（$\mu_0$={mu0:.2f} GeV）")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 子图 2：α1-α2 平面
    ax = axes[0, 1]
    ax.plot(rg[:, 0], rg[:, 1], "--", color="gray", alpha=0.7, label="SM RG")
    ax.plot(Gamma[:, 0], Gamma[:, 1], "-o", color="purple", markersize=3, label="母轨迹")
    ax.set_xlabel(r"$\alpha_1$")
    ax.set_ylabel(r"$\alpha_2$")
    ax.set_title(r"母轨迹在 $\alpha_1$-$\alpha_2$ 平面")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 子图 3：三维耦合空间
    ax = fig.add_subplot(2, 2, 3, projection="3d")
    ax.plot(rg[:, 0], rg[:, 1], rg[:, 2], "--", color="gray", alpha=0.7, label="SM RG")
    ax.plot(Gamma[:, 0], Gamma[:, 1], Gamma[:, 2], "-o", color="darkorange", markersize=3, label="母轨迹")
    ax.set_xlabel(r"$\alpha_1$")
    ax.set_ylabel(r"$\alpha_2$")
    ax.set_zlabel(r"$\alpha_3$")
    ax.set_title("三维耦合空间")

    # 子图 4：逐点误差
    ax = axes[1, 1]
    error = np.abs(Gamma - rg)
    for i in range(3):
        ax.plot(k, error[:, i], "-o", color=colors[i], markersize=3, label=labels[i])
    ax.set_xlabel(r"再生产计数 $k$")
    ax.set_ylabel(r"$|\Gamma_i(k) - \alpha_i(\mu_0 k)|$")
    ax.set_title("母轨迹与 SM RG 的逐点偏差")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"最佳轨迹图已保存: {save_path}")
    else:
        plt.show()


# ---------------------------
# 5. 主程序
# ---------------------------

def main():
    print("=" * 70)
    print("CNT 母轨迹真实计算：标准模型 RG 约束下的反推")
    print("=" * 70)

    # 5.1 验证 SM RG 计算
    print("\n[1] 验证 SM RG 计算（m_Z 处参考值）")
    sm = SMRGRunning()
    alpha_mz = sm.alpha(sm.M_Z)
    print(f"  α_1(m_Z) = {alpha_mz[0]:.5f} (目标: {sm.ALPHA_1_MZ:.5f})")
    print(f"  α_2(m_Z) = {alpha_mz[1]:.5f} (目标: {sm.ALPHA_2_MZ:.5f})")
    print(f"  α_3(m_Z) = {alpha_mz[2]:.5f} (目标: {sm.ALPHA_3_MZ:.5f})")

    # 5.2 μ0 扫描
    print("\n[2] 扫描基本能标 μ0")
    mu0_list = np.linspace(5.0, 50.0, 10)  # GeV
    results = scan_mu0(mu0_list, N_cycle=30)

    for i, mu0 in enumerate(results["mu0"]):
        print(f"  μ0={mu0:5.2f} GeV: 初始损失={results['action_initial'][i]:8.3f}, "
              f"最终损失={results['action_final'][i]:8.3f}, 重建误差={results['reconstruction_error'][i]:.2e}")

    best_idx = np.argmin(results["reconstruction_error"])
    best_mu0 = results["mu0"][best_idx]
    print(f"\n  最佳 μ0 = {best_mu0:.2f} GeV（最小重建误差）")

    # 5.3 保存结果
    output_dir = "d:\\WorkSpace\\物理\\闭合核理论\\CNTFormal\\10-模拟"
    scan_plot_path = os.path.join(output_dir, "02-真实SMRG约束_μ0扫描.png")
    traj_plot_path = os.path.join(output_dir, "02-真实SMRG约束_最佳轨迹.png")

    plot_scan_results(results, save_path=scan_plot_path)
    plot_best_trajectory(results, save_path=traj_plot_path)

    json_path = os.path.join(output_dir, "02-真实SMRG约束_扫描结果.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n扫描数据已保存: {json_path}")

    print("\n" + "=" * 70)
    print("真实计算完成。注意：μ0 的物理起源仍待从 CNT 第一性原理确定。")
    print("=" * 70)


if __name__ == "__main__":
    main()
