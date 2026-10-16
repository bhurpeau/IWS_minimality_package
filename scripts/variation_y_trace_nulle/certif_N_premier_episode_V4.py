"""
Dependance : pip install python-flint==0.9.0 (Arb).  Execution : python3 certif_N_premier_episode_V4.py  (< 1 s, ecrit sortie_certification_N_V4.txt dans le dossier courant).
CERTIFICATION (arithmetique de boules, python-flint / arb) de la condition (N) dans le protocole du premier episode
(Theta = 11/5, forcage U = e sur le noeud 0, depart au repos, traces tau_i(0) = 3/5 e, graphe A1 "kept1").

Ce que le programme encadre RIGOUREUSEMENT (modulo la correction de arb/python-flint et de ce code, cf. controles en fin de fichier) :
  (1) la trajectoire de reference axiale (eps = 0) : h_i, v_i, tau_i (composantes e), w_i = tanh((A~ h)_i) ;
  (2) le zero s_* de v_0 : existence, UNICITE sur [0, t_fin] (signe de v_0 sur chaque pas, monotonie au voisinage du zero), simplicite (v_s < 0) ;
  (3) la reponse lineaire transverse X_V,0(s_*) (coefficient DA(p).e_n0 pour lbar = 1) du systeme
          X_H' = X_V ,   X_V' = -g0 X_V - X_H + zeta A~ X_H + lbar f e_0 ,   f = h_0 tau_0 e^{-beta s} / (1 + tau_0^2) ;
  (4) non-annulation : tau_i > 0 (tous i) ; v_0/s et h_0/s^2 minores au voisinage de s = 0 ; |h_0| minore sur [0.5, t_fin] ;
  (5) marges de pression : max_i P_i sur [0, 4.0] strictement sous Theta ; encadrement du premier declenchement (noeud 0, P_0 croissant).
Convention : toute DECISION (signe, inegalite, bracketing) repose sur des comparaisons de boules Arb ; les conversions en float ne servent qu'a l'AFFICHAGE.
Methode : integrateur de Taylor valide d'ordre M par pas h = 1/20 ; enclosure a priori de Picard (x0 + [0,h] f(B) dans B) ;
reste de Lagrange evalue sur B ; systeme polynomial (w = tanh(z) -> w' = (1-w^2) z', E = e^{-beta s}, q = 1/(1+tau_0^2)).
Les coefficients du noyau sont les rationnels exacts (zeta 4/5, alpha 9/20, beta 3/25, g0 1/4, k1 3/5, k2 2/5, k3 1/2, Theta 11/5, rP 7/20).
"""
import sys
from flint import arb, fmpq, ctx

ctx.prec = 200
M = 22                       # ordre de Taylor
H_STEP = fmpq(1, 20)         # pas
T_END_STEPS = 92             # 92 pas -> t = 4.6


def Q(a, b=1):
    return arb(fmpq(a, b))


def CHECK(cond, msg):
    """Echec bruyant : les comparaisons `x > c` / `x < c` entre boules Arb sont vraies seulement si elles sont CERTAINES."""
    if not bool(cond):
        raise AssertionError("CERTIFICAT ECHOUE : " + msg)
    return True


def dec_bounds(x, k=10):
    """Bornes decimales RIGOUREUSES de la boule x : (floor(10^k lo)/10^k, ceil(10^k up)/10^k), arrondis vers l'exterieur."""
    a = x * (10 ** k)
    lo_i = a.lower().floor().unique_fmpz(); up_i = a.upper().ceil().unique_fmpz()
    CHECK(lo_i is not None and up_i is not None, "bornes decimales non uniques")
    return fmpq(lo_i, 10 ** k), fmpq(up_i, 10 ** k)


def fmt(q, k=10):
    return "%.*f" % (k, float(q))     # affichage seulement ; la rigueur est portee par dec_bounds (valeurs exactes fmpq)


gam0, zeta, alpha, beta = Q(1, 4), Q(4, 5), Q(9, 20), Q(3, 25)
k1, k2, k3, Theta, rP = Q(3, 5), Q(2, 5), Q(1, 2), Q(11, 5), Q(7, 20)

