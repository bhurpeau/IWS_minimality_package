"""
SECONDE IMPLEMENTATION INDEPENDANTE des certificats des episodes 1..8 (meme trajectoire de base q0 = (0,0), graphe kept1).

Independance de methode vis-a-vis de certif_episodes.py (rien n'est importe de ce module) :
  * ETAT (H,V,tau) : AUCUNE enclosure a priori de Picard, AUCUN reste de Lagrange sur boite.  On suit une trajectoire NOMINALE (polynomes de Taylor
    d'ordre K issus d'un point exact) et un rayon de tube eps (norme sup) :
        eps_{k+1} = exp(L h) eps_k + queue_k ,       L = 1 + gamma0 + zeta = 41/20 (constante de Lipschitz GLOBALE du champ pour la norme sup,
        car tanh est 1-lipschitzienne et les lignes de A~ somment a 1),   (Gronwall)
    queue_k = reste de Taylor du flot issu du point nominal, borne par le theoreme de Cauchy--Kovalevskaya (majorant) :
        si |F_i| <= M sur le polydisque complexe de centre x_k et rayon R, la solution est holomorphe pour |t| < rho = R/M, a valeurs dans le polydisque,
        donc |coeff_n| <= R / rho^n  (Cauchy) et, pour 0 <= s <= h < rho,  |x(s) - T_K(s)| <= R q^(K+1)/(1-q),  q = h/rho.
    M est evalue par l'arithmetique de boules COMPLEXES (acb) sur le polydisque.
  * PRESSIONS : P_j(s) = e^{-k3 s} P_j(0) + int_0^s e^{-k3 (s-u)} (k1 ||H_j(u)|| + k2 ||V_j(u)||) du, l'integrale du polynome nominal etant calculee par
    l'integrateur RIGOUREUX de FLINT (acb.integral, controle d'analyticite de sqrt fait ici : Re q > 0) -- et non par un reste de Cauchy ecrit a la main.
    Erreur : la norme euclidienne est 1-lipschitzienne : |g_vrai - g_nominal| <= (k1+k2) sqrt(2) eps_step.
  * EVENEMENT : bissection sur la bande rigoureuse de P_i ; pente > 0 certifiee ; concurrents < Theta (monotonie ou borne grossiere P(0) + h sup g).
  * RECABLAGE : cosinus sur la bande de tube ; selection a marge certifiee ; reset V_i <- V_i/2, P_i <- r_P Theta.
Ce que l'on compare ensuite a certif_episodes.py : T_r, pentes, ecarts de pression, marges, mots -- les enclosures peuvent etre plus larges
(on ne cherche pas la precision, on cherche la certification des evenements).
"""
import sys, os, time, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from flint import arb, acb, arb_series, ctx, fmpq
import numpy as np
import iws_kairos_core as core               # donnees d'entree seulement (graphes, constantes, trace de reference)
import verif_profondeur_propagation as VP
import zero_V0_lib as Z                      # trajectoire de reference DOP853 (comparaison uniquement)

PREC = int(os.environ.get('PREC', 192)); K = int(os.environ.get('KTAY', 30)); MULT = int(os.environ.get('MULT', 6))
KMAX = int(os.environ.get('KMAX', 8)); HREQ = fmpq(int(os.environ.get('HNUM', 2)), int(os.environ.get('HDEN', 128)))
ctx.prec = PREC


def q(a, b=1): return arb(fmpq(a, b))

zeta, alpha, beta, gamma0 = q(4, 5), q(9, 20), q(3, 25), q(1, 4)
k1, k2, k3, Theta, rP, rV = q(3, 5), q(2, 5), q(1, 2), q(5, 4), q(7, 20), q(1, 2)
L = 1 + gamma0 + zeta
SQ2 = arb(2).sqrt()
ang = arb.pi() * 37 / 180
U = [q(5, 2) * ang.cos(), q(5, 2) * ang.sin()]
TAU0 = [arb(float(v)) for v in VP.tau0.reshape(-1)]
NODE_M = {0: 0, 1: 1, 4: 1, 5: 1, 2: 2, 3: 2}


