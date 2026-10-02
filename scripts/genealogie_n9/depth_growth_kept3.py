import numpy as np, itertools, time, pickle

# Meme suivi k=2..5 que depth_growth.py, mais depuis la chambre "garde=3"
# (Aut(A1)=4, sigma=(1 2)(4 5) et tau=(0 3) engendrent un Z2xZ2), meme
# forcage 2D generique 37 deg sur le noeud 0 (sigma le fixe -> ne le casse pas).
# But : comparer la croissance de P_k a celle, deja mesuree, de la branche
# sans symetrie (chambre "garde=1").

N, d = 6, 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1c, k2c, k3c = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5

edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges0: A0[i,j]=A0[j,i]=1
A1 = A0.copy()
A1[0,1]=A1[1,0]=0; A1[0,2]=A1[2,0]=0; A1[0,4]=A1[4,0]=1; A1[0,5]=A1[5,0]=1

def Atilde(A):
    B = A + np.eye(N)
    return B / B.sum(axis=1, keepdims=True)

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p,p)],A)]

auts1 = automorphisms(A1)
print("|Aut(A1)| [garde=3] =", len(auts1), auts1)

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

# ---------------- grille (phi4,phi5), etat apres K1, chambre "garde=3" ----------------
n_grid = 32
phi4_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
phi5_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
PHI4,PHI5 = np.meshgrid(phi4_range,phi5_range,indexing='ij')
G0 = n_grid*n_grid
phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()

mag = 0.3
phi3_fixed = np.radians(10.0)
phi12_fixed = np.radians(140.0)   # tau1 = tau2, exactement, pour rester dans Fix(sigma)

tau_init = np.zeros((G0,N,d))
tau_init[:,0] = mag*np.array([1.0,0.0])
tau_init[:,1] = mag*np.array([np.cos(phi12_fixed), np.sin(phi12_fixed)])
tau_init[:,2] = tau_init[:,1].copy()
tau_init[:,3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
tau_init[:,4] = mag*np.stack([np.cos(phi4_flat), np.sin(phi4_flat)], axis=-1)
tau_init[:,5] = mag*np.stack([np.cos(phi5_flat), np.sin(phi5_flat)], axis=-1)

H0 = np.zeros((G0,N,d)); V0 = np.zeros((G0,N,d)); P0 = np.zeros((G0,N))
P0[:,0] = rP*Theta

groups = [dict(idx=np.arange(G0), A=A1.copy(), H=H0, V=V0, tau=tau_init.copy(), P=P0, path=())]
label_maps = {}
split_records = {}
MAX_DEPTH = 5
t_start_all = time.time()
for depth in range(2, MAX_DEPTH+1):
    t0 = time.time()
    new_groups = []
    splits_here = []
    n_stalled = 0
    for grp in groups:
        Hs,Vs,taus,Ps,done = run_to_kairos(grp['H'],grp['V'],grp['tau'],grp['P'],grp['A'])
        n_stalled += (~done).sum()
        if done.any():
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
                        splits_here.append(dict(depth=depth, parent_size=len(grp['idx']),
                                                 child_a=Sa, child_b=Sb, istar=istar_common,
                                                 n_fixing_auts=len(fixing), structural=bool(structural)))
    groups = new_groups
    split_records[depth] = splits_here
    lab_arr = np.full(G0, -1, dtype=int)
    path_to_id = {}
    for grp in groups:
        key = grp['path']
        if key not in path_to_id: path_to_id[key] = len(path_to_id)
        lab_arr[grp['idx']] = path_to_id[key]
    label_maps[depth] = lab_arr
    print("depth=%d : %d groupes, %d stagnants, temps %.1fs" % (depth, len(path_to_id), n_stalled, time.time()-t0))
    for sp in splits_here:
        tag = "STRUCTUREL" if sp['structural'] else "transverse"
        print("   scission (parent %d pts, i*=%d) : {%s} vs {%s} -> %s (auts fixant i* : %d)" %
              (sp['parent_size'], sp['istar'],
               ",".join(map(str,sorted(sp['child_a']))), ",".join(map(str,sorted(sp['child_b']))),
               tag, sp['n_fixing_auts']))

print("\nTemps total : %.1fs" % (time.time()-t_start_all))

def connected_components(lab_arr_2d):
    n = lab_arr_2d.shape[0]
    visited = np.zeros_like(lab_arr_2d, dtype=bool)
    ncomp = 0
    for i0 in range(n):
        for j0 in range(n):
            if visited[i0,j0]: continue
            ncomp += 1
            stack=[(i0,j0)]; visited[i0,j0]=True; v0=lab_arr_2d[i0,j0]
            while stack:
                i,j = stack.pop()
                for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
                    ni,nj = (i+di)%n,(j+dj)%n
                    if not visited[ni,nj] and lab_arr_2d[ni,nj]==v0:
                        visited[ni,nj]=True; stack.append((ni,nj))
    return ncomp

def wall_pairs(lab_arr_2d):
    n = lab_arr_2d.shape[0]
    pairs=set()
    for i in range(n):
        for j in range(n):
            v0=lab_arr_2d[i,j]
            for di,dj in ((1,0),(0,1)):
                ni,nj=(i+di)%n,(j+dj)%n
                if lab_arr_2d[ni,nj]!=v0: pairs.add(((i,j),(ni,nj)))
    return pairs

print("\n=== Croissance geometrique, grille torique %dx%d ===" % (n_grid,n_grid))
prev_walls=None
summary_rows=[]
for depth in range(2, MAX_DEPTH+1):
    arr2d = label_maps[depth].reshape(n_grid,n_grid)
    ncomp = connected_components(arr2d)
    walls = wall_pairs(arr2d)
    new_walls = len(walls) if prev_walls is None else len(walls-prev_walls)
    n_chambers_alg = len(np.unique(label_maps[depth]))
    print("depth=%d : chambres=%d, composantes=%d, transitions_grille=%d, nouvelles=%d" %
          (depth, n_chambers_alg, ncomp, len(walls), new_walls))
    summary_rows.append(dict(depth=depth, n_chambers_alg=n_chambers_alg, ncomp=ncomp,
                              n_walls=len(walls), n_new_walls=new_walls))
    prev_walls = walls

with open('../../output/depth_growth_kept3.pkl','wb') as f:
    pickle.dump(dict(PHI4=PHI4, PHI5=PHI5, label_maps=label_maps, split_records=split_records,
                      summary_rows=summary_rows, n_grid=n_grid), f)
print("Sauvegarde -> depth_growth_kept3.pkl")
