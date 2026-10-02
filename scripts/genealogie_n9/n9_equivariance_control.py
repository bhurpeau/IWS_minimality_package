import sys, numpy as np, pickle, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, initial_group, advance_one_kairos,
                                  label_map_from_groups, d, build_A_from_label)

# Benoit : controle propre de l'hypothese "1<->2 ne cause rien, c'est le
# contexte tau". Protocole : prendre le point centre choisi pour le zoom
# {1,4,5}, le transporter par sigma=(1 2) (fixant tout le reste, un element
# de Aut(A0)), et relancer EXACTEMENT le meme protocole (meme rayon, memes
# directions de balayage transportees) au point transporte. Si la numerique
# est bien equivariante, sigma.x doit tomber dans la chambre {2,4,5} ET
# produire la MEME suite |P_k^loc| que {1,4,5} (ici : plate, 1 partout).

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1
auts0 = automorphisms(A0, N)
sigma = tuple(2 if v==1 else (1 if v==2 else v) for v in range(N))
print("sigma = (1 2) dans Aut(A0) ?", sigma in auts0)

# equivariance de build_A_from_label : verifier A1_{2,4,5} = sigma . A1_{1,4,5}
A1_145 = build_A_from_label(A0, 0, frozenset([1,4,5]), N)
A1_245 = build_A_from_label(A0, 0, frozenset([2,4,5]), N)
P = np.zeros((N,N))
for v in range(N): P[sigma[v], v] = 1
A1_145_transported = P @ A1_145 @ P.T
print("sigma . A1_{1,4,5} == A1_{2,4,5} ?", np.array_equal(A1_145_transported, A1_245))

with open('n9_branch_centers.pkl','rb') as f:
    centers = pickle.load(f)
b145 = frozenset([1,4,5])
c2_145, c6_145 = centers[b145]
print("Centre original {1,4,5} : (phi2,phi6) =", (c2_145, c6_145))

# Le centre original correspond a un vecteur complet des 9 angles :
phi_fixed_by_node = {0: 0.0, 1: 15.0, 3: 45.0, 4: 5.0, 5: 355.0, 7: 200.0, 8: 160.0}
phi_full_145 = dict(phi_fixed_by_node)
phi_full_145[2] = c2_145   # centre du balayage original
phi_full_145[6] = c6_145

# transport par sigma : nouvel angle du noeud sigma(v) = ancien angle du noeud v
phi_full_sigma = {sigma[v]: phi_full_145[v] for v in range(N)}
print("Point transporte (angles complets) :", {k: round(phi_full_sigma[k],1) for k in sorted(phi_full_sigma)})
# -> le balayage doit maintenant porter sur phi1 (image de phi2) et phi6 (image de phi6, fixe par sigma)
c1_sigma = phi_full_sigma[1]   # = ancien phi2 (noeud 1 est l'image de noeud 2)
c6_sigma = phi_full_sigma[6]   # = ancien phi6 (noeud 6 fixe par sigma)
print("-> nouveau centre de balayage : phi1=%.1f (balaye), phi6=%.1f (balaye), phi2 fixe=%.1f" %
      (c1_sigma, c6_sigma, phi_full_sigma[2]))

n_grid = 60
radius = 15.0
mag = 0.3

def run_zoom(sweep_node_a, center_a, sweep_node_b, center_b, fixed_angles_deg, label_tag):
    phi_a_range = (center_a + np.linspace(-radius, radius, n_grid)) % 360
    phi_b_range = (center_b + np.linspace(-radius, radius, n_grid)) % 360
    PHI_A, PHI_B = np.meshgrid(phi_a_range, phi_b_range, indexing='ij')
    G0 = n_grid*n_grid
    phia_flat = np.radians(PHI_A).ravel(); phib_flat = np.radians(PHI_B).ravel()
    tau_init = np.zeros((G0,N,d))
    tau_init[:,0] = mag*np.array([1.0,0.0])
    for node, ang_deg in fixed_angles_deg.items():
        a = np.radians(ang_deg)
        tau_init[:,node] = mag*np.array([np.cos(a), np.sin(a)])
    a_rad = np.radians(fixed_angles_deg.get(sweep_node_a, None)) if False else None
    tau_init[:,sweep_node_a] = mag*np.stack([np.cos(phia_flat), np.sin(phia_flat)], axis=-1)
    tau_init[:,sweep_node_b] = mag*np.stack([np.cos(phib_flat), np.sin(phib_flat)], axis=-1)

    groups = [initial_group(A0, tau_init, N)]
    seq = []
    t0 = time.time()
    for depth in range(1,6):
        groups, splits = advance_one_kairos(groups, depth, N, verbose=False)
        lab_arr, path_to_id = label_map_from_groups(groups, N if False else G0)
        seq.append(len(path_to_id))
    print("  [%s] temps=%.1fs  |P_k^loc| k=1..5 : %s" % (label_tag, time.time()-t0, seq))
    # verif k=1 : chambre attendue ?
    lab1, p2id1 = label_map_from_groups(groups, G0)  # groups is now at depth5; recompute at depth1 separately below
    return seq, groups

print("\n--- Reference : zoom original {1,4,5} (balayage phi2,phi6) ---")
fixed_145 = {k:v for k,v in phi_full_145.items() if k not in (2,6)}
seq_145, _ = run_zoom(2, c2_145, 6, c6_145, fixed_145, "{1,4,5} original")

print("\n--- Controle equivariant : point transporte par sigma=(1 2), balayage phi1,phi6 ---")
fixed_sigma = {k:v for k,v in phi_full_sigma.items() if k not in (1,6)}
seq_sigma, groups_sigma = run_zoom(1, c1_sigma, 6, c6_sigma, fixed_sigma, "sigma.{1,4,5}")

print("\n=== Comparaison ===")
print(" {1,4,5} original       :", seq_145)
print(" sigma.{1,4,5} transporte:", seq_sigma)
print(" Sequences identiques ?", seq_145 == seq_sigma)

# verifier que le point transporte tombe bien dans la chambre {2,4,5} a k=1
lab_final = groups_sigma[0]['path'] if len(groups_sigma)==1 else None
labs_k1 = {g['path'][0][1] for g in groups_sigma}
print(" Etiquette(s) de depart (k=1) du point transporte :", [sorted(l) for l in labs_k1])
