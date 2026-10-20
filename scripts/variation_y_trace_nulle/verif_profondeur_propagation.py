"""
Profondeur : propagation variationnelle a travers les sauts (reponse a la relecture de Benoit), sur la branche reguliere de
reference (meme protocole que verif_profondeur.py : constantes du manuscrit, Theta = 5/4, N = 6, d = 2, trace FB.tau_ref()).

Etat y = (H, V, tau, P) in R^42, plus le parametre eps (direction (gamma_bar, lambda_bar)).  Pour l'episode j :
  Phi_j   = d(flot a temps FIXE T_j)/dy (42x42) et d/d eps, par differences finies centrees (pas 1e-6) du flot DOP853 (rtol 1e-12) ;
  f-, f+  = champs avant / apres le saut ; n = e_{P_i} (garde P_i = Theta) ; DR = reset (V_i <- r_V V_i, P_i <- r_P P_i) ;
  S_loc   = DR (I - f- n^T/(n^T f-))                     : derivee de l'etat post-saut a HORLOGE LOCALE (temps depuis le saut) ;
  S_glob  = DR + (f+ - DR f-) n^T/(n^T f-)               : saltation de Benoit, derivee a TEMPS GLOBAL fixe.
Chaine : z_j = S_loc,j Phi_j z_{j-1}, z_0 = d y_0/d(vartheta, eps) (42x13).  Les quantites G_r(s) de verif_profondeur.py sont
a temps local fixe dans l'episode r : c'est donc S_loc qui les gouverne ; S_glob est rapportee pour comparaison (norme du produit).
Sorties par rang : n^T f- (= dP_i/dt a l'impact), marge de pression nu_r = Theta - P_j (j = concurrent), marges de recablage (cosinus),
||Phi_r||, ||S_loc||, ||S_glob||, produits cumules des normes, norme effective ||Pi_V z_r,vartheta||/eps (bloc 12 x 12), et
G_r^chaine (norme de Frobenius du bloc 2 x 12 de V_0 a temps local s, max sur la grille) contre G_r^direct (differences finies du
flot hybride complet, memes temps locaux).  Avec --wall : derivee nu'_eps du mur de declenchement a eps = 0 (formule de Benoit),
seuil predit eps_c = nu/|nu'|, comparaison a la difference finie hybride.
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
import zero_V0_lib as Z
import iws_kairos_core as core
import finger_perturbation_ball as FB

N, d = core.N, core.d
tau0 = FB.tau_ref()
U = np.array([core.Ux, core.Uy])
H_FD = 1e-6
NSG = 300                    # grille de temps local de verif_profondeur.py (points de 0 a 0.98 Td)
GRID_IDX = list(range(10, NSG, 10)) + [NSG - 1]


def flow(y, A, eps, gb, lb, T, teval=None):
    f = Z.make_rhs(core.Atilde(A), eps * gb, eps * lb, U)
    te = None if teval is None else np.append(teval, T)
    s = solve_ivp(f, (0.0, T), y, method='DOP853', rtol=Z.RTOL, atol=Z.ATOL, t_eval=te if te is not None else [T])
    return s.y


def flow_jac(y, A, eps, gb, lb, T, teval):
    """Renvoie Phi(T) (42x43 : colonnes y puis eps) et la liste Phi(s_k) (42x43)."""
    ns = len(teval) + 1
    out = [np.zeros((42, 43)) for _ in range(ns)]
    for k in range(42):
        yp = y.copy(); ym = y.copy(); yp[k] += H_FD; ym[k] -= H_FD
        Yp = flow(yp, A, eps, gb, lb, T, teval); Ym = flow(ym, A, eps, gb, lb, T, teval)
        for q in range(ns):
            out[q][:, k] = (Yp[:, q] - Ym[:, q]) / (2 * H_FD)
    he = 1e-6
    Yp = flow(y, A, eps + he, gb, lb, T, teval); Ym = flow(y, A, eps - he, gb, lb, T, teval)
    for q in range(ns):
        out[q][:, 42] = (Yp[:, q] - Ym[:, q]) / (2 * he)
    return out


def vecfield(y, A, eps, gb, lb):
    return Z.make_rhs(core.Atilde(A), eps * gb, eps * lb, U)(0.0, y)


def reset_matrix(i):
    DR = np.eye(42)
    for k in (12 + 2 * i, 13 + 2 * i):
        DR[k, k] = core.rV
    DR[36 + i, 36 + i] = core.rP
    return DR


def rewiring_gap(yT, A):
    """Plus petit ecart de cosinus decidant du recablage : renvoie (gap, i, a, b) avec gap = cos(tau_i,tau_a) - cos(tau_i,tau_b) > 0,
    a = element qui l'emporte, b = son concurrent immediat (retire/conserve, ajoute/non ajoute).  (inf, ...) si aucun choix."""
    P = yT[36:42]; i = int(np.argmax(P)); tau = yT[24:36].reshape(N, d)
    nb = [j for j in range(N) if A[i, j] == 1]; nn = [j for j in range(N) if j != i and A[i, j] == 0]
    m = min(2, len(nb), len(nn))
    if m == 0:
        return np.inf, i, -1, -1
    cs = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-15))
    sn = sorted([(cs(tau[i], tau[j]), j) for j in nb]); sa = sorted([(cs(tau[i], tau[j]), j) for j in nn], reverse=True)
    cands = []
    if len(sn) > m: cands.append((sn[m][0] - sn[m - 1][0], i, sn[m][1], sn[m - 1][1]))
    if len(sa) > m: cands.append((sa[m - 1][0] - sa[m][0], i, sa[m - 1][1], sa[m][1]))
    return min(cands) if cands else (np.inf, i, -1, -1)


