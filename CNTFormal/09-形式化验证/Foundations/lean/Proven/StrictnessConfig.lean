/-
# CNT 严格性配置

所有 CNT 形式化文件必须遵循以下配置。

## 纪律原则
1. 零 sorry（CNTFormal 库）
2. 显式标记所有 axiom
3. 禁用隐式声明
4. 锁定工具链
5. 禁止 unsafe/partial/meta

## 配置说明
- `warningAsError true` — 所有警告视为错误
- `autoImplicit false` — 禁止自动隐式参数
- `relaxedAutoImplicit false` — 禁止宽松自动隐式

## 使用方式
在根模块文件（CNTFormal.lean, CNTConjectures.lean）的 import 之后添加：
```lean
set_option warningAsError true in
set_option autoImplicit false in
set_option relaxedAutoImplicit false in
```
-/
