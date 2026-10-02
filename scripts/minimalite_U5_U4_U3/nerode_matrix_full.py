import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_separating_families import run_pair_family, summarize, K_MAX
from iws_kairos_core_gen import automorphisms, build_A_from_label, d

mag = 0.3

# ---------------------------------------------------------------- familles
#
# Correction (Benoit) : les echantillons finis U5_hat/U4_hat/U3_hat doivent
# etre eux-memes embo
# ites (U5_hat subset U4_hat subset U3_hat), pas seulement les familles
# mathematiques U5 subset U4 subset U3 dont ils proviennent -- sinon
# k_min(U3_hat) < k_min(U4_hat) est possible par simple trou d'echantillonnage
# (c'etait exactement le cas : U3_hat utilisait une grille {amp=2.5, 3 angles}
# disjointe de la grille {amp in {1.5,2.5,3.5}, 11 angles} de U4_hat, au lieu
# de la contenir). Fixe ici par construction : U4_hat(noeud) est definie une
# fois sur une grille (AMPS x ANGS), U5_hat(noeud) est EXACTEMENT sa tranche
# angle=0 (donc U5_hat subset U4_hat au sens ensembliste strict, pas seulement
# en valeur), et U3_hat(noeuds) est l'UNION des U4_hat(noeud) pour noeud dans
# la liste (donc U4_hat(0) subset U3_hat des lors que 0 est dans la liste).
# Avec cette construction, k_min(U3_hat) <= k_min(U4_hat) <= k_min(U5_hat) est
# garanti par construction (plus de famille = plus de chances de separer tot) ;
# toute violation observee serait alors un vrai bug, plus une question
# d'echantillonnage.

AMPS = [1.5, 2.5, 3.5]
ANGS = [0, 15, 37, 60, 90, 120, 160, 200, 250, 290, 330]

def family_U4(node=0):
    # U4_hat : force 2D constante, un seul noeud force -- grille de reference
    return [(node, amp*np.cos(np.radians(ang)), amp*np.sin(np.radians(ang)))
            for amp in AMPS for ang in ANGS]

def family_U5(node=0):
    # U5_hat : tranche angle=0 EXACTE de U4_hat(node) -> sous-ensemble strict
    return [(node, amp*np.cos(np.radians(0)), amp*np.sin(np.radians(0))) for amp in AMPS]

def family_U3(nodes):
    # U3_hat : union des U4_hat(node) pour node dans la liste -> U4_hat(0) y
    # est inclus tel quel des lors que 0 figure dans "nodes"
    out = []
    for node in nodes:
        out.extend(family_U4(node))
    return out

results = {}

def kmin(first_divergence):
    vals = [v for v in first_divergence if v is not None]
    return min(vals) if vals else None

def check_nesting_and_monotonicity(pname, fam_order, families, results):
    # 1) verifie l'emboitement ENSEMBLISTE des echantillons (pas seulement
    #    des familles mathematiques dont ils proviennent)
    for j in range(len(fam_order)-1):
        small, big = families[fam_order[j]], families[fam_order[j+1]]
        set_small, set_big = set(small), set(big)
        if not set_small.issubset(set_big):
            missing = set_small - set_big
            print("  !! ALERTE emboitement : %s n'est PAS un sous-ensemble de %s "
                  "(%d protocole(s) manquant(s), ex: %s)"
                  % (fam_order[j], fam_order[j+1], len(missing), next(iter(missing))))
        else:
            print("  [ok] %s subset %s (echantillons, %d <= %d protocoles)"
                  % (fam_order[j], fam_order[j+1], len(small), len(big)))
    # 2) verifie la monotonie de k_min induite
    kmins = [kmin(results[(pname, f)]['first_divergence']) for f in fam_order]
    for j in range(len(fam_order)-1):
        k_small = kmins[j] if kmins[j] is not None else float('inf')
        k_big   = kmins[j+1] if kmins[j+1] is not None else float('inf')
        if k_big > k_small:
            print("  !! VIOLATION monotonie : k_min(%s)=%s > k_min(%s)=%s"
                  % (fam_order[j+1], kmins[j+1], fam_order[j], kmins[j]))
        else:
            print("  [ok] k_min(%s)=%s <= k_min(%s)=%s"
                  % (fam_order[j+1], kmins[j+1], fam_order[j], kmins[j]))

# ================================================================ N = 6
N6 = 6
with open(_lp('nerode_pairs.pkl'), 'rb') as f:
    saved = pickle.load(f)
A1_6 = saved['A1_6']
phisA, phisAp = saved['phisA'], saved['phisAp']   # paire A : symetrie miroir mono-axe

def tau6_from_phis(phis_deg5, N=N6):
    # phis_deg5 = [phi1,phi2,phi3,phi4,phi5] en degres, noeud 0 fixe a (mag,0)
    tau = np.zeros((N, d))
    tau[0] = mag*np.array([1.0, 0.0])
    for k, phi in enumerate(phis_deg5):
        tau[k+1] = mag*np.array([np.cos(np.radians(phi)), np.sin(np.radians(phi))])
    return tau

tau_A  = tau6_from_phis(phisA)
tau_Ap = tau6_from_phis(phisAp)

