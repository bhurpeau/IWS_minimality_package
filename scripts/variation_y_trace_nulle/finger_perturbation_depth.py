"""
Stabilite perturbative a mot fixe : dependance en PROFONDEUR k du coefficient lineaire C_{K,k} (candidat, non acquis).

Meme boule de traces initiales que finger_perturbation_ball.py (delta petit, bruit gaussien sur les 12 coordonnees
de tau^0 autour du point de reference), mais on suit KMAX-1 sauts de Kairos et on retient, parmi les chemins
structurels realises a eps = 0, le plus peuple a la profondeur KMAX (mot w de longueur KMAX-2 ; rang r = r-ieme
instant de Kairos).  A eps > 0 on exige que l'echantillon realise EXACTEMENT le meme mot (sinon il est exclu et compte).
Pour chaque rang r = 2..KMAX :
   dev_r(eps) = max | tau_eps^{(r)} - (b_r^(0) + L_r^(0) tau^0) |     (forme affine de eps=0)
   oos_r(eps) = residu hors echantillon de la forme affine ajustee a eps
et C_r = dev_r/eps (a eps petit) -> croissance en r ?  (gamma_1 et lambda separement, puis ensemble.)
Le dernier rang KMAX est lu a l'instant de Kairos suivant sans appliquer le saut (comme dans les scripts precedents).

Temoin numerique seulement.   Usage : python3 finger_perturbation_depth.py [--kmax 8] [--delta 0.003] [--n 600]
"""
import sys, os, argparse, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB

N, d = core.N, core.d


def run_deep(tau_init, dt, g1, lam, kmax):
    """taus[r] pour r=1..kmax ; path[i] = chemin (tuple) de l'echantillon i apres kmax-2 sauts ; stalled -> None."""
    FP.install(dt, g1, lam)
    n = tau_init.shape[0]
    groups = [core.initial_group(core.A1_kept1, tau_init)]
    taus = {1: tau_init.copy()}
    path = [None] * n
    for depth in range(2, kmax):
        groups, _ = core.advance_one_kairos(groups, depth, verbose=False)
        T = np.full((n, N, d), np.nan)
        for g in groups:
            T[g['idx']] = g['tau']
            for i in g['idx']:
                path[i] = g['path']
        taus[depth] = T
    Tk = np.full((n, N, d), np.nan)
    for g in groups:
        Hs, Vs, ts, Ps, done = core.run_to_kairos(g['H'], g['V'], g['tau'], g['P'], g['A'])
        Tk[g['idx'][done]] = ts[done]
    taus[kmax] = Tk
    return taus, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--n', type=int, default=600)
    ap.add_argument('--delta', type=float, default=0.003)
    ap.add_argument('--kmax', type=int, default=8)
    ap.add_argument('--seed', type=int, default=11)
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sortie_perturbation_depth.json'))
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    X0 = FB.tau_ref().reshape(1, -1) + a.delta * rng.standard_normal((a.n, N * d))
    T_init = X0.reshape(a.n, N, d)
    taus0, path0 = run_deep(T_init, a.dt, 0.0, 0.0, a.kmax)
    from collections import Counter
    cnt = Counter(p for p in path0 if p is not None)
    wbest, nbest = cnt.most_common(1)[0]
    print("eps=0 : %d chemins distincts a la profondeur %d ; le plus peuple (%d/%d tirages) :" % (len(cnt), a.kmax, nbest, a.n))
    print("   w =", [(i, sorted(s)) for i, s in wbest], "  (%.0fs)" % (time.time() - t0), flush=True)
    keep0 = np.array([i for i in range(a.n) if path0[i] == wbest and not np.isnan(taus0[a.kmax][i]).any()])
    ranks = list(range(2, a.kmax + 1))
    fit0 = {r: FB.fit(X0, taus0[r], keep0, a.delta) for r in ranks}
    tr, te = keep0[::2], keep0[1::2]
    for r in ranks:
        T = taus0[r]
        ins = np.abs(T[keep0].reshape(len(keep0), -1) - FB.ev(X0, fit0[r], keep0, a.delta)).max()
        c = FB.fit(X0, T, tr, a.delta)
        oos = np.abs(T[te].reshape(len(te), -1) - FB.ev(X0, c, te, a.delta)).max()
        print("  eps=0 rang %d : residu affine dans l'echantillon %.2e ; hors echantillon %.2e" % (r, ins, oos), flush=True)
    scans = {'gamma1 seul': lambda e: (e, 0.0), 'lambda seul': lambda e: (0.0, e), 'couple (1.25 eps, 2 eps)': lambda e: (1.25 * e, 2.0 * e)}
    eps_list = [1e-3, 1e-2]
    res = {}
    for name, fn in scans.items():
        print("\n--- %s ---" % name, flush=True)
        res[name] = {}
        for e in eps_list:
            g1, lam = fn(e)
            taus, path = run_deep(T_init, a.dt, g1, lam, a.kmax)
            kk = np.array([i for i in keep0 if path[i] == wbest and not np.isnan(taus[a.kmax][i]).any()])
            lost = len(keep0) - len(kk)
            if len(kk) < 40:
                print("  eps=%.0e : mot conserve pour %d/%d seulement" % (e, len(kk), len(keep0)))
                continue
            tr2, te2 = kk[::2], kk[1::2]
            row = {}
            for r in ranks:
                T = taus[r]
                dev = np.abs(T[kk].reshape(len(kk), -1) - FB.ev(X0, fit0[r], kk, a.delta)).max()
                c = FB.fit(X0, T, tr2, a.delta)
                oos = np.abs(T[te2].reshape(len(te2), -1) - FB.ev(X0, c, te2, a.delta)).max()
                row[r] = (float(dev), float(oos))
            res[name][e] = dict(n_in=len(kk), n_lost=lost, rows=row)
            print("  eps=%.0e : mot conserve %d/%d (perdus %d)" % (e, len(kk), len(keep0), lost), flush=True)
            print("     rang :   " + "  ".join("%9d" % r for r in ranks))
            print("     dev/eps: " + "  ".join("%9.2e" % (row[r][0] / e) for r in ranks))
            print("     oos/eps: " + "  ".join("%9.2e" % (row[r][1] / e) for r in ranks))
        # croissance de C_r = dev_r/eps entre rangs consecutifs (eps = 1e-3)
        if 1e-3 in res[name]:
            C = [res[name][1e-3]['rows'][r][0] / 1e-3 for r in ranks]
            print("     rapports C_{r+1}/C_r : " + "  ".join("%.2f" % (C[i + 1] / C[i]) for i in range(len(C) - 1)))
            print("     differences C_{r+1}-C_r : " + "  ".join("%.2e" % (C[i + 1] - C[i]) for i in range(len(C) - 1)))
        if 1e-3 in res[name] and 1e-2 in res[name]:
            print("     linearite (dev(1e-2)/dev(1e-3)/10) par rang : " + "  ".join(
                "%.3f" % (res[name][1e-2]['rows'][r][0] / res[name][1e-3]['rows'][r][0] / 10) for r in ranks))
    json.dump(dict(args=vars(a), w=str(wbest), res=res), open(a.out, 'w'), indent=1, default=str)
    print("\nTotal %.0fs ; resultats : %s" % (time.time() - t0, a.out))


if __name__ == "__main__":
    main()
