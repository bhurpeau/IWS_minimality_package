"""
CERTIFICATS DES EPISODES 1..K (trajectoire de base, q0 = (theta, eps) = (0, 0), graphe initial A_1 = kept1) -- arithmetique de boules.

Generalisation de certif_rang1.py (pilote, conserve tel quel).  Pour chaque episode r :
  * integrateur de Taylor valide (ordre ORD, enclosure a priori de Picard, reste de Lagrange) pour (H,V,tau) in R^36, graphe A_r courant ;
  * les SIX pressions P_j par la formule de Duhamel (quadrature centree sur M morceaux par pas, reste borne par l'oscillation de la derivee
    de l'integrande), avec majorant rigoureux de P_j sur chaque morceau ;
  * premier franchissement de Theta par la pression du declencheur attendu i_r : pente > 0 sur le pas, pas ou P_i atteint Theta, bissection
    du temps d'impact T_r in [T_r^-, T_r^+] ; toutes les autres pressions < Theta sur [0, T_r^+] ;
  * (H5) minorants de ||tau_j|| et (H2) minorants de ||V_j||, ||H_j|| sur [0, T_r + delta] ;
  * (H1) selection de recablage par cosinus (marges certifiees) ; reset V_i <- r_V V_i, P_i <- r_P Theta ; nouvelle boite pour l'episode r+1.
L'etat au franchissement est la reunion des evaluations sur [T^-, T^+] (autonomie : (H,V,tau) autonome a eps = 0, forcage constant sur le noeud 0).
Episode 1 : depart au repos, developpement en t = 0 sur [0, t0] (coefficients d'annulation exactement nuls, quotients minores), puis meme boucle.
Statut : calcul assiste par ordinateur (python-flint / Arb) ; les entrees (tau_ref en doubles, U) sont prises comme exactes.
"""
import sys, os, time, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from flint import arb, arb_series, ctx, fmpq
import numpy as np
import iws_kairos_core as core
import verif_profondeur_propagation as VP
import zero_V0_lib as Z

PREC, ORD = int(os.environ.get('PREC', 192)), int(os.environ.get('ORD', 24))
MPIECES = int(os.environ.get('MPIECES', 32))
TIGHTEN = int(os.environ.get('TIGHTEN', 6))
MINMULT = int(os.environ.get('MINMULT', 8))
KMAX = int(os.environ.get('KMAX', 8))
ctx.prec = PREC


# ---- arrondi dirige
def _exq(p):
    assert p.rad() == 0
    m, e = p.man_exp()
    m, e = int(m), int(e)
    return fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, 2 ** (-e))
def exq_lo(x): return _exq(x.lower())
def exq_hi(x): return _exq(x.upper())
def _dec(q, d, upflag):
    fr = Fraction(int(q.numerator), int(q.denominator)) * 10 ** d
    n = math.ceil(fr) if upflag else math.floor(fr)
    sgn = '-' if n < 0 else ''
    n = abs(n); ip, fp = divmod(n, 10 ** d)
    return "%s%d.%0*d" % (sgn, ip, d, fp)
def dn(x, d=6): return _dec(x if isinstance(x, fmpq) else exq_lo(x), d, False)
def up(x, d=6): return _dec(x if isinstance(x, fmpq) else exq_hi(x), d, True)
def qs(q): return "%d/%d" % (int(q.numerator), int(q.denominator))


def q(a, b=1): return arb(fmpq(a, b))

zeta, alpha, beta, gamma0 = q(4, 5), q(9, 20), q(3, 25), q(1, 4)
k1, k2, k3, Theta, rP, rV = q(3, 5), q(2, 5), q(1, 2), q(5, 4), q(7, 20), q(1, 2)
assert (core.zeta, core.alpha, core.beta, core.gamma0, core.k1c, core.k2c, core.k3c, core.Theta, core.rP, core.rV) == (0.8, 0.45, 0.12, 0.25, 0.6, 0.4, 0.5, 1.25, 0.35, 0.5)
ang = arb.pi() * 37 / 180
U = [q(5, 2) * ang.cos(), q(5, 2) * ang.sin()]
TAU0 = [arb(float(v)) for v in VP.tau0.reshape(-1)]
NODE_M = {0: 0, 1: 1, 4: 1, 5: 1, 2: 2, 3: 2}


def tanh_s(z):
    e = (z * 2).exp()
    return (e - 1) / (e + 1)

def norm_lo(a, b):
    la, lb = a.abs_lower(), b.abs_lower()
    return (la * la + lb * lb).sqrt()

def norm_hi(a, b):
    ua, ub = a.abs_upper(), b.abs_upper()
    return (ua * ua + ub * ub).sqrt()

