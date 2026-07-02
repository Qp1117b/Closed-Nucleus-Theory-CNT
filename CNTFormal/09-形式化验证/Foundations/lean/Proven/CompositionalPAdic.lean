import Init

/-
合成p进数（Compositional p-adic Numbers）— Lean 4 严格形式化验证
对应: 05-合成p进数.md  |  Lean 4.29.1  |  只使用 Init

定理 (零 sorry, 零假证明):
  T1: encode_is_function       — rw (定理3.3正向)
  T2: encode_deterministic     — ∃+∀ (定理3.3正向)
  T3: decode_non_unique        — native_decide+反例 (定理3.3反向)
  T4: pAdicSum_mod_eq_a0       — dvd+mod (引理3.4)
  T5: layerEq_trans            — 结构归纳 (§5.3核心)
  T6: prefixEq_succ_imp        — Bool逻辑
-/

/-! ============================================================
## 自定义辅助 (autoImplicit=false → 显式类型参数)
============================================================ -/

def listJoin {α : Type} : List (List α) → List α
  | [] => []
  | xs :: xss => xs ++ listJoin xss

def cartesianPairs (xs ys : List (List Nat)) : List (List (List Nat)) :=
  listJoin (List.map (λ x => List.map (λ y => [x, y]) ys) xs)

/-! ============================================================
## 第2节: 基本定义
============================================================ -/

open List

def plainSum : List Nat → Nat := sum

def pAdicSum : List Nat → Nat → Nat
  | [],       _    => 0
  | a :: as, base => a + base * pAdicSum as base

example : plainSum [3,5,2] = 10 := by native_decide
example : pAdicSum [7,4] 10 = 47 := by native_decide

def encodeGo (layers : List (List Nat)) (acc_x acc_P : Nat) (prev_p : Option Nat) : Nat :=
  match layers with
  | [] => acc_x
  | layer :: rest =>
    match prev_p with
    | none =>
      let S0 := plainSum layer
      encodeGo rest (acc_x + S0 * acc_P) S0 (some S0)
    | some pn =>
      let Sn := pAdicSum layer pn
      encodeGo rest (acc_x + Sn * acc_P) (acc_P * Sn) (some Sn)

def encode (coeffs : List (List Nat)) : Nat := encodeGo coeffs 0 1 none

def example1 : List (List Nat) := [[3,5,2], [7,4]]
def example2 : List (List Nat) := [[3], [2]]

example : encode example1 = 480 := by native_decide
example : encode example2 = 9 := by native_decide

/-! ============================================================
## 定理 3.3: 确定性编码
============================================================ -/

theorem encode_is_function {c1 c2 : List (List Nat)} (h : c1 = c2) : encode c1 = encode c2 := by
  rw [h]

theorem encode_deterministic (coeffs : List (List Nat)) :
    ∃ x, x = encode coeffs ∧ ∀ y, y = encode coeffs → y = x := by
  refine ⟨encode coeffs, rfl, ?_⟩
  intro y hy; exact hy

def ex_altA : List (List Nat) := [[5], [95]]
def ex_altB : List (List Nat) := [[5], [90, 1]]
def ex_altC : List (List Nat) := [[5], [65, 1, 1]]

example : encode ex_altA = 480 := by native_decide
example : encode ex_altB = 480 := by native_decide
example : encode ex_altC = 480 := by native_decide
example : example1 ≠ ex_altA := by native_decide
example : encode example1 = encode ex_altA := by native_decide

theorem decode_non_unique : ∃ (c1 c2 : List (List Nat)),
    c1 ≠ c2 ∧ encode c1 = encode c2 := by
  refine ⟨example1, ex_altA, ?_, ?_⟩
  · native_decide
  · native_decide

/-! ============================================================
## 引理 3.4: 基底同余
============================================================ -/

theorem pAdicSum_mod_eq_a0 (a : Nat) (as : List Nat) (base : Nat) :
    pAdicSum (a :: as) base % base = a % base := by
  unfold pAdicSum
  have h_dvd : base ∣ base * pAdicSum as base :=
    ⟨pAdicSum as base, rfl⟩
  have h_zero : (base * pAdicSum as base) % base = 0 :=
    Nat.mod_eq_zero_of_dvd h_dvd
  rw [Nat.add_mod, h_zero]
  simp

/-! ============================================================
## §5.3: layerEq 传递性

layerEq 通过结构递归直接定义, 对 h1,h2 同步遍历, 索引 k 递减。
============================================================ -/

def layerEq : List (List Nat) → List (List Nat) → Nat → Bool
  | [],      [],      _ => true
  | [],      _::_,    _ => false
  | _::_,    [],      _ => false
  | l1::h1,  l2::h2,  0 => l1 == l2
  | _::h1,   _::h2,  k+1 => layerEq h1 h2 k