# ------------------------------------------------------------------ arrondi dirige
def _exq(p):
    assert p.rad() == 0
    m, e = p.man_exp(); m, e = int(m), int(e)
    return fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, 2 ** (-e))
def exq_lo(x): return _exq(x.lower())
def exq_hi(x): return _exq(x.upper())
def _dec(qv, d, upflag):
    fr = Fraction(int(qv.numerator), int(qv.denominator)) * 10 ** d
    n = math.ceil(fr) if upflag else math.floor(fr)
    sgn = '-' if n < 0 else ''
    n = abs(n); ip, fp = divmod(n, 10 ** d)
    return "%s%d.%0*d" % (sgn, ip, d, fp)
def dn(x, d=6): return _dec(x if isinstance(x, fmpq) else exq_lo(x), d, False)
def up(x, d=6): return _dec(x if isinstance(x, fmpq) else exq_hi(x), d, True)
def qs(v): return "%d/%d" % (int(v.numerator), int(v.denominator))
def dyadic(x, den=4096):
    """plus grand multiple de 1/den inferieur ou egal a x (fmpq)."""
    n = (x * den).floor()
    return fmpq(int(n), den)


# ------------------------------------------------------------------ champ de vecteurs generique
class Graph:
    def __init__(self, Aadj):
        self.A = Aadj.copy()
        self.At = [[None] * 6 for _ in range(6)]
        for i in range(6):
            d1 = int(Aadj[i].sum()) + 1
            for j in range(6):
                self.At[i][j] = q(1, d1) if (Aadj[i, j] == 1 or i == j) else None

    def field(self, x, th_fn):
        th = []
        for i in range(6):
            for c in range(2):
                acc = None
                for j in range(6):
                    a = self.At[i][j]
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


def tanh_ser(z):
    e = (z * 2).exp()
    return (e - 1) / (e + 1)


def taylor_coeffs(G, x0):
    """coefficients de Taylor (ordre K) de la solution issue du point x0 (liste d'arb) : iteration de Picard sur les series."""
    ctx.cap = K + 1
    x = [arb_series([c]) for c in x0]
    for _ in range(K):
        f = G.field(x, tanh_ser)
        x = [arb_series([x0[i]]) + f[i].integral() for i in range(36)]
    return [list(s.coeffs()) + [arb(0)] * (K + 1 - len(s.coeffs())) for s in x]


def ck_bound(G, x0):
    """(R, M, rho) : M = max_i sup |F_i| sur le polydisque complexe de centre x0 et de rayon R (enclos par des carres complexes), rho = R / M ; meilleur R parmi quelques valeurs."""
    best = None
    for R in (fmpq(1, 2), fmpq(1, 4), fmpq(1, 8)):
        Rb = arb(R)
        z = [acb(arb(c.mid(), c.rad() + Rb), arb(0, Rb)) for c in x0]
        F = G.field(z, lambda w: w.tanh())
        M = arb(0)
        ok = True
        for f in F:
            a = f.abs_upper()
            if not a.is_finite():
                ok = False; break
            if a > M:
                M = a
        if not ok:
            continue
        M = M.upper()
        rho = Rb / M
        if best is None or rho > best[2]:
            best = (R, M, rho)
    return best


def horner(c, S):
    v = c[-1]
    for k in range(len(c) - 2, -1, -1):
        v = v * S + c[k]
    return v


def horner_c(c, z):
    v = acb(c[-1])
    for k in range(len(c) - 2, -1, -1):
        v = v * z + c[k]
    return v


def pieces(h, n):
    return [arb(h * i / n).union(arb(h * (i + 1) / n)) for i in range(n)]


