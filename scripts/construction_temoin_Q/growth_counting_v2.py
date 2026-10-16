"""
Reprise de growth_counting.py avec la taxonomie a 4 types de Benoit :
  F!= : g = c_i - c_j constant != 0  (ordre gele, aucun mur possible)
  F=  : g constant == 0              (tie identique sur toute la chambre)
  M   : g non constant, 0 pas dans l'image (competition mobile, pas de mur dans C)
  W   : g non constant, 0 dans l'image   (genere au moins un mur actif)
Seuls les W alimentent N_comp/N_int. N_cand = tous les (C,alpha) examines.
N_frozen = F!= + F=.

Meme fenetre/chambre que growth_counting.py (site2_bas, A1_kept1, chambre {1,4,5}).
"""
import sys, pickle, time, itertools
import numpy as np
from scipy import ndimage

sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (N, A1_kept1, automorphisms, make_tau_init,
                              initial_group, advance_one_kairos, run_to_kairos,
                              cos_sim)

OUTDIR = '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad'
TOL = 1e-8  # constance / tie : l'invariant mesure a 1e-32, la variation reelle a >=1e-6

nphi = 140
phi4_1d = np.linspace(200.0, 228.0, nphi)
phi5_1d = np.linspace(335.0, 363.0, nphi)
PHI4, PHI5 = np.meshgrid(phi4_1d, phi5_1d, indexing='ij')
shape = PHI4.shape
G0 = PHI4.size
phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0

tau_init = make_tau_init(np.radians(PHI4).ravel(), np.radians(PHI5).ravel(),
                          phi1_fixed, phi2_fixed, phi3_fixed)

t0 = time.time()
groups = [initial_group(A1_kept1, tau_init)]
for depth in (2, 3):
    groups, _ = advance_one_kairos(groups, depth, verbose=False)

target = frozenset({1, 4, 5})
groups = [g for g in groups if g['path'][-1][1] == target and g['path'][-1][0] == 0]
print("chambre {1,4,5} au depart de r=4 : %d groupe(s), %d points (t=%.1fs)" %
      (len(groups), sum(len(g['idx']) for g in groups), time.time() - t0))


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


def is_structural(A, istar, i, j):
    if {i, j} != {4, 5}:
        return False
    for p in automorphisms(A):
        if p[istar] != istar:
            continue
        fixed_others = all(p[k] == k for k in range(N) if k not in (istar, 4, 5))
        if fixed_others and p[4] == 5 and p[5] == 4:
            return True
    return False


records = []
counts = {}

for r in (4, 5, 6, 7):
    tr0 = time.time()
    rec_r = []
    tally = dict(F_neq=0, F_eq=0, M=0, W=0)
    ncomp = 0
    nint_loci = 0

    for gi, grp in enumerate(groups):
        if len(grp['idx']) == 0:
            continue
        Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
        if not done.any():
            continue
        idx_local = grp['idx']
        istar_arr = np.argmax(Ps, axis=1)
        A = grp['A']

        for ist in np.unique(istar_arr[done]):
            msk = done & (istar_arr == ist)
            if not msk.any():
                continue
            nb = [j for j in range(N) if A[ist, j] == 1]
            nn = [j for j in range(N) if j != ist and A[ist, j] == 0]
            m = min(2, len(nb), len(nn))
            if m == 0:
                continue
            tau_i = taus[:, ist, :]
            scores = {k: cos_sim(tau_i, taus[:, k, :]) for k in (nb + nn)}

            all_pairs = [(i, j, a, 'nb') for (i, j, a) in active_pairs_side(nb, scores, m, 'remove')]
            all_pairs += [(i, j, a, 'nn') for (i, j, a) in active_pairs_side(nn, scores, m, 'add')]

            pair_components = []
            for (i, j, active_flat, side) in all_pairs:
                sel = msk & active_flat
                if not sel.any():
                    continue
                g_active = (scores[i] - scores[j])[sel]
                gmin, gmax = g_active.min(), g_active.max()
                spread = gmax - gmin
                struct = is_structural(A, ist, i, j)

                if spread < TOL:
                    gc = 0.5 * (gmin + gmax)
                    ptype = 'F_eq' if abs(gc) < TOL else 'F_neq'
                    tally[ptype] += 1
                    rec_r.append(dict(r=r, chamber=gi, istar=int(ist), pair=(i, j), side=side,
                                       type=ptype, structural=bool(struct), n_points=int(sel.sum()),
                                       g_const=float(gc)))
                    continue

                if gmin > 0 or gmax < 0:
                    tally['M'] += 1
                    rec_r.append(dict(r=r, chamber=gi, istar=int(ist), pair=(i, j), side=side,
                                       type='M', structural=bool(struct), n_points=int(sel.sum()),
                                       g_min=float(gmin), g_max=float(gmax)))
                    continue

                # type W : construit le champ 2D, composantes connexes
                tally['W'] += 1
                g = scores[i] - scores[j]
                g2d = np.full(G0, np.nan)
                g2d[idx_local[sel]] = g[sel]
                g2d = g2d.reshape(shape)
                finite = np.isfinite(g2d)
                signchg = np.zeros(shape, dtype=bool)
                for shift, axis in ((1, 0), (-1, 0), (1, 1), (-1, 1)):
                    sh = np.roll(g2d, shift, axis=axis)
                    shf = np.roll(finite, shift, axis=axis)
                    ok = finite & shf
                    cross = ok & (np.sign(g2d) != np.sign(sh)) & (np.sign(sh) != 0)
                    cross = cross & ok
                    signchg |= cross
                lbl, ncc = ndimage.label(signchg, structure=np.ones((3, 3)))
                ncomp += ncc
                for cidx in range(1, ncc + 1):
                    comp_mask = (lbl == cidx)
                    rec_r.append(dict(r=r, chamber=gi, istar=int(ist), pair=(i, j), side=side,
                                       type='W', structural=bool(struct), n_points=int(comp_mask.sum())))
                    pair_components.append((i, j, comp_mask))

            if len(pair_components) >= 2:
                owner_count = np.zeros(shape, dtype=np.int16)
                for (i, j, cm) in pair_components:
                    dil = ndimage.binary_dilation(cm, structure=np.ones((3, 3)))
                    owner_count += dil.astype(np.int16)
                multi = owner_count >= 2
                lbl2, ncc2 = ndimage.label(multi, structure=np.ones((3, 3)))
                nint_loci += ncc2

    n_cand = sum(tally.values())
    n_frozen = tally['F_neq'] + tally['F_eq']
    counts[r] = dict(N_cand=n_cand, N_frozen=n_frozen, N_F_neq=tally['F_neq'], N_F_eq=tally['F_eq'],
                      N_M=tally['M'], N_wall=tally['W'], N_comp=ncomp, N_int=nint_loci)
    print("r=%d : N_cand=%d  N_frozen=%d (F!=%d, F=%d)  N_M=%d  N_wall=%d  N_comp=%d  N_int=%d  (t=%.1fs)" %
          (r, n_cand, n_frozen, tally['F_neq'], tally['F_eq'], tally['M'], tally['W'], ncomp, nint_loci,
           time.time() - tr0))
    records.extend(rec_r)

    groups, splits = advance_one_kairos(groups, r, verbose=False)
    groups = [g for g in groups if len(g['idx']) > 0]

with open(OUTDIR + '/growth_counting_v2.pkl', 'wb') as f:
    pickle.dump(dict(counts=counts, records=records, PHI4=PHI4, PHI5=PHI5, shape=shape), f)
print("Total: %.1fs" % (time.time() - t0))
print("Sauvegarde growth_counting_v2.pkl")
