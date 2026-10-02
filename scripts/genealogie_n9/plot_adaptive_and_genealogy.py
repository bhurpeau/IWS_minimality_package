import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle

okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]

# ---- figure 1 : carte grossiere + cellules raffinees ----
d = pickle.load(open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/adaptive_refine.pkl','rb'))
PHI4_0, PHI5_0, lab_0, flagged, n0 = d['PHI4_0'], d['PHI5_0'], d['lab_0'], d['flagged'], d['n0']
step = 360.0/n0

fig, ax = plt.subplots(figsize=(7,7))
n_lab = lab_0.max()+1
cmap = ListedColormap(okabe_ito[:max(n_lab,1)])
norm = BoundaryNorm(np.arange(-0.5,n_lab+0.5,1), cmap.N)
ax.pcolormesh(PHI4_0, PHI5_0, lab_0, cmap=cmap, norm=norm, shading="nearest")
for (i,j) in flagged:
    ax.add_patch(Rectangle((PHI4_0[i,j], PHI5_0[i,j]), step, step,
                            fill=False, edgecolor="black", linewidth=0.8))
ax.set_title("Grille grossière (%dx%d) — cellules raffinées en noir (%d/%d)" % (n0,n0,len(flagged),n0*n0))
ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_adaptive_overview.png", dpi=150)
print("Figure 1 sauvegardée.")

# ---- figure 2 : zoom sur le deuxieme site trouve ----
d2 = pickle.load(open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/adaptive_refine_zoom2.pkl','rb'))
fig, axes = plt.subplots(1,2, figsize=(11,5.5))
for ax, name, title in zip(axes, ["site2_haut","site2_bas"],
                            ["site 2 : (φ4≈214°, φ5≈11°)", "site 2 : (φ4≈214°, φ5≈349°)"]):
    PHI4, PHI5, lab = d2[name]['PHI4'], d2[name]['PHI5'], d2[name]['lab']
    n_lab = lab.max()+1
    cmap = ListedColormap(okabe_ito[:max(n_lab,1)])
    norm = BoundaryNorm(np.arange(-0.5,n_lab+0.5,1), cmap.N)
    ax.pcolormesh(PHI4, PHI5, lab, cmap=cmap, norm=norm, shading="nearest")
    ax.set_title(title + " : %d chambres" % n_lab)
    ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
    ax.set_aspect("equal")
fig.suptitle("Deuxième site riche trouvé par raffinement adaptatif (inconnu avant le passage A)")
fig.tight_layout(rect=[0,0,1,0.94])
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_adaptive_site2.png", dpi=150)
print("Figure 2 sauvegardée.")

# ---- figure 3 : carte a k=6 (26 chambres) dans le coin (0,0), palette continue ----
d3 = pickle.load(open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/zoom_deep_genealogy.pkl','rb'))
PHI4, PHI5, label_maps, n_grid = d3['PHI4'], d3['PHI5'], d3['label_maps'], d3['n_grid']
fig, axes = plt.subplots(1,3, figsize=(15,5))
for ax, depth in zip(axes, [4,6,7]):
    arr = label_maps[depth].reshape(n_grid,n_grid)
    n_lab = arr.max()+1
    im = ax.pcolormesh(PHI4, PHI5, arr, cmap="tab20", shading="nearest")
    ax.set_title(f"k={depth} : {n_lab} chambre(s)")
    ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
    ax.set_aspect("equal")
fig.suptitle("Arbre de raffinement auto-similaire au coin (0°,0°) — même triplet {1,4,5} à chaque étape paire")
fig.tight_layout(rect=[0,0,1,0.93])
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_genealogie_k4_6_7.png", dpi=150)
print("Figure 3 sauvegardée.")
