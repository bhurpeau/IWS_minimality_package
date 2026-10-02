"""
Recherche d'un contre-exemple a la separation par U4 (Benoit) : une paire
x,x' separee par un seul noeud force different de 0 (donc par U3\\U4), mais
PAS separee par U4 (noeud 0 seul, 2D, toute amplitude/direction testee)
jusqu'a une profondeur genereuse.

Pas un scan aveugle : on exploite le mecanisme du Lemme de transport
(Delta_tau garde une direction FIXE dans l'espace (N,d), fixee par Delta_tau(0),
tant que les deux branches restent confondues structurellement -- seul son
module decroit en e^{-beta t}). Le pouvoir separant d'une famille U tient a
sa capacite a amener, a un Kairos donne, une comparaison cos_sim qui PROJETTE
sur la direction de Delta_tau restante. Idee : concentrer Delta_tau(0) sur UN
SEUL noeud m != 0, choisi parmi les noeuds qui ne sont jamais (ou rarement)
le site i* ni un candidat nb/nn direct de i*=0 a profondeur 1 sous forcage
noeud-0 -- en esperant que U4 (noeud 0 toujours i* ou presque) ne "voit"
jamais ce noeud a temps, alors que le forcer directement (U3\\U4) le rend
immediatement pertinent (il devient i* lui-meme, ou un voisin/non-voisin
direct du nouveau i*).

Graphe temoin N=6 (A1_6, chambre "garde=1"), edges = 0-1,0-2,0-3,1-4,2-5,3-4,3-5,4-5.
nb(0)={1,2,3}, nn(0)={4,5} -> a i*=0, TOUS les autres noeuds sont deja dans
l'horizon de comparaison du premier saut. On teste neanmoins systematiquement
chaque noeud m, a plusieurs profondeurs K, parce que l'intuition seule ne
suffit pas a trancher (c'est exactement la mise en garde de Benoit : chercher
"moins aveuglement", pas "sans verifier").
"""
import sys, numpy as np, time, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_separating_families import run_pair_family, summarize
from iws_kairos_core_gen import automorphisms, d

N6 = 6
# IMPORTANT (bug trouve puis corrige) : A1_6 doit etre le graphe REEL de la
# chambre "garde=1" tel qu'obtenu par simulation (sauvegarde dans
# nerode_pairs.pkl), pas un edge-list retape a la main -- une premiere
# version de ce script utilisait un graphe DIFFERENT (memes 8 aretes
# "typiques" du temoin mais sur la mauvaise chambre), avec une structure
# d'automorphismes differente (2 au lieu de ce qui est effectivement observe
# ici) et donc des resultats non comparables au reste du chantier.
with open('nerode_pairs.pkl', 'rb') as f:
    _saved = pickle.load(f)
A1_6 = _saved['A1_6']
mag = 0.3

AMPS = [1.5, 2.5, 3.5]
ANGS = [0, 15, 37, 60, 90, 120, 160, 200, 250, 290, 330]
def family(node):
    return [(node, amp*np.cos(np.radians(ang)), amp*np.sin(np.radians(ang)))
            for amp in AMPS for ang in ANGS]

def tau6_generic(angles5, pert_node=None, delta=0.0):
    # angles5 : angles (deg) des noeuds 1..5 ; pert_node in {1..5} recoit +delta
    tau = np.zeros((N6, d))
    tau[0] = mag*np.array([1.0, 0.0])
    for k in range(5):
        a = angles5[k] + (delta if (pert_node == k+1) else 0.0)
        tau[k+1] = mag*np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    return tau

K_DEEP = 12

baselines = [
    [80.0, 160.0, 250.0, 310.0, 30.0],
    [5.0, 95.0, 185.0, 275.0, 350.0],
    [20.0, 40.0, 60.0, 80.0, 100.0],
]
deltas = [0.3, 1.0, 3.0]

print("Graphe : |Aut(A1_6)| =", len(automorphisms(A1_6, N6)))
print("Recherche de contre-exemple a U4 : U4(noeud 0) echoue, U(noeud m!=0) reussit\n")

found_any = False
t_start = time.time()
for b_i, base in enumerate(baselines):
    for m in [1,2,3,4,5]:
        for delta in deltas:
            tau_x  = tau6_generic(base, pert_node=None, delta=0.0)
            tau_xp = tau6_generic(base, pert_node=m, delta=delta)

            fam0 = family(0)
            fd0, _, _ = run_pair_family(A1_6, N6, tau_x, tau_xp, fam0, K=K_DEEP)
            sep0 = any(v is not None for v in fd0)
            k0 = min([v for v in fd0 if v is not None], default=None)

            famm = family(m)
            fdm, _, _ = run_pair_family(A1_6, N6, tau_x, tau_xp, famm, K=K_DEEP)
            sepm = any(v is not None for v in fdm)
            km = min([v for v in fdm if v is not None], default=None)

            tag = ""
            if (not sep0) and sepm:
                tag = "  <<<< CONTRE-EXEMPLE CANDIDAT (U4 echoue, U(noeud %d) reussit)" % m
                found_any = True
            print("baseline#%d noeud=%d delta=%.1f : U4(0) %s (k=%s) | U(%d) %s (k=%s)%s"
                  % (b_i, m, delta, "SEP" if sep0 else "non-sep", k0, m,
                     "SEP" if sepm else "non-sep", km, tag))

print("\n(%.1fs)" % (time.time()-t_start))
if not found_any:
    print("\nAucun contre-exemple trouve dans cette grille structuree "
          "(baselines x noeuds x deltas) -- a elargir si Benoit veut pousser.")

# ---------------------------------------------------------------------------
# SUITE (apres premiere passe) : les deux candidats les plus nets trouves
# ci-dessus ("U4(0) non-sep jusqu'a k=12" sur la grille a 33 protocoles) ont
# ete stress-testes avec une grille dense (10 amplitudes x 36 angles = 360
# protocoles, meme noeud 0) et une profondeur poussee a k=20 -- DANS LES
# DEUX CAS, la separation reapparait via le noeud 0 seul (a k=5 et k=4
# respectivement), juste via un protocole absent de la grille a 33 points
# (angle ~110 deg, hors des 11 angles testes). Conclusion : ces deux
# candidats sont des artefacts de sous-echantillonnage de U4_hat (33 pts),
# pas des contre-exemples a U4 (famille mathematique). Meme lecon que le
# bug d'emboitement U3/U4 trouve par Benoit, mais cote "non-separation"
# cette fois : il faut stress-tester un U4(0) dense avant de conclure a un
# echec de la famille, pas seulement constater l'echec de l'echantillon de
# reference a 33 points.
