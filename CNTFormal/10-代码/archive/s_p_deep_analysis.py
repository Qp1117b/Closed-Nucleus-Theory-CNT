#!/usr/bin/env python3
"""
s_p 深度模式分析
===============
发现:
  s_3 = 2 + 1/√2  (偏差 0.0076%)
  s_2 = 5/14     (偏差 0.0076%)
  两者偏差一致 → 近似精确恒等式
"""
import mpmath as mp
mp.mp.dps = 60

C = 1 + mp.euler/2 - mp.log(4*mp.pi)/2
g1 = mp.zetazero(1).imag
E1 = mp.mpf('0.25') + g1**2

def qc():
    def tail(q,k):
        if k > 60: return mp.mpf('0')
        n = 2*k+1
        return q**2/(n**2 - 2*q - tail(q,k+1))
    return mp.findroot(lambda q:1-3*q-tail(q,1),(29-mp.sqrt(661))/10)
q_c = qc()
lc = 4*q_c

ap = {2:mp.mpf('1.544317'),3:mp.mpf('0.430377'),5:mp.mpf('0.841413')}
s_obs = {2:mp.mpf('0.357170'),3:mp.mpf('2.707312'),5:mp.mpf('0.508952')}

s3_exact = 2 + 1/mp.sqrt(2)
s2_exact = mp.mpf(5)/14

def Gp(p,s):
    return (1-p**(s-1))/(1-p**(-s))

print("="*72)
print("  发现1: s_3 = 2 + 1/√2   s_2 = 5/14  偏差一致")
print("="*72)
d3 = (s_obs[3]-s3_exact)/s3_exact
d2 = (s_obs[2]-s2_exact)/s2_exact
print(f"  s_3 偏差: {float(d3*100):+.8f}%")
print(f"  s_2 偏差: {float(d2*100):+.8f}%")
print(f"  比值: {float(d3/d2):.6f}")
print(f"  偏差绝对值: {float(d3):.3e}")
# 检查偏差是否为 C/304 ≈ 7.6e-5
print(f"  C/300 = {float(C/300):.3e}")
print(f"  C/304 = {float(C/304):.3e}")
print(f"  C/(E1/4) = {float(C/(E1/4)):.3e}")

print("\n" + "="*72)
print("  发现2: s_5 = ? — 系统搜索")
print("="*72)
print(f"  s_5 obs = {float(s_obs[5]):.10f}")

# 以 s_2 和 s_3 为锚点搜索 s_5
print("\n  --- s_5 / s_2 关系 ---")
r52 = s_obs[5]/s2_exact
print(f"  s_5/s_2_exact = {float(r52):.10f}")
print(f"  √2 = {float(mp.sqrt(2)):.10f}  偏差 {float((r52-mp.sqrt(2))/mp.sqrt(2)*100):+.4f}%")
print(f"  1.425 = {float(mp.mpf('1.425')):.10f}")
print(f"  e/2 = {float(mp.e/2):.10f}")
print(f"  π/2.2 = {float(mp.pi/2.2):.10f}")

print("\n  --- s_3 × s_5 / s_2 ---")
print(f"  s_3_exact × s_5/s_2 = {float(s3_exact*r52):.10f}")

print("\n  --- s_5 作为 s_2 和 s_3 的函数 ---")
# s_5 = s_2 × √(s_3 - 1)?
pred = s2_exact * mp.sqrt(s3_exact - 1)
print(f"  s_2√(s_3-1) = {float(pred):.10f}  偏差 {float((s_obs[5]-pred)/s_obs[5]*100):+.4f}%")
# s_5 = s_2/√(s_3 - 2)?
pred = s2_exact / mp.sqrt(s3_exact - 2)
print(f"  s_2/√(s_3-2) = {float(pred):.10f}  偏差 {float((s_obs[5]-pred)/s_obs[5]*100):+.4f}%")

print("\n  --- 纯代数候选 ---")
candidates = [
    ("1/2", mp.mpf('0.5')),
    ("2/π", 2/mp.pi),
    ("1/(2√(π))", 1/(2*mp.sqrt(mp.pi))),
    ("e^{-1}", mp.e**(-1)),
    ("e^{-1/√2}", mp.e**(-1/mp.sqrt(2))),
    ("ln(2)", mp.log(2)),
    ("√2/π", mp.sqrt(2)/mp.pi),
    ("Γ(3/4)/√π", mp.gamma(mp.mpf('0.75'))/mp.sqrt(mp.pi)),
    ("π/6", mp.pi/6),
    ("(e-1)/π", (mp.e-1)/mp.pi),
    ("C/0.04538", C/mp.mpf('0.04538')),
    ("(2-√2)/π", (2-mp.sqrt(2))/mp.pi),
    ("1/(e√2)", 1/(mp.e*mp.sqrt(2))),
]
for name, val in candidates:
    dev = (s_obs[5] - val)/s_obs[5]*100
    flag = " ★" if abs(float(dev)) < 1 else ""
    print(f"  s_5 ≈ {name:<14} = {float(val):.10f}  偏差 {float(dev):+.4f}%{flag}")

print("\n" + "="*72)
print("  发现3: 假设 s_2=5/14, s_3=2+1/√2 精确, 求 s_5 公式")
print("="*72)
# 从几何平均: s_5² = s_2 × s_3 / k, 试 k
print(f"  √(s_2×s_3) = {float(mp.sqrt(s2_exact*s3_exact)):.10f}")
# 从调和平均: 2/(1/s_2 + 1/s_3)
hmean = 2/(1/s2_exact + 1/s3_exact)
print(f"  H(s_2,s_3) = {float(hmean):.10f}")
# 从某种对称性
print(f"  s_2 + s_5 + s_3 = {float(s2_exact + s_obs[5] + s3_exact):.10f}")
print(f"  s_2 × s_5 × s_3 = {float(s2_exact * s_obs[5] * s3_exact):.10f}")

# 关键: s_5 = s_2 × ρ where ρ ≈ √2 × (1 + small_correction)
print("\n  --- 关键模式: s_5 = s_2 × ρ ---")
rho_obs = s_obs[5]/s_obs[2]  # using observed s_2
rho_exact = s_obs[5]/s2_exact  # using exact s_2 = 5/14
print(f"  s_5/s_2_obs   = {float(rho_obs):.10f}")
print(f"  s_5/s_2_exact = {float(rho_exact):.10f}")
print(f"  √2            = {float(mp.sqrt(2)):.10f}")
# 校正项
corr = rho_exact / mp.sqrt(2) - 1
print(f"  (s_5/s_2)/√2 - 1 = {float(corr*100):+.4f}%")
print(f"  C  = {float(C):.6f}")
print(f"  C² = {float(C**2):.6e}")

print("\n" + "="*72)
print("  发现4: 跨扇区 Gamma 关系")
print("="*72)
for p in [2,3,5]:
    g = Gp(p, 1-ap[p])
    S = s_obs[p] * abs(g)
    print(f"  p={p}: s_p={float(s_obs[p]):.10f}  |Γ|={float(abs(g)):.10f}  S={float(S):.10f}")
    print(f"        ln(s_p)={float(mp.log(s_obs[p])):.8f}  ln(|Γ|)={float(mp.log(abs(g))):.8f}  ln(S)={float(mp.log(S)):.8f}")