def gap_gradient(yT, i, a, b):
    """Gradient (en tau, 12 composantes) de cos(tau_i,tau_a) - cos(tau_i,tau_b), par differences finies centrees."""
    def g(tv):
        t = tv.reshape(N, d)
        cs = lambda x, y: float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-15))
        return cs(t[i], t[a]) - cs(t[i], t[b])
    t0 = yT[24:36].copy(); gr = np.zeros(12)
    for k in range(12):
        tp = t0.copy(); tm = t0.copy(); tp[k] += 1e-7; tm[k] -= 1e-7
        gr[k] = (g(tp) - g(tm)) / 2e-7
    return gr


def chain(eps, gb, lb, K, verbose=True):
    y = Z.initial_state(tau0); A = core.A1_kept1.copy()
    z = np.zeros((42, 13)); z[24:36, :12] = np.eye(12); z[42 - 42 + 0:0, :] = 0   # d y_0/d(vartheta) ; colonne eps nulle
    rows = []
    prodS = prodSg = 1.0
    for r in range(1, K + 1):
        sol, Td, yT = Z.episode(y, A, eps * gb, eps * lb, U)
        teval = np.array([0.98 * Td * g / (NSG - 1) for g in GRID_IDX])
        Js = flow_jac(y, A, eps, gb, lb, Td, teval)
        PhiT = Js[-1]
        zaug = np.vstack([z, np.concatenate([np.zeros(12), [1.0]])])           # 43 x 13
        Phi_aug = np.vstack([PhiT, np.concatenate([np.zeros(42), [1.0]])])     # 43 x 43
        # Phi_aug @ zaug : derivee de l'etat a temps local fixe Td
        Dfix = Phi_aug @ zaug                                                  # 43 x 13
        # chaine G a temps local s_k (bloc V_0 : lignes 12, 13)
        Gc = 0.0
        for q, g in enumerate(GRID_IDX):
            Dq = np.vstack([Js[q], np.concatenate([np.zeros(42), [1.0]])]) @ zaug
            Gc = max(Gc, np.linalg.norm(Dq[12:14, :12]) / eps) if eps > 0 else np.nan
        # saut
        P = yT[36:42]; i = int(np.argmax(P)); Pj = np.sort(P)[::-1]
        y2, key, A2 = Z.apply_jump(yT, A)
        fm = vecfield(yT, A, eps, gb, lb); fp = vecfield(y2, A2, eps, gb, lb)
        nvec = np.zeros(42); nvec[36 + i] = 1.0
        ndot = float(nvec @ fm)
        DR = reset_matrix(i)
        Sloc = DR @ (np.eye(42) - np.outer(fm, nvec) / ndot)
        Sglob = DR + np.outer(fp - DR @ fm, nvec) / ndot
        rec, ri, ra, rb = rewiring_gap(yT, A)
        # derivee de l'etat pre-saut a l'impact (avant reset) et du mur : nu = Theta - P_j
        Dhit = (np.eye(43) - np.outer(np.concatenate([fm, [0.0]]), np.concatenate([nvec, [0.0]])) / ndot) @ Dfix
        j = int(np.argsort(P)[-2])
        nu = core.Theta - P[j]
        dnu_eps = -Dhit[36 + j, 12]
        drec_eps = float(gap_gradient(yT, ri, ra, rb) @ Dhit[24:36, 12]) if np.isfinite(rec) else 0.0
        rth = rec / np.linalg.norm(gap_gradient(yT, ri, ra, rb) @ Dhit[24:36, :12]) if np.isfinite(rec) else np.inf   # rayon de chambre en vartheta (1er ordre)
        ec_trig = nu / (-dnu_eps) if dnu_eps < 0 else np.inf
        ec_rec = rec / (-drec_eps) if (np.isfinite(rec) and drec_eps < 0) else np.inf
        z_new = np.vstack([Sloc @ Dfix[:42], np.zeros((0, 13))])               # 42 x 13
        nS = np.linalg.norm(Sloc, 2); nSg = np.linalg.norm(Sglob, 2); nPhi = np.linalg.norm(PhiT[:, :42], 2)
        prodS *= nS * nPhi; prodSg *= nSg * nPhi
        zV = z_new[12:24, :12]
        eff = np.linalg.norm(zV, 2) / eps if eps > 0 else np.nan     # non defini a eps = 0 (la reponse est en O(eps))
        rows.append(dict(w=Dfix[:42, :12].copy(), fm=fm.copy(), yT=yT.copy(), yplus=y2.copy(), r=r, rth=rth, ec_trig=ec_trig, ec_rec=ec_rec, drec_eps=drec_eps, Td=Td, trig=i, comp=j, ndot=ndot, nu=nu, dnu_eps=dnu_eps, rec=rec, nPhi=nPhi, nS=nS, nSg=nSg,
                         prod=prodS, prodg=prodSg, eff=eff, Gc=Gc, zeps=z_new[:, 12].copy()))
        if verbose:
            print("%2d  Td=%.4f trig=%d conc=%d  ndot=%.4f  nu=%.4f  nu'_eps=%+.4f  eps_c(decl)=%.2e  rec=%.4f rec'_eps=%+.4f eps_c(rec)=%.2e rayon_chambre_vartheta=%.2e | |Phi|=%.3f |S_loc|=%.3f |S_glob|=%.3f  prod|S_loc Phi|=%.3e prod|S_glob Phi|=%.3e | eff(V-bloc)/eps=%s  G_chaine=%s" % (
                r, Td, i, j, ndot, nu, dnu_eps, ec_trig, rec, drec_eps, ec_rec, rth, nPhi, nS, nSg, prodS, prodSg, ('%.4f' % eff if eps > 0 else 'n/a'), ('%.4f' % Gc if eps > 0 else 'n/a')), flush=True)
        y, A, z = y2, A2, z_new
    return rows


