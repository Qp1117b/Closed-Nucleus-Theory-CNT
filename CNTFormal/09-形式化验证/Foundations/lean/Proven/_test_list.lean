import Init
open List

-- Test more functions
#eval filter (λ x => x % 2 = 0) (range 5)
#eval reverse [1,2,3]
#eval replicate 3 5
#eval take 2 [1,2,3,4]
#eval drop 2 [1,2,3,4]
#eval [] ++ []
#eval concat [1,2] 3
-- test mem/elem
#eval elem 2 [1,2,3]
