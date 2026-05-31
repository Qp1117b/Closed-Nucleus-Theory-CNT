(* 双闭合核（对形成）的精细分析 *)

phi = (1 + Sqrt[5])/2;
alphaExp = 1/137.036;

Print["=== 实验值 ==="];
Print["1/alpha_exp = ", N[1/alphaExp]];

(* 关键发现：N=2时，delta = 1/(2*phi) 或 delta = S_E/phi (S_E=1) 给出最佳结果 *)
(* 这意味着双闭合核系统可能是最基本的物理单元 *)

(* 分析双闭合核系统的物理意义 *)
Print["\n=== 双闭合核系统的物理分析 ==="];

(* 1. 总自旋分析 *)
(* 两个自旋1/2的闭合核可以形成单态（S=0）或三重态（S=1） *)
Print["\n1. 自旋耦合："];
Print["两个j=1/2闭合核耦合："];
Print["  单态（S=0）：总自旋 = 0"];
Print["  三重态（S=1）：总自旋 = 1"];

(* 2. 纠缠熵分析 *)
Print["\n2. 纠缠熵："];
Print["对于两个闭合核的最大纠缠态："];
Print["  S_E = log(2) = ", N[Log[2]]];
Print["  S_E（以2为底）= 1"];

(* 3. 几何分析 *)
(* 两个4-单纯形复合可能形成什么结构？ *)
Print["\n3. 复合几何："];
Print["两个4-单纯形共享一个3-面（四面体）"];
Print["这种结构在5维中是最简单的复合单纯形"];

(* 4. 尝试不同的双核修正形式 *)
Print["\n=== 双核修正的多种形式 ==="];

(* 形式1：delta = 1/(2*phi) *)
delta1 = 1/(2*phi);
sin2_1 = (375 + delta1)/4096;
invAlpha1 = 4*Pi/sin2_1;
Print["形式1：delta = 1/(2*phi) = ", N[delta1]];
Print["  1/alpha = ", N[invAlpha1], ", 偏差 = ", N[invAlpha1 - 137.036]];

(* 形式2：delta = log(2)/phi *)
delta2 = Log[2]/phi;
sin2_2 = (375 + delta2)/4096;
invAlpha2 = 4*Pi/sin2_2;
Print["\n形式2：delta = log(2)/phi = ", N[delta2]];
Print["  1/alpha = ", N[invAlpha2], ", 偏差 = ", N[invAlpha2 - 137.036]];

(* 形式3：delta = 1/phi^2 *)
delta3 = 1/phi^2;
sin2_3 = (375 + delta3)/4096;
invAlpha3 = 4*Pi/sin2_3;
Print["\n形式3：delta = 1/phi^2 = ", N[delta3]];
Print["  1/alpha = ", N[invAlpha3], ", 偏差 = ", N[invAlpha3 - 137.036]];

(* 形式4：delta = (phi-1)/2 = 1/(2*phi)（与形式1相同） *)
Print["\n形式4：delta = (phi-1)/2 = ", N[(phi-1)/2]];
Print["  注意：(phi-1)/2 = 1/(2*phi) = ", N[1/(2*phi)]];

(* 形式5：delta = 1/4 - 1/(4*phi) *)
delta5 = 1/4 - 1/(4*phi);
sin2_5 = (375 + delta5)/4096;
invAlpha5 = 4*Pi/sin2_5;
Print["\n形式5：delta = 1/4 - 1/(4*phi) = ", N[delta5]];
Print["  1/alpha = ", N[invAlpha5], ", 偏差 = ", N[invAlpha5 - 137.036]];

(* 形式6：delta = sin(Pi/10) = (phi-1)/2 *)
delta6 = Sin[Pi/10];
sin2_6 = (375 + delta6)/4096;
invAlpha6 = 4*Pi/sin2_6;
Print["\n形式6：delta = sin(Pi/10) = ", N[delta6]];
Print["  1/alpha = ", N[invAlpha6], ", 偏差 = ", N[invAlpha6 - 137.036]];
Print["  注意：sin(Pi/10) = (phi-1)/2 = ", N[(phi-1)/2]];

(* 关键验证：sin(Pi/10) 与黄金比例的关系 *)
Print["\n=== 黄金比例与三角函数 ==="];
Print["sin(Pi/10) = ", N[Sin[Pi/10]]];
Print["cos(2*Pi/5) = ", N[Cos[2*Pi/5]]];
Print["(phi-1)/2 = 1/(2*phi) = ", N[(phi-1)/2]];
Print["sin(Pi/10) == (phi-1)/2 ? ", Sin[Pi/10] == (phi-1)/2];

(* 尝试：delta = cos(2*Pi/5) *)
delta7 = Cos[2*Pi/5];
sin2_7 = (375 + delta7)/4096;
invAlpha7 = 4*Pi/sin2_7;
Print["\n形式7：delta = cos(2*Pi/5) = ", N[delta7]];
Print["  1/alpha = ", N[invAlpha7], ", 偏差 = ", N[invAlpha7 - 137.036]];

(* 最终表达式 *)
Print["\n=== 最终表达式 ==="];
Print["1/alpha = 4*Pi*4096 / (375 + sin(Pi/10))"];
Print["其中 sin(Pi/10) = (sqrt(5)-1)/4 = 1/(2*phi)"];
Print["数值结果：1/alpha = ", N[4*Pi*4096/(375 + Sin[Pi/10])]];
Print["实验值：1/alpha = ", N[1/alphaExp]];
Print["偏差 = ", N[4*Pi*4096/(375 + Sin[Pi/10]) - 1/alphaExp]];

(* 检查是否可以写成更简洁的形式 *)
Print["\n=== 简化形式 ==="];
Print["375 + sin(Pi/10) = 375 + (sqrt(5)-1)/4"];
Print["= (1500 + sqrt(5) - 1)/4"];
Print["= (1499 + sqrt(5))/4"];
simplified = (1499 + Sqrt[5])/4;
Print["= ", N[simplified]];
Print["验证：375 + (sqrt(5)-1)/4 = ", N[375 + (Sqrt[5]-1)/4]];

invAlphaSimplified = 4*Pi*4096/simplified;
Print["\n1/alpha = 16*Pi*4096 / (1499 + sqrt(5))"];
Print["= ", N[invAlphaSimplified]];
