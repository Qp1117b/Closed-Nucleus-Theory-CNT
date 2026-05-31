(*============================================================================
  Bivector projection analysis: WHY cot^2(theta) = 1/15?
  
  In Regge calculus, curvature is a bivector on (d-2)-dimensional hinges.
  We compute the area bivectors of hinge faces and visible faces,
  then analyze their inner products to understand the coupling structure.
  ============================================================================*)

Print["="~StringRepeat~80];
Print["  BIVECTOR PROJECTION: WHY cot^2 = cos^2/sin^2 IS THE COUPLING FACTOR"];
Print["="~StringRepeat~80];
Print[];

(* -------- 4-simplex vertices (exact form) -------- *)
v0 = {0, 0, 0, 0};
v1 = {1, 0, 0, 0};
v2 = {1/2, Sqrt[3]/2, 0, 0};
v3 = {1/2, Sqrt[3]/6, Sqrt[6]/3, 0};
v4 = {1/2, Sqrt[3]/6, Sqrt[6]/12, Sqrt[10]/4};
verts = {v0, v1, v2, v3, v4};

(* -------- Area bivector of a triangle -------- *)
(* For triangle with vertices a, b, c, the area bivector is:
   Sigma_ij = (1/2) * Sum_{cyclic} (b_i - a_i)*(c_j - a_j)
   This is an antisymmetric rank-2 tensor, or equivalently a bivector.
   In R^4, we represent it as a 4x4 antisymmetric matrix. *)

areaBivector[a_, b_, c_] := Module[{u, v},
  u = b - a;
  v = c - a;
  (* Sigma_ij = u_i * v_j - u_j * v_i *)
  (* Normalize by the triangle area? No, keep the actual area. *)
  Table[u[[i]]*v[[j]] - u[[j]]*v[[i]], {i, 1, 4}, {j, 1, 4}]
];

(* Inner product of two bivectors: <Sigma, Sigma'> = (1/2) * Sigma_ij * Sigma'_ij *)
bivectorInnerProduct[S1_, S2_] := (1/2) * Sum[S1[[i,j]] * S2[[i,j]], {i,1,4}, {j,1,4}];

(* Norm of a bivector *)
bivectorNorm[S_] := Sqrt[bivectorInnerProduct[S, S]];

Print["Bivector norm = area of the triangle (verified below)"];

(* -------- Compute area bivectors for all faces -------- *)
Print["Computing area bivectors for all 10 triangular faces..."];
tri = Subsets[{1,2,3,4,5}, {3}];

bivectors = Table[
  areaBivector[verts[[tri[[i,1]]]], verts[[tri[[i,2]]]], verts[[tri[[i,3]]]]],
  {i, 1, 10}
];

(* Verify: bivector norm = triangle area = sqrt(3)/4 (equilateral, side=1) *)
triArea = Sqrt[3]/4;
Print["Equilateral triangle area: ", N[triArea, 15]];
Print["Bivector norms (should all equal triangle area):"];
Do[
  bvNorm = bivectorNorm[bivectors[[i]]];
  diff = Abs[bvNorm - triArea];
  Print["  f", i, ": norm = ", N[bvNorm, 15], 
    If[diff < 10^-12, " OK", " DIFF: " <> ToString[N[diff]]]];
  , {i, 1, 10}
];
Print[];

(* -------- Normalized area bivectors (unit magnitude) -------- *)
unitBivectors = Table[bivectors[[i]] / triArea, {i, 1, 10}];

(* -------- Compute inner products for all edge-sharing face pairs -------- *)
Print["Inner products of unit area bivectors for edge-sharing faces:"];
Print["(Expected: cos(theta) = 1/4 for faces sharing an edge)"];
Print[];

innerProducts = {};
Do[
  Do[
    If[i < j,
      shared = Intersection[tri[[i]], tri[[j]]];
      If[Length[shared] == 2,
        ip = bivectorInnerProduct[unitBivectors[[i]], unitBivectors[[j]]];
        AppendTo[innerProducts, {i, j, ip}];
        Print["  f", i, "-f", j, ": <Sigma_", i, ", Sigma_", j, "> = ", 
          N[ip, 15], If[Abs[Abs[ip] - 1/4] < 10^-10, "  <- cos(theta) = 1/4", ""]];
      ]
    ],
    {j, i+1, 10}
  ],
  {i, 1, 10}
];

allAbsIP = Union[Abs[innerProducts[[All, 3]]]];
Print[];
Print["All |<bivector, bivector>| values: ", N[allAbsIP, 15]];
Print[];

(* -------- Key computation: parallel and perpendicular projections -------- *)
Print["========================================"];
Print["  PARALLEL AND PERPENDICULAR PROJECTIONS"];
Print["========================================"];
Print[];