class Step:
    """Un pas d'etat : polynome nominal (coeffs), longueur h, rayon de tube sur le pas."""
    def __init__(self, G, x0, eps0, h_req):
        self.G = G
        self.x0, self.eps0 = x0, eps0
        R, M, rho = ck_bound(G, x0)
        hmax = dyadic(exq_lo(rho) / MULT)
        self.h = min(h_req, hmax)
        assert self.h > 0
        self.c = taylor_coeffs(G, x0)
        qq = arb(self.h) / rho
        assert qq <= arb(fmpq(1, MULT)), (float(qq.mid()), MULT)
        self.tail = arb(R) * qq ** (K + 1) / (1 - qq)
        self.tail = self.tail.upper()
        self.R, self.M, self.rho = R, M, rho
        self.eps_step = ((L * arb(self.h)).exp() * eps0 + self.tail).upper()
        end = [horner(self.c[i], arb(self.h)) for i in range(36)]
        self.x_next = [e.mid() for e in end]
        rad = max(e.rad() for e in end)
        self.eps_next = (self.eps_step + rad).upper()

    def ev(self, i, S):
        return horner(self.c[i], S)

    def norm_range(self, i0, i1, S, tube=True):
        """enclosure de ||(x_{i0}, x_{i1})|| sur S (bande de tube incluse) : (borne inf, borne sup)."""
        a, b = self.ev(i0, S), self.ev(i1, S)
        lo = (a.abs_lower() ** 2 + b.abs_lower() ** 2).sqrt()
        hi = (a.abs_upper() ** 2 + b.abs_upper() ** 2).sqrt()
        if tube:
            t = SQ2 * self.eps_step
            lo = (lo - t).nonnegative_part()
            hi = hi + t
        return lo.lower(), hi.upper()

    def norm_bounds_over(self, i0, i1, npieces=4):
        los, his = [], []
        for S in pieces(self.h, npieces):
            lo, hi = self.norm_range(i0, i1, S)
            los.append(lo); his.append(hi)
        lo = los[0]
        for v in los[1:]:
            if exq_lo(v) < exq_lo(lo):
                lo = v
        hi = his[0]
        for v in his[1:]:
            if exq_hi(v) > exq_hi(hi):
                hi = v
        return lo, hi


def sqrt_an(qv, an):
    if an and not (qv.real > 0):
        return acb(arb("nan"), arb("nan"))
    return qv.sqrt()


def p_integral(st, j, shiftH, shiftV, s_end):
    """int_0^{s_end} e^{-k3 (s_end - u)} (k1 ||H_j(u)|| + k2 ||V_j(u)||) du pour le polynome nominal du pas (arb, rayon propre)."""
    cH = (st.c[2 * j][shiftH:], st.c[2 * j + 1][shiftH:])
    cV = (st.c[12 + 2 * j][shiftV:], st.c[13 + 2 * j][shiftV:])
    se = arb(s_end)

    def f(z, an):
        qh = horner_c(cH[0], z) ** 2 + horner_c(cH[1], z) ** 2
        qv = horner_c(cV[0], z) ** 2 + horner_c(cV[1], z) ** 2
        g = k1 * (z ** shiftH) * sqrt_an(qh, an) + k2 * (z ** shiftV) * sqrt_an(qv, an)
        return g * (k3 * (z - se)).exp()

    I = acb.integral(f, 0, se, rel_tol=2 ** -120, abs_tol=arb("1e-50"))
    assert I.real.is_finite()
    return I.real


class PState:
    """Pression nominale (point) et rayon d'erreur."""
    def __init__(self, P, eps):
        self.P, self.eps = P, eps


def p_at(st, j, ps, s_end, shifts=(0, 0)):
    """P_j(s_end) : (centre ball, rayon de bande) ; vrai P_j(s_end) dans centre +- bande."""
    ctr = (-k3 * arb(s_end)).exp() * ps.P + p_integral(st, j, shifts[0], shifts[1], s_end)
    band = (-k3 * arb(s_end)).exp() * ps.eps + (k1 + k2) * SQ2 * st.eps_step * arb(s_end)
    return ctr, band.upper()


def cosv(a, b):
    return (a[0] * b[0] + a[1] * b[1]) / ((a[0] * a[0] + a[1] * a[1]).sqrt() * (b[0] * b[0] + b[1] * b[1]).sqrt())


