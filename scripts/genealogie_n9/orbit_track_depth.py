import numpy as np
import itertools
import time

src = open('/mnt/user-data/outputs/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}
exec(src, g)
rk4, kairos, Atilde, A0, N, d, Theta = g['rk4'], g['kairos'], g['Atilde'], g['A0'], g['N'], g['d'], g['Theta']
dt = 1e-3

def automorphisms(A):
    auts = []
    for p in itertools.permutations(range(N)):
        Ap = A[np.ix_(p, p)]
        if np.array_equal(Ap, A):
            auts.append(p)
    return auts

def stab(auts, tau, tol=1e-9):
    return [p for p in auts if np.allclose(tau[list(p)], tau, atol=tol)]

tau0 = np.array([[0.30, 0.00], [0.30, 0.05], [0.30, 0.05],
                  [-0.20, 0.10], [0.10, 0.20], [0.10, 0.20]])

def u_cont(t, U=2.5):
    u = np.zeros((N, d)); u[0] = (U, 0.0); return u

def track(tau_init, depth, Tmax=40.0, label=""):
    s = (np.zeros((N, d)), np.zeros((N, d)), tau_init.copy(), np.zeros(N))
    A = A0.copy()
    rows = []
    for k in range(depth):
        t = 0.0
        stuck = False
        while s[3].max() < Theta and t < Tmax:
            s_new = rk4(s, A, lambda tt: u_cont(tt), t, dt)
            if s_new[3].max() >= Theta:
                lo, hi = 0.0, dt
                for _ in range(40):
                    mid = (lo + hi) / 2
                    if rk4(s, A, lambda tt: u_cont(tt), t, mid)[3].max() >= Theta:
                        hi = mid
                    else:
                        lo = mid
                s = rk4(s, A, lambda tt: u_cont(tt), t, hi); t += hi
                break
            s, t = s_new, t + dt
        else:
            stuck = True
        if stuck:
            print(f"  [{label}] arrêt : pas de Kairos atteint avant Tmax à k={k}")
            break
        tau_at_kairos = s[2].copy()
        auts = automorphisms(A)
        G = stab(auts, tau_at_kairos)
        post, A2, info = kairos(s, A)
        auts_next = automorphisms(A2)
        G_next = stab(auts_next, post[2])
        rows.append(dict(k=k, i=info['i'], removed=tuple(info['removed']), added=tuple(info['added']),
                          Aut_size=len(auts), G_size=len(G),
                          Aut_next_size=len(auts_next), G_next_size=len(G_next),
                          G_nontrivial=len(G) > 1))
        s, A = post, A2
    return rows

DEPTH = 15

t0 = time.time()
print("=== Branche exactement symétrique (q=0), profondeur", DEPTH, "===")
rows_sym = track(tau0.copy(), depth=DEPTH, label="sym")
for r in rows_sym:
    print(r)

print("\n=== Branche générique (q=0.05, transverse), profondeur", DEPTH, "===")
tau_g = tau0.copy(); tau_g[1] = tau0[1] + np.array([0., 0.05]); tau_g[2] = tau0[2] - np.array([0., 0.05])
rows_gen = track(tau_g, depth=DEPTH, label="gen")
for r in rows_gen:
    print(r)

print("\n--- temps de calcul : %.1fs ---" % (time.time() - t0))

print("\n=== Résumé : occurrences de G_size > 1 (vraie obstruction orbitale) ===")
for label, rows in (("symétrique", rows_sym), ("générique", rows_gen)):
    hits = [r['k'] for r in rows if r['G_nontrivial']]
    print(f"  branche {label} : k avec G_size>1 -> {hits}")
    reappear_inert = [r['k'] for r in rows if r['Aut_size'] > 1 and not r['G_nontrivial']]
    print(f"  branche {label} : k avec Aut_size>1 mais G_size==1 (réapparition inerte) -> {reappear_inert}")
