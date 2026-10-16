"""
Stabilite perturbative a mot fixe -- test DISCRIMINANT de l'affinite (complement de finger_perturbation.py).

Pourquoi ce second script : dans finger_perturbation.py le parametre cache est un seul angle phi4 sur une fenetre
de 5 deg.  Sur une fenetre aussi etroite, toute fonction lisse de phi est affine dans (1, cos phi, sin phi) a
O(w^3) ~ 1e-4 pres : le residu hors echantillon y est quasi aveugle a la perte d'affinite.  Ici le parametre cache
est le vecteur COMPLET tau^0 in R^{N x d} (12 coordonnees), perturbe autour d'un point de reference de la chambre
de mot w = ((0,{1,2,3}),(0,{1,4,5})) par un bruit gaussien de taille delta ; la forme affine testee est

        tau^{(r)}(tau^0) = b_r + L_r tau^0        (L_r : 12 x 12, b_r : 12)

Mesures, a delta et eps fixes (gamma_1 et lambda varies separement et ensemble) :
  oos_r  = residu max hors echantillon de l'ajustement affine propre a eps (moitie des echantillons -> autre moitie)
  dev_r  = max | tau_eps - (b_r^(0) + L_r^(0) tau^0) |   (forme affine de eps = 0, ajustee a eps = 0 sur les memes tau^0)
et leurs pentes en eps (log-log) et en delta.  Attendu si l'affinite se perd a l'ordre 2 en delta : oos ~ eps delta^2.

Temoin numerique seulement.
Usage : python3 finger_perturbation_ball.py [--dt 2e-3] [--n 400] [--deltas 0.003,0.01,0.03]
"""
import sys, os, argparse, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP

N, d = core.N, core.d
REF = FP.REF
PHI4_REF = 222.5


def tau_ref():
    return core.make_tau_init(np.radians([PHI4_REF]), np.array([np.radians(FP.PHI5_DEG)]), FP.PHI1, FP.PHI2, FP.PHI3)[0]


def run_ball(tau_init, dt, g1, lam):
    """Meme pipeline que FP.run_word, mais pour un tableau (n,N,d) de traces initiales arbitraires."""
    FP.install(dt, g1, lam)
    n = tau_init.shape[0]
    groups = [core.initial_group(core.A1_kept1, tau_init)]
    taus = {1: tau_init.copy()}
    word = [None] * n
    for depth in (2, 3):
        groups, _ = core.advance_one_kairos(groups, depth, verbose=False)
        T = np.full((n, N, d), np.nan)
        for g in groups:
            T[g['idx']] = g['tau']
            for i in g['idx']:
                word[i] = g['path']
        taus[depth] = T
    T4 = np.full((n, N, d), np.nan)
    for g in groups:
        if g['path'] != REF:
            continue
        Hs, Vs, ts, Ps, done = core.run_to_kairos(g['H'], g['V'], g['tau'], g['P'], g['A'])
        T4[g['idx'][done]] = ts[done]
    taus[4] = T4
    mask = np.array([w == REF for w in word]) & ~np.isnan(T4).any(axis=(1, 2))
    return taus, mask


def fit(X0, T, idx, delta):
    X = np.concatenate([np.ones((len(idx), 1)), (X0[idx] - tau_ref().reshape(1, -1)) / delta], axis=1)
    coef, *_ = np.linalg.lstsq(X, T[idx].reshape(len(idx), -1), rcond=None)
    return coef


