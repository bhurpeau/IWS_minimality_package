import sys, numpy as np, pickle, time, itertools
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, initial_group, advance_one_kairos,
                                  label_map_from_groups, d, build_A_from_label)

# Benoit : pousser les 4 chambres de k=1 (N=9) en parallele, meme grille,
# memes diagnostics, jusqu'a k=4 ou 5, sans en choisir une a priori.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1
auts0 = automorphisms(A0, N)

n_grid = 60
phi2_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
phi6_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
PHI2,PHI6 = np.meshgrid(phi2_range,phi6_range,indexing='ij')
G0 = n_grid*n_grid
phi2_flat = np.radians(PHI2).ravel(); phi6_flat = np.radians(PHI6).ravel()

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

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
MAX_DEPTH = 5
label_maps = {}
split_records = {}
t_start = time.time()
for depth in range(1, MAX_DEPTH+1):
    groups, splits = advance_one_kairos(groups, depth, N, verbose=True)
    split_records[depth] = splits
    lab_arr, path_to_id = label_map_from_groups(groups, G0)
    label_maps[depth] = (lab_arr, path_to_id)
print("Temps total : %.1fs" % (time.time()-t_start))

# diagnostics directs pour chacune des 4 A1 (branches de k=1)
print("\n=== Diagnostics par A1 (k=1) ===")
def orbits(auts, n):
    seen, orbs = set(), []
    for v in range(n):
        if v in seen: continue
        orb = sorted({p[v] for p in auts})
        orbs.append(orb); seen.update(orb)
    return orbs

branch_labels = [frozenset(s) for s in ([1,4,5],[2,4,5],[1,4,6],[2,4,6])]
A1_by_branch = {}
for lab in branch_labels:
    A1 = build_A_from_label(A0, 0, lab, N)
    auts1 = automorphisms(A1, N)
    orbs1 = orbits(auts1, N)
    A1_by_branch[lab] = A1
    print("  A1 pour %s : |Aut(A1)|=%d, orbites=%s" % (sorted(lab), len(auts1), orbs1))

# regrouper, a chaque profondeur, par branche d'origine (label de k=1)
print("\n=== |P_k| par branche d'origine (k=1..5) ===")
# reconstruire, pour chaque groupe final, son ancetre de profondeur 1
def ancestor_label(path):
    return frozenset(path[0][1])

for depth in range(1, MAX_DEPTH+1):
    lab_arr, path_to_id = label_maps[depth]
    id_to_path = {v:k for k,v in path_to_id.items()}
    counts_per_branch = {b: set() for b in branch_labels}
    sizes_per_branch = {b: 0 for b in branch_labels}
    for pid, path in id_to_path.items():
        anc = ancestor_label(path)
        counts_per_branch[anc].add(pid)
        sizes_per_branch[anc] += int((lab_arr==pid).sum())
    print(" k=%d :" % depth, {tuple(sorted(b)): len(counts_per_branch[b]) for b in branch_labels})

with open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/n9_depth_growth_4branches.pkl','wb') as f:
    pickle.dump(dict(PHI2=PHI2, PHI6=PHI6, label_maps=label_maps, split_records=split_records,
                      n_grid=n_grid, branch_labels=branch_labels, A1_by_branch=A1_by_branch), f)
print("\nSauvegarde -> n9_depth_growth_4branches.pkl")
