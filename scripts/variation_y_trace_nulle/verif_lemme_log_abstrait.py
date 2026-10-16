"""
Verification NUMERIQUE du lemme de singularite logarithmique sur un exemple jouet SANS aucun lien avec IWS.

Lemme (voir lemme_singularite_log.tex) : W in C^2(J x (-d0,d0); R^m), m >= 2, g in C^1, g(s0) > 0, W(s,0) != 0 pour s != s0,
W(s0,0) = 0, w = d_s W(s0,0) != 0 (v = |w|), z = d_delta W(s0,0), a = |P_{w^perp} z|.  Alors pour F(delta) = int_J g |W| ds :
     F(delta) + F(-delta) - 2 F(0) = 2 g(s0) (a^2 / v) delta^2 ln(1/|delta|) + O(delta^2).
On calcule F par quadrature adaptative (points de coupure au minimum de |W|), et on trace
     R(delta) = [F(delta)+F(-delta)-2F(0)]/delta^2 - 2 g(s0) a^2/v ln(1/delta),
qui doit rester BORNE (et converger) quand delta -> 0, alors que le terme logarithmique, lui, diverge.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

def make(m):
    v, a2, a3 = 1.3, 0.8, 0.5
    def W(s, d):
        w1 = v*s + 0.4*s**2 + 0.3*s**3 + d*(0.7 + 0.5*s) + 0.2*d**2
        w2 = a2*d + 0.6*s**2 + 0.8*s*d + 0.3*d**2 + 0.2*s**3
        w3 = a3*d + 0.9*s**2*(1+s) + 0.4*s*d - 0.2*d**2
        return np.array([w1, w2, w3][:m])
    a = np.sqrt(a2**2 + (a3**2 if m == 3 else 0.0))
    return W, v, a

def g(s): return 1.0 + 0.5*s + 0.3*s**2

def F(W, d, J=(-0.5, 0.7)):
    f = lambda s: g(s)*np.linalg.norm(W(s, d))
    # point de coupure : minimum de |W|^2 pres de 0
    m = minimize_scalar(lambda s: float(np.sum(W(s, d)**2)), bounds=(-0.05, 0.05), method='bounded', options=dict(xatol=1e-15))
    pts = sorted(set([m.x, 0.0]))
    tot = 0.0
    edges = [J[0]] + pts + [J[1]]
    for lo, hi in zip(edges[:-1], edges[1:]):
        if hi > lo:
            tot += quad(f, lo, hi, epsabs=1e-15, epsrel=1e-14, limit=500)[0]
    return tot

if __name__ == "__main__":
    for m in (2, 3):
        W, v, a = make(m)
        F0 = F(W, 0.0)
        print("\nm=%d : v=%.3f, a=%.4f, g(s0)=1, coefficient predit 2 a^2/v = %.6f" % (m, v, a, 2*a*a/v))
        print("   delta        S/delta^2       pred*ln(1/delta)    R(delta)=difference")
        prev = None
        for d in (3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4):
            S = F(W, d) + F(W, -d) - 2*F0
            Sd = S/d**2
            pl = 2*a*a/v*np.log(1/d)
            print("   %.0e    %.8f      %.8f        %.8f" % (d, Sd, pl, Sd - pl))
