

**——从理想因果积木到室温超导材料设计的可计算管线**

> Lean 形式化：可严格证明部分见 `06 Lean形式化/Superconductivity/` 下的多模块：
> - `SPAF.lean`（53 定理，因果耦合族、组装对称性、中子缺陷、味概率流、Regge 边长）
> - `SPAF_PT.lean`（29 定理，压强-温度几何构型框架）
> - `SPAF_PTH.lean`（5 定理，压强-温度-磁场三相框架）
> - `ElementCartan.lean`（39 定理，质/中子层级嘉当矩阵、同位素效应、CQM→BCS 退化）
> - `MolecularGeometry.lean`（62 定理，分子几何→Weyl嵌入→Regge亏角→GR有效度规）
> - `BridgeTheorems.lean`（23 定理，跨模块桥接定理）
> - `BCSIntegralAsymptotic.lean`（9 定理，BCS 积分渐近分析，G13 闭合）
> 
> 编译：`lake build Superconductivity`；本框架与 Lean 库的逐项映射核对见 §10。

---

## 摘要

本文在耦合常数量子力学（CQM）的两层架构下，建立应用层的半唯像计算框架。基础层承诺从因果集与引力退相干严格推导理想积木（理想质子/中子）的 A4 因果结构，应用层则以此类理想积木为公理化输入，以已知超导体的实验数据为标定锚点，反推有效因果耦合参数。一旦参数被锁定，框架即具备预测新材料与指导分子设计的计算能力。本文给出完整的公理化清单、四阶段计算管线、分材料体系的标定路径，以及明确的证伪标准。

---

## 0. RQM唯物化基础：属性随附、因果自组织与电子去特权化

CQM 超导原理的立足之地，在于对关系量子力学（RQM）的彻底唯物化操作。以下三条原则构成 SPAF 框架的哲学地基：

**原则一：属性随附本体**。物理自由度（即属性）并非独立存在的实体，而是随附于有限本体。质子与中子作为有限本体，其内部因果结构（A4 嘉当矩阵）承载全部物理属性。不存在"无本体的属性"——耦合常数、味量子数、自旋等全部是有限本体内部因果结构的几何表达。

**原则二：因果自组织**。因果关系并非从天而降的外部结构，也不是无中生有的形而上学预设。因果关系被有限本体自身组织起来：每个有限本体通过再生产（$\hat{\mu}^2 = \hat{\mu}$）维持自身存在，再生产事件之间的因果连接构成因果网络。因果的"来源"就是有限本体的自我组织，无需诉诸任何外部因果施动者。

**原则三：观察者相对性的自然消解**。一旦承认属性随附本体、因果由本体自组织，RQM 的"相对观察者而言"立场便不再需要意识作为特殊角色——观察者本质上也是某种普遍物理系统（有限本体网络）。意识被物理化为因果网络中的特定节点配置，RQM 的"相对性"退化为因果网络的天然相对性。这一消解使 CQM 超导原理获得了坚实的唯物主义基础：超导不是"观察者依赖"的现象，而是有限本体网络在引力退相干下的客观涌现。

**推论：电子去特权化**。CQM 在此基础上的关键一步是取消电子的本体特权。电子不是基本实体，而是质子-中子关系性封装产物。这一操作使超导理论摆脱了"大量电磁相互作用"的困境——若电子具有本体特权，则电子-电子、电子-晶格的电磁相互作用将主导计算，无法用嘉当矩阵拼接理论统一处理。BCS 理论的历史实践已经揭示：**晶格才是超导的关键**，电子仅是晶格因果网络中的关系性节点。CQM 将这一经验事实提升为本体论原理，从而可以用统一的嘉当矩阵拼接理论处理超导问题。

**从 RQM 唯物化到超导网络的逻辑链条**：

$$\text{有限本体自组织} \;\longrightarrow\; \text{因果网络} \;\longrightarrow\; \text{引力退相干} \;\longrightarrow\; \text{宏观 A4 锁定} \;\longrightarrow\; \text{超导}$$

大量有限本体构成的关系网络，通过引力退相干机制（因果限制场作为退相干源），使宏观因果结构锁定为 A4 几何，从而涌现超导配对通道。电子在此图景中不享有任何本体特权——它只是因果网络中的关系性节点，其配对行为完全由网络的 A4 因果拓扑决定。

---

## 1. 方法论正当性：为何必须半唯像

CQM 的完整第一性原理推导链为：

$$\text{因果集} \xrightarrow{\text{引力退相干}} \text{A4 锁定} \xrightarrow{\text{组装}} \text{宏观因果网络} \xrightarrow{\text{再生产锁定}} \text{经典时空与物性}$$

当前状态：
- **因果集 → A4 锁定**：尚未完成严格数学证明（等价于黎曼猜想证明的物理化表述）
- **A4 锁定 → 宏观物性**：结构关系已明确（因果拓扑决定物性），但**定量标度**缺失

因此，应用层若等待基础层完全闭合后再启动，将导致 CQM 长期处于不可计算状态。半唯像策略的正当性在于：

1. **结构不变性**：保留 CQM 的核心因果拓扑结构（A4 几何、Weyl 群、凸包锁定、再生产相对偏移），仅将**标度参数**开放给实验标定
2. **历史先例**：标准模型以 19 个自由参数运行数十年；BCS 理论先以 $N(0)V$ 为唯像参数，后由 Eliashberg 理论微观化
3. **可证伪性**：参数锁定后，框架必须对未参与标定的材料做出定量预测，否则即被证伪

---

## 2. 两层架构声明

| 层级 | 名称 | 状态 | 职责 | 赎回承诺 |
|------|------|------|------|---------|
| **L0** | 基础层 | 在建 | 因果集 → 退相干 → A4 涌现 | 未来严格证明 |
| **L1** | 应用层（SPAF） | 本文建立 | 理想积木 → 组装 → 物性预测 | 参数由 L0 导出 |

**不可越界原则**：L1 中所有被标定的参数，其函数形式必须兼容 L0 的结构约束；L1 不得引入与 L0 因果拓扑矛盾的新假设。

