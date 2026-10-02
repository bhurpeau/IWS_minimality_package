import pathlib as _pathlib
_pathlib.Path(__file__).resolve().parent.joinpath('figures').mkdir(exist_ok=True)
import numpy as np

# ---------------------------------------------------------------------------
# Etape 1 du programme "F_y / ~_N" : fixer y=(A,H,V,P) (donc i*), faire varier
# tau, caracteriser la partition de F_y induite par le comportement observable
# au PROCHAIN Kairos (le graphe A_suivant, seule chose qui depend de tau ici :
# H,V,P ne jouent aucun role dans le choix retires/ajoutes, seulement dans le
# DECLENCHEMENT du Kairos, deja fixe puisque y est fixe).
#
# Temoin N=6 (celui de tout ce fil) : i*=0, nb(0)={1,2,3}, nn(0)={4,5}.
# m = min(2,|nb|,|nn|) = 2 : |nn|=2 -> "ajoutes" est toujours {4,5} (trivial).
# Toute la combinatoire est donc dans "retires" = les 2 candidats de nb(0) de
# plus faible similarite a tau_0, i.e. le complementaire du candidat KEPT de
# plus forte similarite (argmax des cosinus).
# ---------------------------------------------------------------------------

def cos(phi):
    return np.cos(phi)

# phi_j := angle(tau_j) - angle(tau_0) ; seule la difference compte pour le cosinus.
phi3_fixed = 2.0  # generique (evite 0, +-pi/2, +-pi qui sont des points speciaux)

n = 361
phi1 = np.linspace(0, 2*np.pi, n, endpoint=False)
phi2 = np.linspace(0, 2*np.pi, n, endpoint=False)
P1, P2 = np.meshgrid(phi1, phi2, indexing='ij')

f1, f2, f3 = cos(P1), cos(P2), cos(phi3_fixed)
kept = np.where((f1 >= f2) & (f1 >= f3), 1, np.where((f2 >= f1) & (f2 >= f3), 2, 3))

# --- verification : nombre fini de regions (composantes connexes de chaque classe) ---
from scipy import ndimage
labels_summary = {}
for k in (1, 2, 3):
    mask = (kept == k)
    # torus: on double le tableau pour capter les composantes qui traversent le bord
    mask2 = np.tile(mask, (2, 2))
    lab, num = ndimage.label(mask2)
    # composantes touchant le "coeur" (premier tile) : approx du compte reel sur le tore
    core_labels = set(np.unique(lab[:n, :n])) - {0}
    labels_summary[k] = len(core_labels)

print("=== Etape 1 : partition P_1 sur le temoin N=6 (phi3 fixe =", phi3_fixed, "rad) ===")
print("  aires (fraction du carre phi1 x phi2) :",
      {k: round((kept == k).mean(), 4) for k in (1, 2, 3)})
print("  nb composantes connexes (sur le tore, approx) :", labels_summary)
print("  => partition en un nombre FINI de regions, comme attendu analytiquement")
print("     (kept = argmax_j cos(phi_j), j in {1,2,3} ; seul l'ordre des 3 valeurs compte)")

# --- figure ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Okabe-Ito (colorblind-safe) : bleu, orange, vert bleuté
okabe_ito = ["#0072B2", "#E69F00", "#009E73"]
cmap = ListedColormap(okabe_ito)

fig, ax = plt.subplots(figsize=(6.2, 6.0), dpi=150)
ax.set_facecolor("white")
im = ax.pcolormesh(np.degrees(phi1), np.degrees(phi2), kept.T, cmap=cmap,
                    vmin=0.5, vmax=3.5, shading="nearest")

# murs "transverses" (coincidence de valeur, cos(phi1)=cos(phi2) via phi1=-phi2) : trait fin
for branch in (-1, 1):
    xs = np.degrees(phi1)
    ys = np.degrees((branch * phi1) % (2*np.pi))
    order = np.argsort(xs)
    if branch == -1:
        ax.plot(xs[order], ys[order], color="0.15", lw=1.0, ls=(0, (2, 2)),
                 label="mur transverse : cos φ1=cos φ2 (φ1=−φ2), pas de symétrie de graphe")

# mur "structurel" (tau_1 = tau_2 comme vecteurs : phi1=phi2, correspond a l'automorphisme sigma) : trait épais
xs = np.degrees(phi1)
ys = np.degrees(phi1 % (2*np.pi))
order = np.argsort(xs)
ax.plot(xs[order], ys[order], color="black", lw=2.2,
         label="mur structurel : τ₁=τ₂ (lieu fixe de σ=(1 2)(4 5) ∈ Aut(A))")

ax.axhline(np.degrees(phi3_fixed), color="0.4", lw=0.8, ls=":")
ax.axvline(np.degrees(phi3_fixed), color="0.4", lw=0.8, ls=":")
ax.set_xlabel(r"$\varphi_1 = \angle(\tau_1)-\angle(\tau_0)$  (deg)")
ax.set_ylabel(r"$\varphi_2 = \angle(\tau_2)-\angle(\tau_0)$  (deg)")
ax.set_title(r"$P_1$ sur $F_y$ (témoin N=6) — nœud gardé parmi $\{1,2,3\}$, $\varphi_3$ fixé")
ax.set_xlim(0, 360); ax.set_ylim(0, 360)
ax.set_xticks([0, 90, 180, 270, 360]); ax.set_yticks([0, 90, 180, 270, 360])

# légende catégorielle (jamais couleur seule)
from matplotlib.patches import Patch
handles = [Patch(facecolor=okabe_ito[i], label=f"gardé = nœud {i+1}") for i in range(3)]
handles += [plt.Line2D([0], [0], color="black", lw=2.2, label="mur structurel (τ₁=τ₂, ∈ Fix(σ))"),
            plt.Line2D([0], [0], color="0.15", lw=1.0, ls=(0, (2, 2)), label="mur transverse (coïncidence de valeur)")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=1, fontsize=8, frameon=False)

fig.tight_layout()
fig.savefig(str(_pathlib.Path(__file__).resolve().parent / 'figures' / 'partition_Fy_N6_etape1.png'), bbox_inches="tight")
print("\nFigure sauvegardée.")
