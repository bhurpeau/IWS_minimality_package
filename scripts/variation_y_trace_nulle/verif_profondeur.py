"""
Profondeur (uniformite en le rang r des impacts) : premieres mesures sur le noyau complet, protocole du manuscrit
(Theta = 1.25, constantes du manuscrit, N = 6, d = 2, trace de reference FB.tau_ref(), forcage U sur le noeud 0).
Temoins numeriques (DOP853, rtol 1e-12), pas de certification.

Partie A  (eps = 0)  : trajectoire visible de reference jusqu'au rang KA : noeud declencheur, marge de declenchement
                       (Theta - deuxieme pression), ||V_0|| au debut / a la fin / minimum interieur de l'episode.
Partie B  (eps > 0)  : gain transverse G_r = max_s ||d_theta V_0(s)||/eps et quotient de hessienne de norme
                       Q_r = max_s |grad_theta (V_0 . n)|^2 / (eps^2 ||V_0||),  n = normale unitaire a V_0,
                       differences finies centrees en theta in R^12 (pas 1e-4), a TEMPS LOCAL s fixe dans l'episode r,
                       pour (gamma_bar, lambda_bar) = (1,0), (0,1) et eps = 1e-2, 1e-3 (test : Q_r/eps^2 independant de eps).
Partie C  (eps = 0)  : persistance du mot sous perturbation gaussienne de theta, jusqu'au rang KC.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import zero_V0_lib as Z
import iws_kairos_core as core
import finger_perturbation_ball as FB

tau0 = FB.tau_ref()
U = np.array([core.Ux, core.Uy])
KA, KC = 40, 30
KB = int(os.environ.get('IWS_KB', '14'))        # rang maximal de la partie B (14 par defaut ; 40 : long)
ONLY_B = os.environ.get('IWS_ONLY_B') == '1'      # 1 : ne lance que la partie B en (0,1), eps = 1e-3
NS, DEL = 300, 1e-4


def partie_A():
    res = Z.run(tau0, 0.0, 0.0, U, KA, word_ref=None)
    print("== Partie A : trajectoire visible (eps = 0), rang | declencheur | marge Theta-P_2e | ||V_0|| debut / fin / min interieur | ||V_decl|| fin")
    for r, (t0, sol, Td) in enumerate(res['sols']):
        yT = sol.sol(Td)
        P = np.sort(yT[36:42])[::-1]
        trig = res['word'][r][0] if r < len(res['word']) else int(np.argmax(yT[36:42]))
        tl = np.linspace(0, Td, 2000)
        nv = np.linalg.norm(sol.sol(tl)[12:14], axis=0)
        i = 2 + int(np.argmin(nv[2:-2]))
        Vtr = np.linalg.norm(yT[12:24].reshape(6, 2)[trig])
        print("%3d  node %d  marge %.4f  |V0| %.4f / %.4f / %.4f (s=%.3f)  |V_decl| %.4f" % (
            r + 1, trig, P[0] - P[1], nv[0], nv[-1], nv[i], tl[i], Vtr))


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
    G = np.zeros((KB, 12, NS, 2)); bad = 0
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
    print("-- (gamma_bar, lambda_bar) = (%g, %g), eps = %g, perturbations changeant le mot : %d" % (gb, lb, eps, bad))
    for r in range(KB):
        V = Vb[r]; nV = np.linalg.norm(V, axis=1)
        nV = np.maximum(nV, 1e-300)
        n = np.stack([-V[:, 1], V[:, 0]], 1) / nV[:, None]
        gp2 = (np.einsum('jsk,sk->js', G[r], n) ** 2).sum(0)
        gtot = np.sqrt((G[r] ** 2).sum((0, 2)))
        Q = gp2 / nV
        print("r=%2d  min||V0||=%.4f  G=max||D_th V||/eps=%.4f  Q=max|grad(V.n)|^2/(eps^2||V||)=%.4f" % (
            r + 1, nV[1:].min(), gtot.max() / eps, Q[1:].max() / eps ** 2))


def partie_C():
    base = Z.run(tau0, 0.0, 0.0, U, KC, word_ref=None)
    rng = np.random.default_rng(1)
    print("== Partie C : rang de divergence du mot (eps = 0), 12 tirages gaussiens, KC-1 = %d signifie jamais" % (KC - 1))
    for amp in (1e-4, 1e-3, 3e-3):
        w_all = []
        for k in range(12):
            rr = Z.run(tau0 + amp * rng.standard_normal((6, 2)), 0.0, 0.0, U, KC, word_ref=None)
            w = 0
            while w < KC - 1 and w < len(rr['word']) and rr['word'][w] == base['word'][w]:
                w += 1
            w_all.append(w)
        print("amplitude %g : %s" % (amp, sorted(w_all)))


if __name__ == '__main__':
    if ONLY_B:
        partie_B(0, 1, 1e-3)
    else:
        partie_A()
        print("== Partie B")
        for (gb, lb) in [(1, 0), (0, 1)]:
            for eps in (1e-2, 1e-3):
                partie_B(gb, lb, eps)
        partie_C()
