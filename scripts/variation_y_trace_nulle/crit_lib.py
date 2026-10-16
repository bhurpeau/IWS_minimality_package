"""Outils communs aux scripts de criticite transverse (noyau IWS reel, axe e=(1,0), n=(0,1))."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
import zero_V0_lib as Z, iws_kairos_core as core

U = np.array([1.0, 0.0])
C0 = 0.6                      # traces de base axiales NON nulles : tau_i(0) = C0*e pour tout noeud
BASE = np.zeros((6, 2)); BASE[:, 0] = C0

def ep2(tau0, g1, lam):
    """Episode 2 : (res, sol, Td, zero) avec zero=(s*, a, v_s) : a = composante n de V_0 au zero de sa composante e."""
    res = Z.run(tau0, g1, lam, U, 2, word_ref=None)
    t0, sol, Td = res['sols'][1]
    tl = np.linspace(0, Td, 4001); vx = sol.sol(tl)[12]
    idx = [i for i in range(len(tl) - 1) if vx[i] * vx[i + 1] < 0]
    zero = None
    if idx:
        i = idx[0]; s = brentq(lambda t: sol.sol(t)[12], tl[i], tl[i + 1], xtol=1e-14)
        vs = (sol.sol(s + 1e-6)[12] - sol.sol(s - 1e-6)[12]) / 2e-6
        zero = (s, float(sol.sol(s)[13]), float(vs))
    return res, sol, Td, zero

def cos_gaps(tau0=None):
    """Similarites cosinus entre tau_{i*} et les noeuds, a l'instant du premier Kairos (trajectoire de reference eps=0) :
    le mot est regulier si les ecarts entre 'retires/ajoutes' et 'gardes' sont stricts."""
    tau0 = BASE.copy() if tau0 is None else tau0
    res = Z.run(tau0, 0.0, 0.0, U, 2, word_ref=None)
    t0, sol, Td = res['sols'][0]
    tau = sol.sol(Td)[24:36].reshape(6, 2)
    return tau, res['word']
