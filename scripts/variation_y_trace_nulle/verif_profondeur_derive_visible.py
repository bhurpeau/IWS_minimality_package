"""
Derive lineaire en eps de la vitesse VISIBLE ||V_0|| (a ETAT de l'episode fixe par le temps local s = 0.48 Td_ref, pas par un
extremum) : explique l'ecart de Q_r/eps^2 entre eps = 1e-2 et 1e-3 pour lambda_bar = 1 (voir la note V2).
Pente_eps(r) = (||V_0||_eps - ||V_0||_0)/eps pour eps = 1e-3 et 1e-2, rangs 2..K.  Meme protocole que verif_profondeur.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import zero_V0_lib as Z, iws_kairos_core as core, finger_perturbation_ball as FB
tau0 = FB.tau_ref(); U = np.array([core.Ux, core.Uy]); K = 40
for (gb, lb) in [(0, 1), (1, 0)]:
    runs = {e: Z.run(tau0, e * gb, e * lb, U, K, word_ref=None) for e in (0.0, 1e-3, 1e-2)}
    print("== (gamma_bar, lambda_bar) = (%g, %g) : ||V_0|| a s = 0.48*Td_ref(eps=0) ; mot identique a eps = 0 sur les premieres lettres : eps=1e-3 : %d, eps=1e-2 : %d" % (
        gb, lb, *[next((k for k in range(K - 1) if runs[e]['word'][k] != runs[0.0]['word'][k]), K - 1) for e in (1e-3, 1e-2)]))
    for r in range(1, K):
        s = 0.48 * runs[0.0]['dur'][r]
        v = [np.linalg.norm(runs[e]['sols'][r][1].sol(min(s, runs[e]['sols'][r][2]))[12:14]) for e in (0.0, 1e-3, 1e-2)]
        print("r=%2d  V(0)=%.5f  V(1e-3)=%.5f  V(1e-2)=%.5f  pente(1e-3)=%+.3f  pente(1e-2)=%+.3f" % (
            r + 1, v[0], v[1], v[2], (v[1] - v[0]) / 1e-3, (v[2] - v[0]) / 1e-2))
