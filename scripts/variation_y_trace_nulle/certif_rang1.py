"""
CERTIFICAT DU RANG 1 (pilote) -- point de base q0 = (theta, eps) = (0, 0), graphe A_1 = kept1, protocole des notes V2.x.
Arithmetique de boules (python-flint / Arb) ; integrateur de Taylor valide (ordre ORD, enclosure a priori de Picard, reste de Lagrange).

A eps = 0 : gamma_1 = lambda = 0, le sous-systeme (H,V,tau) est autonome et ne depend pas de la direction (gamma_bar, lambda_bar).
Etat suivi : x = (H,V,tau) in R^36 depuis t = 0 ; puis, a partir de t0, la pression P_0 du noeud declencheur (norme analytique car ||H_0||,||V_0|| > 0).
Pressions des autres noeuds : borne grossiere P_j <= sup g_j / kappa_3 (P_j(0) = 0).

Ce qui est certifie (cf. note transmission_profondeur_finie, hypotheses H1-H5, rang r = 1) :
 (H2) non-annulation des quotients H_j / t^(2m+2), V_j / t^(2m+1) sur [0, t0] (developpement en t = 0, ordres d'annulation verifies
      EXACTEMENT egaux a 0 pour les coefficients d'ordre < 2m+1 / 2m+2), puis des normes ||H_j||, ||V_j|| sur ]t0, T + delta].
 (H3) premier franchissement de Theta par la pression du noeud 0, pente > 0, unicite, autres pressions < Theta.
 (H5) min_j ||tau_j|| > 0 sur [0, T + delta].
 (H1) tau_j(T) != 0 ; marge de la selection de recablage : parmi les voisins {1,4,5} de 0, le plus similaire (a conserver) est strictement separe des deux autres ;
      les non-voisins {2,3} sont tous deux ajoutes (m = min(2, 3, 2) = 2), sans selection.
Les constantes sont les rationnels du manuscrit ; U = 2.5 (cos 37deg, sin 37deg) en boule ; tau_ref = doubles de FB.tau_ref() pris comme exacts.
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, arb_series, ctx, fmpq
import iws_kairos_core as core

# ---- arrondi dirige : extremites exactes (rationnels) et chaines decimales arrondies vers l'exterieur
def _exq(p):
    """fmpq exact d'une boule-point (rayon nul)."""
    assert p.rad() == 0
    m, e = p.man_exp()
    m, e = int(m), int(e)
    return fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, 2 ** (-e))
def exq_lo(x):
    return _exq(x.lower())
def exq_hi(x):
    return _exq(x.upper())
def _dec(q, d, up):
    from fractions import Fraction
    fr = Fraction(int(q.numerator), int(q.denominator)) * 10 ** d
    import math
    n = math.ceil(fr) if up else math.floor(fr)
    sgn = '-' if n < 0 else ''
    n = abs(n); ip, fp = divmod(n, 10 ** d)
    return "%s%d.%0*d" % (sgn, ip, d, fp)
def dn(x, d=6):
    """minorant decimal (arrondi vers le bas) de la borne inferieure de x (arb ou fmpq)."""
    q = x if isinstance(x, fmpq) else exq_lo(x)
    return _dec(q, d, False)
def up(x, d=6):
    q = x if isinstance(x, fmpq) else exq_hi(x)
    return _dec(q, d, True)
def qs(q):
    return "%d/%d" % (int(q.numerator), int(q.denominator))
import verif_profondeur_propagation as VP

PREC, ORD = 256, 24
ctx.prec = PREC
NODE_M = {0: 0, 1: 1, 4: 1, 5: 1, 2: 2, 3: 2}           # distance a 0 dans A_1


def q(a, b=1):
    return arb(fmpq(a, b))


