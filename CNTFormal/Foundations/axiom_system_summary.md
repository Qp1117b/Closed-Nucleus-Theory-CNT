# DCNC 公理体系总览

> 闭合核理论（Closed Nucleus Theory, CNT）形式化项目
> 生成日期：2026-05-23

---

## 前言

本文档完整梳理闭合核理论的公理体系结构，涵盖六条核心公理、所有已证明定理、工作假设、猜想，以及各命题之间的逻辑推导关系。**本文档列出所有已形式化的定理**。

---

## 符号约定

| 标记 | 含义 |
|------|------|
| **[A]** | 公理（Axiom），理论的出发点 |
| **[T]** | 定理（Theorem），已严格证明 |
| **[D]** | 定义（Definition），概念的形式化 |
| **[H]** | 工作假设（Working Hypothesis），临时假定 |
| **[C]** | 猜想（Conjecture），未证明 |
| **[S]** | 标记为 sorry（未完成） |

---

# 第一部分：CNTFormal 核心库

**严格性**：0 个 sorry，纯公理 + 严格证明的定理。

---

## 一、DCNC 六公理 [A]

### 公理 1：闭合核的充要条件（五判据）

范畴中的每个对象 S 若要成为闭合核，必须同时满足五个判据：

1. **操作闭合** —— 存在自态射 f: S→S 满足 f ∘ f = f
2. **自我指涉** —— 存在子对象分解 S_in, S_out
3. **再生产** —— 存在结合态射 μ: S→S 满足 μ ∘ μ = μ
4. **条件债务** —— 存在非可逆态射 ε: S→S
5. **历史沉淀** —— 存在适应度函子和选择性余极限

### 公理 2：选择性余极限的存在性

存在适应度函子 F: C→ℝ 和选择性余极限 colim，使得候选稳定态集合非空且所有候选态的适应度非负。

### 公理 3：历史路径的不可逆性

对于任意非可逆态射 f: S→S，不存在 g: S→S 使得 f ∘ g = id_S。等价于：历史不可逆——闭合核不能通过有限步骤精确回到之前的状态。

### 公理 4：再生产的结合性（幂等性）

所有自态射都满足幂等性：μ ∘ μ = μ。

### 公理 5：适应度函子的单调性

若存在态射 f: X→Y，则适应度满足 fitness(X) ≤ fitness(Y)。

### 公理 6：闭合核的个体化

同构的闭合核必然相等。如果闭核 S₁ 与 S₂ 同构，则 S₁ = S₂。

---

## 二、核心定义 [D]