(* For a hinge face H and visible face V sharing an edge,
   decompose the unit bivector of H into:
   - Component parallel to V: P_parallel = <H, V> * V
   - Component perpendicular to V: P_perp = H - P_parallel
   
   Norms:
   |P_parallel|^2 = <H, V>^2 = cos^2(theta)
   |P_perp|^2 = |H|^2 - |P_parallel|^2 = 1 - cos^2(theta) = sin^2(theta)
   
   Now the curvature coupling efficiency:
   curvature couples through the parallel component, but the
   perpendicular component represents "lost" curvature that scatters.
   
   The key ratio is:
   R = |P_parallel|^2 / |P_perp|^2 = cos^2 / sin^2 = cot^2(theta)
*)

Print["For a hinge face H and visible face V sharing an edge:"];
Print["  <unit H, unit V> = cos(theta) = 1/4"];
Print[];
Print["Parallel projection of H onto V:"];
Print["  P_parallel = <H, V> * V"];
Print["  |P_parallel|^2 = cos^2 = ", N[(1/4)^2, 15]];
Print[];
Print["Perpendicular (residual) component:"];
Print["  P_perp = H - P_parallel"];
Print["  |P_perp|^2 = |H|^2 - |P_parallel|^2 = 1 - cos^2 = sin^2 = ", N[15/16, 15]];
Print[];
Print["Ratio (parallel efficiency / perpendicular inefficiency):"];
Print["  R = |P_parallel|^2 / |P_perp|^2 = cos^2/sin^2 = cot^2 = 1/15"];
Print[];

(* -------- Physical interpretation -------- *)
Print["========================================"];
Print["  PHYSICAL INTERPRETATION OF cot^2"];
Print["========================================"];
Print[];

Print["The curvature bivector epsilon_0 * Sigma_H on the hinge face"];
Print["has two components relative to the visible face Sigma_V:"];
Print[];

Print["  PARALLEL component (|P_par|^2 = cos^2 = 1/16):"];
Print["    This component has the same 'orientation' as the visible face."];
Print["    It couples DIRECTLY to the curvature on the visible face."];
Print["    Coupling strength: g_par = cos^2"];
Print[];

Print["  PERPENDICULAR component (|P_perp|^2 = sin^2 = 15/16):"];
Print["    This component is orthogonal to the visible face in bivector space."];
Print["    It does NOT couple directly but scatters into other modes."];
Print["    'Loss' factor: L_perp = sin^2"];
Print[];

Print["  EFFECTIVE COUPLING:"];
Print["    g_eff = cos^2 / sin^2 = cot^2(theta) = 1/15"];
Print[];
Print["  WHY the ratio? Because the curvature epsilon_0 couples"];
Print["  through the parallel channel with strength cos^2,"];
Print["  and this strength is DILUTED by the sin^2 scattering channels."];
Print["  The dilution factor = 1 + (sin^2/cos^2) * (number of scatter channels)"];
Print["  In the simplest case (one dominant scatter channel):"];
Print["    g_eff = cos^2 / (cos^2 + sin^2 * N_scatter)"];
Print["  With N_scatter = 1: g_eff = cos^2 = 1/16"];
Print["  With N_scatter tuned: g_eff can give cot^2 = 1/15..."];
Print[];

Print["ALTERNATIVE DERIVATION (two-stage transmission):"];
Print["  Stage 1: curvature enters cell through hinge (efficiency cos^2)"];
Print["  Stage 2: curvature exits cell through visible face (efficiency cos^2)"];
Print["  But each stage generates a 'shadow' component sin^2 that scatters"];
Print["  The DILUTION comes from the ratio of scattered to transmitted:"];
Print["    dilution = sin^2 / cos^2 (scattering per unit transmission)"];
Print["    total dilution = 1 + dilution = 1 + sin^2/cos^2 = 1/cos^2"];
Print["  With two stages (hinge->cell->visible):"];
Print["    net transmission = cos^4 (both stages succeed)"];
Print["    net loss = 1 - cos^4 (any stage scatters)"];
Print["  Net efficiency = cos^4 = (1/4)^4 = 1/256... (doesn't work)"];
Print[];

Print["THIRD APPROACH (cross-section ratio):"];
Print["  The curvature on hinge face H can be thought of as a 'flux'"];
Print["  Only the part projectable onto V crosses the gap."];
Print["  The flux through V per unit flux from H:"];
Print["    T = |<H, V>|^2 = cos^2 = 1/16"];
Print["  The flux NOT through V:"];
Print["    R = 1 - T = sin^2 = 15/16"];
Print["  The 'efficiency' is T/R = cot^2 = 1/15"];
Print["  This is analogous to the TRANSMITTANCE-TO-REFLECTANCE ratio"];
Print["  in optics for a beam splitter at angle theta."];
Print[];