zeta, alpha, beta, gamma0 = q(4, 5), q(9, 20), q(3, 25), q(1, 4)
k1, k2, k3, Theta, rP = q(3, 5), q(2, 5), q(1, 2), q(5, 4), q(7, 20)
assert (core.zeta, core.alpha, core.beta, core.gamma0, core.k1c, core.k2c, core.k3c, core.Theta, core.rP) == (0.8, 0.45, 0.12, 0.25, 0.6, 0.4, 0.5, 1.25, 0.35)

A = core.A1_kept1
At = [[None] * 6 for _ in range(6)]
for i in range(6):
    deg1 = int(A[i].sum()) + 1
    for j in range(6):
        At[i][j] = q(1, deg1) if (A[i, j] == 1 or i == j) else None
ang = arb.pi() * 37 / 180
U = [q(5, 2) * ang.cos(), q(5, 2) * ang.sin()]
tau0 = VP.tau0.reshape(-1)
TAU0 = [arb(float(v)) for v in tau0]                      # doubles exacts


def tanh_s(z):
    e = (z * 2).exp()
    return (e - 1) / (e + 1)


def tanh_a(z):
    return z.tanh()


def norm_lo(a, b):
    la, lb = a.abs_lower(), b.abs_lower()
    return (la * la + lb * lb).sqrt()


def norm_hi(a, b):
    ua, ub = a.abs_upper(), b.abs_upper()
    return (ua * ua + ub * ub).sqrt()


def nrm(a, b, series):
    """norme euclidienne ; l'arithmetique de boules perd la positivite de a*a quand le rayon est grand : on impose le terme constant
    par les bornes abs_lower/abs_upper (enclosure valide de la norme au carre)."""
    if not series:
        return norm_lo(a, b).union(norm_hi(a, b))
    a0, b0 = a.coeffs()[0], b.coeffs()[0]
    c0 = (a0.abs_lower() ** 2 + b0.abs_lower() ** 2).union(a0.abs_upper() ** 2 + b0.abs_upper() ** 2)
    sq = a * a + b * b
    cs = list(sq.coeffs())
    cs[0] = c0
    return arb_series(cs).sqrt()


def make_F(withP, series):
    th_fn = tanh_s if series else tanh_a

    def F(x):
        dim = 37 if withP else 36
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
        out = [None] * dim
        for k in range(12):
            out[k] = x[12 + k]
            u = U[k % 2] if k // 2 == 0 else None
            v = -gamma0 * x[12 + k] - x[k] + zeta * th[k]
            out[12 + k] = v + u if u is not None else v
            out[24 + k] = alpha * th[k] - beta * x[24 + k]
        if withP:
            nh = nrm(x[0], x[1], series)
            nv = nrm(x[12], x[13], series)
            out[36] = k1 * nh + k2 * nv - k3 * x[36]
        return out
    return F


F_ser = {False: make_F(False, True), True: make_F(True, True)}
F_sca = {False: make_F(False, False), True: make_F(True, False)}


def jets(x0, n, withP):
    ctx.cap = n + 1
    dim = len(x0)
    x = [arb_series([c]) for c in x0]
    F = F_ser[withP]
    for _ in range(n):
        f = F(x)
        x = [arb_series([x0[i]]) + f[i].integral() for i in range(dim)]
    return [list(s.coeffs()) + [arb(0)] * (n + 1 - len(s.coeffs())) for s in x]


def hull_inflate(b, rel=q(1, 4)):
    r = b.rad() * rel + arb("1e-70")
    return b + arb(0).union(r) - arb(0).union(r) if False else b + (-r).union(r)


def apriori(X, h, withP):
    dim = len(X)
    F = F_sca[withP]
    hI = arb(0).union(h)
    F0 = F(X)
    B = [X[i] + hI * F0[i] for i in range(dim)]
    for _ in range(80):
        Bi = [hull_inflate(b) for b in B]
        FB = F(Bi)
        Bn = [X[i] + hI * FB[i] for i in range(dim)]
        if all(Bi[i].contains(Bn[i]) for i in range(dim)):
            return Bi
        B = [Bi[i].union(Bn[i]) for i in range(dim)]
    raise RuntimeError("enclosure a priori non trouvee (h trop grand)")


