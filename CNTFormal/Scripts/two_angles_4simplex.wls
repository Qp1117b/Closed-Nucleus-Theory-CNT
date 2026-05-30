(* Verify TWO distinct angles in the regular 4-simplex:
   1. 3D hyperplane dihedral angle: cos = 1/4 (between tetrahedral cells)
   2. 2D face bivector angle: cos = 1/3 (between triangular faces sharing an edge)
   Both are geometrically fundamental. Only the 3D hyperplane angle (1/4)
   is relevant for curvature propagation -- and gives cot^2 = 1/15. *)

Print["================================================"];
Print["  TWO FUNDAMENTAL ANGLES OF THE REGULAR 4-SIMPLEX"];
Print["================================================"];
Print[];

(* Coordinates (edge = 1) *)
v = {
  {0, 0, 0, 0},           (* v1 *)
  {1, 0, 0, 0},           (* v2 *)
  {1/2, Sqrt[3]/2, 0, 0}, (* v3 *)
  {1/2, Sqrt[3]/6, Sqrt[6]/3, 0}, (* v4 *)
  {1/2, Sqrt[3]/6, Sqrt[6]/12, Sqrt[10]/4} (* v5 *)
};

(* ============ ANGLE 1: 3D hyperplane dihedral ============ *)
Print["ANGLE 1: 3D hyperplane dihedral angle (between tetrahedral cells)"];
Print["-"~StringRepeat~70];

(* Method: compute the outwards normal of each tetrahedral cell *)
centroid = Total[v]/5;

normals3D = Table[
  Module[{cellVerts, a, b, c, d, M, ns},
    cellVerts = Delete[v, i]; (* tetrahedral cell: all vertices except v_i *)
    a = cellVerts[[1]];
    b = cellVerts[[2]];
    c = cellVerts[[3]];
    d = cellVerts[[4]];
    (* 4x4 matrix: edge vectors + centroid offset *)
    M = {b-a, c-a, d-a, N[centroid - a]};
    ns = NullSpace[M];
    If[Length[ns] == 1, 
      Normalize[ns[[1]]],
      Print["WARNING at cell ", i];
      {0,0,0,0}
    ]
  ],
  {i, 1, 5}
];

Print["5 tetrahedral cell hyperplane normals computed."];
Print[];

Print["Angles between cell hyperplanes (all pairs):"];
allCos = {};
Do[
  Do[
    If[i < j,
      cosVal = Dot[normals3D[[i]], normals3D[[j]]];
      AppendTo[allCos, Abs[cosVal]];
    ],
    {j, i+1, 5}
  ],
  {i, 1, 5}
];
Print["  All |cos| values: ", N[Union[Chop[allCos]], 15]];
Print["  Expected: {1/4} = {", N[1/4, 15], "}"];
Print["  Match: ", Length[Union[Chop[allCos]]] == 1 && Abs[Union[Chop[allCos]][[1]] - 1/4] < 10^-10];
Print[];

(* ============ ANGLE 2: 2D face bivector angle ============ *)
Print["ANGLE 2: 2D face bivector principal angle (between triangular faces sharing edge)"];
Print["-"~StringRepeat~70];

(* Compute the second principal angle between two face 2-planes.
   Two faces {a,b,c} and {a,b,d} share edge {a,b}.
   Within each 3D cell, find the vector orthogonal to (b-a) in the face's direction. *)

(* Face 1: {1,2,3}, Face 2: {1,2,5} share edge {1,2} *)
a = v[[1]]; b = v[[2]]; c = v[[3]]; d = v[[5]];

u = b - a;  (* shared edge direction *)
uUnit = Normalize[u];

(* Vector from a to c, orthogonalized against u *)
w1 = (c - a) - Dot[(c - a), uUnit] * uUnit;
w1Unit = Normalize[w1];

(* Vector from a to d, orthogonalized against u *)
w2 = (d - a) - Dot[(d - a), uUnit] * uUnit;
w2Unit = Normalize[w2];

cosBeta = Dot[w1Unit, w2Unit];
beta = ArcCos[cosBeta];

Print["Face {1,2,3} and Face {1,2,5} sharing edge {1,2}:"];
Print["  Principal angle 1: 0 (shared edge direction)"];
Print["  Principal angle 2: beta = arccos(", N[cosBeta, 15], ") = ", N[beta, 15], " rad"];
Print[];
Print["  cos(beta) = 1/3?  ", Abs[cosBeta - 1/3] < 10^-10];
Print["  cos(pi-beta) = -1/3? (opposite sign convention possible)"];
Print[];

(* Verify: this gives bivector inner product *)
Print["Bivector inner product check (correctly normalized):"];
biv1 = Table[u[[i]]*w1[[j]] - u[[j]]*w1[[i]], {i,1,4}, {j,1,4}];
biv2 = Table[u[[i]]*w2[[j]] - u[[j]]*w2[[i]], {i,1,4}, {j,1,4}];
bivNorm1 = Sqrt[(1/2)*Sum[biv1[[i,j]]^2, {i,1,4}, {j,1,4}]];
bivNorm2 = Sqrt[(1/2)*Sum[biv2[[i,j]]^2, {i,1,4}, {j,1,4}]];
unitBiv1 = biv1 / bivNorm1;
unitBiv2 = biv2 / bivNorm2;
bivIP = (1/2)*Sum[unitBiv1[[i,j]] * unitBiv2[[i,j]], {i,1,4}, {j,1,4}];
Print["  <unit biv1, unit biv2> = cos(0)*cos(beta) = ", N[bivIP, 15]];
Print["  Expected: cos(beta) = 1/3 = ", N[1/3, 15]];
Print["  Match: ", Abs[bivIP - 1/3] < 10^-10];
Print[];

(* ============ SUMMARY ============ *)
Print["========================================"];
Print["  SUMMARY: TWO FUNDAMENTAL ANGLES"];
Print["========================================"];
Print[];
Print["3D hyperplane dihedral: cos = 1/4, theta ~ 75.5 deg"];
Print["  -> This is the angle between tetrahedral CELLS"];
Print["  -> cot^2 = 1/15 comes from THIS angle"];
Print["  -> It governs how curvature propagates between CELLS"];
Print[];
Print["2D face bivector:       cos = 1/3, beta  ~ 70.5 deg"];
Print["  -> This is the angle between triangular FACES (sharing edge)"];
Print["  -> It governs how curvature is distributed WITHIN a cell"];
Print["  -> NOT directly relevant for Casimir (but may be for other physics)"];
Print[];

Print["WHY 1/4 and not 1/3 for Casimir?"];
Print["  Curvature (deficit angle) lives on 2D hinges (triangle faces)."];
Print["  But curvature PROPAGATES through the 4-simplex via the 3D cells."];
Print["  The angle between cells determines the coupling between"];
Print["  hinge curvature and visible face curvature."];
Print["  This is the 3D hyperplane angle: arccos(1/4) -> cot^2 = 1/15."];
Print[];

Print["  The fact that cot^2(arccos(1/4)) = 1/15 and NOT"];
Print["  cot^2(arccos(1/3)) = 1/8 is a NON-TRIVIAL prediction:"];
Print["  if the coupling used the face bivector angle, we'd predict"];
Print["  C0 = pi^2/(16*8) = pi^2/128 ~ 0.077 instead of pi^2/240 ~ 0.041."];
Print["  The prediction is unique: C0 = pi^2/240."];
Print[];