"""
Benoit : generaliser m_7 a tous les rangs r=1,2,...,K tant que x,x' n'ont pas
encore divergé (meme chemin structurel), et tester la conjecture
    k_min = min{r : m_7^(r)(x) * m_7^(r)(x') < 0}
sur l'ensemble des 800 protocoles (pas seulement les deux chambres separantes
deja etudiees -- y compris la fuite a k=1, qui est exactement le meme
mecanisme au rang r=1).

Argument structurel (etabli analytiquement, deja verifie a r=2) : tant que
x,x' partagent le meme graphe A_cur, (H,V,P) sont EXACTEMENT identiques (ne
dependent jamais de tau), et dtau_j/dt = alpha*th_j(H) - beta*tau_j est
lineaire, decouplee noeud par noeud, avec meme second membre pour x et x'
des que j!=7 -- donc tau_j(t) est EXACTEMENT identique entre x et x' pour
tout j!=7, a tout instant, tant que le graphe est partage. Consequence : a
CHAQUE Kairos tant que x,x' n'ont pas encore diverge, le seul candidat dont
le score peut differer entre x et x' est le noeud 7 (sauf si istar lui-meme
est le noeud 7 -- cas different, traite a part ci-dessous).

Convention ties : le noyau utilise np.argsort(..., kind='stable') -- en cas
d'egalite EXACTE, l'ordre d'indice d'origine (croissant) l'emporte. On
applique la meme regle ici et on compte les ties rencontres (devrait etre 0
generiquement sur une grille de floats).
"""
import sys, pickle, pathlib, time
import numpy as np

_HERE = pathlib.Path(__file__).resolve().parent
def _lp(name): return str(_HERE / name)
sys.path.insert(0, str(_HERE))

from iws_kairos_core_gen import d, Theta, rP, rV, zeta, alpha, beta, gamma0, k1c, k2c, k3c, cos_sim, build_A_from_label, jump_batch

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi8_fixed = np.radians(160.0)
phi2_c, phi6_c = 348.0, 12.0

def tau9_pert7(phi7_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_c)), np.sin(np.radians(phi2_c))])
    tau[3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
    tau[4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
    tau[5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_c)), np.sin(np.radians(phi6_c))])
    tau[7] = mag*np.array([np.cos(np.radians(phi7_deg)), np.sin(np.radians(phi7_deg))])
    tau[8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])
    return tau

amps_grid = np.load(_lp('phi7_amps.npy')); angs_grid = np.load(_lp('phi7_angs.npy'))
protocols = [(0, a*np.cos(np.radians(g)), a*np.sin(np.radians(g))) for a,g in zip(amps_grid,angs_grid)]

delta = 60.0
tau_x  = tau9_pert7(200.0)
tau_xp = tau9_pert7(200.0+delta)

K_MAX = 7
MOVING = 7

def Atilde_batched(A_batch, N):
    B = A_batch + np.eye(N)[None,:,:]
    return B / B.sum(axis=2, keepdims=True)
def rhs_batch_g(H,V,tau,P,At_g,u):
    th = np.tanh(np.einsum('gij,gjd->gid', At_g, H))
    return V, -gamma0*V - H + zeta*th + u, alpha*th - beta*tau, k1c*np.linalg.norm(H,axis=-1) + k2c*np.linalg.norm(V,axis=-1) - k3c*P
def rk4_batch_g(H,V,tau,P,At_g,t,dt,ufun):
    a1 = rhs_batch_g(H,V,tau,P,At_g,ufun(t))
    a2 = rhs_batch_g(H+dt/2*a1[0],V+dt/2*a1[1],tau+dt/2*a1[2],P+dt/2*a1[3],At_g,ufun(t+dt/2))
    a3 = rhs_batch_g(H+dt/2*a2[0],V+dt/2*a2[1],tau+dt/2*a2[2],P+dt/2*a2[3],At_g,ufun(t+dt/2))
    a4 = rhs_batch_g(H+dt*a3[0],V+dt*a3[1],tau+dt*a3[2],P+dt*a3[3],At_g,ufun(t+dt))
    H2=H+dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0]); V2=V+dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
    tau2=tau+dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2]); P2=P+dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
    return H2,V2,tau2,P2

