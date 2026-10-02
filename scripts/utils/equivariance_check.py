import numpy as np
src = open('../axiomes_crash_tests/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}
exec(src, g)
rk4, kairos, Atilde, A0, N, d, Theta = g['rk4'], g['kairos'], g['Atilde'], g['A0'], g['N'], g['d'], g['Theta']
dt = 1e-3

perm = [0,2,1,3,5,4]  # sigma = (1 2)(4 5), involution
def act_vec(X):  # relabelling d'un tableau (N,d)
    return X[perm]
def act_graph(A):
    return A[np.ix_(perm, perm)]

tau0 = np.array([[0.30,0.00],[0.30,0.05],[0.30,0.05],
                 [-0.20,0.10],[0.10,0.20],[0.10,0.20]])

def u_cont(t, U=2.5):
    u = np.zeros((N,d)); u[0] = (U,0.0); return u

def first_kairos(tau_init):
    s = (np.zeros((N,d)), np.zeros((N,d)), tau_init.copy(), np.zeros(N))
    A = A0.copy(); t = 0.0
    while s[3].max() < Theta and t < 40:
        s_new = rk4(s, A, lambda tt: u_cont(tt), t, dt)
        if s_new[3].max() >= Theta:
            lo, hi = 0.0, dt
            for _ in range(40):
                mid = (lo+hi)/2
                if rk4(s, A, lambda tt: u_cont(tt), t, mid)[3].max() >= Theta:
                    hi = mid
                else:
                    lo = mid
            s = rk4(s, A, lambda tt: u_cont(tt), t, hi); t += hi
            break
        s, t = s_new, t+dt
    post, A1, info = kairos(s, A)
    return s, A1, info

print("Vérification A0 est bien sigma-invariant :", (act_graph(A0) == A0).all())

for q in (0.05, -0.05, 0.02):
    tau = tau0.copy(); tau[1] = tau0[1] + np.array([0.,q]); tau[2] = tau0[2] - np.array([0.,q])
    tau_sig = act_vec(tau)

    pre1, A1, info1 = first_kairos(tau)
    pre2, A2, info2 = first_kairos(tau_sig)

    A1_pushed = act_graph(A1)
    same_graph = (A1_pushed == A2).all()
    i_relation = (perm[info1['i']] == info2['i'])
    removed_pushed = sorted(perm[j] for j in info1['removed'])
    added_pushed   = sorted(perm[j] for j in info1['added'])
    print(f"q={q:+.3f}  i1={info1['i']} rem={info1['removed']} add={info1['added']}"
          f"  | i2={info2['i']} rem={info2['removed']} add={info2['added']}"
          f"  | sigma(A1)==A2 : {same_graph}  sigma(i1)==i2 : {i_relation}"
          f"  sigma(rem1)=={sorted(info2['removed'])} : {removed_pushed==sorted(info2['removed'])}")

print("\n--- Sur la strate fixe (q=0, tie exacte) ---")
pre1, A1, info1 = first_kairos(tau0)
tau0_sig = act_vec(tau0)
print("tau0 est-il exactement sigma-invariant ?", np.allclose(tau0_sig, tau0))
pre2, A2, info2 = first_kairos(tau0_sig)
print(f"i1={info1['i']} rem={info1['removed']} add={info1['added']}  |  i2={info2['i']} rem={info2['removed']} add={info2['added']}")
print("sigma(A1)==A2 (doit être trivialement vrai car tau0 sigma-invariant) :", (act_graph(A1)==A2).all())
print("A1 lui-même est-il sigma-invariant (i.e. le tie-break a-t-il cassé la symétrie) ?", (act_graph(A1)==A1).all())
