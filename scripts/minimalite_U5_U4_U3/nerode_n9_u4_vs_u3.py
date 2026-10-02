"""
N=9, chambre {2,4,6} : recherche directe d'un contre-exemple a "U4 separe",
cible sur l'orbite {6,7,8} (noeuds isoles de A0, degre 0) et sur le mur
d'AJOUT plutot que de retrait (absent du temoin N=6).

A0 (edges=(0,1),(0,2),(0,3),(4,5)) : nb(0)={1,2,3}, nn(0)={4,5,6,7,8}.
m=min(2,3,5)=2 -> au premier Kairos, 2 des 3 voisins {1,2,3} sont retires
(1 garde), et 2 des 5 non-voisins {4,5,6,7,8} sont ajoutes (classement
cos_sim decroissant). La chambre {2,4,6} (deja etudiee §4.15/4.16) resulte
de : garde=2, ajoutes={4,6} -- 6 bat 5,7,8 au classement d'ajout.

Idee : {6,7,8} sont isoles dans A0 (Aut(A0)=72 = 3!(sur 1,2,3) x 3!(sur
6,7,8) x 2(sur 4,5)), donc une difference de tau portee sur ce triplet ne
touche RIEN d'autre structurellement a k=0 -- candidate naturelle pour une
difference "loin" du mecanisme (2 6) deja connu, et qui agit precisement
sur le classement d'AJOUT (6,7,8 sont tous les trois dans nn(0)).

Methode : au centre de zoom connu de {2,4,6} (phi2,phi6)=(348,12), on
perturbe phi7 (fixe a 200 deg dans le zoom d'origine) par un petit delta,
en laissant tout le reste identique. On verifie d'abord que la paire
diverge reellement sous un protocole de reference (temoin x!~_N x'), puis
on stress-teste U4(noeud 0, grille dense) contre U3 (union sur plusieurs
noeuds, meme grille dense), a profondeur genereuse.
"""
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from nerode_separating_families import run_pair_family, summarize
from iws_kairos_core_gen import automorphisms, d

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1
print("Aut(A0) =", len(automorphisms(A0, N9)))

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi8_fixed = np.radians(160.0)
phi2_c, phi6_c = 348.0, 12.0   # centre de zoom connu de la chambre {2,4,6}

def tau9_pert7(phi7_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_c)), np.sin(np.radians(phi2_c))])
    tau[3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
    tau[4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
    tau[5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_c)), np.sin(np.radians(phi6_c))])
    tau[7] = mag*np.array([np.cos(np.radians(phi7_deg)), np.sin(np.radians(phi7_deg))])
    tau[8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])
    return tau

# ---- etape 1 : confirmer la divergence sous un protocole de reference ----
ref_protocol = [(0, 2.5*np.cos(np.radians(37.0)), 2.5*np.sin(np.radians(37.0)))]
print("\nEtape 1 : recherche d'un delta sur phi7 qui separe sous le protocole de reference")
for delta in [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 60.0]:
    tau_x  = tau9_pert7(200.0)
    tau_xp = tau9_pert7(200.0 + delta)
    fd, px, pxp = run_pair_family(A0, N9, tau_x, tau_xp, ref_protocol, K=8)
    k = fd[0]
    print("  delta=%5.1f : %s (k=%s)  path_x[:3]=%s  path_xp[:3]=%s"
          % (delta, "SEPARE" if k is not None else "non-sep", k, px[0][:3], pxp[0][:3]))
