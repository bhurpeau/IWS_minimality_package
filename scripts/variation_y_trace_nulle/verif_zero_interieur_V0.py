"""
Test discriminant d'une ANNULATION INTERIEURE de V_0 (noeud 0 forcee) -- necessite de l'hypothese (N) de P2.

Principe.  Sous (N) le temps d'impact T_r est C^2 en theta (traces initiales) a eps fixe, avec ||D^2_theta T_r|| <= M_r eps.
Si ||V_0|| s'annule a l'interieur d'un episode, la production kappa_2 ||V_0|| de P_0 n'est plus C^2 en theta :
au voisinage de la traversee, ||V_0(t;theta)|| ~ sqrt(v^2 (t-t*)^2 + (d + eps a.delta)^2), d'ou
     d^2/ddelta^2 \int ||V_0|| dt  ~  (2 eps^2 a^2 / v) * ln( 2 L v / (d + eps a delta) )  :
   - d = 0 (zero EXACT au centre) : Q_T ~ eps^2 ln(1/(eps delta))  -> Q_T/eps = c1 + c2 eps ln(1/(eps delta)), pas de limite quand delta->0 ;
   - d > 0 : Q_T finie en delta->0, ~ eps^2 ln(1/d) (C^2 a eps fixe, mais constante degradee).
Construction du zero (RACINE, pas minimisation).  A eps = 0 le visible ne depend pas de theta ; avec u le long d'un axe
(angle 0) le mouvement de V_0 est unidimensionnel (symetrie du tanh composante par composante) et traverse 0
a l'interieur de l'episode 7 : zero exact PROTEGE PAR LA SYMETRIE.  Avec gamma_1 seul la symetrie (y -> -y) subsiste pour
tout eps (la friction est un scalaire devant V) : V_0 reste sur l'axe pour TOUT theta, la traversee est une traversee 1D
(changement de signe), pour laquelle int ||V_0|| dt reste C^2 en theta : AUCUN signal logarithmique n'est attendu.
Avec lambda (M_lambda melange les composantes) la symetrie est brisee a O(eps) : on construit la racine de la
distance signee de la courbe t -> V_0(t) a l'origine (angle du protocole, brentq ; Uamp ajuste pour que t* soit
interieur), pour le noyau couple exact au CENTRE theta_0 : zero exact NON symetrique, ou la theorie predit le signal.
Le mot est verifie en chaque point.
Controle : reference non nulle (37 deg), et reference a distance d > 0 du zero.
Integrateur : DOP853 rtol 1e-12 + evenement exact (zero_V0_lib.py), pas RK4+interpolation lineaire.  ATTENTION : au zero exact un
schema adaptatif ordinaire enjambe le coude de ||V_0|| (largeur d/v) et fabrique un FAUX signal qui diverge quand delta -> 0
(et depend de rtol) ; zero_V0_lib.refine_episode reintegre en coupant au minimum de ||V_0|| (REFINE=True, par defaut).
Temoin numerique seulement.
Usage : python3 verif_zero_interieur_V0.py [--ndir 8] [--rank 7]
"""
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import fsolve
import zero_V0_lib as Z

core = Z.core
N, d = Z.N, Z.d
WREF = Z.ref_word_periodic(6)
DELTAS = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
RANK = 7


def Tcum(theta_flat, g1, lam, ang, uamp, kmax=RANK):
    res = Z.run(theta_flat.reshape(N, d), g1, lam, Z.U_of(uamp, ang), kmax, word_ref=WREF)
    if (not res['ok']) or len(res['T']) < kmax:
        return np.full(kmax, np.nan)
    return res['T']


def construct_any(theta0, g1, lam, uamps=(2.45, 2.43, 2.41, 2.39, 2.37, 2.35, 2.33, 2.31, 2.29, 2.27, 2.25, 2.47, 2.49), amax=1.5):
    """Premier Uamp de la liste pour lequel la distance signee change de signe avec un t* strictement interieur
    (t* entre 10% et 85% de la duree) ; renvoie (uamp, ang, t*, ||V_0||min, Td) ou None."""
    for ua in uamps:
        z = Z.construct_zero_ang(theta0.reshape(N, d), g1, lam, ua, RANK, WREF, amax=amax, npts=121)
        if z is not None and 0.10 * z[3] < z[1] < 0.85 * z[3] and z[2] < 1e-6:
            return (ua,) + z
    return None


