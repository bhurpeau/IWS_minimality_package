import io, contextlib, numpy as np
src = open('../axiomes_crash_tests/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}; exec(src, g)
rk4, A0, N, d, Theta = g['rk4'], g['A0'], g['N'], g['d'], g['Theta']
def maxP(U, Tmax=200, dt=2e-3):
    s = (np.zeros((N,d)), np.zeros((N,d)), np.zeros((N,d)), np.zeros(N)); best=0
    for k in range(int(Tmax/dt)):
        V0 = s[1][0]; nv = np.linalg.norm(V0)
        u = np.zeros((N,d)); u[0] = U*(V0/nv if nv>1e-9 else np.array([1.,0.]))
        s = rk4(s, A0, lambda t: u, k*dt, dt); best = max(best, s[3].max())
        if best >= Theta: return best, k*dt
    return best, None
for U in (0.05,0.1,0.15,0.2,0.3,0.5):
    print(U, maxP(U))