def nrm_ball(a, b):
    return norm_lo(a, b).union(norm_hi(a, b))


def nrm_series(a, b):
    """norme euclidienne d'une serie (a, b) : terme constant impose par abs_lower/abs_upper (la positivite de a*a se perd sur les boules larges)."""
    a0, b0 = a.coeffs()[0], b.coeffs()[0]
    c0 = (a0.abs_lower() ** 2 + b0.abs_lower() ** 2).union(a0.abs_upper() ** 2 + b0.abs_upper() ** 2)
    cs = list((a * a + b * b).coeffs())
    cs[0] = c0
    return arb_series(cs).sqrt()


class Model:
    """Champ de vecteurs (H,V,tau) pour un graphe donne."""
    def __init__(self, Aadj):
        self.A = Aadj.copy()
        self.At = [[None] * 6 for _ in range(6)]
        for i in range(6):
            deg1 = int(Aadj[i].sum()) + 1
            for j in range(6):
                self.At[i][j] = q(1, deg1) if (Aadj[i, j] == 1 or i == j) else None
        self.Fser = self._make(True)
        self.Fsca = self._make(False)

    def _make(self, series):
        th_fn = tanh_s if series else (lambda z: z.tanh())
        At = self.At

        def F(x):
            th = []
            for i in range(6):
                for c in range(2):
                    acc = None
                    for j in range(6):
                        a = At[i][j]
                        if a is None:
                            continue
                        term = a * x[2 * j + c]
                        acc = term if acc is None else acc + term
                    th.append(th_fn(acc))
            out = [None] * 36
            for k in range(12):
                out[k] = x[12 + k]
                v = -gamma0 * x[12 + k] - x[k] + zeta * th[k]
                out[12 + k] = v + U[k % 2] if k // 2 == 0 else v
                out[24 + k] = alpha * th[k] - beta * x[24 + k]
            return out
        return F


_models = {}
def get_model(Aadj):
    key = Aadj.tobytes()
    if key not in _models:
        _models[key] = Model(Aadj)
    return _models[key]


def jets(model, x0, n):
    ctx.cap = n + 1
    dim = len(x0)
    F = model.Fser
    x = [arb_series([c]) for c in x0]
    for _ in range(n):
        f = F(x)
        x = [arb_series([x0[i]]) + f[i].integral() for i in range(dim)]
    return [list(s.coeffs()) + [arb(0)] * (n + 1 - len(s.coeffs())) for s in x]


def hull_inflate(b, rel=q(1, 4)):
    r = b.rad() * rel + arb("1e-70")
    return b + (-r).union(r)


def apriori(model, X, h):
    dim = len(X)
    F = model.Fsca
    hI = arb(0).union(h)
    F0 = F(X)
    B = [X[i] + hI * F0[i] for i in range(dim)]
    for _ in range(80):
        Bi = [hull_inflate(b) for b in B]
        FB = F(Bi)
        Bn = [X[i] + hI * FB[i] for i in range(dim)]
        if all(Bi[i].contains(Bn[i]) for i in range(dim)):
            # raffinement : B <- X + [0,h] F(B) est encore une enclosure (l'operateur de Picard preserve l'inclusion)
            Bc = Bn
            for _ in range(TIGHTEN):
                FB = F(Bc)
                Bc = [X[i] + hI * FB[i] for i in range(dim)]
            # la solution est dans Bc ; on le rend un peu plus large pour le reste de Lagrange (securite : intersection non necessaire)
            return Bc
        B = [Bi[i].union(Bn[i]) for i in range(dim)]
    raise RuntimeError("enclosure a priori non trouvee (h trop grand)")


class Slab:
    def __init__(self, model, X, h):
        self.model, self.h = model, h
        dim = len(X)
        self.dim = dim
        self.c = jets(model, X, ORD)
        self.B = apriori(model, X, h)
        cB = jets(model, self.B, ORD + 1)
        self.rem = [ci[ORD + 1] for ci in cB]
        hp = [arb(1)]
        for _ in range(ORD + 1):
            hp.append(hp[-1] * h)
        self.end = [sum((self.c[i][k] * hp[k] for k in range(ORD + 1)), arb(0)) + self.rem[i] * hp[ORD + 1] for i in range(dim)]

    def ev(self, S, i):
        c = self.c[i]
        v = c[ORD]
        for k in range(ORD - 1, -1, -1):
            v = v * S + c[k]
        return v + self.rem[i] * S ** (ORD + 1)

    def vec(self, S):
        return [self.ev(S, i) for i in range(self.dim)]


class PressureUnsound(Exception):
    pass