def select(cs, m, smallest):
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


# ------------------------------------------------------------------ un episode
def run_episode(r, Aadj, x0, eps0, Pnom, i_exp, first=False, delta=fmpq(1, 50)):
    t_wall = time.time()
    G = Graph(Aadj)
    nodes_other = [j for j in range(6) if j != i_exp]
    x, eps = list(x0), eps0
    PS = {j: Pnom[j] for j in range(6)}           # PState
    tn = fmpq(0)
    mins = dict(tau={k: None for k in range(6)}, V={k: None for k in range(6)}, H={k: None for k in range(6)})
    supP = {j: None for j in range(6)}
    def upd(dic, key, val, hi=True):
        cur = dic[key]
        if cur is None or (exq_hi(val) > exq_hi(cur) if hi else exq_lo(val) < exq_lo(cur)):
            dic[key] = val.upper() if hi else val.lower()
    crossing = None; ext_end = None; nsteps = 0
    while True:
        # --- pas d'etat
        if first and tn == 0:
            h_req = fmpq(1, 128)
        elif first:
            h_req = dyadic(min(HREQ, tn / 8))
        else:
            h_req = HREQ
        st = Step(G, x, eps, h_req)
        h = st.h
        # --- minima de normes (H2),(H5)
        for k in range(6):
            lo, hi = st.norm_bounds_over(24 + 2 * k, 25 + 2 * k)
            assert lo > 0, ("tau s'annule ?", r, float(tn), k)
            upd(mins['tau'], k, lo, hi=False)
            if not (first and tn == 0):
                loV, _ = st.norm_bounds_over(12 + 2 * k, 13 + 2 * k)
                loH, _ = st.norm_bounds_over(2 * k, 2 * k + 1)
                assert loV > 0 and loH > 0, ("norme nulle non exclue", r, float(tn), k, float(loV.mid()), float(loH.mid()))
                upd(mins['V'], k, loV, hi=False); upd(mins['H'], k, loH, hi=False)
        # --- pressions
        if crossing is None:
            nsteps += 1
            shifts = {j: ((2 * NODE_M[j] + 2, 2 * NODE_M[j] + 1) if (first and tn == 0) else (0, 0)) for j in range(6)}
            if first and tn == 0:
                # exactitude des ordres d'annulation en t = 0
                for j in range(6):
                    m = NODE_M[j]
                    for comp in range(2):
                        assert all(st.c[12 + 2 * j + comp][n].is_zero() for n in range(0, 2 * m + 1))
                        assert all(st.c[2 * j + comp][n].is_zero() for n in range(0, 2 * m + 2))
            newP, bands, gup, glo = {}, {}, {}, {}
            for j in range(6):
                ctr, band = p_at(st, j, PS[j], h, shifts[j])
                newP[j], bands[j] = ctr, band
                # bornes de g sur le pas
                loH, hiH = st.norm_bounds_over(2 * j, 2 * j + 1)
                loV, hiV = st.norm_bounds_over(12 + 2 * j, 13 + 2 * j)
                gup[j] = (k1 * hiH + k2 * hiV).upper()
                glo[j] = (k1 * loH + k2 * loV).lower()
            # enclosure de P_i au debut et a la fin du pas
            def Pend_ball(j): return newP[j] + (-bands[j]).union(bands[j])
            P0ball = {j: PS[j].P + (-PS[j].eps).union(PS[j].eps) for j in range(6)}
            iscross = False
            # concurrents : sup < Theta (grossier : P(0) + h gup ; sinon monotonie P' > 0 et P(fin) < Theta)
            def safe(j):
                crude = (P0ball[j] + arb(h) * gup[j]).upper()
                if crude < Theta:
                    return crude
                dlo = glo[j] - k3 * crude
                if dlo > 0 and Pend_ball(j) < Theta:
                    return Pend_ball(j).upper()
                return None
            for j in nodes_other:
                s_ = safe(j)
                assert s_ is not None, ("concurrent non exclu", r, j, float(tn), float(P0ball[j].mid()))
                upd(supP, j, s_)
            sj = safe(i_exp)
            if sj is not None:
                upd(supP, i_exp, sj)
            else:
                crude = (P0ball[i_exp] + arb(h) * gup[i_exp]).upper()
                dlo = glo[i_exp] - k3 * crude
                assert dlo > 0, ("P_i' > 0 non etabli sur le pas", r, float(tn))
                Pe = Pend_ball(i_exp)
                if Pe > Theta:
                    iscross = True
                elif not (Pe < Theta):
                    raise RuntimeError("pas ambigu")
                else:
                    upd(supP, i_exp, Pe)
            if iscross:
                shi = shifts[i_exp]
                def band_at(s):
                    ctr, bd = p_at(st, i_exp, PS[i_exp], s, shi)
                    return ctr, bd
                lo_, hi_ = fmpq(0), h
                # plus grand s certainement < Theta
                a_, b_ = lo_, hi_
                for _ in range(200):
                    mid = (a_ + b_) / 2
                    ctr, bd = band_at(mid)
                    if (ctr + (-bd).union(bd)) < Theta:
                        a_ = mid
                    else:
                        b_ = mid
                    if b_ - a_ < fmpq(1, 10 ** 45):
                        break
                lo_ = a_
                a_, b_ = lo_, hi_
                for _ in range(200):
                    mid = (a_ + b_) / 2
                    ctr, bd = band_at(mid)
                    if (ctr + (-bd).union(bd)) > Theta:
                        b_ = mid
                    else:
                        a_ = mid
                    if b_ - a_ < fmpq(1, 10 ** 45):
                        break
                hi_ = b_
                # concurrents jusqu'a T^+ (monotonie sur [0,hi_] ou borne grossiere)
                for j in nodes_other:
                    ctr, bd = p_at(st, j, PS[j], hi_, shifts[j])
                    Pe = ctr + (-bd).union(bd)
                    crude = (P0ball[j] + arb(hi_) * gup[j]).upper()
                    val = crude if crude < Theta else (Pe.upper() if (glo[j] - k3 * crude > 0 and Pe < Theta) else None)
                    assert val is not None, ("concurrent non exclu sur [0,T+]", r, j)
                    upd(supP, j, val)
                crossing = dict(tn=tn, lo=lo_, hi=hi_, st=st, PS=PS, shifts=shifts, P0ball=P0ball, gup=gup)
                ext_end = tn + h + delta
            else:
                for j in range(6):
                    PS[j] = PState(newP[j].mid(), (bands[j] + newP[j].rad()).upper())
        x, eps = st.x_next, st.eps_next
        tn = tn + h
        if crossing is not None and tn >= ext_end:
            break
        if tn > fmpq(4):
            raise RuntimeError("pas de franchissement")
    # --- resultats
    c = crossing
    st = c['st']
    Tlo, Thi = c['tn'] + c['lo'], c['tn'] + c['hi']
    SS = arb(c['lo']).union(arb(c['hi']))
    loH, hiH = st.norm_range(2 * i_exp, 2 * i_exp + 1, SS)
    loV, hiV = st.norm_range(12 + 2 * i_exp, 13 + 2 * i_exp, SS)
    dP = (k1 * loH + k2 * loV - k3 * Theta).lower()
    assert dP > 0
    # etat a T : centre au milieu de [lo,hi]
    Tm = (c['lo'] + c['hi']) / 2
    wT = arb(c['hi'] - c['lo']) / 2
    xT = [st.ev(i, arb(Tm)) for i in range(36)]
    # derivee du polynome sur [lo,hi] (pour l'incertitude de temps)
    dpoly = []
    for i in range(36):
        ci = [st.c[i][n] * n for n in range(1, K + 1)]
        dpoly.append(horner(ci, SS))
    dmax = max(d.abs_upper() for d in dpoly)
    eps_T = (st.eps_step + wT * dmax + max(v.rad() for v in xT)).upper()
    xT_c = [v.mid() for v in xT]
    # cosinus (bande de tube : chaque composante +- eps_T)
    tube = (-eps_T).union(eps_T)
    tauT = [(xT_c[24 + 2 * k] + tube, xT_c[25 + 2 * k] + tube) for k in range(6)]
    for k in range(6):
        assert (tauT[k][0] ** 2 + tauT[k][1] ** 2) > 0 or True
    nb = [j for j in range(6) if Aadj[i_exp, j] == 1]
    nn = [j for j in range(6) if j != i_exp and Aadj[i_exp, j] == 0]
    m = min(2, len(nb), len(nn))
    cs_nb = {j: cosv(tauT[i_exp], tauT[j]) for j in nb}
    cs_nn = {j: cosv(tauT[i_exp], tauT[j]) for j in nn}
    removed, mrem = select(cs_nb, m, True)
    added, madd = select(cs_nn, m, False)
    newnb = (set(nb) - removed) | added
    A2 = Aadj.copy()
    for j in range(6):
        if j != i_exp:
            A2[i_exp, j] = A2[j, i_exp] = 1 if j in newnb else 0
    # pressions a T
    Pnext = {}
    for j in range(6):
        if j == i_exp:
            Pnext[j] = PState(rP * Theta, arb(0))
            continue
        ctr, bd = p_at(st, j, c['PS'][j], Tm, c['shifts'][j])
        slope = (c['gup'][j] + k3 * Theta).upper()
        bd2 = (bd + ctr.rad() + wT * slope).upper()
        Pnext[j] = PState(ctr.mid(), bd2)
    X2 = list(xT_c)
    X2[12 + 2 * i_exp] = rV * X2[12 + 2 * i_exp]
    X2[13 + 2 * i_exp] = rV * X2[13 + 2 * i_exp]
    nu = min((exq_lo(Theta - supP[j]), j) for j in nodes_other)
    rec = dict(r=r, i=i_exp, Tlo=Tlo, Thi=Thi, dP=dP, nu=nu, mins=mins, cos_nb=cs_nb, cos_nn=cs_nn, removed=removed, added=added, newnb=newnb,
               mrem=mrem, madd=madd, nsteps=nsteps, eps_next=eps_T, elapsed=time.time() - t_wall, supP=supP)
    return rec, X2, eps_T, Pnext, A2


