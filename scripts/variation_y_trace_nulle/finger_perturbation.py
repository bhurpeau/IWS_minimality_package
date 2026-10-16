"""
Stabilite perturbative a mot fixe : noyau decouple (gamma_1 = lambda = 0)  ->  noyau faiblement couple.
CANDIDAT (non acquis) teste ici comme TEMOIN numerique :

    a mot w fixe, profondeur k fixee, compact K de parametres caches, horizon borne :
        sup_{theta in K} || tau_{eps,w}^{(k)}(theta) - [ b_{k,w}^{(0)} + Lambda_{k,w}^{(0)} tau^0(theta) ] || <= C_{K,k} eps

Ici : y = present de reference (N=6, A1_kept1, H(0)=V(0)=0, P(0)=(rP*Theta,0,...)), protocole u constant
(Uamp=2.5, 37 deg sur le noeud 0), parametre cache theta = phi4 = angle de tau_4(0) dans une fenetre
([220,225] deg par defaut) ou le mot de reference
        w = ((0,{1,2,3}), (0,{1,4,5}))
est realise a eps = 0.  Le noyau est le noyau COMPLET
        V' = -(gamma_0 + gamma_1 |tau_i|) V - M(tau_i) H + zeta tanh(A~ H) + u ,
        M(tau) = I - lambda/(1+(1+lambda)|tau|^2) tau tau^T ,
et l'on fait varier gamma_1 et lambda SEPAREMENT (puis ensemble) ; le mot est re-determine par la dynamique
a chaque eps (regroupement par chemin), les echantillons dont le mot a change sont exclus ET comptes.

Mesures, par rang de Kairos r in {2,3,4} (instant de franchissement P_{i*}=Theta interpole EXACTEMENT) :
  dev_r(eps)   = max_{theta, noeuds, composantes} | tau_eps - fit_0(theta) |   (fit_0 = forme affine eps=0, ajustee sur la grille)
  oos_r(eps)   = residu HORS ECHANTILLON de la forme affine ajustee a eps lui-meme
                 (ajustement sur les indices pairs, evaluation sur les impairs) : mesure la PERTE d'affinite
  ext_r(eps)   = idem mais ajustement sur le tiers central, evaluation sur les deux tiers exterieurs (extrapolation)
  pentes log-log de dev, oos en eps ; C_r = dev_r/eps (coefficient lineaire) et sa croissance avec r.

Rappel de discipline : un resultat numerique est un TEMOIN, pas une preuve.

Usage :  python3 finger_perturbation.py [--dt 2e-3] [--n 41] [--lo 220] [--hi 225] [--quick]
"""
import sys, os, argparse, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import iws_kairos_interp as KI

N, d = core.N, core.d
REF = ((0, frozenset({1, 2, 3})), (0, frozenset({1, 4, 5})))
PHI5_DEG, PHI1, PHI2, PHI3 = 349.0, np.radians(10.0), np.radians(40.0), 2.0

_G1 = 0.0
_LAM = 0.0


def rhs_coupled(H, V, tau, P, At, u):
    """Noyau complet (par noeud).  gamma_1 = lambda = 0 redonne EXACTEMENT core.rhs_batch."""
    th = np.tanh(np.einsum('ij,gjd->gid', At, H))
    nt = np.linalg.norm(tau, axis=-1)                       # (G,N)
    Gam = core.gamma0 + _G1 * nt
    c = _LAM / (1.0 + (1.0 + _LAM) * nt ** 2)
    MH = H - (c * (tau * H).sum(-1))[..., None] * tau
    dH = V
    dV = -Gam[..., None] * V - MH + core.zeta * th + u
    dtau = core.alpha * th - core.beta * tau
    dP = core.k1c * np.linalg.norm(H, axis=-1) + core.k2c * np.linalg.norm(V, axis=-1) - core.k3c * P
    return dH, dV, dtau, dP


def install(dt, g1, lam):
    """Branche le noyau couple et l'interpolation exacte de l'instant de Kairos dans le coeur."""
    global _G1, _LAM
    _G1, _LAM = float(g1), float(lam)
    core.rhs_batch = rhs_coupled
    f = lambda H, V, tau, P, A, dt_=dt, Tmax=15.0: KI.run_to_kairos_interp(H, V, tau, P, A, dt_, Tmax)
    core.run_to_kairos = f


