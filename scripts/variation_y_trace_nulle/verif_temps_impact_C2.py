"""
Regularite C^2 des TEMPS D'IMPACT T_r(theta, eps) du noyau couple, a mot fixe (temoin N=6) -- lemme de transmission.

Le lemme de transmission (TeX regularite_P2_transmission.tex) affirme : si la pression pre-impact P~_r est C^2 en (t,theta)
avec derivees d'ordre 2 en theta de classe C^1 en eps, alors T_r l'est aussi (IFT), et les reinitialisations
des episodes precedents n'y font pas obstacle (termes de bord de la formule de Leibniz).  Ici on mesure directement
          Q_T(delta,h) = | T_r(th0 + delta h) - 2 T_r(th0) + T_r(th0 - delta h) | / delta^2
(h direction unitaire de R^12) a eps fixe, puis Q_T/eps.  Attendu si T_r est C^2 avec d_eps D^2_theta T_r continue :
 (i) Q_T = 0 a eps = 0 (le visible est independant de theta, T_r est constant : autonomie conditionnelle) ;
 (ii) Q_T/eps converge quand delta -> 0 (pas de facteur log(1/delta)) et est ~ constant en eps.
Instants exacts par interpolation lineaire de P_{i*} = Theta a l'interieur du pas ; temps cumules sur les episodes.
Temoin numerique seulement (O(dt^2) d'erreur d'interpolation).
Usage : python3 verif_temps_impact_C2.py [--dt 2e-3] [--ndir 6] [--kmax 7]
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB

N, d = core.N, core.d


def run_episode_timed(H, V, tau, P, A, dt, Tmax=15.0):
    """Comme iws_kairos_interp.run_to_kairos_interp, mais renvoie aussi la duree de l'episode (interpolee)."""
    G = H.shape[0]
    At = core.Atilde(A)
    ufun = core.make_u(G)
    done = np.zeros(G, dtype=bool)
    Hs, Vs, ts, Ps = H.copy(), V.copy(), tau.copy(), P.copy()
    dur = np.full(G, np.nan)
    t = 0.0
    for step in range(int(Tmax / dt)):
        Hp, Vp, tp, Pp = H, V, tau, P
        H, V, tau, P = core.rk4_batch(H, V, tau, P, At, t, dt, ufun)
        newly = (~done) & (P.max(axis=1) >= core.Theta)
        if newly.any():
            idx = np.flatnonzero(newly)
            ist = np.argmax(P[idx], axis=1)
            p0 = Pp[idx, ist]; p1 = P[idx, ist]
            th = np.clip((core.Theta - p0) / (p1 - p0), 0.0, 1.0)
            w2 = th[:, None]; w3 = th[:, None, None]
            Hs[idx] = Hp[idx] + w3 * (H[idx] - Hp[idx])
            Vs[idx] = Vp[idx] + w3 * (V[idx] - Vp[idx])
            ts[idx] = tp[idx] + w3 * (tau[idx] - tp[idx])
            Ps[idx] = Pp[idx] + w2 * (P[idx] - Pp[idx])
            Ps[idx, ist] = core.Theta
            dur[idx] = t + th * dt
            done[idx] = True
        t += dt
        if done.all():
            break
    return Hs, Vs, ts, Ps, done, dur


