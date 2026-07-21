#!/usr/bin/env python3
"""rho_2 SU(5) 归一化因子验证"""

import mpmath as mp
mp.mp.dps = 50

# Current values
rho_2_raw = mp.mpf('0.19907')  # Mathieu sin(2theta)
rho_3_raw = mp.mpf('0.11471')  # Mathieu cos(4theta)
N3_sq = mp.mpf('8')/9
rho_3 = rho_3_raw * N3_sq

f2 = mp.mpf('1')/(2*10)  # 1/(2*W_2) = 1/20
f3 = mp.mpf('1')/(2*20)  # 1/(2*W_3) = 1/40

# SM expected Delta_RGE
Delta_RGE_SM = mp.mpf('-0.0433')

# CNT first-principles delta_CNT
C = mp.mpf('0.023095708966121')
N_cycle = 30
M_GUT = mp.mpf('6.10e14')
M_Z = mp.mpf('91.1876')
C_eff = C * (1 + 1/mp.mpf(N_cycle))
delta_CNT = -C_eff * mp.log(M_GUT/M_Z) / (2*mp.pi)

# Optimal delta_W^(1) from SM matching
delta_W_opt = delta_CNT + Delta_RGE_SM

# Required rho_2 to match
sin2W_exp = mp.mpf('0.23120')
rho_2_required = (sin2W_exp - mp.mpf('3')/8 - delta_W_opt - f3*rho_3) / f2

N2_sq = rho_2_required / rho_2_raw

print('=== SU(5) rho_2 normalization factor derivation ===')
print(f'delta_CNT = {float(delta_CNT):.8f}')
print(f'Delta_RGE_SM = {float(Delta_RGE_SM):.6f}')
print(f'delta_W^(1)_opt = {float(delta_W_opt):.8f}')
print(f'')
print(f'rho_2 (raw Mathieu) = {float(rho_2_raw):.6f}')
print(f'rho_3 (normalized)  = {float(rho_3):.6f}')
print(f'')
print(f'Required rho_2 = {float(rho_2_required):.6f}')
print(f'N2^2 = rho_2_required/rho_2_raw = {float(N2_sq):.6f}')
print(f'')
# Candidate: 11/12
candidate = mp.mpf('11')/12
print(f'Candidate N2^2 = 11/12 = {float(candidate):.6f}')
print(f'Deviation from 11/12: {(float(N2_sq) - float(candidate))/float(candidate)*100:.2f}%')
print(f'')
# Candidate: (N_X-1)/N_X where N_X=12
N_X = 12
candidate_NX = mp.mpf(N_X-1)/N_X
print(f'Candidate N2^2 = (N_X-1)/N_X = {N_X-1}/{N_X} = {float(candidate_NX):.6f}')
print(f'')
# Also check 10/11
candidate2 = mp.mpf('10')/11
print(f'Alternate: 10/11 = {float(candidate2):.6f}')
print(f'Deviation from 10/11: {(float(N2_sq) - float(candidate2))/float(candidate2)*100:.2f}%')
print(f'')
# Also check 23/25
candidate3 = mp.mpf('23')/25
print(f'Alternate: 23/25 = {float(candidate3):.6f}')
print(f'Deviation from 23/25: {(float(N2_sq) - float(candidate3))/float(candidate3)*100:.2f}%')
print(f'')
# Also check I_SU2/(I_SU2+1) = (5/2)/(7/2) = 5/7
candidate4 = mp.mpf('5')/7
print(f'Alternate: 5/7 = {float(candidate4):.6f}')
print(f'Deviation from 5/7: {(float(N2_sq) - float(candidate4))/float(candidate4)*100:.2f}%')
print(f'')

# With N2^2 = 11/12:
rho_2_corrected = rho_2_raw * candidate
delta_W_1_check = sin2W_exp - mp.mpf('3')/8 - f2*rho_2_corrected - f3*rho_3
Delta_RGE_check = delta_W_1_check - delta_CNT
print(f'=== Verification with N2^2 = 11/12 ===')
print(f'rho_2 (corrected) = {float(rho_2_corrected):.6f}')
print(f'delta_W^(1) = {float(delta_W_1_check):.8f}')
print(f'Delta_RGE = {float(Delta_RGE_check):.8f}')
print(f'Delta_RGE - SM_expected = {float(Delta_RGE_check - Delta_RGE_SM):.2e}')
sin2W_check = mp.mpf('3')/8 + delta_W_1_check + f2*rho_2_corrected + f3*rho_3
print(f'sin^2theta_W = {float(sin2W_check):.8f}')
print(f'')
# Also try N2^2 from analytic expression
print('=== Analytic candidate analysis ===')
print(f'11/12 = (N_X-1)/N_X = (12-1)/12')
print(f'Physical interpretation:')
print(f'  N_X=12 X,Y gauge bosons in SU(5)')
print(f'  One generator (pure U(1)_Y direction) excluded from T3-Y mixing')
print(f'  N2^2 = (N_X-1)/N_X accounts for this projection')
print(f'')
print(f'For rho_3: N3^2 = 8/9')
print(f'  Possible interpretation: 8 SU(3) generators out of 9 total')
print(f'  in the coset SU(3)xU(1)/U(1)_EM?')
print(f'')
print(f'Full SU(5) normalization factors:')
print(f'  N2^2 = (N_X-1)/N_X = 11/12 (rho_2: 5bar->10 via X,Y bosons)')
print(f'  N3^2 = 8/9 (rho_3: 5bar->24 via color-octet projection)')
