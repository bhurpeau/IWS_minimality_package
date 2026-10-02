"""
Témoin numérique minimal de C23^act pour le noyau IWS,
régime gamma_1 = lambda = 0, zeta > 0 (paramètres de référence de l'Annexe F sinon).

Construction (V5.2.1, §crash-test noyau) :
  1. Deux préhistoires symétriques H^± = ±h(t) depuis x0 = (H=0, V=0, tau0, P0, A) :
     même lecture (A,H,V,P) à T, traces tau^± = c ± I différentes.
  2. Continuation commune : poussée sur le nœud i* = 0 jusqu'au Kairos.
  3. Vérification : classements de similarité -> ensembles sélectionnés différents -> A1+ != A2+.
  4. Vérification C23^act : depuis l'état post-cascade, la dérivée de V (qui ne dépend pas de tau)
     diffère selon le graphe, donc la réponse interne de x^(1) n'est pas dans Rep(A2+).

Statut : contrôle numérique de faisabilité [NUM], pas une preuve.
"""
import numpy as np

# ---------------- Paramètres (Annexe F), avec gamma_1 = lambda = 0 ----------------
d = 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1, k2, k3 = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5
N = 6
ISTAR = 0

# ---------------- Graphe : i*=0 voisins {1,2,3}, non-voisins {4,5} ----------------
edges = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)]  # (4,5) rend Ã inversible
A0 = np.zeros((N, N), dtype=int)
for i, j in edges:
    A0[i, j] = A0[j, i] = 1


def Atilde(A):
    B = A + np.eye(len(A))
    return B / B.sum(axis=1, keepdims=True)


def closed_nbhd(A, i):
    return frozenset(np.flatnonzero(A[i]).tolist() + [i])


# ---------------- Dynamique continue (gamma_1 = lambda = 0) ----------------
def rhs(state, A, u):
    H, V, tau, P = state
    At = Atilde(A)
    th = np.tanh(At @ H)
    dH = V
    dV = -gamma0 * V - H + zeta * th + u          # tau absent : gamma_1 = lambda = 0
    dtau = alpha * th - beta * tau
    dP = k1 * np.linalg.norm(H, axis=1) + k2 * np.linalg.norm(V, axis=1) - k3 * P
    return (dH, dV, dtau, dP)


def rk4(state, A, ufun, t, dt):
    def add(s, ds, c):
        return tuple(x + c * dx for x, dx in zip(s, ds))
    a1 = rhs(state, A, ufun(t))
    a2 = rhs(add(state, a1, dt / 2), A, ufun(t + dt / 2))
    a3 = rhs(add(state, a2, dt / 2), A, ufun(t + dt / 2))
    a4 = rhs(add(state, a3, dt), A, ufun(t + dt))
    return tuple(x + dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
                 for x, b1, b2, b3, b4 in zip(state, a1, a2, a3, a4))


def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return 0.0 if na == 0 or nb == 0 else float(a @ b / (na * nb))


def kairos(state, A):
    """Saut du noyau (Tome I) pour le plus petit indice au seuil ; départage par l'indice."""
    H, V, tau, P = (x.copy() for x in state)
    A = A.copy()
    i = int(np.flatnonzero(P >= Theta)[0])
    nb = [j for j in range(N) if A[i, j] == 1]
    nn = [j for j in range(N) if j != i and A[i, j] == 0]
    m = min(2, len(nb), len(nn))
    sim = {j: cosine(tau[i], tau[j]) for j in range(N) if j != i}
    rem = sorted(nb, key=lambda j: (sim[j], j))[:m]            # plus faible similarité
    add = sorted(nn, key=lambda j: (-sim[j], j))[:m]           # plus forte similarité
    for j in rem:
        A[i, j] = A[j, i] = 0
    for j in add:
        A[i, j] = A[j, i] = 1
    P[i] = rP * P[i]
    V[i] = rV * V[i]
    return (H, V, tau, P), A, dict(i=i, m=m, sim=sim, removed=rem, added=add)


# ---------------- 1. Préhistoires symétriques ----------------
T = 3.0
amp = 0.2
At0 = Atilde(A0)
w = np.zeros((N, d))
w[1] = w[2] = (0.0, -1.0)                      # écriture voulue sur 1 et 2, rien sur i* ni 3,4,5
v = np.linalg.solve(At0, w)                    # (Ã v) = w  => (Ã h)_{i*} = 0 exactement
phi = lambda t: np.sin(np.pi * t / T) ** 2
dphi = lambda t: (np.pi / T) * np.sin(2 * np.pi * t / T)
ddphi = lambda t: 2 * (np.pi / T) ** 2 * np.cos(2 * np.pi * t / T)


def u_loop(sign):
    def u(t):
        h = amp * phi(t) * v
        return sign * (amp * ddphi(t) * v + gamma0 * amp * dphi(t) * v + h
                       - zeta * np.tanh(At0 @ h))
    return u


# traces communes visées à T : c = e^{-beta T} tau0
c = np.array([[0.30, 0.00],     # i* : aligné sur e1
              [0.30, 0.05],     # 1 : légèrement au-dessus
              [0.30, -0.05],    # 2 : miroir
              [-0.20, 0.10],    # 3 : peu similaire
              [0.10, 0.20],
              [0.10, -0.20]])
tau0 = np.exp(beta * T) * c
P0 = np.zeros(N)
x0 = (np.zeros((N, d)), np.zeros((N, d)), tau0.copy(), P0.copy())

