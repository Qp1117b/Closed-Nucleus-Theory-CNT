#!/usr/bin/env python3
"""
s_p 统一公式验证
================
假设:
  s_2 = 5/14 (精确)
  s_3 = 2 + 1/√2 (精确)
  s_5 = (5/14) × √2 × (1 + C/3)
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

s2 = mp.mpf(5)/14
s3 = 2 + 1/mp.sqrt(2)

# 候选: s_5 = s_2 × √2 × (1 + C/3)
s5_cand1 = s2 * mp.sqrt(2) * (1 + C/3)
print(f"s_5 候选1 = s_2 × √2 × (1 + C/3)")
print(f"  = {float(s2):.10f} × {float(mp.sqrt(2)):.10f} × {float(1+C/3):.10f}")
print(f"  = {float(s5_cand1):.10f}")
print(f"  obs  = {float(s_obs[5]):.10f}")
print(f"  偏差 = {float((s_obs[5]-s5_cand1)/s_obs[5]*100):+.6f}%")
print()

# 更干净的形式: s_5 = s_2 × √2 + ...
# s_2√2 = 0.505076, s_5 - s_2√2 = 0.003876
s2_sqrt2 = s2 * mp.sqrt(2)
print(f"  s_2 × √2 = {float(s2_sqrt2):.10f}")
print(f"  s_5 - s_2√2 = {float(s_obs[5] - s2_sqrt2):.10f}")
print(f"  C × s_2√2/3 = {float(C * s2_sqrt2 / 3):.10f}")
print(f"  s_2√2 × C/2 = {float(s2_sqrt2 * C/2):.10f}")
print()

# 候选2: s_5 = (3/5) × (s_3 - s_2)? 
s5_cand2 = mp.mpf(3)/5 * (s3 - s2)
print(f"s_5 候选2 = (3/5)(s_3 - s_2) = {float(s5_cand2):.10f}  偏差 {float((s_obs[5]-s5_cand2)/s_obs[5]*100):+.4f}%")
# 候选3: s_5 = s_2 × (1 + s_3/5)?
s5_cand3 = s2 * (1 + s3/5)
print(f"s_5 候选3 = s_2(1+s_3/5) = {float(s5_cand3):.10f}  偏差 {float((s_obs[5]-s5_cand3)/s_obs[5]*100):+.4f}%")
# 候选4: s_5 = s_2 × (s_3 - 2) × (1 + C/2)?
s5_cand4 = s2 * (s3 - 2) * (1 + C/2)
print(f"s_5 候选4 = s_2 × (s_3-2) × (1+C/2) = {float(s5_cand4):.10f}  偏差 {float((s_obs[5]-s5_cand4)/s_obs[5]*100):+.4f}%")
# 候选5: s_5 = (s_2 × s_3) / 1.9?
s5_cand5 = (s2 * s3) / mp.mpf('1.9')
print(f"s_5 候选5 = (s_2×s_3)/1.9 = {float(s5_cand5):.10f}  偏差 {float((s_obs[5]-s5_cand5)/s_obs[5]*100):+.4f}%")
# 候选6: s_5 = s_2 × (s_3 - 2) × (s_3 - 2 + 1)?
# s_3 - 2 = 1/√2
s5_cand6 = s2 * (s3 - 2) * mp.sqrt(s3)
print(f"s_5 候选6 = s_2 × (1/√2) × √s_3 = {float(s5_cand6):.10f}  偏差 {float((s_obs[5]-s5_cand6)/s_obs[5]*100):+.4f}%")

print()
print("="*72)
print("  统一公式模式")
print("="*72)
# 关键观察: s_p = R(p) 其中 R 是某种通用函数
# 检查 s_2 : s_5 : s_3 的比值
print(f"  s_2 : s_5 : s_3 = {float(s2):.6f} : {float(s_obs[5]):.6f} : {float(s3):.6f}")
print(f"  归一化:        = {float(s2/s3):.6f} : {float(s_obs[5]/s3):.6f} : 1")
# 归一化到 s_3 = 1
print(f"  s_2/s_3 = {float(s2/s3):.10f}")
print(f"  s_5/s_3 = {float(s_obs[5]/s3):.10f}")
# s_2/s_3 in terms of simple numbers
print(f"  (s_2/s_3) = (5/14)/(2+1/√2) = {float(s2/s3):.10f}")
# s_2/s_3 ≈ ? 
print(f"  (√2 - 1) = {float(mp.sqrt(2)-1):.10f}  (s_2/s_3偏差 {float((s2/s3-(mp.sqrt(2)-1))/(mp.sqrt(2)-1)*100):+.4f}%)")
print(f"  1/π = {float(1/mp.pi):.10f}  (s_2/s_3偏差 {float((s2/s3-1/mp.pi)/(1/mp.pi)*100):+.4f}%)")
print(f"  1/(π+√2) = {float(1/(mp.pi+mp.sqrt(2))):.10f}")