theorem layerEq_trans (h1 h2 h3 : List (List Nat)) (k : Nat)
    (h12 : layerEq h1 h2 k = true) (h23 : layerEq h2 h3 k = true) :
    layerEq h1 h3 k = true := by
  -- 对 h1 做结构归纳
  induction h1 generalizing h2 h3 k with
  | nil =>
    -- h1 = []
    induction h2 generalizing h3 k with
    | nil =>
      -- h2 = []
      induction h3 with
      | nil => rfl
      | cons l3 h3 =>
        -- h1=[], h2=[], h3=l3::h3 → 第三个子句 → false, 矛盾
        injection h23
    | cons l2 h2 ih =>
      -- h1=[], h2=l2::h2 → 第二子句(k=0)=false 或 第五子句(k+1)
      -- 无论如何 layerEq 返回 false → h12 矛盾
      cases k with
      | zero => simp [layerEq] at h12
      | succ k => simp [layerEq] at h12
  | cons l1 h1 ih =>
    -- h1 = l1::h1
    induction h2 generalizing h3 k with
    | nil =>
      cases k with
      | zero => simp [layerEq] at h12
      | succ k => simp [layerEq] at h12
    | cons l2 h2 ih2 =>
      -- h2 = l2::h2
      induction h3 generalizing k with
      | nil =>
        cases k with
        | zero => simp [layerEq] at h23
        | succ k => simp [layerEq] at h23
      | cons l3 h3 ih3 =>
        -- h3 = l3::h3 — 核心情况
        cases k with
        | zero =>
          -- k=0: layerEq = (l1==l2), (l2==l3), 需证 (l1==l3)
          simp [layerEq] at h12 h23 ⊢
          have hl12 : l1 = l2 := by simpa using h12
          have hl23 : l2 = l3 := by simpa using h23
          subst hl12; subst hl23; rfl
        | succ k =>
          -- k+1: layerEq h1 h2 k+1 = layerEq h1 h2 k
          simp [layerEq] at h12 h23 ⊢
          exact ih h2 h3 k h12 h23

def prefixEq (h1 h2 : List (List Nat)) : Nat → Bool
  | 0 => true
  | n+1 => prefixEq h1 h2 n && layerEq h1 h2 n

theorem prefixEq_succ_imp (h1 h2 : List (List Nat)) (n : Nat)
    (h : prefixEq h1 h2 (n+1) = true) : prefixEq h1 h2 n = true :=
  (Bool.and_eq_true_iff.mp h).left

-- 具体实例验证
def hA : List (List Nat) := [[3,5,2], [7,4], [1,0,2]]
def hB : List (List Nat) := [[3,5,2], [7,4], [9,9,9]]
def hC : List (List Nat) := [[3,5,2], [8,8,8], [1,0,2]]

example : prefixEq hA hB 2 := by native_decide
example : ¬ prefixEq hA hB 3 := by native_decide
example : prefixEq hA hC 1 := by native_decide
example : ¬ prefixEq hA hC 2 := by native_decide
example : prefixEq hB hC 1 := by native_decide
example : (prefixEq hA hB 2 && prefixEq hB hC 1 → prefixEq hA hC 1) := by native_decide

/-! ============================================================
## extractS + computeP
============================================================ -/

def extractSGo (layers : List (List Nat)) (prev_p : Option Nat) : List Nat :=
  match layers with
  | [] => []
  | layer :: rest =>
    match prev_p with
    | none =>
      let S0 := plainSum layer
      S0 :: extractSGo rest (some S0)
    | some pn =>
      let Sn := pAdicSum layer pn
      Sn :: extractSGo rest (some Sn)

def extractS (coeffs : List (List Nat)) : List Nat := extractSGo coeffs none

def computePGo : List Nat → Nat → List Nat
  | [],    acc => [acc]
  | s :: ss, acc => acc :: computePGo ss (acc * s)

def computeP (Ss : List Nat) : List Nat := computePGo Ss 1

example : extractS example1 = [10, 47] := by native_decide
example : computeP [10, 47] = [1, 10, 470] := by native_decide
example : encode example1 = (computeP (extractS example1)).sum - 1 := by native_decide
example : encode example2 = (computeP (extractS example2)).sum - 1 := by native_decide

def example3 : List (List Nat) := [[3,5,2], [7,4], [1, 0, 2]]
example : encode example3 = 2077410 := by native_decide
example : extractS example3 = [10, 47, 4419] := by native_decide
example : computeP (extractS example3) = [1, 10, 470, 2076930] := by native_decide
example : (computeP (extractS example3)).sum = 2077411 := by native_decide
example : encode example3 = (computeP (extractS example3)).sum - 1 := by native_decide

/-! ### 穷举验证: 两层(N=1), 系数≤3, 层长≤3: 64×16=1024条 --/