def run_margin_sequence(A1, N, tau_x, tau_xp, protocols, K=K_MAX, dt=2e-3, Tmax=15.0, moving_node=MOVING):
    M = len(protocols)
    nodes = np.array([p[0] for p in protocols])
    Ux = np.array([p[1] for p in protocols], dtype=float)
    Uy = np.array([p[2] for p in protocols], dtype=float)
    G = 2*M
    nodes_full = np.concatenate([nodes, nodes]); Ux_full = np.concatenate([Ux, Ux]); Uy_full = np.concatenate([Uy, Uy])

    H = np.zeros((G,N,d)); V = np.zeros((G,N,d)); P = np.zeros((G,N))
    tau = np.zeros((G,N,d)); tau[:M] = tau_x[None,:,:]; tau[M:] = tau_xp[None,:,:]
    P[:,0] = rP*Theta

    A_cur = np.stack([A1.copy()]*G, axis=0)
    path = [tuple() for _ in range(G)]
    alive = np.ones(G, dtype=bool)
    first_divergence = [None]*M

    # historique des marges, par protocole (liste de (r, m_x, m_xp, istar, side, tie))
    margin_hist = [[] for _ in range(M)]
    istar_is_moving_count = 0
    tie_count = 0

    def ufun(t):
        u = np.zeros((G,N,d))
        u[np.arange(G), nodes_full, 0] = Ux_full
        u[np.arange(G), nodes_full, 1] = Uy_full
        return u

    nsteps = int(Tmax/dt)
    for depth in range(1, K+1):
        At_g = Atilde_batched(A_cur, N)
        done = np.zeros(G, dtype=bool)
        Hs,Vs,taus,Ps = H.copy(), V.copy(), tau.copy(), P.copy()
        t = 0.0
        for step in range(nsteps):
            H,V,tau,P = rk4_batch_g(H,V,tau,P,At_g,t,dt,ufun); t += dt
            newly = alive & (~done) & (P.max(axis=1) >= Theta)
            if newly.any():
                Hs[newly]=H[newly]; Vs[newly]=V[newly]; taus[newly]=tau[newly]; Ps[newly]=P[newly]; done[newly]=True
            if (done | ~alive).all(): break
        H,V,tau,P = Hs,Vs,taus,Ps
        not_reached = alive & (~done)
        if not_reached.any():
            for g in np.flatnonzero(not_reached): path[g] = path[g] + (('dagger', depth),)
            alive[not_reached] = False

        active = np.flatnonzero(alive)
        if len(active) == 0: break

        # groupage fige UNE SEULE FOIS (erratum run_pair_family)
        groups_map = {}
        for g in active: groups_map.setdefault(A_cur[g].tobytes(), []).append(g)

        for key_bytes, idxs_list in groups_map.items():
            idxs = np.array(idxs_list)
            Ag = A_cur[idxs[0]].copy()

            # --- marge m_7^(depth), seulement pour les protocoles m dont x ET x'
            # sont TOUS DEUX dans idxs (donc n'ont pas encore diverge) ---
            idx_set = set(idxs.tolist())
            for m_local in range(M):
                if m_local in idx_set and (M+m_local) in idx_set:
                    pass  # traite en bloc plus bas (vectorise), ce test sert juste a filtrer

            # construire le sous-ensemble des paires encore non divergentes dans CE groupe.
            # ATTENTION : partager le meme graphe AU RANG COURANT ne suffit pas -- deux
            # trajectoires qui ont deja diverge PUIS reconverge par coincidence vers le
            # meme graphe (chemins differents, meme resultat) ne partagent plus (H,V,P)
            # depuis la premiere divergence ; on exclut donc explicitement toute paire
            # dont first_divergence est deja connu (fixe a une profondeur anterieure).
            pair_m = np.array([m for m in range(M)
                                if (m in idx_set) and (M+m in idx_set) and first_divergence[m] is None])
            if len(pair_m) > 0:
                sub_x = pair_m; sub_xp = pair_m + M
                i2_loc_all = np.argmax(P[idxs], axis=1)
                i2_map = {int(g): int(i2) for g,i2 in zip(idxs, i2_loc_all)}
                istar_x = np.array([i2_map[g] for g in sub_x])
                istar_xp = np.array([i2_map[g] for g in sub_xp])
                same_istar = istar_x == istar_xp  # doit etre vrai partout (H,V,P partages) ; verifie
                for pos in range(len(pair_m)):
                    m = int(pair_m[pos])
                    istar = int(istar_x[pos])
                    assert istar == istar_xp[pos], "istar differe entre x,x' alors que graphe partage -- inattendu"
                    if istar == moving_node:
                        istar_is_moving_count += 1
                        margin_hist[m].append((depth, np.nan, np.nan, istar, 'istar=moving', False))
                        continue
                    nb = [j for j in range(N) if Ag[istar,j]==1]
                    nn = [j for j in range(N) if j!=istar and Ag[istar,j]==0]
                    m_here = min(2, len(nb), len(nn))
                    if m_here == 0 or moving_node not in nb+nn:
                        margin_hist[m].append((depth, np.nan, np.nan, istar, 'n/a', False))
                        continue
                    gx, gxp = int(sub_x[pos]), int(sub_xp[pos])
                    tau_i_x = tau[gx, istar, :]; tau_i_xp = tau[gxp, istar, :]
                    def _cs(a, b):
                        return float((a*b).sum()/(np.linalg.norm(a)*np.linalg.norm(b)+1e-15))
                    if moving_node in nb:
                        side = 'nb'
                        others = [j for j in nb if j != moving_node]
                        so_x  = np.array([_cs(tau_i_x,  tau[gx, j,:])  for j in others])
                        sv_x  = _cs(tau_i_x,  tau[gx, moving_node,:])
                        sv_xp = _cs(tau_i_xp, tau[gxp,moving_node,:])
                        if len(others) >= m_here:
                            thresh = np.sort(so_x)[m_here-1]   # identique pour x,x' (others partages)
                            mx, mxp = sv_x - thresh, sv_xp - thresh
                        else:
                            mx = mxp = np.nan
                    else:
                        side = 'nn'
                        others = [j for j in nn if j != moving_node]
                        so_x  = np.array([_cs(tau_i_x,  tau[gx, j,:])  for j in others])
                        sv_x  = _cs(tau_i_x,  tau[gx, moving_node,:])
                        sv_xp = _cs(tau_i_xp, tau[gxp,moving_node,:])
                        if len(others) >= m_here:
                            thresh = -np.sort(-so_x)[m_here-1]
                            mx, mxp = sv_x - thresh, sv_xp - thresh
                        else:
                            mx = mxp = np.nan
                    tie = bool((not np.isnan(mx)) and abs(mx) < 1e-12)
                    if tie: tie_count += 1
                    margin_hist[m].append((depth, mx, mxp, istar, side, tie))

            H2,V2,tau2,P2, labs, i2s = jump_batch(H[idxs],V[idxs],tau[idxs],P[idxs],Ag,N)
            H[idxs],V[idxs],tau[idxs],P[idxs] = H2,V2,tau2,P2
            for pos,g in enumerate(idxs):
                path[g] = path[g] + ((int(i2s[pos]), labs[pos]),)
                A_cur[g] = build_A_from_label(Ag, int(i2s[pos]), labs[pos], N)

        for m in range(M):
            if first_divergence[m] is None and path[m] != path[M+m]:
                first_divergence[m] = depth

    print("istar == moving_node rencontre %d fois (sur toutes les paires/profondeurs confondues)" % istar_is_moving_count)
    print("ties exacts rencontres : %d" % tie_count)
    return first_divergence, margin_hist