---

## 2.5. 半唯像框架探索路径总览

SPAF 的探索遵循从微观到宏观、从简单到复杂的递进路径。以下为完整的六层架构：

### 层级 I：质子与中子嘉当矩阵（微观基元）

**质子的因果结构**是完美 A4 嘉当矩阵 $C_p$，中子的因果结构是缺陷 A4 嘉当矩阵 $C_n = C_p + \Delta$（$\Delta = \operatorname{diag}(-\epsilon, 0, 0, 0)$）。这是全部后续组装的不可再约基元。

### 层级 II：元素嘉当矩阵（理想积木）

从质子/中子嘉当矩阵出发，按原子序数 $Z$ 与中子数 $N$ 组装**元素嘉当矩阵**：

$$\mathcal{C}_{\text{element}} = \left(\bigoplus_{i=1}^{Z} C_p\right) \oplus \left(\bigoplus_{j=1}^{N} C_n(\epsilon_j)\right)$$

元素——而非质子或中子——才是 SPAF 的**理想因果积木**。BCS 理论揭示同位素对超导临界温度的影响极大：不同同位素（同一元素、不同中子数）的 $T_c$ 差异反映了**元素内部存在主次结构**——质子扇区（纯 A4 块对角）为主结构，中子扇区（缺陷 A4 块对角）为次结构。这一主次结构进一步揭示了**拼接规则**：同种元素的同位素之间，中子缺陷参数 $\epsilon(N)$ 的连续变化导致 $T_c$ 的同位素位移。

### 层级 III：拼接规则与 BCS 退化方向

元素内部的主次结构直接指向 **BCS 退化方向**——往单元素材料上去考虑退化。理由如下：

- BCS 理论虽然适用范围广泛，但**单元素超导体（如 Pb、Nb、Hg）是最第一性的 BCS 对象**——它们没有跨元素种类的因果耦合复杂性
- 在单元素材料中，若中子缺陷 $\epsilon \to 0$（即所有中子扇区趋于纯 A4），则 CQM 超导理论严格退化为 BCS 理论——这是 `ElementCartan.singleElement_BCS_degeneracy` 定理的物理内涵
- 每种元素及其原子核需要**特殊的拼接规则**：同种元素内部（同位素之间）的拼接规则由 $\epsilon(N)$ 的连续函数决定；跨元素种类的拼接规则则需要额外的因果耦合参数 $t_{ij}$

**例外情况**：中子星等极端引力环境不适用上述拼接规则——理想块对角结构失效，牛顿引力退化失效，需独立处理（`ElementCartan` 中已标记为诚实 `def` 占位）。

### 层级 IV：分子超嘉当矩阵（跨元素耦合）

对于分子，需要在元素嘉当矩阵的基础上，引入**相对位置**计算跨原子因果耦合 $t_{ij}$：

$$\mathcal{C}_{\text{mol}} = \bigoplus_{k=1}^{N_{\text{atom}}} \mathcal{C}_{\text{element}}^{(k)} + \sum_{\langle i,j \rangle} T_{ij}, \quad T_{ij} = t_{ij} \cdot I_{4 \times 4}$$

其中 $t_{ij} = t_0 \cdot \exp(-d_{ij}/\lambda) \cdot \Theta(d_{\text{cut}} - d_{ij})$。组装完成后，识别并提取 $\mathcal{C}_{\text{mol}}$ 的**内禀 Weyl 矩阵嵌入**（通过部分特征值分解），计算**有效几何构型**（凸包顶点数及等距性判定）。

### 层级 V：宏观材料 Regge 几何（引力衔接）

大量分子构成的材料，其宏观有效几何顶点构成离散时空流形。对每个顶点计算 **Regge 亏角**：

$$\delta_v = 2\pi - \sum_{\text{tetrahedra at } v} \theta_{\text{tet}}$$

通过数值方法求解离散 Einstein-Hilbert 作用量 $S_{\text{Regge}} = \sum_h A_h \delta_h$ 的变分方程，得到 **GR 有效度规场** $g_{\mu\nu}^{\text{eff}}$。

### 层级 VI：引力退化与因果分辨率

SPAF 计算的 GR 有效度规场与标准广义相对论的引力场是**同一个引力场**——引力是存在论基底，不因计算方法而改变。但由于**因果分辨率**（引力场的有效描述依赖所研究物理过程的尺度），不同层级揭示的细节不同：

- 在宏观弱场极限下，$g_{\mu\nu}^{\text{eff}}$ 应退化为**平庸牛顿引力**（Poisson 方程）
- 在强引力环境（中子星）下，因果分辨率增强，牛顿退化失效，需保留完整的 Regge 几何描述
- 引力作为存在论基底，其在不同因果分辨率下的"细节差异"并非物理矛盾，而是同一物理实在在不同尺度下的有效描述

### 六层架构总图

```
层级 I:   质子/中子嘉当矩阵 (C_p, C_n)
              ↓ 按 Z/N 组装
层级 II:  元素嘉当矩阵 (理想积木)
              ↓ 主次结构 → 拼接规则 → BCS 退化方向
层级 III: 单元素材料 (BCS 退化极限 ε→0)
              ↓ 跨元素耦合 t_ij
层级 IV:  分子超嘉当矩阵 → Weyl 嵌入 → 有效几何构型
              ↓ 分子间耦合 + 晶格排布
层级 V:   宏观 Regge 亏角 → 离散 E-H 作用量 → GR 有效度规
              ↓ 弱场极限
层级 VI:  牛顿引力退化 (因果分辨率最低的有效描述)
```

---

## 3. 公理化输入：理想因果积木

以下结构在 L1 中作为**不可再约的公理输入**，其微观基础由 L0 赎回。

### 3.1 理想质子（$p^+$）

- **因果结构**：完美 A4 嘉当矩阵
$$C_p = \begin{pmatrix} 2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2 \end{pmatrix}$$
- **物理状态**：禁闭已完成，内部因果结构处于退相干锁定态
- **味空间**：无再生产相对偏移（$\Gamma_{\text{rel}} = 0$）