def norm_taylor(cx, cy, shift, h, K, minmult=None):
    """Developpement de s -> s^shift sqrt(qhat(s)), qhat = xhat^2 + yhat^2, ou x(s) = s^shift xhat(s), y(s) = s^shift yhat(s) sont des polynomes
    (coefficients cx, cy de degre <= ORD, les coefficients d'indice < shift etant exactement nuls).
    Renvoie (coefficients g_0..g_K, borne R de |s^shift sqrt(qhat) - somme_{k<=K} g_k s^k| sur [0,h]).
    Reste : estimee de Cauchy ; sqrt(qhat) est holomorphe sur |s| < r des que sum_{k>=1} |q_k| r^k <= q_0/2 (q reste dans le disque de centre q_0, rayon q_0/2),
    avec |sqrt(qhat)| <= sqrt(3 q_0 / 2) sur le disque, d'ou |coefficient_k| <= M / r^k et un reste <= M x^(K-shift+1) / (1 - x), x = h/r."""
    n = len(cx) - shift
    ctx.cap = 2 * n + 2
    ax, ay = arb_series(list(cx[shift:])), arb_series(list(cy[shift:]))
    qs_ = ax * ax + ay * ay
    qc = list(qs_.coeffs())
    q0lo = (cx[shift].abs_lower() ** 2 + cy[shift].abs_lower() ** 2)
    if not (q0lo > 0):
        raise PressureUnsound("terme constant non positif")
    qabs = [c.abs_upper() for c in qc]
    best = None
    for mult in [m_ for m_ in (64, 48, 32, 24, 16, 12, 8, 6, 4, 3, 2) if m_ >= (MINMULT if minmult is None else minmult)]:
        r = arb(h * mult)
        Sr = arb(0)
        rk = arb(1)
        for k in range(1, len(qabs)):
            rk = rk * r
            Sr = Sr + qabs[k] * rk
        if Sr <= q0lo / 2:
            best = mult
            break
    if best is None:
        raise PressureUnsound("rayon de Cauchy insuffisant")
    x = arb(fmpq(1, best))
    q0up = qc[0].abs_upper()
    Mbound = (q0up * 3 / 2).sqrt()
    kk = K - shift
    ctx.cap = kk + 1
    sq = arb_series(qc[:kk + 1]).sqrt()
    sc = list(sq.coeffs()) + [arb(0)] * (kk + 1 - len(sq.coeffs()))
    g = [arb(0)] * shift + sc
    R = (arb(h) ** shift) * Mbound * x ** (kk + 1) / (1 - x)
    return g[:K + 1], R, best


class PTaylor:
    """Pression P_i d'un noeud sur un pas [0,h] : P' = k1 ||H_i|| + k2 ||V_i|| - k3 P.  Polynome de Taylor (coefficients boules) + reste rigoureux
    |P - P_poly| <= h (k1 (R_H + e_H) + k2 (R_V + e_V) + k3 |P_{K+1}| h^(K+1)),  e = norme du reste de Lagrange de l'etat (la norme est 1-lipschitzienne)."""
    def __init__(self, sl, i, P_start, h, shiftH=0, shiftV=0, K=None, minmult=None):
        K = ORD if K is None else K
        self.K = K
        hf = fmpq(h) if not isinstance(h, fmpq) else h
        gH, RH, mH = norm_taylor(sl.c[2 * i], sl.c[2 * i + 1], shiftH, hf, K, minmult)
        gV, RV, mV = norm_taylor(sl.c[12 + 2 * i], sl.c[13 + 2 * i], shiftV, hf, K, minmult)
        harb = arb(hf)
        hp = harb ** (ORD + 1)
        eH = norm_hi(sl.rem[2 * i], sl.rem[2 * i + 1]) * hp
        eV = norm_hi(sl.rem[12 + 2 * i], sl.rem[13 + 2 * i]) * hp
        Pc = [P_start]
        for k in range(K + 1):
            Pc.append((k1 * gH[k] + k2 * gV[k] - k3 * Pc[k]) / (k + 1))
        self.Pc = Pc
        resid = k3 * Pc[K + 1].abs_upper() * harb ** (K + 1)
        dg = k1 * (RH + eH) + k2 * (RV + eV) + resid
        self.rho = (harb * dg).upper()
        self.cauchy = (mH, mV)

    def ev(self, S):
        c = self.Pc
        v = c[-1]
        for k in range(len(c) - 2, -1, -1):
            v = v * S + c[k]
        return v + (-self.rho).union(self.rho)


