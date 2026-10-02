import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core import (A1_kept1, make_tau_init, initial_group, advance_one_kairos,
                              label_map_from_groups, N, d)

# ---------------------------------------------------------------
# Strategie adaptive (Benoit, point A) : grille grossiere sur tout le tore
# (phi4,phi5), detection des cellules heterogenes (= traversees par une
# paroi), puis raffinement local recursif seulement la ou c'est necessaire.
# But : verifier que la richesse trouvee au coin (0,0) au depth 4 n'est pas
# la seule qui existe sur le tore complet -- une grille uniforme a la meme
# resolution locale couterait (360/1.something)^2 points partout.
# ---------------------------------------------------------------

TARGET_DEPTH = 4
phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0

def run_grid(phi4_deg_1d, phi5_deg_1d, toroidal_label_only=True):
    """Simule jusqu'a TARGET_DEPTH sur un rectangle (phi4,phi5) (en degres),
    retourne le tableau d'etiquettes (meme forme que le meshgrid)."""
    PHI4, PHI5 = np.meshgrid(phi4_deg_1d, phi5_deg_1d, indexing='ij')
    phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()
    tau_init = make_tau_init(phi4_flat, phi5_flat, phi1_fixed, phi2_fixed, phi3_fixed)
    groups = [initial_group(A1_kept1, tau_init)]
    for depth in range(2, TARGET_DEPTH+1):
        groups, _ = advance_one_kairos(groups, depth, verbose=False)
    lab_arr, _ = label_map_from_groups(groups, PHI4.size)
    return PHI4, PHI5, lab_arr.reshape(PHI4.shape)

# ---- niveau 0 : grille grossiere sur tout le tore ----
n0 = 16
phi4_0 = np.linspace(0.0, 360.0, n0, endpoint=False)
phi5_0 = np.linspace(0.0, 360.0, n0, endpoint=False)
t0 = time.time()
PHI4_0, PHI5_0, lab_0 = run_grid(phi4_0, phi5_0)
print("Niveau 0 (grille %dx%d, tout le tore) : %d chemins distincts, %.1fs" %
      (n0, n0, len(np.unique(lab_0)), time.time()-t0))

# cellules heterogenes : la cellule (i,j) -> (i+1,j+1) (toroidal) est flagee
# si l'un de ses 4 coins n'a pas la meme etiquette que les autres
flagged = []
for i in range(n0):
    for j in range(n0):
        corners = [lab_0[i,j], lab_0[(i+1)%n0,j], lab_0[i,(j+1)%n0], lab_0[(i+1)%n0,(j+1)%n0]]
        if len(set(corners)) > 1:
            flagged.append((i,j))
print("Cellules grossieres heterogenes (a raffiner) : %d / %d" % (len(flagged), n0*n0))

step = 360.0/n0
n1 = 12  # facteur de raffinement local
results = []
t0 = time.time()
for (i,j) in flagged:
    lo4, hi4 = phi4_0[i], phi4_0[i]+step
    lo5, hi5 = phi5_0[j], phi5_0[j]+step
    phi4_f = np.linspace(lo4, hi4, n1)
    phi5_f = np.linspace(lo5, hi5, n1)
    _,_, lab_f = run_grid(phi4_f, phi5_f)
    n_labels_fine = len(np.unique(lab_f))
    results.append(dict(i=i, j=j, phi4_center=(lo4+hi4)/2, phi5_center=(lo5+hi5)/2,
                         n_labels_coarse_corners=len(set([lab_0[i,j], lab_0[(i+1)%n0,j],
                                                           lab_0[i,(j+1)%n0], lab_0[(i+1)%n0,(j+1)%n0]])),
                         n_labels_fine=n_labels_fine))
print("Raffinement local de %d cellules (grille %dx%d chacune) : %.1fs" % (len(flagged), n1, n1, time.time()-t0))

print("\nRepartition (phi4,phi5) des cellules raffinees et richesse trouvee :")
for r in sorted(results, key=lambda r: -r['n_labels_fine'])[:15]:
    print("  centre (%.1f,%.1f) : %d etiquettes aux coins grossiers -> %d etiquettes en raffine" %
          (r['phi4_center'], r['phi5_center'], r['n_labels_coarse_corners'], r['n_labels_fine']))

with open('../../output/adaptive_refine.pkl','wb') as f:
    pickle.dump(dict(PHI4_0=PHI4_0, PHI5_0=PHI5_0, lab_0=lab_0, flagged=flagged, results=results, n0=n0), f)
print("\nSauvegarde -> adaptive_refine.pkl")
