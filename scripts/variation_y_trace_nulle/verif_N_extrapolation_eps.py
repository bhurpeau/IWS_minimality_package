"""Controle (non rigoureux) du lien noyau <-> formule lineaire : D(eps) = (a(+d)-a(-d))/(2 d eps) pour lbar=1, gbar=0, puis
extrapolation de Richardson eps -> 0, a comparer a l'encadrement certifie X_V,0(s_*) = 0.495473971795 (certif_N_premier_episode_V4.py)."""
import numpy as np
import verif_premier_episode as V
d = 1e-3
vals = []
for eps in [1e-2, 5e-3, 2.5e-3, 1.25e-3]:
    rp = V.ep1(V.tau_with(0, +d), 0.0, eps); rm = V.ep1(V.tau_with(0, -d), 0.0, eps)
    D = (rp['a'] - rm['a']) / (2 * d * eps); vals.append(D)
    print("eps = %.2e : D(eps) = %.9f" % (eps, D))
R1 = [2 * vals[i + 1] - vals[i] for i in range(3)]
print("Richardson ordre 1 :", ["%.9f" % x for x in R1])
R2 = [(4 * R1[i + 1] - R1[i]) / 3 for i in range(2)]
print("Richardson ordre 2 :", ["%.9f" % x for x in R2])
print("encadrement certifie : 0.495473971795 +/- 2.1e-13")