def run_word(phi_deg, dt, g1, lam):
    """Retourne taus[r] (n,N,d) pour r=1..4, mask (mot == REF et r=4 atteint), nombre de mots distincts."""
    install(dt, g1, lam)
    n = len(phi_deg)
    tau_init = core.make_tau_init(np.radians(phi_deg), np.full(n, np.radians(PHI5_DEG)), PHI1, PHI2, PHI3)
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
        ix = g['idx'][done]
        T4[ix] = ts[done]
    taus[4] = T4
    mask = np.array([w == REF for w in word]) & ~np.isnan(T4).any(axis=(1, 2))
    nwords = len({w for w in word if w is not None})
    return taus, mask, nwords


def design(phi_rad):
    return np.stack([np.ones_like(phi_rad), np.cos(phi_rad), np.sin(phi_rad)], axis=1)


def affine_coef(phi_rad, T, idx):
    """T : (n,N,d) ; ajustement tau_{j,c}(phi) = b + m1 cos + m2 sin sur les indices idx."""
    X = design(phi_rad[idx])
    Y = T[idx].reshape(len(idx), -1)
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
    return coef


def affine_eval(phi_rad, coef, shape):
    return (design(phi_rad) @ coef).reshape((len(phi_rad),) + shape)


def measures(phi_deg, taus, mask, fit0):
    phi = np.radians(phi_deg)
    out = {}
    for r in (2, 3, 4):
        T = taus[r]
        m = np.flatnonzero(mask)
        if len(m) < 9:
            out[r] = None
            continue
        dev = np.abs(T[m] - affine_eval(phi[m], fit0[r], T.shape[1:])).max()
        tr, te = m[::2], m[1::2]
        c = affine_coef(phi, T, tr)
        oos = np.abs(T[te] - affine_eval(phi[te], c, T.shape[1:])).max()
        lo_i, hi_i = m[len(m) // 3], m[2 * len(m) // 3]
        mid = m[(m >= lo_i) & (m <= hi_i)]
        outer = np.setdiff1d(m, mid)
        c2 = affine_coef(phi, T, mid)
        ext = np.abs(T[outer] - affine_eval(phi[outer], c2, T.shape[1:])).max() if len(outer) else np.nan
        out[r] = dict(dev=float(dev), oos=float(oos), ext=float(ext))
    return out


def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = (y > 0) & np.isfinite(y)
    if ok.sum() < 3:
        return float('nan')
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dt', type=float, default=2e-3)
    ap.add_argument('--n', type=int, default=41)
    ap.add_argument('--lo', type=float, default=220.0)
    ap.add_argument('--hi', type=float, default=225.0)
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sortie_perturbation.json'))
    a = ap.parse_args()
    phi_deg = np.linspace(a.lo, a.hi, a.n)
    t0 = time.time()

    # --- reference eps = 0 (verifie au passage que le noyau couple a 0 reproduit le noyau decouple)
    taus0, mask0, nw0 = run_word(phi_deg, a.dt, 0.0, 0.0)
    print("eps=0 : %d/%d echantillons dans le mot de reference (%d mots distincts), %.0fs" % (mask0.sum(), a.n, nw0, time.time() - t0), flush=True)
    assert mask0.all(), "le mot de reference doit etre realise sur toute la fenetre a eps=0 : changer --lo/--hi"
    phi = np.radians(phi_deg)
    fit0, res0 = {}, {}
    for r in (2, 3, 4):
        idx = np.arange(a.n)
        fit0[r] = affine_coef(phi, taus0[r], idx)
        res0[r] = float(np.abs(taus0[r] - affine_eval(phi, fit0[r], taus0[r].shape[1:])).max())
        # oos a eps = 0
        c = affine_coef(phi, taus0[r], idx[::2])
        oos = float(np.abs(taus0[r][1::2] - affine_eval(phi[1::2], c, taus0[r].shape[1:])).max())
        print("  rang %d : residu affine (dans l'echantillon) = %.2e ; hors echantillon (pairs->impairs) = %.2e" % (r, res0[r], oos), flush=True)

    eps_list = [1e-5, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1] if a.quick else \
               [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
    G1_REF, LAM_REF = 1.25, 2.0
    results = {}
    # (nom, fonction eps -> (g1, lam)) : echelle absolue ET echelle relative a la valeur de reference
    scans = {
        'gamma1 seul (gamma_1=eps, lambda=0)': lambda e: (e, 0.0),
        'lambda seul (lambda=eps, gamma_1=0)': lambda e: (0.0, e),
        'couple (gamma_1=eps*1.25, lambda=eps*2)': lambda e: (e * G1_REF, e * LAM_REF),
    }
    for name, fn in scans.items():
        print("\n=== %s ===" % name, flush=True)
        print("   eps       in-mot  mots |  rang2: dev  oos  ext |  rang3: dev  oos  ext |  rang4: dev  oos  ext", flush=True)
        rows = []
        for e in eps_list:
            g1, lam = fn(e)
            taus, mask, nw = run_word(phi_deg, a.dt, g1, lam)
            ms = measures(phi_deg, taus, mask, fit0)
            rows.append(dict(eps=e, g1=g1, lam=lam, n_in=int(mask.sum()), nwords=nw, m=ms))
            def fmt(r):
                x = ms[r]
                return "%.2e %.2e %.2e" % (x['dev'], x['oos'], x['ext']) if x else "     -- (mot perdu)      "
            print("  %.0e  %3d/%d  %2d | %s | %s | %s" % (e, mask.sum(), a.n, nw, fmt(2), fmt(3), fmt(4)), flush=True)
        results[name] = rows
        # pentes log-log et coefficient lineaire (sur les eps ou le mot est conserve en entier)
        full = [x for x in rows if x['n_in'] == a.n and x['eps'] <= 1e-2 and all(x['m'][r] for r in (2, 3, 4))]
        for r in (2, 3, 4):
            if len(full) >= 3:
                ep = [x['eps'] for x in full]
                sd = slope(ep, [x['m'][r]['dev'] for x in full])
                so = slope(ep, [x['m'][r]['oos'] for x in full])
                se = slope(ep, [x['m'][r]['ext'] for x in full])
                C = full[0]['m'][r]['dev'] / full[0]['eps']
                Co = full[0]['m'][r]['oos'] / full[0]['eps']
                print("   rang %d : pente(dev)=%.3f  pente(oos)=%.3f  pente(ext)=%.3f | C_dev=dev/eps(eps=%.0e)=%.3e  C_oos=%.3e" %
                      (r, sd, so, se, full[0]['eps'], C, Co), flush=True)

    # --- pleine force : valeurs de reference de l'Annexe F
    print("\n=== pleine force (Annexe F : gamma_1=1.25, lambda=2) et intermediaires ===", flush=True)
    full_rows = []
    for (g1, lam) in [(0.0, LAM_REF), (G1_REF, 0.0), (G1_REF, LAM_REF), (0.125, 0.2), (0.0125, 0.02)]:
        taus, mask, nw = run_word(phi_deg, a.dt, g1, lam)
        ms = measures(phi_deg, taus, mask, fit0)
        full_rows.append(dict(g1=g1, lam=lam, n_in=int(mask.sum()), nwords=nw, m=ms))
        def fmt(r):
            x = ms[r]
            return "dev=%.2e oos=%.2e ext=%.2e" % (x['dev'], x['oos'], x['ext']) if x else "(mot perdu)"
        print("  g1=%.4g lam=%.4g : in-mot %d/%d, %d mots | r2 %s | r3 %s | r4 %s" % (g1, lam, mask.sum(), a.n, nw, fmt(2), fmt(3), fmt(4)), flush=True)
    results['pleine force'] = full_rows
    json.dump(dict(args=vars(a), res0=res0, results=results), open(a.out, 'w'), indent=1, default=str)
    print("\nTotal %.0fs ; resultats : %s" % (time.time() - t0, a.out))


if __name__ == "__main__":
    main()
