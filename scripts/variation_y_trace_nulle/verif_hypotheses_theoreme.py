"""
Verification NUMERIQUE des hypotheses du theoreme de stabilite perturbative a mot fixe (temoin N=6) :
  (A3) transversalite   nu_r  = dP_{i*}/dt (t_r^0)                       (independant de theta : visible decouple)
  (A4) separation       sigma_r = Theta - max_{j != i*} P_j(t_r^0)       (idem)
  (A5) ecart            g_r   = t_r^0 - t_{r-1}^0
  (A6) marges           (i) min_j |tau_j| au Kairos ; (ii) marge de frontiere de selection (m-ieme / (m+1)-ieme
                        similarite, cote retrait et cote ajout), sur le compact K = echantillon de la boule de rayon delta
  (B2) traces non nulles sur tout l'horizon : min_{t, i, theta} |tau_i(t)|
  (B3') |H_{i*}|, |V_{i*}| minimaux sur ]0.05, t_r] (le terme ||.|| de P_{i*} est regulier la ou ils ne s'annulent pas)
Puis test de COHERENCE : le premier eps (sur la droite (gamma_1,lambda)=eps*(1.25,2)) pour lequel le mot change,
echantillon par echantillon, doit croitre avec la marge de selection a eps=0 (prediction : seuil ~ marge / sensibilite).
Temoin numerique seulement.   Usage : python3 verif_hypotheses_theoreme.py [--delta 0.03] [--n 600] [--kmax 6]
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB
import finger_perturbation_depth as FD

N, d = core.N, core.d


def run_tracked(H, V, tau, P, A, t0, dt=2e-3, Tmax=15.0):
    G = H.shape[0]
    At = core.Atilde(A); ufun = core.make_u(G)
    done = np.zeros(G, bool)
    Hs, Vs, ts, Ps = H.copy(), V.copy(), tau.copy(), P.copy()
    tst = np.full(G, np.nan)
    minH = np.full((G, N), np.inf); minV = np.full((G, N), np.inf)
    mintau = np.inf
    t = 0.0
    for step in range(int(Tmax / dt)):
        Hp, Vp, tp, Pp = H, V, tau, P
        H, V, tau, P = core.rk4_batch(H, V, tau, P, At, t, dt, ufun); t += dt
        act = ~done
        if t > 0.05 and act.any():
            minH[act] = np.minimum(minH[act], np.linalg.norm(H[act], axis=-1))
            minV[act] = np.minimum(minV[act], np.linalg.norm(V[act], axis=-1))
        if act.any():
            mintau = min(mintau, np.linalg.norm(tau[act], axis=-1).min())
        newly = (~done) & (P.max(axis=1) >= core.Theta)
        if newly.any():
            idx = np.flatnonzero(newly); ist = np.argmax(P[idx], axis=1)
            p0 = Pp[idx, ist]; p1 = P[idx, ist]
            th = np.clip((core.Theta - p0) / (p1 - p0), 0, 1)
            w2 = th[:, None]; w3 = th[:, None, None]
            Hs[idx] = Hp[idx] + w3 * (H[idx] - Hp[idx]); Vs[idx] = Vp[idx] + w3 * (V[idx] - Vp[idx])
            ts[idx] = tp[idx] + w3 * (tau[idx] - tp[idx]); Ps[idx] = Pp[idx] + w2 * (P[idx] - Pp[idx])
            Ps[idx, ist] = core.Theta
            tst[idx] = t0 + (t - dt) + th * dt
            done[idx] = True
        if done.all():
            break
    return Hs, Vs, ts, Ps, done, tst, minH, minV, mintau


def boundary_gap(tau, istar, A, pairs=None):
    """Marge de frontiere de selection, par echantillon, cote retrait (nb) et cote ajout (nn), comme dans jump_batch.
    pairs=None : paires frontieres lues dans le classement courant ; sinon (pnb, pnn) imposees (indices de noeuds,
    tableaux (G,2)) et la marge est alors SIGNEE (positive tant que le classement de reference est conserve)."""
    nb = [j for j in range(N) if A[istar, j] == 1]
    nn = [j for j in range(N) if j != istar and A[istar, j] == 0]
    m = min(2, len(nb), len(nn))
    G = tau.shape[0]
    inf = np.full(G, np.inf)
    if m == 0:
        return inf, inf, None
    S_nb = np.stack([core.cos_sim(tau[:, istar], tau[:, j]) for j in nb], axis=1)
    S_nn = np.stack([core.cos_sim(tau[:, istar], tau[:, j]) for j in nn], axis=1)
    if pairs is None:
        o_nb = np.argsort(S_nb, axis=1, kind='stable'); o_nn = np.argsort(-S_nn, axis=1, kind='stable')
        pnb = o_nb[:, m - 1:m + 1] if len(nb) > m else None
        pnn = o_nn[:, m - 1:m + 1] if len(nn) > m else None
    else:
        pnb, pnn = pairs
    r = np.arange(G)
    g_nb = (S_nb[r, pnb[:, 1]] - S_nb[r, pnb[:, 0]]) if pnb is not None else inf
    g_nn = (S_nn[r, pnn[:, 0]] - S_nn[r, pnn[:, 1]]) if pnn is not None else inf
    return g_nb, g_nn, (pnb, pnn)


def track(T_in, dt, g1, lam, njump, pairs_ref=None, verbose=False):
    """Suit l'echantillon T_in (tous supposes dans le meme mot) sur njump sauts + l'impact suivant, avec le noyau
    (gamma_1,lambda)=(g1,lam).  Retourne une liste (par impact r=1..njump) de dicts de diagnostics ; les marges de
    selection sont signees si pairs_ref (paires frontieres de reference, eps=0) est fournie."""
    FP.install(dt, g1, lam)
    G = T_in.shape[0]
    grp = core.initial_group(core.A1_kept1, T_in)
    H, V, tau, P, A = grp['H'], grp['V'], grp['tau'], grp['P'], grp['A']
    t0 = 0.0; tprev = 0.0; out = []
    for r in range(1, njump + 2):
        Hs, Vs, ts, Ps, done, tst, minH, minV, mintau = run_tracked(H, V, tau, P, A, t0, dt)
        assert done.all()
        ist = np.argmax(Ps, axis=1); assert (ist == ist[0]).all(); i = int(ist[0])
        nu = core.k1c * np.linalg.norm(Hs[:, i], axis=-1) + core.k2c * np.linalg.norm(Vs[:, i], axis=-1) - core.k3c * core.Theta
        sig = core.Theta - np.delete(Ps, i, axis=1).max(axis=1)
        pr = None if pairs_ref is None or r > njump else pairs_ref[r - 1]
        g_nb, g_nn, pairs = boundary_gap(ts, i, A, pr) if r <= njump else (np.full(G, np.inf), np.full(G, np.inf), None)
        out.append(dict(r=r, istar=i, t=tst.copy(), nu=nu, sigma=sig, mintau_kairos=np.linalg.norm(ts, axis=-1).min(axis=1),
                        g_nb=g_nb, g_nn=g_nn, pairs=pairs, minH=minH[:, i], minV=minV[:, i], mintau_run=mintau, gap=tst.mean() - tprev))
        tprev = tst.mean(); t0 = tprev
        if r > njump:
            break
        H, V, tau, P, labels, i2 = core.jump_batch(Hs, Vs, ts, Ps, A)
        if not all(l == labels[0] for l in labels):
            out[-1]['word_broken'] = True
            return out
        A = core.build_A_from_label(A, i, labels[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--n', type=int, default=600)
    ap.add_argument('--delta', type=float, default=0.03)
    ap.add_argument('--kmax', type=int, default=6)
    ap.add_argument('--seed', type=int, default=5)
    ap.add_argument('--eps_lin', type=float, default=0.02, help="eps de reference pour estimer la derivee de la marge")
    a = ap.parse_args()
    t_start = time.time()
    rng = np.random.default_rng(a.seed)
    X0 = FB.tau_ref().reshape(1, -1) + a.delta * rng.standard_normal((a.n, N * d))
    T_init = X0.reshape(a.n, N, d)
    taus0, path0 = FD.run_deep(T_init, a.dt, 0.0, 0.0, a.kmax)
    from collections import Counter
    word, nw = Counter(p for p in path0 if p is not None).most_common(1)[0]
    keep = np.array([i for i in range(a.n) if path0[i] == word])
    njump = len(word)
    print("delta=%g : mot le plus peuple (%d/%d tirages), %d sauts : %s" % (a.delta, len(keep), a.n, njump, [(i, sorted(s)) for i, s in word]))
    G = len(keep); Tk = T_init[keep]
    ref = track(Tk, a.dt, 0.0, 0.0, njump)
    pairs_ref = [o['pairs'] for o in ref[:njump]]
    print("\n r | t_r     g_r    | nu_r    sigma_r | min|tau_j|@Kairos | marge retrait (min/med) | marge ajout (min/med) | min|H_i*|  min|V_i*|")
    for o in ref:
        print(" %d | %.4f  %.4f | %.4f  %.4f  | %.4f           | %.3e / %.3e   | %.3e / %.3e   | %.3e  %.3e   (i*=%d, etalement de t* = %.1e)" %
              (o['r'], o['t'].mean(), o['gap'], o['nu'].min(), o['sigma'].min(), o['mintau_kairos'].min(), o['g_nb'].min(), np.median(o['g_nb']),
               o['g_nn'].min(), np.median(o['g_nn']), o['minH'].min(), o['minV'].min(), o['istar'], np.ptp(o['t'])))
    print("min_{t,i,theta} |tau_i(t)| sur l'horizon et tout K : %.4f" % min(o['mintau_run'] for o in ref))
    gaps0 = np.stack([np.minimum(o['g_nb'], o['g_nn']) for o in ref[:njump]], axis=1)      # (G, njump)
    margin = gaps0.min(axis=1)
    print("marge de selection minimale par echantillon : min %.3e, mediane %.3e, max %.3e" % (margin.min(), np.median(margin), margin.max()))
    # --- derivee de la marge signee en eps (differences finies) le long de la droite (gamma_1,lambda)=eps*(1.25,2)
    pert = track(Tk, a.dt, 1.25 * a.eps_lin, 2.0 * a.eps_lin, njump, pairs_ref)
    gaps1 = np.stack([np.minimum(o['g_nb'], o['g_nn']) for o in pert[:njump]], axis=1)
    h = (gaps1 - gaps0) / a.eps_lin                                                          # d(marge)/d eps, (G,njump)
    print("derivee de la marge en eps (par saut) : |h| mediane %s, max %s" % (np.round(np.median(np.abs(h), axis=0), 4), np.round(np.abs(h).max(axis=0), 4)))
    with np.errstate(divide='ignore', invalid='ignore'):
        eps_pred_r = np.where(h < 0, gaps0 / (-h), np.inf)
    eps_pred = eps_pred_r.min(axis=1)
    # --- observation : premier eps de perte du mot
    eps_grid = [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4]
    first = np.full(G, np.inf)
    for e in eps_grid:
        tt, pp = FD.run_deep(Tk, a.dt, 1.25 * e, 2.0 * e, a.kmax)
        changed = np.array([pp[j] != word for j in range(G)])
        first = np.where(np.isinf(first) & changed, e, first)
        print("  eps=%.2f : %d/%d echantillons ont perdu le mot (%.0fs)" % (e, changed.sum(), G, time.time() - t_start), flush=True)
    ok = np.isfinite(first)
    print("\nPrediction lineaire eps* = marge/|h| (h<0) : %d echantillons predits perdus avant eps=%.1f (observe : %d)" %
          ((eps_pred <= eps_grid[-1]).sum(), eps_grid[-1], ok.sum()))
    both = ok & np.isfinite(eps_pred)
    if both.sum() >= 5:
        from scipy.stats import spearmanr
        rho, pv = spearmanr(eps_pred[both], first[both])
        print("  parmi les %d echantillons perdus ET predits : Spearman(eps*, premier eps observe) = %.3f (p=%.1e) ; rapport observe/predit : mediane %.2f, quartiles %.2f - %.2f" %
              (both.sum(), rho, pv, *np.percentile(first[both] / eps_pred[both], [50, 25, 75])))
    miss = ok & ~np.isfinite(eps_pred)
    print("  perdus mais non predits (h>=0 sur tous les sauts) : %d ; predits mais non perdus avant %.1f : %d" % (miss.sum(), eps_grid[-1], ((eps_pred <= eps_grid[-1]) & ~ok).sum()))
    print("Total %.0fs" % (time.time() - t_start))


if __name__ == "__main__":
    main()
