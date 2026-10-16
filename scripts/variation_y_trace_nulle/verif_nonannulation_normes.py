"""
Condition (N0) du theoreme 2 : le noeud declencheur i_r (ici toujours le noeud force 0) a ||H|| et ||V|| non nuls
sur ]0, t_k + rho] le long de la trajectoire VISIBLE de reference (a eps = 0 elle ne depend pas de theta, par
autonomie conditionnelle).  On mesure, avec un pas fin (dt=5e-4), les minima de ||H_0(s)||/min(s,1)^2 et ||V_0(s)||/min(s,1),
la distance minimale a l'origine de la courbe plane s -> V_0(s), et les comportements en s -> 0 (attendus : ||V_0||/s -> |u|=2.5,
||H_0||/s^2 -> |u|/2=1.25).  Temoin numerique : un minimum sur une grille ne certifie pas l'absence de passage exact par 0
entre deux points de grille, mais la courbe plane (H_0 ou V_0) ne passe par 0 qu'en un point de codimension 2.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import iws_kairos_core as core
import finger_perturbation as FP
import finger_perturbation_ball as FB

N, d = core.N, core.d
dt = 5e-4
FP.install(dt, 0.0, 0.0)
tau0 = FB.tau_ref()[None]
grp = core.initial_group(core.A1_kept1, tau0)
H, V, tau, P, A = grp['H'], grp['V'], grp['tau'], grp['P'], grp['A']
t = 0.0; ts = []; nH = []; nV = []; imp = []
for r in range(1, 8):
    At = core.Atilde(A); ufun = core.make_u(1)
    done = False; t_stage0 = t
    while not done:
        Hp, Vp, tp, Pp = H, V, tau, P
        H, V, tau, P = core.rk4_batch(H, V, tau, P, At, t - t_stage0, dt, ufun); t += dt
        ts.append(t); nH.append(np.linalg.norm(H[0, 0])); nV.append(np.linalg.norm(V[0, 0]))
        if P.max() >= core.Theta:
            i = int(np.argmax(P[0]))
            imp.append((r, t, i)); done = True
    if r < 7:
        H, V, tau, P, labels, _ = core.jump_batch(H, V, tau, P, A)
        A = core.build_A_from_label(A, i, labels[0])
ts = np.array(ts); nH = np.array(nH); nV = np.array(nV)
print("impacts (rang, t, noeud) :", [(r, round(tt, 4), i) for r, tt, i in imp])
for s0 in (0.002, 0.01, 0.05):
    k = np.searchsorted(ts, s0)
    print("s=%.3f : ||V_0||/s = %.4f   ||H_0||/s^2 = %.4f   (attendu 2.5 et 1.25 quand s -> 0)" % (ts[k], nV[k] / ts[k], nH[k] / ts[k] ** 2))
nHn = nH / np.minimum(ts, 1.0) ** 2; nVn = nV / np.minimum(ts, 1.0)
m = ts > 0.002
print("min_{s>0.002} ||H_0||/min(s,1)^2 = %.4f (a t=%.3f) ; min_{s>0.002} ||V_0||/min(s,1) = %.4f (a t=%.3f)" %
      (nHn[m].min(), ts[m][np.argmin(nHn[m])], nVn[m].min(), ts[m][np.argmin(nVn[m])]))
print("||V_0|| juste avant chaque impact :", [round(float(nV[np.searchsorted(ts, tt) - 1]), 4) for _, tt, _ in imp])
print("||H_0|| juste avant chaque impact :", [round(float(nH[np.searchsorted(ts, tt) - 1]), 4) for _, tt, _ in imp])
print("minimum de ||V_0|| sur chaque episode (hors s<0.01) :", [round(float(nV[(ts > a) & (ts <= b)].min()), 4) for a, b in zip([0.01] + [tt for _, tt, _ in imp[:-1]], [tt for _, tt, _ in imp])])
print("minimum de ||H_0|| sur chaque episode :", [round(float(nH[(ts > a) & (ts <= b)].min()), 4) for a, b in zip([0.01] + [tt for _, tt, _ in imp[:-1]], [tt for _, tt, _ in imp])])
