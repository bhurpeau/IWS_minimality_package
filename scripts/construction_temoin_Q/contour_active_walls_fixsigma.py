"""
Experience de contour actif, cas structurel Fix(sigma).
Temoin N=6, chambre 'garde=3' (A1_kept3, Aut(A1)=4, sigma=(1 2)(4 5)),
tau1=tau2 impose (etat initial dans Fix(sigma)), rang=2 (premier Kairos depuis
A1_kept3), nb(0)={3,4,5}, m=2 (competition de retrait, 1 survivant).
Attendu : le mur g45=c4-c5=0 doit coincider EXACTEMENT avec la diagonale
phi4=phi5 (Fix(sigma)), pas juste la croiser transversalement.
"""
import sys, time, numpy as np, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (A1_kept3, make_tau_init, Atilde, make_u, rk4_batch,
                              jump_batch, build_A_from_label, cos_sim, Theta, N,
                              initial_group, advance_one_kairos, automorphisms)

# tau1 = tau2 EXACTEMENT (Fix(sigma)) : phi1_fixed = phi2_fixed
phi1_fixed = np.radians(10.0)
phi2_fixed = np.radians(10.0)
phi3_fixed = 2.0  # rad, comme dans les experiences precedentes (hors Fix, "loin")

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
    print("Aut(A1_kept3) =", len(automorphisms(A1_kept3)), "elements")
    sigma_candidates = [p for p in automorphisms(A1_kept3) if p!=tuple(range(N))]
    print("non-identite :", sigma_candidates)

    nphi = 160
    phi4_1d = np.linspace(-30.0, 30.0, nphi)
    phi5_1d = np.linspace(-30.0, 30.0, nphi)
    PHI4, PHI5 = np.meshgrid(phi4_1d, phi5_1d, indexing='ij')
    phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()
    G0 = phi4_flat.size
    print("grille:", nphi, "x", nphi, "=", G0, "points, phi1=phi2=10 deg (Fix(sigma))")

    tau_init = make_tau_init(phi4_flat, phi5_flat, phi1_fixed, phi2_fixed, phi3_fixed)
    H = np.zeros((G0,N,2)); V = np.zeros((G0,N,2)); tau = tau_init.copy()
    P = np.zeros((G0,N)); P[:,0] = 0.35*Theta
    A_common = A1_kept3.copy()

    # rang 2 (premier Kairos depuis A1_kept3) : avancer jusqu'au contact, extraire scores AVANT saut
    Hs,Vs,taus,Ps,done = run_to_kairos_batch(H,V,tau,P,A_common)
    assert done.all(), "stagnation a depth=2"
    istars = np.argmax(Ps, axis=1)
    istar_vals, istar_counts = np.unique(istars, return_counts=True)
    print("i* au rang 2 (valeurs, comptes) :", list(zip(istar_vals.tolist(), istar_counts.tolist())))
    istar = int(istar_vals[np.argmax(istar_counts)])
    print(f"i*={istar} partage par {(istars==istar).mean()*100:.2f}%")

    nb = [j for j in range(N) if A_common[istar,j]==1]
    nn = [j for j in range(N) if j!=istar and A_common[istar,j]==0]
    m = min(2, len(nb), len(nn))
    print("nb =", nb, " nn =", nn, " m =", m)

    tau_i = taus[:, istar, :]
    scores = {j: cos_sim(tau_i, taus[:,j,:]) for j in nb}

    H2,V2,tau2,P2, labels, i2 = jump_batch(Hs,Vs,taus,Ps,A_common)
    lab_arr = np.empty(G0, dtype=object)
    for g_ in range(G0): lab_arr[g_] = labels[g_]
    uniq_true = sorted(set(lab_arr.tolist()), key=lambda s: sorted(s))
    print("labels reels observes a depth2 :", [sorted(u) for u in uniq_true])
    lab_id = np.array([uniq_true.index(l) for l in lab_arr]).reshape(nphi,nphi)

    out = dict(PHI4=PHI4, PHI5=PHI5, nb=nb, nn=nn, m=m, istar=istar,
               scores={j: scores[j].reshape(nphi,nphi) for j in nb},
               lab_id=lab_id, uniq_true=uniq_true, sigma_candidates=sigma_candidates)
    with open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/contour_active_walls_fixsigma.pkl','wb') as f:
        pickle.dump(out, f)
    print(f"Sauvegarde. ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
