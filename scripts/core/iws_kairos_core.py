"""
Brique commune aux scripts de suivi F_y/~_N (temoin N=6, regime gamma_1=lambda=0).
Factorisee a partir de depth_growth.py / depth_growth_zoom.py / depth_growth_kept3.py
pour eviter de dupliquer une quatrieme fois la meme mecanique vectorisee.
"""
import numpy as np, itertools, time

N, d = 6, 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1c, k2c, k3c = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5

edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges0: A0[i,j]=A0[j,i]=1

# "garde=1" : Aut(A1)={e}
A1_kept1 = A0.copy()
A1_kept1[0,2]=A1_kept1[2,0]=0; A1_kept1[0,3]=A1_kept1[3,0]=0
A1_kept1[0,4]=A1_kept1[4,0]=1; A1_kept1[0,5]=A1_kept1[5,0]=1

# "garde=3" : Aut(A1)=4 (sigma=(1 2)(4 5), tau=(0 3))
A1_kept3 = A0.copy()
A1_kept3[0,1]=A1_kept3[1,0]=0; A1_kept3[0,2]=A1_kept3[2,0]=0
A1_kept3[0,4]=A1_kept3[4,0]=1; A1_kept3[0,5]=A1_kept3[5,0]=1

def Atilde(A):
    B = A + np.eye(N)
    return B / B.sum(axis=1, keepdims=True)

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p,p)],A)]

Uang = np.radians(37.0); Uamp = 2.5
Ux, Uy = Uamp*np.cos(Uang), Uamp*np.sin(Uang)

def make_u(G):
    def u_cont_batch(t):
        u = np.zeros((G,N,d)); u[:,0]=(Ux,Uy); return u
    return u_cont_batch

def rhs_batch(H,V,tau,P,At,u):
    th = np.tanh(np.einsum('ij,gjd->gid', At, H))
    dH = V
    dV = -gamma0*V - H + zeta*th + u
    dtau = alpha*th - beta*tau
    dP = k1c*np.linalg.norm(H,axis=-1) + k2c*np.linalg.norm(V,axis=-1) - k3c*P
    return dH,dV,dtau,dP

def rk4_batch(H,V,tau,P,At,t,dt,ufun):
    a1 = rhs_batch(H,V,tau,P,At,ufun(t))
    a2 = rhs_batch(H+dt/2*a1[0],V+dt/2*a1[1],tau+dt/2*a1[2],P+dt/2*a1[3],At,ufun(t+dt/2))
    a3 = rhs_batch(H+dt/2*a2[0],V+dt/2*a2[1],tau+dt/2*a2[2],P+dt/2*a2[3],At,ufun(t+dt/2))
    a4 = rhs_batch(H+dt*a3[0],V+dt*a3[1],tau+dt*a3[2],P+dt*a3[3],At,ufun(t+dt))
    H2=H+dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0]); V2=V+dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
    tau2=tau+dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2]); P2=P+dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
    return H2,V2,tau2,P2

def cos_sim(a,b):
    return (a*b).sum(axis=-1)/(np.linalg.norm(a,axis=-1)*np.linalg.norm(b,axis=-1)+1e-15)

def run_to_kairos(H,V,tau,P,A,dt=2e-3,Tmax=15.0):
    G = H.shape[0]
    At = Atilde(A)
    ufun = make_u(G)
    done = np.zeros(G, dtype=bool)
    H_snap,V_snap,tau_snap,P_snap = H.copy(),V.copy(),tau.copy(),P.copy()
    nsteps = int(Tmax/dt)
    t = 0.0
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

def jump_batch(H,V,tau,P,A):
    G = H.shape[0]
    i2 = np.argmax(P, axis=1)
    H2,V2,tau2,P2 = H.copy(),V.copy(),tau.copy(),P.copy()
    labels = [None]*G
    for istar in np.unique(i2):
        idx = np.flatnonzero(i2==istar)
        nb = [j for j in range(N) if A[istar,j]==1]
        nn = [j for j in range(N) if j!=istar and A[istar,j]==0]
        m = min(2, len(nb), len(nn))
        if m==0:
            for gi in idx: labels[gi] = frozenset(nb)
            continue
        tau_i = tau[idx, istar, :]
        sim_nb = np.stack([cos_sim(tau_i, tau[idx,j,:]) for j in nb], axis=1)
        order_nb = np.argsort(sim_nb, axis=1, kind='stable')
        removed_pos = order_nb[:, :m]
        sim_nn = np.stack([cos_sim(tau_i, tau[idx,j,:]) for j in nn], axis=1)
        order_nn = np.argsort(-sim_nn, axis=1, kind='stable')
        added_pos = order_nn[:, :m]
        nb_arr, nn_arr = np.array(nb), np.array(nn)
        for k_local, gi in enumerate(idx):
            removed = set(nb_arr[removed_pos[k_local]].tolist())
            added = set(nn_arr[added_pos[k_local]].tolist())
            labels[gi] = frozenset((set(nb) - removed) | added)
        P2[idx, istar] = rP * P[idx, istar]
        V2[idx, istar] = rV * V[idx, istar]
    return H2,V2,tau2,P2, labels, i2

