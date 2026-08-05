# -*- coding: utf-8 -*-
"""
CQM 超导 T_c 计算器 (CQM Superconductivity Tc Calculator)
=========================================================

对应《CQM 超导 金属氢机制与计算框架》的计算层。纯标准库实现，Python 3。

公式（与 Lean 形式化 Superconductivity.Reduction 逐项对应）：
  BCS 弱耦合（CQM 退化核心）:
      k_B T_c = (2e^γ/π) * hbar * omega_D * exp(-1/(N(0)V))   [bcs_tc]
      （2e^γ/π ≈ 1.1339；文献公式常写 1.13，那只是三位数值近似。
        Lean 内用精确常数 bcsExactConstant，此处用浮点值近似之）
  McMillan-Dynes 强耦合（金属氢化物 lambda ~ 2 需此形式）:
      k_B T_c = (omega_ln/1.2) * exp[-1.04(1+lambda)/(lambda - mu*(1+0.62*lambda))]
                                                                [mcmillan_dynes_tc]
      （1.2 与 1.04 为文献经验系数）
  同位素定律（CQM 退化到晶格扇区后还原 BCS）:
      T_c(M2)/T_c(M1) = sqrt(M1/M2)  =>  alpha = 1/2           [isotope_tc_ratio]
  CQM 几何因子修正（同位素指数偏离 1/2 的预言）:
      M_eff = M_ion * f(geometry),  alpha_eff = 1/2 + d(ln f)/d(ln M)/2

用法:
  python "CQM超导Tc计算器.py"            # 打印验证表与预言
  python "CQM超导Tc计算器.py" 1330 1.94 0.123   # 自定义: omega_ln(K) lambda mu*
"""

import math
import sys

# ---------------------------------------------------------------------------
# 精确常数（与 Lean 模块 Superconductivity.Reduction 的 bcsExactConstant 对应）
# ---------------------------------------------------------------------------

EULER_GAMMA = 0.5772156649015329   # 欧拉-马歇罗尼常数 γ（浮点近似）
BCS_CONST = 2 * math.exp(EULER_GAMMA) / math.pi   # 2e^γ/π ≈ 1.1339
BCS_CONST_LIT_APPROX = 1.13        # 文献三位数值近似（BCS 公式常见写法）

# ---------------------------------------------------------------------------
# 公式层（与 Lean 模块 Superconductivity.Reduction 对应）
# ---------------------------------------------------------------------------

def bcs_tc(w_debye_K, n0v):
    """BCS 弱耦合临界温度：T_c = (2e^γ/π)·omega_D·exp(-1/(N(0)V))。

    (2e^γ/π) 为精确常数（≈1.1339），Lean 内为 bcsExactConstant；
    文献公式常写 1.13，那只是三位数值近似（相对偏差 <0.4%）。
    注意：该公式仅在弱耦合 (N(0)V ≈ λ ≪ 1) 有效。"""
    return BCS_CONST * w_debye_K * math.exp(-1.0 / n0v)


def mcmillan_dynes_tc(omega_ln_K, lam, mu_star):
    """McMillan-Dynes 强耦合临界温度（单位 K）。"""
    den = lam - mu_star * (1 + 0.62 * lam)
    if den <= 0:
        raise ValueError("lambda 不满足强耦合判据 lam > mu*(1+0.62*lam)")
    return (omega_ln_K / 1.2) * math.exp(-1.04 * (1 + lam) / den)


def isotope_tc_ratio(m_light, m_heavy):
    """同位素定律：T_c(重)/T_c(轻) = sqrt(m_轻/m_重)。
       例: H->D, m_light=1, m_heavy=2 => 1/sqrt(2) = 0.707 (alpha = 1/2)。"""
    return math.sqrt(m_light / m_heavy)


def isotope_exponent(tc_h, tc_d):
    """实测同位素指数：alpha = ln(T_c(H)/T_c(D)) / ln(2)。"""
    return math.log(tc_h / tc_d) / math.log(2.0)


def cqm_geometric_isotope_exponent(f_h, f_d):
    """CQM 预言：若几何因子 f(M) 引入质量标度，同位素指数
       alpha = 1/2 + ln(f(H)/f(D))/ln(2)。f 常数时精确回到 1/2。"""
    return 0.5 + math.log(f_h / f_d) / math.log(2.0)


# ---------------------------------------------------------------------------
# 单位换算
# ---------------------------------------------------------------------------

MEV_TO_K = 11.6045    # 1 meV = 11.6045 K (k_B)
CM1_TO_K = 1.4388     # 1 cm^-1 = 1.4388 K (k_B)

# ---------------------------------------------------------------------------
# 材料参数（文献值）
# ---------------------------------------------------------------------------

