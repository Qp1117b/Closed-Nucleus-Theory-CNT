# CQM 超导：金属氢机制与计算框架

> **上承**：[CQM 超导 涌现论](./CQM%20超导%20涌现论.md)（第 1–5 层本体论与机制）、[CQM 超导 涌现积分](./CQM%20超导%20涌现积分.md)（第 6–9 层公式）
> **下启**：[CQM 室温超导方向](./CQM%20室温超导方向.md)（第三步）
> **Lean 形式化**：`06 Lean形式化/Superconductivity/Reduction.lean`（第一步：BCS 退化与还原）
> **计算器**：[CQM超导Tc计算器.py](./CQM超导Tc计算器.py)

---

## 0. 为什么金属氢是 CQM 的理想推导对象

CQM 的本体论基石是**质子 = 有限本体**（自再产生因果环，`proton_is_finite_ontology`）。
在这个本体论下，一切材料的超导能力都来自**有限本体网络的密度与完整性**：

| 材料 | 核 = 有限本体 | CQM 视角 |
|:---|:---|:---|
| 普通金属（Al、Pb） | 重核 + 大量中子 | 网络被"缺陷"稀释（中子 = 缺陷有限本体），因果截断低 |
| **金属氢（含富氢材料）** | **每个氢核 = 单个质子 = 最简最纯的有限本体** | **最密、最纯、最完整的有限本体网络；因果截断最高** |

**"单个氢是单个质子有限本体"的三重推论**：

1. **网络纯度**：氢亚晶格不含任何"缺陷本体"（中子），关系网络的因果锁定最完整——这就是第一性计算发现"LaH10 中 H 光学模式贡献 λ 的 80–90%、H3S 中 90% 以上"的本体论根源。
2. **因果截断最高**：ω_D = √(k/M) 中 M = M_proton 是全元素周期表最小的离子质量，金属氢的德拜频率是所有晶格中最高的（LaH10 的 ω_log ≈ 797 cm⁻¹ ≈ 1147 K，远超任何重元素晶格）。
3. **同位素定律最纯粹**：氢氘替换直接改变质子有限本体的质量（M → 2M），同位素实验是 CQM 最干净的探针。

---

## 1. 第一步：CQM 必须退化和还原已有超导理论（公式层已 Lean 对应）

### 1.1 退化条件（晶格扇区）

CQM 的 T_c 公式（第 8 层）在自然单位下：

$$k_B T_c = \frac{2e^\gamma}{\pi} \cdot \hbar\omega_{\text{causal}} \cdot \exp\left(-\frac{1}{N(0)\cdot V_0}\right)$$

其中 2e^γ/π ≈ 1.1339（γ 为欧拉-马歇罗尼常数）；文献公式常写 1.13，
那只是该系数的三位数值近似——Lean 内一律使用精确常数 `bcsExactConstant`。

**退化到 BCS 的两个条件**（`Reduction.lean` 中的 `cqm_reduces_to_bcs`、`cqm_debye_reduction`）：

1. **配对通道 = 晶格声子扇区**：因果截断频率取德拜频率 ω_D = √(k/M_ion)（`debyeFrequency`）。晶格振动是质子有限本体网络在其禁闭几何（正四单纯形）中的因果锁定周期运动——"声子"就是 CQM 晶格扇区的因果截断激发。
2. **耦合常数对应**：态密度 × 耦合乘积 N(0)·V₀ ≡ d·c。

### 1.2 还原的公式（三层严格区分：公式定义 / 性质定理 / 文献数值近似）

> **严格性注记（勿把定义当证明）**：下表每行"公式层"列给出 BCS 公式的结构，
> "Lean 定义"列是**公式的正式声明**（`noncomputable def`，即"把 BCS 公式本身
> 定义为数学对象"，这一步不是"证明公式成立"）；"性质定理"列才是 **Lean 已证明
> 的结论**（正性、单调性、方程解、恒等式、极限）。凡数值（1.13、3.53、0.707、
> 1.2、1.04）均为文献近似，仅在注释中标示，**不冒充定理**。
>
> 公理化边界：这些定义所依据的物理前提（如声子机制、BCS 近似的成立域）不在
> 本模块内证明，而是 `physical_hypothesis` 公理或文献输入——证明的是"在此
> 前提下，所定义的量满足这些数学性质"。

