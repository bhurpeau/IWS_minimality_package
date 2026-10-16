"""
Contre-exemple a (U3) dans le PREMIER episode (aucun Kairos avant le zero) : le mot n'intervient pas.
Protocole : noyau reel, N=6, d=2, graphe A1_kept1, forcage U=(1,0) sur le noeud 0, depart au repos, traces tau_i(0)=0.6 e
(point de base axial), seuil de pression Theta=2.2 (au lieu de 1.25) pour que le zero de V_0^x (s*~3.70) precede l'impact T_1~4.455.
Tests : 0) le zero precede le Kairos ; 1) reponse transverse par noeud (noyau vs formule lineaire, tous les noeuds valides) ;
2) additivite sur 12 directions (6 axiales : a=0 ; 6 normales) ; 3) P_0(t=4.0) et T_1 : D^2 le long de n (noeud 0).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import zero_V0_lib as Z, iws_kairos_core as core
from crit_lib import BASE, U

core.Theta = 2.2
THETA = core.Theta
A1 = core.A1_kept1.copy()
At = core.Atilde(A1)

def ep1(tau0, g1, lam):
    y0 = Z.initial_state(tau0)
    sol, Td, yT = Z.episode(y0, A1, g1, lam, U, Tmax=40.0)
    tl = np.linspace(0, Td, 6001); vx = sol.sol(tl)[12]
    idx = [i for i in range(len(tl) - 1) if vx[i] * vx[i + 1] < 0]
    if len(idx) != 1:
        return None
    i = idx[0]
    s = brentq(lambda t: sol.sol(t)[12], tl[i], tl[i + 1], xtol=1e-14)
    vs = (sol.sol(s + 1e-6)[12] - sol.sol(s - 1e-6)[12]) / 2e-6
    return dict(sol=sol, Td=Td, s=s, a=float(sol.sol(s)[13]), vs=float(vs), istar=int(np.argmax(yT[36:42])), nz=len(idx))

def tau_with(j, dn, dx=0.0):
    t = BASE.copy(); t[j, 1] += dn; t[j, 0] += dx; return t

def P0_at(tau0, g1, lam, tend, r):
    """P_0(tend) en integrant avec coupures autour du zero (point anguleux sur un bord de pas)."""
    f = Z.make_rhs(At, g1, lam, U); y0 = Z.initial_state(tau0)
    s = r['s']; W = 0.05
    cuts = [0.0, s - W, s, s + W, tend]; y = y0
    for k in range(4):
        ms = W / 300 if k in (1, 2) else np.inf
        s2 = solve_ivp(f, (cuts[k], cuts[k + 1]), y, method='DOP853', rtol=1e-12, atol=1e-14, max_step=ms)
        y = s2.y[:, -1]
    return y[36]

def lin_response(lb, gb=0.0):
    """Reponse lineaire A_j (par unite de dtheta^n_j) : systeme transverse (X_H, X_V) le long de la reference axiale (eps=0)."""
    f0 = Z.make_rhs(At, 0.0, 0.0, U); y0 = Z.initial_state(BASE)
    r0 = ep1(BASE, 0.0, 0.0); s = r0['s']
    out = np.zeros(6)
    for j in range(6):
        def aug(t, Y):
            yr = Y[:42]; X = Y[42:]
            H = yr[:12].reshape(6, 2); tau = yr[24:36].reshape(6, 2)
            XH, XV = X[:6], X[6:]
            tn = np.exp(-core.beta * t) * np.eye(6)[j]          # tau^n_i(t) = e^{-beta t} dtheta^n_i (ordre dominant)
            src = lb * tau[:, 0] * H[:, 0] * tn / (1.0 + tau[:, 0] ** 2)
            dXV = -core.gamma0 * XV - XH + core.zeta * (At @ XH) + src
            return np.concatenate([f0(t, yr), XH * 0 + XV, dXV])
        Y0 = np.concatenate([y0, np.zeros(12)])
        so = solve_ivp(aug, (0, s), Y0, method='DOP853', rtol=1e-12, atol=1e-14)
        out[j] = so.y[42 + 6, -1]                                   # X_V du noeud 0 au zero
    return out

if __name__ == "__main__":
    eps = 1e-2; d = 1e-2
    print("======== Test 0 : le zero de V_0^x precede le premier Kairos (reference eps=0, Theta=%.2f)" % THETA)
    r0 = ep1(BASE, 0.0, 0.0)
    print("s* = %.6f   T_1 = %.6f   marge T_1 - s* = %.4f   v_s = %.6f   noeud declencheur i* = %d   nb zeros dans [0,T_1] = %d"
          % (r0['s'], r0['Td'], r0['Td'] - r0['s'], r0['vs'], r0['istar'], r0['nz']))
    tl = np.linspace(0.5, r0['Td'], 4001)
    nv = np.linalg.norm(r0['sol'].sol(tl)[0:2], axis=0)
    print("min ||H_0|| sur [0.5,T_1] : %.4f (non nul ; H_0 -> 0 seulement en t=0, depart au repos)" % nv.min())

    print("\n======== Test 1 : reponse transverse par noeud, eps=%.0e, d=%.0e : (a(+d)-a(-d))/(2 d eps)" % (eps, d))
    print("noeud : (g,l)=(1,0)  (0,1)  (1,1) | formule lineaire (lbar=1) | ecart relatif (0,1)")
    L = lin_response(1.0)
    resp = np.zeros((6, 3))
    for j in range(6):
        row = []
        for c, (gb, lb) in enumerate([(1, 0), (0, 1), (1, 1)]):
            rp = ep1(tau_with(j, +d), eps * gb, eps * lb); rm = ep1(tau_with(j, -d), eps * gb, eps * lb)
            v = (rp['a'] - rm['a']) / (2 * d * eps); resp[j, c] = v; row.append(v)
        print("  %d   : %+.3e %+.3e %+.3e | %+.6e | %.2e" % (j, row[0], row[1], row[2], L[j], abs(row[1] - L[j]) / max(abs(L[j]), 1e-30)))

    print("\n======== Test 2 : additivite et directions axiales (12 directions du sous-espace cache)")
    rng = np.random.default_rng(7)
    dx = 0.3 * rng.standard_normal((6, 2)); dx[:, 1] = 0.0
    ra = ep1(BASE + dx, eps * 1, eps * 1)
    print("perturbation axiale aleatoire (6 noeuds, rayon 0.3) : a = %.3e   (attendu 0)" % ra['a'])
    h = rng.standard_normal(6) * 1e-2
    tt = BASE.copy(); tt[:, 1] += h
    rh = ep1(tt, eps * 1, eps * 1); tm = BASE.copy(); tm[:, 1] -= h; rhm = ep1(tm, eps * 1, eps * 1)
    print("direction normale h aleatoire : (a(+h)-a(-h))/(2 eps) = %+.6e   somme_j resp_j h_j = %+.6e" %
          ((rh['a'] - rhm['a']) / (2 * eps), float(resp[:, 2] @ h)))
    print("DA(p) (gamma,lambda)=(1,1), 6 composantes normales : ", np.array2string(resp[:, 2], precision=4))
    print("norme de DA(p) = %.4f  >> 0 : (N) vrai au point axial dans le premier episode" % np.linalg.norm(resp[:, 2]))

    print("\n======== Test 3 : D^2 le long de n (noeud 0), eps=0.1, gamma1bar=1, lam=eps*lb")
    eps = 0.1
    t_fix = 4.0
    rr = ep1(BASE, eps, eps)
    T0 = rr['Td']
    yT = rr['sol'].sol(T0); Hn = np.linalg.norm(yT[0:2]); Vn = np.linalg.norm(yT[12:14])
    Pdot = core.k1c * Hn + core.k2c * Vn - core.k3c * yT[36]
    ap = (ep1(tau_with(0, 1e-3), eps, eps)['a'] - ep1(tau_with(0, -1e-3), eps, eps)['a']) / 2e-3
    Kfix = 2 * core.k2c * np.exp(-core.k3c * (t_fix - rr['s'])) * ap ** 2 / abs(rr['vs'])
    KT = 2 * core.k2c * np.exp(-core.k3c * (T0 - rr['s'])) * ap ** 2 / abs(rr['vs'])
    print("(eps=0.1, lam=eps) : s*=%.5f  v_s=%.5f  a'=%.5e  T_1=%.5f  P_t(T_1)=%.5f ; t_fix=%.2f" % (rr['s'], rr['vs'], ap, T0, Pdot, t_fix))
    print("pente predite (par decade) :  D2P_0(t_fix) : +%.5e   D2T_1 : -%.5e" % (Kfix * np.log(10), KT * np.log(10) / Pdot))

    def Tclean(tau, lam):
        r_ = ep1(tau, eps, lam)
        g = lambda t: P0_at(tau, eps, lam, t, r_) - THETA
        return brentq(g, r_['Td'] - 0.1, r_['Td'] + 0.1, xtol=1e-14)     # T_1 par racine de P_0(t)=Theta sur l'integration coupee autour du zero

    deltas = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
    print("delta     D2P0(t_fix): lam=0   lam=eps  |  D2T_1 (racine) : lam=0   lam=eps  | D2T_1 (evenement solve_ivp) lam=eps")
    rows = []
    for dl in deltas:
        out = []
        for lam in (0.0, eps):
            r_c = ep1(BASE, eps, lam)
            Pp = P0_at(tau_with(0, +dl), eps, lam, t_fix, ep1(tau_with(0, +dl), eps, lam))
            Pm = P0_at(tau_with(0, -dl), eps, lam, t_fix, ep1(tau_with(0, -dl), eps, lam))
            P00 = P0_at(BASE, eps, lam, t_fix, r_c)
            d2P = (Pp + Pm - 2 * P00) / dl ** 2
            d2T = (Tclean(tau_with(0, +dl), lam) + Tclean(tau_with(0, -dl), lam) - 2 * Tclean(BASE, lam)) / dl ** 2
            Te = (ep1(tau_with(0, +dl), eps, lam)['Td'] + ep1(tau_with(0, -dl), eps, lam)['Td'] - 2 * r_c['Td']) / dl ** 2
            out += [d2P, d2T, Te]
        rows.append(out)
        print(" %.0e   %+.7e %+.7e |  %+.7e %+.7e | %+.7e" % (dl, out[0], out[3], out[1], out[4], out[5]))
    rows = np.array(rows)
    print("pentes mesurees par decade (lam=eps) :  D2P0(t_fix)  |  D2T_1 racine  |  D2T_1 evenement")
    for k in range(len(deltas) - 1):
        dec = np.log10(deltas[k] / deltas[k + 1])
        print("   %.0e -> %.0e : %+.4e  | %+.4e | %+.4e" % (deltas[k], deltas[k + 1],
              (rows[k + 1, 3] - rows[k, 3]) / dec, (rows[k + 1, 4] - rows[k, 4]) / dec, (rows[k + 1, 5] - rows[k, 5]) / dec))
    print("Lecture : D2P0 et D2T_1 (racine) ont la pente predite ; la version 'evenement' derive aux petits delta (bruit de localisation de l'evenement, de l'ordre 1e-9 sur T) ;")
    print("pour lam=0 les deux restent bornees (D2T_1 -> %.7f)." % rows[-1, 1])
