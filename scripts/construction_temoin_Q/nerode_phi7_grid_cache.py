import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import numpy as np, time
import sys, pathlib
_SCRIPTS = pathlib.Path(__file__).resolve().parents[1]   # remonte à scripts/
for _sub in ("core", "minimalite_U5_U4_U3", "R0_reachability", "construction_temoin_Q", "utils"):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_R0_sequential import map_R0_sequential

amps_grid = np.repeat(np.linspace(0.5, 10.0, 20), 40)
angs_grid = np.tile(np.linspace(0, 352, 40), 20)
print("Grille : %d protocoles" % len(amps_grid))
t0=time.time()
theta1, theta2, alive_seq = map_R0_sequential(amps_grid, angs_grid)
print("  (%.1fs)" % (time.time()-t0))
np.save(_lp('phi7_amps.npy'), amps_grid); np.save(_lp('phi7_angs.npy'), angs_grid)
np.save(_lp('phi7_theta1.npy'), theta1); np.save(_lp('phi7_theta2.npy'), theta2); np.save(_lp('phi7_alive.npy'), alive_seq)
print("sauvegarde OK, %d/%d valides" % (alive_seq.sum(), len(alive_seq)))
