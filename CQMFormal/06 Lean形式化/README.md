# CQMFormal — CQM 的 Lean 4 形式化验证

本目录包含**耦合常数量子力学（CQM）**的 Lean 4 形式化验证项目。

## 编译状态

✅ **全部 6 个库编译通过**（1923 jobs） | Lean 4.29.1

## 库结构

| 库 | 内容 | 关键类型/定理 |
|:---|:---|:---|
| **CausalSet** | 因果集公理 | `CausalSet`、`ReproductionOperator`、`asymm` |
| **CouplingSpace** | 耦合空间 | `couplingStrength`、`uncertaintyRelation` |
| **CartanAlgebra** | 嘉当代数 | `cartanA4`、`dynkinIndex`、`simplexEulerChar` |
| **SpectralGeometry** | 谱几何 | `spectralQuantum`、`mathieuCritical`、`GNFactor` |
| **Decoherence** | 退相干 | `confinementScale`、`confinement_equiv_decoherence` |
| **PhysicalConstants** | 物理常数 | `GN_spectral_formula`、`alpha_inverse_SU5` |

## 编译命令

```bash
cd "06 Lean形式化"
lake build                    # 编译全部
lake build CausalSet          # 编译单个库
```

## 理论对应

| CQM 理论 | Lean 库 |
|:---|:---|
| 因果集本体论 | `CausalSet` |
| 耦合空间与不确定性 | `CouplingSpace` |
| SU(5) 嘉当矩阵 | `CartanAlgebra` |
| 谱量子 C 与 Mathieu 方程 | `SpectralGeometry` |
| 禁闭-退相干等价 | `Decoherence` |
| G_N 谱公式与 α⁻¹ | `PhysicalConstants` |

## 已知缺口

| 缺口 | 描述 | 库 |
|:---|:---|:---|
| G5 | 退相干 = 禁闭的严格推导 | `Decoherence`（当前为 `axiom`） |
| — | 非交换 → 交换几何相变 | `Decoherence`（当前为 `axiom`） |
| — | G_N 谱公式数值验证 | `PhysicalConstants`（需数值计算） |

## 版本

- **项目版本**: 0.2.0
- **Lean 版本**: 4.29.1
- **依赖**: mathlib, physlib