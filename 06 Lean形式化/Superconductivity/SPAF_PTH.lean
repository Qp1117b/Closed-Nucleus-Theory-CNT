import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Superconductivity.SPAF
import Superconductivity.Reduction
import Superconductivity.FirstPrinciples
import Superconductivity.CartanSuperconductivity

/-!
# CQM SPAF 压强-温度-磁场完整三相框架 (P-T-H Semi-Phenomenological Framework)

本模块在 SPAF.lean 的基础上，建立完整的超导三相半唯像框架：
**压强 (P) — 温度 (T) — 磁场 (H)**。覆盖以下物理内容：

## 1. 压强标度律（SPAF §6.1）
- 德拜频率与压强的标度关系：ω_D(P) = ω_D(P₀) · (P/P₀)^γ
- 电子-声子耦合与压强的标度关系：λ(P) = λ(P₀) · (P/P₀)^δ
- 中子缺陷参数 ε 的压强依赖性（高压下缺陷位被压缩 → ε 减小）

## 2. 临界磁场（SPAF §6.2）
- 热力学临界场 H_c(T) = H_c(0) · [1 − (T/T_c)²]
- 第 I 类超导体：H_c 即相界
- 第 II 类超导体：下临界场 H_c1(T) 和上临界场 H_c2(T)
- Ginzburg-Landau 参数 κ = λ_L/ξ 与超导分类

## 3. 超导分类学（SPAF §6.3）
- 第 I 类（经典元素超导体：Al, Pb, Sn 等）
- 第 II 类（传统合金 + 高压氢化物）
- 高温超导体（铜氧化物，非 BCS 配对机制）
- CQM 分类判据：因果网络完整性、缺陷本体浓度、引力拓扑因子

## 4. CQM 第一性约束（SPAF §6.4）
- 中子缺陷正定条件：ε < 5/4 ⟹ 因果网络可支撑超导
- 压强-缺陷竞争：高压压缩缺陷位 → ε(P) 递减
- 引力拓扑因子 T_grav ≥ 1（强引力不破坏超导，只增强因果锁定）
- 网络完整性：缺陷本体浓度超过阈值则超导消失

## 定理一览
- [pressureScaling_valid]：压强标度律的形式有效性（正压 → 正 ω_D, λ）
- [criticalField_T_dependence]：H_c(T) 的抛物型温度依赖
- [upperCriticalField_T_dependence]：H_c2(T) 的 WHH 型温度依赖
- [superconductorType_iff_kappa]：GL 参数 κ 与超导类型的对应关系
- [cqm_pressure_defect_coupling]：CQM 压强-缺陷-耦合的三方约束
- [roomTemperature_feasibility_with_pressure]：含压强约束的室温可行域
- [phaseDiagram_boundary_monotone]：相界的单调性（T_c 随 P 非单调，H_c 随 T 单调减）

## 参考文献
- Ginzburg, Landau (1950). On the Theory of Superconductivity.
- Werthamer, Helfand, Hohenberg (1966). Phys. Rev. 147, 295.
- McMillan (1968). Transition Temperature of Strong-Coupled Superconductors.
- ruster (2026). CQM SPAF 半唯像应用框架. CQMFormal/08 超导/.
-/

namespace CQM

open scoped BigOperators

/-! ## 1. 压强标度律（SPAF §6.1） -/

/-- 参考压强 P₀（大气压 ≈ 0 GPa 或指定参考压力）。 -/
noncomputable def referencePressure : ℝ := 0

/-- 压强标度指数 γ 的物理范围：典型氢化物 γ ∈ [0.2, 0.5]。
    高压下晶格硬化 → ω_D 随 P 亚线性增长。 -/
noncomputable def pressureExponentOmega (gamma : ℝ) : Prop :=
  0 < gamma ∧ gamma < 1

/-- 德拜频率的压强标度律：ω_D(P) = ω_D(P₀) · (P/P₀)^γ。
    P₀ 为参考压强，γ 为 Grüneisen 型标度指数。
    此定义在 CQM 中对应：高压压缩减小禁闭几何的体积 → 提高 A₄ 循环刚度。 -/
noncomputable def debyeFrequencyAtPressure (omegaRef : ℝ) (pRef p gamma : ℝ) : ℝ :=
  omegaRef * (p / pRef) ^ gamma

/-- 电子-声子耦合的压强标度律：λ(P) = λ(P₀) · (P/P₀)^δ。
    δ 通常为负（高压下费米面态密度降低 → 耦合减弱）。
    这正是 LaH10 实验中 T_c(P) 非单调的原因：ω_D 与 λ 的竞争。 -/
noncomputable def couplingAtPressure (lamRef : ℝ) (pRef p delta : ℝ) : ℝ :=
  lamRef * (p / pRef) ^ delta

