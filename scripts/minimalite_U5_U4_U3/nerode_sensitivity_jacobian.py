import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
"""
Test de sensibilite local (Benoit) : au lieu d'un scan aveugle de paires, on
calcule directement le Jacobien du score de decision K* par rapport au
controle, noeud par noeud, pour reperer une direction de mur g_ij=0 que le
noeud 0 ne peut pas exciter mais qu'un autre noeud peut.

Definition retenue pour un mur, a un Kairos donne (i* fixe, candidats
nb(i*)/nn(i*) fixes par la trajectoire de reference) :
  - mur de RETRAIT : les candidats au retrait sont les nb(i*) les moins
    similaires a tau_i* ; le mur pertinent est entre le m-ieme et le
    (m+1)-ieme candidat (classement croissant) -- c'est la frontiere qui
    decide si le m-ieme ou le (m+1)-ieme nb est retire.
    g_retrait(k) = sim_nb[rank m-1] - sim_nb[rank m]
  - mur d'AJOUT : symetrique, nn(i*) classes par similarite decroissante,
    g_ajout(k) = sim_nn[rank m-1] - sim_nn[rank m]

Jacobien J^(r)_{.,k} = d g(k) / d(u_{r,x}, u_{r,y}), calcule par difference
centree (perturbation +-eps autour d'un controle de reference, le noeud 0
force en permanence a une amplitude generique, les autres noeuds a zero sauf
le noeud r perturbe).

But : trouver (k, mur, r!=0) tel que |J^(0)| ~ 0 (le noeud 0 n'a aucune prise
locale sur ce mur) alors que |J^(r)| est significatif -- ce serait la
signature recherchee par Benoit d'une vraie difference de pouvoir separant
entre U4 et U3, pas seulement de vitesse.
"""
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core_gen import (Atilde, rhs_batch, rk4_batch, cos_sim,
                                   build_A_from_label, d, Theta, rP, rV)

N6 = 6
with open(_lp('nerode_pairs.pkl'), 'rb') as f:
    saved = pickle.load(f)
A1_6 = saved['A1_6']
mag = 0.3

def tau6_generic(angles5):
    tau = np.zeros((N6, d))
    tau[0] = mag*np.array([1.0, 0.0])
    for k in range(5):
        tau[k+1] = mag*np.array([np.cos(np.radians(angles5[k])), np.sin(np.radians(angles5[k]))])
    return tau

def run_to_k_diagnostics(A0, tau0, N, ufun, k_target, dt=2e-3, Tmax=15.0):
    """Simule une seule trajectoire jusqu'au k_target-ieme Kairos ; a chaque
    Kairos, enregistre (i*, nb classes, sim_nb classes, nn classes, sim_nn
    classes) puis applique le meme recablage que le reste du code (regle du
    m=min(2,|nb|,|nn|)). Retourne la liste des diagnostics, un par Kairos."""
    H = np.zeros((1,N,d)); V = np.zeros((1,N,d)); P = np.zeros((1,N)); P[0,0] = rP*Theta
    tau = tau0.copy()[None,:,:]
    A = A0.copy()
    diags = []
    for depth in range(1, k_target+1):
        At = Atilde(A, N)
        nsteps = int(Tmax/dt)
        reached = False
        for step in range(nsteps):
            t = step*dt
            H,V,tau,P = rk4_batch(H,V,tau,P,At,t,dt,ufun)
            if P[0].max() >= Theta:
                reached = True
                break
        if not reached:
            return diags, False
        istar = int(np.argmax(P[0]))
        nb = [j for j in range(N) if A[istar,j]==1]
        nn = [j for j in range(N) if j!=istar and A[istar,j]==0]
        tau_i = tau[0,istar,:]
        sim_nb = np.array([cos_sim(tau_i, tau[0,j,:]) for j in nb]) if nb else np.array([])
        sim_nn = np.array([cos_sim(tau_i, tau[0,j,:]) for j in nn]) if nn else np.array([])
        order_nb = np.argsort(sim_nb, kind='stable') if len(nb) else np.array([], dtype=int)
        order_nn = np.argsort(-sim_nn, kind='stable') if len(nn) else np.array([], dtype=int)
        m = min(2, len(nb), len(nn))
        diags.append(dict(depth=depth, istar=istar, nb=nb, nn=nn,
                           sim_nb_sorted=sim_nb[order_nb] if len(nb) else sim_nb,
                           sim_nn_sorted=sim_nn[order_nn] if len(nn) else sim_nn,
                           m=m))
        # recablage reel (meme regle que jump_batch) pour poursuivre la trajectoire
        if m == 0:
            new_nb = frozenset(nb)
        else:
            removed = set(np.array(nb)[order_nb[:m]].tolist()) if len(nb) else set()
            added = set(np.array(nn)[order_nn[:m]].tolist()) if len(nn) else set()
            new_nb = frozenset((set(nb) - removed) | added)
            P[0,istar] = rP*P[0,istar]; V[0,istar] = rV*V[0,istar]
        A = build_A_from_label(A, istar, new_nb, N)
    return diags, True

