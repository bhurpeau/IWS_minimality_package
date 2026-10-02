import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core_gen import (automorphisms, initial_group, advance_one_kairos,
                                  label_map_from_groups, d, build_A_from_label)

# Reprise corrigee : la premiere passe (n9_depth_growth_4branches.py) a une
# resolution tres inegale entre branches (2860 vs 440 vs 260 vs 40 points
# sur 3600, heritee des aires du partage a k=1) -> les |P_k| ne sont PAS
# directement comparables tels quels. Correction : on reprend chaque branche
# separement avec un zoom local (meme budget de points, meme rayon angulaire)
# centre sur un point interieur verifie de chacune des 4 regions.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1
auts0 = automorphisms(A0, N)

with open(_lp('n9_branch_centers.pkl'),'rb') as f:
    centers = pickle.load(f)
branch_labels = list(centers.keys())

n_grid = 60
radius = 15.0  # demi-largeur en degres autour du centre, meme pour les 4
mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

MAX_DEPTH = 5
results = {}

for b in branch_labels:
    c2, c6 = centers[b]
    print("\n########## Branche %s : zoom local autour (phi2,phi6)=(%.1f,%.1f), rayon=%.1f ##########"
          % (tuple(sorted(b)), c2, c6, radius))
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
    label_maps_b = {}
    split_records_b = {}
    t0 = time.time()
    for depth in range(1, MAX_DEPTH+1):
        groups, splits = advance_one_kairos(groups, depth, N, verbose=True)
        split_records_b[depth] = splits
        lab_arr, path_to_id = label_map_from_groups(groups, G0)
        label_maps_b[depth] = (lab_arr, path_to_id)
        print("  k=%d : |P_k^loc|=%d groupes (sur %d pts)" % (depth, len(path_to_id), G0))
    print(" temps branche : %.1fs" % (time.time()-t0))

    # verification : a k=1, tous les points sont-ils bien dans la bonne branche ?
    lab1, p2id1 = label_maps_b[1]
    id2path1 = {v:k for k,v in p2id1.items()}
    ok = sum(1 for pid in np.unique(lab1) if frozenset(id2path1[pid][0][1])==b)
    n_ok = sum(int((lab1==pid).sum()) for pid in np.unique(lab1) if frozenset(id2path1[pid][0][1])==b)
    print("  verif k=1 : %d/%d points confirmes dans la branche %s" % (n_ok, G0, tuple(sorted(b))))

    results[b] = dict(PHI2=PHI2, PHI6=PHI6, label_maps=label_maps_b, split_records=split_records_b,
                       n_grid=n_grid, G0=G0, center=(c2,c6), radius=radius, n_ok=n_ok)

with open(_lp('n9_depth_growth_4branches_zoom.pkl'),'wb') as f:
    pickle.dump(dict(results=results, branch_labels=branch_labels), f)

print("\n\n=== RESUME : |P_k^loc| par branche (resolution EGALE, 3600 pts chacune) ===")
print("%-12s" % "branche", "k=1  k=2  k=3  k=4  k=5   (verif k1)")
for b in branch_labels:
    r = results[b]
    seq = [len(r['label_maps'][k][1]) for k in range(1,6)]
    print("%-12s" % str(tuple(sorted(b))), "  ".join("%3d"%x for x in seq), "  (%d/%d)"%(r['n_ok'], r['G0']))
