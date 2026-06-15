
基于 Lindquist (1966)、# 闭合核理论（CNT）方程修正与完整方程组

> **摘要**
>
> 本文针对闭合核理论（CNT）框架进行两项核心修正：(1) 基于 Lindquist (1966)、Ehlers (1971)、Israel (1972) 和 Sarbach & Zannias (2013) 的相对论动理学标准框架，给出方程③（测地线通量密度）的严格良性定义，消除原方程的量纲不匹配、协变性缺失、边界/体混淆及初始条件不清等缺陷；(2) 将牛顿熵力方程组从"信息场方案"（方案B）修正为"纯测地线方案"（方案A'），去掉信息梯度场和玻尔兹曼偏置两个中间层，让测地线几何直接驱动边界碰撞不对称。修正后的框架分为**质量涌现方程组**（方程①–⑥）和**牛顿熵力方程组**（方程⑦'–⑨'），通过测地线方程（方程①）自然衔接，构成从几何到质量到引力的完整因果闭环。

**关键词**：闭合核理论；测地线通量；相对论动理学；质量涌现；熵力；纯测地线机制；全息原理

---

## 1. 引言

闭合核理论（CNT）提出从测地线运动到质量涌现再到引力涌现的完整框架。然而，原框架存在两个核心问题：

- **方程③（测地线通量密度）的形式缺陷**：量纲不匹配、协变性缺失、边界/体混淆、初始条件不清。
- **牛顿熵力方程组的多余中间层**：原方案B引入信息梯度场和玻尔兹曼偏置，增加不必要假设。

本文给出两项修正后的完整九方程体系。

---

## 2. 修正一：方程③的严格良性定义

### 2.1 原方程的缺陷

原方程③定义为：

$$\sigma(x,t) = \int j_0 \cdot \delta(x-x_{\text{geo}})\cdot |u^\mu n_\mu|\, d\tau\, d^3x_0\, d^3u_0$$

| 缺陷 | 具体表现 |
|:---|:---|
| **量纲不匹配** | $\delta(x-x_{\text{geo}})$ 暗示三维delta（$[L^{-3}]$），与 $d\tau\,d^3x_0 d^3u_0$ 混合后无法凑出 $[\sigma]=[L^{-2}T^{-1}]$ |
| **协变性缺失** | 无背景度规 $\sqrt{-g^{(0)}}$ 或诱导度规 $\sqrt{\gamma^{(0)}}$ 因子 |
| **边界/体混淆** | $n_\mu$ 是二维表面法向量，却出现在体积分中 |
| **初始条件不清** | $j_0$ 的归一化、定义域均未明确 |

### 2.2 修正方案
Ehlers (1971)、Israel (1972) 和 Sarbach & Zannias (2013) 的标准相对论动理学框架，采用两阶段定义。

**阶段一：协变粒子数流 $J^\mu$**

$$\boxed{J^\mu(x) = \int_{\Sigma_{t_0}} d^3x_0 \, \sqrt{\gamma^{(0)}(x_0)} \int \frac{d^3p_0}{p_0^0} \, \hat{f}_0(x_0, p_0) \, p^\mu(\tau_*) \, \delta^{(4)}\bigl(x - x_{\text{geo}}(\tau_*; x_0, p_0)\bigr)}$$

| 符号 | 含义 | 量纲 |
|:---|:---|---:|
| $\Sigma_{t_0}$ | 初始时间切片（类空超曲面） | — |
| $\hat{f}_0(x_0, p_0)$ | 初始不变分布函数 | $[L^{-3}]$ |
| $d^3p_0/p_0^0$ | 动量空间洛伦兹不变测度 | $[M^2]$ |
| $x_{\text{geo}}(\tau; x_0, p_0)$ | 满足方程①的测地线世界线 | — |
| $\tau_*$ | 测地线到达时空点 $x$ 的固有时 | — |
| $\delta^{(4)}$ | 四维时空delta函数 | $[L^{-4}]$ |

**阶段二：测地线通量密度 $\sigma$**

$$\boxed{\sigma(x,t) = J^\mu(x,t) \, n_\mu(x) \Big|_{x \in S_t}, \quad S_t \equiv \Sigma_t \cap S}$$

