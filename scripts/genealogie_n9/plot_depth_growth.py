import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

d = pickle.load(open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/depth_growth.pkl','rb'))
PHI4, PHI5, label_maps, n_grid = d['PHI4'], d['PHI5'], d['label_maps'], d['n_grid']

okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]

fig, axes = plt.subplots(2, 2, figsize=(10, 9))
depths = [2, 3, 4, 5]
for ax, depth in zip(axes.ravel(), depths):
    arr = label_maps[depth].reshape(n_grid, n_grid)
    n_lab = arr.max() + 1
    cmap = ListedColormap(okabe_ito[:max(n_lab, 1)])
    bounds = np.arange(-0.5, n_lab + 0.5, 1)
    norm = BoundaryNorm(bounds, cmap.N)
    im = ax.pcolormesh(PHI4, PHI5, arr, cmap=cmap, norm=norm, shading="nearest")
    ax.set_title(f"profondeur k={depth} : {n_lab} chambre(s)")
    ax.set_xlabel(r"$\varphi_4$ (deg)")
    ax.set_ylabel(r"$\varphi_5$ (deg)")
    ax.set_aspect("equal")

fig.suptitle("Croissance de $\\mathcal{P}_k$ avec $k$ — chambre « gardé=1 », forçage 2D générique (N=6)",
             fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_croissance_k2a5.png", dpi=150)
print("Figure sauvegardée.")
