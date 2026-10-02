import sys, numpy as np, time, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_separating_families import run_pair_family, summarize, K_MAX
from iws_kairos_core_gen import automorphisms, build_A_from_label, d

mag = 0.3
def vec(phi_deg):
    r = np.radians(phi_deg); return mag*np.array([np.cos(r), np.sin(r)])

# ---------------- N=6, chambre "garde=1" (Aut(A1)={e}) ----------------
N6 = 6
edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0_6 = np.zeros((N6,N6))
for i,j in edges0: A0_6[i,j]=A0_6[j,i]=1
A1_6 = A0_6.copy()
A1_6[0,2]=A1_6[2,0]=0; A1_6[0,3]=A1_6[3,0]=0; A1_6[0,4]=A1_6[4,0]=1; A1_6[0,5]=A1_6[5,0]=1
print("|Aut(A1_6)| [garde=1] =", len(automorphisms(A1_6, N6)))

def tau6(phis):
    t = np.zeros((N6,d)); t[0] = mag*np.array([1.0,0.0])
    for i in range(1,6): t[i] = vec(phis[i-1])
    return t

# Pair A : symetrie de reflexion induite par le forcage mono-axe sur le noeud 0.
# Sous u0=(U,0), H_y,V_y restent nuls (deja verifie plus tot dans la session),
# donc le systeme est invariant par negation simultanee de TOUS les angles.
# x et x' = -x (mod 360) doivent donc etre indiscernables sous TOUTE la famille
# U5 (mono-axe, noeud 0), quelle que soit l'amplitude -- et typiquement
# separes des que Uy != 0.
phisA = [15.0, 205.0, 100.0, 130.0, 310.0]
phisAp = [(-p) % 360 for p in phisA]
tau_A = tau6(phisA); tau_Ap = tau6(phisAp)
print("Pair A (N=6, symetrie mono-axe) :")
print("  x  :", phisA)
print("  x' :", phisAp, " (= -x mod 360)")

# Pair B/C : recherche d'une paire proche qui diverge sous le protocole
# standard (2D, 37 deg, noeud 0) a profondeur <=K_MAX -- paroi transverse /
# mecanisme combinatoire recursif pres du coin (0,0) deja documente (S4.13).
np.random.seed(0)
std_protocol = [(0, 0.3*np.cos(np.radians(37.0))/mag*mag*0+2.5*np.cos(np.radians(37.0)), 2.5*np.sin(np.radians(37.0)))]
# (le /mag*mag*0 ci-dessus est un artefact de copie, on corrige juste en dessous)
std_protocol = [(0, 2.5*np.cos(np.radians(37.0)), 2.5*np.sin(np.radians(37.0)))]

def phis_near_corner(d4, d5):
    return [10.0, 40.0, 2.0, d4, d5]   # phi1,phi2,phi3 fixes comme dans les scripts precedents, phi4,phi5 libres

candidates = []
for dx in [0.5, 1.0, 1.5, 2.0, 3.0]:
    for dy in [0.5, 1.0, 1.5, 2.0, 3.0]:
        base = (0.2, 0.2)
        p1 = phis_near_corner(base[0], base[1])
        p2 = phis_near_corner((base[0]+dx) % 360, (base[1]+dy) % 360)
        candidates.append((p1,p2))

print("\nRecherche d'une paire proche divergente sous le protocole standard (coin 0,0)...")
found_BC = None
for p1,p2 in candidates:
    fd,_,_ = run_pair_family(A1_6, N6, tau6(p1), tau6(p2), std_protocol, K=K_MAX)
    if fd[0] is not None:
        found_BC = (p1,p2,fd[0])
        print(f"  trouve : {p1} vs {p2} -> divergent a profondeur {fd[0]}")
        break
if found_BC is None:
    print("  aucune paire divergente trouvee dans la grille testee -- a elargir")
    found_BC = (phis_near_corner(0.2,0.2), phis_near_corner(1.0,3.0), None)

phisB, phisBp, depthB = found_BC
tau_B, tau_Bp = tau6(phisB), tau6(phisBp)

with open('nerode_pairs.pkl','wb') as f:
    pickle.dump(dict(A1_6=A1_6, phisA=phisA, phisAp=phisAp, phisB=phisB, phisBp=phisBp, depthB=depthB), f)
print("\nPaires sauvegardees -> nerode_pairs.pkl")