| BCS 公式 | 数值（文献近似） | Lean 定义 | 性质定理（已证） |
|:---|:---|:---|:---|
| T_c = (2e^γ/π)·ω_D·exp(−1/(N(0)V)) | 2e^γ/π ≈ 1.1339（文献写 1.13） | `bcsCriticalTemperature`、`criticalTemperature` | `bcsCriticalTemperature_pos`、`criticalTemperature_pos`、`criticalTemperature_monotone_in_cutoff` |
| CQM→BCS 退化（记号对应） | — | `cqm_reduces_to_bcs`、`cqm_debye_reduction` | 两个都只是 `rfl`/定义展开的记号等同，**不是** BCS 物理的独立推导 |
| 零温能隙 Δ₀ = 2·ω_D·exp(−1/(N(0)V)) | — | `bcsGap` | `bcsGap_pos`（弱耦合极限式，有限 λ 的逼近见下两行） |
| 能隙方程闭式解 Δ = ω_D/sinh(1/λ) | — | `bcsGapFromGapEquation` | `bcs_gap_equation`（确为能隙方程的解）、`bcs_gap_equation_unique`（唯一解） |
| 弱耦合退化 | — | — | `bcs_gap_weak_coupling_limit`（λ→0⁺ 精确解/标准式 → 1，极限定理非等式）、`bcs_gap_ratio_eq`（比值恒等式 (1−e^{−2/λ})⁻¹） |
| **普适能隙比** 2Δ₀/(k_B T_c) | 2πe^{−γ} ≈ **3.5278**（文献常写 3.53） | — | `bcs_universal_gap_ratio`（精确定理，与 ω_D、N(0)V 无关） |
| **同位素定律** T_c ∝ M^(−1/2) | α = 1/2 | `debyeFrequency` | `debyeFrequency_decreases_with_mass`、`criticalTemperature_isotope_shift`、`criticalTemperature_decreases_with_ion_mass` |
| 氢/氘位移 T_c(D) = T_c(H)/√2 | √(1/2) ≈ 0.707 | — | `hydrogen_deuterium_isotope_shift` |
| McMillan–Dynes 强耦合 | 1.2 与 1.04 为文献经验系数 | `mcmillanDynesTc` | `mcmillanDynesTc_pos`、`mcmillan_strong_coupling_condition` |
| London 穿透深度 λ_L | — | `londonPenetrationDepth` | `londonPenetrationDepth_pos` |
| BCS 相干长度 ξ₀ | — | `bcsCoherenceLength` | `bcsCoherenceLength_pos` |
| 磁通量子 Φ₀ = h/2e | π（自然单位） | `fluxQuantum` | `fluxQuantum_eq_pi` |

> **注意**：T_c、能隙、London、ξ₀、Φ₀ 的"公式本身"在 Lean 中都是**定义**——
> 它们把 BCS/Meissner/London 的已知结果转为符号对象，其正确性来自实验与文献，
> **不是**由 Lean 导出；Lean 导出的是这些定义所满足的运算性质。这正是本节标题
> "三层严格区分"的含义：定义 ≠ 定理 ≠ 数值。`cqm_reduces_to_bcs` 一次注明为
> 记号对应层，避免与"独立推导出 BCS"混淆。

### 1.3 朴素 CQM 异常（条件定理）

`naive_cqm_isotope_anomaly`：若**不**退化到晶格扇区，朴素 CQM 的
ω_causal = 2πM_eff 与离子质量成正比，给出 T_c 随质量**单调不减**
（按 T_c ∝ M^(−α) 的约定 α = −1），与 BCS 同位素定律（α = 1/2）
及实验（H3S/D3S，α ≈ 0.47）方向相反。