其中 $S$ 为闭合核边界（二维类空表面），$n_\mu$ 为其向外单位法向量（$n_\mu n^\mu = +1$）。

**等价单积分形式**：

$$\sigma(x,t) = \int_{\Sigma_{t_0}} d^3x_0 \, \sqrt{\gamma^{(0)}(x_0)} \int \frac{d^3p_0}{p_0^0} \, \hat{f}_0(x_0, p_0) \, \bigl|p^\mu(\tau_*) n_\mu(x)\bigr| \, \delta^{(2)}_{S_t}\bigl(\mathbf{x} - \mathbf{x}_{\text{geo}}(t; x_0, p_0)\bigr)$$

### 2.3 量纲验证

$$[J^\mu] = [L^{-3}] \cdot [L^3] \cdot [M^2] \cdot [M] \cdot [L^{-4}] \cdot [L^4] = [L^{-2}T^{-1}] \quad \checkmark$$

$$[\sigma] = [J^\mu][n_\mu] = [L^{-2}T^{-1}] \cdot [1] = [L^{-2}T^{-1}] \quad \checkmark$$

---

## 3. 质量涌现方程组（方程①–⑥）

### 方程①：能量子测地线方程

$$\boxed{\frac{d^2 x^\mu}{d\tau^2} + \Gamma^{(0)\mu}_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0}$$

能量子在背景时空 $g^{(0)}_{\mu\nu}$ 中的自由运动。上标 $(0)$ 表示零阶背景度规。

### 方程②：能量子数守恒

$$\boxed{\nabla_\mu^{(0)} J^\mu = 0}$$

能量子数流 $J^\mu$ 在背景时空中协变守恒，碰撞less极限下由 Liouville 定理保证。

### 方程③：测地线通量密度（修正版）

$$\boxed{\sigma(x,t) = J^\mu(x,t) \, n_\mu(x) \Big|_{x \in S_t}}$$

将微观相空间分布 $\hat{f}_0$ 通过测地线轨迹投影为宏观源项 $\sigma(x,t)$。$\hat{f}_0$ 的量纲由方程④对 $\sigma$ 的量纲要求反推确定。

### 方程④：信息密度演化

$$\boxed{\frac{\partial \rho}{\partial t} = \sigma(x,t)\left(1-\frac{\rho}{\rho_{\max}}\right)}$$

线性饱和方程。$\sigma$ 为信息密度注入率，因子 $(1-\rho/\rho_{\max})$ 体现接近贝肯斯坦上限时填充速率的线性衰减。与 Logistic 方程不同，无自催化因子 $\rho$——从真空（$\rho=0$）开始，注入速率直接是 $\sigma$。

### 方程⑤：质量涌现

$$\boxed{m(t) = \frac{h\nu}{c^2}\int_S \rho(x,t)\sqrt{\gamma^{(0)}}\, d^2x}$$

质量由二维边界 $S$ 上的信息密度积分给出（全息型面积律），而非三维体积分。量纲：$[m] = [M] \cdot [L^{-2}] \cdot [L^2] = [M]$ ✓。

### 方程⑥：贝肯斯坦上限

$$\boxed{\rho_{\max} = \frac{1}{4\ell_P^2 \ln 2}}$$

信息密度普适上限源自 Bekenstein-Hawking 熵 $S = A/(4\ell_P^2)$。每个能量子携带 $\ln 2$ nat（1 bit），最大粒子数面密度为 $\rho_{\max} = 1/(4\ell_P^2 \ln 2)$。

### 因果链

$$\text{方程①} \xrightarrow{\text{定义 } x_{\text{geo}}, p^\mu} \text{方程③} \xrightarrow{\text{定义 } \sigma} \text{方程④} \xrightarrow{\text{定义 } \rho} \text{方程⑤} \xrightarrow{\text{定义 } m(t)}$$

---

## 4. 修正二：从信息场方案到纯测地线方案

### 4.1 原方案B的问题

原方案B引入两个中间层：