dt = 1e-3
steps = int(round(T / dt))
res = {}
for sign in (+1, -1):
    s, uf, Pmax, umax = x0, u_loop(sign), 0.0, 0.0
    for k in range(steps):
        s = rk4(s, A0, uf, k * dt, dt)
        Pmax = max(Pmax, s[3].max())
        umax = max(umax, np.abs(uf(k * dt)).max())
    res[sign] = dict(state=s, Pmax=Pmax, umax=umax)

sP, sM = res[+1]['state'], res[-1]['state']
print("=== 1. Préhistoires symétriques (T = %.1f) ===" % T)
print("  (Ã v)_{i*} =", (At0 @ v)[ISTAR], " jumeaux i*/1/2 :",
      closed_nbhd(A0, 0) == closed_nbhd(A0, 1) or closed_nbhd(A0, 0) == closed_nbhd(A0, 2))
print("  max P pendant la boucle : +%.4f  -%.4f   (Theta = %.2f)" % (res[1]['Pmax'], res[-1]['Pmax'], Theta))
print("  max |u| pendant la boucle : %.4f" % res[1]['umax'])
for name, idx in (("H", 0), ("V", 1), ("P", 3)):
    print("  écart %s entre branches à T : %.2e" % (name, np.abs(sP[idx] - sM[idx]).max()))
print("  tau^+(T) - tau^-(T) (nœuds 0..5) :\n", np.round(sP[2] - sM[2], 4))

# ---------------- 2. Continuation commune : poussée sur i* ----------------
U = 2.5


def u_cont(t):
    u = np.zeros((N, d))
    u[ISTAR] = (U, 0.0)
    return u


out = {}
for sign, s in ((+1, sP), (-1, sM)):
    t = 0.0
    while s[3].max() < Theta and t < 20:
        s_new = rk4(s, A0, u_cont, t, dt)
        if s_new[3].max() >= Theta:          # raffinement simple du premier contact
            lo, hi = 0.0, dt
            for _ in range(40):
                mid = (lo + hi) / 2
                if rk4(s, A0, u_cont, t, mid)[3].max() >= Theta:
                    hi = mid
                else:
                    lo = mid
            s = rk4(s, A0, u_cont, t, hi)
            t += hi
            break
        s, t = s_new, t + dt
    first = int(np.flatnonzero(s[3] >= Theta)[0])
    post, A_plus, info = kairos(s, A0)
    out[sign] = dict(pre=s, post=post, A=A_plus, info=info, t=t, first=first)

print("\n=== 2. Kairos commun ===")
for sign in (+1, -1):
    o = out[sign]
    print("  branche %+d : t* = %.4f, premier nœud au seuil = %d, m = %d" %
          (sign, o['t'], o['first'], o['info']['m']))
    print("     similarités s(i*,j) :", {j: round(x, 4) for j, x in o['info']['sim'].items()})
    print("     retirés", o['info']['removed'], " ajoutés", o['info']['added'])
print("  écart (H,V,P) pré-saut entre branches : %.2e" %
      max(np.abs(out[1]['pre'][k] - out[-1]['pre'][k]).max() for k in (0, 1, 3)))
A1, A2 = out[1]['A'], out[-1]['A']
print("  A1+ != A2+ :", bool((A1 != A2).any()))

# marge de classement : écart entre le voisin conservé et le suivant, dans chaque branche
for sign in (+1, -1):
    sim = out[sign]['info']['sim']
    ranked = sorted([1, 2, 3], key=lambda j: -sim[j])
    print("  marge de classement branche %+d : %.4f (conservé %d)" %
          (sign, sim[ranked[0]] - sim[ranked[1]], ranked[0]))

# ---------------- 3. Vérification de C23^act ----------------
post1, post2 = out[1]['post'], out[-1]['post']
print("\n=== 3. C23^act ===")
print("  écart (H,V,P) post-cascade : %.2e" %
      max(np.abs(post1[k] - post2[k]).max() for k in (0, 1, 3)))
H = post1[0]
D = Atilde(A1) - Atilde(A2)
print("  ||(Ã1+ - Ã2+) H|| = %.4e" % np.linalg.norm(D @ H))
dV_diff = zeta * (np.tanh(Atilde(A1) @ H) - np.tanh(Atilde(A2) @ H))
print("  ||dV/dt(graphe A1+) - dV/dt(graphe A2+)|| à même (H,V) = %.4e" % np.linalg.norm(dV_diff))

# réponse interne sous une attente u = 0 : x^(1) sous A1+ vs même (H,V,P) sous A2+,
# pour deux traces cachées différentes (tau n'influe pas sur (H,V,P))
zero = lambda t: np.zeros((N, d))


def wait(state, A, Tw=0.5):
    s = state
    for k in range(int(round(Tw / dt))):
        s = rk4(s, A, zero, k * dt, dt)
    return s


r1 = wait(post1, A1)
r2a = wait(post1, A2)                                  # même (H,V,P), même tau, autre graphe
r2b = wait((post1[0], post1[1], post2[2], post1[3]), A2)  # autre tau, autre graphe
print("  écart lecture interne après attente, A1+ vs A2+ : %.4e" %
      max(np.abs(r1[k] - r2a[k]).max() for k in (0, 1, 3)))
print("  même chose avec une autre trace cachée sous A2+ : %.4e (tau ne compense pas)" %
      max(np.abs(r1[k] - r2b[k]).max() for k in (0, 1, 3)))
print("  écart entre les deux traces sous A2+ (doit être ~0) : %.2e" %
      max(np.abs(r2a[k] - r2b[k]).max() for k in (0, 1, 3)))
