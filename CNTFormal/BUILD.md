# CNTFormal 项目编译指南

## 项目概述

CNTFormal 是一个基于 Lean 4 的形式化验证项目，用于实现闭合核理论（Closed Nucleus Theory）的严格数学推导和验证。

## 环境要求

- **Lean 版本**: v4.29.1（由 `lean-toolchain` 指定）
- **构建工具**: Lake（Lean 4 的构建系统）
- **工具链管理**: Elan

## 编译步骤

### 1. 安装工具链

```bash
elan update
```

确保安装了 Lean v4.29.1 工具链。

### 2. 配置依赖

项目依赖以下本地包（位于 `.lake/packages/` 目录）：
- `mathlib` - 数学库
- `physlib` - 物理库
- `batteries` - 基础工具库
- `Qq` - 元编程库
- `aesop` - 自动化证明策略
- `proofwidgets` - 交互式证明组件
- `LeanSearchClient` - Lean 搜索客户端
- `plausible` - 合理推理库
- `UnicodeBasic` - Unicode 支持
- 其他依赖...

### 3. 编译项目

#### 编译单个库

```bash
# 编译 Foundations 库
lake build Foundations

# 编译 PreLevel1 库
lake build PreLevel1

# 编译 Level1 库
lake build Level1

# 编译 PostLevel1PreLevel2 库
lake build PostLevel1PreLevel2

# 编译 Level2 库
lake build Level2
```

#### 编译整个项目

```bash
lake build
```

## 项目结构

```
CNTFormal/
├── Foundations/           # 基础理论层
│   ├── lean/
│   │   └── Proven/       # 已证明的理论
│   │       ├── AlphaDerivation.lean      # 精细结构常数推导
│   │       ├── Basic.lean                # 基础定义
│   │       ├── CategoryTheory.lean       # 范畴论
│   │       ├── Dimensions.lean           # 量纲系统
│   │       ├── ReproductionEnergy.lean   # 再生能量
│   │       ├── ReproductionPeriod.lean   # 再生周期
│   │       ├── SimplexGeometry.lean      # 单纯形几何
│   │       └── StrictnessConfig.lean     # 严格性配置
│   └── *.md              # 理论文档
├── PreLevel1/             # 一级质变前理论
│   └── lean/
│       ├── Conjectures/  # 猜想
│       │   └── KernelPerspective.lean
│       └── Proven/       # 已证明
│           └── L0Bootstrap.lean          # ℓ₀ Bootstrap定理
├── Level1/                # 一级质变理论
│   └── lean/
│       ├── Conjectures/  # 猜想
│       └── Proven/       # 已证明
├── PostLevel1PreLevel2/   # 一级后二级前理论
│   └── lean/
│       ├── Conjectures/
│       └── Proven/
├── Level2/                # 二级质变理论
│   └── lean/
│       └── Proven/
├── Papers/                # 学术论文
├── lakefile.toml          # Lake 构建配置
└── lean-toolchain         # Lean 版本指定
```

## 编译状态

| 库名 | 状态 | 备注 |
|------|------|------|
| Foundations | ✅ 成功 | 基础理论层 |
| PreLevel1 | ✅ 成功 | 含2个sorry（KernelPerspective.lean:169, 206） |
| Level1 | ✅ 成功 | 一级质变理论 |
| PostLevel1PreLevel2 | ✅ 成功 | 过渡理论层 |
| Level2 | ✅ 成功 | 二级质变理论 |

## 已知问题

1. **KernelPerspective.lean** 包含2个 `sorry`：
   - 第169行
   - 第206行

   这些是未完成的证明，需要后续补充。

2. **PhaseTransitionSearch.lean** 输出调试信息：
   - 第671行输出：10
   - 第673行输出：参数配置列表

## 常见问题

### Q: 编译时出现依赖包找不到的错误

A: 确保所有依赖包已正确放置在 `.lake/packages/` 目录下。

### Q: LeanSearchClient 编译失败

A: 确保使用正确版本的 LeanSearchClient（rev: c5d5b8f），该版本使用 `module` 声明和 `public meta import`。

### Q: proofwidgets 编译失败

A: 需要手动构建 widget 资源，或注释掉 `lakefile.lean` 中的 `needs := #[widgetJsAll]`。

## 版本信息

- **项目版本**: 0.1.0
- **Lean 版本**: 4.29.1
- **最后编译成功时间**: 2026-05-29