edges = [(0, 1), (0, 4), (0, 5), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)]      # A1 "kept1" (iws_kairos_core.A1_kept1)
adj = [[0] * 6 for _ in range(6)]
for i, j in edges:
    adj[i][j] = adj[j][i] = 1
for i in range(6):
    adj[i][i] = 1
deg = [sum(r) for r in adj]
Ad = [[(Q(1, deg[i]) if adj[i][j] else None) for j in range(6)] for i in range(6)]
NB = [[j for j in range(6) if adj[i][j]] for i in range(6)]

# indices : h 0-5, v 6-11, tau 12-17, w 18-23, XH 24-29, XV 30-35, E 36, q 37
NV = 38
IH, IV, IT, IW, IXH, IXV, IE, IQ = 0, 6, 12, 18, 24, 30, 36, 37


def taylor(x0, order):
    """Coefficients de Taylor (jusqu'a l'ordre `order`) de la solution de l'EDO polynomiale issue de x0 (liste de NV boules)."""
    c = [[x0[i]] + [None] * order for i in range(NV)]
    s = [[None] * (order + 1) for _ in range(6)]
    u = [[None] * (order + 1) for _ in range(6)]
    uX = [[None] * (order + 1) for _ in range(6)]
    a1 = [None] * (order + 1); a2 = [None] * (order + 1); f = [None] * (order + 1)
    q2 = [None] * (order + 1); r1 = [None] * (order + 1); td0 = [None] * (order + 1)
    for k in range(order):
        for i in range(6):
            wi = c[IW + i]
            s[i][k] = sum((wi[j] * wi[k - j] for j in range(k + 1)), arb(0))
            u[i][k] = sum((Ad[i][j] * c[IV + j][k] for j in NB[i]), arb(0))
            uX[i][k] = sum((Ad[i][j] * c[IXH + j][k] for j in NB[i]), arb(0))
        a1[k] = sum((c[IH][j] * c[IT][k - j] for j in range(k + 1)), arb(0))
        a2[k] = sum((a1[j] * c[IE][k - j] for j in range(k + 1)), arb(0))
        f[k] = sum((a2[j] * c[IQ][k - j] for j in range(k + 1)), arb(0))
        q2[k] = sum((c[IQ][j] * c[IQ][k - j] for j in range(k + 1)), arb(0))
        r1[k] = sum((q2[j] * c[IT][k - j] for j in range(k + 1)), arb(0))
        td0[k] = alpha * c[IW][k] - beta * c[IT][k]
        dq = -2 * sum((r1[j] * td0[k - j] for j in range(k + 1)), arb(0))
        kk = k + 1
        for i in range(6):
            c[IH + i][kk] = c[IV + i][k] / kk
            dv = -gam0 * c[IV + i][k] - c[IH + i][k] + zeta * c[IW + i][k]
            if i == 0 and k == 0:
                dv = dv + 1                                   # forcage U = 1 sur le noeud 0
            c[IV + i][kk] = dv / kk
            c[IT + i][kk] = (alpha * c[IW + i][k] - beta * c[IT + i][k]) / kk
            dw = u[i][k] - sum((s[i][j] * u[i][k - j] for j in range(k + 1)), arb(0))
            c[IW + i][kk] = dw / kk
            c[IXH + i][kk] = c[IXV + i][k] / kk
            dxv = -gam0 * c[IXV + i][k] - c[IXH + i][k] + zeta * uX[i][k]
            if i == 0:
                dxv = dxv + f[k]
            c[IXV + i][kk] = dxv / kk
        c[IE][kk] = -beta * c[IE][k] / kk
        c[IQ][kk] = dq / kk
    return c


def horner(coefs, tau, rem=None, m=None):
    """sum coefs[j] tau^j  (+ rem * tau^(m+1))."""
    r = arb(0)
    for cj in reversed(coefs):
        r = r * tau + cj
    if rem is not None:
        r = r + rem * tau ** (len(coefs))
    return r


