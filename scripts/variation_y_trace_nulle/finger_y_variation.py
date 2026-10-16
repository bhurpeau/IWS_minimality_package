"""
Variation du present observable y (Benoit, 'prochain pas', N=6, k=4) :
on garde la meme coupe cachee (tranche phi5 = 349 deg, phi4 variable) et le meme protocole,
et on deplace UNE composante de H(0) (noeud NODE, composante COMP) de eta.
Pour chaque eta on suit, dans la classe de mot (chemin) qui contient le doigt a eta=0,
les racines de g_14^(4) = c_1 - c_4 au rang 4 (nb(0)={1,4,5}, m=2), i.e. les deux
bords du doigt (~218.56 et ~219.46 deg a eta=0).
Sorties : tableau eta -> (chemin retrouve ?, racines, largeur), pour reperer un eta* critique.
"""
import sys, os, time, pickle
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core'))
from iws_kairos_core import (N, A1_kept1, make_tau_init, initial_group, advance_one_kairos,
                              run_to_kairos, jump_batch, cos_sim)

NPHI = int(os.environ.get('NPHI', sys.argv[1] if (__name__ == '__main__' and len(sys.argv) > 1) else 3000))
NODE, COMP = 0, 0
PHI5_DEG = 349.0
PHI_LO = float(os.environ.get('PHI_LO', 200.0)); PHI_HI = float(os.environ.get('PHI_HI', 228.0))
phi4_deg = np.linspace(PHI_LO, PHI_HI, NPHI)
phi1_fixed, phi2_fixed, phi3_fixed = np.radians(10.0), np.radians(40.0), 2.0
tau_init = make_tau_init(np.radians(phi4_deg), np.full(NPHI, np.radians(PHI5_DEG)),
                         phi1_fixed, phi2_fixed, phi3_fixed)
TARGET = frozenset({1, 4, 5})


def groups_at_depth3(eta):
    g0 = initial_group(A1_kept1, tau_init)
    g0['H'][:, NODE, COMP] = eta
    groups = [g0]
    for depth in (2, 3):
        groups, _ = advance_one_kairos(groups, depth, verbose=False)
    return [g for g in groups if len(g['idx']) > 0]


def rank4_scores(grp):
    Hs, Vs, taus, Ps, done = run_to_kairos(grp['H'], grp['V'], grp['tau'], grp['P'], grp['A'])
    ist = np.argmax(Ps, axis=1)
    istar = int(np.bincount(ist[done]).argmax()) if done.any() else -1
    A = grp['A']
    nb = [j for j in range(N) if A[istar, j] == 1]
    tau_i = taus[:, istar, :]
    sc = {j: cos_sim(tau_i, taus[:, j, :]) for j in nb}
    H4, V4, t4, P4, labels, i2 = jump_batch(Hs[done], Vs[done], taus[done], Ps[done], A)
    return istar, nb, sc, done, labels


def roots_of(phi, g, ok):
    out = []
    for a in range(len(phi) - 1):
        if ok[a] and ok[a + 1] and g[a] * g[a + 1] < 0:
            t = g[a] / (g[a] - g[a + 1])
            out.append(phi[a] + t * (phi[a + 1] - phi[a]))
    return out


def analyse(eta, ref_path=None, near=None):
    near = float(os.environ.get('NEAR', 219.0)) if near is None else near
    groups = groups_at_depth3(eta)
    cands = [g for g in groups if g['path'] and g['path'][-1][1] == TARGET and g['path'][-1][0] == 0]
    info = dict(eta=eta, n_groups=len(groups), n_cands=len(cands))
    if ref_path is None:
        best = None
        for g in cands:
            d = np.min(np.abs(phi4_deg[g['idx']] - near))
            if best is None or d < best[0]:
                best = (d, g)
        grp = best[1]
    else:
        match = [g for g in cands if g['path'] == ref_path]
        if not match:
            info['path_found'] = False
            info['paths_now'] = [g['path'] for g in cands]
            return info, None
        grp = match[0]
    info['path_found'] = True
    istar, nb, sc, done, labels = rank4_scores(grp)
    info['istar'] = istar
    info['nb'] = nb
    idx = grp['idx']
    order = np.argsort(idx)
    idx_s = idx[order]
    phi = phi4_deg[idx_s]
    ok = np.ones(len(idx_s), dtype=bool)
    ok[:-1] &= (np.diff(idx_s) == 1)
    ok &= done[order]
    if 1 in sc and 4 in sc:
        g14 = (sc[1] - sc[4])[order]
        info['roots_g14'] = roots_of(phi, g14, ok)
        info['g14_min_abs'] = float(np.nanmin(np.abs(g14[ok])))
    if 4 in sc and 5 in sc:
        g45 = (sc[4] - sc[5])[order]
        info['roots_g45'] = roots_of(phi, g45, ok)
    if 1 in sc and 5 in sc:
        g15 = (sc[1] - sc[5])[order]
        info['roots_g15'] = roots_of(phi, g15, ok)
    # transitions de label reel dans la classe
    lab = np.array([sorted(l) for l in labels], dtype=object)
    labs_s = [tuple(lab[k]) for k in order[done[order]]] if False else None
    info['phi_range'] = (float(phi.min()), float(phi.max()), len(phi))
    return info, grp['path']


if __name__ == "__main__":
    t0 = time.time()
    info0, ref = analyse(0.0)
    print("eta=0 :", {k: v for k, v in info0.items()}, " (%.1fs)" % (time.time() - t0), flush=True)
    print("chemin de reference :", ref, flush=True)
    results = [info0]
    etas = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else \
        [-0.08, -0.04, -0.02, -0.01, -0.005, 0.005, 0.01, 0.02, 0.04, 0.08]
    for eta in etas:
        t1 = time.time()
        info, _ = analyse(eta, ref_path=ref)
        results.append(info)
        print("eta=%+.4f :" % eta, {k: (np.round(v, 4).tolist() if isinstance(v, list) and v and not isinstance(v[0], (tuple, frozenset)) else v)
                                    for k, v in info.items() if k not in ('eta', 'paths_now')},
              " (%.1fs)" % (time.time() - t1), flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finger_y_variation_%s.pkl' % os.environ.get('TAG','base')), 'wb') as f:
        pickle.dump(dict(results=results, ref=ref, NODE=NODE, COMP=COMP, PHI5_DEG=PHI5_DEG), f)
    print("Total %.1fs" % (time.time() - t0))
