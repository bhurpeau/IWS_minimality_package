"""
Verification du lemme de forme affine de Benoit : tau_i^(r)(q) = b_{i,C} + lambda_{r,C} * tau_i^0(q)
dans une chambre a chemin A(t) fixe, et demonstration (pas constat) de l'absence de mur aux rangs
impairs via l'extremum de c_isole(phi) en forme close, evalue sur l'intervalle REEL de la chambre
(echantillonnage tres fin, pas la grille d'origine).

Chambres testees (rang 5, cf. §4.21) : gi=1 (nb={2,3,4}, isole=4), gi=3 (nb={2,3,5}, isole=5).
"""
import sys
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core import (N, A1_kept1, make_tau_init, initial_group, advance_one_kairos,
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
groups, _ = advance_one_kairos(groups, 4, verbose=False)
groups = [g for g in groups if len(g['idx']) > 0]

mag = 0.3


def analyze(gi, isolated_node, varying_phi):
    grp = groups[gi]
    Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
    idx_local = grp['idx']
    PHI_flat = (PHI4 if varying_phi == 4 else PHI5).ravel()
    phi_chamber = PHI_flat[idx_local]
    nb = [j for j in range(N) if grp['A'][0, j] == 1]
    others = [j for j in nb if j != isolated_node]
    tau0 = taus[:, 0, :].mean(axis=0)
    tau_iso = taus[:, isolated_node, :]

    # fit affine b + lambda*mag*e(phi) = tau_iso sur 2 points, verifie sur tous les autres
    order = np.argsort(phi_chamber)
    i1, i2 = order[0], order[-1]
    pa, pb = np.radians(phi_chamber[i1]), np.radians(phi_chamber[i2])
    ea = np.array([np.cos(pa), np.sin(pa)])
    eb = np.array([np.cos(pb), np.sin(pb)])
    Ta, Tb = tau_iso[i1], tau_iso[i2]
    diff = Ta - Tb
    deno = mag * (ea - eb)
    lam = np.dot(diff, deno) / np.dot(deno, deno)
    b = Ta - lam * mag * ea
    e_all = np.stack([np.cos(np.radians(phi_chamber)), np.sin(np.radians(phi_chamber))], axis=1)
    resid = np.abs((b[None, :] + lam * mag * e_all) - tau_iso).max()

    def c_closed(phi_rad):
        e = np.stack([np.cos(phi_rad), np.sin(phi_rad)], axis=-1)
        p = b + lam * mag * e
        return (tau0 * p).sum(-1) / (np.linalg.norm(tau0) * np.linalg.norm(p, axis=-1) + 1e-15)

    c_pred = c_closed(np.radians(phi_chamber))
    c_sim = cos_sim(np.broadcast_to(tau0, (len(idx_local), 2)).copy(), tau_iso)
    closed_form_err = np.abs(c_pred - c_sim).max()

    lo, hi = np.radians(phi_chamber.min()), np.radians(phi_chamber.max())
    fine = np.linspace(lo, hi, 2_000_000)
    cvals = c_closed(fine)
    others_c = [cos_sim(np.broadcast_to(tau0, (len(idx_local), 2)).copy(), taus[:, k, :]).mean()
                for k in others]

    print("gi=%d isole=%d  phi%d range=[%.4f,%.4f] deg  npts=%d" %
          (gi, isolated_node, varying_phi, np.degrees(lo), np.degrees(hi), len(idx_local)))
    print("  residu fit affine (tau) = %.3e   ecart forme close (c) = %.3e" % (resid, closed_form_err))
    print("  c_%d : inf=%.10f sup=%.10f   concurrents geles=%s" %
          (isolated_node, cvals.min(), cvals.max(), {k: round(v, 6) for k, v in zip(others, others_c)}))
    print("  marge (inf(c_isole) - max(concurrents)) = %.6f  => mur possible : %s" %
          (cvals.min() - max(others_c), (cvals.min() - max(others_c)) < 0))


analyze(1, 4, 4)
analyze(3, 5, 5)
