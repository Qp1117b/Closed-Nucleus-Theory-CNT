(* 验证汇总文档中的所有关键数值 *)
alphaExp = 1/137.036;
phi = (1 + Sqrt[5])/2;
theta = ArcCos[1/4];
eps0 = 2*Pi - 3*theta;

Print["=== 1. 基本几何常数 ==="];
Print["Theta = ", N[theta], " rad = ", N[theta*180/Pi], " 度"];
Print["sin^2(5*Theta) = 375/4096 = ", N[375/4096]];
Print["cos(5*Theta) = 61/64 = ", N[61/64]];

Print["\n=== 2. 裸精细结构常数 ==="];
Print["1/alpha0 = 16384*Pi/375 = ", N[16384*Pi/375]];
Print["alpha0 = ", N[375/(16384*Pi)]];
Print["与实验（137.036）偏差 = ", N[16384*Pi/375 - 137.036]];

Print["\n=== 3. 旋转修正后的精细结构常数 ==="];
(* 修正项 delta = 1/phi *)
delta = 1/phi;
Print["delta = 1/phi = ", N[delta]];
Print["375 + 1/phi = ", N[375 + delta]];
Print["sin^2_eff = (375+1/phi)/4096 = ", N[(375 + delta)/4096]];
invAlpha = 4*Pi/((375 + delta)/4096);
Print["1/alpha = ", N[invAlpha]];
Print["偏差 = ", N[invAlpha - 137.036]];
Print["相对偏差 = ", N[(invAlpha - 137.036)/137.036 * 100], " %"];
Print["精度提升：裸值偏差 ", N[16384*Pi/375 - 137.036], " -> 修正后偏差 ", N[invAlpha - 137.036]];

Print["\n=== 4. 简化形式验证 ==="];
Print["8*Pi*4096/(749 + Sqrt[5]) = ", N[8*Pi*4096/(749 + Sqrt[5])]];
Print["与 4*Pi*4096/(375 + 1/phi) 一致？", N[8*Pi*4096/(749 + Sqrt[5]) == invAlpha]];

Print["\n=== 5. 黄金比例三角恒等式 ==="];
Print["sin(Pi/10) = ", N[Sin[Pi/10]]];
Print["cos(2*Pi/5) = ", N[Cos[2*Pi/5]]];
Print["1/(2*phi) = ", N[1/(2*phi)]];
Print["sin(Pi/10) = 1/(2*phi) ? ", Sin[Pi/10] == 1/(2*phi)];
Print["(sqrt(5)-1)/4 = ", N[(Sqrt[5]-1)/4]];

Print["\n=== 6. 稳态质量公式验证 ==="];
mFinalFormula = "3*Sqrt[3]*Pi*Log[2]/8 * c*nu*ell0^2/G";
Print["m_final = ", mFinalFormula];

(* 数值估计 *)
c = 3*10^8;
nu = 10^23;
ell0 = 10^(-35);
G = 6.67*10^(-11);
mFinal = (3*Sqrt[3]*Pi*Log[2]/8) * c * nu * ell0^2 / G;
Print["m_final ~ ", ScientificForm[mFinal], " kg"];
Print["电子质量 me = ", 9.109*10^(-31), " kg"];
Print["m_final/me = ", N[mFinal/9.109*10^(-31)]];

Print["\n=== 7. 所有N的对比 ==="];
For[n = 1, n <= 5, n++,
  jh = Switch[n, 1, 1/2, 2, 1, 3, 1/2, 4, 0, 5, 1/2];
  deltaN = jh/phi;
  invAlphaN = 4*Pi*4096/(375 + deltaN);
  dev = invAlphaN - 137.036;
  Print["N=", n, ", J/hbar=", jh, ", 1/alpha=", N[invAlphaN], ", 偏差=", N[dev]];
];
