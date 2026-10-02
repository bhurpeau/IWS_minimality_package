import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
"""
Due diligence sur les 3 cas "NON SEPARE jusqu'a K=7" obtenus avec U5
(mono-axe, noeud 0, direction fixee a 0 deg, amplitude variable) :
- Pour la paire A, le mecanisme est THEORIQUEMENT explique (symetrie miroir
  exacte sous toute amplitude quand la direction de forcage est Uy=0 :
  H,V restent nuls sur tous les axes y, donc negater tous les angles caches
  laisse la dynamique (H,V,P) invariante -> AUCUNE amplitude ne peut separer).
  On verifie ici que meme un balayage dense ne separe pas, et qu'on comprend
  pourquoi ce n'est pas qu'un echantillonnage trop grossier.
- Pour les paires B et C (PAS des paires miroir), le NON-SEPARE pourrait etre
  soit (i) un vrai phenomene mecanique (mais lequel ?), soit (ii) un artefact
  de richesse insuffisante de la famille U5 telle que testee (7 amplitudes,
  K<=7). On teste deux extensions independantes :
    1) meme famille U5 (7 amplitudes), K pousse jusqu'a 12
    2) balayage BEAUCOUP plus dense d'amplitudes (40 valeurs, 0.1 a 8.0), K=7
"""
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_separating_families import run_pair_family, summarize
from iws_kairos_core_gen import d

mag = 0.3
N6, N9 = 6, 9

# --- reconstruire les 3 paires exactement comme dans nerode_matrix_full.py ---
with open(_lp('nerode_pairs.pkl'), 'rb') as f:
    saved = pickle.load(f)
A1_6 = saved['A1_6']
phisA, phisAp = saved['phisA'], saved['phisAp']

def tau6_from_phis(phis_deg5, N=N6):
    tau = np.zeros((N, d))
    tau[0] = mag*np.array([1.0, 0.0])
    for k, phi in enumerate(phis_deg5):
        tau[k+1] = mag*np.array([np.cos(np.radians(phi)), np.sin(np.radians(phi))])
    return tau

tau_A, tau_Ap = tau6_from_phis(phisA), tau6_from_phis(phisAp)

phi1_fixed_B, phi2_fixed_B, phi3_fixed_B_rad = np.radians(10.0), np.radians(40.0), 2.0
def tau6_B(phi4_deg, phi5_deg):
    tau = np.zeros((N6, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed_B), np.sin(phi1_fixed_B)])
    tau[2] = mag*np.array([np.cos(phi2_fixed_B), np.sin(phi2_fixed_B)])
    tau[3] = mag*np.array([np.cos(phi3_fixed_B_rad), np.sin(phi3_fixed_B_rad)])
    tau[4] = mag*np.array([np.cos(np.radians(phi4_deg)), np.sin(np.radians(phi4_deg))])
    tau[5] = mag*np.array([np.cos(np.radians(phi5_deg)), np.sin(np.radians(phi5_deg))])
    return tau
tau_B, tau_Bp = tau6_B(-5.0, 0.08474576271186418), tau6_B(-5.0, 0.5932203389830502)

edges9 = [(0,1),(0,2),(0,3),(4,5)]
A1_9 = np.zeros((N9,N9))
for i,j in edges9: A1_9[i,j]=A1_9[j,i]=1
phi1_fixed9, phi3_fixed9 = np.radians(15.0), np.radians(45.0)
phi4_fixed9, phi5_fixed9 = np.radians(5.0), np.radians(355.0)
phi7_fixed9, phi8_fixed9 = np.radians(200.0), np.radians(160.0)
def tau9(phi2_deg, phi6_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed9), np.sin(phi1_fixed9)])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_deg)), np.sin(np.radians(phi2_deg))])
    tau[3] = mag*np.array([np.cos(phi3_fixed9), np.sin(phi3_fixed9)])
    tau[4] = mag*np.array([np.cos(phi4_fixed9), np.sin(phi4_fixed9)])
    tau[5] = mag*np.array([np.cos(phi5_fixed9), np.sin(phi5_fixed9)])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_deg)), np.sin(np.radians(phi6_deg))])
    tau[7] = mag*np.array([np.cos(phi7_fixed9), np.sin(phi7_fixed9)])
    tau[8] = mag*np.array([np.cos(phi8_fixed9), np.sin(phi8_fixed9)])
    return tau
tau_C  = tau9(341.64406779661016, 358.52542372881356)
tau_Cp = tau9(341.64406779661016, 359.03389830508473)

cases = [
    ('Pair A (N=6, miroir)', A1_6, N6, tau_A, tau_Ap),
    ('Pair B (N=6, coin (0,0))', A1_6, N6, tau_B, tau_Bp),
    ('Pair C (N=9, {2,4,6})', A1_9, N9, tau_C, tau_Cp),
]

print("="*78)
print("TEST 1 : meme U5 (7 amplitudes : 1.0..4.0), K pousse jusqu'a 12")
print("="*78)
U5_std = [(0, U, 0.0) for U in [1.0,1.5,2.0,2.5,3.0,3.5,4.0]]
for name, A1, N, tx, txp in cases:
    t0=time.time()
    fd, px, pxp = run_pair_family(A1, N, tx, txp, U5_std, K=12)
    summarize(name + " [K<=12]", fd, U5_std, K=12)
    print("    (%.1fs)" % (time.time()-t0))

print()
print("="*78)
print("TEST 2 : U5 dense (40 amplitudes, 0.1 a 8.0), K=7")
print("="*78)
U5_dense = [(0, U, 0.0) for U in np.linspace(0.1, 8.0, 40)]
for name, A1, N, tx, txp in cases:
    t0=time.time()
    fd, px, pxp = run_pair_family(A1, N, tx, txp, U5_dense, K=7)
    summarize(name + " [dense]", fd, U5_dense)
    print("    (%.1fs)" % (time.time()-t0))

print()
print("="*78)
print("TEST 3 : U5 generalise -- direction PAS fixee a 0, noeud 0, K=7")
print("  (pour verifier que A echoue ENCORE -- prediction theorique --")
print("   et voir si B/C se separent dès qu'on autorise une direction != 0)")
print("="*78)
U5_anydir = [(0, amp*np.cos(np.radians(ang)), amp*np.sin(np.radians(ang)))
             for amp in [1.0, 2.5, 4.0] for ang in [0,10,20,30,45,60,90]]
for name, A1, N, tx, txp in cases:
    t0=time.time()
    fd, px, pxp = run_pair_family(A1, N, tx, txp, U5_anydir, K=7)
    summarize(name + " [dir!=0 autorisee]", fd, U5_anydir)
    print("    (%.1fs)" % (time.time()-t0))
