"""Criticite transverse (U3) dans le noyau IWS reel (zero_V0_lib / iws_kairos_core : N=6, d=2, forcage constant U sur le noeud 0).
Axe e=(1,0), n=(0,1).  Forcage axial U=(1,0) : la trajectoire de reference (eps=0) est portee par e et V_0^x change de signe
dans l'episode 2 (zero simple interieur).  tau(0)=theta in R^{6x2}.
 Test 1  lambda=0, gamma_1>0 : invariance de l'axe  =>  a = 0 identiquement (colinearite), pour theta aleatoire dans une boule.
 Test 2  reponse transverse au premier ordre au point de base theta=0, par noeud, pour (gamma1,lam) in {(g,0),(0,l),(g,l)}.
 Test 3  consequence pour l'instant d'impact T_2 : D^2 T_2 le long de la direction n du noeud 0, delta -> 0 : borne si a=0,
         croissance logarithmique si Da != 0, avec pente predite  K = 2 k2 exp(-k3 (T-s*)) a'^2 / (|v_s| P_t)  (T_2 = fin episode 2).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
import zero_V0_lib as Z, iws_kairos_core as core

from crit_lib import U, C0, BASE, ep2

def block(title): print("\n" + "=" * 8, title)

# ---------------------------------------------------------------- Test 1
block("Test 1 : lambda=0, gamma1=0.3 : invariance de l'axe, theta aleatoire (rayon 1 sur les 12 composantes)")
rng = np.random.default_rng(3)
worst = 0.0; nz = 0; nok = 0
for k in range(8):
    th = rng.normal(size=(6, 2)); th *= 1.0 / max(1.0, np.linalg.norm(th) / 1.0)
    res = Z.run(th, 0.3, 0.0, U, 3, word_ref=None)
    for (t0, sol, Td) in res['sols']:
        Y = sol.sol(np.linspace(0, Td, 1500))
        Vn = np.abs(Y[12:24].reshape(6, 2, -1)[:, 1, :]).max(); Hn = np.abs(Y[:12].reshape(6, 2, -1)[:, 1, :]).max()
        worst = max(worst, Vn, Hn)
    r2, sol2, Td2, zero = ep2(th, 0.3, 0.0)
    nz += zero is not None; nok += (len(res['word']) >= 1)
print(f"max |composante n de H ou V| sur episodes 1-3, 8 tirages : {worst:.3e}  (zero simple dans l'episode 2 pour {nz}/8 tirages)")

# ---------------------------------------------------------------- Test 2
block("Test 2 : reponse transverse au point de base theta=0, eps=1e-2, d=1e-2 : (a(+d)-a(-d))/(2 d eps) par noeud (direction n)")
eps = 1e-2; d = 1e-2
print("noeud : (gamma1bar,lambar)=(1,0)   (0,1)   (1,1)")
rows = []
for j in range(6):
    vals = []
    for (gb, lb) in ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0)):
        a = []
        for sg in (+1, -1):
            th = np.zeros((6, 2)); th[j, 1] = sg * d
            _, _, _, z = ep2(th, eps * gb, eps * lb); a.append(z[1] if z else np.nan)
        vals.append((a[0] - a[1]) / (2 * d * eps))
    rows.append(vals); print(f"  {j}   : {vals[0]:+.3e}  {vals[1]:+.3e}  {vals[2]:+.3e}")
# direction e (axiale) : a = 0
th = np.zeros((6, 2)); th[0, 0] = 0.3; _, _, _, z = ep2(th, eps, eps)
print(f"perturbation axiale (e) de tau_0 de 0.3, lam>0 : a = {z[1]:.3e}  (attendu 0 : sous-espace axial)")
th = np.zeros((6, 2)); th[0, 1] = 0.3; _, _, _, zp = ep2(th, eps, eps); th[0, 1] = -0.3; _, _, _, zm = ep2(th, eps, eps)
print(f"imparite sous la reflexion n -> -n : a(+0.3)={zp[1]:+.6e}, a(-0.3)={zm[1]:+.6e}")

# ---------------------------------------------------------------- Test 3

block("Test 2b : meme mesure depuis le point de base axial a traces non nulles tau_i(0)=0.6 e, eps=1e-2, d=1e-2 (direction n du noeud j)")
WORD0 = ep2(BASE.copy(), 1e-2, 1e-2)[0]["word"]
print("noeud : (gamma1bar,lambar)=(1,0)   (0,1)   (1,1)")
for j in range(6):
    vals = []
    for (gb, lb) in ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0)):
        a = []; same = True
        for sg in (+1, -1):
            th = BASE.copy(); th[j, 1] = sg * 1e-2
            r_, _, _, z = ep2(th, 1e-2 * gb, 1e-2 * lb); a.append(z[1] if z else np.nan)
            same &= (r_['word'] == WORD0)
        vals.append((a[0] - a[1]) / (2 * 1e-2 * 1e-2))
    print(f"  {j}   : {vals[0]:+.3e}  {vals[1]:+.3e}  {vals[2]:+.3e}   mot de reference conserve : {same}")

block("Test 3 : [point de base tau_i(0)=0.6 e, traces non nulles]  D^2 T_2 le long de n (noeud 0) : eps=0.1, gamma1bar=1, lam=eps*lb ; T_2 cumule (impact de fin d'episode 2)")
eps = 0.1
def T2(delta, lb):
    th = BASE.copy(); th[0, 1] += delta
    res = Z.run(th, eps * 1.0, eps * lb, U, 2, word_ref=None); return res['T'][1]
T0 = {lb: T2(0.0, lb) for lb in (0.0, 1.0)}
deltas = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]
print("delta     D2T (lam=0)     D2T (lam=eps)")
D2 = {0.0: [], 1.0: []}
for dl in deltas:
    row = []
    for lb in (0.0, 1.0):
        v = 2 * (T2(dl, lb) - T0[lb]) / dl ** 2   # T paire en delta par symetrie de reflexion
        D2[lb].append(v); row.append(v)
    print(f"{dl:7.0e}   {row[0]:+.6e}   {row[1]:+.6e}")
# pente predite
_, sol, Td, z = ep2(BASE.copy(), eps * 1.0, eps * 1.0)
res = Z.run(BASE.copy(), eps, eps, U, 2, word_ref=None)
s_star, _, vs = z
t0, sol, Td = res['sols'][1]
yT = sol.sol(Td)
Pt = core.k1c * np.linalg.norm(yT[0:2]) + core.k2c * np.linalg.norm(yT[12:14]) - core.k3c * yT[36]
th = BASE.copy(); th[0, 1] = 1e-3; _, _, _, zp = ep2(th, eps, eps); th[0, 1] = -1e-3; _, _, _, zm = ep2(th, eps, eps)
ap = (zp[1] - zm[1]) / 2e-3
K = 2 * core.k2c * np.exp(-core.k3c * (Td - s_star)) * ap ** 2 / (abs(vs) * Pt)
print(f"\nparametres de la pente predite : s*={s_star:.5f}, v_s={vs:.5f}, a'={ap:.5e}, Td={Td:.5f}, P_t(T)={Pt:.5f}")
print(f"pente predite  dD2T/d ln(1/delta) = -K = {-K:.4e}  (par decade : {-K*np.log(10):.4e})")
l1 = np.array(D2[1.0]); lg = np.log(1 / np.array(deltas))
print("pentes mesurees par decade (lam>0) entre deltas successifs :")
for i in range(len(deltas) - 1):
    print(f"   {deltas[i]:.0e} -> {deltas[i+1]:.0e} : {(l1[i+1]-l1[i])/(lg[i+1]-lg[i])*np.log(10):+.4e}")
