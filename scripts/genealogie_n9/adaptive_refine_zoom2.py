import sys, numpy as np, pickle, time
import pathlib
_SCRIPTS = pathlib.Path(__file__).resolve().parents[1]   # remonte à scripts/
for _sub in ("core", "minimalite_U5_U4_U3", "R0_reachability", "construction_temoin_Q", "utils"):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core import A1_kept1, make_tau_init, initial_group, advance_one_kairos, label_map_from_groups

# zoom local sur le deuxieme site interessant trouve par adaptive_refine.py :
# (phi4,phi5) autour de (213.8, 11.2) et (213.8, 348.8)
TARGET_DEPTH = 4
phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0

def run_grid(phi4_deg_1d, phi5_deg_1d):
    PHI4, PHI5 = np.meshgrid(phi4_deg_1d, phi5_deg_1d, indexing='ij')
    phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()
    tau_init = make_tau_init(phi4_flat, phi5_flat, phi1_fixed, phi2_fixed, phi3_fixed)
    groups = [initial_group(A1_kept1, tau_init)]
    for depth in range(2, TARGET_DEPTH+1):
        groups, _ = advance_one_kairos(groups, depth, verbose=False)
    lab_arr, _ = label_map_from_groups(groups, PHI4.size)
    return PHI4, PHI5, lab_arr.reshape(PHI4.shape)

windows = {
    "site2_haut": (200.0, 228.0, -2.0, 26.0),
    "site2_bas":  (200.0, 228.0, 335.0, 363.0),
}
out = {}
for name,(lo4,hi4,lo5,hi5) in windows.items():
    phi4_f = np.linspace(lo4,hi4,50); phi5_f = np.linspace(lo5,hi5,50)
    PHI4,PHI5,lab = run_grid(phi4_f,phi5_f)
    out[name] = dict(PHI4=PHI4,PHI5=PHI5,lab=lab)
    print(name, "n_labels=", len(np.unique(lab)))

with open('../../output/adaptive_refine_zoom2.pkl','wb') as f:
    pickle.dump(out, f)
print("Sauvegarde.")
