"""
Benoit (suite du 4.17) : abandon de la construction ex nihilo p,q,r,s ;
retour a la paire N=9 deja validee (perturbation de phi7, isole dans
{6,7,8}, cf. nerode_n9_u4_vs_u3.py) qui a un vrai phenomene sequentiel :
non separee par le protocole de reference, mais on sait (session precedente)
que U4 dense la separe a k=2 pour certains protocoles.

Puisque la base (phi1..phi6,phi8) de tau9_pert7(200.0) EST EXACTEMENT celle de
nerode_R0_sequential.tau9_base (meme graphe A0, memes 8 angles fixes), et que
le noeud 7 est isole (degre 0) dans A0 -- donc invisible aux dynamiques de
TOUS les autres noeuds jusqu'a ce qu'un saut l'y connecte -- tau_0(t) est
IDENTIQUE entre x=tau9_pert7(200) et x'=tau9_pert7(200+delta) jusqu'au moment
ou leurs CHEMINS (frozenset ajoutes/retires) different reellement. On peut
donc reutiliser map_R0_sequential (qui suit tau_0 a k=1,2) comme les
coordonnees (theta1,theta2) PARTAGEES de ce protocole, et les correler avec
le k_min de separation reel de la paire (x,x').

Question posee (Benoit) : les protocoles separants forment-ils une region
nette de R0^{(1,2)}, dependent-ils surtout de theta2 seul, ou se repartissent-
ils en plusieurs composantes signe d'un chemin structurel intermediaire
different (A1) ?
"""
import sys, numpy as np, time
import pathlib
_SCRIPTS = pathlib.Path(__file__).resolve().parents[1]   # remonte à scripts/
for _sub in ("core", "minimalite_U5_U4_U3", "R0_reachability", "construction_temoin_Q", "utils"):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_separating_families import run_pair_family
from nerode_R0_sequential import map_R0_sequential
from iws_kairos_core_gen import d

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

# ---------------------------------------------------------------- grille
amps_grid = np.repeat(np.linspace(0.5, 10.0, 30), 72)
angs_grid = np.tile(np.linspace(0, 355, 72), 30)
M = len(amps_grid)
print("Grille : %d protocoles" % M)

print("\nEtape A : (theta1,theta2) partages (base = x, phi7=200, deja valable pour x' tant qu'ils ne divergent pas)")
t0=time.time()
theta1, theta2, alive_seq = map_R0_sequential(amps_grid, angs_grid)
print("  (%.1fs)" % (time.time()-t0))

protocols = [(0, a*np.cos(np.radians(g)), a*np.sin(np.radians(g))) for a,g in zip(amps_grid,angs_grid)]

for delta in [10.0, 30.0, 60.0, 90.0, 120.0, 160.0]:
    tau_x  = tau9_pert7(200.0)
    tau_xp = tau9_pert7(200.0+delta)
    t0=time.time()
    fd, px, pxp = run_pair_family(A0, N9, tau_x, tau_xp, protocols, K=4)
    dt_elapsed = time.time()-t0
    ks = np.array([k if k is not None else -1 for k in fd])
    n_sep = (ks>0).sum()
    n_sep_k1 = (ks==1).sum()
    n_sep_k2 = (ks==2).sum()
    n_sep_k3p = ((ks>=3)).sum()
    print("delta=%6.1f : %d/%d separent (k=1:%d k=2:%d k>=3:%d)  (%.1fs)"
          % (delta, n_sep, M, n_sep_k1, n_sep_k2, n_sep_k3p, dt_elapsed))
    if n_sep>0 and n_sep_k1==0:
        # cas interessant : separation retardee (jamais a k=1), on regarde ou
        sep_mask = ks>0
        valid = alive_seq & ~np.isnan(theta1) & ~np.isnan(theta2) & sep_mask
        novalid = alive_seq & ~np.isnan(theta1) & ~np.isnan(theta2) & ~sep_mask
        print("    -> parmi les %d valides (theta1,theta2 definis) : %d separent, %d non"
              % (valid.sum()+novalid.sum(), valid.sum(), novalid.sum()))
        if valid.sum()>0:
            print("    theta1[separent]  : min=%.1f max=%.1f median=%.1f" % (theta1[valid].min(), theta1[valid].max(), np.median(theta1[valid])))
            print("    theta2[separent]  : min=%.1f max=%.1f median=%.1f" % (theta2[valid].min(), theta2[valid].max(), np.median(theta2[valid])))
        if novalid.sum()>0:
            print("    theta1[non-sep]   : min=%.1f max=%.1f median=%.1f" % (theta1[novalid].min(), theta1[novalid].max(), np.median(theta1[novalid])))
            print("    theta2[non-sep]   : min=%.1f max=%.1f median=%.1f" % (theta2[novalid].min(), theta2[novalid].max(), np.median(theta2[novalid])))
        np.save('phi7_delta%d_ks.npy' % int(delta), ks)
