import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import sys, pathlib, numpy as np, time, pickle
_SCRIPTS = pathlib.Path(__file__).resolve().parents[1]   # remonte à scripts/
for _sub in ("core", "minimalite_U5_U4_U3", "R0_reachability", "construction_temoin_Q", "utils"):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_separating_families import run_pair_family
from iws_kairos_core_gen import d

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi8_fixed = np.radians(160.0)
phi2_c, phi6_c = 348.0, 12.0

def tau9_pert7(phi7_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_c)), np.sin(np.radians(phi2_c))])
    tau[3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
    tau[4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
    tau[5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_c)), np.sin(np.radians(phi6_c))])
    tau[7] = mag*np.array([np.cos(np.radians(phi7_deg)), np.sin(np.radians(phi7_deg))])
    tau[8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])
    return tau

amps_grid = np.load(_lp('phi7_amps.npy')); angs_grid = np.load(_lp('phi7_angs.npy'))
protocols = [(0, a*np.cos(np.radians(g)), a*np.sin(np.radians(g))) for a,g in zip(amps_grid,angs_grid)]

delta = float(sys.argv[1])
K = int(sys.argv[2]) if len(sys.argv)>2 else 4
tau_x  = tau9_pert7(200.0)
tau_xp = tau9_pert7(200.0+delta)
t0=time.time()
fd, px, pxp = run_pair_family(A0, N9, tau_x, tau_xp, protocols, K=K)
print("delta=%.1f K=%d : (%.1fs)" % (delta, K, time.time()-t0))

# chambre A1 = frozenset ajoute/retire au premier saut, cote x (meme que x' si pas de fuite k=1)
chamber1_x  = [p[0][1] if len(p)>0 else None for p in px]
chamber1_xp = [p[0][1] if len(p)>0 else None for p in pxp]
with open('phi7_delta%d_chambers.pkl' % int(delta), 'wb') as f:
    pickle.dump(dict(fd=fd, chamber1_x=chamber1_x, chamber1_xp=chamber1_xp), f)
print("sauvegarde -> phi7_delta%d_chambers.pkl" % int(delta))

# recap rapide : chambres distinctes rencontrees, et separation par chambre
from collections import Counter
cnt = Counter(chamber1_x)
print("Chambres A1 (cote x) rencontrees :", {str(sorted(k)) if k else k: v for k,v in cnt.items()})
leak_k1 = sum(1 for cx,cxp in zip(chamber1_x,chamber1_xp) if cx!=cxp)
print("Fuite a k=1 (chambre x != chambre x') : %d/%d" % (leak_k1, len(chamber1_x)))
