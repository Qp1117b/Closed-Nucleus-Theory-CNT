# CQM 研究框架重构计划

## 背景

当前项目 `闭合核理论/CNTFormal/` 处于从 CNT（闭合核理论）向 CQM（耦合常数量子力学）过渡的关键阶段。7 份最新 CQM 文档已产出但尚未纳入正式目录结构，与大量历史 CNT 文档混放在根目录和编号子目录中。需要：

1. 将框架名从 CNT 统一为 CQM
2. 将 7 份最新 CQM 文档按主题归类到清晰的新目录结构
3. 全部历史 CNT 文档归档到 `归档_CNT/` 子目录
4. 全局统一概念、公式、术语命名
5. Lean 形式化项目独立保留

## 新目录结构

```
闭合核理论/
├── CQMFormal/                              ← 重命名自 CNTFormal
│   ├── README.md                           ← 全新重写
│   ├── .gitignore
│   │
│   ├── 01_核心理论/                        ← 理论主干
│   │   ├── CQM_核心_集成理论.md            (from CQM_v2.1_Integrated_System_Scale_Hierarchy.md)
│   │   └── CQM_核心_一证七联.md            (from CQM_CoreStructure_Summary.md)
│   │
│   ├── 02_量子引力/
│   │   └── CQM_引力_量子引力集成.md        (from CQM_Quantum_Gravity_Integrated_v2.md)
│   │
│   ├── 03_引力与退相干/
│   │   ├── CQM_引力_GN谱公式.md            (from CQM_GN_Spectral_Formula_v2.md)
│   │   └── CQM_退相干_质数数轴.md          (from CDPNA_Conceptual_Framework.md)
│   │
│   ├── 04_谱与混合/
│   │   └── CQM_混合_混合矩阵.md            (from CNT_Mixing_Matrix_v2_NoConstraint2.md)
│   │
│   ├── 05_方法论与批判/
│   │   └── CQM_方法论_HilbertPolya批判.md  (from Hilbert_Polya_Critique_CQM.md)
│   │
│   ├── 06_Lean形式化/                      ← 全部来自 09-形式化验证/
│   │   ├── lakefile.toml
│   │   ├── lake-manifest.json
│   │   ├── lean-toolchain
│   │   ├── BUILD.md
│   │   ├── README.md
│   │   ├── .github/
│   │   └── .lake/
│   │
│   └── 归档_CNT/                           ← 全部历史 CNT 文档
│       ├── README.md                       ← 归档索引
│       ├── 01_入门与脉络/                  (5 文件)
│       ├── 02_公理与本体论/                (2 文件)
│       ├── 03_方法论/                      (8 文件)
│       ├── 04_核心方程/                    (1 文件)
│       ├── 05_前沿研究/                    (2 文件)
│       ├── 06_论文/                        (3 文件)
│       ├── 07_计算框架/                    (9 文件)
│       ├── 08_代码/                        (18 Python 文件 + archive/)
│       └── 09_前期探索/                    (来自原 归档/ 目录)
```

## 文件映射表

### 7 份 CQM 新文档

| 旧路径 | 新路径 |
|:---|:---|
| `CNTFormal/CQM_v2.1_Integrated_System_Scale_Hierarchy.md` | `CQMFormal/01_核心理论/CQM_核心_集成理论.md` |
| `CNTFormal/CQM_CoreStructure_Summary.md` | `CQMFormal/01_核心理论/CQM_核心_一证七联.md` |
| `CNTFormal/CQM_Quantum_Gravity_Integrated_v2.md` | `CQMFormal/02_量子引力/CQM_引力_量子引力集成.md` |
| `CNTFormal/CQM_GN_Spectral_Formula_v2.md` | `CQMFormal/03_引力与退相干/CQM_引力_GN谱公式.md` |
| `CNTFormal/CDPNA_Conceptual_Framework.md` | `CQMFormal/03_引力与退相干/CQM_退相干_质数数轴.md` |
| `CNTFormal/CNT_Mixing_Matrix_v2_NoConstraint2.md` | `CQMFormal/04_谱与混合/CQM_混合_混合矩阵.md` |
| `CNTFormal/Hilbert_Polya_Critique_CQM.md` | `CQMFormal/05_方法论与批判/CQM_方法论_HilbertPolya批判.md` |

