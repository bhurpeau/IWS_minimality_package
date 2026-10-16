"""
Analyse (presque gratuite, Benoit) : pour chaque rang r et chaque chambre, (J_r, J_r cap Q, i_r*),
Q={4,5}, et confrontation avec le fait que la chambre ait produit >=1 paire de type W.
Reutilise exactement la construction de growth_counting_v2.py (meme fenetre/chambre).
"""
import sys, itertools
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (N, A1_kept1, make_tau_init, initial_group, advance_one_kairos,
                              run_to_kairos, cos_sim)

Q = {4, 5}
TOL = 1e-8

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


def active_pairs_side(cands, scores_dict, m, mode):
    out = []
    n = len(cands)
    if n <= m:
        return out
    target_below = (m - 1) if mode == 'remove' else (n - m - 1)
    for i, j in itertools.combinations(cands, 2):
        others = [scores_dict[k] for k in cands if k not in (i, j)]
        ci, cj = scores_dict[i], scores_dict[j]
        lo, hi = np.minimum(ci, cj), np.maximum(ci, cj)
        below = np.zeros_like(ci, dtype=int)
        above = np.zeros_like(ci, dtype=int)
        for ok in others:
            below += (ok < lo).astype(int)
            above += (ok > hi).astype(int)
        active = (below == target_below) & (above == (len(others) - target_below))
        out.append((i, j, active))
    return out


for r in (4, 5, 6, 7):
    print("=== r=%d ===" % r)
    any_wall_this_rank = False
    for gi, grp in enumerate(groups):
        if len(grp['idx']) == 0:
            continue
        Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
        if not done.any():
            continue
        istar_arr = np.argmax(Ps, axis=1)
        A = grp['A']
        for ist in np.unique(istar_arr[done]):
            msk = done & (istar_arr == ist)
            if not msk.any():
                continue
            nb = [j for j in range(N) if A[ist, j] == 1]
            nn = [j for j in range(N) if j != ist and A[ist, j] == 0]
            m = min(2, len(nb), len(nn))
            Jr = set(nb) | set(nn)
            s_r = len(Jr & Q)
            in_Q = (ist in Q)

            wall_here = False
            if m > 0:
                tau_i = taus[:, ist, :]
                scores = {k: cos_sim(tau_i, taus[:, k, :]) for k in Jr}
                all_pairs = [(i, j, a) for (i, j, a) in active_pairs_side(nb, scores, m, 'remove')]
                all_pairs += [(i, j, a) for (i, j, a) in active_pairs_side(nn, scores, m, 'add')]
                for (i, j, active_flat) in all_pairs:
                    sel = msk & active_flat
                    if not sel.any():
                        continue
                    g_active = (scores[i] - scores[j])[sel]
                    if g_active.min() <= 0 <= g_active.max() and (g_active.max() - g_active.min()) >= TOL:
                        wall_here = True

            any_wall_this_rank = any_wall_this_rank or wall_here
            nb_has_nontrivial_contest = len(nb) > m
            nn_has_nontrivial_contest = len(nn) > m
            print("  gi=%d  i*=%d  nb=%s (∩Q=%s, contest=%s)  nn=%s (∩Q=%s, contest=%s)  m=%d  mur=%s  npts=%d" %
                  (gi, ist, nb, sorted(set(nb) & Q), nb_has_nontrivial_contest,
                   nn, sorted(set(nn) & Q), nn_has_nontrivial_contest, m, wall_here, int(msk.sum())))
    print("  --> au moins un mur au rang %d : %s" % (r, any_wall_this_rank))
    groups, _ = advance_one_kairos(groups, r, verbose=False)
    groups = [g for g in groups if len(g['idx']) > 0]