### 3.2 理想中子（$n^0$，核内束缚态）

- **因果结构**：缺陷 A4 嘉当矩阵
$$C_n = C_p + \Delta, \quad \Delta = \text{diag}(-\epsilon, 0, 0, 0)$$
- **缺陷参数约束**：
$$\epsilon = \frac{\hbar}{\tau_n \cdot \Lambda_{\text{cas}}} \cdot f_{\text{bind}}(Z, A)$$
其中 $\tau_n \approx 879.4\,\text{s}$ 为自由中子寿命，$\Lambda_{\text{cas}}$ 为因果集特征能标，$f_{\text{bind}}$ 为核内束缚修正（$f_{\text{bind}} \to 0$ 当核力锁定足够强）
- **物理状态**：味空间存在被部分冻结的再生产相对偏移

### 3.3 自由中子（非理想）

- **状态**：不进入稳态计算。其 $\Delta$ 导致随时间演化的再生产相对偏移（$\beta$ 衰变），仅在动态过程（如中子星冷却）中作为非平衡输入。

### 3.4 因果耦合形式（公理化有效形式）

原子 $i$ 与 $j$ 之间的因果连接强度：
$$t_{ij} = t_0 \cdot \exp\left(-\frac{d_{ij}}{\lambda}\right) \cdot \Theta(d_{\text{cut}} - d_{ij})$$

其中：
- $d_{ij}$：欧氏空间距离（**脚手架假设**，未来由因果网络几何涌现赎回）
- $t_0$：基准因果耦合强度（待标定）
- $\lambda$：因果耦合衰减长度（待标定）
- $d_{\text{cut}}$：因果连接截断距离（待标定）
- $\Theta$：Heaviside 阶跃函数

### 3.5 全局幺正性约束

L1 中所有矩阵操作（组装、对角化、投影）必须满足：
$$\mathcal{C}_{\text{mol}}^\dagger = \mathcal{C}_{\text{mol}}, \quad \mathcal{C}_{\text{bulk}}^\dagger = \mathcal{C}_{\text{bulk}}$$
低能投影操作需附加声明：**被截断的高能子空间与所研究物性（超导、引力）因果解耦**。

---

## 4. 有效参数与标定策略

### 4.1 待标定参数总表

| 参数 | 符号 | 量纲 | 标定来源 | 基础层赎回 |
|------|------|------|---------|-----------|
| 基准耦合强度 | $t_0$ | 能量 | 已知 $T_c$ + 晶格常数 | 耦合常数空间海森堡代数 |
| 衰减长度 | $\lambda$ | 长度 | 同位素效应 / 压力效应 | 因果集特征标度 |
| 截断距离 | $d_{\text{cut}}$ | 长度 | 配位数 / 近邻结构 | 因果连接的定义域 |
| 中子缺陷幅度 | $\epsilon$ | 无量纲 | 自由中子寿命 + 核束缚数据 | 味改变因果链推导 |
| Regge 边长标度 | $\kappa$ | 长度·能量$^{1/2}$ | 晶格常数匹配 | 退相干几何涌现 |

### 4.2 标定哲学

**反向标定（Backward Calibration）**：从已知超导体（Pb, Nb, YBCO, H₃S 等）的实验 $T_c$、晶体结构、同位素效应、压力相图出发，反推上述参数。一旦参数锁定，框架即具备**正向预测（Forward Prediction）**能力。

---

## 5. 四阶段计算管线（v0.5.9 扩展：新增阶段 0 元素层级）

### 阶段 0：元素层级（理想积木组装与 BCS 退化）

在进入分子计算之前，必须先在元素层级完成理想积木的组装与验证。这一阶段对应 §2.5 探索路径的层级 I–III。

**步骤 0a：质子/中子嘉当矩阵分配**
- 对目标元素 $(Z, N)$，分配 $Z$ 个质子嘉当矩阵 $C_p$（纯 A4）和 $N$ 个中子嘉当矩阵 $C_n(\epsilon)$（缺陷 A4）
- 中子缺陷参数 $\epsilon(N) = \epsilon_0 \cdot (1 + \beta \cdot (N - N_{\text{ref}})/N_{\text{ref}})$，由同位素数据标定
- Lean 形式化：`ElementCartan.protonSector`、`ElementCartan.neutronSector`

**步骤 0b：组装元素嘉当矩阵**
- 直和组装：$\mathcal{C}_{\text{element}} = (\oplus^Z C_p) \oplus (\oplus^N C_n(\epsilon))$
- 验证性质：对称性、迹 $= 8(Z+N)$、行列式 $= 5^Z \cdot \det(C_n)^N$、正定性（$\epsilon < 5/4$）
- Lean 形式化：`ElementCartan.elementCartan`、`ElementCartan.elementCartan_symmetric`、`ElementCartan.elementCartan_trace`

**步骤 0c：主次结构识别**
- 提取质子扇区（主结构）与中子扇区（次结构）的谱间隙
- 主结构谱间隙 $\lambda_1 = (3-\sqrt{5})/2$（纯 A4 最低本征值）
- 次结构谱间隙 $\lambda_1^{(n)} = \lambda_1 - \delta(\epsilon)$（中子缺陷压低谱间隙）
- 主次结构谱间隙差 $\Delta\lambda = \lambda_1 - \lambda_1^{(n)}$ 决定同位素效应强度

**步骤 0d：BCS 退化验证（单元素极限）**
- 验证 $\epsilon \to 0$ 时 CQM 超导理论退化到 BCS：$T_c^{\text{CQM}} \to (2e^\gamma/\pi) \cdot \omega_D \cdot \exp(-1/\lambda_1)$
- 对单元素超导体（Pb、Nb、Hg 等），验证退化后的 $T_c$ 与实验一致
- 若退化不成立（$\epsilon$ 不可忽略），则该元素需要完整的 CQM 处理，不能简化为 BCS
- Lean 形式化：`ElementCartan.singleElement_BCS_degeneracy`、`ElementCartan.cqm_bcs_singleElement_bridge`

