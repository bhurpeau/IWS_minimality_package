"""Verification numerique de la reduction (R) a regularite renforcee (plan, W in C^5, g in C^2) :
F(th) = int_J g(s) |W(s,th)| ds  =  b(th) Phi_eta(a(th)) + C^2,
b = g(sigma)/sqrt(A(sigma)), a = det(dW/ds, W)/|dW/ds| au minimum temporel sigma.
Test A : a(th) ~ th (zero transverse)  -> F'' ~ 2 b a'^2 ln(1/th)  (pente par decade = 2 b a'^2 ln 10)
Test B : a(th) ~ c th^2 (non colineaire)-> F'' converge (C^2)
Test C : a = th^2-0.01, zero regulier en th=0.1 -> F'' diverge en 0.1+e
Precision 30 chiffres, quadrature coupee au minimum sigma."""
from mpmath import mp, mpf, quad, sqrt, findroot, diff, log
mp.dps = 30
g  = lambda s: 1 + mpf('0.5')*s
def run(name, W, dW, th0, J=(-mpf('0.5'), mpf('0.5'))):
    def sigma(t):
        f_s = lambda s: 2*(W(s,t)[0]*dW(s,t)[0] + W(s,t)[1]*dW(s,t)[1])
        return findroot(f_s, mpf(0))
    def F(t):
        sg = sigma(t)
        n = lambda s: g(s)*sqrt(W(s,t)[0]**2 + W(s,t)[1]**2)
        return quad(n, [J[0], sg, J[1]])
    def a(t):
        sg = sigma(t); w, d = W(sg,t), dW(sg,t)
        return (d[0]*w[1]-d[1]*w[0])/sqrt(d[0]**2+d[1]**2)
    h = mpf('1e-7')
    def F2(t): return (F(t+h)-2*F(t)+F(t-h))/h**2
    print(name)
    for e in ['1e-1','1e-2','1e-3','1e-4','1e-5']:
        t = th0 + mpf(e)
        print("  e=%-6s a=%.3e   F''=%.5f" % (e, float(a(t)), float(F2(t))))
    return F, a, F2
c = mpf('0.3')
# Test A : a'(0)=1
WA  = lambda s,t: (s + c*t + mpf('0.4')*s**2, t + mpf('0.5')*s*t + mpf('0.7')*s**2)
dWA = lambda s,t: (1 + mpf('0.8')*s, mpf('0.5')*t + mpf('1.4')*s)
F,a,F2 = run("Test A (a ~ th, zero transverse)", WA, dWA, mpf(0))
print("  pente par decade attendue 2*b*a'^2*ln10 = %.4f (b=g/v=1, a'=1)" % float(2*log(10)))
# Test B : a ~ c th^2
WB  = lambda s,t: (s + c*t + mpf('0.4')*s**2, t**2 + mpf('0.5')*s*t + mpf('0.7')*s**2)
dWB = lambda s,t: (1 + mpf('0.8')*s, mpf('0.5')*t + mpf('1.4')*s)
run("Test B (a ~ th^2, hors colinearite)", WB, dWB, mpf(0))
# Test C : zero regulier a th=0.1
t0 = mpf('0.1')
WC  = lambda s,t: (s + c*(t-t0) + mpf('0.4')*s**2, t**2 - mpf('0.01') + mpf('0.5')*s*(t-t0) + mpf('0.7')*s**2)
dWC = lambda s,t: (1 + mpf('0.8')*s, mpf('0.5')*(t-t0) + mpf('1.4')*s)
run("Test C (a = th^2-0.01, zero regulier en 0.1)", WC, dWC, t0)
print("  pente par decade attendue 2*b*a'^2*ln10 = %.4f (a'=0.2)" % float(2*(mpf('0.04'))*log(10)))
