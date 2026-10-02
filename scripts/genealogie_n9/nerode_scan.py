import numpy as np
src = open('/mnt/user-data/outputs/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}
exec(src, g)
rk4, kairos, Atilde, A0, N, d, Theta = g['rk4'], g['kairos'], g['Atilde'], g['A0'], g['N'], g['d'], g['Theta']
dt = 1e-3

# état de base : (H,V,P)=0, structure A0. tau0 exactement symétrique 1<->2, 4<->5.
tau0 = np.array([[0.30,0.00],
                  [0.30,0.05],
                  [0.30,0.05],   # = noeud 1 : tie exacte a q=0
                  [-0.20,0.10],
                  [0.10,0.20],
                  [0.10,0.20]])  # = noeud 4 : tie exacte a q=0

def u_cont(t, U=2.5):
    u = np.zeros((N,d)); u[0] = (U,0.0); return u

def run(tau_init, depth=2, Tmax=40.0):
    s = (np.zeros((N,d)), np.zeros((N,d)), tau_init.copy(), np.zeros(N))
    A = A0.copy()
    word = []
    for k in range(depth):
        t = 0.0
        while s[3].max() < Theta and t < Tmax:
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
        else:
            word.append(None); break
        post, A2, info = kairos(s, A)
        word.append((info['i'], tuple(info['removed']), tuple(info['added'])))
        s, A = post, A2
    return word

def delta(q, dv):
    d_ = dv.copy(); return d_

print("=== Direction transverse (brise 1<->2) : v = e1*(0,dq) - e2*(0,dq) ===")
for q in (-0.10,-0.05,-0.01,-0.001,0.0,0.001,0.01,0.05,0.10):
    tau = tau0.copy()
    tau[1] = tau0[1] + np.array([0.0,q])
    tau[2] = tau0[2] - np.array([0.0,q])
    w = run(tau, depth=2)
    print(f" q={q:+.3f}  mot={w}")

print("\n=== Direction symétrique (préserve 1<->2, 4<->5) : v uniforme sur (1,2) et (4,5) ===")
for q in (-0.10,-0.05,-0.01,0.0,0.01,0.05,0.10):
    tau = tau0.copy()
    tau[1] = tau0[1] + np.array([0.0,q]); tau[2] = tau0[2] + np.array([0.0,q])
    tau[4] = tau0[4] + np.array([0.0,q]); tau[5] = tau0[5] + np.array([0.0,q])
    w = run(tau, depth=2)
    print(f" q={q:+.3f}  mot={w}")