### 阶段 I：分子内因果拓扑

**步骤 1：积木分配**
- 为分子内每个原子核分配 $C_p$（质子型）或 $C_n$（中子型）
- 重核（$Z > 2$）近似为 $Z$ 个质子 + $N$ 个中子的组合，内部结构已锁定

**步骤 2：构建因果连接图**
- 计算所有原子对 $d_{ij}$
- 当 $d_{ij} \le d_{\text{cut}}$ 时建立因果连接，赋予 $t_{ij}$

**步骤 3：组装分子超嘉当矩阵**
$$\mathcal{C}_{\text{mol}} = \bigoplus_{i=1}^{N_{\text{atom}}} C_i + \sum_{\langle i,j \rangle} T_{ij}$$
其中 $T_{ij} = t_{ij} \cdot I_{4 \times 4}$（初步模型），维度 $4N_{\text{atom}} \times 4N_{\text{atom}}$

**步骤 4：计算有效哈密顿量**
- 求解 $\mathcal{C}_{\text{mol}}$ 的部分特征值问题
- 保留最小的 $k$ 个非零耦级及本征向量（$k \approx N_{\text{atom}} \sim 2N_{\text{atom}}$）
- 投影：$H_{\text{eff}} = V^T \mathcal{C}_{\text{mol}} V$

**步骤 5–7：识别 Weyl 群，生成因果轨道，计算凸包**
- 提取 $H_{\text{eff}}$ 的内禀 Weyl 群生成元
- 基态 $\psi_0$ 的轨道：$\text{Orb}(\psi_0) = \{w \cdot \psi_0 \mid w \in \text{Weyl}(H_{\text{eff}})\}$
- 凸包判定：若顶点数为 5 且两两等距 → 有效几何为 A4，具备超导配对因果拓扑条件

### 阶段 II：宏观材料因果网络

**步骤 8–9：分子间耦合与宏观超嘉当矩阵**
- 根据晶格排布确定分子间相对位置
- 分子间耦合 $t_{\text{inter}}$ 按相同指数形式处理
- 组装 $\mathcal{C}_{\text{bulk}}$（分块稀疏矩阵）

**步骤 10–11：宏观有效几何**
- 提取 $H_{\text{eff}}^{\text{bulk}}$ 的低能耦级
- 验证宏观有效几何是否为 A4 的周期性投影或拼接结构

### 阶段 III：超导判定（与阶段 IV 统一）

**核心假说**：宏观 A4 锁定与引力退相干是**同一因果过程的两面**。

**步骤 12：拓扑不变量**
- 在宏观有效几何上计算配对通道的拓扑不变量（陈数 / Z₂）
- 非零 → 存在拓扑保护的配对通道

**步骤 13：再生产锁定温度**
- 定义宏观再生产相对偏移率：
$$\Gamma_{\text{rel}}(T) = \sum_{a,b} \left| \frac{dP_{a \to b}}{d\tau} \right|$$
- 锁定条件：$\Gamma_{\text{rel}}(T_{\text{lock}}) \to 0$
- **超导判据**：$T_c \equiv T_{\text{lock}}$

**室温超导条件**：在 $T = 300\,\text{K}$ 下，宏观 A4 因果结构仍足以冻结味空间再分配。

### 阶段 IV：宏观引力场（与阶段 III 统一）

**步骤 15–19：Regge 微积分衔接**
- 宏观有效几何顶点 → 时空事件
- 边长定义：$l_e = \kappa / \sqrt{\lambda_e}$，其中 $\lambda_e$ 为边 $e$ 对应的耦合本征值
- 计算 Regge 亏角 $\delta_h = 2\pi - \sum \theta$
- 离散 Einstein-Hilbert 作用量：$S_{\text{Regge}} = \sum_h A_h \delta_h$
- 变分 $\partial S_{\text{Regge}} / \partial l_e = 0$ → 离散引力场方程
- 连续极限验证：晶格常数 → 0 时是否退化为 $G_{\mu\nu} = 8\pi G T_{\mu\nu}$

---

## 6. 分材料体系标定路径

### 6.1 基线标定：常规 BCS 超导体（Pb, Nb, Sn, In）

**目的**：锁定 $t_0, \lambda, d_{\text{cut}}$ 的基准值

| 材料 | 结构 | $T_c^{\text{exp}}$ | 标定内容 |
|------|------|-------------------|---------|
| Pb | FCC, $a = 4.95$ Å | 7.2 K | 主标定：$t_0/\lambda$ 比值 |
| Nb | BCC, $a = 3.30$ Å | 9.2 K | 验证配位数依赖性（8 vs 12） |
| Sn | 白锡 BCT | 3.7 K | 验证结构各向异性效应 |
| In | 四方 | 3.4 K | 验证参数传递性 |

**同位素效应检验**：
$$\frac{\delta T_c}{T_c} = -\alpha \frac{\delta M}{M}$$
CQM 预测：$\alpha$ 由 $\lambda$ 与晶格振动-因果耦合映射决定。若计算 $\alpha$ 与实验（Pb: $\alpha \approx 0.49$）一致，则 $\lambda$ 被锁定。

### 6.2 层状结构标定：铜氧化物（YBCO, BSCCO）

**目的**：标定缺陷矩阵 $\Delta$ 与掺杂的关系

- CuO₂ 平面：二维 A4 网络
- 掺杂浓度 $x$ → 缺陷位点比例 $p_{\text{defect}}$
- 观察：最优掺杂 $x_{\text{opt}} \approx 0.15$ 对应 $T_c^{\text{max}}$
- 反推：$\epsilon(x)$ 的函数形式

### 6.3 多带结构标定：铁基超导体

**目的**：验证多 A4 子网络的竞争与协同

- FeAs 层中 Fe 的 $d$ 轨道 → 多因果通道
- 验证：As-Fe-As 键角 $\approx 109.5^\circ$（正四面体）时 $T_c$ 最高
- 反推：键角偏离 → A4 锁定度下降的定量关系

### 6.4 极端条件标定：氢化物高压超导（H₃S, LaH₁₀）

