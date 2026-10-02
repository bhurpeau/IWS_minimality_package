"""
Obstruction sequentielle (Benoit) : R_0 = S^1 au premier Kairos (verifie),
mais une seule commande constante u=(amp,ang) doit a la fois placer
tau_0(t1) ET tau_0(t2) -- les angles de tau_0 aux PREMIER et DEUXIEME
Kairos -- et ces deux angles ne sont pas des degres de liberte
independants : ils sont tous deux fonctions des 2 MEMES parametres reels
(amp,ang) de U4. Le reachable set conjoint

  R_0^{(1,2)} = { (theta_1(u), theta_2(u)) : u in U4 } subset S^1 x S^1

est donc au plus une sous-variete de DIMENSION 2 dans un tore de dimension
2 -- pas automatiquement tout le tore, meme si chaque marginale (theta_1
seul, theta_2 seul) couvre tout S^1 separement. Si R_0^{(1,2)} laisse un
trou (une combinaison (theta_1*, theta_2*) jamais atteinte alors que
theta_1* et theta_2* sont chacun individuellement atteints), c'est le
type d'obstruction "plus subtile" que Benoit anticipe : pas un defaut
d'angle isole, mais un defaut de pouvoir les realiser SIMULTANEMENT sous
un controle constant.

On cartographie R_0^{(1,2)} sur le temoin N=9, chambre {2,4,6}, puis on
visualise/quantifie les trous.
"""
import sys, numpy as np, time
import sys, pathlib
_SCRIPTS = pathlib.Path(__file__).resolve().parents[1]   # remonte à scripts/
for _sub in ("core", "minimalite_U5_U4_U3", "R0_reachability", "construction_temoin_Q", "utils"):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core_gen import Atilde, rk4_batch, cos_sim, build_A_from_label, d, Theta, rP, rV

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1

mag = 0.3
phi1,phi2,phi3,phi4,phi5,phi6,phi7,phi8 = 15.0,348.0,45.0,5.0,355.0,12.0,200.0,160.0
def tau9_base():
    tau=np.zeros((N9,d))
    tau[0]=mag*np.array([1.0,0.0])
    for k,phi in zip(range(1,9),[phi1,phi2,phi3,phi4,phi5,phi6,phi7,phi8]):
        tau[k]=mag*np.array([np.cos(np.radians(phi)),np.sin(np.radians(phi))])
    return tau
tau0_base = tau9_base()

def jump_batch_grouped(H,V,tau,P,A_cur,N):
    """Comme jump_batch mais gere un batch ou A_cur peut differer d'un
    element a l'autre (regroupe par graphe identique)."""
    G = H.shape[0]
    H2,V2,tau2,P2 = H.copy(),V.copy(),tau.copy(),P.copy()
    A_next = A_cur.copy()
    istars = np.zeros(G, dtype=int)
    for key in {A_cur[g].tobytes() for g in range(G)}:
        idx = np.array([g for g in range(G) if A_cur[g].tobytes()==key])
        Ag = A_cur[idx[0]]
        i2 = np.argmax(P[idx], axis=1)
        istars[idx] = i2
        for istar in np.unique(i2):
            sub = idx[i2==istar]
            nb = [j for j in range(N) if Ag[istar,j]==1]
            nn = [j for j in range(N) if j!=istar and Ag[istar,j]==0]
            m = min(2, len(nb), len(nn))
            tau_i = tau[sub, istar, :]
            if m == 0:
                new_nb = frozenset(nb)
                for g in sub: A_next[g] = build_A_from_label(Ag, istar, new_nb, N)
                continue
            sim_nb = np.stack([cos_sim(tau_i, tau[sub,j,:]) for j in nb], axis=1)
            order_nb = np.argsort(sim_nb, axis=1, kind='stable')
            sim_nn = np.stack([cos_sim(tau_i, tau[sub,j,:]) for j in nn], axis=1)
            order_nn = np.argsort(-sim_nn, axis=1, kind='stable')
            nb_arr, nn_arr = np.array(nb), np.array(nn)
            for pos, g in enumerate(sub):
                removed = set(nb_arr[order_nb[pos,:m]].tolist())
                added = set(nn_arr[order_nn[pos,:m]].tolist())
                new_nb = frozenset((set(nb)-removed)|added)
                A_next[g] = build_A_from_label(Ag, istar, new_nb, N)
            P2[sub, istar] = rP*P[sub, istar]
            V2[sub, istar] = rV*V[sub, istar]
    return H2,V2,tau2,P2,A_next,istars

