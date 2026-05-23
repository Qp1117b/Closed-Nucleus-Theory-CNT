-- This module serves as the root of the `CNTConjectures` library.
-- All unproven conjectures, working hypotheses, and speculative extensions
-- that depend on the rigorous CNTFormal core axioms.
--
-- CNTFormal (纯净库): 6 DCNC公理 + 严格证明的定理, 0 sorry
-- CNTConjectures (猜想库): 猜想、工作假设、待验证扩展
--
-- 当前状态:
--   [猜想] = theorem + sorry, 待从公理严格证明
--   [工作假设] = 待数值验证或推导的假设
--
-- 所有标记为sorry的定理不会污染主库CNTFormal的严格性。
import CNTConjectures.AxiomConsistency
import CNTConjectures.AxiomDerivationChain
import CNTConjectures.HPIAxiomCorrespondence
import CNTConjectures.HPICorrection
import CNTConjectures.IdempotentQuantization
import CNTConjectures.IntertwinerStructure
import CNTConjectures.OntologicalMechanics
import CNTConjectures.ReproductionEnergy

-- 严格性配置（猜想库也需要纪律）
set_option autoImplicit false
set_option relaxedAutoImplicit false