def p_advance(sl, Pstart, s_end, M, nodes):
    """Pressions P_j (j in nodes) en s_end dans le pas sl (Duhamel, quadrature centree sur M morceaux) et majorants de P_j sur [0, s_end].
    Pstart : dict j -> boule (valeur au debut du pas).  Renvoie (Pend, sup)."""
    model = sl.model
    Q = {j: Pstart[j] for j in nodes}
    P = {j: Pstart[j] for j in nodes}
    sup = {j: Pstart[j] for j in nodes}
    for i in range(M):
        a, b = s_end * i / M, s_end * (i + 1) / M
        w = arb((b - a) / 2); mfq = (a + b) / 2
        Si = arb(a).union(arb(b))
        vm = sl.vec(arb(mfq)); vi = sl.vec(Si); dv = model.Fsca(vi)
        em = (k3 * arb(mfq)).exp(); ei = (k3 * Si).exp(); eb = (-k3 * arb(b)).exp()
        lenp = arb(b - a)
        for j in nodes:
            gm = k1 * nrm_ball(vm[2 * j], vm[2 * j + 1]) + k2 * nrm_ball(vm[12 + 2 * j], vm[13 + 2 * j])
            nH, nV = nrm_ball(vi[2 * j], vi[2 * j + 1]), nrm_ball(vi[12 + 2 * j], vi[13 + 2 * j])
            gbox = k1 * nH + k2 * nV
            gp = k1 * (vi[2 * j] * vi[12 + 2 * j] + vi[2 * j + 1] * vi[13 + 2 * j + 0]) / nH + k2 * (vi[12 + 2 * j] * dv[12 + 2 * j] + vi[13 + 2 * j] * dv[13 + 2 * j]) / nV
            D = ei * (k3 * gbox + gp)
            err = (w * w / 2) * (D.upper() - D.lower())
            Ii = 2 * w * em * gm + (-err).union(err)
            slope = gbox.upper() - k3 * P[j].lower()
            sup[j] = sup[j].union(P[j] + lenp * slope.nonnegative_part())
            Q[j] = Q[j] + Ii
            P[j] = Q[j] * eb
    return P, sup


def pressures_others(sl, Pcur, s_end, M, nodes):
    """Pressions des noeuds non declencheurs en s_end (fmpq) et majorants sur [0, s_end] : Taylor + Cauchy quand le rayon de Cauchy le permet,
    sinon Duhamel (quadrature centree sur M morceaux)."""
    Pend, sup, fb = {}, {}, []
    for j in nodes:
        try:
            pt = PTaylor(sl, j, Pcur[j], s_end, minmult=3)
            Pend[j], sup[j] = pt.ev(arb(s_end)), pt.ev(arb(0).union(arb(s_end)))
        except PressureUnsound:
            fb.append(j)
    if fb:
        Pd, sd = p_advance(sl, Pcur, s_end, M, fb)
        for j in fb:
            Pend[j], sup[j] = Pd[j], sd[j]
    return Pend, sup


def cosv(a, b):
    return (a[0] * b[0] + a[1] * b[1]) / ((a[0] * a[0] + a[1] * a[1]).sqrt() * (b[0] * b[0] + b[1] * b[1]).sqrt())


def select(cs, m, smallest):
    """cs : dict j -> boule (cosinus).  Choisit les m plus petits (smallest) ou plus grands ; renvoie (ensemble choisi, marge certifiee ou None)."""
    items = sorted(cs.items(), key=lambda kv: float(kv[1].mid()), reverse=not smallest)
    chosen, rest = items[:m], items[m:]
    gaps = []
    for jc, cc in chosen:
        for jr, cr in rest:
            gaps.append((cr - cc) if smallest else (cc - cr))
    if not gaps:
        return set(j for j, _ in chosen), None
    lows = [g.lower() for g in gaps]
    marge = lows[0]
    for l in lows[1:]:
        if exq_lo(l) < exq_lo(marge):
            marge = l
    assert marge > 0, ("selection de recablage non certifiee", [(jc, float(cc.mid())) for jc, cc in items])
    return set(j for j, _ in chosen), marge