class Slab:
    def __init__(self, X, h, withP):
        self.h, self.withP = h, withP
        self.c = jets(X, ORD, withP)
        self.B = apriori(X, h, withP)
        cB = jets(self.B, ORD + 1, withP)
        self.rem = [ci[ORD + 1] for ci in cB]
        hp = [arb(1)]
        for _ in range(ORD + 1):
            hp.append(hp[-1] * h)
        self.end = [sum((self.c[i][k] * hp[k] for k in range(ORD + 1)), arb(0)) + self.rem[i] * hp[ORD + 1] for i in range(len(X))]

    def ev(self, S, i):
        c = self.c[i]
        v = c[ORD]
        for k in range(ORD - 1, -1, -1):
            v = v * S + c[k]
        # reste : rem * S^(ORD+1)  avec S in [0,h]
        return v + self.rem[i] * S ** (ORD + 1)

    def vec(self, S):
        return [self.ev(S, i) for i in range(len(self.c))]


report = {}
t_start = time.time()
# ------------------------------------------------------------------ etape 0 : [0, t0], developpement en t = 0
t0f = fmpq(1, 100)
t0 = arb(t0f)
X0 = [arb(0)] * 24 + TAU0
S0 = Slab(X0, t0, False)
print("etape 0 : ordre %d, h = %s, largeur de l'enclosure a priori (max) = %s" % (ORD, t0f, max(float(b.rad()) for b in S0.B)))
St = arb(0).union(t0)

ok_orders = True
hats = {}
for k in range(6):
    m = NODE_M[k]
    # ordres d'annulation exacts : V_k coefficients j <= 2m nuls, H_k coefficients j <= 2m+1 nuls
    for comp in range(2):
        for j in range(0, 2 * m + 1):
            ok_orders &= S0.c[12 + 2 * k + comp][j].is_zero()
        for j in range(0, 2 * m + 2):
            ok_orders &= S0.c[2 * k + comp][j].is_zero()

    def hat(idx, order):
        c = S0.c[idx]
        v = c[ORD]
        # sum_{j=order}^{ORD} c_j S^(j-order) + rem * S^(ORD+1-order)
        v = c[ORD]
        for j in range(ORD - 1, order - 1, -1):
            v = v * St + c[j]
        return v + S0.rem[idx] * St ** (ORD + 1 - order)
    Vh = [hat(12 + 2 * k + comp, 2 * m + 1) for comp in range(2)]
    Hh = [hat(2 * k + comp, 2 * m + 2) for comp in range(2)]
    hats[k] = dict(Vlo=norm_lo(*Vh), Vhi=norm_hi(*Vh), Hlo=norm_lo(*Hh), Hhi=norm_hi(*Hh), V0=(S0.c[12 + 2 * k][2 * m + 1], S0.c[12 + 2 * k + 1][2 * m + 1]))
print("ordres d'annulation en t = 0 (coefficients exactement nuls, tous noeuds) : %s" % ok_orders)
assert ok_orders
print("quotients V_k/t^(2m+1), H_k/t^(2m+2) sur [0, t0] : minorants certifies (norme)")
for k in range(6):
    h_ = hats[k]
    print("  noeud %d (m=%d) : ||Vhat|| >= %s (<= %s) ; ||Hhat|| >= %s (<= %s)" % (k, NODE_M[k], dn(h_['Vlo'], 8), up(h_['Vhi'], 8), dn(h_['Hlo'], 8), up(h_['Hhi'], 8)))
    assert h_['Vlo'] > 0 and h_['Hlo'] > 0
report['hats_lower_bounds_[0,t0]'] = {k: dict(V=dict(lo=qs(exq_lo(hats[k]['Vlo']))), H=dict(lo=qs(exq_lo(hats[k]['Hlo'])))) for k in range(6)}