### CNT 根层文档 → 归档

| 旧路径 | 归档路径 |
|:---|:---|
| `CNTFormal/CNT_读者入门.md` | `归档_CNT/01_入门与脉络/CNT_读者入门.md` |
| `CNTFormal/CNT_完整脉络：从因果集到物理常数.md` | `归档_CNT/01_入门与脉络/CNT_完整脉络：从因果集到物理常数.md` |
| `CNTFormal/CNT_研究展开链.md` | `归档_CNT/01_入门与脉络/CNT_研究展开链.md` |
| `CNTFormal/CNT_设计记录.md` | `归档_CNT/01_入门与脉络/CNT_设计记录.md` |
| `CNTFormal/CNT_猜想关联与诚实评估.md` | `归档_CNT/01_入门与脉络/CNT_猜想关联与诚实评估.md` |

### 编号子目录 → 归档

| 旧子目录 | 归档子目录 |
|:---|:---|
| `01-公理体系/` | `归档_CNT/02_公理与本体论/` |
| `02-本体论/` | `归档_CNT/02_公理与本体论/` |
| `03-方法论/` | `归档_CNT/03_方法论/` |
| `04-核心方程/` | `归档_CNT/04_核心方程/` |
| `05-前沿研究/` | `归档_CNT/05_前沿研究/` |
| `07-论文/` | `归档_CNT/06_论文/` |
| `08-计算框架/` | `归档_CNT/07_计算框架/` |
| `10-代码/` | `归档_CNT/08_代码/` |
| `归档/` | `归档_CNT/09_前期探索/` |

### 特殊处理

- `09-形式化验证/` → `CQMFormal/06_Lean形式化/`（整个目录移动）
- `CNTFormal/.gitignore` → `CQMFormal/.gitignore`
- `CNTFormal/README.md` → 重写为 CQM 版
- `06-前沿研究/`（空目录）→ 删除

## 实施步骤

### 步骤 1：创建新目录结构（所有新目录一次性创建）

### 步骤 2：移动 7 份 CQM 新文档到对应主题文件夹

### 步骤 3：移动 Lean 形式化项目到 06_Lean形式化/

### 步骤 4：移动 CNT 根层参考文档到归档

### 步骤 5：移动编号子目录到归档

### 步骤 6：清理空目录（原 01-10 及 归档/ 空目录）

### 步骤 7：移动 .gitignore

### 步骤 8：删除已清空的 CNTFormal 目录

### 步骤 9：编写归档_CNT/README.md（归档索引）

### 步骤 10：重写 CQMFormal/README.md（新主 README）

### 步骤 11：Git 提交

## 内容一致性

### 术语统一

- 框架名：**耦合常数量子力学（CQM）**
- 核心常数：$C = \xi'(1)/\xi(1)$
- 耦合空间坐标：$u = \ln r$
- 嘉当矩阵：$A_4 = \text{Cartan}(\text{SU}(5))$
- 因果集：$(X, \prec)$
- 层级标记：L1（禁闭内部）、L2（禁闭边界）、L3+（外部）

### 公式一致性

- $[\hat{u}, \hat{p}_u] = i$
- $G_N = I \cdot \lambda_c \cdot C^2 \cdot \mathfrak{c}_1 \cdot \exp(-2/C) \cdot (1 + \kappa C) / m_p^2$
- $\mathfrak{c}_n^{(R)} = 1/4 + \gamma_n^2$
- $\kappa = (31+C)/30$
- $\alpha^{-1}_{\text{SU(5)}} = 16384\pi/375$

## 验证

1. 确认 CQMFormal/ 目录树完整，7 份 CQM 文档各归其位
2. 确认归档_CNT/ 包含全部历史文档
3. 确认 CNTFormal/ 已删除
4. 确认 git status 显示正确的添加/删除/重命名
5. 确认新 README.md 链接正确可点击