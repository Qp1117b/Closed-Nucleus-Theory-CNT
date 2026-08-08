# CQM 室温超导方向

> **上承**：[CQM 超导 涌现论](./CQM%20超导%20涌现论.md)、[CQM 超导 涌现积分](./CQM%20超导%20涌现积分.md)、[CQM 超导 金属氢机制与计算框架](./CQM%20超导%20金属氢机制与计算框架.md)
> **SPAF 框架**：[CQM SPAF 半唯像应用框架](./CQM%20SPAF%20半唯像应用框架.md)（v0.5.9，六层探索架构、元素主次结构、BCS 退化方向）
> **Lean 形式化**（v0.5.9，16 模块，310 定理）：`Reduction.lean`、`FirstPrinciples.lean`（第一性链 + 室温方向双单调骨架 + 室温可行域量化判据）、`SPAF_PT.lean`（压强-温度几何构型：χ(P)、R(T)、自洽 T_c）、`ElementCartan.lean`（元素主次结构、CQM→BCS 退化）、`MolecularGeometry.lean`（分子几何→Regge亏角→GR度规）
> **数值实现**：原 Python 唯项计算脚本（CQM_SPAF_PT_唯项计算、test_metallic_hydrogen_800GPa_300K）已作为落后脚本删除，其压强标度律与 T_c(P) 穹顶的数值例现由 `SPAF_PT.lean` 的已证定理（几何压缩因子、自洽 T_c）覆盖。

---

## 0. 从公式到方向

CQM 退化到 BCS 后的 T_c 公式（自然单位）：

$$k_B T_c = \frac{2e^\gamma}{\pi} \cdot \omega_D \cdot \exp\left(-\frac{1}{N(0)V}\right), \qquad \omega_D = \sqrt{\frac{k}{M_{\text{ion}}}}$$

（2e^γ/π ≈ 1.1339；文献公式常写 1.13，那只是三位数值近似。）

**方向骨架已形式化**（`bcsCriticalTemperature_mono_in_debye` /
`bcsCriticalTemperature_mono_in_coupling`）：T_c = 常·ω_D·e^{−1/λ} 对 ω_D 与 λ
**均为单调不减**——室温路线只可能沿两个坐标：提高 ω_D（轻晶格 + 高压硬化）与
提高 λ（强耦合）。凡声称的室温材料都必须落在这一双单调骨架内。

**室温可行域量化判据（新严格化）**（`roomTemperature_iff_debyeLowerBound`
`roomTemperatureDebyeLowerBound_antitone_in_coupling`）：给定目标室温 T_room，

$$T_c(\omega_D, \lambda) \geq T_{room} \iff \omega_D \geq \frac{T_{room}}{2e^\gamma/\pi}\, e^{1/\lambda}$$

左边是室温可行域，右边给出达成室温**必需的德拜频率下界** f(λ) = (T_room/2e^γ/π)·e^{1/λ}。
推论（已严格证明）：f(λ) 随 λ **反单调**——强耦合系统性降低所需的 ω_D 下界。于是
两大室温杠杆可沿等值下界互换/叠加：轻晶格 + 高压（把 ω_D 抬过某个 λ 下的下界）与
强耦合（把下界本身压低）是同一不等式两侧的两种等价发力方向。

室温目标（T_c ≥ 300 K）立即给出**三条可操作的杠杆**：

| 杠杆 | 公式位置 | 物理手段 |
|:---|:---|:---|
| **轻离子** | M_ion → 最小 | 氢（M = M_proton，全周期表最小；D 减半） |
| **强耦合** | N(0)V → 最大 | 金属化 + 费米面嵌套 + 高态密度（van Hove 奇点） |
| **高刚度** | k → 最大 | 高压压缩（体积小 → 力常数大），化学预压 |

CQM 本体论为这三条杠杆提供统一表述：**室温超导 = 最大化质子有限本体
网络的密度、纯度和因果锁定刚度**。氢是唯一同时最大化全部三条杠杆的元素
（最轻 + 高压下最强耦合 + 网络最纯）——这正是 2026 年全部室温候选材料
都是"富氢化合物"的 CQM 理由。

---

## 1. CQM 判据：T_c 上限与最佳窗口

对给定材料，CQM 预言的压力最佳窗口由两个竞争项决定：

- 压力 ↑ → 体积 ↓ → 力常数 k ↑ → ω_D ↑（T_c 上升）
- 压力 ↑ → λ 通常 ↓（LaH10: 220 GPa 时 4.24 → 300 GPa 时 1.86）（T_c 下降）

**最优压力 ≈ 两者交叉的窗口**。实验事实（LaH10 最佳窗口 ~170 GPa、H3S ~155 GPa）
与理论计算一致。CQM 的附加承诺：引力拓扑因子 T_grav(Φ) = 1 + Φ + Φ² 在整个
窗口内只增强因果锁定，因此**强引力本身不构成室温超导的障碍**（
`strong_gravity_keeps_pairing_channels`、`gravitationalTopologyFactor_ge_one`）。

---

## 2. 三条路线