def g_wall(diag, wall):
    m = diag['m']
    if m == 0:
        return None
    if wall == 'retrait':
        s = diag['sim_nb_sorted']
        if len(s) <= m: return None
        return float(s[m-1] - s[m])
    else:
        s = diag['sim_nn_sorted']
        if len(s) <= m: return None
        return float(s[m-1] - s[m])

def make_ufun(baseline_node, baseline_u, pert_node, pert_u):
    def ufun(t):
        u = np.zeros((1, N6, d))
        u[0, baseline_node] = baseline_u
        if pert_node is not None:
            u[0, pert_node] = u[0, pert_node] + np.array(pert_u)
        return u
    return ufun

def jacobian_at(A1, tau0, N, k_target, wall, node_r, baseline_node=0,
                 baseline_u=(2.0,1.0), eps=0.05):
    """Difference centree de g_wall au k_target-ieme Kairos, par rapport aux
    deux composantes du controle au noeud node_r (en plus du controle de
    reference au noeud baseline_node, actif en permanence)."""
    def g_for(pert_u):
        ufun = make_ufun(baseline_node, baseline_u, node_r, pert_u)
        diags, ok = run_to_k_diagnostics(A1, tau0, N, ufun, k_target)
        if not ok or len(diags) < k_target:
            return None
        return g_wall(diags[k_target-1], wall)
    g_px = g_for((eps, 0.0)); g_mx = g_for((-eps, 0.0))
    g_py = g_for((0.0, eps)); g_my = g_for((0.0, -eps))
    if None in (g_px, g_mx, g_py, g_my):
        return None
    return ((g_px-g_mx)/(2*eps), (g_py-g_my)/(2*eps))

# ---------------------------------------------------------------- experience
base = [80.0, 160.0, 250.0, 310.0, 30.0]
tau0 = tau6_generic(base)

print("Jacobien J^(r)_{mur,k} = d g_mur(k) / d(u_r,x, u_r,y)")
print("Controle de reference permanent : noeud 0, amplitude (2.0, 1.0)")
print("Recherche : |J^(0)| petit, |J^(r)| grand pour un r != 0\n")

t0 = time.time()
found = []
for k_target in range(1, 6):
    for wall in ['retrait', 'ajout']:
        js = {}
        for r in range(N6):
            j = jacobian_at(A1_6, tau0, N6, k_target, wall, r)
            js[r] = j
        line = "k=%d mur=%-8s : " % (k_target, wall)
        line += " | ".join("r=%d:(% .3f,% .3f)" % (r, js[r][0], js[r][1]) if js[r] is not None
                            else "r=%d:None" % r for r in range(N6))
        print(line)
        j0 = js[0]
        if j0 is not None:
            n0 = np.hypot(*j0)
            for r in range(1, N6):
                jr = js[r]
                if jr is None: continue
                nr = np.hypot(*jr)
                if n0 < 0.02 and nr > 0.15:
                    found.append((k_target, wall, r, n0, nr))

print("\n(%.1fs)" % (time.time()-t0))
if found:
    print("\nCandidats directionnels trouves (|J0|<0.02, |Jr|>0.15) :")
    for k_target, wall, r, n0, nr in found:
        print("  k=%d mur=%s r=%d : |J0|=%.4f |Jr|=%.4f" % (k_target, wall, r, n0, nr))
else:
    print("\nAucune direction ou le noeud 0 est localement aveugle alors qu'un "
          "autre noeud voit clairement le mur, sur cette configuration/depth testees.")
