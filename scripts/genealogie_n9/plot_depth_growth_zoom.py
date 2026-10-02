import pathlib as _pathlib
_pathlib.Path(__file__).resolve().parent.joinpath('figures').mkdir(exist_ok=True)
import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

d = pickle.load(open(str(_pathlib.Path(__file__).resolve().parent / 'depth_growth_zoom.pkl'),'rb'))
PHI4, PHI5, label_maps, n_grid = d['PHI4'], d['PHI5'], d['label_maps'], d['n_grid']

okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9",
             "#F0E442", "#999999", "#000000", "#332288"]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
depths = [2, 3, 4]
for ax, depth in zip(axes, depths):
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

fig.suptitle("Zoom local (~x20) autour du coin (0°,0°) — chambre « gardé=1 », N=6", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(str(_pathlib.Path(__file__).resolve().parent / 'figures' / 'partition_Fy_N6_zoom_coin.png'), dpi=150)
print("Figure sauvegardée.")