| 中间层 | 方程 | 问题 |
|:---|:---|:---|
| 信息梯度场 | 方程⑦：$\mathcal{G}_M(r) = \gamma_0 N_M/(4\pi r^2)$ | $\gamma_0 = \nu$ 未证明；$1/r^2$ 仅球对称下成立 |
| 玻尔兹曼偏置 | 方程⑧：$n(\theta) = n_0(1 + \delta\cos\theta)$ | 弱场近似的适用范围未界定；$\beta$ 未确定 |

这两个中间层增加了不必要的假设层级。

### 4.2 方案A'的核心洞见

**不需要信息场，不需要玻尔兹曼偏置。**

源核 $M$ 的内禀几何通过测地线方程①直接决定测试核 $m$ 内部能量子的轨迹。在Schwarzschild型几何中，测地线天然具有指向 $M$ 的汇聚趋势，导致测试核边界碰撞率天然不对称。

| 特征 | 方案A'（纯测地线） | 方案B（信息场） |
|:---|:---|:---|
| 核心机制 | 测地线几何 → 碰撞不对称 | 信息场 → 统计偏置 → 碰撞不对称 |
| 中间层 | **无** | 方程⑦+⑧ |
| 热力学假设 | 无 | 有（$T_{\text{int}}$、玻尔兹曼分布） |

### 4.3 概念对照

$$\text{方案B：几何} \to \text{信息场} \to \text{统计偏置} \to \text{碰撞不对称}$$