t0 = time.time()
fd, margin_hist = run_margin_sequence(A0, N9, tau_x, tau_xp, protocols, K=K_MAX)
print("Calcul termine (%.1fs)" % (time.time()-t0))

with open(_lp('phi7_delta60_margin7_sequence.pkl'), 'wb') as f:
    pickle.dump(dict(fd=fd, margin_hist=margin_hist), f)
print("Sauvegarde ->", _lp('phi7_delta60_margin7_sequence.pkl'))

# ---- test de la conjecture : k_min = min{r : signe(m_x)!=signe(m_xp)} ----
ks = np.array([k if k is not None else -1 for k in fd])
n_total = len(fd)
n_tested = 0; n_match = 0; n_mismatch = 0; n_undetermined = 0
mismatches = []
for m in range(n_total):
    hist = margin_hist[m]
    pred = None
    undetermined_hit = False
    for (r, mx, mxp, istar, side, tie) in hist:
        if side in ('istar=moving','n/a'):
            undetermined_hit = True
            break  # mecanisme simple non applicable a partir d'ici pour ce protocole
        if np.isnan(mx) or np.isnan(mxp):
            undetermined_hit = True
            break
        if (mx>0) != (mxp>0):
            pred = r
            break
    real = ks[m] if ks[m]>0 else None
    if pred is None and not undetermined_hit:
        pred = None  # jamais de flip observe dans la fenetre K testee -> non separe predit
    if undetermined_hit and pred is None:
        n_undetermined += 1
        continue
    n_tested += 1
    if pred == real:
        n_match += 1
    else:
        n_mismatch += 1
        if len(mismatches) < 15:
            mismatches.append((m, pred, real))

print("\n--- Test de la conjecture k_min = min{r : signe(m_7^(r)) flip} ---")
print("n_total=%d  n_tested(mecanisme simple applicable)=%d  n_undetermined(istar=7 ou n/a rencontre avant tout flip)=%d"
      % (n_total, n_tested, n_undetermined))
print("accord = %.4f%% (%d/%d)" % (100*n_match/n_tested if n_tested else 0, n_match, n_tested))
if mismatches:
    print("exemples de desaccord (protocole, k_pred, k_reel) :", mismatches)
