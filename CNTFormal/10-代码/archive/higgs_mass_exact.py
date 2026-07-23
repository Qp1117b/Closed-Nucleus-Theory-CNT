#!/usr/bin/env python3
"""
M_H = M_Z × √(1 + C·ln(M_Pl/(e·M_Z))) — 精密验证
=====================================================
理论：γ_H^eff = C·[ln(M_Pl/M_Z) - 1]  （谱流归一化 ln→ln/e）
"""
import mpmath as mp
mp.mp.dps = 60

C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
g1 = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + g1**2
M_PL = mp.mpf('1.220890e19')
M_Z = mp.mpf('91.1876')  # PDG
M_H_exp = mp.mpf('125.25')  # PDG

γ_H = C * mp.log(M_PL / M_Z)

# 候选1: M_H = M_Z · √(1 + γ_H)          (dev +0.64%)
# 候选2: M_H = M_Z · √(1 + γ_H - C)      (dev +0.04%) ★ WINNER

print("="*72)
print("  M_H 第一性公式验证")
print("="*72)
print(f"  C  = {float(C):.10f}")
print(f"  γ_H = C·ln(M_Pl/M_Z) = {float(γ_H):.10f}")
print()

candidates = [
    ("1 + γ_H", 1 + γ_H),
    ("1 + γ_H - C", 1 + γ_H - C),
    ("1 + C·ln(M_Pl/(e·M_Z))", 1 + C * mp.log(M_PL / (mp.e * M_Z))),
    ("1 + γ_H - 2C", 1 + γ_H - 2*C),
    ("1 + γ_H - C/2", 1 + γ_H - C/2),
]

for name, val in candidates:
    r = mp.sqrt(val)
    M_H_pred = M_Z * r
    dev = (M_H_pred - M_H_exp) / M_H_exp * 100
    print(f"  M_H = M_Z × √({name:<25s}) = {float(r):.8f} → {float(M_H_pred):.4f} GeV  偏差 {float(dev):+.4f}%")

print()
print("  实验检验:")
print(f"  M_H_exp = {float(M_H_exp):.4f} ± 0.17 GeV")
M_H_best = M_Z * mp.sqrt(1 + γ_H - C)
print(f"  M_H_CNT = {float(M_H_best):.4f} GeV  (偏差 {(float(M_H_best)-float(M_H_exp))/float(M_H_exp)*100:+.4f}%)")
print(f"  (M_H_CNT - M_H_exp) / σ = {(float(M_H_best)-125.25)/0.17:.2f} σ")
print()

# 深入: ln(M_Pl/(e·M_Z)) 的意义
print("  理论分析:")
print(f"  ln(M_Pl/M_Z) = {float(mp.log(M_PL/M_Z)):.6f}")
print(f"  ln(M_Pl/(e·M_Z)) = ln(M_Pl/M_Z) - 1 = {float(mp.log(M_PL/M_Z)-1):.6f}")
print(f"  γ_H_eff = C·[ln(M_Pl/M_Z) - 1] = {float(C*(mp.log(M_PL/M_Z)-1)):.10f}")
print(f"  γ_H - C = {float(γ_H-C):.10f}  (一致: {float((γ_H-C)-C*(mp.log(M_PL/M_Z)-1)):.2e})")
