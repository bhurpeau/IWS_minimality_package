"""
Profondeur, V2 (corrections de la relecture de Benoit sur la V1) : memes protocole et memes grandeurs que
verif_profondeur.py, avec
  * m_r = minimum de ||V_0|| sur l'episode (s dans [0, Td]) par minimisation bornee autour du minimum de grille
    (rang 1 : V_0(0) = 0 par construction, non reporte) ;
  * pour chaque rang : s_minV, s_maxQ, numerateur transverse |grad(V.n)| en s_minV et en s_maxQ, Q_max, borne G^2/m,
    rapport Q_max / (G^2/m) ;
  * comparaison EXPLICITE des mots entre eps = 1e-2 et eps = 1e-3 (premier indice de divergence), a (gamma,lambda)_bar fixe ;
  * partie C poussee au rang KC = 60.
Variables d'environnement : IWS_KB (rang max de B, defaut 14), IWS_NS (points de temps local, defaut 300),
IWS_PART in {B, C, B40} (defaut : B puis C).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize_scalar
import zero_V0_lib as Z
import iws_kairos_core as core
import finger_perturbation_ball as FB

tau0 = FB.tau_ref()
U = np.array([core.Ux, core.Uy])
KB = int(os.environ.get('IWS_KB', '14'))
NS = int(os.environ.get('IWS_NS', '300'))
KC = 60
DEL = 1e-4


def min_norm_V0(sol, Td):
    tl = np.linspace(0, Td, 4001)
    nv = np.linalg.norm(sol.sol(tl)[12:14], axis=0)
    i = int(np.argmin(nv))
    if 0 < i < len(tl) - 1:
        m = minimize_scalar(lambda t: float(np.sum(sol.sol(t)[12:14] ** 2)), bounds=(tl[i - 1], tl[i + 1]),
                            method='bounded', options=dict(xatol=1e-14))
        return float(np.sqrt(m.fun)), float(m.x)
    return float(nv[i]), float(tl[i])


def sample(tau, g1, lam, smax):
    res = Z.run(tau, g1, lam, U, KB, word_ref=None)
    out = []
    for r in range(KB):
        t0, sol, Td = res['sols'][r]
        s = np.linspace(0, 1, NS) * smax[r]
        out.append(sol.sol(np.minimum(s, Td))[12:14].T)
    return res, out


def partie_B(gb, lb, eps):
    base = Z.run(tau0, eps * gb, eps * lb, U, KB, word_ref=None)
    smax = [0.98 * base['dur'][r] for r in range(KB)]
    _, Vb = sample(tau0, eps * gb, eps * lb, smax)
    wb = base['word']
    G = np.zeros((KB, 12, NS, 2)); bad = 0; ratios = []
    for j in range(12):
        sg = []
        for sgn in (+1, -1):
            t = tau0.copy().reshape(-1); t[j] += sgn * DEL
            rr, Vp = sample(t.reshape(6, 2), eps * gb, eps * lb, smax)
            if rr['word'][:KB - 1] != wb[:KB - 1] or len(rr['sols']) < KB:
                bad += 1
            sg.append(Vp)
        for r in range(KB):
            G[r, j] = (sg[0][r] - sg[1][r]) / (2 * DEL)
    print("-- (gamma_bar, lambda_bar) = (%g, %g), eps = %g, NS = %d, perturbations changeant le mot : %d" % (gb, lb, eps, NS, bad))
    print("   r |   m_r   s_minV |   G_r   | perp(s_minV) perp(s_maxQ) s_maxQ |  Q_max   G^2/m  rapport")
    for r in range(KB):
        V = Vb[r]; nV = np.maximum(np.linalg.norm(V, axis=1), 1e-300)
        n = np.stack([-V[:, 1], V[:, 0]], 1) / nV[:, None]
        perp = np.sqrt((np.einsum('jsk,sk->js', G[r], n) ** 2).sum(0)) / eps       # |grad(V.n)|/eps, par s
        gtot = np.sqrt((G[r] ** 2).sum((0, 2))) / eps
        Q = perp ** 2 / nV
        sl = slice(1, None)
        t0, sol, Td = base['sols'][r]
        if r == 0:
            m_r, s_m = float('nan'), float('nan')
        else:
            m_r, s_m = min_norm_V0(sol, Td)
        iq = 1 + int(np.argmax(Q[sl])); im = 1 + int(np.argmin(nV[sl]))
        Gmax = gtot[sl].max()
        if r == 0:      # V_0(0) = 0 par construction : m_1, G^2/m et le rapport ne sont pas definis
            print("%4d |    n/a    n/a | %.4f | %.4f %.4f %.3f | %.4f      n/a     n/a" % (
                r + 1, Gmax, perp[im], perp[iq], iq / (NS - 1) * smax[r], Q[iq]))
            continue
        ratios.append(Q[iq] / (Gmax ** 2 / m_r))
        print("%4d | %.4f %.3f | %.4f | %.4f %.4f %.3f | %.4f %.4f %.3f" % (
            r + 1, m_r, s_m, Gmax, perp[im], perp[iq], iq / (NS - 1) * smax[r], Q[iq], Gmax ** 2 / m_r, ratios[-1]))
    print("   rapport Q_max/(G^2/m) sur les rangs 2..%d : min %.3f (rang %d), max %.3f (rang %d)" % (
        KB, min(ratios), 2 + int(np.argmin(ratios)), max(ratios), 2 + int(np.argmax(ratios))))
    return base['word']


def compare_words(gb, lb):
    w1 = Z.run(tau0, 1e-2 * gb, 1e-2 * lb, U, KB, word_ref=None)['word']
    w2 = Z.run(tau0, 1e-3 * gb, 1e-3 * lb, U, KB, word_ref=None)['word']
    k = 0
    while k < min(len(w1), len(w2)) and w1[k] == w2[k]:
        k += 1
    print("mots (gamma_bar, lambda_bar) = (%g,%g) : eps=1e-2 et eps=1e-3 identiques sur les %d premieres lettres (sur %d)" % (gb, lb, k, min(len(w1), len(w2))))
    if k < min(len(w1), len(w2)):
        print("   lettre %d : eps=1e-2 -> (%d,%s) ; eps=1e-3 -> (%d,%s)" % (k + 1, w1[k][0], sorted(w1[k][1]), w2[k][0], sorted(w2[k][1])))


def partie_C():
    base = Z.run(tau0, 0.0, 0.0, U, KC, word_ref=None)
    rng = np.random.default_rng(1)
    print("== Partie C : rang de divergence du mot (eps = 0), 12 tirages gaussiens ; KC-1 = %d signifie jamais" % (KC - 1))
    for amp in (1e-4, 1e-3, 3e-3):
        w_all = []
        for k in range(12):
            rr = Z.run(tau0 + amp * rng.standard_normal((6, 2)), 0.0, 0.0, U, KC, word_ref=None)
            w = 0
            while w < KC - 1 and w < len(rr['word']) and rr['word'][w] == base['word'][w]:
                w += 1
            w_all.append(w)
        print("amplitude %g : %s" % (amp, sorted(w_all)), flush=True)


if __name__ == '__main__':
    part = os.environ.get('IWS_PART', 'BC')
    if 'B' in part and part != 'B40':
        print("== Partie B")
        for (gb, lb) in [(1, 0), (0, 1)]:
            for eps in (1e-2, 1e-3):
                partie_B(gb, lb, eps)
            compare_words(gb, lb)
    if part == 'B40':
        partie_B(0, 1, 1e-3)
    if 'C' in part:
        partie_C()