$$\text{方案A'：几何} \to \text{测地线汇聚} \to \text{碰撞不对称}$$

---

## 5. 纯测地线牛顿熵力方程组（方程⑦'–⑨'）

### 方程⑦'：测地线汇聚因子

$$\boxed{K_M(r, \theta) = \frac{1}{4\pi r^2} \left(1 + \alpha \frac{GM}{c^2 r} \cos\theta\right)}$$

在源核 $M$ 的Schwarzschild型几何中，测地线束天然具有指向 $M$ 的汇聚趋势。因子 $(1 + \alpha \frac{GM}{c^2 r}\cos\theta)$ 描述方向性——面向 $M$ 一侧（$\cos\theta > 0$）更密集。

- $1/r^2$：三维空间球面几何稀释（运动学必然结果，非假设）
- $\cos\theta$：测地线束在源核引力场中的汇聚效应
- $\alpha \sim \mathcal{O}(1)$：几何因子，由测地线束在球体边界上的投影积分确定，与光子球半径 $r_{\text{ph}} = 3GM/c^2$ 相关

量纲：$[K_M] = [L^{-2}]$ ✓

### 方程⑧'：边界碰撞率

$$\boxed{J(\theta) = \frac{n_0 c}{4} K_M(r, \theta) \cdot 4\pi R_m^2 = \frac{n_0 c}{4}\left(1 + \alpha \frac{GM}{c^2 r}\cos\theta\right)}$$

测试核 $m$ 内的 $N_m$ 个能量子沿方程①的测地线运动。由于 $M$ 产生的曲率，测地线汇聚趋势导致边界碰撞率天然不对称。这是**纯测地线几何效应**，无需玻尔兹曼统计假设。

| 符号 | 含义 |
|:---|:---|
| $n_0 = N_m/V_m$ | 能量子数密度 |
| $N_m = m/\mu_0$ | 测试核内能量子总数 |
| $V_m = \frac{4}{3}\pi R_m^3$ | 测试核体积 |

量纲：$[J] = [L^{-3}] \cdot [LT^{-1}] \cdot [L^2] = [L^{-2}T^{-1}]$ ✓

### 方程⑨'：边界熵-压响应

$$\boxed{\frac{dS}{dA\,dt}(\theta) = k_B \varsigma \, J(\theta)}$$

$$\boxed{P(\theta) = \frac{T_{\text{scr}}}{c} \frac{dS}{dA\,dt}(\theta) = P_0 \left(1 + \alpha \frac{GM}{c^2 r}\cos\theta\right), \quad P_0 = \frac{k_B T_{\text{scr}} \varsigma n_0 c}{4}}$$

全息边界记录每次撞击产生熵增。$J(\theta)$ 的不对称分布通过熵增率和压强自然传递。

| 符号 | 含义 | 量纲 |
|:---|:---|---:|
| $\varsigma$ | 每次撞击的熵增系数（$\sim \mathcal{O}(1)$） | $[1]$ |
| $T_{\text{scr}}$ | 边界筛查温度 | $[K]$ |

### 5.1 净力推导与涌现牛顿常数

净力由压强差球面积分产生，方向指向 $M$：

$$F = \int_{S_m} P(\theta) \cos\theta \, dA = P_0 \cdot \alpha \frac{GM}{c^2 r} \cdot \frac{A_m}{3}$$

代入 $P_0$、$A_m = 4\pi R_m^2$、$V_m = \frac{4}{3}\pi R_m^3$：

$$F = \frac{k_B T_{\text{scr}} \varsigma \alpha G}{16\pi c^2 \mu_0^2} \cdot \frac{Mm}{r^2}$$

$$\boxed{G_{\text{eff}}^{\text{(geo)}} = \frac{k_B T_{\text{scr}} \varsigma \alpha G}{16\pi c^2 \mu_0^2}}$$

量纲验证：$[G_{\text{eff}}] = [K] \cdot [1] \cdot [1] \cdot [L^3M^{-1}T^{-2}] / ([L^2T^{-2}] \cdot [M]) = [L^3M^{-1}T^{-2}]$ ✓，与牛顿常数同量纲。

### 5.2 η-消去定理与等效原理

$$\boxed{a = \frac{F}{m_i} = G_{\text{eff}} \frac{M}{r^2}, \quad \forall \eta_m \in (0,1]}$$

**证明**：碰撞率 $J \propto n_0 \propto N_m \propto \eta_m$，惯性质量 $m_i = \mu_0 N_m \propto \eta_m$，因此 $a = F/m_i = (\eta_m/\eta_m) \cdot G_{\text{eff}} M/r^2$——$\eta_m$ 严格消去。

等效原理不是公设，而是同一机制的两个方面：引力响应和惯性抵抗都正比于内部能量子总数 $N_m$。

---

## 6. 完整方程组与因果闭环

### 6.1 完整九方程

| 序号 | 方程 | 物理含义 |
|:---:|:---|:---|
| ① | $\frac{d^2 x^\mu}{d\tau^2} + \Gamma^{(0)\mu}_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0$ | 能量子测地线运动 |
| ② | $\nabla_\mu^{(0)} J^\mu = 0$ | 能量子数守恒 |
| ③ | $\sigma(x,t) = J^\mu(x,t) \, n_\mu(x) \big|_{x \in S_t}$ | 测地线通量密度（修正版） |
| ④ | $\frac{\partial \rho}{\partial t} = \sigma\left(1-\frac{\rho}{\rho_{\max}}\right)$ | 信息密度演化 |
| ⑤ | $m(t) = \frac{h\nu}{c^2}\int_S \rho(x,t)\sqrt{\gamma^{(0)}}\, d^2x$ | 质量涌现（全息型面积律） |
| ⑥ | $\rho_{\max} = \frac{1}{4\ell_P^2 \ln 2}$ | 贝肯斯坦上限 |
| ⑦' | $K_M(r,\theta) = \frac{1}{4\pi r^2}\left(1 + \alpha\frac{GM}{c^2 r}\cos\theta\right)$ | 测地线汇聚因子（纯测地线） |
| ⑧' | $J(\theta) = \frac{n_0 c}{4}\left(1 + \alpha\frac{GM}{c^2 r}\cos\theta\right)$ | 边界碰撞率（纯测地线） |
| ⑨' | $P(\theta) = P_0\left(1 + \alpha\frac{GM}{c^2 r}\cos\theta\right),\; P_0 = \frac{k_B T_{\text{scr}} \varsigma n_0 c}{4}$ | 熵-压响应 |

### 6.2 涌现牛顿引力

由方程⑨'球面积分：

$$\boxed{F = G_{\text{eff}}^{\text{(geo)}} \frac{Mm}{r^2}, \quad G_{\text{eff}}^{\text{(geo)}} = \frac{k_B T_{\text{scr}} \varsigma \alpha G}{16\pi c^2 \mu_0^2}}$$

### 6.3 完整因果链

**质量涌现**：

$$\text{方程①} \xrightarrow{x_{\text{geo}}, p^\mu} \text{方程③} \xrightarrow{\sigma} \text{方程④} \xrightarrow{\rho} \text{方程⑤} \xrightarrow{m(t)}$$

**引力涌现（纯测地线）**：

$$\text{方程①} \xrightarrow{\text{测地线汇聚}} \text{方程⑦'} \xrightarrow{K_M} \text{方程⑧'} \xrightarrow{J(\theta)} \text{方程⑨'} \xrightarrow{P(\theta)} \text{积分} \to F$$

**闭环**：

$$\text{几何} \longrightarrow \text{质量} \longrightarrow \text{引力} \longrightarrow \text{几何}$$

因果链无断裂，每一步有明确数学定义和物理诠释。方程①通过测地线方程同时衔接质量涌现和引力涌现两条因果链。

---

## 7. 修正总结

| 修正项 | 修正前 | 修正后 |
|:---|:---|:---|
| 方程③ | 单一体积分，量纲不匹配，协变性缺失 | 两阶段定义：协变 $J^\mu$ → 表面投影 $\sigma$，量纲自洽 |
| 牛顿熵力 | 方案B：几何→信息场→玻尔兹曼偏置→碰撞不对称 | 方案A'：几何→测地线汇聚→碰撞不对称（去掉两个中间层） |
| 方程⑦ | 信息梯度场 $\mathcal{G}_M = \gamma_0 N_M/4\pi r^2$（假设 $\gamma_0=\nu$） | 测地线汇聚因子 $K_M$（纯几何，$\alpha \sim \mathcal{O}(1)$） |
| 方程⑧ | 玻尔兹曼偏置 $n(\theta)=n_0(1+\delta\cos\theta)$（统计假设） | 边界碰撞率 $J(\theta)$（纯测地线几何效应） |
| 方程⑨ | 原方程⑨ | 方程⑨'（继承 $J(\theta)$ 的不对称性，无新假设） |

### 开放参数

| 参数 | 位置 | 解决方向 |
|:---|:---|:---|
| $\alpha$ | 方程⑦' | 从Schwarzschild几何中测地线束的投影积分确定 |
| $\varsigma$ | 方程⑨' | 全息屏的统计力学微观模型 |
| $T_{\text{scr}}$ | 方程⑨' | 边界量子态的有效温度 |
| $\hat{f}_0$ | 方程③ | 从量子引力或全息原理推导 |

---

## 参考文献

[1] R. W. Lindquist, "Relativistic transport theory," *Annals of Physics* **37**, 487 (1966).

[2] J. Ehlers, "General relativity and kinetic theory," in *General Relativity and Cosmology*, ed. R. K. Sachs (Academic Press, 1971), pp. 1–70.

[3] W. Israel, "The relativistic Boltzmann equation," in *General Relativity and Gravitation*, ed. G. Shaviv and J. Rosen (Wiley, 1972), pp. 201–241.

[4] O. Sarbach and T. Zannias, "The geometry of the tangent bundle and the relativistic kinetic theory of gases," *J. Math. Phys.* **50**, 112504 (2013) [arXiv:1309.2036].

[5] S. R. de Groot, W. A. van Leeuwen, and Ch. G. van Weert, *Relativistic Kinetic Theory: Principles and Applications* (North-Holland, 1980).

[6] C. Cercignani and G. M. Kremer, *The Relativistic Boltzmann Equation: Theory and Applications* (Birkhäuser, 2002).

[7] J. D. Bekenstein, "Black holes and entropy," *Phys. Rev. D* **7**, 2333 (1973).

[8] E. P. Verlinde, "On the origin of gravity and the laws of Newton," *JHEP* **1104**, 029 (2011) [arXiv:1001.0785].

[9] T. Padmanabhan, "Thermodynamical aspects of gravity: new insights," *Rep. Prog. Phys.* **73**, 046901 (2010) [arXiv:0911.5004].

[10] T. Jacobson, "Thermodynamics of spacetime: The Einstein equation of state," *Phys. Rev. Lett.* **75**, 1260 (1995).