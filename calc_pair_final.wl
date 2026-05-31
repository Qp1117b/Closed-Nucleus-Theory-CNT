(* 双闭合核（对形成）的精细分析 - 最终版 *)

phiGR = (1 + Sqrt[5])/2;
alphaExp = 1/137.036;

Print["=== 实验值 ==="];
Print["1/alpha_exp = ", N[1/alphaExp]];

(* 尝试不同的双核修正形式 *)
Print["\n=== 双核修正的多种形式 ==="];

(* 形式A：delta = 1/(2*phi) *)
dA = 1/(2*phiGR);
s2A = (375 + dA)/4096;
iaA = 4*Pi/s2A;
Print["形式A：delta = 1/(2*phi) = ", N[dA]];
Print["  1/alpha = ", N[iaA], ", 偏差 = ", N[iaA - 137.036]];

(* 形式B：delta = log(2)/phi *)
dB = Log[2]/phiGR;
s2B = (375 + dB)/4096;
iaB = 4*Pi/s2B;
Print["\n形式B：delta = log(2)/phi = ", N[dB]];
Print["  1/alpha = ", N[iaB], ", 偏差 = ", N[iaB - 137.036]];

(* 形式C：delta = 1/phi *)
dC = 1/phiGR;
s2C = (375 + dC)/4096;
iaC = 4*Pi/s2C;
Print["\n形式C：delta = 1/phi = ", N[dC]];
Print["  1/alpha = ", N[iaC], ", 偏差 = ", N[iaC - 137.036]];

(* 形式D：delta = sin(Pi/10) *)
dD = Sin[Pi/10];
s2D = (375 + dD)/4096;
iaD = 4*Pi/s2D;
Print["\n形式D：delta = sin(Pi/10) = ", N[dD]];
Print["  1/alpha = ", N[iaD], ", 偏差 = ", N[iaD - 137.036]];

(* 形式E：delta = 2/phi *)
dE = 2/phiGR;
s2E = (375 + dE)/4096;
iaE = 4*Pi/s2E;
Print["\n形式E：delta = 2/phi = ", N[dE]];
Print["  1/alpha = ", N[iaE], ", 偏差 = ", N[iaE - 137.036]];

(* 验证三角恒等式 *)
Print["\n=== 三角恒等式验证 ==="];
Print["sin(Pi/10) = ", N[Sin[Pi/10]]];
Print["cos(2*Pi/5) = ", N[Cos[2*Pi/5]]];
Print["(phi-1)/2 = ", N[(phiGR-1)/2]];
Print["1/(2*phi) = ", N[1/(2*phiGR)]];
Print["sin(Pi/10) == cos(2*Pi/5) ? ", Sin[Pi/10] == Cos[2*Pi/5]];
Print["sin(Pi/10) == (phi-1)/2 ? ", Sin[Pi/10] == (phiGR-1)/2];

(* 最终结论 *)
Print["\n=== 结论 ==="];
Print["对于双闭合核系统（N=2）："];
Print["最佳修正：delta = 1/phi = ", N[1/phiGR]];
Print["给出：1/alpha = ", N[iaC]];
Print["与实验值137.036的偏差：", N[iaC - 137.036]];

(* 纠缠熵分析 *)
Print["\n纠缠熵分析："];
Print["N=2时，S_E = log_2(2) = 1"];
Print["delta = S_E/phi = 1/phi = ", N[1/phiGR]];
Print["这与最佳修正一致！"];

(* 最终表达式 *)
Print["\n=== 最终表达式 ==="];
Print["1/alpha = 4*Pi*4096 / (375 + 1/phi)"];
Print["其中 phi = (1+Sqrt[5])/2 是黄金比例"];
Print["数值结果：1/alpha = ", N[iaC]];
Print["实验值：1/alpha = ", N[1/alphaExp]];
Print["偏差 = ", N[iaC - 1/alphaExp]];

(* 简化形式 *)
Print["\n=== 简化形式 ==="];
Print["375 + 1/phi = 375 + 2/(1+Sqrt[5])"];
Print["= 375 + (Sqrt[5]-1)/2"];
Print["= (750 + Sqrt[5] - 1)/2"];
Print["= (749 + Sqrt[5])/2"];
simplifiedNum = (749 + Sqrt[5])/2;
Print["= ", N[simplifiedNum]];

iaSimplified = 8*Pi*4096/(749 + Sqrt[5]);
Print["\n1/alpha = 8*Pi*4096 / (749 + Sqrt[5])"];
Print["= ", N[iaSimplified]];
