(* 基本常数 *)
alphaExp = 1/137.036;
theta = ArcCos[1/4];
phi = 5*theta;
sin2phi = Sin[phi]^2;
alpha0 = sin2phi/(4*Pi);

(* 输出基本值 *)
Print["二面角 Theta = ", N[theta]];
Print["EPRL相位 phi = ", N[phi]];
Print["sin^2(phi) = ", N[sin2phi]];
Print["裸精细结构常数 alpha0 = ", N[alpha0]];
Print["1/alpha0 = ", N[1/alpha0]];
Print["实验值 1/alpha = ", N[1/alphaExp]];
Print["偏差 = ", N[(1/alpha0 - 1/alphaExp)]];

(* 计算Chebyshev多项式验证 *)
cosPhi = ChebyshevT[5, 1/4];
Print["cos(phi) = T_5(1/4) = ", N[cosPhi]];
Print["sin^2(phi) = 1 - cos^2(phi) = ", N[1 - cosPhi^2]];

(* 精确分数形式 *)
Print["sin^2(phi) 精确值 = ", sin2phi];
Print["1/alpha0 精确值 = ", 1/alpha0];
