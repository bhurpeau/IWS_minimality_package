"""
Variante de run_to_kairos avec interpolation lineaire de l'etat a l'instant exact de franchissement
P_{i*} = Theta (au lieu de l'instantane du premier pas apres franchissement).  Sans cela, l'etat de Kairos
(donc b(eta), lambda(eta)) est une fonction en escalier de eta (le pas de temps est discret), d'ou
des sauts de l'ordre de dt*|d tau/dt| dans Delta(eta).  L'interpolation est affine en tau : la forme
affine en phi est conservee exactement.
"""
import numpy as np
import iws_kairos_core as core

def run_to_kairos_interp(H, V, tau, P, A, dt=2e-3, Tmax=15.0):
    G = H.shape[0]
    At = core.Atilde(A)
    ufun = core.make_u(G)
    done = np.zeros(G, dtype=bool)
    Hs, Vs, ts, Ps = H.copy(), V.copy(), tau.copy(), P.copy()
    t = 0.0
    for step in range(int(Tmax / dt)):
        Hp, Vp, tp, Pp = H, V, tau, P
        H, V, tau, P = core.rk4_batch(H, V, tau, P, At, t, dt, ufun)
        t += dt
        newly = (~done) & (P.max(axis=1) >= core.Theta)
        if newly.any():
            idx = np.flatnonzero(newly)
            ist = np.argmax(P[idx], axis=1)
            p0 = Pp[idx, ist]; p1 = P[idx, ist]
            th = np.clip((core.Theta - p0) / (p1 - p0), 0.0, 1.0)
            w2 = th[:, None]; w3 = th[:, None, None]
            Hs[idx] = Hp[idx] + w3 * (H[idx] - Hp[idx])
            Vs[idx] = Vp[idx] + w3 * (V[idx] - Vp[idx])
            ts[idx] = tp[idx] + w3 * (tau[idx] - tp[idx])
            Ps[idx] = Pp[idx] + w2 * (P[idx] - Pp[idx])
            Ps[idx, ist] = core.Theta
            done[idx] = True
        if done.all():
            break
    return Hs, Vs, ts, Ps, done

def patch(dt=2e-3):
    import finger_y_variation as F, finger_critical as C
    f = lambda H, V, tau, P, A, dt_=dt, Tmax=15.0: run_to_kairos_interp(H, V, tau, P, A, dt_, Tmax)
    f.__defaults__ = (dt, 15.0)
    core.run_to_kairos = f; F.run_to_kairos = f; C.run_to_kairos = f
    return f