def ev(X0, coef, idx, delta):
    X = np.concatenate([np.ones((len(idx), 1)), (X0[idx] - tau_ref().reshape(1, -1)) / delta], axis=1)
    return X @ coef


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--n', type=int, default=400)
    ap.add_argument('--deltas', default='0.003,0.01,0.03')
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sortie_perturbation_ball.json'))
    a = ap.parse_args()
    deltas = [float(x) for x in a.deltas.split(',')]
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    eps_list = [1e-4, 1e-3, 1e-2, 1e-1]
    scans = {
        'gamma1 seul': lambda e: (e, 0.0),
        'lambda seul': lambda e: (0.0, e),
        'couple (1.25 eps, 2 eps)': lambda e: (1.25 * e, 2.0 * e),
    }
    res = {}
    for delta in deltas:
        xi = rng.standard_normal((a.n, N * d))
        X0 = tau_ref().reshape(1, -1) + delta * xi
        T_init = X0.reshape(a.n, N, d)
        taus0, mask0 = run_ball(T_init, a.dt, 0.0, 0.0)
        keep = np.flatnonzero(mask0)
        print("\n##### delta=%g : %d/%d tirages dans le mot de reference a eps=0 (%.0fs)" % (delta, len(keep), a.n, time.time() - t0), flush=True)
        if len(keep) < 60:
            print("  chambre trop etroite pour ce delta : on passe")
            continue
        tr, te = keep[::2], keep[1::2]
        fit0, row0 = {}, {}
        for r in (2, 3, 4):
            T = taus0[r]
            fit0[r] = fit(X0, T, keep, delta)
            c = fit(X0, T, tr, delta)
            oos = np.abs(T[te].reshape(len(te), -1) - ev(X0, c, te, delta)).max()
            ins = np.abs(T[keep].reshape(len(keep), -1) - ev(X0, fit0[r], keep, delta)).max()
            row0[r] = (ins, oos)
            print("  eps=0 rang %d : residu affine dans l'echantillon %.2e ; hors echantillon %.2e" % (r, ins, oos), flush=True)
        res[delta] = {'eps0': {r: row0[r] for r in row0}, 'scans': {}}
        for name, fn in scans.items():
            print("  --- %s --- (eps | in-mot | rang2 dev oos | rang3 dev oos | rang4 dev oos)" % name, flush=True)
            rows = []
            for e in eps_list:
                g1, lam = fn(e)
                taus, mask = run_ball(T_init, a.dt, g1, lam)
                kk = np.flatnonzero(mask & mask0)
                if len(kk) < 40:
                    print("   %.0e  %d/%d : mot perdu sur trop de tirages" % (e, len(kk), len(keep)))
                    rows.append(dict(eps=e, n_in=len(kk)))
                    continue
                tr2, te2 = kk[::2], kk[1::2]
                out = {}
                for r in (2, 3, 4):
                    T = taus[r]
                    dev = np.abs(T[kk].reshape(len(kk), -1) - ev(X0, fit0[r], kk, delta)).max()
                    c = fit(X0, T, tr2, delta)
                    oos = np.abs(T[te2].reshape(len(te2), -1) - ev(X0, c, te2, delta)).max()
                    out[r] = (float(dev), float(oos))
                rows.append(dict(eps=e, n_in=len(kk), m=out))
                print("   %.0e  %3d/%d | %.2e %.2e | %.2e %.2e | %.2e %.2e" %
                      (e, len(kk), len(keep), *out[2], *out[3], *out[4]), flush=True)
            ok = [x for x in rows if 'm' in x and x['eps'] <= 1e-2]
            for r in (2, 3, 4):
                if len(ok) >= 3:
                    ep = [x['eps'] for x in ok]
                    print("   rang %d : pente(dev)=%.3f  pente(oos)=%.3f ; dev/eps=%.3e ; oos/eps=%.3e (eps=%.0e)" %
                          (r, FP.slope(ep, [x['m'][r][0] for x in ok]), FP.slope(ep, [x['m'][r][1] for x in ok]),
                           ok[0]['m'][r][0] / ok[0]['eps'], ok[0]['m'][r][1] / ok[0]['eps'], ok[0]['eps']), flush=True)
            res[delta]['scans'][name] = rows
    # dependance en delta de oos/eps (coefficient de perte d'affinite) a eps = 1e-2
    print("\n=== dependance en delta (eps=1e-2) : oos/eps par rang ===")
    for name in scans:
        for r in (2, 3, 4):
            pts = []
            for delta in deltas:
                if delta in res:
                    rows = [x for x in res[delta]['scans'].get(name, []) if x.get('eps') == 1e-2 and 'm' in x]
                    if rows:
                        pts.append((delta, rows[0]['m'][r][1] / 1e-2, rows[0]['m'][r][0] / 1e-2))
            if len(pts) >= 2:
                ds = [p[0] for p in pts]
                print("  %-26s rang %d : " % (name, r) + " ; ".join("delta=%g oos/eps=%.2e dev/eps=%.2e" % p for p in pts) +
                      " | pente(oos/eps vs delta)=%.2f pente(dev/eps vs delta)=%.2f" % (FP.slope(ds, [p[1] for p in pts]), FP.slope(ds, [p[2] for p in pts])))
    json.dump(dict(args=vars(a), res=res), open(a.out, 'w'), indent=1, default=str)
    print("Total %.0fs ; resultats : %s" % (time.time() - t0, a.out))


if __name__ == "__main__":
    main()
