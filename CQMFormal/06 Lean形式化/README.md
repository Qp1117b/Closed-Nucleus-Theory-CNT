# CQMFormal — CQM 的 Lean 4 形式化验证

本目录包含**耦合常数量子力学（CQM）**的 Lean 4 形式化验证项目。

## 编译状态

✅ **全部 9 个库编译通过**（3334 jobs） | Lean 4.29.1 | **零 CQM 警告**

> 注：构建过程中 8 条 Mathlib 内部 ProofWidgets 模块重复注册警告来自 Mathlib 4.29.1 上游，
> 非 CQM 代码问题，无法从本项目消除。`lake build` 完全成功。 -/

## 库结构

| 库 | 文件 | 关键类型/定理 |
|:---|:---|:---|
| **CausalSet** | `Basic.lean`, `Reproduction.lean`, `Sprinkling.lean`, `Axioms.lean` | `CausalSet`、`ReproductionOperator`、`asymm`、`sprinklingDensity` |
| **CouplingSpace** | `Basic.lean`, `Uncertainty.lean` | `couplingStrength`、`CanonicalCommutation`、`robertson_ccr_inequality` |
| **CartanAlgebra** | `Basic.lean` | `cartanA4`、本征值精确表达式、`dynkinIndex`、`simplexEulerChar` |
| **SpectralGeometry** | `Basic.lean`, `Mathieu.lean`, `RiemannXi.lean` | `spectralQuantum`、`mathieuParameter`、`goldenRatio`、`adeleCycle`、Sierra-CQM 耦谱、黎曼 ξ 函数 |
| **Decoherence** | `Basic.lean` | `confinementScale`、`CausalLayer`、三层结构 |
| **PhysicalConstants** | `Basic.lean` | `GN_spectral_formula`、`alpha_inverse_SU5`、CODATA 偏差 |
| **Superconductivity** | `Ontology.lean`, `Gravity.lean`, `Mechanism.lean`, `Integral.lean`, `TransitionTemperature.lean`, `StrongGravity.lean`, `Reduction.lean` | 强引力超导：有限本体论、τ_res/ω_causal、三方因果闭环、涌现积分、T_c、T_grav、**BCS 退化与还原** |

## 形式化推导链

```
Axioms
├── A0.1-3: 因果集 + 再生产算子
│   ├── 因果偏序非对称性 (asymm)
│   ├── Alexandrov 区间有限性 (interval_finite)
│   ├── 再生产幂等性 (muHat_idempotent)
│   └── Sprinkling → 耦合空间 (u, τ)
│       ├── Sprinkling 密度 ρ(u) = exp(u)
│       ├── 耦合速度 c = 1/ρ
│       └── 保序嵌入 (sprinkling_preserves_order)
│
├── A1.1: 正则对易关系 [û, p̂_u] = i
│   ├── 耦合强度 r = exp(u) > 0
│   ├── 耦合坐标 u = ln r
│   ├── 不确定性关系 Δr/⟨r⟩ · Δv_τ ≥ C/2 (Robertson 不等式)
│   └── 14 个辅助定理（中心化算子、方差、Hermitian 性等）
│
├── H3.3 + A2.1: 退相干稳态 = 正四单纯形 → A₄ 嘉当矩阵
│   ├── 对称性: A₄_{ij} = A₄_{ji}
│   ├── 迹 = 8, 行列式 = 5
│   ├── Aₙ 行列式 = n+1 (A₁:2, A₂:3, A₃:4, A₄:5)
│   ├── 本征值精确表达式:
│   │   λ₁ = (3-√5)/2, λ₂ = (5-√5)/2
│   │   λ₃ = (3+√5)/2, λ₄ = (5+√5)/2
│   ├── 本征值之和 = 8, 之积 = 5
│   ├── 逆嘉当矩阵 A₄⁻¹ 显式条目
│   ├── 正定性: 所有主子式 > 0
│   ├── 4-单纯形 f-向量回文性 (5,10,10,5)
│   ├── SU(5) Weyl 群 = S₅ = 4-单纯形对称群
│   └── Dynkin 指数 I = 5/3
│
├── A2.2: 谱量子 C = ξ'(1)/ξ(1)
│   ├── Mathieu 参数 q = φ/2（黄金比例一半，从 A₄ 本征值严格导出）
│   │   ├── φ = (1+√5)/2, φ² = φ + 1
│   │   ├── q = (λ₄-λ₁)/(λ₄+λ₁) = φ/2 ≈ 0.809
│   │   └── λ₄/λ₁ = 5+2√5 ≈ 9.472
│   ├── Mathieu 临界值 λ_c（系统在稳定区: q < λ_c）
│   ├── 第一耦级 𝔠₁ (Sierra-CQM: 𝔠_n = 1/4 + γ_n²)
│   ├── Adele 周期 N_cycle = 30
│   ├── 4-单纯形 f-向量和 = 30 = N_cycle
│   ├── 谱修正因子 κ = (31+C)/30
│   ├── G_N 因子 F(C) = C²·𝔠₁·exp(-2/C)·(1+κC)
│   ├── F(C) 严格为正
│   └── 谱常数网络: C·λ_c·𝔠₁ ∈ (6, 10)
│
├── 素数结构
│   ├── 活跃素数 {2, 3, 5}：Φ(k) > 0 的唯一素数
│   ├── 素数冻结定理：∀ k > 5, Φ(k) = 0 (axiom)
│   ├── N_cycle = 2·3·5 = 30 = 活跃素数积
│   └── 活跃素数个数 3 = rank(SU(5)) - 1
│
├── 退相干三层结构 L1/L2/L3
│   ├── 禁闭标度 L = 1
│   ├── 退相干条件 ρ(u) ≥ L
│   └── 退相干速率 Γ(u) = ρ(u)
│
└── m_p（实验输入）
    └── G_N = I·λ_c·C²·𝔠₁·exp(-2/C)·(1+κC) / m_p²
        ├── G_N > 0（严格正性）
        ├── G_N 因子分解
        ├── 层级因子 exp(-2/C) ≈ 10⁻³⁸
        ├── CODATA 偏差 < 10 ppm
        └── α⁻¹_SU(5) = 16384π/375 ≈ 137.27
            ├── 137 < α⁻¹_SU(5) < 138
            ├── 群论因子 = 2^14/(3×5^3) = 16384/375
            ├── α_SU(5) > 0
            └── 0.007 < α_SU(5) < 0.01
```

