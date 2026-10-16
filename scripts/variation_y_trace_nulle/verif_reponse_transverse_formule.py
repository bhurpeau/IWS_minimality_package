"""Calcul independant de la reponse transverse du premier ordre A'(base).h au point de base axial tau_i(0)=C0 e (traces non nulles),
forcage axial U=(1,0), (gamma1,lambda)=eps*(0,1) : on integre le systeme LINEAIRE transverse
   H^n' = V^n ,  V^n' = -gamma0 V^n - H^n + zeta*At_k H^n + f(t),   f_i(t) = lbar * H_i^x(t) tau_i^x(t) tau_i^n(t) / (1+tau_i^x(t)^2),
   tau_i^n(t) = exp(-beta t) h_i   (ordre dominant),
le long de la trajectoire de reference AXIALE (eps=0) tiree du noyau, avec le reset V^n_{i*} <- rV V^n_{i*} au Kairos et le changement de graphe.
La reponse est X_{V_0}(s*) (composante n de V_0 au temps du zero de reference), comparee a (a(+d)-a(-d))/(2 d eps) du noyau complet.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
import zero_V0_lib as Z, iws_kairos_core as core
from crit_lib import ep2, BASE, U

N = 6
ref = Z.run(BASE.copy(), 0.0, 0.0, U, 2, word_ref=None)
(t01, sol1, Td1), (t02, sol2, Td2) = ref['sols']
_, _, _, zero = ep2(BASE.copy(), 0.0, 0.0); s_star, a0, vs = zero
A1 = core.A1_kept1.copy()
# graphe de l'episode 2 : par le saut du noyau applique a l'etat de fin d'episode 1
yT1 = sol1.sol(Td1)
y2, key, A2 = Z.apply_jump(yT1, A1)
istar = key[0]
Mats = [core.Atilde(A1), core.Atilde(A2)]

def response(hvec, lbar=1.0):
    X = np.zeros(2 * N)
    out = None
    for k, (sol, Td) in enumerate(((sol1, Td1), (sol2, Td2))):
        At = Mats[k]
        def rhs(t, X):
            Y = sol.sol(t)
            Hx = Y[0:12].reshape(N, 2)[:, 0]; tx = Y[24:36].reshape(N, 2)[:, 0]
            tg = t + (Td1 if k == 1 else 0.0)   # temps GLOBAL pour tau^n(t)=exp(-beta t) h
            f = lbar * Hx * tx * np.exp(-core.beta * tg) * hvec / (1.0 + tx ** 2)
            Hn, Vn = X[:N], X[N:]
            return np.concatenate([Vn, -core.gamma0 * Vn - Hn + core.zeta * (At @ Hn) + f])
        tend = Td if k == 0 else s_star
        s = solve_ivp(rhs, (0.0, tend), X, method='DOP853', rtol=1e-12, atol=1e-14)
        X = s.y[:, -1]
        if k == 0:
            X = X.copy(); X[N + istar] *= core.rV    # reset de V_{i*} (composante n), le reste est inchange
            # NB : le temps du saut bouge de O(eps) mais agit sur la trajectoire axiale => pas de composante n au premier ordre.
    return X[N + 0]    # V_0^n au temps du zero de reference (indice local de l'episode 2)

print(f"zero de reference (eps=0) : s*={s_star:.6f}, v_s={vs:.6f}, noeud declencheur i*={istar}")
print("noeud j : formule lineaire  |  noyau complet (Test 2b, lam=1e-2 seul, d=1e-2)")
eps = 1e-2; d = 1e-2
for j in range(N):
    h = np.zeros(N); h[j] = 1.0
    fm = response(h)
    a = []
    for sg in (+1, -1):
        th = BASE.copy(); th[j, 1] = sg * d
        _, _, _, z = ep2(th, 0.0, eps * 1.0); a.append(z[1])
    kern = (a[0] - a[1]) / (2 * d * eps)
    print(f"  {j}    : {fm:+.6e}   |   {kern:+.6e}   (ecart relatif {abs(fm-kern)/abs(kern):.2e})")