**注意（严格性）**：这是一个**条件定理**——它证明的是"若采用朴素替换，
则 T_c 随质量的变化方向与实验相反"，是对模型选择的判别，**不是**
"退化是逻辑必然"的证明。"配对通道取晶格声子扇区"是物理选择，其依据
是与实验的一致性和下述本体论承诺：

> 晶格振动 = 有限本体网络在其禁闭几何（正四单纯形）中的因果锁定周期运动；
> "声子" = CQM 晶格扇区的因果截断激发。

CQM 因此并非一个"替代 BCS 的机制"，而是为 BCS 的每个要素提供本体论
**底层解释**（声子的因果本质、N(0)V 的网络本质、同位素定律的质量本质），
并保留了**超出 BCS 的预言空间**（几何因子，见 §4）。

### 1.4 强耦合扩展

金属氢化物 λ ≈ 2，已超出 BCS 弱耦合有效域（λ ≲ 0.3）。计算框架中的
**McMillan–Dynes 强耦合公式**（`mcmillanDynesTc`）：

$$k_B T_c = \frac{\omega_{\ln}}{1.2}\exp\left[-\frac{1.04(1+\lambda)}{\lambda - \mu^*(1+0.62\lambda)}\right]$$

分母正性条件 λ > μ*(1+0.62λ) 已形式化为 `mcmillan_strong_coupling_condition`。
H3S：λ ≈ 1.94 ≫ μ* ≈ 0.12，满足。

---

## 2. CQM 完整超导机制链（金属氢映射）

```
有限本体（质子 = 自再产生因果环）
  │  晶格 = 有限本体关系网络（金属氢 = 最密最纯网络）
  ▼
晶格振动 = 网络因果锁定的周期性调制
  │  因果截断频率 ω_D = √(k/M_proton)（全元素周期表最高）
  ▼
声子 = CQM 晶格扇区的因果截断激发（第 3 层引力因果限制场的晶格实现）
  │  电子与晶格因果结构的相互作用
  ▼
三方因果闭环：电子 — 晶格 — 电子（第 4 层，tripleLoopStrength_locked_pos）
  │  闭环锁定 → 配对通道开启（superconductivity_requires_relation_network）
  ▼
Cooper 对 = 关系性封装（RQM 组合操作）
  │  宏观相位相干 = 网络中全部因果环的同步锁定
  ▼
涌现积分 ψ(r,T) = ∫ d³k D_lattice·P_electron·C_triple·K_causal·e^{−Γ|τ|}（第 6–7 层）
  │  emergenceIntegral_pos：序参量严格为正
  ▼
T_c = (2e^γ/π)·ω_causal·exp(−1/(N(0)V₀))（第 8 层，criticalTemperature_pos；1.13 为近似）
  │  退化条件：ω_causal → ω_D = √(k/M)，N(0)V₀ → d·c
  ▼
BCS（弱耦合核心，cqm_reduces_to_bcs）→ McMillan–Dynes（强耦合，λ ≈ 2）
```

### 2.1 每个要素的本体论地位

| 计算要素 | 物理含义 | CQM 本体论地位 | Lean 对应 |
|:---|:---|:---|:---|
| ω_D（ω_ln） | 德拜/对数声子频率 | 有限本体网络因果锁定的周期 | `debyeFrequency` |
| λ = N(0)V | 电子-声子耦合 | 网络密度 × 因果闭环操作强度 | `densityOfStates*coupling` |
| μ* | 库仑赝势 | 未屏蔽的缺陷本体间的斥力（网络缺陷项） | `muStar` |
| Δ₀ | 零温能隙 | 三方闭环锁定的能量尺度 | `bcsGap` |
| f(geometry) | 几何因子（因果屏蔽） | 禁闭在正四单纯形内部、不参与因果截断的质量份额 | `effectiveMass = M_ion·f` |
| T_grav | 引力拓扑因子 | 强引力只增强因果锁定（不破坏配对） | `gravitationalTopologyFactor` |