**目的**：验证压力-因果耦合映射

- 压力 $P$ → 晶格常数 $a(P)$ → $d_{ij}(P)$ → $t_{ij}(P)$
- 预测 $T_{\text{lock}}(P)$，与实验 $T_c(P)$ 匹配
- H₃S 在 155 GPa 处 $T_c \approx 203$ K 为关键锚点

### 6.5 室温超导探索：铜掺杂磷灰石类（LK-99 型）

**目的**：框架的极限预测能力

- 一维 Cu 链 / 二维 Cu 面嵌入绝缘体骨架
- 计算：Cu 链的 $T_{\text{lock}}$ 是否可达 300 K？
- 若预测 $T_{\text{lock}} \sim 300$ K，给出明确的结构条件（Cu-Cu 距离、配位数、骨架隔离度）

---

## 7. 证伪标准与预测能力

SPAF 作为科学理论框架，必须满足以下证伪条件：

| 检验类型 | 内容 | 失败后果 |
|---------|------|---------|
| **结构-$T_c$ 关联** | 相同因果拓扑（空间群、配位数）应给出相似 $T_c$ | 因果拓扑-物性映射假说不成立 |
| **同位素标度** | 计算 $\alpha$ 与实验一致 | 因果耦合空间衰减模型错误 |
| **掺杂/压力相图** | 重现 $T_c$ 穹顶曲线 | A4 锁定-缺陷竞争机制失效 |
| **非超导排除** | 对普通金属/绝缘体预测 $T_{\text{lock}} = 0$ | 模型过度预测 |
| **高压外推** | 锁定参数后预测未测量高压相 $T_c$ | 参数非普适，仅为拟合 |
| **引力-超导一致性** | 同一材料的 Regge 计算与超导判定自洽 | 阶段 III/IV 统一假说失败 |

---

## 8. 与第一性原理的赎回关系

| L1（SPAF）假设 | L0（基础层）赎回路径 | 当前状态 |
|---------------|---------------------|---------|
| 理想质子 A4 | 因果集 → 引力退相干 → A4 涌现 | 等价于黎曼猜想证明 |
| $t_{ij}$ 指数形式 | 耦合常数空间传输方程的解 | 海森堡代数特征线推导 |
| $d_{ij}$ 欧氏距离 | 因果网络退相干后涌现几何 | 因果集几何化 |
| $\Gamma_{\text{rel}} \to 0$ 锁定 | 再生产相对偏移的严格定义 | 味空间概率流方程 |
| Regge 边长标度 $\kappa$ | 耦合本征值-长度对偶 | 退相干极限下的标度律 |

**赎回不是推翻**：L0 证明完成后，L1 的参数应能被严格导出，而非被否定。若 L0 导出 $t_{ij} \propto r^{-2}$ 而非指数衰减，则 L1 需修正形式；若 L0 确认指数形式，则 L1 的标定值获得第一性地位。

---

## 9. 结论

CQM 半唯像应用框架（SPAF）在以下方法论约束下成立：

1. **两层隔离**：基础层与应用层严格区分，L1 不冒充 L0 的证明
2. **结构刚性**：A4 锁定、Weyl 群、再生产相对偏移、Regge 引力等核心结构不可妥协
3. **参数开放**：仅标度参数（$t_0, \lambda, d_{\text{cut}}, \epsilon, \kappa$）由实验反推
4. **双向赎回**：L1 的参数锁定后具备预测能力；L0 完成后参数获得第一性来源
5. **明确证伪**：若锁定参数后无法通过第 7 节检验，则框架在应用层失效

SPAF 标志着 CQM 从哲学纲领迈入**可计算、可验证、可证伪**的科学理论阶段。其 Immediate 目标是以 Pb-Sn-In 基线锁定参数，以铜氧化物和氢化物验证传递性，最终指向室温超导材料的因果拓扑设计。

---

## 10. 与 Lean 形式化的映射核对（v0.5.8）

本节把 SPAF 各环节与 `06 Lean形式化` 的既有定理逐一对照（`CartanAlgebra` 库、`Superconductivity` 库 16 模块）。图例：**✓ 已覆盖**（严格定理已建）、**◐ 部分覆盖**（结构接近、缺具体形式）、**✗ 未覆盖**（缺口）。

> 状态更新（v0.5.7 → v0.5.8）：以下新模块落地：
> - `SPAF_PT.lean`（29 定理）——压强→几何压缩因子 χ(P)、温度→再生产因子 R(T)
> - `ElementCartan.lean`（39 定理）——质/中子层级嘉当矩阵、同位素效应 ε(N)、CQM→BCS 退化
> - `MolecularGeometry.lean`（62 定理）——分子→Weyl嵌入→Regge亏角→GR度规
> - `BridgeTheorems.lean`（23 定理）——谱间隙↔BCS↔Regge 跨模块桥接
> - `BCSIntegralAsymptotic.lean`（9 定理）——BCS 积分渐近（G13 闭合）
> 
> 缺口 3–5 进一步严格化：中子缺陷正定判据（SOS 分解）、双原子耦合正定性（Cauchy-Schwarz）、`bcsConstant_gt_one` 从公理升为定理。
> 
> 状态更新（v0.5.8 → v0.5.9）：文档架构更新——
> - 新增 §0「RQM唯物化基础」：属性随附、因果自组织、电子去特权化三原则
> - 新增 §2.5「探索路径总览」：六层架构（质子/中子→元素→单元素→分子→Regge→牛顿退化）
> - 新增 §5「阶段 0：元素层级」：元素嘉当矩阵组装、主次结构识别、BCS 退化验证
> - 更新 §10 映射核对：新增步骤 0a–0d 的 Lean 状态对照

### 10.1 公理化输入（§3）