def diag(theta0, g1, lam, ang, uamp):
    g, tc, nv, Td, res = Z.signed_distance(theta0.reshape(N, d), g1, lam, uamp, ang, RANK, WREF)
    t0, sol, _ = res['sols'][RANK - 1]
    h = 1e-6
    vd = np.linalg.norm(sol.sol(min(tc + h, Td))[12:14] - sol.sol(max(tc - h, 0))[12:14]) / (2 * h) if np.isfinite(tc) else np.nan
    return g, tc, nv, vd, Td, res['ok']


def Q_table(theta0, g1, lam, ang, uamp, dirs):
    """Q_{T_r}(delta,h) = |T(th+dh) - 2T(th) + T(th-dh)|/delta^2, r = 6, 7 (indices 5, 6) ; NaN si le mot change."""
    Tc = Tcum(theta0, g1, lam, ang, uamp)
    Q = np.full((len(DELTAS), len(dirs), 2), np.nan)
    if not np.all(np.isfinite(Tc)):
        return Q
    for di, dl in enumerate(DELTAS):
        for m, h in enumerate(dirs):
            Tp = Tcum(theta0 + dl * h, g1, lam, ang, uamp)
            Tm = Tcum(theta0 - dl * h, g1, lam, ang, uamp)
            for k, r in enumerate((5, 6)):
                if np.isfinite(Tp[r]) and np.isfinite(Tm[r]):
                    Q[di, m, k] = abs(Tp[r] - 2 * Tc[r] + Tm[r]) / dl ** 2
    return Q