def impact_times(theta_flat, dt, g1, lam, kmax, ref_path=None):
    """Temps d'impact cumules T_1..T_kmax pour chaque ligne de theta_flat ; NaN si le mot differe de ref_path
    (ref_path = liste de (istar, label) fixee par le centre).  Le k-ieme saut n'est pas applique au dernier rang."""
    FP.install(dt, g1, lam)
    n = theta_flat.shape[0]
    tau = theta_flat.reshape(n, N, d).copy()
    grp = core.initial_group(core.A1_kept1, tau)
    H, V, P, A = grp['H'], grp['V'], grp['P'], grp['A']
    alive = np.ones(n, dtype=bool)
    T = np.full((n, kmax), np.nan)
    cum = np.zeros(n)
    path = []
    for r in range(kmax):
        Hs, Vs, ts, Ps, done, dur = run_episode_timed(H, V, tau, P, A, dt)
        alive &= done
        cum = cum + np.where(done, dur, np.nan)
        T[:, r] = np.where(alive, cum, np.nan)
        if r == kmax - 1:
            break
        H2, V2, tau2, P2, labels, i2 = core.jump_batch(Hs, Vs, ts, Ps, A)
        key = [(int(i2[k]), tuple(sorted(labels[k]))) for k in range(n)]
        if ref_path is None:
            ref = key[0]
        else:
            ref = ref_path[r]
        path.append(ref)
        same = np.array([key[k] == ref for k in range(n)])
        alive &= same
        A = core.build_A_from_label(A, ref[0], set(ref[1]))
        H, V, tau, P = H2, V2, tau2, P2
    return T, alive, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--ndir', type=int, default=6)
    ap.add_argument('--kmax', type=int, default=7)
    ap.add_argument('--seed', type=int, default=4)
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    th0 = FB.tau_ref().reshape(-1)
    dirs = rng.standard_normal((a.ndir, N * d)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    deltas = [5e-4, 1e-3, 2e-3, 4e-3]
    pts = [th0]
    for dl in deltas:
        for m in range(a.ndir):
            pts.append(th0 + dl * dirs[m]); pts.append(th0 - dl * dirs[m])
    pts = np.array(pts)
    # mot de reference au centre (eps = 0)
    Tc, okc, path = impact_times(th0.reshape(1, -1), a.dt, 0.0, 0.0, a.kmax)
    print("mot au centre (istar, retire/ajoute) :", path)
    print("T_r au centre (eps=0) :", np.round(Tc[0], 5))
    print("eps=0 : les T_r ne dependent pas de theta (autonomie conditionnelle) : ecart max sur les points :", flush=True)
    T0, ok0, _ = impact_times(pts, a.dt, 0.0, 0.0, a.kmax, path)
    print("   ", np.nanmax(np.abs(T0 - Tc[0]), axis=0), " (mot conserve %d/%d)" % (ok0.sum(), len(ok0)), flush=True)

    def Qtab(g1, lam):
        T, ok, _ = impact_times(pts, a.dt, g1, lam, a.kmax, path)
        out = np.full((len(deltas), a.ndir, a.kmax), np.nan)
        for di, dl in enumerate(deltas):
            for m in range(a.ndir):
                ip = 1 + 2 * (di * a.ndir + m); im = ip + 1
                if ok[0] and ok[ip] and ok[im]:
                    out[di, m] = np.abs(T[ip] - 2 * T[0] + T[im]) / dl ** 2
        return out, ok

    for name, fn in {'gamma1 seul': lambda e: (e, 0.0), 'lambda seul': lambda e: (0.0, e),
                     'couple (1.25 eps, 2 eps)': lambda e: (1.25 * e, 2.0 * e)}.items():
        print("\n=== %s ===" % name)
        res = {}
        for e in (0.02, 0.1):
            Q, ok = Qtab(*fn(e)); res[e] = Q
            print(" eps=%.2f (mot conserve %d/%d points)   mediane sur directions de Q_T/eps :" % (e, ok.sum(), len(ok)))
            print("   rang  " + "  ".join("d=%.1e" % dl for dl in deltas))
            for r in range(a.kmax):
                row = []
                for di in range(len(deltas)):
                    v = res[e][di, :, r]; v = v[np.isfinite(v)]
                    row.append("%.3e" % (np.median(v) / e) if len(v) else "    --    ")
                print("   %d     " % (r + 1) + "  ".join(row))
        print("   rapport Q_T(eps=0.1)/Q_T(eps=0.02)/5 a delta=1e-3 (1 = lineaire en eps) :",
              np.round(np.nanmedian(res[0.1][1] / res[0.02][1], axis=0) / 5.0, 3))
    print("Total %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
