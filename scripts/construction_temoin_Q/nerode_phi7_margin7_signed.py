"""
Correction du script precedent (nerode_phi7_margins_k2.py) : la statistique
"margin_event = min(margin_nb,margin_nn) par trajectoire" melange un ecart qui
peut etre non pertinent (le seuil interne d'une trajectoire, meme quand le
noeud qui varie n'est pas pres de ce seuil-la) avec le vrai mecanisme causal.

Fait structurel utilise ici (verifie numeriquement ci-dessous) : dans ce
regime (gamma_1=lambda=0), l'EDO de tau est decouplee noeud par noeud et ne
depend de H que via th_i(H) -- commun a x et x' tant que le graphe A_cur est
identique. Donc tau_j(t) est EXACTEMENT identique entre x et x' pour tout
noeud j != 7 (le noeud perturbe), a tout instant, tant que les deux
trajectoires partagent le meme graphe. Le seul canal de difference, a
n'importe quel Kairos, est la position du noeud 7 dans le classement des
cosinus -- s'il n'est candidat (dans nb ou nn de i*) a aucun Kairos, x et x'
ne peuvent JAMAIS se separer.

Ici (chambre A1={1,4,5} ou {2,4,5}, istar2=0, nb=A1 (ne contient pas 7),
nn=le reste (contient 7)) : le noeud 7 est TOUJOURS dans nn, jamais dans nb.
Donc le canal pertinent est uniquement le seuil d'AJOUT (addition), et la
marge causale correcte est :
    margin7(x) = sim_nn(tau_0,tau_7 ; x) - seuil(x)
ou seuil(x) = m-ieme plus grande similarite PARMI LES AUTRES candidats de nn
(hors noeud 7) -- cette valeur est IDENTIQUE pour x et x' puisqu'elle ne
depend que de noeuds != 7. Le noeud 7 est ajoute (rentre dans le nouveau
voisinage) ssi margin7 > 0.
Separation a k=2  <=>  signe(margin7(x)) != signe(margin7(x')).
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

K_MAX = 4

def Atilde_batched(A_batch, N):
    B = A_batch + np.eye(N)[None,:,:]
    return B / B.sum(axis=2, keepdims=True)

def rhs_batch_g(H,V,tau,P,At_g,u):
    th = np.tanh(np.einsum('gij,gjd->gid', At_g, H))
    dH = V
    dV = -gamma0*V - H + zeta*th + u
    dtau = alpha*th - beta*tau
    dP = k1c*np.linalg.norm(H,axis=-1) + k2c*np.linalg.norm(V,axis=-1) - k3c*P
    return dH,dV,dtau,dP

def rk4_batch_g(H,V,tau,P,At_g,t,dt,ufun):
    a1 = rhs_batch_g(H,V,tau,P,At_g,ufun(t))
    a2 = rhs_batch_g(H+dt/2*a1[0],V+dt/2*a1[1],tau+dt/2*a1[2],P+dt/2*a1[3],At_g,ufun(t+dt/2))
    a3 = rhs_batch_g(H+dt/2*a2[0],V+dt/2*a2[1],tau+dt/2*a2[2],P+dt/2*a2[3],At_g,ufun(t+dt/2))
    a4 = rhs_batch_g(H+dt*a3[0],V+dt*a3[1],tau+dt*a3[2],P+dt*a3[3],At_g,ufun(t+dt))
    H2=H+dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0]); V2=V+dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
    tau2=tau+dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2]); P2=P+dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
    return H2,V2,tau2,P2

def run_pair_family_margin7(A1, N, tau_x, tau_xp, protocols, K=K_MAX, dt=2e-3, Tmax=15.0, moving_node=7):
    M = len(protocols)
    nodes = np.array([p[0] for p in protocols])
    Ux = np.array([p[1] for p in protocols], dtype=float)
    Uy = np.array([p[2] for p in protocols], dtype=float)

    G = 2*M
    nodes_full = np.concatenate([nodes, nodes])
    Ux_full = np.concatenate([Ux, Ux])
    Uy_full = np.concatenate([Uy, Uy])

    H = np.zeros((G,N,d)); V = np.zeros((G,N,d)); P = np.zeros((G,N))
    tau = np.zeros((G,N,d))
    tau[:M] = tau_x[None,:,:]
    tau[M:] = tau_xp[None,:,:]
    P[:,0] = rP*Theta

    A_cur = np.stack([A1.copy()]*G, axis=0)
    path = [tuple() for _ in range(G)]
    alive = np.ones(G, dtype=bool)
    first_divergence = [None]*M

    margin7 = np.full(G, np.nan)      # signed margin (>0 => moving_node ajoute)
    side7 = np.full(G, '', dtype=object)  # 'nb' ou 'nn'
    istar2_rec = np.full(G, -1, dtype=int)
    n_diff_check = np.full(G, -1, dtype=int)  # sanity : nb de candidats dont sim(x) != sim(x') (devrait etre <=1)

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
            H,V,tau,P = rk4_batch_g(H,V,tau,P,At_g,t,dt,ufun)
            t += dt
            newly = alive & (~done) & (P.max(axis=1) >= Theta)
            if newly.any():
                Hs[newly]=H[newly]; Vs[newly]=V[newly]; taus[newly]=tau[newly]; Ps[newly]=P[newly]
                done[newly] = True
            if (done | ~alive).all():
                break
        H,V,tau,P = Hs,Vs,taus,Ps
        not_reached = alive & (~done)
        if not_reached.any():
            for g in np.flatnonzero(not_reached):
                path[g] = path[g] + (('dagger', depth),)
            alive[not_reached] = False

        active = np.flatnonzero(alive)
        if len(active) == 0:
            break

        # cf. erratum nerode_separating_families.py : grouper UNE SEULE FOIS sur l'etat
        # d'avant tout saut de cette profondeur (jamais re-scanner A_cur en cours de mutation).
        groups_map = {}
        for g in active:
            groups_map.setdefault(A_cur[g].tobytes(), []).append(g)
        for key_bytes, idxs_list in groups_map.items():
            idxs = np.array(idxs_list)
            Ag = A_cur[idxs[0]].copy()

            if depth == 2:
                i2_loc = np.argmax(P[idxs], axis=1)
                for istar in np.unique(i2_loc):
                    sub = idxs[i2_loc == istar]
                    nb = [j for j in range(N) if Ag[istar,j]==1]
                    nn = [j for j in range(N) if j!=istar and Ag[istar,j]==0]
                    m_here = min(2, len(nb), len(nn))
                    istar2_rec[sub] = istar
                    if m_here == 0 or moving_node == istar:
                        continue
                    tau_i = tau[sub, istar, :]
                    cands = nb + nn
                    sims = {j: cos_sim(tau_i, tau[sub, j, :]) for j in cands}
                    # sanity: combien de candidats varient entre x et x' dans ce sous-groupe
                    # (seulement mesurable si sub contient a la fois des indices <M et >=M issus
                    #  du MEME protocole -- ici on compare plutot, pour chaque element, sa propre
                    #  position ; le check croise x vs x' est fait plus bas apres coup)
                    if moving_node in nb:
                        side = 'nb'
                        sim_nb = np.stack([sims[j] for j in nb], axis=1)
                        others = [j for j in nb if j != moving_node]
                        sim_others = np.stack([sims[j] for j in others], axis=1) if others else np.zeros((len(sub),0))
                        # seuil : m-ieme plus PETITE valeur parmi les autres (ascendant), car ici
                        # le retrait prend les m plus FAIBLES -- moving_node est retire ssi sa
                        # similarite est parmi les m plus faibles de l'ensemble complet, ce qui
                        # equivaut a : sim(moving) < (m-ieme plus petite valeur parmi les autres)
                        if sim_others.shape[1] >= m_here and sim_others.shape[1] > 0:
                            thresh = np.sort(sim_others, axis=1)[:, m_here-1] if sim_others.shape[1]>=m_here else np.full(len(sub), np.nan)
                            margin7[sub] = sims[moving_node] - thresh  # >0 => moving NON retire (garde), <0 => retire
                        side7[sub] = side
                    elif moving_node in nn:
                        side = 'nn'
                        others = [j for j in nn if j != moving_node]
                        sim_others = np.stack([sims[j] for j in others], axis=1) if others else np.zeros((len(sub),0))
                        if sim_others.shape[1] >= m_here and sim_others.shape[1] > 0:
                            thresh = -np.sort(-sim_others, axis=1)[:, m_here-1]  # m-ieme plus GRANDE parmi les autres
                            margin7[sub] = sims[moving_node] - thresh  # >0 => moving AJOUTE
                        side7[sub] = side

            H2,V2,tau2,P2, labs, i2s = jump_batch(H[idxs],V[idxs],tau[idxs],P[idxs],Ag,N)
            H[idxs],V[idxs],tau[idxs],P[idxs] = H2,V2,tau2,P2
            for pos,g in enumerate(idxs):
                path[g] = path[g] + ((int(i2s[pos]), labs[pos]),)
                A_cur[g] = build_A_from_label(Ag, int(i2s[pos]), labs[pos], N)

        for m in range(M):
            if first_divergence[m] is None and path[m] != path[M+m]:
                first_divergence[m] = depth

    return (first_divergence, margin7[:M], margin7[M:], side7[:M], istar2_rec[:M],
            [tuple(path[m]) for m in range(M)], [tuple(path[M+m]) for m in range(M)])

t0 = time.time()
fd, margin7_x, margin7_xp, side7, istar2, px, pxp = run_pair_family_margin7(A0, N9, tau_x, tau_xp, protocols, K=K_MAX)
print("Calcul termine (%.1fs)" % (time.time()-t0))

chamber1_x  = [p[0][1] if len(p)>0 else None for p in px]
chamber1_xp = [p[0][1] if len(p)>0 else None for p in pxp]
no_leak = np.array([cx==cxp for cx,cxp in zip(chamber1_x, chamber1_xp)])
ks = np.array([k if k is not None else -1 for k in fd])
chambers_key = np.array([tuple(sorted(c)) if c else None for c in chamber1_x], dtype=object)

with open(_lp('phi7_delta60_margin7_signed.pkl'), 'wb') as f:
    pickle.dump(dict(fd=fd, margin7_x=margin7_x, margin7_xp=margin7_xp, side7=side7,
                      istar2=istar2, chamber1_x=chamber1_x, chamber1_xp=chamber1_xp), f)
print("Sauvegarde ->", _lp('phi7_delta60_margin7_signed.pkl'))

# sanity check central : separation a k=2  <=>  signes opposes de margin7
both_valid = no_leak & ~np.isnan(margin7_x) & ~np.isnan(margin7_xp)
sign_flip = np.sign(margin7_x) != np.sign(margin7_xp)
k_is_2 = (ks == 2)
print("\n--- Verification du mecanisme (noeud 7, seuil d'ajout) ---")
print("n points valides (pas de fuite k1, marge definie) :", both_valid.sum())
print("accord signe_oppose <=> k_min==2 :", (sign_flip[both_valid] == k_is_2[both_valid]).mean())
agree_tab = {}
for sf in [True, False]:
    for k2 in [True, False]:
        agree_tab[(sf,k2)] = int((both_valid & (sign_flip==sf) & (k_is_2==k2)).sum())
print("table (sign_flip, k_min==2) -> compte :", agree_tab)

print("\n--- |margin7| (cote x) par categorie, par chambre ---")
for chamber in [(1,4,5),(2,4,5)]:
    mask = both_valid & (chambers_key == chamber)
    if mask.sum()==0: continue
    print(" Chambre", chamber, "n=", mask.sum())
    for key,sel in [("non-sep", ks==-1), ("k2", ks==2), ("k3p", ks>=3)]:
        sub = mask & sel
        if sub.sum()==0: continue
        absmin = np.minimum(np.abs(margin7_x[sub]), np.abs(margin7_xp[sub]))
        print("   %-8s n=%3d  |margin7|_min moy=%.4f std=%.4f [min=%.4f max=%.4f]" %
              (key, sub.sum(), absmin.mean(), absmin.std(), absmin.min(), absmin.max()))
