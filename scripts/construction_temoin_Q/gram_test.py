"""
Test du Gram normalise (Benoit) sur les chambres gelees de §4.19 (r=5,7).
G^tau_{ij} = <tau_i/|tau_i|, tau_j/|tau_j|> pour i,j dans {0,1,2,3}.
Si le sous-bloc est EXACTEMENT constant sur toute la chambre alors que les tau_i
varient individuellement, le gel vient d'une rotation commune + mises a l'echelle
individuelles (tau_i(q) = a_i(q) R(q) tau_bar_i), pas d'un decouplage.
"""
import sys, itertools
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (A1_kept1, make_tau_init, initial_group, advance_one_kairos,
                              run_to_kairos, cos_sim)

nphi = 140
phi4_1d = np.linspace(200.0, 228.0, nphi)
phi5_1d = np.linspace(335.0, 363.0, nphi)
PHI4, PHI5 = np.meshgrid(phi4_1d, phi5_1d, indexing='ij')
phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0

tau_init = make_tau_init(np.radians(PHI4).ravel(), np.radians(PHI5).ravel(),
                          phi1_fixed, phi2_fixed, phi3_fixed)

groups = [initial_group(A1_kept1, tau_init)]
for depth in (2, 3):
    groups, _ = advance_one_kairos(groups, depth, verbose=False)
target = frozenset({1, 4, 5})
groups = [g for g in groups if g['path'][-1][1] == target and g['path'][-1][0] == 0]

block = [0, 1, 2, 3]

def gram_report(label, taus):
    print("---", label, "---")
    for i in block:
        v = taus[:, i, :]
        norm = np.linalg.norm(v, axis=-1)
        print("  |tau_%d| : min=%.6g max=%.6g (var=%.3g)" % (i, norm.min(), norm.max(), norm.var()))
    worst = 0.0
    for i, j in itertools.combinations(block, 2):
        G = cos_sim(taus[:, i, :], taus[:, j, :])
        spread = G.max() - G.min()
        worst = max(worst, spread)
        print("  G[%d,%d] : min=%.12g max=%.12g spread=%.3g" % (i, j, G.min(), G.max(), spread))
    print("  spread max sur le bloc : %.3g" % worst)

for r in (4, 5, 6, 7):
    for gi, grp in enumerate(groups):
        Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
        gram_report("r=%d gi=%d (A0row=%s, npts=%d)" % (r, gi, grp['A'][0].astype(int).tolist(), len(grp['idx'])), taus)
    groups, _ = advance_one_kairos(groups, r, verbose=False)
    groups = [g for g in groups if len(g['idx']) > 0]