## 定理统计

| 库 | 已证明定理 | 公理/待证 |
|:---|:---:|:---:|
| CausalSet | 22 | 4 |
| CouplingSpace | 21 | 0 |
| CartanAlgebra | 30 | 0 |
| SpectralGeometry | 81 | 4 |
| Decoherence | 6 | 0 |
| PhysicalConstants | 20 | 0 |
| Superconductivity | 59 | 5 |
| **总计** | **239** | **13** |

## 已知缺口

| 缺口 | 描述 | 涉及库 | 状态 |
|:---|:---|:---|:---:|
| G5 | 退相干 = 禁闭的严格推导 | `CausalSet/Axioms` | `axiom` (H3.1) |
| G5 | 非交换 → 交换几何相变 | `CausalSet/Axioms` | `axiom` (H3.2) |
| A | 退相干稳态 = 正四单纯形 | `CausalSet/Axioms` | `axiom` (H3.3) |
| — | Sierra-CQM 耦谱定理严格证明 | `SpectralGeometry` | 数值验证 (偏差 < 1e-8) |
| — | Mathieu 第一特征值 b₁(q) | `SpectralGeometry` | `axiom` (待 Mathieu 函数理论) |
| — | 素数冻结定理严格证明 | `SpectralGeometry` | 数值验证 (100% 成功率) |
| — | Adele 约束 ∏_p ℤ_p = 1/30（有限乘积形式） | `SpectralGeometry` | 已证明 (`native_decide`) |
| — | 谱量子 C = ξ'(1)/ξ(1) 的闭式表达式 | `SpectralGeometry` | 已严格证明 |

## 编译命令

```bash
cd "06 Lean形式化"
lake build                    # 编译全部
lake build CausalSet          # 编译单个库
lake build CartanAlgebra      # 编译嘉当代数库
lake build SpectralGeometry   # 编译谱几何库（含 Mathieu）
lake build Superconductivity  # 编译强引力超导库（7 模块）
```

## 理论对应

| CQM 理论 | Lean 库 | 核心定理数 |
|:---|:---|:---:|
| 因果集本体论 | `CausalSet` | 22 |
| 耦合空间与不确定性 | `CouplingSpace` | 21 |
| SU(5) 嘉当矩阵 | `CartanAlgebra` | 30 |
| 谱几何与 Mathieu 方程 | `SpectralGeometry` | 81 |
| 禁闭-退相干等价 | `Decoherence` | 6 |
| G_N 谱公式与 α⁻¹ | `PhysicalConstants` | 20 |
| 强引力超导涌现 | `Superconductivity` | 59 |

## 本次更新亮点 (v0.5.3)

