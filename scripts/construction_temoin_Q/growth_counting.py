"""
Programme de comptage (N_pair, N_comp, N_int) pour r=4,5,6,7, chambre par chambre
de P_{r-1}, sur la meme chambre {1,4,5}/fenetre site2_bas que le test transverse
precedent (contour_active_walls.py).

Garde-fous demandes par Benoit :
  - calcul chambre-par-chambre dans P_{r-1} (pas de i*/seuil unique global) ;
  - genealogie par composante : (r, chambre_parent, (i,j), cote nb/nn,
    structurel/transverse, nb_points) ;
  - N_int compte des LIEUX geometriques distincts (avec multiplicite a part),
    pas des couples de murs ;
  - les lieux de tie exact (type Fix(sigma)) ne sont pas une erreur, ils ne sont
    simplement pas cherches ici (cette chambre n'a pas la symetrie 4<->5 realisee
    puisque phi1_fixe=10 deg != phi2_fixe=40 deg -> aucun automorphisme utile
    n'est "realise" sur cette fenetre ; verifie explicitement par is_structural).
"""
import sys, pickle, time, itertools
import numpy as np
from scipy import ndimage

sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (N, A1_kept1, automorphisms, make_tau_init,
                              initial_group, advance_one_kairos, run_to_kairos,
                              cos_sim)

OUTDIR = '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad'

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
    groups, splits = advance_one_kairos(groups, depth, verbose=True)

target = frozenset({1, 4, 5})
groups = [g for g in groups if g['path'][-1][1] == target and g['path'][-1][0] == 0]
print("chambre {1,4,5} au depart de r=4 : %d groupe(s), %d points (t=%.1fs)" %
      (len(groups), sum(len(g['idx']) for g in groups), time.time() - t0))


def active_pairs_side(cands, scores_dict, m, mode):
    """mode='remove' (nb : on enleve les m plus bas) ou 'add' (nn : on garde les m plus hauts)."""
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
    """Mur force (c_i=c_j identiquement) ssi un automorphisme de A fixant istar,
    identite sur les noeuds fixes du parametrage, et echangeant i<->j={4,5} existe."""
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
    npair = 0
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
                npair += 1
                g = scores[i] - scores[j]
                g2d = np.full(G0, np.nan)
                sel = msk & active_flat
                g2d[idx_local[sel]] = g[sel]
                g2d = g2d.reshape(shape)
                if sel.any():
                    print("    r=%d gi=%d ist=%d pair=(%d,%d) side=%s : n_active=%d g_min=%.4g g_max=%.4g" %
                          (r, gi, ist, i, j, side, int(sel.sum()), np.nanmin(g2d), np.nanmax(g2d)))
                else:
                    print("    r=%d gi=%d ist=%d pair=(%d,%d) side=%s : AUCUN POINT ACTIF" %
                          (r, gi, ist, i, j, side))
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
                struct = is_structural(A, ist, i, j)
                for cidx in range(1, ncc + 1):
                    comp_mask = (lbl == cidx)
                    rec_r.append(dict(r=r, chamber=gi, istar=int(ist), pair=(i, j), side=side,
                                       structural=bool(struct), n_points=int(comp_mask.sum())))
                    pair_components.append((i, j, comp_mask))

            if len(pair_components) >= 2:
                owner_count = np.zeros(shape, dtype=np.int16)
                for (i, j, cm) in pair_components:
                    dil = ndimage.binary_dilation(cm, structure=np.ones((3, 3)))
                    owner_count += dil.astype(np.int16)
                multi = owner_count >= 2
                lbl2, ncc2 = ndimage.label(multi, structure=np.ones((3, 3)))
                nint_loci += ncc2

    counts[r] = dict(N_pair=npair, N_comp=ncomp, N_int=nint_loci)
    print("r=%d : N_pair=%d  N_comp=%d  N_int=%d  (%d groupes actifs, t=%.1fs)" %
          (r, npair, ncomp, nint_loci, len(groups), time.time() - tr0))
    records.extend(rec_r)

    groups, splits = advance_one_kairos(groups, r, verbose=False)
    groups = [g for g in groups if len(g['idx']) > 0]

with open(OUTDIR + '/growth_counting.pkl', 'wb') as f:
    pickle.dump(dict(counts=counts, records=records, PHI4=PHI4, PHI5=PHI5, shape=shape), f)
print("Total: %.1fs" % (time.time() - t0))
print("Sauvegarde growth_counting.pkl")
