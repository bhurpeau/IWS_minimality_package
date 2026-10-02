import numpy as np
import time

# ---------------------------------------------------------------------------
# Etape 2 (Benoit) : a l'interieur d'UNE chambre de P_1 (celle ou le noeud 1
# est garde au Kairos 1 : retires={2,3}, ajoutes={4,5}), on integre reellement
# la dynamique de A_1 jusqu'au Kairos 2, et on regarde comment le mur du
# classement au Kairos 2 se dessine dans les MEMES coordonnees (phi1,phi2)
# qu'a l'etape 1 -- pour voir si c'est encore une preimage simple d'une
# egalite de scores, ou deja quelque chose de deforme par le flot.
# ---------------------------------------------------------------------------

N, d = 6, 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1, k2, k3 = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5

edges0 = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
A0 = np.zeros((N, N))
for i, j in edges0:
    A0[i, j] = A0[j, i] = 1

def Atilde(A):
    B = A + np.eye(N)
    return B / B.sum(axis=1, keepdims=True)

# Graphe apres Kairos 1 dans la chambre "garde=1" : (0,2),(0,3) retirees, (0,4),(0,5) ajoutees
A1 = A0.copy()
A1[0, 2] = A1[2, 0] = 0
A1[0, 3] = A1[3, 0] = 0
A1[0, 4] = A1[4, 0] = 1
A1[0, 5] = A1[5, 0] = 1
At1 = Atilde(A1)

def u_cont_batch(t, G, U=2.5):
    u = np.zeros((G, N, d))
    u[:, 0] = (U, 0.0)
    return u

def rhs_batch(H, V, tau, P, A_t, u):
    th = np.einsum('ij,gjd->gid', A_t, H)
    th = np.tanh(th)
    dH = V
    dV = -gamma0 * V - H + zeta * th + u
    dtau = alpha * th - beta * tau
    dP = k1 * np.linalg.norm(H, axis=-1) + k2 * np.linalg.norm(V, axis=-1) - k3 * P
    return dH, dV, dtau, dP

def rk4_batch(H, V, tau, P, A_t, t, dt, G):
    def add(x, dx, c):
        return x + c * dx
    a1 = rhs_batch(H, V, tau, P, A_t, u_cont_batch(t, G))
    a2 = rhs_batch(add(H,a1[0],dt/2), add(V,a1[1],dt/2), add(tau,a1[2],dt/2), add(P,a1[3],dt/2), A_t, u_cont_batch(t+dt/2, G))
    a3 = rhs_batch(add(H,a2[0],dt/2), add(V,a2[1],dt/2), add(tau,a2[2],dt/2), add(P,a2[3],dt/2), A_t, u_cont_batch(t+dt/2, G))
    a4 = rhs_batch(add(H,a3[0],dt), add(V,a3[1],dt), add(tau,a3[2],dt), add(P,a3[3],dt), A_t, u_cont_batch(t+dt, G))
    H2 = H + dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0])
    V2 = V + dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
    tau2 = tau + dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2])
    P2 = P + dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
    return H2, V2, tau2, P2

# --- grille (phi1,phi2) a l'interieur de la chambre "garde=1" (voir figure etape 1) ---
n_grid = 45
phi1_range = np.linspace(1.0, 20.0, n_grid)   # degres, loin des murs phi1=0 et phi1=phi2
phi2_range = np.linspace(25.0, 55.0, n_grid)
PHI1, PHI2 = np.meshgrid(phi1_range, phi2_range, indexing='ij')
G = n_grid * n_grid
phi1_flat = np.radians(PHI1).ravel()
phi2_flat = np.radians(PHI2).ravel()

mag = 0.3
phi3 = 2.0  # rad, comme en etape 1
tau_init = np.zeros((G, N, d))
tau_init[:, 0] = mag * np.array([1.0, 0.0])
tau_init[:, 1] = mag * np.stack([np.cos(phi1_flat), np.sin(phi1_flat)], axis=-1)
tau_init[:, 2] = mag * np.stack([np.cos(phi2_flat), np.sin(phi2_flat)], axis=-1)
tau_init[:, 3] = mag * np.array([np.cos(phi3), np.sin(phi3)])
tau_init[:, 4] = np.array([0.10, 0.20])
tau_init[:, 5] = np.array([-0.10, 0.15])