def report(rec, ref=None):
    r, i = rec['r'], rec['i']
    print("=== [independant] episode %d : declencheur noeud %d ; %d pas ; %.1f s" % (r, i, rec['nsteps'], rec['elapsed']))
    print("  T_%d in [%s, %s] (largeur %.2e)%s" % (r, _dec(rec['Tlo'], 12, False), _dec(rec['Thi'], 12, True), float(rec['Thi'] - rec['Tlo']), ("  ; DOP853 : %.12f" % ref['Td']) if ref else ""))
    print("  pente P_%d'(T_%d) >= %s" % (i, r, dn(rec['dP'])))
    print("  ecart de pression : Theta - max_{j != %d} sup P_j >= %s (noeud %d)" % (i, _dec(rec['nu'][0], 6, False), rec['nu'][1]))
    print("  (H5) min ||tau_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['tau'][k], 5)) for k in range(6)))
    if rec['mins']['V'][0] is not None:
        print("  (H2) min ||V_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['V'][k], 6)) for k in range(6)))
        print("  (H2) min ||H_j|| >= " + ", ".join("n%d %s" % (k, dn(rec['mins']['H'][k], 6)) for k in range(6)))
    for j, cc in sorted(rec['cos_nb'].items()):
        print("  cos(tau_%d, tau_%d) (voisin) in [%s, %s]" % (i, j, dn(cc, 7), up(cc, 7)))
    for j, cc in sorted(rec['cos_nn'].items()):
        print("  cos(tau_%d, tau_%d) (non-voisin) in [%s, %s]" % (i, j, dn(cc, 7), up(cc, 7)))
    print("  recablage : retires %s, ajoutes %s => voisins de %d : %s ; marge retrait %s, marge ajout %s" % (
        sorted(rec['removed']), sorted(rec['added']), i, sorted(rec['newnb']), dn(rec['mrem'], 6) if rec['mrem'] is not None else '-', dn(rec['madd'], 6) if rec['madd'] is not None else '-'))
    print("  rayon de tube post-impact (norme sup) : %.3e" % float(rec['eps_next'].mid()))
    sys.stdout.flush()


def fref():
    y = Z.initial_state(VP.tau0); A = core.A1_kept1.copy(); Uv = np.array([core.Ux, core.Uy]); out = []
    for r in range(1, KMAX + 1):
        sol, Td, yT = Z.episode(y, A, 0.0, 0.0, Uv)
        P = yT[36:42]; i = int(np.argmax(P))
        y2, key, A2 = Z.apply_jump(yT, A)
        out.append(dict(Td=Td, i=i, A=A.copy(), A2=A2.copy()))
        y, A = y2, A2
    return out


def to_json(rec):
    return dict(rank=rec['r'], trigger=rec['i'], T_lo=qs(rec['Tlo']), T_hi=qs(rec['Thi']), T_lo_dec=_dec(rec['Tlo'], 12, False), T_hi_dec=_dec(rec['Thi'], 12, True),
                slope_lower=qs(exq_lo(rec['dP'])), slope_lower_dec=dn(rec['dP'], 6), pressure_gap_lower=qs(rec['nu'][0]), pressure_gap_lower_dec=_dec(rec['nu'][0], 6, False),
                pressure_gap_node=rec['nu'][1],
                min_tau_lower_dec={k: dn(rec['mins']['tau'][k], 6) for k in range(6)},
                min_V_lower_dec={k: (dn(rec['mins']['V'][k], 6) if rec['mins']['V'][k] is not None else None) for k in range(6)},
                min_H_lower_dec={k: (dn(rec['mins']['H'][k], 6) if rec['mins']['H'][k] is not None else None) for k in range(6)},
                removed=sorted(rec['removed']), added=sorted(rec['added']), new_neighbours=sorted(rec['newnb']),
                margin_removal_lower_dec=dn(rec['mrem'], 6) if rec['mrem'] is not None else None,
                margin_addition_lower_dec=dn(rec['madd'], 6) if rec['madd'] is not None else None,
                cos_neighbours={j: [qs(exq_lo(c)), qs(exq_hi(c))] for j, c in rec['cos_nb'].items()},
                cos_nonneighbours={j: [qs(exq_lo(c)), qs(exq_hi(c))] for j, c in rec['cos_nn'].items()},
                sup_pressure_upper={j: (qs(exq_hi(v)) if v is not None else None) for j, v in rec['supP'].items() if j != rec['i']},
                tube_radius_post_impact=float(rec['eps_next'].mid()), steps=rec['nsteps'])


if __name__ == '__main__':
    t_all = time.time()
    refs = fref()
    print("seconde implementation (tube de Gronwall + Cauchy--Kovalevskaya + integrateur FLINT) ; precision %d bits ; ordre %d ; pas max %s" % (PREC, K, HREQ))
    A = core.A1_kept1.copy()
    x = [arb(0)] * 24 + TAU0
    eps = arb(0)
    P = {j: PState(rP * Theta if j == 0 else arb(0), arb(0)) for j in range(6)}
    out = dict(method="tube Gronwall + Cauchy-Kovalevskaya + acb.integral", precision_bits=PREC, taylor_order=K, episodes=[])
    for r in range(1, KMAX + 1):
        ref = refs[r - 1]
        assert np.array_equal(A, ref['A'])
        rec, x, eps, P, A2 = run_episode(r, A, x, eps, P, ref['i'], first=(r == 1))
        assert np.array_equal(A2, ref['A2']), ("graphe different", r)
        report(rec, ref)
        out['episodes'].append(to_json(rec))
        json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificat_independant.json"), "w"), indent=1)
        A = A2
    print("duree totale %.1f s" % (time.time() - t_all))
