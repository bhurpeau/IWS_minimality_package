"""
Decomposition du saut du rang 8 (declencheur : noeud 1, dP_1/dt = 0.2264) et comparaison aux rangs voisins, sur la branche reguliere
(lambda_bar = 1, eps = 1e-3 ; protocole de verif_profondeur.py).

Pour le rang r : w = Phi_r z_{r-1}[:, vartheta] (derivee de l'etat pre-saut a TEMPS LOCAL fixe), dT = -n^T w / (n^T f-) (derivee de l'instant
d'impact par rapport a vartheta, 12 composantes), et la derivee de l'etat post-saut a horloge locale  DR (w + f- dT) = A + B avec
   A = DR w            (part "temps fixe"),    B = DR f- dT       (part "decalage de l'instant d'impact").
Pour chaque noeud k reporte (noeud declencheur et noeud 0) : ||V_k||, ||dV_k/dt|| avant saut, norme (Frobenius, /eps) des blocs A_Vk, B_Vk et A+B,
et composante TRANSVERSE a V_k (normale unitaire n_k a V_k) de chacun : |grad_vartheta (n_k . V_k)| / eps pour A, B, A+B.
Pour le noeud declencheur : ||dT||/eps, et hypotheses de regularite elementaires (simplicite du franchissement, dP/dt, min de ||H|| et ||V|| sur l'episode).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import verif_profondeur_propagation as VP
import zero_V0_lib as Z
import iws_kairos_core as core

EPS, GB, LB, K = 1e-3, 0.0, 1.0, 10
rows = VP.chain(EPS, GB, LB, K, verbose=False)
# episode-par-episode : minima de ||H_k||, ||V_k|| sur l'episode (reference, meme eps)
res = Z.run(VP.tau0, EPS * GB, EPS * LB, VP.U, K, word_ref=None)


def blk(M, k):          # lignes V_k de M (42 x 12) -> 2 x 12
    return M[12 + 2 * k: 14 + 2 * k, :]


def transverse(M, Vk):  # |grad_vartheta (n . V_k)| pour M = d V_k / d vartheta (2 x 12)
    n = np.array([-Vk[1], Vk[0]]) / np.linalg.norm(Vk)
    return np.linalg.norm(n @ M)


print("rang | decl | dP_decl/dt | ||dT||/eps | ||grad P_decl||/eps | noeud : ||V-|| ||dV/dt-|| | A(Frob/eps) B(Frob/eps) A+B(post, Frob/eps) | transverse: A  B  A+B (post)")
for rw in rows:
    r = rw['r']; i = rw['trig']
    yT = rw['yT']; fm = rw['fm']; w = rw['w']
    DR = VP.reset_matrix(i)
    nvec = np.zeros(42); nvec[36 + i] = 1.0
    dT = -(nvec @ w) / (nvec @ fm)                    # (12,)
    A = DR @ w
    B = DR @ np.outer(fm, dT)
    for k in sorted({i, 0}):
        Vk = yT[12 + 2 * k: 14 + 2 * k]
        Vdot = fm[12 + 2 * k: 14 + 2 * k]
        # etat post-saut : V_k est multiplie par r_V si k est le declencheur ; la direction est conservee
        Vpost = (core.rV if k == i else 1.0) * Vk
        a, b = blk(A, k), blk(B, k)
        print("%3d | %d | %.4f | %.4f | %.4f | n%d : %.4f %.4f | %.4f %.4f %.4f | %.4f %.4f %.4f" % (
            r, i, (nvec @ fm), np.linalg.norm(dT) / EPS, abs(nvec @ fm) * np.linalg.norm(dT) / EPS, k, np.linalg.norm(Vk), np.linalg.norm(Vdot),
            np.linalg.norm(a) / EPS, np.linalg.norm(b) / EPS, np.linalg.norm(a + b) / EPS,
            transverse(a, Vpost) / EPS, transverse(b, Vpost) / EPS, transverse(a + b, Vpost) / EPS))

print()
print("== noeud 1 a l'episode 8 : regularite elementaire (min sur l'episode, hors s = 0)")
t0, sol, Td = res['sols'][7]
tl = np.linspace(0, Td, 3000)[1:]
Y = sol.sol(tl)
for k in (0, 1):
    nH = np.linalg.norm(Y[2 * k: 2 * k + 2], axis=0); nV = np.linalg.norm(Y[12 + 2 * k: 14 + 2 * k], axis=0)
    print("noeud %d : min||H||=%.4f  min||V||=%.4f  P(Td)=%.4f" % (k, nH.min(), nV.min(), sol.sol(Td)[36 + k]))
P1 = Y[37]; dP1 = np.gradient(P1, tl)
print("P_1(t) - Theta : min sur le dernier dixieme de l'episode = %.5f ; dP_1/dt a l'impact = %.4f ; P_1 monotone croissante sur la fin : %s" % (
    (P1 - core.Theta)[-300:].min(), dP1[-1], bool(np.all(dP1[-300:] > 0))))

print()
print("== noeud 1 : comportement au depart (noeud non force, depart au repos) et non-annulation sur les rangs 1-8")
t0, sol, Td = res['sols'][0]
for tt in (1e-3, 3e-3, 1e-2, 3e-2, 1e-1):
    y = sol.sol(tt); nV1 = np.linalg.norm(y[14:16]); nH1 = np.linalg.norm(y[2:4])
    print("t=%.0e : ||V_1||/t^3=%.4f  ||H_1||/t^4=%.4f  (pentes locales log-log : V %.2f, H %.2f)" % (
        tt, nV1 / tt ** 3, nH1 / tt ** 4,
        np.log(np.linalg.norm(sol.sol(1.1 * tt)[14:16]) / nV1) / np.log(1.1), np.log(np.linalg.norm(sol.sol(1.1 * tt)[2:4]) / nH1) / np.log(1.1)))
tl = np.linspace(0, Td, 4000)[1:]; Y = sol.sol(tl)
fac = np.minimum(tl, 1.0)
print("episode 1 : min_{t>0} ||V_1||/min(t,1)^3 = %.4f ; min ||H_1||/min(t,1)^4 = %.4f" % (
    (np.linalg.norm(Y[14:16], axis=0) / fac ** 3).min(), (np.linalg.norm(Y[2:4], axis=0) / fac ** 4).min()))
mV = []; mH = []
for r in range(1, 8):
    t0, sol, Td = res['sols'][r]; Y = sol.sol(np.linspace(0, Td, 3000))
    mV.append(np.linalg.norm(Y[14:16], axis=0).min()); mH.append(np.linalg.norm(Y[2:4], axis=0).min())
print("episodes 2-8 : min ||V_1|| par episode =", np.round(mV, 4), "; min ||H_1|| =", np.round(mH, 4))