### 路线 A：金属氢本体（终极目标）

- **对象**：原子金属氢（P ≈ 400–500 GPa 的晶态氢）。
- **CQM 理由**：100% 质子有限本体网络，无任何缺陷本体稀释；ω_D 理论极大；
  同位素定律最纯粹（α = 1/2 精确）。
- **现状**：第一性计算预言 T_c 在 200–400 K 量级（各方法差异大）；
  实验上高温超导态尚未确证（Metallic hydrogen 的室温导电性仍有争议）。
- **CQM 判别性预言**：若同位素实验测得 α 精确 = 1/2（几何因子无质量标度），
  则金属氢是纯 BCS 晶格扇区；若 α 偏离，则是几何因子（因果屏蔽）的证据。

### 路线 B：富氢化合物（化学预压，最接近现实的路线）

- **对象**：LaH10（250–260 K @ 170 GPa）、H3S（203 K @ 155 GPa）、YH6/YH9、
  CaH6 等。
- **CQM 理由**：重元素"预压"替身（化学预压）在 ~170 GPa 就达到金属氢
  在 ~400 GPa 才能达到的网络密度；氢亚晶格贡献 λ 的 80–90%，是网络的真正主体。
- **方向**：
  1. **提高 H 含量**：LaH10 → LaH16（已预言 156 K）、YH10（理论预言可达
     303 K @ 400 GPa，Peng 2017）——氢越多，网络越纯。
  2. **机器学习结构搜索**：寻找更高 λ 或更高 ω_D 的稳定氢化物
     （HfH10、ThH10 等候选族）。
  3. **量子声子稳定化**：Errea 2020 证明量子非谐效应把 Fm3̄m-LaH10 稳定到
     实验压力窗口——量子晶格效应（= CQM 中晶格因果锁定的非经典部分）
     是高压氢化物合成的关键自由度。
- **CQM 预期**：300 K 目标在 LaH10 家族的方向上，需要把 ω_ln 从 ~1150 K
  提到 ~1500 K（更纯 H 网络）或把 λ 从 2.35 提到 ~3（量子声子稳定化的
  强耦合结构）。

### 路线 C：常压/低压路线（亚稳工程）

- **对象**：亚稳氢化物、氢富集薄膜、异质结/界面超导、二维氢化物。
- **CQM 理由**：T_c 只依赖 ω_D·exp(−1/λ) 这两个网络量，不依赖"必须整体
  金属化"——只要能构造出局部高密度、高完整性的质子网络。
- **方向**：非静水压 + 应变工程（力常数 k 的局域增强）、
  轻元素合金（Be、B、C 氢化物）、氢原子注入（PdH 类但提高 H 化学势）。
- **CQM 预期**：这条路线目前无确证候选，但它是"降低压力"的唯一长期出路。

---

## 3. CQM 的独特贡献与判别性实验

### 3.1 同位素指数：CQM 存在性探针

BCS 谐波预言 α = 1/2。H3S/D3S 实测 α ≈ 0.466（偏差来自非谐 + S 亚晶格）。
**CQM 预言**：几何因子 f(M) 引入质量标度时，α 系统性偏离 1/2，且偏离量随压力
可调（模型函数 cqm_geometric_isotope_exponent（非 Lean 符号）：
f(D)/f(H) = 0.9 ⇒ α ≈ 0.65；Lean 未形式化此预言——它依赖未标定的 f(M)）。

> **判别性实验**：对同一材料（如 LaH10）在不同压力下做 H/D 同位素实验，
> 测 α(P) 曲线。若 α 随压力偏离 1/2，且与
> f(P) = M_eff/M_ion 的因果屏蔽标度一致——CQM 几何因子成立；
> 若 α(P) ≡ 1/2（扣除非谐修正后）——CQM 的"朴素"退化成立，几何因子无质量标度。

### 3.2 强引力不破坏超导的实验室检验

第 5 层的核心命题在 150–300 GPa 的 DAC 实验中处于**有效检验范围**
（强引力拓扑因子 T_grav ≥ 1 的方向性）。金属氢的 T_c(P) 曲线的斜率
（实验：LaH10 在 170–210 GPa 以 6±1 K/40 GPa 下降；理论：16 K/40 GPa）
与 CQM 的"引力只增强、压力竞争项决定斜率"解释相容。

> **CQM 特有方向（引力退相干不破坏、反而支撑超导）**：CQM 中引力场是
> **因果限制退相干场**（G2 禁闭-退相干等价），对电子基础自由度做关系性筛选
> （P_C 投影）后才涌现超导新自由度（[CQM 超导 涌现积分](./CQM%20超导%20涌现积分.md)）。
> 因此强引力场不仅不必然破坏超导，反而是"退相干筛选 → 涌现"链路的必要环节
> （`strong_gravity_does_not_lower_causal_cutoff`、
> `strong_gravity_keeps_pairing_channels`）。室温方向的 CQM 推论：
> 超导态必须在高压（强引力）环境中**持续再生产**——锁定因子 e^{−Γ|τ|} 随
> 再生产间隔衰减（`phaseLockingFactor_tendsto_zero`），高压下因果耦合事件密度高、
> 有效 Γ 大，恰好满足"反复维持"条件（坍缩难题②的确定性由再生产机制承载）。