# H5 sur [0,t0]
tau_min = {}
for k in range(6):
    S_ = S0.vec(St)
    n = norm_lo(S_[24 + 2 * k], S_[24 + 2 * k + 1])
    assert n > 0
    tau_min[k] = n.lower()
# pression de depart du noeud 0 a t0 et bornes grossieres sur [0,t0]
intg = lambda lo, hi, p: (lo, hi)
V0lo, V0hi, H0lo, H0hi = hats[0]['Vlo'], hats[0]['Vhi'], hats[0]['Hlo'], hats[0]['Hhi']
Iint = k2 * arb(0).union(1) * 0  # placeholder pour la lisibilite
Jlo = k2 * V0lo * t0 ** 2 / 2 + k1 * H0lo * t0 ** 3 / 3
Jhi = k2 * V0hi * t0 ** 2 / 2 + k1 * H0hi * t0 ** 3 / 3
expm = (-k3 * t0).exp()
P0_t0 = expm * (rP * Theta) + (expm.union(arb(1))) * (Jlo.union(Jhi))
print("P_0(t0) in [%s, %s]" % (dn(P0_t0, 8), up(P0_t0, 8)))
assert P0_t0 < Theta
supg = [arb(0)] * 6
for k in range(6):
    S_ = S0.vec(St)
    g = k1 * norm_hi(S_[2 * k], S_[2 * k + 1]) + k2 * norm_hi(S_[12 + 2 * k], S_[12 + 2 * k + 1])
    supg[k] = g.upper()
# controle explicite de P_0 sur tout [0,t0] : P_0' <= g_0 (P_0 >= 0)  =>  P_0(t) <= P_0(0) + t0 sup g_0
P0_sup_init = rP * Theta + t0 * supg[0]
print("P_0 sur [0,t0] : sup <= P_0(0) + t0 sup g_0 <= %s  (< Theta = 1.25) ; sup g_0 <= %s" % (up(P0_sup_init, 8), up(supg[0], 8)))
assert P0_sup_init < Theta
report['P0_sup_[0,t0]_hi'] = qs(exq_hi(P0_sup_init))

# ------------------------------------------------------------------ etapes suivantes : (H,V,tau) a partir de t0 ; P_0 par quadrature centree
def p0_advance(sl, P_start, s_end, M=8):
    """P_0 en s_end dans le slab sl (formule de Duhamel, quadrature en forme centree sur M pieces).
    Renvoie (P_0(s_end), borne superieure rigoureuse de P_0 sur [0, s_end])."""
    Q = P_start                      # Q = P e^{k3 s}
    sup = P_start
    P = P_start
    for i in range(M):
        a, b = s_end * i / M, s_end * (i + 1) / M
        w = arb((b - a) / 2); mfq = (a + b) / 2
        Si = arb(a).union(arb(b))
        vm = sl.vec(arb(mfq)); vi = sl.vec(Si)
        gm = k1 * nrm(vm[0], vm[1], False) + k2 * nrm(vm[12], vm[13], False)
        Gm = (k3 * arb(mfq)).exp() * gm
        dv = F_sca[False](vi)
        nH, nV = nrm(vi[0], vi[1], False), nrm(vi[12], vi[13], False)
        gbox = k1 * nH + k2 * nV
        gp = k1 * (vi[0] * vi[12] + vi[1] * vi[13]) / nH + k2 * (vi[12] * dv[12] + vi[13] * dv[13]) / nV
        D = (k3 * Si).exp() * (k3 * gbox + gp)
        err = (w * w / 2) * (D.upper() - D.lower())
        Ii = 2 * w * Gm + (-err).union(err)
        sup = sup.union(P + 2 * w * gbox.upper())
        Q = Q + Ii
        P = Q * (-k3 * arb(b)).exp()
    return P, sup


