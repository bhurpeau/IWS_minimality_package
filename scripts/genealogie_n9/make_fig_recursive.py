import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
d3 = pickle.load(open(_lp('zoom_deep_genealogy.pkl'),'rb'))
PHI4, PHI5, label_maps, n_grid = d3['PHI4'], d3['PHI5'], d3['label_maps'], d3['n_grid']
fig, axes = plt.subplots(1,3, figsize=(15,5), dpi=150)
for ax, depth in zip(axes, [4,6,7]):
    arr = label_maps[depth].reshape(n_grid,n_grid)
    n_lab = arr.max()+1
    ax.pcolormesh(PHI4, PHI5, arr, cmap="tab20", shading="nearest")
    ax.set_title(f"k={depth} : {n_lab} chambre(s)")
    ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
    ax.set_aspect("equal")
fig.suptitle("Motif de raffinement récursif local (témoin N=6, coin $(0^\\circ,0^\\circ)$)", fontsize=12)
fig.tight_layout(rect=[0,0,1,0.93])
fig.savefig("../../output/opacity_recursive_refinement.pdf", bbox_inches="tight")
print("OK recursive_refinement")
