"""
Bibliotheque du test d'annulation interieure de V_0 (noeud 0, forcee) : integrateur DOP853 haute precision
(solve_ivp, rtol 1e-12) avec evenement exact P_max = Theta, au lieu du schema RK4 + interpolation lineaire de
verif_temps_impact_C2.py (dont l'erreur O(dt^2) contamine les differences secondes minuscules).
Noyau : V' = -(g0 + g1|tau_i|) V - M_lam(tau_i) H + zeta tanh(At H) + u ;  P' = k1|H|+k2|V|-k3 P.
Le saut (reecriture du graphe par similarite cosinus, P_{i*} <- rP P, V_{i*} <- rV V) reutilise core.jump_batch.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB

N, d = core.N, core.d
RTOL, ATOL = 1e-12, 1e-14
WORD_REF = ((0, frozenset({1, 2, 3})), (0, frozenset({1, 4, 5})))


def make_rhs(At, g1, lam, U):
    u = np.zeros((N, d)); u[0] = U
    def f(t, y):
        H = y[:12].reshape(N, d); V = y[12:24].reshape(N, d); tau = y[24:36].reshape(N, d); P = y[36:42]
        th = np.tanh(At @ H)
        nt = np.linalg.norm(tau, axis=1)
        Gam = core.gamma0 + g1 * nt
        c = lam / (1.0 + (1.0 + lam) * nt ** 2)
        MH = H - (c * (tau * H).sum(1))[:, None] * tau
        dV = -Gam[:, None] * V - MH + core.zeta * th + u
        dtau = core.alpha * th - core.beta * tau
        dP = core.k1c * np.linalg.norm(H, axis=1) + core.k2c * np.linalg.norm(V, axis=1) - core.k3c * P
        return np.concatenate([V.ravel(), dV.ravel(), dtau.ravel(), dP])
    return f


REFINE = True          # integration "consciente du point anguleux" de ||V_0|| (voir refine_episode)
REFINE_DMAX = 0.05     # on ne raffine que si le minimum interieur de ||V_0|| est < REFINE_DMAX


def _ev_factory():
    ev = lambda t, y: y[36:42].max() - core.Theta
    ev.terminal = True; ev.direction = 1
    return ev


def refine_episode(f, y0, sol, Td):
    """||V_0|| a un point anguleux (zero exact) ou un coude de largeur w = d/v (d = min ||V_0||, v = ||V_0'||) que
    l'integrateur adaptatif, qui ne voit le coude qu'a travers ses points intermediaires, peut enjamber sans l'echantillonner :
    erreur ~ d^2/v, soit ~1e-10 quand d ~ eps*delta (bruit constant dans les differences secondes, mis en evidence par
    la variation de rtol).  On relocalise le minimum interieur t_c de ||V_0|| (sur la sortie dense de la premiere passe),
    puis on RE-INTEGRE depuis t=0 en coupant en t_c - W, t_c, t_c + W (W = 60 w + 3e-5) avec un pas maximal W/300
    dans la fenetre : le point anguleux tombe sur un bord de pas.  Renvoie None si pas de minimum interieur petit."""
    ng = 2001
    tl = np.linspace(0, Td, ng)
    nv = np.linalg.norm(sol.sol(tl)[12:14], axis=0)
    lo, hi = int(0.005 * ng), int(0.995 * ng)
    i = lo + int(np.argmin(nv[lo:hi]))
    if i <= lo + 2 or i >= hi - 3 or nv[i] > REFINE_DMAX:
        return None
    m = minimize_scalar(lambda t: float(np.sum(sol.sol(t)[12:14] ** 2)), bounds=(tl[i - 2], tl[i + 2]), method='bounded', options=dict(xatol=1e-14))
    tc = float(m.x); h = 1e-6
    dmin = float(np.linalg.norm(sol.sol(tc)[12:14]))
    vv = float(np.linalg.norm(sol.sol(tc + h)[12:14] - sol.sol(tc - h)[12:14]) / (2 * h))
    W = min(60.0 * dmin / max(vv, 1e-3) + 3e-5, 0.05)
    cuts = [0.0, tc - W, tc, tc + W, Td + 0.05]
    ev = _ev_factory()
    y = y0.copy(); t = 0.0
    for k in range(4):
        a, b = cuts[k], cuts[k + 1]
        ms = W / 300.0 if k in (1, 2) else np.inf
        s2 = solve_ivp(f, (a, b), y, method='DOP853', rtol=RTOL, atol=ATOL, events=ev, max_step=ms)
        if s2.t_events[0].size:
            return float(s2.t_events[0][0]), s2.y_events[0][0], tc, dmin
        y = s2.y[:, -1]
    return None


def episode(y0, A, g1, lam, U, Tmax=15.0, dense=True):
    At = core.Atilde(A)
    f = make_rhs(At, g1, lam, U)
    ev = _ev_factory()
    sol = solve_ivp(f, (0.0, Tmax), y0, method='DOP853', rtol=RTOL, atol=ATOL, events=ev, dense_output=True)
    if sol.t_events[0].size == 0:
        return None
    Td = float(sol.t_events[0][0]); yT = sol.y_events[0][0]
    if REFINE:
        r = refine_episode(f, y0, sol, Td)
        if r is not None:
            Td, yT = r[0], r[1]
    return sol, Td, yT


def initial_state(tau0):
    y = np.zeros(42)
    y[24:36] = tau0.reshape(-1)
    y[36] = core.rP * core.Theta
    return y


def apply_jump(yT, A):
    H = yT[:12].reshape(1, N, d); V = yT[12:24].reshape(1, N, d); tau = yT[24:36].reshape(1, N, d); P = yT[36:42].reshape(1, N)
    H2, V2, tau2, P2, labels, i2 = core.jump_batch(H, V, tau, P, A)
    ist = int(i2[0]); lab = frozenset(labels[0])
    y2 = np.concatenate([H2.ravel(), V2.ravel(), tau2.ravel(), P2.ravel()])
    return y2, (ist, lab), core.build_A_from_label(A, ist, set(lab))


def run(tau0, g1, lam, U, kmax, word_ref=WORD_REF, keep_dense=False):
    """kmax impacts (le kmax-ieme saut n'est pas applique).  Renvoie dict(T=cumul (kmax,), dur, ok, word, eps_sol) ;
    ok=False des que le mot differe de word_ref (ou pas de Kairos).  word_ref=None : mot libre."""
    y = initial_state(tau0); A = core.A1_kept1.copy()
    cum = 0.0; T = []; dur = []; word = []; sols = []; ok = True
    for r in range(kmax):
        out = episode(y, A, g1, lam, U)
        if out is None:
            ok = False; break
        sol, Td, yT = out
        cum += Td; T.append(cum); dur.append(Td); sols.append((cum - Td, sol, Td))
        if r == kmax - 1:
            break
        y, key, A = apply_jump(yT, A)
        word.append(key)
        if word_ref is not None and r < len(word_ref) and key != word_ref[r]:
            ok = False
    # mot de reference periodique ((0,{1,2,3}),(0,{1,4,5}))^3
    return dict(T=np.array(T), dur=np.array(dur), ok=ok, word=word, sols=sols)


def ref_word_periodic(n):
    return tuple(WORD_REF[r % 2] for r in range(n))


def V0_series(res, r, n=4000):
    """(t_loc, ||V_0||, V_0) sur l'episode r (0-indexe)."""
    t0, sol, Td = res['sols'][r]
    tl = np.linspace(0, Td, n)
    Y = sol.sol(tl)
    V0 = Y[12:14].T
    return tl, np.linalg.norm(V0, axis=1), V0


# ---------------------------------------------------------------------------------------------
#  Construction d'un zero exact de V_0 (racine, pas minimisation) :  V_0(t_loc; Uamp) = 0  dans R^2
# ---------------------------------------------------------------------------------------------
from scipy.optimize import fsolve


def U_of(Uamp, ang_deg):
    a = np.radians(ang_deg)
    return Uamp * np.array([np.cos(a), np.sin(a)])


def V0_at(tau0, g1, lam, Uamp, ang_deg, rank, t_loc, kmax=None):
    """V_0 a l'instant local t_loc de l'episode `rank` (1-indexe), trajectoire de reference de mot libre."""
    kmax = kmax or rank
    res = run(tau0, g1, lam, U_of(Uamp, ang_deg), kmax, word_ref=None)
    if len(res['sols']) < rank:
        return np.array([np.nan, np.nan]), res
    t0, sol, Td = res['sols'][rank - 1]
    t_loc = min(max(t_loc, 0.0), Td)
    return sol.sol(t_loc)[12:14], res


def find_zero(tau0, g1, lam, ang_deg, rank, Uamp0, t0, kmax=None):
    """Resout V_0(t_loc, Uamp) = 0 (2 equations, 2 inconnues t_loc, Uamp) par fsolve.  Renvoie (Uamp, t_loc, residu)."""
    def F(x):
        v, _ = V0_at(tau0, g1, lam, x[1], ang_deg, rank, x[0], kmax)
        return v
    sol, info, ier, msg = fsolve(F, [t0, Uamp0], full_output=True, xtol=1e-14)
    return sol[1], sol[0], np.linalg.norm(F(sol)), ier


# ---------------------------------------------------------------------------------------------
#  Construction robuste : DISTANCE SIGNEE de la courbe t -> V_0(t) a l'origine, racine en l'angle (brentq)
# ---------------------------------------------------------------------------------------------
from scipy.optimize import brentq, minimize_scalar


def signed_distance(tau0, g1, lam, Uamp, ang_deg, rank, word_ref=None, ngrid=4001):
    """Renvoie (g, t_c, ||V_0(t_c)||, Td, res) : t_c = abscisse du minimum INTERIEUR de ||V_0|| sur l'episode `rank`,
    g = V_0(t_c) x V_0'(t_c)/||V_0'(t_c)||  (distance signee a la droite tangente ; change de signe quand la courbe
    traverse l'origine).  g = nan si pas de minimum interieur (minimum au bord de l'episode)."""
    res = run(tau0, g1, lam, U_of(Uamp, ang_deg), rank, word_ref=word_ref)
    if len(res['sols']) < rank:
        return np.nan, np.nan, np.nan, np.nan, res
    t0, sol, Td = res['sols'][rank - 1]
    tl = np.linspace(0, Td, ngrid)
    nv = np.linalg.norm(sol.sol(tl)[12:14], axis=0)
    lo = int(0.01 * ngrid); hi = int(0.99 * ngrid)
    i = lo + int(np.argmin(nv[lo:hi]))
    if i <= lo + 1 or i >= hi - 2:
        return np.nan, tl[i], nv[i], Td, res
    fun = lambda t: float(np.sum(sol.sol(t)[12:14] ** 2))
    m = minimize_scalar(fun, bounds=(tl[i - 2], tl[i + 2]), method='bounded', options=dict(xatol=1e-14))
    tc = m.x
    h = 1e-6
    v = sol.sol(tc)[12:14]
    vd = (sol.sol(tc + h)[12:14] - sol.sol(tc - h)[12:14]) / (2 * h)
    g = (v[0] * vd[1] - v[1] * vd[0]) / np.linalg.norm(vd)
    return g, tc, float(np.linalg.norm(v)), Td, res


def construct_zero_ang(tau0, g1, lam, Uamp, rank=7, word_ref=None, amax=0.5, npts=81):
    """Cherche l'angle ang* tel que la courbe V_0(t) de l'episode `rank` passe EXACTEMENT par 0 : scan de g(ang) sur
    [-amax, amax] degres, premier changement de signe, brentq (xtol 1e-16).  Renvoie (ang, t*, ||V_0(t*)||, Td) ou None."""
    angs = np.linspace(-amax, amax, npts)
    gs = np.array([signed_distance(tau0, g1, lam, Uamp, a, rank, word_ref)[0] for a in angs])
    for k in range(len(angs)):
        if np.isfinite(gs[k]) and abs(gs[k]) < 1e-11:      # zero deja sur la grille (cas protege par symetrie : ang = 0)
            g, tc, nv, Td, _ = signed_distance(tau0, g1, lam, Uamp, angs[k], rank, word_ref)
            return angs[k], tc, nv, Td
    for k in range(len(angs) - 1):
        if np.isfinite(gs[k]) and np.isfinite(gs[k + 1]) and gs[k] * gs[k + 1] < 0:
            f = lambda a: signed_distance(tau0, g1, lam, Uamp, a, rank, word_ref)[0]
            a_star = brentq(f, angs[k], angs[k + 1], xtol=1e-16, rtol=1e-15, maxiter=200)
            g, tc, nv, Td, _ = signed_distance(tau0, g1, lam, Uamp, a_star, rank, word_ref)
            return a_star, tc, nv, Td
    return None