def map_R0_sequential(amps, angs, dt=2e-3, Tmax=15.0):
    G = len(amps)
    H = np.zeros((G,N9,d)); V = np.zeros((G,N9,d)); P = np.zeros((G,N9)); P[:,0]=rP*Theta
    tau = np.repeat(tau0_base[None,:,:], G, axis=0)
    A_cur = np.stack([A0.copy()]*G, axis=0)
    Ux = amps*np.cos(np.radians(angs)); Uy = amps*np.sin(np.radians(angs))
    def ufun(t):
        u = np.zeros((G,N9,d)); u[:,0,0]=Ux; u[:,0,1]=Uy; return u
    theta1 = np.full(G, np.nan); theta2 = np.full(G, np.nan)
    alive = np.ones(G, dtype=bool)
    nsteps = int(Tmax/dt)

    for depth in [1,2]:
        # Atilde par graphe (different par element) :
        B = A_cur + np.eye(N9)[None,:,:]
        At_g = B / B.sum(axis=2, keepdims=True)
        done = np.zeros(G, dtype=bool)
        Hs,Vs,taus,Ps = H.copy(),V.copy(),tau.copy(),P.copy()
        t = 0.0
        for step in range(nsteps):
            th = np.tanh(np.einsum('gij,gjd->gid', At_g, H))
            dH = V
            dV = -0.25*V - H + 0.8*th + ufun(t)
            dtau = 0.45*th - 0.12*tau
            dP = 0.6*np.linalg.norm(H,axis=-1) + 0.4*np.linalg.norm(V,axis=-1) - 0.5*P
            # RK4 complet via rk4_batch (reutilise la fonction existante, qui
            # attend un At PARTAGE -- ici on l'appelle noeud par noeud n'est pas
            # necessaire car on a deja le gradient ci-dessus pour un pas Euler;
            # pour rester fidele au reste du chantier on utilise un RK4 simplifie
            # manuel avec At_g (meme formule que rk4_batch, developpee) :
            def rhs(H_,V_,tau_,P_,tt):
                th_ = np.tanh(np.einsum('gij,gjd->gid', At_g, H_))
                dH_ = V_
                dV_ = -0.25*V_ - H_ + 0.8*th_ + ufun(tt)
                dtau_ = 0.45*th_ - 0.12*tau_
                dP_ = 0.6*np.linalg.norm(H_,axis=-1) + 0.4*np.linalg.norm(V_,axis=-1) - 0.5*P_
                return dH_,dV_,dtau_,dP_
            a1 = rhs(H,V,tau,P,t)
            a2 = rhs(H+dt/2*a1[0],V+dt/2*a1[1],tau+dt/2*a1[2],P+dt/2*a1[3],t+dt/2)
            a3 = rhs(H+dt/2*a2[0],V+dt/2*a2[1],tau+dt/2*a2[2],P+dt/2*a2[3],t+dt/2)
            a4 = rhs(H+dt*a3[0],V+dt*a3[1],tau+dt*a3[2],P+dt*a3[3],t+dt)
            H = H+dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0])
            V = V+dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
            tau = tau+dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2])
            P = P+dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
            t += dt
            newly = alive & (~done) & (P.max(axis=1) >= Theta)
            if newly.any():
                Hs[newly]=H[newly]; Vs[newly]=V[newly]; taus[newly]=tau[newly]; Ps[newly]=P[newly]
                done[newly]=True
            if (done | ~alive).all():
                break
        H,V,tau,P = Hs,Vs,taus,Ps
        not_reached = alive & (~done)
        alive[not_reached] = False
        ang_now = np.degrees(np.arctan2(tau[:,0,1], tau[:,0,0])) % 360
        if depth==1: theta1[alive] = ang_now[alive]
        else: theta2[alive] = ang_now[alive]
        active = np.flatnonzero(alive)
        if len(active)==0: break
        H2,V2,tau2,P2,A_next,istars = jump_batch_grouped(H,V,tau,P,A_cur,N9)
        H,V,tau,P,A_cur = H2,V2,tau2,P2,A_next
    return theta1, theta2, alive

# -------------------------------------------------------------- balayage
# (protege par __main__ pour que ce module soit importable sans relancer le
#  balayage -- piege rencontre et corrige en route)
if __name__ == '__main__':
  amps_grid = np.repeat(np.linspace(0.5, 10.0, 24), 90)
  angs_grid = np.tile(np.linspace(0, 356, 90), 24)
  print("Balayage sequentiel : %d protocoles" % len(amps_grid))
  t0=time.time()
  th1, th2, alive = map_R0_sequential(amps_grid, angs_grid)
  print("  (%.1fs)" % (time.time()-t0))
  valid = alive & ~np.isnan(th1) & ~np.isnan(th2)
  print("  %d/%d protocoles valides (atteignent k=2)" % (valid.sum(), len(valid)))

  # grille conjointe 10 deg x 10 deg (36x36) pour visualiser les trous
  G1, G2 = 36, 36
  joint = np.zeros((G1,G2), dtype=int)
  for a,b in zip(th1[valid], th2[valid]):
      i = int(a//10) % G1; j = int(b//10) % G2
      joint[i,j] += 1
  n_empty = (joint==0).sum()
  print("  cases 10x10deg jamais visitees (sur %d) : %d" % (G1*G2, n_empty))

  # marginales : theta1 seul, theta2 seul, couvrent-elles S^1 ?
  b1 = np.zeros(36,dtype=int); b2 = np.zeros(36,dtype=int)
  for a in th1[valid]: b1[int(a//10)%36]+=1
  for b in th2[valid]: b2[int(b//10)%36]+=1
  print("  marginale theta1 : %d/36 cases (10deg) vides" % (b1==0).sum())
  print("  marginale theta2 : %d/36 cases (10deg) vides" % (b2==0).sum())

  if n_empty>0:
      print("\n  Cases conjointes (theta1_bin,theta2_bin) jamais visitees (10deg chacune) :")
      idxs = np.argwhere(joint==0)
      print("   total vide =", len(idxs), "; exemples:", idxs[:20].tolist())