P0cur = P0_t0
X = list(S0.end)
tn = t0f
slabs = []
crossing = None
extension_end = None
min_norm = {k: dict(V=None, H=None) for k in range(6)}
delta = fmpq(1, 50)
n_steps = 0
inc_window = False
while True:
    hq = min(fmpq(3, 100), tn / 8)
    h = arb(hq)
    sl = Slab(X, h, False)
    Sh = arb(0).union(h)
    vec = sl.vec(Sh)
    for k in range(6):
        nV = norm_lo(vec[12 + 2 * k], vec[13 + 2 * k]); nH = norm_lo(vec[2 * k], vec[2 * k + 1]); nT = norm_lo(vec[24 + 2 * k], vec[25 + 2 * k])
        assert nV > 0 and nH > 0 and nT > 0, ("annulation non exclue", n_steps, float(tn), k, nV, nH, nT)
        m = NODE_M[k]
        tmax = arb(tn + hq)
        for key, val in (('V', nV / tmax ** (2 * m + 1)), ('H', nH / tmax ** (2 * m + 2))):
            cur = min_norm[k][key]
            vl = val.lower()
            if cur is None or exq_lo(vl) < exq_lo(cur):
                min_norm[k][key] = vl
        nTl = nT.lower()
        if exq_lo(nTl) < exq_lo(tau_min[k]):
            tau_min[k] = nTl
        if k != 0:
            g = k1 * norm_hi(vec[2 * k], vec[2 * k + 1]) + k2 * norm_hi(vec[12 + 2 * k], vec[13 + 2 * k])
            gu = g.upper()
            if exq_hi(gu) > exq_hi(supg[k]):
                supg[k] = gu
    P0_end, P0_sup = p0_advance(sl, P0cur, hq)
    slabs.append((tn, hq, sl, P0cur))
    n_steps += 1
    if os.environ.get('DBG') and (n_steps < 4 or n_steps % 5 == 0 or float(tn) > 1.2):
        print('slab', n_steps, round(float(tn), 4), float(hq), 'P0 end', float(P0_end.mid()), 'rad', float(P0_end.rad()), 'sup', float(P0_sup.upper().mid()))
    if crossing is None:
        if not inc_window and P0_sup < Theta:
            pass
        else:
            # fenetre de croissance : P_0 < Theta certain au debut de la fenetre, P_0' > 0 certifie sur tous les slabs de la fenetre
            if not inc_window:
                assert P0cur < Theta, "debut de fenetre ambigu"
                inc_window = True; win_start = len(slabs) - 1
            dP_lo = k1 * norm_lo(vec[0], vec[1]) + k2 * norm_lo(vec[12], vec[13]) - k3 * P0_sup.upper()
            assert dP_lo > 0, ("P_0' > 0 non etabli sur le slab", n_steps, float(tn))
            if P0_end > Theta:
                # bissection dans ce slab
                lo, hi = fmpq(0), hq
                for _ in range(60):
                    mid = (lo + hi) / 2
                    pv, _ = p0_advance(sl, P0cur, mid)
                    if pv < Theta:
                        lo = mid
                    elif pv > Theta:
                        hi = mid
                    else:
                        break
                crossing = dict(slab=len(slabs) - 1, tn=tn, lo=lo, hi=hi, win_start=win_start)
                extension_end = tn + hq + delta
    X = sl.end
    P0cur = P0_end
    tn = tn + hq
    if extension_end is not None and tn >= extension_end:
        break
    if tn > fmpq(3):
        raise RuntimeError("pas de franchissement avant t = 3")
print("%d slabs, duree de calcul %.1f s" % (n_steps + 1, time.time() - t_start))

# ------------------------------------------------------------------ resultats
c = crossing
Tlo, Thi = c['tn'] + c['lo'], c['tn'] + c['hi']
sl = slabs[c['slab']][2]
SS = (arb(c['lo']).union(arb(c['hi'])))
vT = sl.vec(SS)
dP_T = k1 * norm_lo(vT[0], vT[1]) + k2 * norm_lo(vT[12], vT[13]) - k3 * Theta
print("T_1 in [%s, %s]  (largeur %.2e) ; DOP853 : 1.353301412736424" % (_dec(Tlo, 9, False), _dec(Thi, 9, True), float(Thi - Tlo)))
print("P_0'(T_1) >= %s   (numerique : 1.357069)" % dn(dP_T, 6))
assert dP_T > 0