| 定义 | 说明 |
|------|------|
| **FitnessFunctor** | 适应度函子：C→ℝ 且单调 |
| **SelectiveColimit** | 选择性余极限：从候选集选择最优态，含选择最优性和收敛性 |
| **CNTCriteria** | 闭合核五判据结构体 |
| **CNTCategory** | CNT范畴类型类，继承 CNTCriteria |
| **BerryPhase** | Berry相位的几何定义（底空间、纤维、联络、曲率） |
| **DissipativeBerryPhase** | 耗散Berry相位（含耗散率 γ>0） |
| **F₁ 基础范畴层** | F1_level = C |
| **F₂ 函子层** | F2_level = C ⥤ D |
| **F₃ 自然变换层** | F3_level = F ⟶ G |
| **F₄ 高阶函子层** | F4_level = (C⥤C)⥤(C⥤C) |
| **F₅ 选择性余极限层** | F5_level = C × ℝ |
| **Simplex4Hom** | 4-单纯形态射类型（id, mu, eps, comp） |
| **simplex4Comp** | 4-单纯形态射复合操作 |
| **CompactFormSpace** | 紧致形式空间（含直径 diameter > 0） |
| **ReproductionPeriodStrict** | 严格正再生产周期类型 {τ:ℝ // τ>0} |
| **HistoryDependentPeriod** | 历史依赖周期序列 ℕ→ReproductionPeriodStrict |
| **FitnessPeriodRelation** | 适应度-周期关系（单调递减函数） |
| **FitnessSequenceBounded** | 适应度序列有上界 |
| **PhysicalQuantity** | 物理量类型（电荷、质量、自旋、磁矩、稳定性、耦合常数） |
| **PhysicalMeasurement** | 物理量测量函子（保持同构） |
| **ChargeFunctor** | 电荷函子（拓扑不变量，整数量子化） |
| **SpinFunctor** | 自旋函子（半整数量子化 n/2） |
| **MagneticMomentFunctor** | 磁矩函子（电荷×自旋×g因子） |
| **StabilityFunctor** | 结构稳定性函子（稳定性=适应度） |
| **FourSimplexVertex** | 4-单纯形顶点类型（5个顶点） |
| **FormNumber** | 形式数类型 ℕ×ℕ×ℕ |
| **formDist** | 形式距离（度量空间） |

---

## 三、已证明定理 [T]（完全严格，无 sorry）

### 3.1 公理间推导链

| # | 定理 | 说明 |
|---|------|------|
| T1 | **DedekindFiniteCategory** | CNT范畴是Dedekind-有限的：有右逆的自态射必为同构。从公理3直接导出 |
| T2 | **axiom1_implies_axiom3** | 公理1（条件债务）+ Dedekind有限性 ⟹ 公理3 |
| T3 | **axiom2_implies_axiom5** | 公理2（选择性余极限存在）⟹ 公理5（适应度单调） |
| T4 | **axiom4_implies_quantization** | 公理4（幂等性）⟹ 物理量量子化结构（IdempotentSpectrum） |
| T5 | **closed_nucleus_uniqueness** | 公理6（个体化）⟹ 闭合核唯一性：同构⇒相等 |
| T6 | **dcnc_axiom_derivation_chain** | 以上全部推导的组合定理 |

### 3.2 公理系统一致性

| # | 定理 | 说明 |
|---|------|------|
| T7 | **axiom1_axiom3_compatibility** | 公理1与公理3兼容：操作闭合存在 ⇒ 存在非可逆态射 |
| T8 | **axiom4_category_associativity_consistency** | 公理4与范畴论结合律一致 |
| T9 | **simplex4_consistent_with_DCNC** | 4-单纯形假设与DCNC六公理自洽 |

### 3.3 4-单纯形几何与自洽性

| # | 定理 | 说明 |
|---|------|------|
| T10 | **simplex4_assoc** | 4-单纯形范畴结合律成立 |
| T11 | **simplex4_id_left / id_right** | 4-单纯形范畴单位律成立 |
| T12 | **simplex4_mu_idem** | μ ∘ μ = μ 在4-单纯形中成立（公理4） |
| T13 | **simplex4_eps_not_iso'** | ε 没有左逆（公理3） |
| T14 | **simplex4_fitness / simplex4_colim** | 适应度函子和选择性余极限在4-单纯形上可定义 |

### 3.4 4-单纯形组合拓扑

| # | 定理 | 说明 |
|---|------|------|
| T15 | **simplex4_euler_verify** | 4-单纯形欧拉示性数 χ=1 |
| T16 | **simplex4_is_compact** | 4-单纯形是紧致的（有限点集凸包） |

### 3.5 辐射速度与光速

| # | 定理 | 说明 |
|---|------|------|
| T17 | **radiative_velocity_bounded** | 辐射速度有上界：v_rad ≤ D_max/τ |
| T18 | **speedOfLightCandidate** | 光速候选 c_candidate = D_max/τ |

### 3.6 4-单纯形几何到精细结构常数

| # | 定理 | 说明 |
|---|------|------|
| T19 | **cos_dihedral_eq** | cos(二面角) = 1/4 |
| T20 | **cos_five_dihedral** | cos(5Θ) = 61/64（Chebyshev多项式 T₅ 推导） |
| T21 | **sin_sq_five_dihedral** | sin²(5Θ) = 375/4096 |
| T22 | **inv_alpha_0_eq** | 1/α₀ = 16384π/375 |
| T23 | **inv_alpha_0_from_geometry** | 1/α₀ = 4π/sin²(φ) |
| T24 | **four_pi_factor_origin** | 4π因子来自SU(2)→U(1) Hopf纤维化球面立体角 |
| T25 | **simplex4_trig_identity** | cos²θ + sin²θ = 1 对4-单纯形二面角成立 |
| T26 | **bare_coupling_simplex_relation** | 裸耦合常数与4-单纯形几何相位的关系 |
| T27 | **pythagorean_identity** | 61² + 375×64 = 64²（cos²+sin²=1 的数值验证） |
| T28 | **inv_alpha_relation** | 16384 = 4×4096（4/sin²(φ)的数值等价） |

### 3.7 再生产周期

| # | 定理 | 说明 |
|---|------|------|
| T29 | **reproduction_period_positive** | 再生产周期严格大于零（从公理3+公理4推导） |
| T30 | **reproduction_period_lower_bound_exists** | 再生产周期下界存在 |
| T31 | **reproduction_frequency_positive** | 再生产频率严格为正 |
| T32 | **reproduction_frequency_finite** | 再生产频率有限 |
| T33 | **single_reproduction_action_eq_h** | 单次再生产作用量恒为 h |
| T34 | **n_reproduction_action_eq** | n 次再生产总作用量为 n·h |
| T35 | **discrete_time_slice_monotone** | 离散时间切片单调递增 |
| T36 | **discrete_time_slice_step** | 离散时间切片步长一致 |
| T37 | **discrete_time_slice_disjoint** | 离散时间切片互不相交 |
| T38 | **irreversibility_requires_positive_time** | 不可逆性需要正的时间 |

### 3.8 再生产辐射速度

| # | 定理 | 说明 |
|---|------|------|
| T39 | **radiative_velocity_positive** | 再生产辐射速度严格为正 |
| T40 | **radiative_velocity_unbounded_above** | 辐射速度在特定条件下无上界 |

### 3.9 历史累积效应

| # | 定理 | 说明 |
|---|------|------|
| T41 | **period_always_positive** | 历史依赖周期序列的每一项均为正 |
| T42 | **period_sequence_bounded_below** | 若适应度有上界，则周期序列有正下界 |
| T43 | **reproduction_action_invariant** | 单次再生产作用量与历史无关，恒为 h |

### 3.10 物理量映射

| # | 定理 | 说明 |
|---|------|------|
| T44 | **charge_quantization_theorem** | 电荷量子化：电荷函子的值取整数 |
| T45 | **alpha_from_category** | 精细结构常数可从范畴论几何结构表示 |
| T46 | **spin_intertwiner_relation** | 自旋与intertwiner维数的关系：dim = Catalan(N/2) |

### 3.11 公理对物理量的约束

| # | 定理 | 说明 |
|---|------|------|
| T47 | **axiom1_constraint** | 公理1 ⇒ 电荷量子化拓扑结构 |
| T48 | **axiom2_constraint** | 公理2 ⇒ 选择性余极限存在 |
| T49 | **axiom3_constraint** | 公理3 ⇒ 非可逆态射无右逆 |
| T50 | **axiom4_constraint** | 公理4 ⇒ 幂等性 |
| T51 | **axiom5_constraint** | 公理5 ⇒ 适应度单调性 |
| T52 | **axiom6_constraint** | 公理6 ⇒ 同构⇒相等 |

### 3.12 实验兼容性

| # | 定理 | 说明 |
|---|------|------|
| T53 | **axiom_system_experiment_compatibility** | 理论值 137.258 与实验值 137.036 的相对偏差 < 1% |

### 3.13 实验值定义

| # | 定义 | 说明 |
|---|------|------|
| D1 | **experimental_inv_alpha_codata** | CODATA 2018 实验值：137.035999084 |
| D2 | **absolute_deviation** | 理论值与实验值绝对偏差 |
| D3 | **relative_deviation** | 理论值与实验值相对偏差 |

---

## 四、KernelPerspective 补充文件

该文件**不被 CNTFormal.lean 导入**，因此其 sorry 不影响核心库严格性。

### 4.1 4-单纯形核视角结构

| 定义 | 说明 |
|------|------|
| **FourSimplexVertex** | 5个顶点的枚举类型 |
| **FourSimplexFace** | 4-单纯形的面类型（4个顶点的子集） |
| **allVertices** | 5个顶点的 Finset |
| **singletonFace** | 单�面的构造 |
| **boundaryFaces** | 5个边界面 |
| **oppositeFace** | 对径面（不含核顶点的面） |
| **facesContainingKernel** | 包含核顶点的面集合（4个） |
| **IsVisibleFrom** | 可见性公理（核顶点k能"看到"的面） |
| **kernelPerspective** | 核视角公理：存在唯一的核顶点使可见面恰为3个 |
| **stabilizerSubgroup** | 稳定子群 |
| **ProductChannel** | 产物通道 = visibleFaces |
| **HistoryFace** | 历史面 = oppositeFace |

### 4.2 Kernel 已证明定理

| # | 定理 | 说明 |
|---|------|------|
| T54 | **allVertices_card** | 顶点总数为5 |
| T55 | **boundaryFaces_card** | 边界面总数为5 |
| T56 | **facesContainingKernel_card** | 包含核的面恰为4个 |
| T57 | **oppositeFace_card** | 对径面包含4个顶点 |
| T58 | **kernelBreaksSymmetryToS4** | 核的存在将S₅对称性破缺到S₄ |
| T59 | **threeVisibleFacesDistinguishable** | 3个可见面可区分 |
| T60 | **oppositeFaceNotVisible** | 对径面不可见（不在可见面中） |
| T61 | **historyFaceAccumulatesHPI** | 历史面对径面承载HPI累积 |
| T62 | **trichotomyOfBoundary** | 边界三分性定理：5个边界面=3个可见面+1个对径面+1个盲区面 |

**特殊情况**：
| # | 定理 | 状态 |
|---|------|------|
| T63 | **kernelBreaksSymmetryToS3** | 核的存在将S₄进一步破缺到S₃（基数不匹配问题） |
| T64 | **formDistIsMetric** | 形式距离的5条度量公理：（1）非负性、（2）对称性、（3）自距离为零、（4）三角不等式、（5）正定性，全部已证明 |

---

# 第二部分：CNTConjectures 猜想库

**严格性**：允许 sorry，包含工作假设和猜想。

---

## 五、IdempotentQuantization 幂等算子量子化

### 5.1 已证明定理

| # | 定理 | 说明 |
|---|------|------|
| T65 | **idempotent_eigenvalue_equation** | 幂等算子 μ²=μ 的特征值满足 λ²=λ |
| T66 | **idempotent_eigenvalues_binary** | 幂等算子特征值只能是 0 或 1 |
| T67 | **physical_quantity_quantization** | 物理量量子化：幂等算子测量结果离散化 |
| T68 | **projection_operator_quantization** | 投影算子量子化 |
| T69 | **idempotent_trace_is_nat** | 幂等算子迹等于像空间维数（自然数） |
| T70 | **idempotent_trace_is_integer_conjecture** | 幂等算子迹为整数 |

### 5.2 未完��证明

| # | 定理 | 状态 | 说明 |
|---|------|------|------|
| T71 | **idempotent_trace_is_finrank** | [S] | 迹=finrank：依赖 mathlib 谱分解基础设施（Submodule.isCompl, trace_add），当前版本缺失 |

---

## 六、AxiomDerivationChain 公理推导链

### 6.1 已证明

| # | 定理 | 说明 |
|---|------|------|
| T72 | **CNTCategory_is_DedekindFinite** | CNT范畴是Dedekind-有限的 |
| T73 | **axiom1_implies_axiom3**（重复，在核心库之外重证） | 公理1⇒公理3 |
| T74 | **axiom2_implies_axiom5**（重复） | 公理2⇒公理5 |
| T75 | **axiom4_implies_quantization**（重复） | 公理4⇒量子化 |
| T76 | **closed_nucleus_uniqueness**（重复） | 公理6⇒唯一性 |

### 6.2 已证明引理

| # | 定理 | 说明 |
|---|------|------|
| L1 | **not_iso_implies_no_right_inverse** | 非可逆态射⇒无右逆（Dedekind-有限范畴中） |

---

## 七、OntologicalMechanics 存在论力学

### 7.1 定义

| 定义 | 说明 |
|------|------|
| **ReproductiveEvent** | 再生产事件（态射+幂等性） |
| **ReproductiveHistory** | 再生产历史（事件列表） |
| **BackactionSystem** | 再生产反作用系统（反作用严格正） |
| **HPISystem** | 历史路径积分系统（HPI=Σ backaction×Δτ） |
| **ConditionDebt** | 条件债务（非可逆态射+程度度量） |
| **OntologicalMechanics** | 存在论力学类型类（含反作用、HPI、历史沉淀、锁定条件） |
| **ReproductivePerturbation** | 再生产扰动 |
| **HPILockCondition** | HPI锁定条件 |
| **EffectiveActionLimit** | 有效作用量极限 |
| **TimeArrowedClosedNucleus** | 时间箭头范畴 |
| **replace_event_at** | 替换历史中的事件 |
| **perturb_history** | 历史扰动函数 |
| **hpi_variation** | HPI变分（δ=HPI(扰动)-HPI(原始)） |

### 7.2 已证明定理

| # | 定理 | 说明 |
|---|------|------|
| T77 | **lock_implies_hpi_variation_zero** | HPI锁定⇒HPI变分为零 |
| T78 | **hpi_stationary_iff_locked_conjecture**（→方向已证，←方向通过工作假设） | HPI平稳⇔历史沉淀锁定 |
| T79 | **backaction_lagrangian_correspondence_conjecture**（部分） | 反作用严格为正已证明 |
| T80 | **time_arrow_from_axiom3** | 时间箭头存在性（从公理3推导） |

### 7.3 工作假设 [H]

| 假设 | 说明 |
|------|------|
| **historicalPrecipitation** | 历史沉淀锁定条件 |
| **hpi_variation_stationary_implies_precipitation** | HPI平稳⇒历史沉淀锁定（变分原理逆命题） |
| **HPILockCondition** | 锁定状态下单事件扰动不改变HPI |
| **EffectiveActionLimit** | 条件债务→0时HPI退化为标准作用量 |

---

## 八、HPICorrection 和 HPIAxiomCorrespondence（HPI修正，研究暂停）

### 8.1 定义

| 定义 | 说明 |
|------|------|
| **HPICorrection** | HPI修正结构体（含4个修正项） |
| **standard_hpi_correction** | 标准HPI修正（4项之和） |
| **hpi_total_correction** | HPI修正求 |
| **corrected_inv_alpha** | 修正后的精细结构常数倒数 = inv_alpha_0 + 修正 |

### 8.2 修正项定义

| 项 | 表达式 | 对应公理 |
|----|--------|---------|
| **boundary_fluctuation** | 1/√Catalan(4) | 公理3（历史记忆） |
| **topological_defect** | 1/(4π) | 公理1（拓扑结构） |
| **multi_path_interference** | cos(5Θ)/(2π) | 公理2（路径叠加） |
| **running_coupling** | β函数修正 | 公理5（能标单调） |

### 8.3 已证明定理

| # | 定理 | 状态 | 说明 |
|---|------|------|------|
| T81 | **original_deviation_value** | ✅ | 原始偏差值已计算 |
| T82 | **hpi_correction_moves_away_from_experiment** | [S] | HPI修正使偏差增大（HPI研究暂停） |
| T83 | **boundary_fluctuation_axiom3_correspondence** | ✅ | 边界涨落⇔公理3对应 |
| T84 | **topological_defect_axiom1_correspondence** | ✅ | 拓扑缺陷⇔公理1对应 |
| T85 | **interference_axiom2_correspondence** | ✅ | 多路径干涉⇔公理2对应 |
| T86 | **running_coupling_axiom5_correspondence** | ✅ | 能标跑动⇔公理5对应 |
| T87 | **hpi_idempotency_breakdown_analysis** | ✅ | HPI修正下幂等性偏差的代数分析：δ=c(2μ-1+c) |
| T88 | **hpi_idempotency_deviation_magnitude** | [S] | HPI修正下幂等性不保持 |
| T89 | **axiom4_hpi_correspondence_impossible** | [S] | 不存在满足公理4约束的非零HPI修正 |
| T90 | **axiom6_hpi_correspondence** | ✅ | 公理6约束下HPI修正确立唯一性 |
| T91 | **hpi_correction_axiom_constraint** | ✅ | HPI修正满足所有公理约束的分解 |

---

## 九、ReproductionEnergy 再生产能量

### 9.1 定义

| 定义 | 说明 |
|------|------|
| **QuantaPeriodCoupling** | 能量子-周期耦合关系 |
| **MaterialFormConservation** | 材料-形式守恒（能量子守恒+形式变化+不可逆） |
| **ReproductionSignature** | 再生产签名（链接范畴对象与物理量） |
| **NucleusState / ReproductionStep** | 核状态与再生产步骤 |
| **FormFixedPoint** | 形式不动点 |
| **FormMark / FormDirection** | 形式标记与方向 |
| **FormConfiguration** | 形式构型空间 |
| **FormGraph** | 形式图（多核连通结构） |

### 9.2 工作假设 [H]

| 假设 | 说明 |
|------|------|
| **reproduction_quanta_period_coupled** | 能量子-周期耦合 |
| **reproduction_uncertainty_allowed** | 再生产不确定性范围 |
| **reproduction_satisfies_material_form_conservation** | 材料-形式守恒 |
| **every_nucleus_has_reproduction_signature** | 每个闭合核有再生产签名 |

### 9.3 已证明定理

| # | 定理 | 说明 |
|---|------|------|
| T92 | **conservatism_supports_idempotency** | 材料守恒⇒幂等性物理合理性 |
| T93 | **quanta_count_is_invariant** | 能量子数在再生产中守恒 |
| T94 | **form_changes_in_reproduction** | 形式在再生产中改变 |
| T95 | **reproduction_changes_nucleus_state** | 再生产改变核状态 |
| T96 | **fixed_point_supports_idempotency** | 形式不动点⇒幂等性 |
| T97 | **form_stability_implies_physical_idempotency** | 形式稳定⇒物理幂等性 |
| T98 | **formDist_nonneg** | 形式距离非负 |
| T99 | **formDist_symm** | 形式距离对称 |
| T100 | **formDist_self** | 形式距离自距离为零 |
| T101 | **formDist_triangle** | 形式距离三角不等式 |
| T102 | **formDist_zero_iff** | 形式距离为零⇔形式相等 |
| T103 | **nuclearProductDistance_pos_iff** | 核-产物距离为正⇔核形式≠产物形式 |
| T104 | **internuclearDistance_symm** | 核间距离对称 |
| T105 | **internuclearDistance_nonneg** | 核间距离非负 |
| T106 | **space_and_motion_emerge** | 空间与运动从再生产涌现（综述定理） |
| T107 | **phase1_no_universal_connection** | 第一阶段：孤立离散核之间无普适连接 |
| T108 | **reproduction_establishes_network_connection** | 再生产建立核间网络连接 |
| T109 | **phase2_universal_connection_emerges** | 第二阶段：普适连接涌现 |
| T110 | **classical_spacetime_emerges_framework** | 第三阶段：经典时空涌现框架 |

---

## 十、IntertwinerStructure

### 10.1 定义

| 定义 | 说明 |
|------|------|
| **intertwiner_space** | Intertwiner空间（Hom集合） |
| **intertwiner_dim_nat** | Intertwiner维数 |
| **catalan_number** | Catalan数：C(2k, k)/(k+1) |

### 10.2 已证明定理

| # | 定理 | 说明 |
|---|------|------|
| T111 | **He4_intertwiner_dim_value** | 4价intertwiner（He⁴）的维数为2 |
| T112 | **He4_intertwiner_dim_catalan** | 4价intertwiner维数=Catalan数(2)=2 |
| T113 | **intertwiner_reproduction_associativity** | Intertwiner再生产结合性 |

---

## 十一、证明状态总结

```
总共统计
━━━━━━━━━━━━━━━━━━━━━━
CNTFormal 核心库：  6 公理 + 13 核心定义 + 53 已证明定理
                   含 4-单纯形几何、再生产周期、精细结构常数推导、
                   辐射速度上限、历史累积效应、物理量映���
                   0 个 sorry

KernelPerspective：  4 公理 + 9 定义 + 11 个定理（含1个部分证明）
                   1 个不标准的 sorry（S₃破缺）

CNTConjectures：    6 工作假设 + 38 已证明定理 + 4 个 sorry
                   含IdempotentQuantization、OntologicalMechanics、
                   HPI、ReproductionEnergy、Intertwiner
                   sorry主要在HPI（暂停研究）和幂等算子谱分解

总计定理数：        约 110 个已证明定理 + 6 公理 + 9 工作假设 + 4 猜想

HPI研究暂停部分：   3 个 sorry (HPICorrection + HPIAxiomCorrespondence)
幂等算子谱分解：     1 个 sorry (依赖mathlib基础设施)
```

---

## 十二、逻辑结构图

```
DCNC 六公理体系
├── 公理 1（五判据）
│   ├──→ 公理 3（历史不可逆）[T2]
│   ├──→ 电荷量子化拓扑结构 [T44, T47]
│   └──→ 兼容性定理 [T7]
│
├── 公理 2（选择性余极限）
│   ├──→ 公理 5（适应度单调）[T3]
│   └──→ 多路径干涉机制 [T85]
│
├── 公理 4（再生产幂等性）
│   ├──→ 物理量量子化 [T4, T65-T70]
│   ├──→ 再生产周期正定性 [T29]
│   ├──→ 单次作用量恒为h [T33]
│   └──→ 4-单纯形自洽性 [T9]
│
├── 公理 6（个体化）
│   └──→ 闭合核唯一性 [T5, T76]

几何扩展
├── 4-单纯形组合拓扑 [T15]
│   ├── 紧致性 → 辐射速度上限 [T17] → 光速候选 [T18]
│   └── 欧拉示性数 χ=1
├── 4-单纯形二面角 cosΘ=1/4 [T19]
├── EPRL相位 cos(5Θ)=61/64 [T20], sin²=375/4096 [T21]
├── 裸耦合常数 1/α₀=16384π/375 [T22, T23]
├── 4π因子：SU(2)→U(1) Hopf纤维化 [T24]
├── 实验兼容性偏差<1% [T53]
└── LQG对接：2-面↔自旋泡沫面 [T25, T26]

存在论力学
├── 再生产事件+历史
├── 反作用严格为正 [T79]
├── HPI锁定⇒变分为零 [T77]
├── HPI平稳⇔锁定 [T78]（←方向通过工作假设）
├── 时间箭头从公理3 [T80]
└── 有效作用量极限（工作假设）

Kernel核视角
├── 边界三分性 [T62]：3可见面+1对径面+1盲区面
├── 对径面不可见 [T60]
├── 历史面承载HPI累积 [T61]
└── S₅→S₄对称性破缺 [T58]

形式空间与时空涌现
├── 形式距离5条度量公理 [T98-T102]
├── 核-产物距离 [T103]
├── 核间距离 [T104, T105]
├── 空间与运动涌现 [T106]
├── 三阶段时空涌现 [T107-T110]
└── 能量子守恒 [T93] + 形式变化 [T94]
```

---

## 十三、开放问题与下一步方向

### 近期优先

1. **idempotent_trace_is_finrank [S]** —— 完成幂等算子迹=维数的证明。依赖 mathlib `Submodule.isCompl` 和 `trace_add`，或自行构造联合基证明。

2. **存在论力学严格化** —— 补齐 HPI 平稳⇒历史沉淀锁定的严格推导（当前为工作假设），建立 HPILockCondition 从公理的推导。

3. **核视角S₃破缺 [T63]** —— 基数不匹配问题（24 vs 6）需要重新审视。

### 中长期方向

4. **HPI修正重启** —— 先解决符号问题（所有修正项均为正导致偏离而非接近实验值），探索负贡献项或相消干涉机制。

5. **公理系统完备性** —— 建立 CNT 范畴的模型论基础。

6. **光速精确计算** —— 如果 c = D_max/τ，D_max 和 τ 如何从第一性原理确定？
