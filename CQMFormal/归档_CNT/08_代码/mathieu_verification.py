#!/usr/bin/env python3
"""验证 Mathieu 特征值 vs 已知微扰级数"""
import mpmath as mp
mp.mp.dps = 50

def mathieu_eval(q, m, n=80):
    """返回 Mathieu 最低特征值"""
    N = n
    if m == 1:
        H = mp.matrix(N,N)
        H[0,0] = 1 + q; H[0,1] = -q
        for k in range(1,N):
            nk = 2*k+1; H[k,k] = nk**2
            if k+1<N: H[k,k+1] = -q
            if k-1>=0: H[k,k-1] = -q
    elif m == 2:
        H = mp.matrix(N,N)
        H[0,0] = 1 - q; H[0,1] = -q
        for k in range(1,N):
            nk = 2*k+1; H[k,k] = nk**2
            if k+1<N: H[k,k+1] = -q
            if k-1>=0: H[k,k-1] = -q
    else:
        H = mp.matrix(N,N)
        for k in range(N):
            nk = 2*(k+1); H[k,k] = nk**2
            if k+1<N: H[k,k+1] = -q
            if k-1>=0: H[k,k-1] = -q
    
    E, V = mp.eig(H)
    return min(complex(e).real for e in E)

# 已知微扰级数 (Abramowitz & Stegun, Ch.20)
# b₁(q) = 1 + q - q²/8 + q³/64 - q⁴/1536 + ...
# a₁(q) = 1 - q - q²/8 + q³/64 - q⁴/1536 + ...
# b₂(q) = 4 + q²/12 + 5q⁴/13824 + ...

def b1_series(q):
    qf = float(q)
    return 1 + qf - qf**2/8 + qf**3/64 - qf**4/1536 + qf**5/36864

def a1_series(q):
    qf = float(q)
    return 1 - qf - qf**2/8 + qf**3/64 - qf**4/1536 + qf**5/36864

def b2_series(q):
    qf = float(q)
    return 4 + qf**2/12 + 5*qf**4/13824

qs = [0.1, 0.3, 0.5, 0.658, 0.8, 1.0]
print("验证 Mathieu 特征值 vs 已知微扰级数 (n_terms=80)")
print()
print("m=1 (b₁, DN):")
for qq in qs:
    q = mp.mpf(str(qq))
    num = float(mathieu_eval(q, 1))
    ser = b1_series(q)
    print(f"  q={qq:.3f}: 数值={num:.6f}, 级数={ser:.6f}, 差={abs(num-ser):.2e}")

print()
print("m=2 (a₁, ND):")
for qq in qs:
    q = mp.mpf(str(qq))
    num = float(mathieu_eval(q, 2))
    ser = a1_series(q)
    print(f"  q={qq:.3f}: 数值={num:.6f}, 级数={ser:.6f}, 差={abs(num-ser):.2e}")

print()
print("m=3 (b₂, DD):")
for qq in qs:
    q = mp.mpf(str(qq))
    num = float(mathieu_eval(q, 3))
    ser = b2_series(q)
    print(f"  q={qq:.3f}: 数值={num:.6f}, 级数={ser:.6f}, 差={abs(num-ser):.2e}")

print()
print("CNT 目标值对比:")
print(f"  λ₁(target)=1.316, our b₁(0.658)={float(mathieu_eval(mp.mpf('0.658011'),1)):.4f}")
print(f"  λ₂(target)=3.559, our a₁(1.780)={float(mathieu_eval(mp.mpf('1.779640'),2)):.4f}")
print(f"  λ₃(target)=7.433, our b₂(3.716)={float(mathieu_eval(mp.mpf('3.716423'),3)):.4f}")
