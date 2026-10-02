import numpy as np
import itertools

src = open(str(_pathlib.Path(__file__).resolve().parents[1] / 'axiomes_crash_tests' / 'temoin_C23_noyau.py')).read().split("# ---------------- 1.")[0]
g = {}
exec(src, g)
rk4, kairos, Atilde, cosine = g['rk4'], g['kairos'], g['Atilde'], g['cosine']
dt = 1e-3
d = g['d']
Theta = g['Theta']

# ---------------- Nouveau témoin N=9 : orbite-3 en nb(0), deux orbites (2 et 3) en nn(0) ----------------
N = 9
g['N'] = N
edges = [(0, 1), (0, 2), (0, 3), (4, 5)]   # 6,7,8 isolés ; nb(0)={1,2,3} jumeaux ; nn(0)={4,5}∪{6,7,8}
A_new = np.zeros((N, N), dtype=int)
for i, j in edges:
    A_new[i, j] = A_new[j, i] = 1
g['A0'] = A_new

def automorphisms_fast(A, n):
    deg = A.sum(axis=1)
    classes = {}
    for v in range(n):
        classes.setdefault(deg[v], []).append(v)
    keys = list(classes.keys())
    per_class_perms = [list(itertools.permutations(classes[k])) for k in keys]
    auts = []
    for combo in itertools.product(*per_class_perms):
        p = [None] * n
        for k, cls_perm in zip(keys, combo):
            for orig, img in zip(classes[k], cls_perm):
                p[orig] = img
        p = tuple(p)
        if np.array_equal(A[np.ix_(p, p)], A):
            auts.append(p)
    return auts

def orbits(auts, n):
    seen, orbs = set(), []
    for v in range(n):
        if v in seen:
            continue
        orb = sorted({p[v] for p in auts})
        orbs.append(orb)
        seen.update(orb)
    return orbs

auts0 = automorphisms_fast(A_new, N)
print("=== Graphe témoin N=9 ===")
print("  arêtes :", edges)
print("  |Aut(A0)| =", len(auts0))
print("  orbites de Aut(A0) :", orbits(auts0, N))

def stab(auts, tau, tol=1e-9):
    return [p for p in auts if np.allclose(tau[list(p)], tau, atol=tol)]

def u_cont(t, U=2.5):
    u = np.zeros((N, d)); u[0] = (U, 0.0); return u

# état initial : tau bloc-symétrique -> tau[1]=tau[2]=tau[3], tau[4]=tau[5] (proche de v0), tau[6]=tau[7]=tau[8]
v0  = np.array([0.30, 0.00])
vA  = np.array([-0.20, 0.10])   # bloc nb(0)={1,2,3}
vB  = np.array([0.30, 0.02])    # bloc nn {4,5} : très proche de v0
vC  = np.array([0.10, 0.20])    # bloc nn {6,7,8} : moins proche
tau_init = np.zeros((N, d))
tau_init[0] = v0
tau_init[1] = tau_init[2] = tau_init[3] = vA
tau_init[4] = tau_init[5] = vB
tau_init[6] = tau_init[7] = tau_init[8] = vC

s = (np.zeros((N, d)), np.zeros((N, d)), tau_init.copy(), np.zeros(N))
A = A_new.copy()
t = 0.0
Tmax = 40.0
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

print("\n=== Premier Kairos ===")
print("  t* =", round(t, 4), " nœud au seuil :", int(np.flatnonzero(s[3] >= Theta)[0]))
G0 = stab(auts0, s[2])
print("  |G(tau au Kairos)| =", len(G0), " (= |Aut(A0)| ?", len(G0) == len(auts0), ")")

post, A_next, info = kairos(s, A)
print("  i* =", info['i'], " m =", info['m'])
print("  similarités :", {j: round(x, 6) for j, x in info['sim'].items()})
print("  retirés (nb) :", info['removed'], "  ajoutés (nn) :", info['added'])

# lecture du cas selon le lemme : T = ensemble tie au seuil pertinent, a = nb strictement mieux classés
sim = info['sim']
nb = [1, 2, 3]
nn = [4, 5, 6, 7, 8]
sim_nb_sorted = sorted(nb, key=lambda j: sim[j])
sim_nn_sorted = sorted(nn, key=lambda j: -sim[j])
print("\n  -- côté retrait (nb) -- valeurs triées :", [(j, round(sim[j], 6)) for j in sim_nb_sorted])
print("  -- côté ajout   (nn) -- valeurs triées :", [(j, round(sim[j], 6)) for j in sim_nn_sorted])

print("\n=== Recâblage : structure de Aut(A) avant / après ===")
auts_next = automorphisms_fast(A_next, N)
print("  |Aut(A0)|      =", len(auts0), " orbites :", orbits(auts0, N))
print("  |Aut(A_next)|  =", len(auts_next), " orbites :", orbits(auts_next, N))
