import sys, numpy as np, pickle, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, run_to_kairos, jump_batch,
                                  build_A_from_label, d)

# Benoit : approfondir {2,4,6} (seule branche avec richesse structurelle
# avérée) jusqu'à k=6,7, avec deux questions précises :
#  (1) (2 6) reste-t-il temoin a chaque nouvelle scission structurelle, et
#      le meme type orbital (meme famille de temoins) revient-il, ou le
#      stabilisateur s'enrichit/s'appauvrit ?
#  (2) une branche qui n'a PAS pris la scission structurelle tot peut-elle
#      plus tard "retomber" sur une configuration ou (2 6) redevient actif ?

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1

SIGMA_26 = tuple(6 if v==2 else (2 if v==6 else v) for v in range(N))

with open('n9_branch_centers.pkl','rb') as f:
    centers = pickle.load(f)
b246 = frozenset([2,4,6])
c2, c6 = centers[b246]
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

# reconstruire exactement l'echantillon conditionne de n9_resample_conditioned.py
N_TARGET = 3600
radius, n_side = 15.0, 90
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
    match = np.array([lab==b246 and i2v==0 for lab,i2v in zip(labels,i2)])
    if match.sum() >= N_TARGET: break
    radius *= 1.4; n_side = int(n_side*1.3)
sel = np.flatnonzero(match)[:N_TARGET]
print("Echantillon conditionne reconstruit : %d points" % N_TARGET)

groups = [dict(idx=np.arange(N_TARGET), A=build_A_from_label(A0,0,b246,N),
               H=H2[sel], V=V2[sel], tau=tau2[sel], P=P2[sel], path=((0,b246),))]

def advance_instrumented(groups, depth, N):
    new_groups = []
    log = []
    for grp in groups:
        Hs,Vs,taus,Ps,done = run_to_kairos(grp['H'],grp['V'],grp['tau'],grp['P'],grp['A'],N)
        if not done.any(): continue
        H2,V2,tau2,P2, labels, i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],grp['A'],N)
        idx_done = grp['idx'][done]
        uniq = {}
        for k_local, lab in enumerate(labels):
            uniq.setdefault((lab, int(i2[k_local])), []).append(k_local)
        children = []
        for (lab, istar), pos_list in uniq.items():
            pos = np.array(pos_list)
            A_next = build_A_from_label(grp['A'], istar, lab, N)
            child = dict(idx=idx_done[pos], A=A_next, H=H2[pos], V=V2[pos], tau=tau2[pos], P=P2[pos],
                         path=grp['path']+((istar,lab),))
            children.append(child)
            new_groups.append(child)
        auts_parent = automorphisms(grp['A'], N)
        has_26_parent = SIGMA_26 in auts_parent
        if len(children) > 1:
            istar_common = children[0]['path'][-1][0]
            fixing = [p for p in auts_parent if p[istar_common]==istar_common]
            for a_i in range(len(children)):
                for b_i in range(a_i+1, len(children)):
                    Sa = set(children[a_i]['path'][-1][1])
                    Sb = set(children[b_i]['path'][-1][1])
                    witnesses = [p for p in fixing if set(p[j] for j in Sa)==Sb]
                    structural = len(witnesses) > 0
                    has_26_witness = SIGMA_26 in witnesses
                    log.append(dict(depth=depth, parent_path=grp['path'], parent_size=len(grp['idx']),
                                     istar=istar_common, child_a=Sa, child_b=Sb,
                                     structural=structural, n_witnesses=len(witnesses),
                                     has_26_witness=has_26_witness, has_26_in_parent_aut=has_26_parent,
                                     n_fixing_auts=len(fixing)))
        else:
            log.append(dict(depth=depth, parent_path=grp['path'], parent_size=len(grp['idx']),
                             istar=None, child_a=None, child_b=None, structural=False, n_witnesses=0,
                             has_26_witness=False, has_26_in_parent_aut=has_26_parent, n_fixing_auts=None,
                             no_split=True))
    return new_groups, log

all_log = []
t0 = time.time()
for depth in range(2, 8):
    groups, log = advance_instrumented(groups, depth, N)
    all_log.extend(log)
    n_groups = len({g['path'] for g in groups})
    print("depth=%d : %d groupes (temps cumule %.1fs)" % (depth, n_groups, time.time()-t0))

print("\n=== (2 6) dans Aut(A_parent) a chaque noeud de l'arbre, par profondeur ===")
for depth in range(2,8):
    entries = [e for e in all_log if e['depth']==depth]
    n_with_26 = sum(1 for e in entries if e['has_26_in_parent_aut'])
    print(" k=%d : %d/%d groupes-parents ont (2 6) dans Aut(A) avant le Kairos suivant" %
          (depth, n_with_26, len(entries)))

print("\n=== Scissions STRUCTURELLES avec (2 6) comme temoin ===")
for e in all_log:
    if e['structural'] and e['has_26_witness']:
        print(f" k={e['depth']}  chemin parent={e['parent_path']}  "
              f"{sorted(e['child_a'])} <-> {sorted(e['child_b'])}  "
              f"(n_temoins={e['n_witnesses']}, parent_size={e['parent_size']})")

print("\n=== Scissions STRUCTURELLES SANS (2 6) comme temoin (nouvelle symetrie ?) ===")
for e in all_log:
    if e['structural'] and not e['has_26_witness']:
        print(f" k={e['depth']}  chemin parent={e['parent_path']}  "
              f"{sorted(e['child_a'])} <-> {sorted(e['child_b'])}  "
              f"(n_temoins={e['n_witnesses']}, parent_size={e['parent_size']})")

print("\n=== Branches SANS scission a ce pas, mais ou (2 6) est present dans Aut(A) (reactivation possible) ===")
for e in all_log:
    if e.get('no_split') and e['has_26_in_parent_aut']:
        print(f" k={e['depth']}  chemin={e['parent_path']}  taille={e['parent_size']}  (2,6) present mais pas de scission ce pas-ci")

with open('n9_246_deep_26.pkl','wb') as f:
    pickle.dump(dict(all_log=all_log), f)
print("\nSauvegarde -> n9_246_deep_26.pkl")
print("Temps total : %.1fs" % (time.time()-t0))
