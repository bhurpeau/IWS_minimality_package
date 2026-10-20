"""
AUDIT du reste de Cauchy utilise dans certif_episodes.py (norm_taylor / PTaylor).

Partie A : tests unitaires de norm_taylor sur des polynomes aleatoires et des cas adverses (zero de q proche du bord du disque),
  contre un calcul INDEPENDANT a haute precision (mpmath, 120 chiffres) de s^shift sqrt(q(s)) et de son reste de Taylor :
    (A1) les coefficients g_k renvoyes sont compatibles avec ceux de mpmath (contenus dans les boules) ;
    (A2) le reste vrai |g(s) - sum_{k<=K} g_k s^k| est <= R pour s dans [0,h] (et on reporte le rapport reste_vrai/R : le majorant est-il serre ?) ;
    (A3) l'hypothese du lemme (q(s) reste dans le disque de centre q_0, rayon q_0/2 pour |s| <= r) est verifiee a posteriori sur un maillage du cercle |s| = r.
Partie B : validation croisee de PTaylor sur les pas REELS des huit episodes : pour chaque PTaylor construit par certif_episodes, on recalcule
  P(h) = e^{-k3 h} P(0) + int_0^h e^{-k3 (h-s)} g_poly(s) ds par l'integrateur rigoureux de FLINT (acb.integral, drapeau analytic controle ici),
  avec le meme terme d'erreur d'etat, et on exige que les deux enclosures de P(h) se recoupent ; on reporte le plus grand ecart |milieu1 - milieu2| / (rayon1 + rayon2).
"""
import sys, os, random, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, acb, arb_series, ctx, fmpq
import mpmath as mp
import certif_episodes as C

mp.mp.dps = 120


def poly_balls(coefs):
    return [arb(c) for c in coefs]


def mp_sqrt_series(qc, n):
    """coefficients de Taylor de sqrt(q) jusqu'a l'ordre n (mpmath, recurrence classique b_k = (q_k - sum b_j b_{k-j}) / (2 b_0))."""
    b = [mp.sqrt(qc[0])]
    for k in range(1, n + 1):
        s = qc[k] if k < len(qc) else mp.mpf(0)
        for j in range(1, k):
            s -= b[j] * b[k - j]
        b.append(s / (2 * b[0]))
    return b


def partA(ntests=60, seed=1):
    random.seed(seed)
    K = C.ORD
    worst_ratio, worst_g = 0.0, 0.0
    nfail = 0
    stats = {}
    for t in range(ntests):
        shift = random.choice([0, 0, 0, 2, 3, 4])
        n = K + 1 - shift
        kappa = random.choice([0.2, 0.5, 1.0, 2.0, 4.0])
        scale = random.choice([1.0, 0.1, 1e-3])
        # coefficients decroissants geometriquement : |c_k| ~ scale * kappa^k * U(-1,1)
        cx = [mp.mpf(random.uniform(-1, 1)) * scale * kappa ** k for k in range(n)]
        cy = [mp.mpf(random.uniform(-1, 1)) * scale * kappa ** k for k in range(n)]
        cx[0] = mp.mpf(abs(random.uniform(0.3, 1.0))) * scale
        cy[0] = mp.mpf(random.uniform(-1, 1)) * scale
        h = fmpq(random.choice([1, 2, 3, 5, 10]), random.choice([100, 300, 1000]))
        cxa = [arb(0)] * shift + [arb(mp.nstr(c, 60)) for c in cx]
        cya = [arb(0)] * shift + [arb(mp.nstr(c, 60)) for c in cy]
        try:
            g, R, mult = C.norm_taylor(cxa, cya, shift, h, K)
        except C.PressureUnsound:
            stats['unsound'] = stats.get('unsound', 0) + 1
            continue
        # q vrai (mpmath) et sa serie sqrt a l'ordre 400 pour estimer le reste vrai
        qc = [mp.mpf(0)] * (2 * n)
        for i in range(n):
            for j in range(n):
                qc[i + j] += cx[i] * cx[j] + cy[i] * cy[j]
        kk = K - shift
        bser = mp_sqrt_series(qc, 600)
        # (A1) coefficients
        for k in range(kk + 1):
            gk = g[shift + k]
            mid = mp.mpf(str(gk.mid().str(80, radius=False)))
            err = abs(mid - bser[k])
            if err > 1e-30 * (1 + abs(bser[k])):
                nfail += 1
                print("A1 ECART coefficient", t, k, mp.nstr(err, 5))
        # (A2) reste
        hf = mp.mpf(int(h.numerator)) / mp.mpf(int(h.denominator))
        Rf = mp.mpf(R.upper().mid().str(60, radius=False)) * (1 + mp.mpf('1e-40'))
        for frac in (1.0, 0.7, 0.3):
            s = hf * mp.mpf(frac)
            exact = s ** shift * mp.sqrt(sum(qc[k] * s ** k for k in range(len(qc))))
            poly = s ** shift * sum(bser[k] * s ** k for k in range(kk + 1))
            true_rem = abs(exact - poly)
            if true_rem > Rf:
                nfail += 1
                print("A2 VIOLATION du reste", t, frac, mp.nstr(true_rem, 5), ">", mp.nstr(Rf, 5))
            if Rf > 0 and true_rem > 0:
                worst_ratio = max(worst_ratio, float(true_rem / Rf))
        stats[mult] = stats.get(mult, 0) + 1
        # (A3) hypothese du lemme sur le cercle |s| = r = h * mult
        r = hf * mult
        q0 = qc[0]
        maxdev = 0
        for j in range(720):
            z = r * mp.expjpi(mp.mpf(j) / 360)
            val = sum(qc[k] * z ** k for k in range(len(qc)))
            maxdev = max(maxdev, abs(val - q0) / q0)
        if maxdev > mp.mpf('0.5') * (1 + mp.mpf('1e-12')):
            nfail += 1
            print("A3 HYPOTHESE FAUSSE", t, mp.nstr(maxdev, 5))
    print("[A] %d tests, rayons choisis (mult:nb) %s, violations %d, plus grand rapport reste_vrai/R = %.3e" % (ntests, stats, nfail, worst_ratio))
    return nfail