def build_A_from_label(A_before, istar, new_nb):
    A_next = A_before.copy()
    for j in range(N):
        if j==istar: continue
        A_next[istar,j] = A_next[j,istar] = 1 if j in new_nb else 0
    return A_next

def make_tau_init(phi4_flat, phi5_flat, phi1_fixed_rad, phi2_fixed_rad, phi3_fixed_rad, mag=0.3):
    G = phi4_flat.shape[0]
    tau_init = np.zeros((G,N,d))
    tau_init[:,0] = mag*np.array([1.0,0.0])
    tau_init[:,1] = mag*np.array([np.cos(phi1_fixed_rad), np.sin(phi1_fixed_rad)])
    tau_init[:,2] = mag*np.array([np.cos(phi2_fixed_rad), np.sin(phi2_fixed_rad)])
    tau_init[:,3] = mag*np.array([np.cos(phi3_fixed_rad), np.sin(phi3_fixed_rad)])
    tau_init[:,4] = mag*np.stack([np.cos(phi4_flat), np.sin(phi4_flat)], axis=-1)
    tau_init[:,5] = mag*np.stack([np.cos(phi5_flat), np.sin(phi5_flat)], axis=-1)
    return tau_init

def initial_group(A1, tau_init):
    G0 = tau_init.shape[0]
    H0 = np.zeros((G0,N,d)); V0 = np.zeros((G0,N,d)); P0 = np.zeros((G0,N))
    P0[:,0] = rP*Theta
    return dict(idx=np.arange(G0), A=A1.copy(), H=H0, V=V0, tau=tau_init.copy(), P=P0, path=())

def advance_one_kairos(groups, depth, verbose=True):
    """Fait avancer chaque groupe d'un Kairos ; retourne les nouveaux groupes et
    les scissions detectees (avec classification structurel/transverse)."""
    new_groups = []
    splits_here = []
    n_stalled = 0
    for grp in groups:
        Hs,Vs,taus,Ps,done = run_to_kairos(grp['H'],grp['V'],grp['tau'],grp['P'],grp['A'])
        n_stalled += int((~done).sum())
        if not done.any():
            continue
        H2,V2,tau2,P2, labels, i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],grp['A'])
        idx_done = grp['idx'][done]
        uniq = {}
        for k_local, lab in enumerate(labels):
            uniq.setdefault((lab, int(i2[k_local])), []).append(k_local)
        children = []
        for (lab, istar), pos_list in uniq.items():
            pos = np.array(pos_list)
            A_next = build_A_from_label(grp['A'], istar, lab)
            child = dict(idx=idx_done[pos], A=A_next, H=H2[pos], V=V2[pos], tau=tau2[pos], P=P2[pos],
                         path=grp['path']+((istar,lab),))
            children.append(child)
            new_groups.append(child)
        if len(children) > 1:
            auts = automorphisms(grp['A'])
            istar_common = children[0]['path'][-1][0]
            fixing = [p for p in auts if p[istar_common]==istar_common]
            for a_i in range(len(children)):
                for b_i in range(a_i+1, len(children)):
                    Sa = set(children[a_i]['path'][-1][1])
                    Sb = set(children[b_i]['path'][-1][1])
                    structural = any(set(p[j] for j in Sa)==Sb for p in fixing)
                    splits_here.append(dict(depth=depth, parent_size=len(grp['idx']), parent_path=grp['path'],
                                             child_a=Sa, child_b=Sb, istar=istar_common,
                                             n_fixing_auts=len(fixing), structural=bool(structural)))
    if verbose:
        path_ids = {g['path'] for g in new_groups}
        print("  depth=%d : %d groupes, %d stagnants" % (depth, len(path_ids), n_stalled))
        for sp in splits_here:
            tag = "STRUCTUREL" if sp['structural'] else "transverse"
            print("     scission (parent %d pts, i*=%d) : {%s} vs {%s} -> %s" %
                  (sp['parent_size'], sp['istar'],
                   ",".join(map(str,sorted(sp['child_a']))), ",".join(map(str,sorted(sp['child_b']))), tag))
    return new_groups, splits_here

def label_map_from_groups(groups, G0):
    lab_arr = np.full(G0, -1, dtype=int)
    path_to_id = {}
    for grp in groups:
        key = grp['path']
        if key not in path_to_id: path_to_id[key] = len(path_to_id)
        lab_arr[grp['idx']] = path_to_id[key]
    return lab_arr, path_to_id