| SPAF 输入 | Lean 状态 |
|:---|:---|
| 理想质子 $C_p$ = A₄ 嘉当矩阵 | ✓ `CartanAlgebra.cartanA4` 全系：对称（`cartanA4_symmetric`）、主对角 2（`cartanA4_diag`）、迹 8（`cartanA4_trace`）、det 5（`cartanA4_det_eq_5`）、正定（`cartanA4_positive_definite_real`）、本征值精确正（`eigenvalue1..4_pos`、`eigenvalues_sum_eq_8`）、Aₙ det 模式（`cartanA_det_pattern`）、Weyl 群（`Weyl_group_order_SU5`） |
| 理想 proton = 退相干稳态 4-单纯形 | ◐ L0 现状即 `CausalSet/Axioms.decoherence_steady_state_is_4simplex`（`axiom`，物理假设 H3.3）——与 §1 所述"尚未完成严格证明"一致，非定理 |
| 中子缺陷 $C_n = C_p + \Delta$、$\Delta=\operatorname{diag}(-\epsilon,0,0,0)$ | ✓ `SPAF.neutronDefect`（`diag(−ε,0,0,0)`）+ `SPAF.neutronCartan`（$\epsilon$ 逐点缺陷嘉当矩阵）：对称（`neutronCartan_symmetric`）、对角元（`neutronCartan_diag00` = $2-\epsilon$、`neutronCartan_diag_ne00` = 2）、$\epsilon=0$ 退化质子（`neutronCartan_zero_eq_proton`） |
| $\epsilon = \hbar/(\tau_n\Lambda_{\text{cas}}) \cdot f_{\text{bind}}(Z,A)$ | ✗ 依赖未定义量 $\tau_n$、$\Lambda_{\text{cas}}$；仅有 `PhysicalConstants` 质能常数锚点（$\epsilon$ 的微观赎回属 L0，SPAF 以参数输入处理） |
| 因果耦合 $t_{ij} = t_0 e^{-d_{ij}/\lambda}\Theta(d_{\text{cut}}-d_{ij})$ | ✓ `SPAF.causalCoupling`（以 Heaviside 截断函数）：截断内严格正（`causalCoupling_pos`）、截断外恒零（`causalCoupling_zero_of_cutoff`）、对距离单调衰减（`causalCoupling_antitone_in_distance`，`Real.exp_monotone`）、全局非负（`causalCoupling_nonneg`） |
| 全局幺正性 $\mathcal{C}_{\text{mol}}^\dagger=\mathcal{C}_{\text{mol}}$ | ✓ `SPAF.superCartan_symmetric`（对称矩阵叠加保对称）+ `SPAF.identityBlock_symmetric`（$T_{ij}=t_{ij}I_4$ 标量倍单位矩阵对称）+ `SPAF.cartanA4Stack_symmetric`（A₄ 直接拼接保实对称）；实对称矩阵即自伴 |
| 质子/中子主次结构 | ✓ `ElementCartan.protonSector`（⊕^Z A₄ 纯 A₄ 块对角）+ `ElementCartan.neutronSector`（⊕^N C_n(ε) 缺陷 A₄）+ `ElementCartan.elementCartan`（直和组装） |
| 同位素效应 ε(N) | ✓ `ElementCartan.isotopeDefect`（ε(N) = ε₀·(1+β·(N−N_ref)/N_ref)）+ `ElementCartan.singleElement_BCS_degeneracy`（ε→0 时 CQM→BCS）+ `ElementCartan.cqm_bcs_singleElement_bridge`（CQM↔BCS 桥接） |
| 压强→几何压缩 χ(P) | ✓ `SPAF_PT.geometricCompression`（χ(P) = (P/P_ref)^(1/3)）+ `SPAF_PT.compressionToDebye`（χ(P)→ω_D(P) 桥接）+ `SPAF_PT.compressionToCoupling`（χ(P)→λ(P) 桥接） |
| 温度→再生产衰减 R(T) | ✓ `SPAF_PT.reproductionFactor`（R(T) = exp(−Γ_eff(T)·τ)）+ `SPAF_PT.selfConsistentTc`（T_c^eff = (1−R(T))·T_c^BCS 自洽方程） |
| 分子→Weyl 嵌入→Regge 亏角 | ✓ `MolecularGeometry.molecularSuperCartan` + `MolecularGeometry.weylEmbedding` + `MolecularGeometry.reggeDeficit` + `MolecularGeometry.effectiveGRMetric`（完整管线） |
| 两质子耦合正定性 | ✓ `MolecularGeometry.twoProtonCoupling_exactThreshold`（G20-ext 闭合，SOS 分解 + 黄金比例恒等式） |
| 双原子超嘉当正定性 | ✓ `BridgeTheorems.twoAtomSuperCartan_quadratic_lowerBound`（Cauchy-Schwarz + AM-GM，|t| < λ_min 时正定） |
| A₄ 谱间隙→BCS T_c 上限 | ✓ `BridgeTheorems.spectralGap_bcsTc_bound`（T_c ≤ (2e^γ/π)·ω_D·exp(−1/λ₁)） |
| BCS 积分渐近（G13） | ✓ `BCSIntegralAsymptotic.bcsTcFromIntegral_solved`（积分方程唯一正解 = BCS T_c 闭式）+ `bcsConstant_gt_one`（2e^γ/π > 1 定理） |

### 10.2 四阶段管线（§5 步骤号，v0.5.9 扩展）