def a_priori(x0, h):
    """Enclosure a priori de Picard-Lindelof sur [0, h].
    Si B verifie  x0 + [0,h] f(B)  contenu dans  B  (f = champ, evalue en arithmetique de boules), alors la solution issue de x0 existe
    sur [0,h] et reste dans B ; de plus x(t) = x0 + int_0^t f(x(s)) ds appartient a  newB = x0 + [0,h] f(B)  pour tout t dans [0,h].
    newB est donc elle-meme une enclosure valide (et plus fine que B) : on la renvoie directement, sans second test
    (l'inclusion newB dans B deja verifiee et l'isotonie de l'evaluation par intervalles suffisent)."""
    t01 = arb(h / 2, h / 2)
    B = [x + arb(0, fmpq(1, 10 ** 6)) for x in x0]
    for it in range(60):
        c1 = taylor(B, 1)
        newB = [x0[i] + t01 * c1[i][1] for i in range(NV)]
        if all(B[i].contains(newB[i]) for i in range(NV)):
            return newB
        B = [B[i].union(newB[i]) for i in range(NV)]
        B = [b + arb(0, b.rad() * fmpq(1, 2) + fmpq(1, 10 ** 9)) for b in B]
    raise RuntimeError("enclosure a priori non trouvee")


def one_step(x0, h):
    B = a_priori(x0, h)
    c = taylor(x0, M)                       # coefficients 0..M en x0
    R = taylor(B, M + 1)                    # coefficient M+1 en B
    Rc = [R[i][M + 1] for i in range(NV)]
    ha = arb(h)
    xend = [horner(c[i], ha, Rc[i]) for i in range(NV)]
    return dict(c=c, R=Rc, B=B, xend=xend, h=h)


def tube(rec, var, tau):
    return horner(rec['c'][var], tau, rec['R'][var])


def lo(x): return x.lower()
def up(x): return x.upper()