def episode1_start():
    """Developpement en t = 0 sur [0, t0] ; renvoie (X(t0), P(t0), t0, infos)."""
    t0f = fmpq(1, 100); t0 = arb(t0f)
    X0 = [arb(0)] * 24 + TAU0
    model = get_model(core.A1_kept1)
    S0 = Slab(model, X0, t0)
    St = arb(0).union(t0)
    ok = True; hats = {}
    for k in range(6):
        m = NODE_M[k]
        for comp in range(2):
            for j in range(0, 2 * m + 1):
                ok &= S0.c[12 + 2 * k + comp][j].is_zero()
            for j in range(0, 2 * m + 2):
                ok &= S0.c[2 * k + comp][j].is_zero()

        def hat(idx, order):
            c = S0.c[idx]
            v = c[ORD]
            for j in range(ORD - 1, order - 1, -1):
                v = v * St + c[j]
            return v + S0.rem[idx] * St ** (ORD + 1 - order)
        Vh = [hat(12 + 2 * k + comp, 2 * m + 1) for comp in range(2)]
        Hh = [hat(2 * k + comp, 2 * m + 2) for comp in range(2)]
        hats[k] = dict(Vlo=norm_lo(*Vh), Vhi=norm_hi(*Vh), Hlo=norm_lo(*Hh), Hhi=norm_hi(*Hh))
    assert ok
    print("[ep1] etape 0 : ordres d'annulation exacts en t=0 : %s" % ok)
    for k in range(6):
        h_ = hats[k]
        print("  noeud %d (m=%d) : ||Vhat|| >= %s (<= %s) ; ||Hhat|| >= %s (<= %s)" % (k, NODE_M[k], dn(h_['Vlo'], 8), up(h_['Vhi'], 8), dn(h_['Hlo'], 8), up(h_['Hhi'], 8)))
        assert h_['Vlo'] > 0 and h_['Hlo'] > 0
    S_ = S0.vec(St)
    mins = dict(tau={}, V={}, H={})
    for k in range(6):
        n = norm_lo(S_[24 + 2 * k], S_[24 + 2 * k + 1]); assert n > 0
        mins['tau'][k] = n.lower()
    # pressions a t0 : Taylor + estimee de Cauchy sur [0, t0] (coefficients de depart exacts), tous les noeuds
    P_t0, P_supinit = {}, {}
    for j in range(6):
        m = NODE_M[j]
        P_init = rP * Theta if j == 0 else arb(0)
        pt = PTaylor(S0, j, P_init, t0f, shiftH=2 * m + 2, shiftV=2 * m + 1)
        P_t0[j] = pt.ev(t0)
        P_supinit[j] = pt.ev(St).upper()
        assert P_supinit[j] < Theta
    print("[ep1] P_j(t0) = " + ", ".join("n%d [%s, %s]" % (j, dn(P_t0[j], 8), up(P_t0[j], 8)) for j in range(6)))
    print("[ep1] rayon P_0(t0) = %.2e ; sup_[0,t0] P_j <= " % float(P_t0[0].rad()) + ", ".join("n%d %s" % (j, up(P_supinit[j], 8)) for j in range(6)) + "  (< Theta)")
    return S0.end, P_t0, t0f, dict(hats=hats, mins=mins, P_supinit=P_supinit)


