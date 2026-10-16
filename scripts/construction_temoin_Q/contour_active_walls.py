"""
Experience de contour actif (chambre gardé={1,4,5} a depth3, fenetre site2_bas).
Utilise advance_one_kairos (gestion correcte des scissions) pour les rangs 2,3,
isole la sous-chambre qui revient a nb(0)={1,4,5}, puis pour CETTE sous-chambre
calcule au rang 4 les scores c_1,c_4,c_5 juste avant le saut, construit les trois
champs pairwise et leur region active, et compare au label reel observe.
"""
import sys, time, numpy as np, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (A1_kept1, make_tau_init, Atilde, make_u, rk4_batch,
                              jump_batch, build_A_from_label, cos_sim, Theta, N,
                              initial_group, advance_one_kairos)

phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0

def run_to_kairos_batch(H,V,tau,P,A,dt=2e-3,Tmax=15.0):
    G = H.shape[0]
    At = Atilde(A); ufun = make_u(G)
    done = np.zeros(G, dtype=bool)
    H_snap,V_snap,tau_snap,P_snap = H.copy(),V.copy(),tau.copy(),P.copy()
    nsteps = int(Tmax/dt); t = 0.0
    for step in range(nsteps):
        H,V,tau,P = rk4_batch(H,V,tau,P,At,t,dt,ufun)
        t += dt
        newly = (~done) & (P.max(axis=1) >= Theta)
        if newly.any():
            H_snap[newly]=H[newly]; V_snap[newly]=V[newly]
            tau_snap[newly]=tau[newly]; P_snap[newly]=P[newly]
            done[newly]=True
        if done.all():
            break
    return H_snap,V_snap,tau_snap,P_snap,done

def main():
    t0=time.time()
    nphi = 140
    phi4_1d = np.linspace(200.0, 228.0, nphi)
    phi5_1d = np.linspace(335.0, 363.0, nphi)
    PHI4, PHI5 = np.meshgrid(phi4_1d, phi5_1d, indexing='ij')
    phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()
    G0 = phi4_flat.size
    print("grille:", nphi, "x", nphi, "=", G0, "points")

    tau_init = make_tau_init(phi4_flat, phi5_flat, phi1_fixed, phi2_fixed, phi3_fixed)
    groups = [initial_group(A1_kept1, tau_init)]
    for depth in (2,3):
        groups, splits = advance_one_kairos(groups, depth, verbose=True)

    # garder seulement la sous-chambre qui revient a nb(0)={1,4,5}
    target = frozenset({1,4,5})
    keep = [g for g in groups if g['path'][-1][1]==target and g['path'][-1][0]==0]
    assert len(keep) >= 1, "sous-chambre {1,4,5} introuvable"
    istars0 = set(g['path'][-1][0] for g in keep)
    print(f"{len(keep)} sous-groupe(s) retrouvent nb(0)={{1,4,5}} ; total points = {sum(len(g['idx']) for g in keep)}")

    idx_all = np.concatenate([g['idx'] for g in keep])
    H = np.concatenate([g['H'] for g in keep], axis=0)
    V = np.concatenate([g['V'] for g in keep], axis=0)
    tau = np.concatenate([g['tau'] for g in keep], axis=0)
    P = np.concatenate([g['P'] for g in keep], axis=0)
    A_common = keep[0]['A']
    for g in keep[1:]:
        assert np.array_equal(g['A'], A_common), "graphes differents malgre meme label -- inattendu"
    print("nb(0) =", sorted(j for j in range(N) if A_common[0,j]==1))

    # rang 4 : avancer jusqu'au contact, extraire scores AVANT saut
    Hs,Vs,taus,Ps,done = run_to_kairos_batch(H,V,tau,P,A_common)
    assert done.all(), "stagnation a depth=4"
    istars = np.argmax(Ps, axis=1)
    istar_vals, istar_counts = np.unique(istars, return_counts=True)
    print("i* au rang 4 (valeurs, comptes) :", list(zip(istar_vals.tolist(), istar_counts.tolist())))
    istar = int(istar_vals[np.argmax(istar_counts)])
    frac_common = (istars==istar).mean()
    print(f"i*={istar} partage par {frac_common*100:.2f}% des points de cette sous-chambre")

    nb = [j for j in range(N) if A_common[istar,j]==1]
    nn = [j for j in range(N) if j!=istar and A_common[istar,j]==0]
    m = min(2, len(nb), len(nn))
    print("nb =", nb, " nn =", nn, " m =", m)

    tau_i = taus[:, istar, :]
    scores = {j: cos_sim(tau_i, taus[:,j,:]) for j in nb}

    H4,V4,tau4,P4, labels4, i2_4 = jump_batch(Hs,Vs,taus,Ps,A_common)
    lab_arr = np.empty(len(idx_all), dtype=object)
    for g_ in range(len(idx_all)): lab_arr[g_] = labels4[g_]
    uniq_true = sorted(set(lab_arr.tolist()), key=lambda s: sorted(s))
    print("labels reels observes a depth4 (sous-chambre) :", [sorted(u) for u in uniq_true])
    lab_id_sub = np.array([uniq_true.index(l) for l in lab_arr])

    # reconstruire sur grille pleine (nphi x nphi), NaN hors sous-chambre
    full_scores = {j: np.full(G0, np.nan) for j in nb}
    for j in nb: full_scores[j][idx_all] = scores[j]
    full_lab = np.full(G0, -1, dtype=int)
    full_lab[idx_all] = lab_id_sub
    full_istar_ok = np.zeros(G0, dtype=bool)
    full_istar_ok[idx_all] = (istars==istar)

    out = dict(PHI4=PHI4, PHI5=PHI5, nb=nb, nn=nn, m=m, istar=istar,
               scores={j: full_scores[j].reshape(nphi,nphi) for j in nb},
               lab_id=full_lab.reshape(nphi,nphi), uniq_true=uniq_true,
               istar_ok=full_istar_ok.reshape(nphi,nphi),
               in_chamber=np.isin(np.arange(G0), idx_all).reshape(nphi,nphi))
    with open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/contour_active_walls.pkl','wb') as f:
        pickle.dump(out, f)
    print(f"Sauvegarde. ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