- **BCS 退化与还原**：新增 `Reduction.lean`（19 定理 + 1 引理）；`cqm_reduces_to_bcs` / `cqm_debye_reduction` 为记号对应层定理；`criticalTemperature` 改用精确 BCS 常数 2e^γ/π（`bcsExactConstant`，文献 1.13 是其三位近似）
- **能隙方程的严格推导**：`bcs_gap_equation` / `bcs_gap_equation_unique` 从 T=0 能隙方程 1 = λ·arsinh(ω_D/Δ) 导出唯一闭式解 Δ = ω_D/sinh(1/λ)；`bcs_gap_weak_coupling_limit` 证明 λ→0⁺ 时闭式解渐近于 BCS 标准式 2ω_D·e^{−1/λ}（极限定理，非有限 λ 等式）
- **普适能隙比（精确）**：2Δ₀/k_BT_c = 2πe^{−γ} ≈ 3.5278（文献 3.53、旧公式 4/1.13 均为数值近似）——`bcs_universal_gap_ratio`
- **同位素定律**：α = 1/2（`criticalTemperature_isotope_shift`）、氢/氘位移 T_c(D) = T_c(H)/√2（`hydrogen_deuterium_isotope_shift`）
- **朴素 CQM 异常（条件定理）**：`naive_cqm_isotope_anomaly` 只证明朴素替换下 T_c 随质量单调不减、与实验相反；它标示、而非证明退化的必要性
- **严格性整治**：消除 4/1.13 循环论证；能隙公式从凭空定义改为能隙方程推导；所有数值近似（1.13、3.53、0.707、1.2、1.04）在文档字符串中如实标注，不冒充定理结论
- **公理依赖审计（`#print axioms`）**：`criticalTemperature_pos`、`bcs_universal_gap_ratio`、`bcs_gap_equation(_unique)`、`bcs_gap_weak_coupling_limit`、同位素三定理、`emergenceIntegral_pos`、`strong_gravity_keeps_pairing_channels` 等全部只依赖 Lean 内核逻辑公理（`propext`、`Classical.choice`、`Quot.sound`），**不依赖任何 `physical_hypothesis` 本体论公理**——物理假设仅作公理存在、未冒充定理结论
- **金属氢机制文档与计算器**：`08 超导/CQM 超导 金属氢机制与计算框架.md`（H3S 203 K / LaH10 250 K / MgB2 39 K 验证）+ `CQM超导Tc计算器.py`（BCS/McMillan–Dynes/同位素）
- **室温方向文档**：`08 超导/CQM 室温超导方向.md`（三条路线 + 同位素指数 α(P) 判别性实验）

## 本次更新亮点 (v0.5.2)

- **新增强引力超导库**：`Superconductivity`（6 模块，38 定理 / 5 公理），对应 [08 超导](../08%20超导/) 两卷文档
- **分层映射**：Ontology（第 1–2 层有限本体论）→ Gravity（第 3 层引力因果限制场）→ Mechanism（第 4–5 层超导机制）→ Integral（第 6–7 层涌现积分）→ TransitionTemperature（第 8 层 T_c）→ StrongGravity（第 9 层强引力修正）
- **核心定理**：`fourSimplex_euler_char_zero`、`causalCutoff_eq_two_pi_over_resolution`（ω_causal=2π/τ_res）、`strong_gravity_does_not_lower_causal_cutoff`、`superconductivity_requires_relation_network`、`tripleLoopStrength_locked_pos`、`emergenceIntegral_pos`、`criticalTemperature_pos`、`neutronStar_cutoff_blueshift`
- **新公理**：5 条 `physical_hypothesis`（有限本体/缺陷体/禁闭几何/内部量子引力/电子封装），沿用 CausalSet.Axioms 不透明公理模式

## 本次更新亮点 (v0.5.0)

- **消除所有 CQM 警告**：零 CQM 代码警告，构建完全清洁 ✅
- **修复 Mathieu.lean 矛盾公理**：`b1` 从占位符 `def ... := 0` 改为不透明 `axiom`，消除与 `mathieu_stable_region` 的逻辑矛盾
- **移除 4 个未使用的裸 `Prop` 公理**：`sierra_cqm_coupling_spectrum`、`prime_freezing_theorem`、`adele_constraint`、`coupling_formula_pi_factor` 替换为文档注释
- **修复文档错误**：`firstCoupling_sierraCQM_matches` → `firstCoupling_sierraCQM_deviation`、`spectralProduct_lt_one` → `spectralProduct_lt_ten`
- **定理总数**：从 96 → 160（+64 个严格证明的定理，得益于完整计数）
- **公理数**：从 14 → 7（减少 50%，消除所有未使用的声明）
- **Robertson 不等式**：从 CCR 严格推导（14 个辅助定理，无 `sorry`）✅
- **α⁻¹_SU(5) = 16384π/375**：从 A₄ 群论不变量严格证明 137 < α⁻¹ < 138 ✅
- **G_N 谱公式**：严格正性 + CODATA 偏差 < 10 ppm ✅

## 本次更新亮点 (v0.5.1)

- **Adele 约束严格化**：将 `adeleConstraint` 从公理改为由 `native_decide` 直接证明的定理，消除一个不必要的公理
- **删除未使用公理**：移除 `mathieu_critical_condition`（对占位函数 `b1` 的任意约束，且无任何定理引用）
- **清理测试残留**：删除未加入 `lakefile.toml` 且含 `sorry` 的 `TestNum.lean`
- **更新定理/公理统计**：按实际代码重新计数，当前 180 个定理 / 8 个公理（含物理假设与数值桥梁）
- **消除虚假精确等式**：谱量子 `C` 严格定义为 `1 + γ/2 - (1/2)ln(4π)`，数值近似以区间公理显式标注

## 版本

- **项目版本**: 0.5.3
- **Lean 版本**: 4.29.1
- **依赖**: mathlib, physlib
- **最后更新**: 2026-08-05