def run_episode(r, Aadj, X, Pvec, i_exp, t_init=fmpq(0), hmax=fmpq(3, 100), shrink=False, delta=fmpq(1, 50), init=None, M=MPIECES):
    t_wall = time.time()
    model = get_model(Aadj)
    nodes_other = [j for j in range(6) if j != i_exp]
    tn = t_init
    Pcur = {j: Pvec[j] for j in range(6)}
    assert Pcur[i_exp] < Theta
    mins = dict(tau={k: arb(10) for k in range(6)}, V={k: None for k in range(6)}, H={k: None for k in range(6)})
    qmin = dict(V={k: None for k in range(6)}, H={k: None for k in range(6)})
    if init is not None:
        mins['tau'] = dict(init['mins']['tau'])
    mins['tau'] = {k: (mins['tau'][k].lower() if isinstance(mins['tau'][k], arb) else mins['tau'][k]) for k in range(6)}
    supP = {j: (init['P_supinit'][j] if init is not None else Pvec[j]) for j in range(6)}
    def upd(j, new):
        if exq_hi(new) > exq_hi(supP[j]):
            supP[j] = new.upper()
    crossing = None; ext_end = None; n_steps = 0
    while True:
        h0 = min(hmax, tn / 32) if shrink else hmax
        hq = h0
        while True:
            sl = Slab(model, X, arb(hq))
            if crossing is not None:
                break
            try:
                pt = PTaylor(sl, i_exp, Pcur[i_exp], hq)
            except PressureUnsound:
                hq = hq / 2
                continue
            Pe_ = pt.ev(arb(hq))
            if not (Pe_ < Theta) and not (Pe_ > Theta):     # pas ambigu : on coupe
                assert hq > fmpq(1, 10 ** 9), "pas ambigu irreductible"
                hq = hq / 2
                continue
            break
        Sh = arb(0).union(arb(hq))
        vec = sl.vec(Sh)
        tmax = arb(tn + hq)
        for k in range(6):
            nV, nH, nT = norm_lo(vec[12 + 2 * k], vec[13 + 2 * k]), norm_lo(vec[2 * k], vec[2 * k + 1]), norm_lo(vec[24 + 2 * k], vec[25 + 2 * k])
            assert nV > 0 and nH > 0 and nT > 0, ("annulation non exclue", r, float(tn), k, nV, nH, nT)
            for key, nn_ in (('V', nV), ('H', nH)):
                lo = nn_.lower()
                if mins[key][k] is None or exq_lo(lo) < exq_lo(mins[key][k]):
                    mins[key][k] = lo
            if shrink:
                m = NODE_M[k]
                for key, val in (('V', nV / tmax ** (2 * m + 1)), ('H', nH / tmax ** (2 * m + 2))):
                    vl = val.lower()
                    if qmin[key][k] is None or exq_lo(vl) < exq_lo(qmin[key][k]):
                        qmin[key][k] = vl
            nTl = nT.lower()
            if exq_lo(nTl) < exq_lo(mins['tau'][k]):
                mins['tau'][k] = nTl
        if crossing is None:
            n_steps += 1
            Pi_end, si = pt.ev(arb(hq)), pt.ev(Sh)
            iscross = False
            if not (si < Theta):
                dP_lo = k1 * norm_lo(vec[2 * i_exp], vec[2 * i_exp + 1]) + k2 * norm_lo(vec[12 + 2 * i_exp], vec[13 + 2 * i_exp]) - k3 * si.upper()
                assert dP_lo > 0, ("P_i' > 0 non etabli sur le pas", r, float(tn), float(hq))
                if Pi_end > Theta:
                    iscross = True
            Pend, sup = pressures_others(sl, Pcur, hq, M, nodes_other)
            if not iscross:
                for j in nodes_other:
                    assert sup[j] < Theta, ("pression concurrente non exclue", r, j, float(tn))
                    upd(j, sup[j])
                upd(i_exp, si)
                Pcur = dict(Pend); Pcur[i_exp] = Pi_end
            else:
                lo, hi = fmpq(0), hq
                for _ in range(400):
                    mid = (lo + hi) / 2
                    pv = pt.ev(arb(mid))
                    if pv < Theta:
                        lo = mid
                    elif pv > Theta:
                        hi = mid
                    else:
                        break
                    if hi - lo < fmpq(1, 10 ** 60):
                        break
                # largeur de la zone ambigue : deux bissections separees (P_i est croissante sur le pas)
                a_, b_ = lo, hi
                for _ in range(400):                      # plus grand s certainement < Theta
                    mid = (a_ + b_) / 2
                    if pt.ev(arb(mid)) < Theta:
                        a_ = mid
                    else:
                        b_ = mid
                    if b_ - a_ < fmpq(1, 10 ** 60):
                        break
                lo = a_
                a_, b_ = lo, hi
                for _ in range(400):                      # plus petit s certainement > Theta
                    mid = (a_ + b_) / 2
                    if pt.ev(arb(mid)) > Theta:
                        b_ = mid
                    else:
                        a_ = mid
                    if b_ - a_ < fmpq(1, 10 ** 60):
                        break
                hi = b_
                Po, so = pressures_others(sl, Pcur, hi, M, nodes_other)
                for j in nodes_other:
                    assert so[j] < Theta, ("pression concurrente non exclue sur [0,T+]", r, j)
                    upd(j, so[j])
                upd(i_exp, si)
                Plo, _s = pressures_others(sl, Pcur, lo, M, nodes_other)
                crossing = dict(tn=tn, lo=lo, hi=hi, sl=sl, Plo_other=Plo)
                ext_end = tn + hq + delta
        X = sl.end
        tn = tn + hq
        if crossing is not None and tn >= ext_end:
            break
        if tn > fmpq(4):
            raise RuntimeError("pas de franchissement")
    # ---- resultats de l'episode
    c = crossing
    Tlo, Thi = c['tn'] + c['lo'], c['tn'] + c['hi']
    SS = arb(c['lo']).union(arb(c['hi']))
    vT = c['sl'].vec(SS)
    dP_T = k1 * norm_lo(vT[2 * i_exp], vT[2 * i_exp + 1]) + k2 * norm_lo(vT[12 + 2 * i_exp], vT[13 + 2 * i_exp]) - k3 * Theta
    assert dP_T > 0
    wT = arb(c['hi'] - c['lo'])
    PT = {i_exp: Theta}
    for j in nodes_other:
        gj = (k1 * norm_hi(vT[2 * j], vT[2 * j + 1]) + k2 * norm_hi(vT[12 + 2 * j], vT[13 + 2 * j])).upper()
        PT[j] = c['Plo_other'][j] + wT * ((-k3 * supP[j].upper()).union(gj))
    nu = min((exq_lo(Theta - supP[j]), j) for j in nodes_other)
    # recablage
    tauT = [(vT[24 + 2 * k], vT[25 + 2 * k]) for k in range(6)]
    for k in range(6):
        assert norm_lo(*tauT[k]) > 0
    Ai = Aadj
    nb = [j for j in range(6) if Ai[i_exp, j] == 1]
    nn = [j for j in range(6) if j != i_exp and Ai[i_exp, j] == 0]
    m = min(2, len(nb), len(nn))
    cs_nb = {j: cosv(tauT[i_exp], tauT[j]) for j in nb}
    cs_nn = {j: cosv(tauT[i_exp], tauT[j]) for j in nn}
    removed, marge_rem = select(cs_nb, m, True)
    added, marge_add = select(cs_nn, m, False)
    newnb = (set(nb) - removed) | added
    A2 = Ai.copy()
    for j in range(6):
        if j != i_exp:
            A2[i_exp, j] = A2[j, i_exp] = 1 if j in newnb else 0
    # nouvel etat
    X2 = list(vT)
    X2[12 + 2 * i_exp] = rV * X2[12 + 2 * i_exp]
    X2[13 + 2 * i_exp] = rV * X2[13 + 2 * i_exp]
    P2 = dict(PT)
    P2[i_exp] = rP * Theta
    rad = max(float(b.rad()) for b in X2)
    rec = dict(r=r, i=i_exp, Tlo=Tlo, Thi=Thi, dP=dP_T, nu=nu, mins=mins, qmin=qmin, supP=supP, cos_nb=cs_nb, cos_nn=cs_nn,
               removed=removed, added=added, newnb=newnb, marge_rem=marge_rem, marge_add=marge_add, nsteps=n_steps, rad_state=rad,
               elapsed=time.time() - t_wall, nb=nb, nn=nn, m=m, P_T=PT, A_after=A2)
    return rec, X2, P2, A2


