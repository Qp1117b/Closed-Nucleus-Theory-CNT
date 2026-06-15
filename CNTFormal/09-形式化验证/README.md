# 09-形式化验证

本目录是CNT形式化验证的文档入口。实际的Lean代码位于 `CNTFormal/` 根目录下的各Lean库中。

## Lean库结构

CNT的形式化验证分为五个层次，对应物理理论的不同阶段：

| 库名 | 状态 | 对应理论层次 | 关键内容 |
|------|------|-------------|---------|
| **Foundations** | ✅ 编译成功 | 公理体系/本体论 | 基础定义、单纯形几何、α推导、再生产周期、范畴论 |
| **PreLevel1** | ✅ 编译成功 | 一级质变前 | ℓ₀ Bootstrap定理、相变搜索、核视角猜想 |
| **Level1** | ✅ 编译成功 | 一级质变理论 | 公理一致性、HPI公理对应、幂等量子化 |
| **PostLevel1PreLevel2** | ✅ 编译成功 | 过渡理论 | 再生产网络质量、标度涌现、再生产无线电速度 |
| **Level2** | ✅ 编译成功 | 二级质变理论 | 交织子结构、二级跃迁 |

## 编译命令

```bash
cd CNTFormal
lake build Foundations
lake build PreLevel1
lake build Level1
lake build PostLevel1PreLevel2
lake build Level2
# 或全部编译
lake build
```

## 已知问题

- `PreLevel1/lean/Conjectures/KernelPerspective.lean` 包含2个 `sorry`（第169、206行）
- `PreLevel1/lean/Proven/PhaseTransitionSearch.lean` 输出调试信息

## 与理论文档的对应关系

| 理论目录 | 对应Lean库 |
|---------|-----------|
| 01-公理体系 | Foundations (SimplexGeometry, AlphaDerivation) |
| 02-本体论 | Foundations (Basic, CategoryTheory) |
| 03-方法论 | Foundations (Dimensions, StrictnessConfig) |
| 04-核心方程 | Foundations (ReproductionEnergy, ReproductionPeriod) |
| 07-质变理论 | Level1, Level2, PreLevel1, PostLevel1PreLevel2 |

详见 [BUILD.md](../BUILD.md)