---

## 3. 计算框架

### 3.1 输入层

对给定材料与压力 P：

| 符号 | 含义 | 来源 |
|:---|:---|:---|
| ω_D 或 ω_ln | 德拜/对数声子频率（K） | 第一性计算 α²F(ω)，或拉曼/非弹性 X 射线实验 |
| λ | 电子-声子耦合常数 λ = 2∫α²F(ω)/ω dω | 同上 |
| μ* | 库仑赝势（典型 0.10–0.16） | Eliashberg 拟合 |
| M_ion | 离子质量 | 同位素（H/D）可替换 |

### 3.2 公式层（层次：弱耦合 → 强耦合）

1. **BCS（CQM 退化核心，仅 λ ≲ 0.3）**：T_c = (2e^γ/π)·ω_D·exp(−1/λ)（1.13 为近似）
2. **McMillan–Dynes（金属氢化物，λ ≈ 2）**：T_c = (ω_ln/1.2)·exp[−1.04(1+λ)/(λ−μ*(1+0.62λ))]
3. **Allen–Dynes 修正（f₁f₂）及各向异性 Eliashberg**：对 H3S/LaH10 的精确计算需此层级（见 §3.4）
4. **同位素定律**：T_c(D)/T_c(H) = √(1/2)（H 亚晶格主导时）
5. **CQM 修正**：M_eff = M_ion·f(geometry)，α_eff = 1/2 + (1/2)·d(ln f)/d(ln M)

### 3.3 CQM 层：高压 = 强引力场

第 5 层承诺"强引力不破坏超导"（`strong_gravity_keeps_pairing_channels`）。
金属氢化物实验恰好运行在 **P ≈ 150–300 GPa 的强引力环境**（等效引力势
Φ/c² ≈ 10⁻⁴ 量级，远高于地球表面 10⁻⁹），CQM 预言：

- 引力拓扑因子 T_grav(Φ) = 1 + Φ + Φ² 只**增强**因果锁定（`gravitationalTopologyFactor_ge_one`）
- 压力升高 → 体积压缩 → 力常数 k 增大 → ω_D 增大（实验：LaH10 的 ω_log 随压力从 467 升到 932 cm⁻¹）
- 同时 λ 随压力下降（LaH10: 220 GPa 时 λ=4.24 → 300 GPa 时 1.86）——两者竞争决定最佳压力窗口

### 3.4 数值验证表（`python "CQM超导Tc计算器.py"` 输出）

| 材料 | P/GPa | ω_ln/K | λ | μ* | McMillan/K | 实验/K | 备注 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| Al | 0 | 428 | 0.43 | 0.10 | 2.6 | 1.18 | BCS 弱耦合标尺 |
| Pb | 0 | 105 | 1.55 | 0.15 | 10.6 | 7.2 | 强耦合经典例子 |
| MgB₂ | 0 | 750 | 0.90 | 0.11 | 41.5 | 39.0 | 双能隙声子超导（符合良好） |
| **H3S** | 155 | 1330 | 1.94 | 0.123 | 177 | **203** | Drozdov 2015；Eliashberg 精确解达 203 |
| **LaH10** | 170 | 1147 | 2.35 | 0.13 | 172 | **250** | Drozdov 2019；各向异性计算达 250–260 |

> McMillan 公式系统性低估强耦合 T_c（H3S 低 13%、LaH10 低 31%），
> Allen–Dynes f₁f₂ 及各向异性 Eliashberg 计算补足——这是文献共识
> （"McMillan or Allen-Dynes formulas substantially lower the critical temperature
> relative to Eliashberg equations"，Szczęśniak et al. 2016）。

### 3.5 同位素验证（CQM 探针）

| 体系 | T_c(H)/K | T_c(D)/K | 实测比 | 谐波预言 1/√2 | 同位素指数 α |
|:---|:---:|:---:|:---:|:---:|:---:|
| H3S/D3S @150 GPa | 203 | 147 | 0.724 | 0.707 | **0.466** |

