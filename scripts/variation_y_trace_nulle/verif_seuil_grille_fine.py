"""
Controle de l'attribution du facteur ~1.92 (seuil de perte du mot observe / predit marge/|h|) :
la grille d'eps du premier test etait grossiere (rapport 1.4 a 2 entre valeurs successives) donc le premier eps
observe surestime le vrai seuil.  Ici : grille GEOMETRIQUE fine (rapport 1.06) le long de (gamma_1,lambda)=eps*(1.25,2),
meme echantillon que verif_hypotheses_theoreme.py (delta=0.003, seed=5, kmax=8), puis comparaison au seuil predit
eps* = marge/|h| (h par differences finies a eps=0.02).  Le seuil vrai est dans ]eps_precedent, eps_observe] ;
on rapporte observe/predit et precedent/predit (bornes).   Temoin numerique seulement.
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation_ball as FB
import finger_perturbation_depth as FD
import verif_hypotheses_theoreme as V

N, d = core.N, core.d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--n', type=int, default=600)
    ap.add_argument('--delta', type=float, default=0.003)
    ap.add_argument('--kmax', type=int, default=8)
    ap.add_argument('--seed', type=int, default=5)
    ap.add_argument('--ratio', type=float, default=1.06)
    ap.add_argument('--eps_lin', type=float, default=0.02)
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    X0 = FB.tau_ref().reshape(1, -1) + a.delta * rng.standard_normal((a.n, N * d))
    T_init = X0.reshape(a.n, N, d)
    taus0, path0 = FD.run_deep(T_init, a.dt, 0.0, 0.0, a.kmax)
    from collections import Counter
    word, _ = Counter(p for p in path0 if p is not None).most_common(1)[0]
    keep = np.array([i for i in range(a.n) if path0[i] == word]); njump = len(word); G = len(keep); Tk = T_init[keep]
    ref = V.track(Tk, a.dt, 0.0, 0.0, njump)
    pairs_ref = [o['pairs'] for o in ref[:njump]]
    gaps0 = np.stack([np.minimum(o['g_nb'], o['g_nn']) for o in ref[:njump]], axis=1)
    pert = V.track(Tk, a.dt, 1.25 * a.eps_lin, 2.0 * a.eps_lin, njump, pairs_ref)
    gaps1 = np.stack([np.minimum(o['g_nb'], o['g_nn']) for o in pert[:njump]], axis=1)
    h = (gaps1 - gaps0) / a.eps_lin
    with np.errstate(divide='ignore', invalid='ignore'):
        eps_pred = np.where(h < 0, gaps0 / (-h), np.inf).min(axis=1)
    print("echantillon : %d tirages, %d sauts ; predits perdus avant 1.5 : %d" % (G, njump, (eps_pred <= 1.5).sum()), flush=True)
    grid = [0.02]
    while grid[-1] < 1.5:
        grid.append(grid[-1] * a.ratio)
    first = np.full(G, np.inf); prev = np.full(G, 0.0)
    last_ok = np.full(G, 0.0)
    for e in grid:
        tt, pp = FD.run_deep(Tk, a.dt, 1.25 * e, 2.0 * e, a.kmax)
        changed = np.array([pp[j] != word for j in range(G)])
        newly = np.isinf(first) & changed
        first[newly] = e; prev[newly] = last_ok[newly]
        last_ok[~changed & np.isinf(first)] = e
        print("  eps=%.4f : %d/%d perdus (%.0fs)" % (e, changed.sum(), G, time.time() - t0), flush=True)
    ok = np.isfinite(first) & np.isfinite(eps_pred)
    r_hi = first[ok] / eps_pred[ok]; r_lo = prev[ok] / eps_pred[ok]
    print("\n%d echantillons perdus et predits (sur %d perdus). Seuil vrai dans ]prev, obs] :" % (ok.sum(), np.isfinite(first).sum()))
    print("  obs/pred : mediane %.3f, quartiles %.3f - %.3f" % (np.median(r_hi), *np.percentile(r_hi, [25, 75])))
    print("  prev/pred : mediane %.3f, quartiles %.3f - %.3f" % (np.median(r_lo), *np.percentile(r_lo, [25, 75])))
    from scipy.stats import spearmanr
    print("  Spearman(pred, obs) = %.3f" % spearmanr(eps_pred[ok], first[ok])[0])
    # dependance du rapport avec la taille de eps_pred (courbure => rapport croissant avec eps)
    q = np.quantile(eps_pred[ok], [0, 0.25, 0.5, 0.75, 1.0])
    for lo, hi in zip(q[:-1], q[1:]):
        m = (eps_pred[ok] >= lo) & (eps_pred[ok] <= hi)
        print("  eps_pred dans [%.3f, %.3f] : obs/pred mediane %.3f (n=%d)" % (lo, hi, np.median(r_hi[m]), m.sum()))
    print("Total %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