def report_episode(rec, ref=None):
    r, i = rec['r'], rec['i']
    print("=== episode %d : declencheur noeud %d ; %d pas ; %.1f s" % (r, i, rec['nsteps'], rec['elapsed']))
    print("  T_%d in [%s, %s] (largeur %.2e)%s" % (r, _dec(rec['Tlo'], 12, False), _dec(rec['Thi'], 12, True), float(rec['Thi'] - rec['Tlo']),
                                                 ("  ; DOP853 (rtol 1e-12) : %.12f" % ref['Td']) if ref else ""))
    print("  pente P_%d'(T_%d) >= %s" % (i, r, dn(rec['dP'], 6)))
    nu, jn = rec['nu']
    print("  ecart de pression : Theta - max_{j != %d} sup_[0,T+] P_j >= %s (noeud %d)" % (i, _dec(rec['nu'][0], 6, False), rec['nu'][1]))
    nu, jn = rec['nu']
    print("  sup_[0,T+] P_j : " + ", ".join("n%d <= %s" % (j, up(rec['supP'][j], 5)) for j in range(6) if j != i))
    print("  (H5) min ||tau_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['tau'][k], 5)) for k in range(6)))
    print("  (H2) min ||V_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['V'][k], 6)) for k in range(6)))
    print("  (H2) min ||H_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['H'][k], 6)) for k in range(6)))
    for j, cc in sorted(rec['cos_nb'].items()):
        print("  cos(tau_%d, tau_%d) (voisin) in [%s, %s]" % (i, j, dn(cc, 7), up(cc, 7)))
    for j, cc in sorted(rec['cos_nn'].items()):
        print("  cos(tau_%d, tau_%d) (non-voisin) in [%s, %s]" % (i, j, dn(cc, 7), up(cc, 7)))
    print("  recablage : m=%d, retires %s, ajoutes %s => voisins de %d : %s ; marge retrait %s, marge ajout %s" % (
        rec['m'], sorted(rec['removed']), sorted(rec['added']), i, sorted(rec['newnb']),
        dn(rec['marge_rem'], 6) if rec['marge_rem'] is not None else "-", dn(rec['marge_add'], 6) if rec['marge_add'] is not None else "-"))
    if rec['r'] == 1:
        print("  (H2) quotients ||V_j||/t^(2m+1) >= " + ", ".join("n%d %s" % (k, dn(rec['qmin']['V'][k], 8)) for k in range(6)) + "  (sur [t0, T+delta])")
        print("  (H2) quotients ||H_j||/t^(2m+2) >= " + ", ".join("n%d %s" % (k, dn(rec['qmin']['H'][k], 8)) for k in range(6)) + "  (sur [t0, T+delta])")
    print("  rayon max de la boite post-impact : %.3e ; rayons des pressions P_j(T) : " % rec['rad_state'] + ", ".join("n%d %.1e" % (j, float(rec['P_T'][j].rad())) for j in range(6)))
    sys.stdout.flush()


def fref():
    y = Z.initial_state(VP.tau0); A = core.A1_kept1.copy()
    Uv = np.array([core.Ux, core.Uy]); out = []
    for r in range(1, KMAX + 1):
        sol, Td, yT = Z.episode(y, A, 0.0, 0.0, Uv)
        P = yT[36:42]; i = int(np.argmax(P))
        y2, key, A2 = Z.apply_jump(yT, A)
        out.append(dict(Td=Td, i=i, A=A.copy(), A2=A2.copy(), P=P.copy()))
        y, A = y2, A2
    return out


def to_json(rec):
    d = dict(rank=rec['r'], trigger=rec['i'],
             T_lo=qs(rec['Tlo']), T_hi=qs(rec['Thi']), T_lo_dec=_dec(rec['Tlo'], 12, False), T_hi_dec=_dec(rec['Thi'], 12, True),
             slope_lower=qs(exq_lo(rec['dP'])), slope_lower_dec=dn(rec['dP'], 6),
             pressure_gap_lower=qs(rec['nu'][0]), pressure_gap_lower_dec=_dec(rec['nu'][0], 6, False), pressure_gap_node=rec['nu'][1],
             sup_pressure_upper={j: qs(exq_hi(rec['supP'][j])) for j in range(6) if j != rec['i']},
             min_tau_lower={k: qs(exq_lo(rec['mins']['tau'][k])) for k in range(6)},
             min_V_lower={k: qs(exq_lo(rec['mins']['V'][k])) for k in range(6)},
             min_H_lower={k: qs(exq_lo(rec['mins']['H'][k])) for k in range(6)},
             min_tau_lower_dec={k: dn(rec['mins']['tau'][k], 6) for k in range(6)},
             min_V_lower_dec={k: dn(rec['mins']['V'][k], 6) for k in range(6)},
             min_H_lower_dec={k: dn(rec['mins']['H'][k], 6) for k in range(6)},
             cos_neighbours={j: [qs(exq_lo(c)), qs(exq_hi(c))] for j, c in rec['cos_nb'].items()},
             cos_nonneighbours={j: [qs(exq_lo(c)), qs(exq_hi(c))] for j, c in rec['cos_nn'].items()},
             removed=sorted(rec['removed']), added=sorted(rec['added']), new_neighbours=sorted(rec['newnb']),
             margin_removal_lower=qs(exq_lo(rec['marge_rem'])) if rec['marge_rem'] is not None else None,
             margin_removal_lower_dec=dn(rec['marge_rem'], 6) if rec['marge_rem'] is not None else None,
             margin_addition_lower=qs(exq_lo(rec['marge_add'])) if rec['marge_add'] is not None else None,
             margin_addition_lower_dec=dn(rec['marge_add'], 6) if rec['marge_add'] is not None else None,
             quotients_after_t0_lower=({'V': {k: qs(exq_lo(rec['qmin']['V'][k])) for k in range(6)}, 'H': {k: qs(exq_lo(rec['qmin']['H'][k])) for k in range(6)}} if rec['r'] == 1 else None),
             P_T_upper={j: qs(exq_hi(rec['P_T'][j])) for j in range(6)}, P_T_lower={j: qs(exq_lo(rec['P_T'][j])) for j in range(6)},
             post_impact_box_max_radius=rec['rad_state'], steps=rec['nsteps'])
    return d


if __name__ == '__main__':
    t_all = time.time()
    refs = fref()
    print("trajectoire de reference (DOP853, rtol 1e-12 ; ecart attendu jusqu'a ~1e-11 au rang 8 : evenement lent) : " + "; ".join("r%d T=%.9f i=%d" % (k + 1, r['Td'], r['i']) for k, r in enumerate(refs)))
    print("precision %d bits ; ordre de Taylor %d ; %d morceaux de quadrature par pas" % (PREC, ORD, MPIECES))
    X, P, t0f, init = episode1_start()
    A = core.A1_kept1.copy()
    out = dict(convention="fractions exactes (bornes de boules arb, arrondi dirige) ; *_dec arrondis vers l'exterieur", precision_bits=PREC, taylor_order=ORD, quad_pieces=MPIECES, episodes=[])
    for r in range(1, KMAX + 1):
        ref = refs[r - 1]
        assert np.array_equal(A, ref['A'])
        if r == 1:
            rec, X2, P2, A2 = run_episode(1, A, X, P, ref['i'], t_init=t0f, shrink=True, init=init)
        else:
            rec, X2, P2, A2 = run_episode(r, A, X, P, ref['i'], hmax=fmpq(1, int(os.environ.get('HLATER', 100))))
        assert np.array_equal(A2, ref['A2']), ("graphe different de la reference", r)
        report_episode(rec, ref)
        out['episodes'].append(to_json(rec))
        json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificat_episodes.json"), "w"), indent=1)
        X, P, A = X2, P2, A2
    print("duree totale %.1f s" % (time.time() - t_all))
