(* 精细结构常数的严格推导尝试 *)

(* 基本参数 *)
theta = ArcCos[1/4];
phi0 = 5*theta;
alpha0 = Sin[phi0]^2/(4*Pi);
alphaExp = 1/137.036;

Print["=== 现有结果 ==="];
Print["1/alpha0 = ", N[1/alpha0]];
Print["1/alpha_exp = ", N[1/alphaExp]];
Print["偏差 = ", N[1/alpha0 - 1/alphaExp]];

(* 关键观察：375/4096 = sin^2(phi) *)
(* 1/alpha0 = 4*Pi / (375/4096) = 16384*Pi/375 *)

Print["\n=== 精确分数形式 ==="];
Print["sin^2(phi) = 375/4096 = ", N[375/4096]];
Print["1/alpha0 = 16384*Pi/375 = ", N[16384*Pi/375]];

(* 尝试：如果分母不是375，而是375 + delta？ *)
(* 1/alpha_exp ≈ 137.036 *)
(* 我们希望 4*Pi/sin^2(phi_eff) = 137.036 *)
(* 即 sin^2(phi_eff) = 4*Pi/137.036 = 0.091895... *)

targetSin2 = 4*Pi/137.036;
Print["\n=== 目标值分析 ==="];
Print["实验值对应的 sin^2 = ", N[targetSin2]];
Print["理论值 sin^2 = ", N[375/4096]];
Print["差值 = ", N[targetSin2 - 375/4096]];

(* 检查375和4096的数论性质 *)
Print["\n=== 数论分析 ==="];
Print["375 = ", FactorInteger[375]];
Print["4096 = ", FactorInteger[4096]];
Print["375/4096 = ", 375/4096];

(* 尝试：如果sin^2(phi) = 375/(4096 + delta) *)
(* 解方程：4*Pi*4096/(375*(1 + delta/4096)) = 137.036 *)

deltaDenom = Solve[4*Pi*(4096 + x)/375 == 137.036, x][[1,1,2]];
Print["\n如果 sin^2 = 375/(4096 + delta)："];
Print["delta = ", N[deltaDenom]];

(* 尝试：如果sin^2(phi) = (375 + delta)/4096 *)
deltaNum = Solve[4*Pi*4096/(375 + x) == 137.036, x][[1,1,2]];
Print["\n如果 sin^2 = (375 + delta)/4096："];
Print["delta = ", N[deltaNum]];

(* 检查delta是否与某个物理量有关 *)
Print["\n=== delta的物理意义 ==="];
Print["deltaNum / 375 = ", N[deltaNum/375]];
Print["deltaNum * 4 = ", N[deltaNum*4]];
Print["deltaNum / (1/4) = ", N[deltaNum*4]];

(* 尝试：delta = 1/4？ *)
Print["\n=== 尝试 delta = 1/4 ==="];
alpha_test1 = (375 + 1/4)/(4096*4*Pi);
Print["如果 sin^2 = (375 + 1/4)/4096：1/alpha = ", N[1/alpha_test1]];

(* 尝试：delta = 1/5？ *)
Print["\n=== 尝试 delta = 1/5 ==="];
alpha_test2 = (375 + 1/5)/(4096*4*Pi);
Print["如果 sin^2 = (375 + 1/5)/4096：1/alpha = ", N[1/alpha_test2]];

(* 尝试：delta = 1/6？ *)
Print["\n=== 尝试 delta = 1/6 ==="];
alpha_test3 = (375 + 1/6)/(4096*4*Pi);
Print["如果 sin^2 = (375 + 1/6)/4096：1/alpha = ", N[1/alpha_test3]];

(* 精确求解：找到使1/alpha = 137.036的分子 *)
exactNum = 4096*4*Pi/137.036;
Print["\n=== 精确解 ==="];
Print["需要的分子 = ", N[exactNum]];
Print["375 + delta = ", N[exactNum]];
Print["delta = ", N[exactNum - 375]];

(* 检查delta是否接近某个简单分数 *)
deltaExact = exactNum - 375;
Print["\ndelta的近似分数："];
Print["delta ≈ 1/", N[1/deltaExact]];
Print["delta ≈ 1/4 = ", N[1/4]];
Print["delta ≈ 1/5 = ", N[1/5]];
Print["delta ≈ 1/6 = ", N[1/6]];
Print["delta ≈ 1/7 = ", N[1/7]];
Print["delta ≈ 1/8 = ", N[1/8]];

(* 关键尝试：delta = 1/4.5？ *)
Print["\n=== 关键尝试 ==="];
For[i = 1, i <= 20, i++,
  testAlpha = (375 + 1/i)/(4096*4*Pi);
  Print["delta = 1/", i, ": 1/alpha = ", N[1/testAlpha], ", 偏差 = ", N[1/testAlpha - 137.036]]
];
