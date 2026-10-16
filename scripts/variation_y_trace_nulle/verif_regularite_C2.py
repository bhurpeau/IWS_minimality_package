"""
Test DISCRIMINANT de la regularite C^2 en theta de l'application theta -> tau_eps^{(r)}(theta) (hypothese P2' du TeX).

Contexte : integrer une norme ne suffit pas a donner une fonction C^2 (ex. J(h)=int sqrt(t^2+h^2) dt ~ h^2 log(1/h)).
Si la norme de H_{i*} ou V_{i*} passait par 0 a un instant interieur pour un theta de la boule, le defaut d'affinite
serait en eps * delta^2 * log(1/delta), et non eps * delta^2.  Les pentes en delta mesurees dans la boule
(1.8-2.0 entre delta = 0.003 et 0.03) ne permettent pas de trancher.  Ici on mesure, a eps fixe et pour des delta
decroissants, la derivee seconde directionnelle par differences centrees :
        Q(delta, h) = || tau_eps(th0 + delta h) - 2 tau_eps(th0) + tau_eps(th0 - delta h) || / delta^2 ,
(h direction unitaire), puis Q/eps.  Si tau_eps est C^2 avec d_eps D^2 continue : Q/eps converge quand delta -> 0.
Si la regularite est seulement de type delta^2 log : Q/eps croit comme log(1/delta).
On verifie aussi que Q est nul a eps = 0 (arrondi) et lineaire en eps.   Temoin numerique seulement.
Usage : python3 verif_regularite_C2.py [--dt 2e-3] [--ndir 8] [--kmax 6]
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB
import finger_perturbation_depth as FD

N, d = core.N, core.d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--ndir', type=int, default=8)
    ap.add_argument('--kmax', type=int, default=6)
    ap.add_argument('--seed', type=int, default=3)
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    th0 = FB.tau_ref().reshape(-1)
    dirs = rng.standard_normal((a.ndir, N * d)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    deltas = [2.5e-4, 5e-4, 1e-3, 2e-3, 4e-3]
    ranks = list(range(2, a.kmax + 1))
    # mot de reference au centre
    taus_c, path_c = FD.run_deep(th0.reshape(1, N, d), a.dt, 0.0, 0.0, a.kmax)
    word = path_c[0]
    print("mot au centre :", [(i, sorted(s)) for i, s in word])
    scans = {'gamma1 seul': lambda e: (e, 0.0), 'lambda seul': lambda e: (0.0, e), 'couple (1.25 eps, 2 eps)': lambda e: (1.25 * e, 2.0 * e)}
    pts = [th0]
    for dl in deltas:
        for m in range(a.ndir):
            pts.append(th0 + dl * dirs[m]); pts.append(th0 - dl * dirs[m])
    pts = np.array(pts).reshape(-1, N, d)

    def evaluate(g1, lam):
        taus, path = FD.run_deep(pts, a.dt, g1, lam, a.kmax)
        ok = np.array([p == word for p in path])
        return taus, ok

    def Q_table(g1, lam):
        taus, ok = evaluate(g1, lam)
        out = np.full((len(deltas), a.ndir, len(ranks)), np.nan)
        for di, dl in enumerate(deltas):
            for m in range(a.ndir):
                ip = 1 + 2 * (di * a.ndir + m); im = ip + 1
                if not (ok[0] and ok[ip] and ok[im]):
                    continue
                for ri, r in enumerate(ranks):
                    dd = taus[r][ip] - 2 * taus[r][0] + taus[r][im]
                    out[di, m, ri] = np.linalg.norm(dd) / dl ** 2
        return out, ok

    Q0, ok0 = Q_table(0.0, 0.0)
    print("eps=0 : retention du mot sur les points : %d/%d ; max Q (devrait etre ~ arrondi/delta^2) = %.2e" %
          (ok0.sum(), len(ok0), np.nanmax(Q0)), flush=True)
    for name, fn in scans.items():
        print("\n=== %s ===" % name)
        for e in (0.02, 0.1):
            g1, lam = fn(e)
            Q, ok = Q_table(g1, lam)
            print(" eps=%.2f (mot conserve sur %d/%d points)" % (e, ok.sum(), len(ok)))
            print("   rang  " + "  ".join("d=%.2e" % dl for dl in deltas) + "   <- mediane sur directions de Q/eps")
            for ri, r in enumerate(ranks):
                row = []
                for di in range(len(deltas)):
                    v = Q[di, :, ri]; v = v[np.isfinite(v)]
                    row.append("%.3e (%d)" % (np.median(v) / e, len(v)) if len(v) else "      --     ")
                print("   %d     " % r + "  ".join(row))
        # lineaire en eps ? rapport Q(0.1)/Q(0.02)/5 sur le plus petit delta
        Qa, _ = Q_table(*fn(0.02)); Qb, _ = Q_table(*fn(0.1))
        for ri, r in enumerate(ranks):
            ra = np.nanmedian(Qb[1, :, ri] / Qa[1, :, ri]) / 5.0
            print("   rang %d : mediane de Q(eps=0.1)/Q(eps=0.02)/5 a delta=5e-4 : %.3f (1 = lineaire en eps)" % (r, ra))
    print("Total %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