# Paire B : minee dans zoom_deep_genealogy.pkl (meme chambre a k=4, separee a k=6).
# ATTENTION convention : dans zoom_deep_genealogy.py, phi3_fixed = 2.0 EST DEJA
# EN RADIANS (pas de np.radians() applique dessus), contrairement a phi1,phi2
# qui eux sont en degres puis convertis. On reconstruit tau a la main pour
# respecter exactement cette convention plutot que de reutiliser tau6_from_phis.
phi1_fixed_B, phi2_fixed_B, phi3_fixed_B_rad = np.radians(10.0), np.radians(40.0), 2.0
phi4_B, phi5_B   = -5.0, 0.08474576271186418
phi4_Bp, phi5_Bp = -5.0, 0.5932203389830502

def tau6_B(phi4_deg, phi5_deg):
    tau = np.zeros((N6, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed_B), np.sin(phi1_fixed_B)])
    tau[2] = mag*np.array([np.cos(phi2_fixed_B), np.sin(phi2_fixed_B)])
    tau[3] = mag*np.array([np.cos(phi3_fixed_B_rad), np.sin(phi3_fixed_B_rad)])
    tau[4] = mag*np.array([np.cos(np.radians(phi4_deg)), np.sin(np.radians(phi4_deg))])
    tau[5] = mag*np.array([np.cos(np.radians(phi5_deg)), np.sin(np.radians(phi5_deg))])
    return tau

tau_B  = tau6_B(phi4_B, phi5_B)
tau_Bp = tau6_B(phi4_Bp, phi5_Bp)

pairs_N6 = {
    'Pair A (symetrie miroir mono-axe, noeud 0)': (tau_A, tau_Ap, 'attendue: separee par U4/U3, PAS par U5 (symetrie H=V=0 exacte)'),
    'Pair B (meme chambre a k=4, separee a k=6, coin (0,0))': (tau_B, tau_Bp, 'attendue: separable, profondeur minimale a determiner (reference k=6)'),
}

families_N6 = {
    'U5 (mono-axe, noeud 0)': family_U5(node=0),
    'U4 (2D constant, noeud 0)': family_U4(node=0),
    'U3 (2D constant, noeud in {0,1,2,3,4,5})': family_U3(list(range(N6))),
}

print("="*70)
print("N=6 : |Aut(A1_6)| =", len(automorphisms(A1_6, N6)))
print("="*70)

for pname, (tx, txp, note) in pairs_N6.items():
    print("\n--- %s ---  (%s)" % (pname, note))
    for fname, fam in families_N6.items():
        t0 = time.time()
        fd, px, pxp = run_pair_family(A1_6, N6, tx, txp, fam, K=K_MAX)
        ok = summarize(fname, fd, fam)
        results[(pname, fname)] = dict(first_divergence=fd, protocols=fam, separated=ok,
                                        path_x=px, path_xp=pxp, dt=time.time()-t0)
    check_nesting_and_monotonicity(pname, ['U5 (mono-axe, noeud 0)', 'U4 (2D constant, noeud 0)',
                                            'U3 (2D constant, noeud in {0,1,2,3,4,5})'], families_N6, results)

# ================================================================ N = 9
N9 = 9
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

# Paire C : minee dans n9_depth_growth_4branches_zoom.pkl, branche {2,4,6},
# meme chambre a k=1, scission structurelle mediee par (2,6) a k=2.
phi2_C, phi6_C  = 341.64406779661016, 358.52542372881356
phi2_Cp, phi6_Cp = 341.64406779661016, 359.03389830508473
tau_C  = tau9(phi2_C, phi6_C)
tau_Cp = tau9(phi2_Cp, phi6_Cp)

pairs_N9 = {
    'Pair C ({2,4,6}, scission (2,6) a k=2)': (tau_C, tau_Cp, 'attendue: separable, profondeur minimale a determiner (reference k=2)'),
}

families_N9 = {
    'U5 (mono-axe, noeud 0)': family_U5(node=0),
    'U4 (2D constant, noeud 0)': family_U4(node=0),
    'U3 (2D constant, noeud in {0,2,4,6})': family_U3([0,2,4,6]),
}

print("\n" + "="*70)
print("N=9 : |Aut(A1_9)| =", len(automorphisms(A1_9, N9)))
print("="*70)

for pname, (tx, txp, note) in pairs_N9.items():
    print("\n--- %s ---  (%s)" % (pname, note))
    for fname, fam in families_N9.items():
        t0 = time.time()
        fd, px, pxp = run_pair_family(A1_9, N9, tx, txp, fam, K=K_MAX)
        ok = summarize(fname, fd, fam)
        results[(pname, fname)] = dict(first_divergence=fd, protocols=fam, separated=ok,
                                        path_x=px, path_xp=pxp, dt=time.time()-t0)
    check_nesting_and_monotonicity(pname, ['U5 (mono-axe, noeud 0)', 'U4 (2D constant, noeud 0)',
                                            'U3 (2D constant, noeud in {0,2,4,6})'], families_N9, results)

with open(_lp('nerode_matrix_results.pkl'), 'wb') as f:
    pickle.dump(results, f)
print("\nSauvegarde -> nerode_matrix_results.pkl")