| 步骤 | 内容 | 状态与 Lean 对应 |
|:--|:---|:---|
| 0a. 质子/中子分配 | 按 $(Z, N)$ 分配 $C_p$、$C_n(\epsilon)$ | ✓ `ElementCartan.protonSector`（⊕^Z A₄）+ `ElementCartan.neutronSector`（⊕^N C_n(ε)） |
| 0b. 元素嘉当矩阵组装 | $\mathcal{C}_{\text{element}} = (\oplus^Z C_p) \oplus (\oplus^N C_n)$ | ✓ `ElementCartan.elementCartan`（直和组装）+ `elementCartan_symmetric` / `elementCartan_trace` |
| 0c. 主次结构识别 | 质子扇区（主）vs 中子扇区（次）谱间隙 | ◐ 主结构谱间隙 λ₁ = (3−√5)/2 已知（`CartanAlgebra`）；次结构谱间隙偏移 δ(ε) 有界但未闭合 |
| 0d. BCS 退化验证 | ε→0 时 CQM→BCS | ✓ `ElementCartan.singleElement_BCS_degeneracy` + `cqm_bcs_singleElement_bridge`（严格退化定理） |
| 3. 组装 $\mathcal{C}_{\text{mol}}$（$\oplus$ 部分） | $\bigoplus C_i$（跨质子零耦合）全系已证 | ✓ `cartanA4Stack_zero_of_proton_ne` / `_block_eq` / `_diag` / `_trace_eq`（Tr=8n）/ `cartanA4Stack_det_eq`（det=5ⁿ）——大量金属氢的禁闭几何按质子数线性累加、不因拼接稀释 |
| 3b. 组装（$\sum T_{ij}$ 项） | $T_{ij}=t_{ij}I_4$ 耦合项 | ✓ `SPAF.identityBlock_symmetric`（标量倍单位矩阵对称）+ `SPAF.superCartan_symmetric`（叠加保对称）——§3.5 全局幺正约束的严格版；$t_{ij}$ 数值未建模 |
| 4. $H_{\text{eff}}=V^T\mathcal{C}_{\text{mol}}V$（投影） | 部分特征值 | 无 Lean 内容（数值流程） |
| 5. Weyl 生成元 | A₄ 的 Weyl 群已知 | ◐ `Weyl_group_order_SU5`（S₅）、`cartanRank_eq_rankSU5`；H_eff 内禀 Weyl 群无构造 |
| 6–7. 轨道 + 凸包 = 5 等距顶点 → A₄ 判定 | f-向量回文 (5,10,10,5)、euler 0 | ◐ 基块性质在 `CartanAlgebra`；"凸包 5 顶点等距 → A₄"判定算法未实现 |
| 8–9. 分子间耦合 + $\mathcal{C}_{\text{bulk}}$ 分块稀疏 | 指数耦合 | ◐ 块对角版本已证（`cartanA4Stack_*`）；分子间 $t_{\text{inter}}$ 项未覆盖 |
| 10–11. 宏观有效几何 | 周期性投影/拼接 | ◐ 拼接的尺度性（Tr=8n、det=5ⁿ）已证明拼接不稀释整体拓扑 |
| 12. 拓扑不变量（陈数 / Z₂） | | ✗ 未覆盖 |
| 13. $\Gamma_{\text{rel}}(T)$ 与 $T_c \equiv T_{\text{lock}}$ | | ◐ 锁定因子 e^{−Γτ}（`Integral.phaseLockingFactor_pos`）、再生产维持（`phaseLockingFactor_tendsto_zero`）、涌现积分正性（`emergenceIntegral_pos`）已证；$\Gamma_{\text{rel}}=\sum_{a,b}|\dot P_{a\to b}|\ge 0$ 已证（`SPAF.flavorFlowRate_nonneg`，非负性前提）；$T_c\equiv T_{\text{lock}}$ 恒等式未证明 |
| 15–19. Regge 边长/亏角/E-H 作用 | 边长 $\ell_e = \kappa/\sqrt{\lambda_e}$ | ◐ 边长正性已证（`SPAF.reggeEdgeLength_pos`，κ>0、λ_e>0 ⟹ ℓ_e>0）；亏角/E-H 作用、量子化锚点（`fluxQuantum_eq_pi` 已证 Φ0=h/2e）未接入 |

### 10.3 材料标定与证伪（§6–§7）

| SPAF 检验 | 状态 | Lean 对应 |
|:---|:---|:---|
| 6.1 同位素效应 α | ✓ | `criticalTemperature_isotope_shift`、`hydrogen_deuterium_isotope_shift`（$T_c(D)=\frac{T_c(H)}{\sqrt2}$）、`debyeFrequency_decreases_with_mass`、`criticalTemperature_decreases_with_ion_mass`、`naive_cqm_isotope_anomaly`、`hydrogen_phonon_higher_than_deuterium` |
| 反向标定机制 | ◐ | `stiffnessRefCalibrated` + `hydrogen*_calibrated_eq`（以主流 ω_D 反解 k₀、精确还原到 BCS 闭式；非 $t_0$ 的直接形式） |
| 6.2 掺杂 $\epsilon(x)$ | ✗ | 未覆盖（需先建 ε 与掺杂-缺陷映射） |
| 6.3 键角 → A₄ 锁定度 | ✗ | 未覆盖 |
| 6.4 压力 → a(P) → t_ij | ✗ | 未覆盖：P→a(P)→d_ij→t_ij 整条压力线未建；已有骨架：`bcsCriticalTemperature_mono_in_debye`（ω_D 上推 T_c）、`causalCutoff_linear_in_effective_mass`、`neutronStar_cutoff_blueshift`（强引力蓝移） |
| 6.5 室温探索 | ✓ | `roomTemperature_iff_debyeLowerBound`（T_c≥T_room ⟺ ω_D≥(T_room/2e^γ/π)·e^{1/λ}）、`roomTemperatureDebyeLowerBound_antitone_in_coupling`，与双单调线（`.mono_in_debye`/`.mono_in_coupling`） |
| 7. 普通金属排除 | ✓（网络必然性） | `Mechanism.no_superconductivity_without_relation_network`、`.requires_relation_network` |
| 7. 引力-超导一致性 | ✓（CQM 特有） | `StrongGravity` 系 + `strong_gravity_does_not_lower_causal_cutoff`、`strong_gravity_keeps_pairing_channels`；Regge 一致性未覆盖（阶段 IV 无形式化） |

### 10.4 缺口清单（可形式化优先序）

缺口按「定义新量的规模 + 证明难度」排序，便于决定形式化次序：

