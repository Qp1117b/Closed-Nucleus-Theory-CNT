import CouplingSpace
import Superconductivity

-- 诚实审计：验证“已证明”定理不偷偷依赖 physical_hypothesis 公理
-- 若某定理的 axiom 列表中含 physical_hypothesis，则它其实依赖未证物理假设。

#print axioms CouplingSpace.robertson_ccr_inequality
#print axioms Superconductivity.Reduction.criticalTemperature_pos
#print axioms Superconductivity.Reduction.bcs_universal_gap_ratio
#print axioms Superconductivity.Mechanism.strong_gravity_keeps_pairing_channels
#print axioms Superconductivity.Integral.emergenceIntegral_pos
-- 下面这个预期会依赖 physical_hypothesis（本体论公理）：
#print axioms Superconductivity.Mechanism.superconductivity_requires_relation_network
