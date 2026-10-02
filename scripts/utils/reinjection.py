import numpy as np
import itertools

src = open('../axiomes_crash_tests/temoin_C23_noyau.py').read().split("# ---------------- 1.")[0]
g = {}
exec(src, g)
rk4, kairos, Atilde, A0, N, d, Theta, cosine = g['rk4'], g['kairos'], g['Atilde'], g['A0'], g['N'], g['d'], g['Theta'], g['cosine']
dt = 1e-3

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p, p)], A)]

def stab(auts, tau, tol=1e-9):
    return [p for p in auts if np.allclose(tau[list(p)], tau, atol=tol)]

def perm_apply(vec_nodewise, p):
    # returns array w with w[i] = vec[p[i]]  (i.e. P_sigma acting by relabelling)
    return vec_nodewise[list(p)]

tau0 = np.array([[0.30, 0.00], [0.30, 0.05], [0.30, 0.05],
                  [-0.20, 0.10], [0.10, 0.20], [0.10, 0.20]])

def u_cont(t, U=2.5):
    u = np.zeros((N, d)); u[0] = (U, 0.0); return u

def run_to_kairos(s, A, Tmax=40.0):
    t = 0.0
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
            return s, t
        s, t = s_new, t + dt
    return s, t

def report_row(label, A, s_at_kairos):
    auts = automorphisms(A)
    G = stab(auts, s_at_kairos[2])
    print(f"  [{label}] Aut(A)={len(auts)}  G(tau)={len(G)}  (tie exacte au sens de sigma : {len(G)>1})")
    return auts, G

# ---------- Phase 1 : reproduire jump 0 et jump 1 normalement (branche symetrique) ----------
s = (np.zeros((N, d)), np.zeros((N, d)), tau0.copy(), np.zeros(N))
A = A0.copy()

print("=== Jump 0 (référence, déjà connu) ===")
s_k, t0 = run_to_kairos(s, A)
report_row("k=0 avant saut", A, s_k)
post0, A1, info0 = kairos(s_k, A)
print("   retirés", info0['removed'], "ajoutés", info0['added'])

print("\n=== Jump 1 (normal, sans intervention) ===")
s_k1, t1 = run_to_kairos(post0, A1)
report_row("k=1 avant saut", A1, s_k1)
post1, A2, info1 = kairos(s_k1, A1)
print("   retirés", info1['removed'], "ajoutés", info1['added'])
print("   A2 == A0 ?", np.array_equal(A2, A0))

# ---------- Phase 2 : réinjection délibérée avant jump 2 ----------
print("\n=== Réinjection : symétrisation complète de l'état sous un automorphisme de A2 ===")
auts_A2 = automorphisms(A2)
sigma = next(p for p in auts_A2 if p != tuple(range(N)))
print("   automorphisme non trivial choisi sigma =", sigma)

H2, V2, tau2, P2 = post1
def symmetrize(vec):
    return 0.5 * (vec + perm_apply(vec, sigma))

H_sym  = symmetrize(H2)
V_sym  = symmetrize(V2)
tau_sym = symmetrize(tau2)
P_sym  = 0.5 * (P2 + P2[list(sigma)])
state_sym = (H_sym, V_sym, tau_sym, P_sym)

print("   écart max avant symétrisation (tau) :", np.abs(tau2 - perm_apply(tau2, sigma)).max())
print("   écart max après  symétrisation (tau) :", np.abs(tau_sym - perm_apply(tau_sym, sigma)).max())
print("   écart max après  symétrisation (H)   :", np.abs(H_sym - perm_apply(H_sym, sigma)).max())

print("\n=== Jump 2, en partant de l'état réinjecté (symétrique par construction) ===")
s_k2, t2 = run_to_kairos(state_sym, A2)
print("   dérive de la symétrie pendant le vol libre jusqu'au prochain Kairos :")
print("   écart max (tau) au moment du saut :", np.abs(s_k2[2] - perm_apply(s_k2[2], sigma)).max())
print("   écart max (H)   au moment du saut :", np.abs(s_k2[0] - perm_apply(s_k2[0], sigma)).max())
auts2, G2 = report_row("k=2 réinjecté, avant saut", A2, s_k2)
post2, A3, info2 = kairos(s_k2, A2)
print("   i* =", info2['i'], " m =", info2['m'])
print("   similarités :", {j: round(x, 6) for j, x in info2['sim'].items()})
print("   retirés", info2['removed'], "ajoutés", info2['added'])

print("\n=== Équivariance après ce second saut engendré (comme pour k=0) ===")
auts3 = automorphisms(A3)
print("   Aut(A2) avant saut :", len(auts2), " -> Aut(A3) après saut :", len(auts3))
print("   sigma encore un automorphisme de A3 ?", any(p == sigma for p in auts3))
print("   même schéma (m,t,a) que le premier obstacle (m=2,t=2,a=1) ?",
      info2['m'] == info0['m'] and set(info2['removed']) == set(sigma_orbit for sigma_orbit in [1,2] if False) or None)
print("   comparaison brute : info0 =", dict(m=info0['m'], removed=info0['removed'], added=info0['added']))
print("                        info2 =", dict(m=info2['m'], removed=info2['removed'], added=info2['added']))
