"""
Fermeture symbolique du point 1 de Benoit : remplace le balayage fin (2e6 points) de
affine_form_check.py par une evaluation en un nombre FINI de points critiques exacts,
via sa formule
    c'(phi) proportionnel a -a*(y+a*sin(phi))*(a+x*cos(phi)+y*sin(phi))
dans le repere aligne sur tau0 (rotation de -theta0, theta0 = arg(tau0)).
Les extrema sur un intervalle sont donc parmi les 2 extremites et les <=4 racines des deux
equations trigonometriques ci-dessus, resolues exactement (pas d'optimisation numerique).
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


def analyze_exact(gi, isolated_node, varying_phi):
    grp = groups[gi]
    Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
    idx_local = grp['idx']
    PHI_flat = (PHI4 if varying_phi == 4 else PHI5).ravel()
    phi_chamber = PHI_flat[idx_local]
    nb = [j for j in range(N) if grp['A'][0, j] == 1]
    others = [j for j in nb if j != isolated_node]
    tau0 = taus[:, 0, :].mean(axis=0)
    tau_iso = taus[:, isolated_node, :]

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
    a = lam * mag

    theta0 = np.arctan2(tau0[1], tau0[0])
    R0 = np.array([[np.cos(theta0), np.sin(theta0)], [-np.sin(theta0), np.cos(theta0)]])
    x, y = (R0 @ b)

    def c_closed(phi_rad):
        e = np.stack([np.cos(phi_rad), np.sin(phi_rad)], axis=-1)
        p = b + a * e
        return (tau0 * p).sum(-1) / (np.linalg.norm(tau0) * np.linalg.norm(p, axis=-1) + 1e-15)

    candidates_phi = []
    s = -y / a
    if abs(s) <= 1:
        for phip in (np.arcsin(s), np.pi - np.arcsin(s)):
            candidates_phi.append(phip + theta0)
    Rr = np.hypot(x, y)
    if Rr >= abs(a) and Rr > 0:
        delta = np.arctan2(y, x)
        val = np.clip(-a / Rr, -1, 1)
        for sign in (1, -1):
            candidates_phi.append(delta + sign * np.arccos(val) + theta0)

    lo, hi = np.radians(phi_chamber.min()), np.radians(phi_chamber.max())
    in_range = []
    for phi in candidates_phi:
        k = round((0.5 * (lo + hi) - phi) / (2 * np.pi))
        phi_mod = phi + k * 2 * np.pi
        if lo - 1e-9 <= phi_mod <= hi + 1e-9:
            in_range.append(phi_mod)

    eval_pts = np.array([lo, hi] + in_range)
    cvals = c_closed(eval_pts)
    others_c = [cos_sim(np.broadcast_to(tau0, (len(idx_local), 2)).copy(), taus[:, k, :]).mean()
                for k in others]

    print("gi=%d isole=%d : candidats critiques DANS l'intervalle : %s" %
          (gi, isolated_node, [round(np.degrees(p), 4) for p in in_range]))
    print("  points evalues (deg) = %s" % np.degrees(eval_pts))
    print("  c_%d = %s" % (isolated_node, cvals))
    print("  inf=%.10f  sup=%.10f  concurrents=%s" %
          (cvals.min(), cvals.max(), {k: round(v, 6) for k, v in zip(others, others_c)}))
    print("  marge exacte = %.6f (nombre FINI de points, pas un balayage)\n" %
          (cvals.min() - max(others_c)))


analyze_exact(1, 4, 4)
analyze_exact(3, 5, 5)
