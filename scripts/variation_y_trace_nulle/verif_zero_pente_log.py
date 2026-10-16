"""
Test QUANTITATIF du mecanisme logarithmique a un zero exact de V_0 (suite de verif_zero_interieur_V0.py).

Au voisinage de la traversee, a delta petit : ||V_0(t;theta0+delta h)|| = sqrt(v^2 (t-t*)^2 + (a_h delta)^2) + (termes lisses),
ou v = ||V_0'(t*)|| et a_h = d(distance signee)/d delta dans la direction h (derivee de g(theta) = V_0 x V_0'/||V_0'|| en t_c).
Alors  d^2/d delta^2 int ||V_0|| dt = (2 a_h^2 / v) ln(C/delta) + lisse, et, comme P_0(T) = e^{-k3 T}(P_0(0) + int e^{k3 s} f ds),
   T'' (second difference signee / delta^2) = + B (2 a_h^2 / v) ln(delta) + lisse,   B = k2 e^{-k3 (T - t*)} / Pdot_0(T),
d'ou la prediction SANS PARAMETRE LIBRE :
   pente de (T(th+dh) - 2T(th) + T(th-dh))/delta^2 en ln(delta)  =  2 B a_h^2 / v .
On la compare a la pente mesuree (ajustement lineaire sur delta in [1e-4, 5e-3], differences secondes SIGNEES).
Cas symetrique (gamma_1 seul) : a_h = 0 pour toutes les directions (y reste nul) et pente mesuree ~ 0.
Temoin numerique seulement.
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import zero_V0_lib as Z
import verif_zero_interieur_V0 as W

core = Z.core
N, d = Z.N, Z.d
DEL = np.array([1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3])   # delta >= 1e-4 : en dessous, la difference seconde de T (~1e-13) est au niveau de l'erreur d'integration/arrondi


def distance_section(theta0, dirs, cfgs):
    """Pente en ln(delta) de la difference seconde SIGNEE de T_7 quand la reference est a distance d du zero
    (decalage eta de l'angle du protocole) : la loi 2 B a^2/v n'est valable que si a*delta >> d ; quand d >> a*delta
    la fonction est C^2 (pente -> 0)."""
    e = 0.02; g1, lam = cfgs['lambda seul'](e)
    z = W.construct_any(theta0, g1, lam)
    ua, ang0, ts, nv, Td0 = z
    print("\n##### distance d au zero (lambda seul, eps=%.2f, Uamp=%.2f) : pente en ln(delta) sur delta in [1e-4, 5e-3] #####" % (e, ua))
    for eta in (0.0, 1e-4, 1e-3, 1e-2, 1e-1):
        ang = ang0 + eta
        g, tc, nvv, vd, Td, okw = W.diag(theta0, g1, lam, ang, ua)
        Tc = W.Tcum(theta0, g1, lam, ang, ua)[6]
        out = []
        for h in dirs:
            S = []
            for dl in DEL:
                Tp = W.Tcum(theta0 + dl * h, g1, lam, ang, ua)[6]; Tm = W.Tcum(theta0 - dl * h, g1, lam, ang, ua)[6]
                S.append((Tp - 2 * Tc + Tm) / dl ** 2)
            S = np.array(S)
            out.append(np.polyfit(np.log(DEL), S, 1)[0] if np.all(np.isfinite(S)) else np.nan)
        print("  eta=%.0e deg : d = %.2e : pentes (4 directions) = %s" % (eta, nvv, " ".join("%+.3e" % o for o in out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ndir', type=int, default=12)
    ap.add_argument('--seed', type=int, default=11)
    ap.add_argument('--dist', action='store_true', help="seulement la section distance d au zero (lambda seul, eps=0.02)")
    a = ap.parse_args()
    Z.RTOL = 1e-12; Z.ATOL = 1e-14
    theta0 = Z.FB.tau_ref().reshape(-1)
    rng = np.random.default_rng(a.seed)
    dirs = rng.standard_normal((a.ndir, N * d)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    cfgs = {'gamma1 seul': lambda e: (e, 0.0), 'lambda seul': lambda e: (0.0, e)}
    if a.dist:
        distance_section(theta0, dirs[:4], cfgs)
        return
    for (name, e) in (('lambda seul', 0.02), ('lambda seul', 0.05), ('gamma1 seul', 0.05)):
        g1, lam = cfgs[name](e)
        z = W.construct_any(theta0, g1, lam)
        if z is None:
            print("%s eps=%.2f : pas de zero" % (name, e)); continue
        ua, ang, ts, nv, Td = z
        # grandeurs au zero central
        res = Z.run(theta0.reshape(N, d), g1, lam, Z.U_of(ua, ang), W.RANK, word_ref=W.WREF)
        t0, sol, Td = res['sols'][W.RANK - 1]
        h_ = 1e-6
        vvec = (sol.sol(ts + h_)[12:14] - sol.sol(ts - h_)[12:14]) / (2 * h_); v = np.linalg.norm(vvec)
        yT = sol.sol(Td)
        Hn = np.linalg.norm(yT[0:12].reshape(N, d)[0]); Vn = np.linalg.norm(yT[12:24].reshape(N, d)[0])
        Pdot = core.k1c * Hn + core.k2c * Vn - core.k3c * core.Theta
        B = core.k2c * np.exp(-core.k3c * (Td - ts)) / Pdot
        print("\n== %s eps=%.2f : Uamp=%.2f, angle*=%+.6e deg, t*=%.5f, T(rang7)-t*=%.4f, v=%.4f, Pdot(T)=%.4f, B=%.4f" % (name, e, ua, ang, ts, Td - ts, v, Pdot, B))
        print("   direction   a_h=dg/ddelta     pente mesuree        pente predite 2B a^2/v     rapport")
        rat = []
        Tc = W.Tcum(theta0, g1, lam, ang, ua)[6]
        for m, h in enumerate(dirs):
            fd = 1e-4
            gp = Z.signed_distance(theta0.reshape(N, d) + fd * h.reshape(N, d), g1, lam, ua, ang, W.RANK, W.WREF)[0]
            gm = Z.signed_distance(theta0.reshape(N, d) - fd * h.reshape(N, d), g1, lam, ua, ang, W.RANK, W.WREF)[0]
            ah = (gp - gm) / (2 * fd)
            S = []
            for dl in DEL:
                Tp = W.Tcum(theta0 + dl * h, g1, lam, ang, ua)[6]; Tm = W.Tcum(theta0 - dl * h, g1, lam, ang, ua)[6]
                S.append((Tp - 2 * Tc + Tm) / dl ** 2)
            S = np.array(S)
            if not np.all(np.isfinite(S)):
                print("   %2d   mot change" % m); continue
            sl = np.polyfit(np.log(DEL), S, 1)[0]
            pred = 2 * B * ah ** 2 / v
            r = sl / pred if pred > 1e-12 else np.nan
            rat.append(r)
            print("   %2d      %+.4e     %+.4e        %+.4e            %s" % (m, ah, sl, pred, ("%.3f" % r) if np.isfinite(r) else "--"))
        rat = np.array([r for r in rat if np.isfinite(r)])
        if len(rat):
            print("   rapport mesure/predit (directions avec a_h non negligeable) : mediane %.3f, min %.3f, max %.3f (n=%d)" % (np.median(rat), rat.min(), rat.max(), len(rat)))
    print("done")


if __name__ == "__main__":
    main()