1. ~~[易] $t_{ij}$ 指数耦合族~~：**已完成（SPAF.lean）**——`causalCoupling` 截断内严格正、截断外恒零、对距离单调减、全局非负（`exp_monotone` + `mul_pos`）；
2. ~~[易] 组装对称性~~：**已完成（SPAF.lean）**——`superCartan_symmetric` / `identityBlock_symmetric` / `cartanA4Stack_symmetric` 覆盖 §3.5 全局幺正约束的严格版本；
3. **[易→◐] 中子缺陷矩阵**：对称、$\epsilon=0$ 退化、对角元、$\epsilon<2$ 时缺陷位对角元为正、**正定判据已证**（`neutronCartan_*`）——SOS 二次型分解 $x^{\dagger}C_nx=(1-\epsilon)x_0^2+x_3^2+(x_0-x_1)^2+(x_1-x_2)^2+(x_2-x_3)^2$（`neutronCartan_quadratic`）；**正方向** $\epsilon<1$ 严格（`neutronCartan_posDef_of_lt_one`），因而判据原文 $\epsilon<\lambda_{\min}$（$\lambda_{\min}=(3-\sqrt5)/2\approx0.382$）亦然（`neutronCartan_posDef_of_lt_spectralGap`）；**反方向** $\epsilon\ge 5/4$ 非正定（见证 $(4,3,2,1)$：$x^{\dagger}C_n x=20-16\epsilon\le0$，`neutronCartan_not_posDef_of_five_fourths_le`）。**仍缺**：$\epsilon\in[1,5/4)$ 区间内正定保持（Sylvester 余子式族展开，数学库未直接建）；**原述「$\epsilon\ge\lambda_{\min}$ 即丧失正定」修正**：真正界是 $\epsilon<5/4$，$\lambda_{\min}\le\epsilon<1$ 区间仍正定；
4. **[中→◐] 味空间概率流**：$\Gamma_{\text{rel}}\ge 0$ **已证**（`flavorFlowRate_nonneg`）；**仍缺**：$T_{\text{lock}}$ 定义与 $T_c\equiv T_{\text{lock}}$ 恒等式（动力学实现）；
5. **[中→◐] Regge 边长正性**：$l_e=\kappa/\sqrt{\lambda_e}>0$ **已证**（`reggeEdgeLength_pos`）；**仍缺**：单位/谱正性嵌入与亏角/E-H 作用；
6. **[中→✓] 压力线**：$P \to a(P) \to d_{ij} \to t_{ij}$ 的压缩增耦合单调线——**形式化**：`SPAF_PT.geometricCompression`（χ(P) = (P/P_ref)^(1/3)）+ `SPAF_PT.compressionToDebye` / `compressionToCoupling`（桥接定理）；**仍缺**：压力→Regge 亏角→GR 度规的数值闭环；
7. **[重] 凸包 A₄ 判定、拓扑不变量、Regge 运动方程、掺杂相图**：需新数学（凸包算法定理、陈数、Regge），暂不部署。
8. ~~[重] 两质子耦合精确阈值~~：**已完成（MolecularGeometry.lean）**——`twoProtonCoupling_exactThreshold`（G20-ext 闭合，SOS 分解 + 黄金比例恒等式）；
9. ~~[重] BCS 积分渐近（G13）~~：**已完成（BCSIntegralAsymptotic.lean）**——`bcsTcFromIntegral_solved`（积分方程→闭式 T_c 唯一正解）+ `bcsConstant_gt_one`（2e^γ/π > 1 定理）；
10. ~~[重] 分子超嘉当矩阵谱间隙界~~：**已完成（BridgeTheorems.lean）**——`twoAtomSuperCartan_quadratic_lowerBound`（Cauchy-Schwarz + AM-GM 严格证明）

### 10.5 新增缺口（v0.5.9，探索路径扩展）

以下缺口对应 §2.5 六层架构中尚未形式化的部分：

11. **[中] 次结构谱间隙闭式**：中子扇区 $C_n(\epsilon)$ 的最低本征值 $\lambda_1^{(n)}(\epsilon)$ 的精确闭式表达式。当前仅知其存在区间（$\epsilon < 5/4$ 时正定）和 $\epsilon=0$ 退化值 $\lambda_1 = (3-\sqrt{5})/2$，但 $\epsilon > 0$ 时的解析闭式未建立。
12. **[中] 主次结构谱间隙差**：$\Delta\lambda(Z, N) = \lambda_1 - \lambda_1^{(n)}$ 作为 $(Z, N)$ 的函数，与同位素效应指数 $\alpha$ 的定量关系。当前仅通过 `ElementCartan.isotopeDefect` 建立了 $\epsilon(N)$ 的参数化，但 $\Delta\lambda \to \alpha$ 的映射未严格推导。
13. **[重] 因果分辨率的形式化**：§2.5 层级 VI 中"同一引力场在不同因果分辨率下细节不同"的物理陈述需要形式化。核心问题是：Regge 亏角密度 $\rho_{\delta}$ 与连续极限下的 Ricci 标量 $R$ 之间，因果分辨率 $\tau_{\text{res}}$ 如何作为截断参数进入。
14. **[重] 牛顿引力退化定理**：在宏观弱场极限下，$g_{\mu\nu}^{\text{eff}}$ 退化到 Poisson 方程 $\nabla^2 \Phi = 4\pi G \rho$ 的严格证明。当前 `ElementCartan` 中仅有 `newtonianGravity_degeneracy` 诚实 `def` 占位。
15. **[中] 单元素拼接规则特殊性**：单元素材料（$\epsilon \to 0$）的拼接规则与多元素材料的拼接规则之间的差异形式化。当前 `ElementCartan.singleElement_BCS_degeneracy` 仅证明退化极限存在，但退化路径（$\epsilon$ 以何种速率趋近于 0）未参数化。

（注：§8 L0 赎回路径的现状 = `CausalSet/Axioms` 物理假设集（H3.3 为 `axiom`）；$t_{ij}$ 指数形式的 L0 推导（CouplingSpace 正则对易特征线）尚未能用于该形式。）

---

**[TL;DR]** 基础层尚未闭合，应用层以理想 A4 积木为公理、以已知超导体为锚点，反向标定 5 个有效参数。参数锁定后，框架具备预测新材料能力；未来基础层证明将严格赎回这些参数的来源。半唯像不是妥协，而是有效理论走向可计算物理的必由之路。
