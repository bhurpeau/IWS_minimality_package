"""Coordonnees tau = s - sigma(th) (zero immobilise en tau=0) : W~(tau,th) = W(sigma(th)+tau, th) = (tau*m, a+tau*nu).
Formule : D^2 F_in = int [ D^2g~ rho + 2 Dg~ (w.DW~) + g~ ( w.D^2 W~ + |P_perp DW~|^2 / rho ) ] dtau,
avec |P_perp DW~|^2/rho = tau^2 N^2/rho^3, N = m Da - a Dm + tau (m Dnu - nu Dm).
Tests : (1) formule vs differences finies de F_in (fenetre fixe en tau), familles A (a~th) et B (a~th^2) ;
(2) exemple a direction tournante W=(s-th)(cos th, sin th) ; (3) contre-exemple de poids g=1/Phi(th)."""
from mpmath import mp, mpf, quad, sqrt, cos, sin, log, fabs, diff
mp.dps = 30
c = mpf('0.3')
def fam(kind):
    if kind == 'A':
        W2  = lambda s,t: t + mpf('0.5')*s*t + mpf('0.7')*s**2
        W2t = lambda s,t: 1 + mpf('0.5')*s;  W2s = lambda s,t: mpf('0.5')*t + mpf('1.4')*s
        W2tt = lambda s,t: mpf(0)
    else:
        W2  = lambda s,t: t**2 + mpf('0.5')*s*t + mpf('0.7')*s**2
        W2t = lambda s,t: 2*t + mpf('0.5')*s;  W2s = lambda s,t: mpf('0.5')*t + mpf('1.4')*s
        W2tt = lambda s,t: mpf(2)
    W1 = lambda s,t: s + c*t + mpf('0.4')*s**2
    return W1, W2, W2t, W2s, W2tt
def setup(kind, t):
    W1, W2, W2t, W2s, W2tt = fam(kind)
    sig = (-1 + sqrt(1 - mpf('1.6')*c*t))/mpf('0.8')
    q_s = 1 + mpf('0.8')*sig
    s1 = -c/q_s                               # sigma'
    s2 = -mpf('0.8')*s1**2/q_s                # sigma''
    def Wt(tau): s = sig + tau; return (W1(s,t), W2(s,t))
    def dW(tau):
        s = sig + tau
        Wth = (c, W2t(s,t)); Ws = (1 + mpf('0.8')*s, W2s(s,t))
        return (Wth[0] + Ws[0]*s1, Wth[1] + Ws[1]*s1)
    def d2W(tau):
        s = sig + tau
        Wss = (mpf('0.8'), mpf('1.4')); Wst = (mpf(0), mpf('0.5')); Wtt = (mpf(0), W2tt(s,t))
        Ws = (1 + mpf('0.8')*s, W2s(s,t))
        return tuple(Wtt[i] + 2*Wst[i]*s1 + Wss[i]*s1**2 + Ws[i]*s2 for i in (0,1))
    g  = lambda tau: 1 + mpf('0.5')*(sig + tau)
    return sig, s1, s2, Wt, dW, d2W, g
R0 = mpf('0.3')
def F_in(kind, t):
    sig, s1, s2, Wt, dW, d2W, g = setup(kind, t)
    return quad(lambda tau: g(tau)*sqrt(Wt(tau)[0]**2 + Wt(tau)[1]**2), [-R0, 0, R0])
def D2F_formula(kind, t):
    sig, s1, s2, Wt, dW, d2W, g = setup(kind, t)
    def integrand(tau):
        w = Wt(tau); r = sqrt(w[0]**2 + w[1]**2); wh = (w[0]/r, w[1]/r)
        d1 = dW(tau); d2 = d2W(tau)
        dg, d2g = mpf('0.5')*s1, mpf('0.5')*s2
        wd1 = wh[0]*d1[0] + wh[1]*d1[1]
        perp2 = d1[0]**2 + d1[1]**2 - wd1**2
        return d2g*r + 2*dg*wd1 + g(tau)*(wh[0]*d2[0] + wh[1]*d2[1] + perp2/r)
    return quad(integrand, [-R0, 0, R0])
h = mpf('1e-6')
print("(1) D^2 F_in : formule en coordonnees tau vs differences finies (fenetre fixe en tau)")
for kind in ('A', 'B'):
    print("  famille", kind)
    for e in ['1e-1', '1e-2', '1e-3', '1e-4']:
        t = mpf(e)
        fd = (F_in(kind, t+h) - 2*F_in(kind, t) + F_in(kind, t-h))/h**2
        fo = D2F_formula(kind, t)
        print("   th=%-6s formule=%12.6f  diff.finies=%12.6f  ecart=%.1e" % (e, float(fo), float(fd), float(fo-fd)))
print("(2) direction tournante W=(s-th)(cos th, sin th), e=(1,0) : exact")
th = mpf('0.4')
F  = lambda t: quad(lambda s: fabs(s-t), [-1, t, 1])
Fp = lambda t: quad(lambda s: fabs((s-t)*cos(t)), [-1, t, 1])
print("   F=%s  1+th^2=%s | F_par=%s  cos(th)(1+th^2)=%s" % (mp.nstr(F(th),12), mp.nstr(1+th**2,12), mp.nstr(Fp(th),12), mp.nstr(cos(th)*(1+th**2),12)))
print("   en coordonnees tau : W~=tau(cos th, sin th), rho=|tau|, DW~=tau(-sin th, cos th) orthogonal a W~ : |P_perp DW~|^2/rho = |tau| (integrable)")
print("   alors que a s fixe, |d_th p|^2/rho ~ sin^2(th)/|s-th| n'est pas integrable : la translation du zero est absorbee par tau = s - sigma(th)")
print("(3) contre-exemple de poids : W=(s,th), g=1/Phi(th), Phi(th)=int_{-1}^{1} sqrt(s^2+th^2) ds")
Phi = lambda t: quad(lambda s: sqrt(s**2+t**2), [-1, 0, 1])
Fg  = lambda t: quad(lambda s: sqrt(s**2+t**2)/Phi(t), [-1, 0, 1])
for t in (mpf('0.1'), mpf('0.01')):
    print("   th=%s  F=%s (=1)   Phi''(th) approx = %.4f  (diverge en 2 ln(1/th))" % (t, mp.nstr(Fg(t), 15), float((Phi(t+h)-2*Phi(t)+Phi(t-h))/h**2)))
