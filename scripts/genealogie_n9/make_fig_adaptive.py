import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle
import os
okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]

d = pickle.load(open(_lp('adaptive_refine.pkl'),'rb'))
PHI4_0, PHI5_0, lab_0, flagged, n0 = d['PHI4_0'], d['PHI5_0'], d['lab_0'], d['flagged'], d['n0']
step = 360.0/n0

d2 = pickle.load(open(_lp('adaptive_refine_zoom2.pkl'),'rb'))
PHI4s, PHI5s, labs = d2['site2_haut']['PHI4'], d2['site2_haut']['PHI5'], d2['site2_haut']['lab']

fig, axes = plt.subplots(1,2, figsize=(12,5.8), dpi=150)

ax = axes[0]
n_lab = lab_0.max()+1
cmap = ListedColormap(okabe_ito[:max(n_lab,1)])
norm = BoundaryNorm(np.arange(-0.5,n_lab+0.5,1), cmap.N)
ax.pcolormesh(PHI4_0, PHI5_0, lab_0, cmap=cmap, norm=norm, shading="nearest")
for (i,j) in flagged:
    ax.add_patch(Rectangle((PHI4_0[i,j], PHI5_0[i,j]), step, step,
                            fill=False, edgecolor="black", linewidth=0.9))
ax.set_title("Grille grossière %dx%d — %d/%d cellules raffinées" % (n0,n0,len(flagged),n0*n0), fontsize=10.5)
ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
ax.set_aspect("equal")

ax = axes[1]
n_lab2 = labs.max()+1
cmap2 = ListedColormap(okabe_ito[:max(n_lab2,1)])
norm2 = BoundaryNorm(np.arange(-0.5,n_lab2+0.5,1), cmap2.N)
ax.pcolormesh(PHI4s, PHI5s, labs, cmap=cmap2, norm=norm2, shading="nearest")
ax.set_title(r"Second site riche : $\varphi_4\simeq214^\circ$, $\varphi_5\simeq11^\circ$ (%d chambres)" % n_lab2, fontsize=10.5)
ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
ax.set_aspect("equal")

fig.suptitle("Raffinement adaptatif sur le tore complet (témoin N=6)", fontsize=12)
fig.tight_layout(rect=[0,0,1,0.94])
fig.savefig("../../output/opacity_adaptive_refinement.pdf", bbox_inches="tight")
fig.savefig("../../output/opacity_adaptive_refinement.png", bbox_inches="tight", dpi=150)
print("OK adaptive_refinement")
