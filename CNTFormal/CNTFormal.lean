-- This module serves as the root of the `CNTFormal` library.
-- CNTFormal (纯净项目): 仅包含6 DCNC公理和严格证明的定理
-- 零 sorry, 零猜想, 零工作假设, 零跳跃
-- 猜想和待验证内容已移至 CNTConjectures 项目
import CNTFormal.Basic
import CNTFormal.CategoryTheory
import CNTFormal.SimplexGeometry
import CNTFormal.AlphaDerivation
import CNTFormal.PhysicalMapping
import CNTFormal.ReproductionPeriod
import CNTFormal.HistoryAccumulation
import CNTFormal.SimplexDominance

-- 严格性配置（纪律防线）
set_option autoImplicit false
set_option relaxedAutoImplicit false