α = 0.466 偏离 0.5 的来源：S 亚晶格不随 H→D 变化 + 强非谐性。
**CQM 的独特预言**：若几何因子 f(M) 引入额外质量标度，同位素指数可系统性偏离 1/2
（计算器演示：f(D)/f(H) = 0.9 时 α → 0.65）——同位素实验是区分 CQM 几何因子
与非谐效应的**判别性实验**。

---

## 4. CQM 预言与可证伪性

| 预言 | 内容 | 可证伪实验 |
|:---|:---|:---|
| P1 | 氢亚晶格贡献 λ 的 80–90%（网络纯度定理的推论） | 已部分证实（LaH10: H1+H2 ≈ 88%；H3S: ≈ 90%） |
| P2 | 同位素指数 α = 1/2 + 几何因子修正；修正大小随压力可调 | 高压 H/D 同位素实验（判别 CQM vs 纯非谐） |
| P3 | 强引力增强因果锁定 → 高压下 T_c 的引力修正项 +1+Φ+Φ² | 极端高压（300+ GPa）金属氢的精确 T_c(P) 曲线 |
| P4 | 网络完整性 → 缺陷（中子/空位）线性压低 T_c | 同位素混合、非晶化实验 |
| P5 | BCS 是 CQM 的弱耦合退化极限（并非独立机制） | 弱耦合材料（Al、Nb）必须精确复现 BCS 全部公式 |

**形式化的意义（严格范围）**：`Reduction.lean` 中证明的是**公式层**定理——
能隙比 2πe^{−γ}（3.53 为其数值近似）、同位素 √(1/2)、退化记号对应、
单调方向、能隙方程闭式解。P1–P5 中涉及材料参数与数值标定的部分
（λ 的氢亚晶格贡献比例、T_grav 的压力依赖、f 的标度）**不是** Lean 定理，
而是依据文献数值的模型预言，仍需实验证伪。剩余数值标定缺口
（σ、Θ_loop、f 的压力依赖）沿用 G9–G12。

---

## 5. 计算器使用说明

```bash
cd "08 超导"
python "CQM超导Tc计算器.py"                        # 验证表 + 同位素 + CQM 预言
python "CQM超导Tc计算器.py" 1330 1.94 0.123        # 自定义: ω_ln(K) λ μ*
```

公式与 `06 Lean形式化/Superconductivity/Reduction.lean` 逐项对应
（bcs_tc ↔ `bcsCriticalTemperature`，mcmillan_dynes_tc ↔ `mcmillanDynesTc`，
isotope_tc_ratio ↔ `criticalTemperature_isotope_shift`）。

---

## 参考文献

1. Bardeen, Cooper, Schrieffer (1957). Theory of Superconductivity. *Phys. Rev.* 108, 1175.
2. McMillan (1968). Transition Temperature of Strong-Coupled Superconductors. *Phys. Rev.* 167, 331.
3. Allen, Dynes (1975). *Phys. Rev. B* 12, 905.
4. Drozdov et al. (2015). Conventional superconductivity at 203 K at high pressures in the sulfur hydride system. *Nature* 525, 73.
5. Drozdov et al. (2019). Superconductivity at 250 K in lanthanum hydride under high pressures. *Nature* 569, 528.
6. Errea et al. (2016). Quantum crystal structure in the 250-kelvin superconducting phase of H3S. *PRL* 117, 065502.
7. Errea et al. (2020). Quantum crystal structure in the 250-kelvin superconducting phase of LaH10. *Nature* 578, 66.
8. Szczęśniak, Durajski (2016). Migdal-Eliashberg equations — the effective model for superconducting state in H3S. arXiv:1609.06079.
9. Liu et al. (2019). Microscopic mechanism of room-temperature superconductivity in compressed LaH10. *Phys. Rev. B* 99, 140501(R).
10. ruster (2026). CQM 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
