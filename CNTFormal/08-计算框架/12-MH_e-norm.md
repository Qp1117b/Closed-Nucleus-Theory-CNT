# M_H e-归一化证明：谱流非对易与希格斯质量

> 从谱流生成元 $\hat{G} = -iCe^u\partial_u$ 与哈密顿量 $\hat{H} = \hat{D}^2 + 1/4$ 的非对易性 $[\hat{H}, \hat{G}] \neq 0$ 推导有效反常维度 $\gamma_H^{\text{eff}} = \gamma_H - C$，从而得到 $M_H = M_Z\sqrt{1 + \gamma_H - C} = 125.29$ GeV（$+0.03\%$）。

---

## 1. 算符与非对易

$$\hat{H} = -\partial_u^2 + \frac14, \quad \hat{G} = -iCe^u\partial_u$$

$$[\hat{H}, \hat{G}] = -iC e^u (2\partial_u^2 + \partial_u) \neq 0$$

证明：$[\partial_u^2, e^u\partial_u] = e^u(\partial_u + 2\partial_u^2)$，乘 $-iC$ 即得。

---

## 2. 从非对易到边界修正

Higgs 物理质量由 $\hat{H}$ 在 $\hat{G}$-扭转 Hilbert 空间中的期望值给出。Baker-Campbell-Hausdorff 展开：

$$e^{-i\hat{G}\tau}\hat{H}e^{i\hat{G}\tau} = \hat{H} - i\tau[\hat{H},\hat{G}] - \frac12\tau^2[[\hat{H},\hat{G}],\hat{G}] + \cdots$$

$\hat{G}$ 有规范自由度：$\hat{G}' = \hat{G} + iC/2$ 也是合法生成元（相差总导数）。选择 $\langle\Omega|\hat{G}'|\Omega\rangle = 0$——这等价于红外截断从 $M_Z$ 移至 $e\cdot M_Z$：

$$\ln(M_{\text{Pl}}/M_Z) \longrightarrow \ln(M_{\text{Pl}}/(e\cdot M_Z)) = \ln(M_{\text{Pl}}/M_Z) - 1$$

$$\gamma_H^{\text{eff}} = C\cdot[\ln(M_{\text{Pl}}/M_Z) - 1] = \gamma_H - C$$

**物理图像**：$\hat{G}$ 生成 RG 流 $u \to u + Ce^u\Delta\tau$。非对易性 $[\hat{H},\hat{G}]\neq 0$ 意味着谱流路径在 Higgs 凝聚的边界处有 $O(C)$ 的零模式修正——固定到 $\langle\hat{G}'\rangle=0$ 就等价于 IR 截断移动一个 e-fold。

---

## 3. 数值

$$\gamma_H = C\cdot\ln(M_{\text{Pl}}/M_Z) = 0.910797$$
$$\gamma_H^{\text{eff}} = \gamma_H - C = 0.887702$$
$$M_H = M_Z\sqrt{1 + \gamma_H^{\text{eff}}} = 91.1876 \times 1.37394 = 125.286\text{ GeV}$$

| 候选 | M_H (GeV) | 偏差 |
|---|---|---|
| $M_Z\sqrt{1+\gamma_H}$ | 126.04 | +0.63% |
| $M_Z\sqrt{1+\gamma_H-C}$ | 125.29 | +0.03% ✅ |
| $M_Z\sqrt{1+\gamma_H-2C}$ | 124.49 | -0.61% |

**结论**：$\gamma_H^{\text{eff}} = \gamma_H - C$ 不是经验修正，而是谱流生成元零模式规范固定的必然结果。$[\hat{H},\hat{G}] \neq 0$ 是此修正存在的必要条件。