def sqrt_an(q, an):
    if an and not (q.real > 0):
        return acb(arb("nan"), arb("nan"))
    return q.sqrt()


def horner(cs, z):
    v = acb(0)
    for c in reversed(cs):
        v = v * z + c
    return v


def ind_integral(sl, i, shiftH, shiftV, P0, h):
    """P(h) independante : e^{-k3 h} P0 + int_0^h e^{-k3 (h-s)} (k1 s^a ||Hhat|| + k2 s^b ||Vhat||) ds + terme d'erreur d'etat."""
    cH = (sl.c[2 * i][shiftH:], sl.c[2 * i + 1][shiftH:])
    cV = (sl.c[12 + 2 * i][shiftV:], sl.c[13 + 2 * i][shiftV:])
    hf = arb(h)

    def f(z, an):
        qh = horner(cH[0], z) ** 2 + horner(cH[1], z) ** 2
        qv = horner(cV[0], z) ** 2 + horner(cV[1], z) ** 2
        g = C.k1 * (z ** shiftH) * sqrt_an(qh, an) + C.k2 * (z ** shiftV) * sqrt_an(qv, an)
        return g * (C.k3 * (z - hf)).exp()

    I = acb.integral(f, 0, hf, rel_tol=2 ** -100, abs_tol=arb("1e-60"))
    return I


def partB_hook():
    """Remplace PTaylor par une sous-classe qui valide chaque instance par l'integrateur de FLINT."""
    orig = C.PTaylor
    log = dict(n=0, worst=0.0, disjoint=0, maxmid=0.0, bad=[])

    class Checked(orig):
        def __init__(self, sl, i, P_start, h, shiftH=0, shiftV=0, K=None, minmult=None):
            super().__init__(sl, i, P_start, h, shiftH, shiftV, K, minmult)
            hf = h if isinstance(h, fmpq) else fmpq(h)
            ctx_prec = ctx.prec
            I = ind_integral(sl, i, shiftH, shiftV, P_start, hf)
            harb = arb(hf)
            hp = harb ** (C.ORD + 1)
            eH = C.norm_hi(sl.rem[2 * i], sl.rem[2 * i + 1]) * hp
            eV = C.norm_hi(sl.rem[12 + 2 * i], sl.rem[13 + 2 * i]) * hp
            Ph_ind = (-C.k3 * harb).exp() * P_start + I.real
            # terme d'erreur d'etat : (k1 eH + k2 eV) * int_0^h e^{-k3 (h-s)} ds <= (k1 eH + k2 eV) * h
            err = (C.k1 * eH + C.k2 * eV) * harb
            Ph_ind = Ph_ind + (-err).union(err)
            Ph_mine = self.ev(harb)
            log['n'] += 1
            if not Ph_ind.overlaps(Ph_mine):
                log['disjoint'] += 1
                log['bad'].append((float(sl.h), float(Ph_ind.mid()), float(Ph_mine.mid())))
            diff = abs(float(Ph_ind.mid() - Ph_mine.mid()))
            tol = float(Ph_ind.rad() + Ph_mine.rad()) + 1e-300
            log['worst'] = max(log['worst'], diff / tol)
            log['maxmid'] = max(log['maxmid'], diff)

    C.PTaylor = Checked
    return log


if __name__ == '__main__':
    t0 = time.time()
    nf = partA(ntests=int(os.environ.get('NA', 80)))
    print("[A] duree %.1f s" % (time.time() - t0))
    if os.environ.get('PARTB', '1') == '1':
        log = partB_hook()
        # execution des episodes demandes avec le crochet
        C.KMAX = int(os.environ.get('KB', 3))
        import numpy as np
        import iws_kairos_core as core
        refs = C.fref()
        X, P, t0f, init = C.episode1_start()
        A = core.A1_kept1.copy()
        for r in range(1, C.KMAX + 1):
            ref = refs[r - 1]
            if r == 1:
                rec, X2, P2, A2 = C.run_episode(1, A, X, P, ref['i'], t_init=t0f, shrink=True, init=init)
            else:
                rec, X2, P2, A2 = C.run_episode(r, A, X, P, ref['i'], hmax=fmpq(1, 100))
            print("[B] episode %d termine : %d PTaylor valides, disjoints %d, plus grand |dmilieu|/(r1+r2) = %.3g, plus grand |dmilieu| = %.3e" % (r, log['n'], log['disjoint'], log['worst'], log['maxmid']))
            X, P, A = X2, P2, A2
        print("[B] duree totale %.1f s ; cas disjoints : %s" % (time.time() - t0, log['bad'][:5]))
