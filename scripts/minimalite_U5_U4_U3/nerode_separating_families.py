"""
Chantier "familles separantes" (Benoit) : pour des paires de reference
x,x' in F_y deja connues pour etre interessantes genealogiquement, on teste
si des familles de protocoles de plus en plus restreintes U5 subset U4
subset U3 suffisent encore a les separer (x not-equiv_k x' pour un k<=K),
ou si la separation se perd.

ATTENTION (garde-fou de Benoit) : on instrumente des sous-familles FINIES
et PARAMETREES de ces classes, jamais M lui-meme. Un "non separe jusqu'a K"
numerique n'est jamais une preuve de non-separabilite -- seulement une
indication a expliquer mecaniquement si elle resiste.

Version vectorisee : chaque element du batch peut porter un graphe A
DIFFERENT (At de forme (G,N,N)), ce qui permet de traiter TOUT un batch
(plusieurs protocoles x deux etats x) en une seule passe RK4 vectorisee,
meme apres que certaines branches aient diverge structurellement.
"""
import sys, numpy as np, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core_gen import (automorphisms, jump_batch, build_A_from_label,
                                  d, Theta, rP, rV, zeta, alpha, beta, gamma0, k1c, k2c, k3c)

K_MAX = 7

def Atilde_batched(A_batch, N):
    # A_batch : (G,N,N) -> At_batch : (G,N,N)
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

def run_pair_family(A1, N, tau_x, tau_xp, protocols, K=K_MAX, dt=2e-3, Tmax=15.0, verbose=False):
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

    A_cur = np.stack([A1.copy()]*G, axis=0)  # (G,N,N)
    path = [tuple() for _ in range(G)]
    alive = np.ones(G, dtype=bool)
    first_divergence = [None]*M

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
        # saut : jump_batch suppose un seul graphe -> on groupe par graphe identique
        for key_bytes in {A_cur[g].tobytes() for g in active}:
            idxs = np.array([g for g in active if A_cur[g].tobytes() == key_bytes])
            Ag = A_cur[idxs[0]]
            H2,V2,tau2,P2, labs, i2s = jump_batch(H[idxs],V[idxs],tau[idxs],P[idxs],Ag,N)
            H[idxs],V[idxs],tau[idxs],P[idxs] = H2,V2,tau2,P2
            for pos,g in enumerate(idxs):
                path[g] = path[g] + ((int(i2s[pos]), labs[pos]),)
                A_cur[g] = build_A_from_label(Ag, int(i2s[pos]), labs[pos], N)

        for m in range(M):
            if first_divergence[m] is None and path[m] != path[M+m]:
                first_divergence[m] = depth
        if verbose:
            print(f"    depth={depth} : {sum(1 for x in first_divergence if x is not None)}/{M} deja separes")

    return first_divergence, [tuple(path[m]) for m in range(M)], [tuple(path[M+m]) for m in range(M)]


def summarize(name, first_divergence, protocols, K=None):
    K_disp = K if K is not None else K_MAX
    found = [(fd, protocols[i]) for i,fd in enumerate(first_divergence) if fd is not None]
    if found:
        best = min(found, key=lambda t: t[0])
        print(f"  [{name}] SEPARE : profondeur minimale = {best[0]}, protocole {best[1]} "
              f"({len(found)}/{len(protocols)} protocoles separent)")
        return True
    else:
        print(f"  [{name}] NON SEPARE jusqu'a K={K_disp} sur les {len(protocols)} protocoles testes")
        return False
