import sys, numpy as np, pickle, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import A1_kept1, make_tau_init, initial_group, advance_one_kairos, label_map_from_groups

# Poursuite du zoom du coin (0,0) [depth_growth_zoom.py, §4.10] jusqu'a k=7,
# avec genealogie complete (Benoit, points B et C) : pour chaque scission,
# la chambre parente, les candidats en competition, et l'origine
# (structurel / transverse).

phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0
n_grid = 60
phi4_range = np.linspace(-5.0, 25.0, n_grid)
phi5_range = np.linspace(-5.0, 25.0, n_grid)
PHI4,PHI5 = np.meshgrid(phi4_range,phi5_range,indexing='ij')
phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()
tau_init = make_tau_init(phi4_flat, phi5_flat, phi1_fixed, phi2_fixed, phi3_fixed)

groups = [initial_group(A1_kept1, tau_init)]
MAX_DEPTH = 7
label_maps = {}
all_splits = {}
t_start = time.time()
for depth in range(2, MAX_DEPTH+1):
    groups, splits = advance_one_kairos(groups, depth, verbose=True)
    all_splits[depth] = splits
    lab_arr, path_to_id = label_map_from_groups(groups, PHI4.size)
    label_maps[depth] = lab_arr
print("Temps total : %.1fs" % (time.time()-t_start))

print("\n=== Genealogie complete (chemins finaux a k=%d, avec taille) ===" % MAX_DEPTH)
sizes = {}
for g in groups:
    sizes[g['path']] = sizes.get(g['path'],0) + len(g['idx'])
for p,c in sorted(sizes.items(), key=lambda x:-x[1]):
    steps = " -> ".join("{%s}" % ",".join(map(str,sorted(lab))) for (istar,lab) in p)
    print("  %4d pts : %s" % (c, steps))

print("\n=== Quels candidats entrent en competition, par profondeur ===")
for depth in range(2, MAX_DEPTH+1):
    pairs = set()
    for sp in all_splits[depth]:
        sym = sp['child_a'].symmetric_difference(sp['child_b'])
        pairs.add(frozenset(sym))
    if pairs:
        print("  k=%d : %s" % (depth, [sorted(p) for p in pairs]))
    else:
        print("  k=%d : aucune scission" % depth)

with open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/zoom_deep_genealogy.pkl','wb') as f:
    pickle.dump(dict(PHI4=PHI4, PHI5=PHI5, label_maps=label_maps, all_splits=all_splits,
                      n_grid=n_grid, final_sizes=sizes), f)
print("\nSauvegarde -> zoom_deep_genealogy.pkl")