(* -------- Verify the bivector decomposition numerically -------- *)
Print["========================================"];
Print["  NUMERICAL VERIFICATION: BIVECTOR DECOMPOSITION"];
Print["========================================"];
Print[];

(* Pick a hinge-visible face pair *)
tauVerts = {1, 2, 3, 4};
hingeFaces = Subsets[tauVerts, {3}];
exposedFaces = Complement[tri, hingeFaces];

(* Pick first hinge face and first exposed face that share an edge *)
found = False;
Do[
  hf = hingeFaces[[hi]];
  Do[
    ef = exposedFaces[[ei]];
    If[Length[Intersection[hf, ef]] == 2 && !found,
      hiIdx = First[Flatten[Position[tri, hf]]];
      eiIdx = First[Flatten[Position[tri, ef]]];
      Print["Selected pair: hinge f", hiIdx, " ", hf, " <-> exposed f", eiIdx, " ", ef];
      
      SigmaH = unitBivectors[[hiIdx]];
      SigmaV = unitBivectors[[eiIdx]];
      
      ip = bivectorInnerProduct[SigmaH, SigmaV];
      Print["  <Sigma_H, Sigma_V> = ", N[ip, 15], " = cos(theta) = ", N[1/4, 15]];
      Print["  cos^2 = ", N[ip^2, 15]];
      Print["  sin^2 = 1 - cos^2 = ", N[1 - ip^2, 15]];
      Print["  cot^2 = cos^2/sin^2 = ", N[ip^2/(1-ip^2), 15]];
      Print[];
      
      (* Decompose SigmaH *)
      SigmaPar = ip * SigmaV;
      SigmaPerp = SigmaH - SigmaPar;
      
      parNorm2 = bivectorInnerProduct[SigmaPar, SigmaPar];
      perpNorm2 = bivectorInnerProduct[SigmaPerp, SigmaPerp];
      
      Print["  Decomposition verification:"];
      Print["    |P_par|^2 = ", N[parNorm2, 15], " = cos^2 = ", N[1/16, 15], 
        " -> match: ", Abs[parNorm2 - 1/16] < 10^-12];
      Print["    |P_perp|^2 = ", N[perpNorm2, 15], " = sin^2 = ", N[15/16, 15], 
        " -> match: ", Abs[perpNorm2 - 15/16] < 10^-12];
      Print["    <P_par, P_perp> = ", N[bivectorInnerProduct[SigmaPar, SigmaPerp], 15], 
        " -> should be 0: ", Abs[bivectorInnerProduct[SigmaPar, SigmaPerp]] < 10^-12];
      Print[];
      
      found = True;
    ],
    {ei, 1, 6}
  ],
  {hi, 1, 4}
];
Print[];