/-- 压强标度律在正压下的正性：正压 → 正 ω_D, 正 λ。 -/
theorem pressureScaling_valid {omegaRef lamRef pRef p gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : 0 < lamRef) (hpRef : 0 < pRef) (hp : 0 < p) :
    debyeFrequencyAtPressure omegaRef pRef p gamma > 0 ∧
    couplingAtPressure lamRef pRef p delta > 0 := by
  constructor
  · unfold debyeFrequencyAtPressure
    have h_div : 0 < p / pRef := div_pos hp hpRef
    have h_pow : 0 < (p / pRef) ^ gamma := Real.rpow_pos_of_pos h_div gamma
    exact mul_pos ho h_pow
  · unfold couplingAtPressure
    have h_div : 0 < p / pRef := div_pos hp hpRef
    have h_pow : 0 < (p / pRef) ^ delta := Real.rpow_pos_of_pos h_div delta
    exact mul_pos hl h_pow

/-- T_c 的压强依赖：T_c(P) = (2e^γ/π) · ω_D(P) · exp(−1/λ(P))。
    这是 T_c(P) 曲线的基本形式，由 ω_D(P) 和 λ(P) 的竞争决定。 -/
noncomputable def tcAtPressure (omegaRef lamRef pRef p gamma delta : ℝ) : ℝ :=
  bcsCriticalTemperature
    (debyeFrequencyAtPressure omegaRef pRef p gamma)
    (couplingAtPressure lamRef pRef p delta)

/-- 中子缺陷参数的压强依赖性：ε(P) = ε₀ · (P₀/P)^ν。
    高压压缩缺陷位 → 禁闭几何恢复 → ε 减小。
    当 P → ∞ 时 ε → 0，所有有限本体趋于理想质子。 -/
noncomputable def neutronDefectAtPressure (eps0 : ℝ) (pRef p nu : ℝ) : ℝ :=
  eps0 * (pRef / p) ^ nu

/-- 高压下中子缺陷趋于零：P → ∞ ⟹ ε(P) → 0（缺陷位被完全压缩）。
    这是 CQM 的独特预言：极限高压下所有重核都趋于纯质子 A₄ 网络。 -/
theorem neutronDefect_tendsto_zero_at_high_pressure {eps0 pRef nu : ℝ}
    (hpRef : 0 < pRef) (hnu : 0 < nu) :
    Filter.Tendsto (fun p : ℝ => neutronDefectAtPressure eps0 pRef p nu)
      Filter.atTop (Filter.𝓝 0) := by
  unfold neutronDefectAtPressure
  have h : Filter.Tendsto (fun p : ℝ => (pRef / p) ^ nu) Filter.atTop (Filter.𝓝 0) := by
    refine (tendsto_rpow_div_atTop hpRef hnu).mono_right ?_
    -- pRef/p → 0 as p → ∞
    have h_div : Filter.Tendsto (fun p : ℝ => pRef / p) Filter.atTop (Filter.𝓝 0) :=
      (tendsto_const_div_atTop_nhds_zero (𝕜 := ℝ)).comp Filter.tendsto_id
    -- 对 r > 0: r^nu → 0 as r → 0
    exact h_div.rpow_const (Or.inl hnu)
  simpa [mul_comm] using Filter.Tendsto.const_mul eps0 h

/-! ## 2. 临界磁场（SPAF §6.2） -/

/-- 热力学临界场 H_c(T) = H_c(0) · [1 − (T/T_c)²]。
    抛物型温度依赖，适用于第 I 类超导体。
    T ≥ T_c 时 H_c = 0（正常态）。 -/
noncomputable def thermodynamicCriticalField (hc0 tc temp : ℝ) : ℝ :=
  if temp < tc then hc0 * (1 - (temp / tc) ^ 2) else 0

/-- H_c(T) 在 T = 0 处取最大值 H_c(0)。 -/
theorem thermodynamicCriticalField_at_zero (hc0 tc : ℝ) (htc : tc > 0) :
    thermodynamicCriticalField hc0 tc 0 = hc0 := by
  unfold thermodynamicCriticalField
  have h : (0 : ℝ) < tc := htc
  simp [h]

/-- H_c(T) 在 T ≥ T_c 时为零（正常态）。 -/
theorem thermodynamicCriticalField_above_tc (hc0 tc temp : ℝ) (h : tc ≤ temp) :
    thermodynamicCriticalField hc0 tc temp = 0 := by
  unfold thermodynamicCriticalField
  simp [h]

/-- H_c(T) 关于温度单调不增：温度越高，临界场越低。 -/
theorem thermodynamicCriticalField_antitone_in_temp (hc0 tc t1 t2 : ℝ)
    (hc0pos : 0 ≤ hc0) (htc : 0 < tc) (h : t1 ≤ t2) :
    thermodynamicCriticalField hc0 tc t2 ≤ thermodynamicCriticalField hc0 tc t1 := by
  unfold thermodynamicCriticalField
  by_cases ht2 : t2 < tc
  · have ht1 : t1 < tc := lt_of_le_of_lt h