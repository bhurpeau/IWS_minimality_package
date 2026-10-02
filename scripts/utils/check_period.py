import numpy as np, itertools
src = open('/mnt/user-data/outputs/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}; exec(src, g)
rk4, kairos, Atilde, A0, N, d, Theta = g['rk4'], g['kairos'], g['Atilde'], g['A0'], g['N'], g['d'], g['Theta']
dt = 1e-3
tau0 = np.array([[0.30,0.00],[0.30,0.05],[0.30,0.05],[-0.20,0.10],[0.10,0.20],[0.10,0.20]])
def u_cont(t, U=2.5):
    u = np.zeros((N,d)); u[0] = (U,0.0); return u

s = (np.zeros((N,d)), np.zeros((N,d)), tau0.copy(), np.zeros(N))
A = A0.copy()
snaps = []
for k in range(8):
    t = 0.0
    while s[3].max() < Theta and t < 40.0:
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
    post, A2, info = kairos(s, A)
    snaps.append((k, A.copy(), s[2].copy(), t))
    s, A = post, A2

print("A_0 == A_2 ?", np.array_equal(snaps[0][1], snaps[2][1]))
print("A_2 == A_4 ?", np.array_equal(snaps[2][1], snaps[4][1]))
print("A_4 == A_6 ?", np.array_equal(snaps[4][1], snaps[6][1]))
for k, Ak, tauk, t in snaps:
    print(f"k={k}  t_kairos={t:.4f}  tau(kairos)=\n{np.round(tauk,4)}")
