import sys, numpy as np, pickle, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import (automorphisms, make_u, initial_group, advance_one_kairos,
                                  label_map_from_groups, d)

# Temoin N=9 : nb(0)={1,2,3} orbite-3 (retrait, m=2 -> obstruction structurelle possible),
# nn(0)={4,5}(orbite-2) union {6,7,8}(orbite-3) (ajout, m=2 -> selection equivariante
# possible via l'orbite-2 seule). Etape 1 : scan (phi2,phi6) generique (pas le tau
# engineere du crash-test initial), forcage sur le noeud 0.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1
auts0 = automorphisms(A0, N)
print("|Aut(A0)| =", len(auts0))

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
t0 = time.time()
groups, splits = advance_one_kairos(groups, 1, N, verbose=True)
print("Temps : %.1fs" % (time.time()-t0))

lab_arr, path_to_id = label_map_from_groups(groups, G0)
print("\nNombre de chemins distincts a k=1 :", len(path_to_id))
for path,pid in path_to_id.items():
    count = (lab_arr==pid).sum()
    istar, nbset = path[0]
    print("  id=%d : nouveau voisinage de 0 = %s : %d pts (%.2f%%)" %
          (pid, sorted(nbset), count, 100*count/G0))

with open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/n9_etape1.pkl','wb') as f:
    pickle.dump(dict(PHI2=PHI2, PHI6=PHI6, lab_arr=lab_arr.reshape(n_grid,n_grid), path_to_id=path_to_id,
                      n_grid=n_grid, A0=A0, auts0=auts0), f)
print("Sauvegarde -> n9_etape1.pkl")
