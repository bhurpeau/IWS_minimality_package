import sys, numpy as np, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_separating_families import run_pair_family, K_MAX
from iws_kairos_core_gen import d

mag = 0.3
def vec(phi_deg):
    r = np.radians(phi_deg); return mag*np.array([np.cos(r), np.sin(r)])

N6 = 6
with open('nerode_pairs.pkl','rb') as f:
    saved = pickle.load(f)
A1_6 = saved['A1_6']

def tau6(phis):
    t = np.zeros((N6,d)); t[0] = mag*np.array([1.0,0.0])
    for i in range(1,6): t[i] = vec(phis[i-1])
    return t

def phis_near_corner(d4, d5):
    return [10.0, 40.0, 2.0, d4, d5]

std_protocol = [(0, 2.5*np.cos(np.radians(37.0)), 2.5*np.sin(np.radians(37.0)))]

base = (0.2, 0.2)
best = None
import itertools
steps = [0.02, 0.05, 0.1, 0.2, 0.3]
for dx in steps:
    for dy in steps:
        for sx,sy in itertools.product([1,-1],[1,-1]):
            p1 = phis_near_corner(base[0], base[1])
            p2 = phis_near_corner((base[0]+sx*dx) % 360, (base[1]+sy*dy) % 360)
            fd,_,_ = run_pair_family(A1_6, N6, tau6(p1), tau6(p2), std_protocol, K=K_MAX)
            d0 = fd[0]
            if d0 is not None and d0 >= 3:
                print(f"dx={dx} dy={dy} sx={sx} sy={sy} -> divergence a k={d0}")
                if best is None or d0 > best[2]:
                    best = (p1,p2,d0)
print("\nMeilleur trouve :", best)
if best:
    with open('nerode_pair_late.pkl','wb') as f:
        pickle.dump(dict(phisB=best[0], phisBp=best[1], depthB=best[2]), f)
    print("Sauvegarde -> nerode_pair_late.pkl")