def main():
    out = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s); out.append(s)

    x0 = [arb(0)] * NV
    x0 = list(x0)
    P("Conditions initiales : H = V = 0 ; tau_i(0) = 3/5 e ; P_0(0) = r_P Theta = 7/20 * 11/5 = 77/100 ; P_i(0) = 0 (i >= 1) ; Theta = 11/5.")
    CHECK(rP * Theta == Q(77, 100) or abs(rP * Theta - Q(77, 100)) < Q(1, 10 ** 30), "P_0(0) = 77/100")
    for i in range(6):
        x0[IT + i] = Q(3, 5)
    x0[IE] = arb(1)
    x0[IQ] = 1 / (1 + Q(3, 5) ** 2)
    recs = []
    x = x0
    h = H_STEP
    t01 = arb(h / 2, h / 2)
    for k in range(T_END_STEPS):
        rec = one_step(x, h)
        rec['t0'] = fmpq(k) * h
        recs.append(rec)
        x = rec['xend']
    P("largeur max de la boite finale (t = %s) : %s" % (float(recs[-1]['t0'] + h), max(float(b.rad()) for b in x)))

    # ---------------------------------------------------------------- (4) non-annulation des traces et de h_0, v_0 pres de 0
    for r in recs:
        for i in range(6):
            CHECK(tube(r, IT + i, t01) > Q(46, 100), "tau_%d^x >= 0.46" % i)
    tau_lb = min(float(lo(tube(r, IT + i, t01))) for r in recs for i in range(6))
    P("(4a) [verifie] tau_i^x >= 0.46 pour tout i sur [0, 4.6] (min calcule : %.6f)" % tau_lb)
    r0 = recs[0]
    # v_0 / s sur [0, h] : coefficients decales
    def shifted(var, sh):
        cc = r0['c'][var][sh:]
        rr = arb(0)
        for cj in reversed(cc):
            rr = rr * t01 + cj
        return rr + r0['R'][var] * t01 ** (M + 1 - sh)
    q_v = shifted(IV, 1)
    q_h = shifted(IH, 2)
    CHECK(q_v > Q(993, 1000), "v_0/s >= 0.993 sur [0,1/20]")
    CHECK(q_h > Q(497, 1000), "h_0/s^2 >= 0.497 sur [0,1/20]")
    P("(4b) [verifie] v_0(s)/s >= 0.993 sur ]0, 1/20] :", q_v.str(8))
    P("(4c) [verifie] h_0(s)/s^2 >= 0.497 sur ]0, 1/20] :", q_h.str(8))
    hmin = min(float(lo(tube(r, IH, t01))) for r in recs[1:])      # h_0 sur [1/20, 4.6] (h_0 > 0 : ||H_0|| = h_0)
    hmin10 = min(float(lo(tube(r, IH, t01))) for r in recs[10:])
    for k_, r in enumerate(recs[1:], start=1):
        CHECK(tube(r, IH, t01) > Q(626, 10 ** 6), "h_0 >= 0.000626 sur [0.05, 4.6]")
    for r in recs[10:]:
        CHECK(tube(r, IH, t01) > Q(117, 1000), "h_0 >= 0.117 sur [0.5, 4.6]")
    P("(4d) [verifie] h_0 >= 0.000626 sur [0.05, 4.6] (min calcule %.6f) ; h_0 >= 0.117 sur [0.5, 4.6] (min calcule %.6f)" % (hmin, hmin10))

    # ---------------------------------------------------------------- (2) zero de v_0
    kz = None
    for k, r in enumerate(recs):
        vt = tube(r, IV, t01)
        if k == 0:
            CHECK(q_v > 0, "v_0/s > 0 sur le premier pas")
            continue
        if vt > 0:
            continue
        kz = k
        break
    CHECK(kz is not None, "le signe de v_0 doit cesser d'etre garanti quelque part")
    P("(2a) v_0 > 0 certifie sur ]0, %.2f] ; premier pas ou le signe n'est plus garanti : k = %d  (t in [%.2f, %.2f])" %
      (float(recs[kz]['t0']), kz, float(recs[kz]['t0']), float(recs[kz]['t0'] + h)))
    rz = recs[kz]
    dvt = []
    # derivee de v_0 sur le pas : v_0' = -g0 v_0 - h_0 + zeta w_0 + 1, evalue sur les tubes
    vdot = -gam0 * tube(rz, IV, t01) - tube(rz, IH, t01) + zeta * tube(rz, IW, t01) + 1
    CHECK(vdot < 0, "v_0' < 0 sur le pas du zero")
    P("(2b) [verifie] v_0' sur le pas du zero :", vdot.str(8), "  < 0 (monotone) ; sup <", float(up(vdot)))
    # bissection sur tau in [0, h]
    a, b = fmpq(0), h
    va = tube(rz, IV, arb(a)); vb = tube(rz, IV, arb(b))
    CHECK(va > 0 and vb < 0, "signes de v_0 aux extremites du pas du zero")
    for _ in range(60):
        mdl = (a + b) / 2
        vm = tube(rz, IV, arb(mdl))
        if vm > 0:
            a = mdl
        elif vm < 0:
            b = mdl
        else:
            break
    tz = arb((a + b) / 2, (b - a) / 2)
    s_star = arb(rz['t0']) + tz
    P("(2c) s_* dans", s_star.str(15), "  (v_0 change de signe, unique : monotone sur le pas ; v_0 > 0 avant)")
    vs = vdot
    xv0 = tube(rz, IXV, tz)
    vs_b = -gam0 * tube(rz, IV, tz) - tube(rz, IH, tz) + zeta * tube(rz, IW, tz) + 1
    CHECK(vs_b < Q(-5578, 10 ** 4) and vs_b > Q(-55784, 10 ** 5), "v_s dans ]-0.55784, -0.5578[")
    P("(2d) [verifie] pente en s_* : v_s =", vs_b.str(10), " dans ]-0.55784, -0.5578[")
    CHECK(xv0 > Q(49547397, 10 ** 8) and xv0 < Q(49547398, 10 ** 8), "0.49547397 < X_V,0(s_*) < 0.49547398")
    lo_d, up_d = dec_bounds(xv0, 12)
    P("(3)  [verifie] X_V,0(s_*) = DA(p).e_n0  (lbar = 1) =", xv0.str(12))
    P("     encadrement RIGOUREUX (arrondis vers l'exterieur, 12 decimales) : %s <= X_V,0(s_*) <= %s" % (fmt(lo_d, 12), fmt(up_d, 12)))
    P("     et en particulier 0.49547397 < X_V,0(s_*) < 0.49547398")
    P("     h_0(s_*) =", tube(rz, IH, tz).str(10), "  tau_0(s_*) =", tube(rz, IT, tz).str(10))

    # signe de v_0 apres le zero : sur les pas suivants, v_0 < 0
    for r in recs[kz + 1:]:
        CHECK(tube(r, IV, t01) < 0, "v_0 < 0 apres le zero")
    P("(2e) [verifie] v_0 < 0 sur les pas k > %d jusqu'a t = 4.6" % kz)

    # ---------------------------------------------------------------- (5) pressions
    # P_i(tau) = e^{-k3 tau} ( P_i(0) + Phi(tau) ),  Phi(tau) = int_0^tau e^{k3 s} g(s) ds,  g = k1 |h_i| + k2 |v_i|  (axial : ||.|| = |.|)
    # g est un polynome (tube de Taylor) a signes certifies ; le reste de Lagrange et la queue de l'exponentielle sont bornes explicitement.
    def expo_poly(deg):
        e = [Q(1)]
        for j in range(1, deg + 1):
            e.append(e[-1] * k3 / j)
        return e
    EXP = expo_poly(M)
    hh_ = arb(h)

    def Phi(gc, gR, a_, b_):
        """int_a^b e^{k3 s} g(s) ds, g(s) = sum gc[j] s^j + gR s^(M+1) (reste), a_, b_ boules dans [0,h]."""
        prod = [arb(0)] * (2 * M + 1)
        for i in range(M + 1):
            for j in range(M + 1):
                prod[i + j] = prod[i + j] + gc[i] * EXP[j]
        def G(t):
            r = arb(0)
            for kq in range(len(prod) - 1, -1, -1):
                r = r * t + prod[kq] / (kq + 1)
            return r * t
        main_ = G(b_) - G(a_)
        # reste de Lagrange de g : |int e^{k3 s} gR s^(M+1)| <= |gR| e^{k3 h} h^(M+2)/(M+2)
        gRabs = abs(gR)
        r1 = gRabs * (k3 * hh_).exp() * hh_ ** (M + 2) / (M + 2)
        # queue de l'exponentielle : |e^{k3 s} - EXP_M(s)| <= e^{k3 h} (k3 h)^(M+1)/(M+1)!
        supg = sum((abs(gc[j]) * hh_ ** j for j in range(M + 1)), arb(0)) + gRabs * hh_ ** (M + 1)
        fact = arb(1)
        for j in range(1, M + 2):
            fact = fact * j
        r2 = hh_ * supg * (k3 * hh_).exp() * (k3 * hh_) ** (M + 1) / fact
        err = r1 + r2
        return main_ + arb(0, err.upper())

    def sign_of(x):
        """Signe CERTAIN de la boule x (comparaisons Arb), 0 si indetermine."""
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    Pst = [rP * Theta] + [arb(0)] * 5
    supP = [0.0] * 6
    ncrude = 0
    for k, r in enumerate(recs):
        newP = []; tubeP = []
        for i in range(6):
            th_ = tube(r, IH + i, t01); tv_ = tube(r, IV + i, t01)
            sh, sv = sign_of(th_), sign_of(tv_)
            if k == 0 and i == 0:
                sh, sv = 1, 1                 # h_0 = s^2 q_h, v_0 = s q_v avec q_h, q_v > 0 (points 4b, 4c)
            cstep = r['c']
            if sh != 0 and sv != 0:
                gc = [k1 * sh * cstep[IH + i][j] + k2 * sv * cstep[IV + i][j] for j in range(M + 1)]
                gR = k1 * sh * r['R'][IH + i] + k2 * sv * r['R'][IV + i]
                Pend = (-k3 * hh_).exp() * (Pst[i] + Phi(gc, gR, arb(0), hh_))
                Ptube = (-k3 * t01).exp() * (Pst[i] + Phi(gc, gR, arb(0), t01))
            elif i == 0 and k == kz:
                # v_0 change de signe en tz : g = k1 h_0 + k2 v_0 avant, k1 h_0 - k2 v_0 apres
                gcp = [k1 * cstep[IH][j] + k2 * cstep[IV][j] for j in range(M + 1)]
                gcm = [k1 * cstep[IH][j] - k2 * cstep[IV][j] for j in range(M + 1)]
                gRp = k1 * r['R'][IH] + k2 * r['R'][IV]; gRm = k1 * r['R'][IH] - k2 * r['R'][IV]
                tzl, tzu = arb(a), arb(b)           # tz in [a, b] (bracket certifie)
                # [0,a] signe +, [a,b] (largeur ~1e-15) borne grossiere, [b,h] signe -
                gmax = k1 * tube(r, IH, t01) + k2 * abs(tube(r, IV, t01))
                mid_crude = arb(0, ((arb(b) - arb(a)) * gmax.upper() * (k3 * hh_).exp()).upper())
                Pend = (-k3 * hh_).exp() * (Pst[i] + Phi(gcp, gRp, arb(0), tzl) + mid_crude + Phi(gcm, gRm, tzu, hh_))
                gb = k1 * th_ + k2 * abs(tv_)
                Ptube = Pst[i] * (-k3 * t01).exp() + gb * (1 - (-k3 * t01).exp()) / k3
            else:
                ncrude += 1
                gb = k1 * abs(th_) + k2 * abs(tv_)
                et = (-k3 * t01).exp(); e1 = (-k3 * hh_).exp()
                Ptube = Pst[i] * et + gb * (1 - et) / k3
                Pend = Pst[i] * e1 + gb * (1 - e1) / k3
            newP.append(Pend); tubeP.append(Ptube)
            if (k + 1) <= 80:
                CHECK(Ptube < Q(2131, 1000), "P_%d < 2.131 sur [0,4]" % i)
                supP[i] = max(supP[i], float(up(Ptube)))
            if i >= 1:
                CHECK(Ptube < Q(74, 100), "P_%d < 0.74 sur [0,4.6]" % i)
        Pst = newP
        r['Pend'] = newP; r['Ptube'] = tubeP
    P("(5-) pas de pression traites par la borne grossiere (signe de h_i ou v_i non certifie sur le pas) :", ncrude, "sur", 6 * len(recs))
    P("(5a) [verifie] P_i < 2.131 < Theta pour t <= 4.0 et tout i ; bornes calculees :", [round(v, 5) for v in supP], "  Theta = 2.2")
    P("(5b) marge min : Theta - max_i sup P_i = %.5f" % (2.2 - max(supP)))
    for tt in [4.35, 4.40, 4.45, 4.50, 4.55]:
        kk = int(round(tt * 20)) - 1
        P("     t = %.2f : P_0 = %s ; max_{i>0} P_i <= %.5f" % (tt, recs[kk]['Pend'][0].str(8), max(float(up(recs[kk]['Pend'][i])) for i in range(1, 6))))
    CHECK(recs[88]['Pend'][0] < Theta and recs[89]['Pend'][0] > Theta, "P_0(4.45) < Theta < P_0(4.50)")
    hh2 = [k1 * tube(recs[kk], IH, t01) + k2 * (-tube(recs[kk], IV, t01)) - k3 * Theta for kk in range(80, 92)]
    for z in hh2:
        CHECK(z > Q(214, 1000), "g - k3 Theta >= 0.214 sur [4.0, 4.6]")
    gmarge = min(float(lo(z)) for z in hh2)
    P("(5c) sur [4.0, 4.6] : g = k1 h_0 + k2 |v_0| verifie g - k3 Theta >= %.5f > 0 ;" % gmarge)
    P("     donc tant que P_0 <= Theta, P_0' = g - k3 P_0 >= %.5f > 0 : P_0 croit strictement jusqu'a son premier passage par Theta," % gmarge)
    P("     lequel est unique ; avec P_0(4.45) < Theta < P_0(4.50) :  T_1(p, eps=0) dans ]4.45, 4.50[ ; sup_{t<=4.0} P_0 < Theta (5a).")
    supP_all = [max(float(up(r['Ptube'][i])) for r in recs[:92]) for i in range(1, 6)]
    P("(5d) [verifie] P_i < 0.74 (i = 1..5) sur [0, 4.6] ; bornes calculees :", [round(v, 5) for v in supP_all], " << Theta : le noeud 0 est l'unique candidat au declenchement.")
    P("TOUS LES CONTROLES CERTIFIES ONT REUSSI (comparaisons de boules Arb ; un echec leve AssertionError).")

    open('sortie_certification_N_V4.txt', 'w').write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