def report(Q, eps):
    print("     delta      Q_T6/eps    Q_T7/eps     (min..max rang 7)   n")
    for di, dl in enumerate(DELTAS):
        a = Q[di, :, 0]; b = Q[di, :, 1]
        a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
        if len(b):
            print("     %.0e    %.4e   %.4e    (%.3e .. %.3e)  %d" % (dl, np.median(a) / eps, np.median(b) / eps, b.min() / eps, b.max() / eps, len(b)))
        else:
            print("     %.0e        --          --" % dl)
    # pente par direction de Q_T7/eps en ln(delta), sur les delta ou cette direction garde le mot
    sl = []; rel = []
    x = np.log(DELTAS)
    for m in range(Q.shape[1]):
        y = Q[:, m, 1] / eps; ok = np.isfinite(y)
        if ok.sum() >= 4:
            c = np.polyfit(x[ok], y[ok], 1)
            sl.append(c[0]); rel.append(c[0] * (x[ok].max() - x[ok].min()) / max(abs(np.median(y[ok])), 1e-300))
    if sl:
        sl = np.array(sl); rel = np.array(rel)
        print("     pentes par direction d(Q_T7/eps)/d ln(delta) : " + " ".join("%+.2e" % v for v in sl))
        print("     variation relative de Q_T7/eps sur [1e-5,1e-2] (pente x amplitude en ln delta / mediane) : " + " ".join("%+.2f" % v for v in rel))
    return sl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ndir', type=int, default=6)
    ap.add_argument('--seed', type=int, default=4)
    ap.add_argument('--rtol', type=float, default=1e-12)
    ap.add_argument('--noise', action='store_true', help='etude du bruit : memes Q a rtol 1e-11,1e-12,1e-13')
    a = ap.parse_args()
    Z.RTOL = a.rtol; Z.ATOL = a.rtol * 1e-2
    t_start = time.time()
    rng = np.random.default_rng(a.seed)
    theta0 = Z.FB.tau_ref().reshape(-1)
    dirs = rng.standard_normal((a.ndir, N * d)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    print("DOP853 rtol=%.0e atol=%.0e ; mot ((0,{1,2,3}),(0,{1,4,5}))^3 ; rang teste = %d ; %d directions unitaires de R^12 (seed %d)" % (a.rtol, Z.ATOL, RANK, a.ndir, a.seed))
    cfgs = {'gamma1 seul': lambda e: (e, 0.0), 'lambda seul': lambda e: (0.0, e), 'couple (1.25 eps, 2 eps)': lambda e: (1.25 * e, 2.0 * e)}

    print("\n##### 0. CONTROLE : reference sans zero (angle 37 deg, Uamp 2.5) #####")
    for name, fn in cfgs.items():
        e = 0.05; g1, lam = fn(e)
        g, tc, nv, vd, Td, okw = diag(theta0, g1, lam, 37.0, 2.5)
        print("\n== %s, eps=%.2f : min ||V_0|| sur l'episode 7 = %.3e (au bord : t=%.3f) ; mot %s" % (name, e, nv, tc, "conserve" if okw else "CHANGE"))
        report(Q_table(theta0, g1, lam, 37.0, 2.5, dirs), e)

    print("\n##### 1. ZERO EXACT de V_0 construit au centre (racine de la distance signee en l'angle du protocole) #####")
    zeros = {}
    for name, fn in cfgs.items():
        for e in (0.02, 0.05, 0.1):
            g1, lam = fn(e)
            z = construct_any(theta0, g1, lam)
            if z is None:
                print("\n== %s, eps=%.2f : AUCUN zero interieur trouve (Uamp 2.25..2.49, |angle| <= 1.5 deg) -> non teste" % (name, e)); continue
            ua, ang, ts, nv, Td = z
            g, tc, nv2, vd, Td, okw = diag(theta0, g1, lam, ang, ua)
            zeros[(name, e)] = z
            print("\n== %s, eps=%.2f : Uamp=%.2f, angle* = %+.8e deg, t* = %.6f (duree %.4f), distance signee g = %.1e, ||V_0(t_c)|| = %.1e, ||V_0'|| = %.3f ; mot %s"
                  % (name, e, ua, ang, tc, Td, g, nv2, vd, "conserve" if okw else "CHANGE"))
            if okw:
                report(Q_table(theta0, g1, lam, ang, ua, dirs), e)

    key = ('lambda seul', 0.02)
    if key in zeros:
        ua, ang0, ts, nv, Td = zeros[key]
        e = 0.02; g1, lam = cfgs['lambda seul'](e)
        print("\n##### 2. DISTANCE d au zero (lambda seul, eps=0.02) : decalage eta de l'angle du protocole #####")
        for eta in (0.0, 1e-4, 1e-3, 1e-2, 1e-1):
            ang = ang0 + eta
            g, tc, nv, vd, Td, okw = diag(theta0, g1, lam, ang, ua)
            print("\n-- eta=%.0e deg : d = ||V_0(t_c)|| = %.3e (t_c=%.3f) ; mot %s" % (eta, nv, tc, "conserve" if okw else "CHANGE"))
            if okw:
                report(Q_table(theta0, g1, lam, ang, ua, dirs), e)

    if a.noise:
        print("\n##### 3. BRUIT : memes Q a trois tolerances (gamma1 seul eps=0.05 zero symetrique ; lambda seul eps=0.02 zero non symetrique) #####")
        for key in (('gamma1 seul', 0.05), ('lambda seul', 0.02)):
            if key not in zeros: continue
            ua, ang, ts, nv, Td = zeros[key]; g1, lam = cfgs[key[0]](key[1])
            for rt in (1e-11, 1e-12, 1e-13):
                Z.RTOL = rt; Z.ATOL = rt * 1e-2
                print("\n== %s eps=%.2f, rtol=%.0e" % (key[0], key[1], rt))
                report(Q_table(theta0, g1, lam, ang, ua, dirs[:4]), key[1])
    print("\nTotal %.0fs" % (time.time() - t_start))


if __name__ == "__main__":
    main()