# (名称, 压力, omega_ln(K), lambda, mu*, 实验Tc(K), 备注)
MATERIALS = [
    # 弱耦合基准（验证 BCS 退化核心）
    ("Al (铝)",           0, 428,    0.43,  0.10,  1.18, "BCS 弱耦合标尺"),
    ("Pb (铅)",           0, 105,    1.55,  0.15,  7.20, "强耦合经典例子"),
    ("MgB2 (二硼化镁)",   0, 750,    0.90,  0.11,  39.0, "双能隙声子超导"),
    # 高压富氢（金属氢化物的代表：H 亚晶格 = 质子有限本体网络）
    ("H3S (硫化氢)",    155, 1330,   1.94,  0.123, 203,  "Drozdov 2015, lambda/omega_ln: Errea 2016"),
    ("LaH10 (氢化镧)",  170, 1147,   2.35,  0.13,  250,  "Drozdov 2019; omega_log=797cm^-1, lambda 于 260GPa"),
]

# 同位素实验（第一步的形式化定理 hydrogen_deuterium_isotope_shift 的对照）
ISOTOPE_EXP = [
    # (体系, T_c(H) K, T_c(D) K, 谐波预言比 sqrt(1/2), 备注)
    ("H3S / D3S @150GPa", 203, 147, "0.707 (H 亚晶格主导)", "0.724"),
]


def main():
    print("=" * 78)
    print("CQM 超导 T_c 计算器 —— 金属氢化物验证表")
    print("=" * 78)
    print(f"{'材料':<16}{'P/GPa':>6}{'omega_ln/K':>11}{'lam':>6}{'mu*':>6}"
          f"{'McMillan/K':>11}{'实验Tc/K':>9}  备注")
    print("-" * 78)
    for name, p, wln, lam, mu, tc_exp, note in MATERIALS:
        try:
            tc = mcmillan_dynes_tc(wln, lam, mu)
        except ValueError:
            tc = float("nan")
        print(f"{name:<16}{p:>6}{wln:>11.0f}{lam:>6.2f}{mu:>6.3f}"
              f"{tc:>11.1f}{tc_exp:>9.1f}  {note}")

    print()
    print("=" * 78)
    print("第一步回顾：CQM 退化到 BCS（Lean: cqm_reduces_to_bcs / bcs_universal_gap_ratio）")
    print("=" * 78)
    # 弱耦合下 BCS 公式（CQM 退化核心）——仅在 lambda << 1 有效
    lam_wc = 0.2
    w_debye_demo = 300  # K
    print(f"  BCS 弱耦合示例(lambda={lam_wc}): T_c = (2e^γ/π)*{w_debye_demo}*exp(-1/0.2)"
          f" = {bcs_tc(w_debye_demo, lam_wc):.2f} K  (2e^γ/π ≈ {BCS_CONST:.4f}，"
          f"文献写 {BCS_CONST_LIT_APPROX})")
    print(f"  ** 金属氢化物 (lambda≈2) 已超出 BCS 弱耦合有效域，必须用 McMillan-Dynes "
          f"(见验证表) —— 这正是 CQM 退化核心之外需要强耦合扩展的原因")
    gap_ratio = 2 * math.pi * math.exp(-EULER_GAMMA)   # 2πe^−γ
    print(f"  普适能隙比: 2*Delta0/(k_B*T_c) = 2πe^−γ = {gap_ratio:.4f}"
          f" (Lean: bcs_universal_gap_ratio 弱耦合极限定理；文献常写 3.53，为数值近似)")
    print(f"  氢/氘同位素定律: T_c(D)/T_c(H) = sqrt(1/2) = {isotope_tc_ratio(1, 2):.4f}"
          " (Lean: hydrogen_deuterium_isotope_shift)")

    print()
    print("=" * 78)
    print("同位素效应实验对照（Lean: hydrogen_deuterium_isotope_shift）")
    print("=" * 78)
    for name, tc_h, tc_d, harmonic, measured in ISOTOPE_EXP:
        alpha = isotope_exponent(tc_h, tc_d)
        print(f"  {name}: T_c(H)={tc_h} K, T_c(D)={tc_d} K")
        print(f"    谐波预言: T_c(D)/T_c(H) = {harmonic}, 实测比 = {tc_d/tc_h:.4f},"
              f" 同位素指数 alpha = {alpha:.3f} (BCS 预言 0.5)")
        print(f"    偏差来源: S 亚晶格不变 + 强非谐性 (CQM 几何因子预言可精确偏离)")

    print()
    print("=" * 78)
    print("CQM 预言：同位素指数作为 CQM 存在性探针")
    print("=" * 78)
    for f_h, f_d in [(1.0, 1.0), (1.0, 0.9), (1.1, 1.0)]:
        alpha = cqm_geometric_isotope_exponent(f_h, f_d)
        print(f"  f(H)={f_h}, f(D)={f_d}: 几何因子引入质量标度 => alpha = {alpha:.3f}"
              " (f 常数 => 精确 1/2)")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        wln, lam, mu = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
        print(f"McMillan-Dynes: omega_ln={wln:.0f} K, lambda={lam}, mu*={mu}")
        print(f"  T_c = {mcmillan_dynes_tc(wln, lam, mu):.1f} K")
    else:
        main()