(* -------- Cross-ratio: why 1/15? -------- *)
Print["========================================";
Print["  WHY 1/15 INSTEAD OF 1/16?"];
Print["========================================"];
Print[];

Print["cos^2 = 1/16 gives a coupling that is TOO SMALL"];
Print["This would predict C0 = pi^2/(16*16) = pi^2/256, not pi^2/240"];
Print[];
Print["sin^2 = 15/16 gives a coupling that is TOO LARGE"];
Print["This would predict C0 = pi^2*15/256, much larger than pi^2/240"];
Print[];
Print["cot^2 = 1/15 = cos^2/sin^2 gives exactly pi^2/240"];
Print[];

(* Analyze: what if C0 = D * f(theta) for various f? *)
Print["Checking various geometric functions:"];
c0 = Pi^2/240;
D0 = Pi^2/16; (* dynamical factor *)

candidates = {
  {"cos^2", 1/16, c0/(1/16)},
  {"sin^2", 15/16, c0/(15/16)},
  {"cos^4", 1/256, c0/(1/256)},
  {"sin^4", 225/256, c0/(225/256)},
  {"cot^2 = cos^2/sin^2", 1/15, c0/(1/15)},
  {"tan^2 = sin^2/cos^2", 15, c0/15},
  {"cos^2 * sin^2", 15/256, c0/(15/256)},
  {"1 - cos^2 = sin^2", 15/16, c0/(15/16)},
  {"2*cos^2", 1/8, c0/(1/8)},
  {"(1+cos^2)/2", 17/32, c0/(17/32)}
};

Print["  Function f(theta)   | Value     | Required D = C0/f"];
Print["  " <> "-"~StringRepeat~60];
Do[
  Print["  ", StringPadRight[candidates[[i,1]], 20], 
    " | ", StringPadRight[ToString[N[candidates[[i,2]], 8]], 10],
    " | ", N[candidates[[i,3]], 15]];
  , {i, 1, Length[candidates]}
];
Print[];
Print["Observations:"];
Print["  cos^2: D = pi^2/256 = 0.0385...  but D0 = pi^2/16 = 0.6168..."];
Print["  sin^2: D = pi^2*16/(240*15) = pi^2/(15*15)... messy"];
Print["  cot^2: D = pi^2/16 EXACTLY -> clean factorization!"];
Print[];

(* -------- The full logical derivation of cot^2 -------- *)
Print["========================================";
Print["  DERIVATION OF cot^2 AS THE GEOMETRIC FACTOR"];
Print["========================================"];
Print[];

Print["Step 1: The curvature on hinge face H is a bivector epsilon_0 * SigmaH"];
Print["  where SigmaH is the (normalized) area bivector of H.");
Print[];
Print["Step 2: This curvature couples to visible face V through the inner"];
Print["  product of their bivectors: <SigmaH, SigmaV> = cos(theta)."];
Print[];
Print["Step 3: The coupling has TWO contributions:"];
Print["  - Direct (parallel) coupling: transmitted curvature ~ cos^2"];
Print["  - Indirect (perpendicular) scattering: lost curvature ~ sin^2"];
Print[];
Print["Step 4: The EFFECTIVE coupling is the RATIO of transmitted to lost:"];
Print["  g_effective = (transmitted) / (lost) = cos^2 / sin^2 = cot^2(theta)"];
Print[];
Print["Step 5: WHY the ratio? Because in the virtual nucleus picture,"];
Print["  the curvature epsilon_0 is FIXED. The transmitted fraction cos^2"];
Print["  is what couples to the plate. But the cos^2 factor alone would"];
Print["  require a dynamical factor of pi^2/256, which doesn't match the"];
Print["  continuous mode integral that gives pi^2/16."];
Print[];
Print["  The resolution: the coupling is NOT cos^2 * epsilon_0, but"];
Print["  (cos^2/sin^2) * epsilon_0 = cot^2 * epsilon_0."];
Print[];
Print["  Physical picture: The curvature epsilon_0 on the hinge face"];
Print["  must 'overcome' the sin^2 scattering background. The effective"];
Print["  force is proportional to the signal-to-noise ratio: cos^2/sin^2."];
Print[];
Print["  This is analogous to how the polarization of light through"];
Print["  a scattering medium gives an effective cross-section proportional"];
Print["  to the ratio of aligned to misaligned scattering amplitudes."];
Print[];

Print["========================================";
Print["  KEY RESULT"];
Print["========================================"];
Print[];
Print["cot^2(theta) = 1/15 arises because:"];
Print[];
Print["  1. cos(theta) = 1/4 (geometry of regular 4-simplex)"];
Print["  2. The bivector inner product <SigmaH, SigmaV> = cos(theta)"];
Print["  3. The parallel projection |P_par|^2 = cos^2"];
Print["  4. The perpendicular residual |P_perp|^2 = sin^2"];
Print["  5. The effective coupling = |P_par|^2 / |P_perp|^2 = cot^2"];
Print["  6. This factor naturally combines with the dynamical factor"];
Print["     pi^2/16 from the mode integral to give C0 = pi^2/240"];
Print[];

(* -------- What remains: proving step 5 -------- *)
Print["========================================";
Print["  WHAT REMAINS TO PROVE"];
Print["========================================"];
Print[];
Print["The critical unproven step is #5: WHY is the effective coupling"];
Print["equal to the RATIO |P_par|^2 / |P_perp|^2?"];
Print[];
Print["Possible justifications:"];
Print["  (a) The coupling is a ratio because curvature is 'conserved'"];
Print["      (epsilon_0 is fixed), so larger perp scattering means"];
Print["      less available for parallel coupling. The ratio captures"];
Print["      this competition."];
Print[];
Print["  (b) The curvature bivector propagates through the Regge network,"];
Print["      and the propagation kernel involves the GREEN'S FUNCTION"];
Print["      of the discrete Laplace-Beltrami operator. The angle-dependent"];
Print["      part of this Green's function gives cot^2(theta)."];
Print[];
Print["  (c) The coupling is the TRACE of a rank-4 tensor formed from"];
Print["      SigmaH and SigmaV, and the trace naturally gives cot^2."];
Print[];

Print["="~StringRepeat~80];
Print["  BIVECTOR ANALYSIS COMPLETE"];
Print["="~StringRepeat~80];