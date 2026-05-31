(* 复合闭合核整体旋转分析 *)
(* 正确物理图像：N个闭合核复合后作为一个整体旋转 *)

phiGR = (1 + Sqrt[5])/2;
alphaExp = 1/137.036;

Print["=== 基本参数 ==="];
Print["实验值：1/alpha = ", N[1/alphaExp]];
Print["单个闭合核（无旋转）：1/alpha0 = ", N[16384*Pi/375]];

(* 正确模型：N个闭合核复合，整体旋转 *)
(* 总角动量：J_total = N * hbar/2（假设同向排列） *)
(* 旋转修正与总角动量有关 *)

Print["\n=== 模型A：旋转修正与总角动量成正比 ==="];
Print["假设 delta = k * J_total / hbar = k * N/2"];

(* 对N=2，最佳delta已知为 1/phi = 0.618 *)
(* 因此 k/2 * 2 = k = 1/phi *)
(* 即 k = 1/phi *)

k = 1/phiGR;
Print["从N=2定标：k = 1/phi = ", N[k]];

Print["\n预测结果："];
For[n = 1, n <= 5, n++,
  delta = k * n/2;
  s2 = (375 + delta)/4096;
  ia = 4*Pi/s2;
  Print["N = ", n, ", J_total = ", n, "/2 hbar, delta = ", N[delta], 
        ", 1/alpha = ", N[ia], ", 偏差 = ", N[ia - 137.036]];
];

(* 模型B：旋转修正与角速度有关 *)
(* omega = J / (M * R^2) *)
(* 假设质量 M 正比于 N，有效半径 R_eff ~ N^(1/3) *)
(* omega ~ N / (N * N^(2/3)) = N^(-2/3) *)

Print["\n=== 模型B：旋转修正与角速度有关 ==="];
Print["假设 delta = k_omega * omega ~ k_omega * N^(-2/3)"];

(* 对N=2，delta = 1/phi *)
kOmega = (1/phiGR) / (2^(-2/3));
Print["从N=2定标：k_omega = ", N[kOmega]];

Print["\n预测结果："];
For[n = 1, n <= 5, n++,
  delta = kOmega * n^(-2/3);
  s2 = (375 + delta)/4096;
  ia = 4*Pi/s2;
  Print["N = ", n, ", omega ~ ", N[n^(-2/3)], ", delta = ", N[delta], 
        ", 1/alpha = ", N[ia], ", 偏差 = ", N[ia - 137.036]];
];

(* 模型C：旋转修正来自Kerr度规的参考系拖拽 *)
(* 在Kerr度规中，参考系拖拽角速度 Omega = 2aMr/((r^2+a^2)^2 - a^2 Delta sin^2 theta) *)
(* 对于极端情况 a ~ M，Omega ~ 1/(2M) *)
(* 如果 M ~ N，则 Omega ~ 1/N *)
(* 修正 delta ~ Omega * t ~ 1/N *)

Print["\n=== 模型C：Kerr参考系拖拽 ==="];
Print["假设 delta = k_kerr * 1/N（Omega ~ 1/M ~ 1/N）"];

kKerr = (1/phiGR) * 2;
Print["从N=2定标：k_kerr = ", N[kKerr]];

Print["\n预测结果："];
For[n = 1, n <= 5, n++,
  delta = kKerr / n;
  s2 = (375 + delta)/4096;
  ia = 4*Pi/s2;
  Print["N = ", n, ", Omega ~ 1/N, delta = ", N[delta], 
        ", 1/alpha = ", N[ia], ", 偏差 = ", N[ia - 137.036]];
];

(* 模型D：旋转修正与总角动量和质量比有关 *)
(* delta = k * J / Mc *)
(* 对于N个闭合核：J = N*hbar/2, M = N*m_1 *)
(* J/M = hbar/(2*m_1)，与N无关！ *)
Print["\n=== 模型D：delta ~ J/M（与N无关） ==="];
Print["J = N*hbar/2, M = N*m_1"];
Print["J/M = hbar/(2*m_1)，与N无关"];
Print["但如果质量不是线性增长..."];

(* 如果质量增长与体积有关：M ~ R^3 ~ N（假设紧密堆积） *)
(* 或者 M ~ N^alpha，其中 alpha != 1 *)
(* 尝试 M ~ N^alpha 对不同的alpha *)

Print["\n尝试不同的 M ~ N^alpha："];
alphas = {1/2, 2/3, 1, 4/3, 3/2};
For[i = 1, i <= Length[alphas], i++,
  a = alphas[[i]];
  Print["\nalpha = ", a, ":"];
  (* J/M ~ N*hbar / N^alpha = N^(1-alpha) *)
  (* 对N=2，delta = 1/phi *)
  kJM = (1/phiGR) / (2^(1-a));
  For[n = 1, n <= 5, n++,
    delta = kJM * n^(1-a);
    s2 = (375 + delta)/4096;
    ia = 4*Pi/s2;
    Print["  N = ", n, ", delta = ", N[delta], 
          ", 1/alpha = ", N[ia], ", 偏差 = ", N[ia - 137.036]];
  ];
];
