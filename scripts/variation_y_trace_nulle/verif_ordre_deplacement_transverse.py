"""Verification analytique/numerique : classement des zeros par l'ordre du deplacement transverse.
F(vartheta) = Phi(a(vartheta)),  Phi(a) = int_{-1}^{1} sqrt(t^2+a^2) dt = sqrt(1+a^2) + a^2 asinh(1/|a|).
Tests : (1) formule exacte vs quadrature ; (2) developpement de B. ; (3) F(d)=Phi(d^2) est C^3, pas C^4 ;
(4) a = th1^2 - th2^2 : C^2 en 0 mais Phi''(a)|Da|^2 diverge sur la diagonale (pas C^2 sur la boule) ;
(5) a = th^m : C^2 ssi m>=2."""
from mpmath import mp, mpf, quad, sqrt, asinh, log, fabs, diff
mp.dps = 40
Phi  = lambda a: mpf(1) if a == 0 else sqrt(1+a*a) + a*a*asinh(1/fabs(a))
Phiq = lambda a: quad(lambda t: sqrt(t*t+a*a), [-1, 0, 1])
print("(1) formule exacte vs quadrature")
for d in [mpf('0.5'), mpf('0.1'), mpf('0.01')]:
    a = d**2
    print("  delta=%s  exact=%s  quad=%s  diff=%.2e" % (d, mp.nstr(Phi(a), 20), mp.nstr(Phiq(a), 20), float(Phi(a)-Phiq(a))))
print("(2) developpement 1 + d^4 ln(2/d^2) + d^4/2 + O(d^8)  (reste/d^8)")
for d in [mpf('0.2'), mpf('0.1'), mpf('0.05'), mpf('0.025')]:
    a = d**2
    r = Phi(a) - (1 + d**4*log(2/d**2) + d**4/2)
    r2 = r - d**8/8 + d**12/32
    print("  delta=%-6s reste=%.3e  reste/d^8=%.5f   (reste-d^8/8+d^12/32)/d^16=%.5f" % (d, float(r), float(r/d**8), float(r2/d**16)))
print("(3) F(d)=Phi(d^2) : derivees d'ordre k en d=h (centrees), comportement ~ d^(4-k) ln(1/d)")
F = lambda d: Phi(d**2)
for k in (2, 3, 4):
    vals = []
    for h in [mpf('1e-2'), mpf('1e-3'), mpf('1e-4')]:
        vals.append(float(diff(F, h, k)))
    print("  F^(%d)(h) pour h=1e-2,1e-3,1e-4 : %s" % (k, ["%.4g" % v for v in vals]))
print("   (F'' -> 0 ; F''' -> 0 ; F'''' diverge en ln : C^3 mais pas C^4)")
print("(4) a = th1^2 - th2^2, th2 = 0.3 fixe ; d^2F/dth1^2 en th1 = 0.3 +- e")
G = lambda t1: Phi(t1**2 - mpf('0.3')**2)
for e in [mpf('1e-1'), mpf('1e-2'), mpf('1e-3'), mpf('1e-4'), mpf('1e-5')]:
    t1 = mpf('0.3') + e
    d2 = diff(G, t1, 2)
    pred = 2*(2*t1)**2*log(2/fabs(t1**2-mpf('0.3')**2))   # Phi''(a)(Da)^2 ~ 2 ln(2/|a|) (2 th1)^2
    print("  e=%-8s  F''=%.4f   2(2th1)^2 ln(2/|a|)=%.4f" % (mp.nstr(e, 3), float(d2), float(pred)))
print("   a l'origine : F-1 = O(|th|^4 ln) donc D^2F(0)=0 ; mais D^2F non borne au voisinage (diagonales).")
print("(5) a = d^m : F''(h) pour h -> 0")
for m in (1, 2, 3):
    Fm = lambda d, m=m: Phi(d**m)
    vals = [float(diff(Fm, h, 2)) for h in [mpf('1e-2'), mpf('1e-3'), mpf('1e-4')]]
    print("  m=%d : F''(1e-2,1e-3,1e-4) = %s" % (m, ["%.4g" % v for v in vals]))

print("(6) lemme de Glaeser local : |Da|^2 <= 2 L |a| quand Da=0 sur Z (a in C^2)")
import numpy as np
# a = x^3 sur [-r,r], L = sup|a''| = 6r
for r in (0.5, 0.1, 0.01):
    x = np.linspace(-r, r, 200001); x = x[x != 0]
    ratio = (3*x**2)**2 / (2*6*r*np.abs(x**3))
    print("  a=x^3, r=%-5g max |Da|^2/(2L|a|) = %.4f  (<=1 attendu)" % (r, ratio.max()))
# a = th1^2 - th2^2 : Da != 0 sur les diagonales -> le rapport n'est pas borne
for e in (1e-2, 1e-4, 1e-6):
    t1, t2 = 0.3+e, 0.3
    a = t1**2-t2**2; Da2 = (2*t1)**2 + (2*t2)**2
    print("  a=th1^2-th2^2, e=%-6g |Da|^2/(2L|a|) = %.3g  (L=2)" % (e, Da2/(2*2*abs(a))))
# a = x^2 sin(1/x)-type oscillant avec Da=0 sur Z ? a = x^4 (sin(1/x)+2) >= 0 : verifier
for r in (0.1, 0.01):
    x = np.linspace(-r, r, 2000001); x = x[x != 0]
    a = x**4*(np.sin(1/x)+2); 
    Da = 4*x**3*(np.sin(1/x)+2) - x**2*np.cos(1/x)
    D2a = 12*x**2*(np.sin(1/x)+2) - 8*x*np.cos(1/x) - np.sin(1/x)   # borne non utilisee ici
    L = np.abs(D2a).max()
    print("  a=x^4(sin(1/x)+2) (C^{1,1}, D2a borne) r=%-5g max |Da|^2/(2L|a|)=%.3f avec L=%.2f" % (r, (Da**2/(2*L*np.abs(a))).max(), L))
