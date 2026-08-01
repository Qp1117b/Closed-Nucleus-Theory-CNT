import CausalSet.Basic
import CausalSet.Reproduction

/-!
# CQM 公理体系 (Axiom System)

本文档收集 CQM 的全部公理，按层级排列，标注每一条的状态。

## 公理状态标注
- `[AXIOM]` — 基本公理，不可从更基本的原则推导
- `[HYPOTHESIS]` — 物理假设，待从公理证明（对应严格性缺口）

## 公理层级

### 层级 0：本体论公理（CausalSet.Basic, CausalSet.Reproduction）
- **A0.1** `CausalSet` — 因果前导 `≺` 是严格偏序 + 局部有限性
- **A0.2** `CountableCausalSet` — 因果集可数性（Sprinkling 嵌入的必然结果）
- **A0.3** `ReproductionOperator` — 再生产算子 `μ̂` 是幂等线性算子

### 层级 1：耦合空间公理（CouplingSpace 库）
- **A1.1** `CanonicalCommutationRelation` — 耦合空间对易关系 [û, p̂_u] = i
- **A1.2** 耦合速度 `c = δu/δτ` 由因果集离散结构决定

### 层级 2：代数结构公理（CartanAlgebra 库）
- **A2.1** 禁闭边界的代数结构是 A₄ 嘉当矩阵
- **A2.2** 谱量子 `C = ξ'(1)/ξ(1)` 是基本常数

### 层级 3：物理假设（待证明）
- **H3.1** 禁闭 = 退相干（缺口 G5）
- **H3.2** 非交换 → 交换几何相变（缺口 G5）
- **H3.3** 退相干稳态 = 正四单纯形（缺口 A）

## 已证明的定理

从以上公理体系已严格证明的定理：

| 定理 | 库 | 证明状态 |
|:---|:---|:---:|
| 因果偏序非对称性 `asymm` | CausalSet | ✅ |
| Alexandrov 区间有限性 `interval_finite` | CausalSet | ✅ |
| 再生产幂等性 `muHat_idempotent` | CausalSet | ✅ |
| 存在子空间是线性子空间 | CausalSet | ✅ |
| 再生产算子的像 = 存在子空间 | CausalSet | ✅ |
| Sprinkling 密度严格为正 | CausalSet | ✅ |
| A₄ 对角元全为 2 | CartanAlgebra | ✅ |
| 4-单纯形 Euler 示性数为 0 | CartanAlgebra | ✅ |
| 谱常数严格为正 | SpectralGeometry | ✅ |
| G_N 谱公式严格为正 | PhysicalConstants | ✅ |
| α_SU(5) 严格为正 | PhysicalConstants | ✅ |

## 参考文献
- ruster (2026). CQM 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

open CausalSet

/-! ## 层级 3：物理假设（待从公理证明） -/

/-- [HYPOTHESIS H3.1] 禁闭 ⇔ 退相干等价。
    对应严格性缺口 G5。待从因果集第一性原理证明。 -/
axiom confinement_equiv_decoherence : True

/-- [HYPOTHESIS H3.2] 禁闭边界处非交换几何 → 交换几何的相变。
    对应严格性缺口 G5。 -/
axiom noncommutative_to_commutative_phase_transition : True

/-- [HYPOTHESIS H3.3] 退相干稳态是正四单纯形。
    对应严格性缺口 A（核心缺口）。 -/
axiom decoherence_steady_state_is_4simplex : True