# verification (sur quelques points) que Kairos 1 donne bien garde=1 partout ici
def cos_sim(a, b):
    na = np.linalg.norm(a, axis=-1); nb = np.linalg.norm(b, axis=-1)
    return (a * b).sum(axis=-1) / (na * nb)
c1 = cos_sim(tau_init[:, 0], tau_init[:, 1])
c2 = cos_sim(tau_init[:, 0], tau_init[:, 2])
c3 = cos_sim(tau_init[:, 0], tau_init[:, 3])
assert np.all((c1 >= c2) & (c1 >= c3)), "hors de la chambre garde=1 !"
print("Chambre garde=1 confirmée sur toute la grille (%d points)." % G)

H = np.zeros((G, N, d)); V = np.zeros((G, N, d))
tau = tau_init.copy()
P = np.zeros((G, N)); P[:, 0] = Theta
# Kairos 1 (deterministe, identique partout dans cette chambre)
P[:, 0] = rP * P[:, 0]
V[:, 0] = rV * V[:, 0]

dt = 2e-3
Tmax = 15.0
nsteps = int(Tmax / dt)
done = np.zeros(G, dtype=bool)
H_snap = H.copy(); V_snap = V.copy(); tau_snap = tau.copy(); P_snap = P.copy()

t0 = time.time()
t = 0.0
for step in range(nsteps):
    H, V, tau, P = rk4_batch(H, V, tau, P, At1, t, dt, G)
    t += dt
    newly = (~done) & (P.max(axis=1) >= Theta)
    if newly.any():
        H_snap[newly] = H[newly]; V_snap[newly] = V[newly]
        tau_snap[newly] = tau[newly]; P_snap[newly] = P[newly]
        done[newly] = True
    if done.all():
        break

print("Temps de calcul : %.1fs (%d pas, %d/%d points terminés)" % (time.time()-t0, step+1, done.sum(), G))
if not done.all():
    print("  ATTENTION : %d points n'ont pas atteint le Kairos 2 avant Tmax=%.1f" % ((~done).sum(), Tmax))

# --- classification au Kairos 2 ---
i2 = np.argmax(P_snap, axis=1)
print("i2* rencontrés :", {int(v): int((i2==v).sum()) for v in np.unique(i2)})

# pour i2*=0 (cas attendu, A1 : voisins de 0 = {1,4,5}, non-voisins = {2,3})
nb0 = [j for j in range(N) if A1[0, j] == 1]
nn0 = [j for j in range(N) if j != 0 and A1[0, j] == 0]
print("  nb(0) dans A1 =", nb0, " nn(0) dans A1 =", nn0)

kept_label = np.full(G, -1, dtype=int)
for g in range(G):
    if i2[g] != 0:
        continue
    sims = {j: cos_sim(tau_snap[g, 0], tau_snap[g, j]) for j in nb0}
    kept = max(sims, key=sims.get)  # m=min(2,3,2)=2 -> un seul retiré parmi 3 -> "kept" = 2 gardés en fait
    # m = min(2, len(nb0)=3, len(nn0)=2) = 2 : on retire 2 des 3 -> UN garde
    order = sorted(sims, key=sims.get)
    removed_here = order[:2]
    kept_node = order[2]
    kept_label[g] = kept_node

vals, counts = np.unique(kept_label, return_counts=True)
print("  classification (nœud gardé parmi nb(0) au Kairos 2) :", dict(zip(vals.tolist(), counts.tolist())))

np.save("/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/depth2_grid.npy",
        dict(PHI1=PHI1, PHI2=PHI2, kept_label=kept_label.reshape(n_grid, n_grid), i2=i2.reshape(n_grid, n_grid)),
        allow_pickle=True)
print("Grille sauvegardée pour tracé.")
