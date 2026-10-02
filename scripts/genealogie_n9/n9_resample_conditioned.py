import sys, numpy as np, pickle, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, initial_group, run_to_kairos, jump_batch,
                                  advance_one_kairos, label_map_from_groups, d, build_A_from_label)

# Benoit : nettoyage methodologique pour {1,4,6} et {2,4,6} (contamination de
# bord ~120/3600 avec le zoom a rayon fixe). On sur-echantillonne (rayon plus
# large), on filtre aux points dont l'etiquette k=1 est EXACTEMENT celle
# attendue, on retient 3600 points parmi les filtres (fenetre irreguliere
# mais chambre garantie a 100%), puis on poursuit jusqu'a k=5.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1

with open('n9_branch_centers.pkl','rb') as f:
    centers = pickle.load(f)

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

def build_tau(phi2_flat, phi6_flat, G0):
    tau_init = np.zeros((G0,N,d))
    tau_init[:,0] = mag*np.array([1.0,0.0])
    tau_init[:,1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
    tau_init[:,2] = mag*np.stack([np.cos(phi2_flat), np.sin(phi2_flat)], axis=-1)
    tau_init[:,3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
    tau_init[:,4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
    tau_init[:,5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
    tau_init[:,6] = mag*np.stack([np.cos(phi6_flat), np.sin(phi6_flat)], axis=-1)
    tau_init[:,7] = mag*np.array([np.cos(phi7_fixed), np.sin(phi7_fixed)])
    tau_init[:,8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])
    return tau_init

N_TARGET = 3600
results = {}
for b in [frozenset([1,4,6]), frozenset([2,4,6])]:
    c2, c6 = centers[b]
    print("\n########## Branche %s : rejection sampling autour (%.1f,%.1f) ##########" % (tuple(sorted(b)), c2, c6))
    radius = 15.0
    n_side = 90
    while True:
        phi2_range = (c2 + np.linspace(-radius, radius, n_side)) % 360
        phi6_range = (c6 + np.linspace(-radius, radius, n_side)) % 360
        PHI2,PHI6 = np.meshgrid(phi2_range,phi6_range,indexing='ij')
        G0 = n_side*n_side
        phi2_flat = np.radians(PHI2).ravel(); phi6_flat = np.radians(PHI6).ravel()
        tau_init = build_tau(phi2_flat, phi6_flat, G0)
        H0=np.zeros((G0,N,d)); V0=np.zeros((G0,N,d)); P0=np.zeros((G0,N)); P0[:,0]=0.35*1.25
        Hs,Vs,taus,Ps,done = run_to_kairos(H0,V0,tau_init,P0,A0,N)
        H2,V2,tau2,P2,labels,i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],A0,N)
        match = np.array([lab==b and i2v==0 for lab,i2v in zip(labels,i2)])
        n_match = match.sum()
        print("  rayon=%.1f, grille=%dx%d : %d/%d points matchent la chambre %s" %
              (radius, n_side, n_side, n_match, G0, tuple(sorted(b))))
        if n_match >= N_TARGET:
            break
        radius *= 1.4; n_side = int(n_side*1.3)

    sel = np.flatnonzero(match)[:N_TARGET]
    phi2_sel = phi2_flat[sel]; phi6_sel = phi6_flat[sel]
    idx_done_global = np.flatnonzero(done)[sel]
    grp0 = dict(idx=np.arange(N_TARGET), A=build_A_from_label(A0,0,b,N),
                H=H2[sel], V=V2[sel], tau=tau2[sel], P=P2[sel], path=((0,b),))
    groups = [grp0]
    seq = [1]
    label_maps_b = {1: (np.zeros(N_TARGET,dtype=int), {((0,b),):0})}
    t0=time.time()
    for depth in range(2,6):
        groups, splits = advance_one_kairos(groups, depth, N, verbose=True)
        lab_arr, path_to_id = label_map_from_groups(groups, N_TARGET)
        label_maps_b[depth] = (lab_arr, path_to_id)
        seq.append(len(path_to_id))
    print("  temps suite k=2..5 : %.1fs" % (time.time()-t0))
    print("  |P_k^loc| (echantillon conditionne, 100%% garanti dans la chambre) k=1..5 :", seq)
    results[b] = dict(phi2_sel=phi2_sel, phi6_sel=phi6_sel, label_maps=label_maps_b, seq=seq, n_match=int(n_match))

with open('n9_resample_conditioned.pkl','wb') as f:
    pickle.dump(results, f)
print("\nSauvegarde -> n9_resample_conditioned.pkl")