### 3.3 网络完整性定理

`superconductivity_requires_relation_network`：网络通道数为零则无超导。
推论：非晶化、空位、同位素无序（H/D 混晶）线性压低 T_c——这是
"缺陷本体稀释网络"的量化预言，可在薄膜实验中直接检验。

---

## 4. 路线图（v0.5.9 更新）

```
第一步（已完成，形式化）   CQM→BCS 退化与还原（Reduction.lean，24 定理）
                           + 第一性推导链（FirstPrinciples.lean，26 定理）
                           + BCS 积分渐近（BCSIntegralAsymptotic.lean，G13 闭合）
                           + 桥接定理（BridgeTheorems.lean，谱间隙↔BCS↔Regge）
第二步（已完成，框架）     金属氢机制 + T_c 计算框架（H3S/LaH10 验证）
                           + 第一性数值例链（校准标定）
                           + 元素嘉当矩阵（ElementCartan.lean，质/中子主次结构）
                           + 分子几何→Regge 亏角（MolecularGeometry.lean，51 定理）
                           + 压强-温度几何构型（SPAF_PT.lean，29 定理）
                           + 数值例链（已由 SPAF_PT.lean / MolecularGeometry.lean / FirstPrinciples.lean 的已证定理覆盖，原 Python 唯项计算脚本已删除）
第三步（本文件）           室温超导方向：A 金属氢 / B 富氢化合物 / C 亚稳工程
                          ↓
   近期（实验室可达）
   1. LaH10 家族 H/D 同位素实验：测 α(P) —— CQM 判别性实验
   2. 提高 H 含量：LaH16/YH10 类化合物的合成与 T_c 测量
   3. 压力-耦合竞争窗口的系统扫描（P 扫描 + λ 第一性计算）
   4. 量子声子稳定化结构（Fm3̄m 类）的强耦合 Eliashberg 精确计算
   5. 缺陷/非晶化对 T_c 的量化压低实验（网络完整性检验）
   6. 金属氢（400-500 GPa）的 T_c 测量与同位素实验 —— 终极检验
   7. 常压方向：氢富集薄膜 + 应变工程的亚稳候选搜索
   中期（形式化推进）
   8. 次结构谱间隙闭式（G14）：C_n(ε) 最低本征值解析表达式
   9. 主次结构谱间隙差→同位素效应映射（G15）：Δλ(Z,N) → α 的严格推导
   10. 牛顿引力退化定理（G17）：Regge 有效度规→Poisson 方程
   长期（理论与实验交汇）
   11. 因果分辨率的形式化（G16）：Regge 亏角密度→Ricci 标量，τ_res 作为截断参数
   12. 完整六层管线端到端数值验证：元素→分子→Regge→GR→超导 T_c
```

---

## 5. 结论

1. **第一步**（Lean 公式层对应）：CQM 退化到晶格扇区后还原 BCS 核心公式
   （T_c = (2e^γ/π)·ω_D·exp(−1/λ)、能隙比 2Δ₀/k_BT_c = 2πe^{−γ} ≈ 3.53、
   同位素 α = 1/2、London、ξ₀、Φ₀；3.53 等数值为文献近似）；
   `naive_cqm_isotope_anomaly` 为**条件定理**：朴素替换下 T_c 随质量单调
   不减、与实验相反——它标示而非证明退化的必要性。
2. **第二步**（框架已建立）：金属氢是 CQM 的理想推导对象（质子 = 最小最纯
   有限本体）；计算框架（BCS → McMillan–Dynes → Eliashberg）在 H3S/LaH10
   上验证，同位素 α ≈ 0.466 与 √(1/2) 的偏离打开 CQM 判别窗口。
3. **第三步**（方向已指明）：室温超导的 CQM 路径 = **富氢化合物**（路线 B，
   最近现实）→ **金属氢本体**（路线 A，终极）→ **亚稳工程**（路线 C，长期）；
   判别性实验是**高压同位素效应 α(P)**。

---

## 参考文献

1. Ashcroft (1968). Metallic Hydrogen: A High-Temperature Superconductor? *PRL* 21, 1748.
2. Drozdov et al. (2015). *Nature* 525, 73 (H3S, 203 K).
3. Drozdov et al. (2019). *Nature* 569, 528 (LaH10, 250 K).
4. Errea et al. (2020). Quantum crystal structure in the 250-kelvin superconducting phase of LaH10. *Nature* 578, 66.
5. Peng et al. (2017). High-temperature superconductivity in Y-H system. arXiv:1706.01234（YH10 理论预言 ≈ 303 K @ 400 GPa）.
6. Liu et al. (2019). Microscopic mechanism of room-temperature superconductivity in compressed LaH10. *PRB* 99, 140501(R).
7. Duan et al. (2014). Pressure-induced metallization of dense (H2S)2H2. *Sci. Rep.* 4, 6968.
8. ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