def direct_G(eps, gb, lb, K):
    """G_r direct : differences finies du flot hybride complet en vartheta (pas 1e-4) aux memes temps locaux (grille de verif_profondeur.py)."""
    base = Z.run(tau0, eps * gb, eps * lb, U, K, word_ref=None)
    smax = [0.98 * base['dur'][r] for r in range(K)]
    Gd = np.zeros(K)
    D = np.zeros((K, 12, len(GRID_IDX), 2))
    for jj in range(12):
        samples = []
        for sg in (+1, -1):
            t = tau0.copy().reshape(-1); t[jj] += sg * 1e-4
            rr = Z.run(t.reshape(N, d), eps * gb, eps * lb, U, K, word_ref=None)
            samples.append([[rr['sols'][r][1].sol(min(smax[r] * g / (NSG - 1), rr['sols'][r][2]))[12:14] for g in GRID_IDX] for r in range(K)])
        for r in range(K):
            D[r, jj] = (np.array(samples[0][r]) - np.array(samples[1][r])) / 2e-4
    for r in range(K):
        Gd[r] = np.sqrt((D[r] ** 2).sum((0, 2))).max() / eps
    return Gd


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--gb', type=float, default=0.0); ap.add_argument('--lb', type=float, default=1.0)
    ap.add_argument('--eps', type=float, default=1e-3); ap.add_argument('--K', type=int, default=14)
    ap.add_argument('--direct', action='store_true')
    a = ap.parse_args()
    print("== chaine variationnelle : (gamma_bar, lambda_bar) = (%g, %g), eps = %g, rangs 1..%d" % (a.gb, a.lb, a.eps, a.K))
    rows = chain(a.eps, a.gb, a.lb, a.K)
    if a.direct:
        Gd = direct_G(a.eps, a.gb, a.lb, a.K)
        print("== G_r : chaine vs direct")
        for rw, g in zip(rows, Gd):
            print("%2d  G_chaine=%.4f  G_direct=%.4f  rapport=%.4f" % (rw['r'], rw['Gc'], g, rw['Gc'] / g if g else np.nan))