# pressions des autres noeuds : P_j <= supg_j / k3
print("fenetre de croissance de P_0 : slabs %d a %d (P_0' > 0 certifie), P_0 < Theta au debut" % (c['win_start'], c['slab']))
print("pressions des autres noeuds : P_j <= sup g_j / kappa_3 :")
for k in range(1, 6):
    bound = supg[k] / k3
    print("   noeud %d : <= %s  (< Theta = 1.25)" % (k, up(bound, 6)))
    assert bound < Theta

# H5 : minorants des traces
print("(H5) min_j ||tau_j(t)|| >= : " + ", ".join("n%d >= %s" % (k, dn(tau_min[k], 5)) for k in range(6)))

# quotients apres t0
print("quotients ||V_k||/t^(2m+1) et ||H_k||/t^(2m+2) apres t0 (minorants, slabs) :")
for k in range(6):
    print("   noeud %d : V >= %s ; H >= %s" % (k, dn(min_norm[k]['V'], 9), dn(min_norm[k]['H'], 9)))

# recablage : cosinus a l'instant d'impact
tauT = [(vT[24 + 2 * k], vT[25 + 2 * k]) for k in range(6)]
for k in range(6):
    assert norm_lo(*tauT[k]) > 0
def cosv(a, b):
    return (a[0] * b[0] + a[1] * b[1]) / ((a[0] * a[0] + a[1] * a[1]).sqrt() * (b[0] * b[0] + b[1] * b[1]).sqrt())
cs = {j: cosv(tauT[0], tauT[j]) for j in (1, 4, 5)}
for j in (1, 4, 5):
    print("   cos(tau_0, tau_%d)(T_1) in [%s, %s]" % (j, dn(cs[j], 8), up(cs[j], 8)))
m14, m15 = cs[1] - cs[4], cs[1] - cs[5]
print("(H1) marge c_1 - c_4 >= %s ; c_1 - c_5 >= %s  (numerique : 1.8096 ; 0.004490)" % (dn(m14, 6), dn(m15, 6)))
assert m14 > 0 and m15 > 0
print("=> voisins de 0 conserves : {1} ; retires : {4,5} ; ajoutes : {2,3}  (mot (0,{1,2,3}), conforme a WORD_REF)")
print("duree totale %.1f s ; precision %d bits ; ordre de Taylor %d" % (time.time() - t_start, PREC, ORD))
report.update(
    T1_lo=qs(Tlo), T1_hi=qs(Thi), T1_lo_dec=_dec(Tlo, 9, False), T1_hi_dec=_dec(Thi, 9, True),
    dP0_lower=qs(exq_lo(dP_T)), dP0_lower_dec=dn(dP_T, 6),
    margin_c1_c4=qs(exq_lo(m14)), margin_c1_c4_dec=dn(m14, 6),
    margin_c1_c5=qs(exq_lo(m15)), margin_c1_c5_dec=dn(m15, 6),
    tau_min_lower={k: qs(exq_lo(tau_min[k])) for k in range(6)},
    tau_min_lower_dec={k: dn(tau_min[k], 5) for k in range(6)},
    quotients_after_t0_lower={k: dict(V=qs(exq_lo(min_norm[k]['V'])), H=qs(exq_lo(min_norm[k]['H']))) for k in range(6)},
    pressions_autres_noeuds_upper={k: qs(exq_hi(supg[k] / k3)) for k in range(1, 6)},
    cos_tau0_tauj={j: [qs(exq_lo(cs[j])), qs(exq_hi(cs[j]))] for j in (1, 4, 5)},
    convention="fractions exactes (bornes de boules arb, arrondi dirige) ; *_dec arrondis vers l'exterieur",
    precision_bits=PREC, taylor_order=ORD)
json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificat_rang1.json"), "w"), indent=1)
