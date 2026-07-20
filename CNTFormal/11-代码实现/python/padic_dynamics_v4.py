"""
CNT p进动力学研究 - 第四版 (v4): 开放问题A (E_n = -(gamma_n/2 + gamma_n^2) 的来源)
背景: v3 定理4.1/4.2 严格导出 s_n=1/2+i*gamma_n (临界线模式).
     结果4.1(唯象谱公式) 给出 E_n = -(gamma_n/2 + gamma_n^2), 诚实标注
     "从 xi 几何与传输方程边界条件的严格推导是开放问题(优先级A)".
     预期来源: "xi 函数在零点处的二阶导数 与 Berry-Keating 相空间量子化的联合效应".

目标: 数值探索 E_n 公式的结构来源, 缩小开放问题A.
"""
import numpy as np
import mpmath as mp

def riemann_zeros(n=20):
    mp.mp.dps = 50
    return np.array([float(mp.zetazero(k+1).imag) for k in range(n)])

def analyze_s_algebra(gammas):
    print("=== H1: s_n 代数结构 vs E_n (v3 公式) ===")
    print("%3s %10s %12s %10s %12s %10s %12s" % ("n","gamma_n","E_n(v3)","|s_n|^2","s_n(1-s_n)","1/4+g^2","E vs -|s|^2"))
    for n, g in enumerate(gammas[:8], 1):
        sn = 0.5 + 1j*g
        abs2 = abs(sn)**2
        sn1sn = sn*(1-sn)
        E_v3 = -(g/2 + g**2)
        candidate = -abs2 - g/2 + 0.25
        print("%3d %10.4f %12.4f %10.4f %12.4f %10.4f %12.4f" % (n,g,E_v3,abs2,sn1sn.real,0.25+g**2,candidate))
    print("\n  E_n(v3) = -(g^2 + g/2) = -(|s_n|^2 - 1/4) - g/2")
    print("  -> -g^2 部分 = -(|s_n|^2 - 1/4), 即来自临界线模平方")

def berry_keating_check(gammas):
    print("\n=== H2: Berry-Keating 半经典 vs E_n 密度 ===")
    T = gammas
    N_actual = np.arange(1, len(T)+1)
    N_theory = T/(2*np.pi)*np.log(T/(2*np.pi*np.e))
    E = -(gammas/2 + gammas**2)
    print("  gamma_n 范围: [%.2f, %.2f]" % (T.min(), T.max()))
    print("  E_n 范围: [%.2f, %.2f]" % (E.min(), E.max()))
    print("  前8个 N_actual(gamma): %s" % N_actual[:8])
    print("  前8个 N_theory(gamma): %s" % np.round(N_theory[:8],2))
    print("  -> gamma_n 是Berry-Keating零点(已确证 L3); E_n 是其单调变换")

def radial_hamiltonian_hypothesis(gammas):
    print("\n=== H3: 径向哈密顿量 k_n=i*s_n 本征值 ===")
    for n, g in enumerate(gammas[:5], 1):
        sn = 0.5 + 1j*g
        k = 1j*sn
        E = -(k**2)
        print("  n=%d: g=%.3f, k_n=i*s_n=%.3f%+.3fi, E_n=-(k^2)=%.3f%+.3fi" % (n,g,k.real,k.imag,E.real,E.imag))
    print("  -> 若 k_n=i*s_n, E_n 实部=1/4-g^2 (缺 -g/2 项), 虚部=g_n")
    print("  -> v3 E_n=-(g/2+g^2) 纯实数: 需取实部并加 -g/2 修正")
    print("  -> 开放项: -g/2 项来源 (Berry-Keating 相空间面积 1/2 修正?)")

def main():
    mp.mp.dps = 50
    g = riemann_zeros(20)
    analyze_s_algebra(g)
    berry_keating_check(g)
    radial_hamiltonian_hypothesis(g)
    print("\n=== 阶段性结论 (开放问题A缩窄) ===")
    print("1. gamma_n 严格 (v3 定理4.2筛选), 来自 Tate/adelic (v3验证).")
    print("2. E_n=-(g_n/2+g_n^2) 是唯象公式 (v3 结果4.1, 开放A).")
    print("3. H1: -g_n^2 = -(|s_n|^2-1/4) 来自临界线模平方; 但 -g_n/2 无 s_n 代数来源.")
    print("4. H3: k_n=i*s_n 时 E_n实部=1/4-g^2 (缺 -g/2), 虚部=g_n (应消除).")
    print("5. 推断: -g_n/2 来自 Berry-Keating 相空间量子化面积修正(半经典1/2项),")
    print("   非 s_n 纯代数. 与 v3 注'xi''''与Berry-Keating联合效应'一致.")

if __name__ == "__main__":
    main()