-- 生成所有系数列表: 长度:=maxLen, 每系数∈{0..maxCoeff}
def allSingleLayers (maxCoeff maxLen : Nat) : List (List Nat) :=
  match maxLen with
  | 0 => [[]]
  | n+1 =>
    listJoin (List.map (λ tail =>
      List.map (λ c => c :: tail) (range (maxCoeff+1)))
      (allSingleLayers maxCoeff n))

def exhaustiveVerify : Bool := Id.run do
  let layers0 := allSingleLayers 3 3
  let layers1 := allSingleLayers 3 2
  for c in cartesianPairs layers0 layers1 do
    let x := encode c
    let ps := computeP (extractS c)
    if ps.sum = 0 then return false
    if x + 1 ≠ ps.sum then return false
  return true

-- 结构性恒等式穷举验证 (用 by native_decide, 因为计算量可控)
example : exhaustiveVerify := by
  native_decide

example : (allSingleLayers 3 3).length = 64 := by
  native_decide

example : (allSingleLayers 3 2).length = 16 := by
  native_decide

example : (cartesianPairs (allSingleLayers 3 3) (allSingleLayers 3 2)).length = 1024 := by
  native_decide

/-! ============================================================
## 递推整除约束
============================================================ -/

example : encode example1 % 10 = 0 := by native_decide
example : (encode example1 / 10 - 1) % 47 = 0 := by native_decide
example : encode example2 % 3 = 0 := by native_decide
example : (encode example2 / 3 - 1) % 2 = 0 := by native_decide
example : encode example3 % 10 = 0 := by native_decide
example : (encode example3 / 10 - 1) % 47 = 0 := by native_decide
example : ((encode example3 / 10 - 1) / 47 - 1) % 4419 = 0 := by native_decide

/-! ============================================================
## §3.3: 剩余的双向结构 — 取模不为零

两种剩余 (对应文档 §3.3):
  (1) 结构性剩余: x mod P_k = S_0 ≠ 0 (高层把握低层)
  (2) 系数性剩余: S_n mod p_n = a_{n,0} ≠ 0 (低层被高层取模)
  统一标准: 取模不为零是剩余存在的数学标志。
============================================================ -/

section RemainderBidirectional

-- §3.3: 剩余的双向结构 — 取模不为零的严格验证
--   (1) 结构性剩余: x mod P_k = S_0 ≠ 0 (高层把握低层)
--   (2) 系数性剩余: S_n mod p_n = a_{n,0} ≠ 0 (低层被高层取模)
--   统一标准: 取模不为零是剩余存在的数学标志。
--   以下用具体例子 example3 (3层: S0=10, S1=47, S2=4419) 严格验证。

-- 已知: P_2 = S0 * S1 = 470
example : 10 * 47 = 470 := by native_decide

-- (1) 结构性剩余: x mod P_2 = S_0 = 10 ≠ 0
example : encode example3 % 470 = 10 := by native_decide
example : encode example3 % 470 ≠ 0 := by native_decide

-- x mod P_3 = S_0 + S_1 * P_1 = 480 ≠ 0
example : encode example3 % (10 * 47 * 4419) = 480 := by native_decide
example : encode example3 % (10 * 47 * 4419) ≠ 0 := by native_decide

-- (2) 系数性剩余: S_n mod p_n = a_{n,0} ≠ 0
-- S_1 mod p_1 = 47 mod 10 = 7 = a_{1,0}
example : 47 % 10 = 7 := by native_decide
example : 47 % 10 ≠ 0 := by native_decide
-- S_2 mod p_2 = 4419 mod 47 = 1 = a_{2,0}
example : 4419 % 47 = 1 := by native_decide
example : 4419 % 47 ≠ 0 := by native_decide

-- 统一定理: 两种取模均不为零 — 剩余是双向的
theorem remainder_bidirectional_example3 :
    encode example3 % 470 ≠ 0 ∧ 47 % 10 ≠ 0 := by
  apply And.intro
  · native_decide
  · native_decide

end RemainderBidirectional

/-! ============================================================
## 命题 5.2: 有限可能性 (N=1 构造性枚举)
============================================================ -/

def allN1Histories (x : Nat) : List (List (List Nat)) :=
  filterMap (λ s0 =>
    if s0 = 0 then none
    else if x % s0 ≠ 0 then none
    else
      let s1 := x / s0 - 1
      if s1 = 0 then none
      else some [[s0], [s1]])
    (range (x + 1))

def myAll {α : Type} (p : α → Bool) : List α → Bool
  | [] => true
  | x :: xs => p x && myAll p xs

example : myAll (λ h => encode h == 480) (allN1Histories 480) := by native_decide
example : (allN1Histories 480).length ≤ 480 := by native_decide
example : (allN1Histories 10).length ≤ 10 := by native_decide
example : (allN1Histories 100).length ≤ 100 := by native_decide
example : (allN1Histories 1).length ≤ 1 := by native_decide
example : (allN1Histories 0).length ≤ 0 := by native_decide
