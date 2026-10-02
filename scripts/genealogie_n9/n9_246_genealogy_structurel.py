import sys, numpy as np, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, initial_group, run_to_kairos, jump_batch,
                                  build_A_from_label, d)

# Benoit : la chambre {2,4,6} montre une scission STRUCTURELLE recurrente a
# k=2 et k=4 (meme paire d'etiquettes {1,3,6} vs {1,2,3} a chaque fois).
# Question posee : est-ce le meme automorphisme (meme type d'orbite) qui
# revient, ou un autre ? On reinstrumente advance_one_kairos pour extraire
# explicitement le(s) automorphisme(s) temoins a chaque occurrence.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1

with open('n9_branch_centers.pkl','rb') as f:
    centers = pickle.load(f)
b246 = frozenset([2,4,6])
c2, c6 = centers[b246]
print("Centre {2,4,6} :", c2, c6)

n_grid = 60
radius = 15.0
mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

phi2_range = (c2 + np.linspace(-radius, radius, n_grid)) % 360
phi6_range = (c6 + np.linspace(-radius, radius, n_grid)) % 360
PHI2,PHI6 = np.meshgrid(phi2_range,phi6_range,indexing='ij')
G0 = n_grid*n_grid
phi2_flat = np.radians(PHI2).ravel(); phi6_flat = np.radians(PHI6).ravel()

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

groups = [initial_group(A0, tau_init, N)]

def advance_instrumented(groups, depth, N):
    new_groups = []
    splits_here = []
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
        if len(children) > 1:
            auts = automorphisms(grp['A'], N)
            istar_common = children[0]['path'][-1][0]
            fixing = [p for p in auts if p[istar_common]==istar_common]
            for a_i in range(len(children)):
                for b_i in range(a_i+1, len(children)):
                    Sa = set(children[a_i]['path'][-1][1])
                    Sb = set(children[b_i]['path'][-1][1])
                    witnesses = [p for p in fixing if set(p[j] for j in Sa)==Sb]
                    if witnesses:
                        # caracteriser chaque temoin : support (points non fixes), type de cycle
                        descs = []
                        for p in witnesses:
                            moved = [v for v in range(N) if p[v]!=v]
                            descs.append(dict(perm=p, moved=tuple(sorted(moved))))
                        splits_here.append(dict(depth=depth, parent_A=grp['A'].copy(), parent_path=grp['path'],
                                                 child_a=Sa, child_b=Sb, istar=istar_common,
                                                 n_fixing_auts=len(fixing), witnesses=descs))
    return new_groups, splits_here

all_splits = []
for depth in range(1,5+1):
    groups, splits = advance_instrumented(groups, depth, N)
    all_splits.extend(splits)
    print("depth=%d : %d groupes" % (depth, len({g['path'] for g in groups})))

print("\n=== Scissions STRUCTURELLES {1,3,6} vs {1,2,3} : temoins exacts ===")
for sp in all_splits:
    Sa, Sb = sp['child_a'], sp['child_b']
    if {1,3,6} in (Sa,Sb) and {1,2,3} in (Sa,Sb):
        print(f"\n-- depth={sp['depth']}, chemin parent={sp['parent_path']}, istar={sp['istar']}, n_fixing_auts={sp['n_fixing_auts']}")
        for w in sp['witnesses']:
            print("   temoin : deplace %s ; p=%s" % (w['moved'], {v:w['perm'][v] for v in w['moved']}))
