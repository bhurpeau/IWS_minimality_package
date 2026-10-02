import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

data = np.load("depth2_kept3_2D_grid.npy", allow_pickle=True).item()
PHI4, PHI5, kept = data["PHI4"], data["PHI5"], data["kept_label"]

okabe_ito = ["#009E73", "#0072B2", "#E69F00"]
label_map = {3:0, 4:1, 5:2}
kept_idx = np.vectorize(lambda x: label_map.get(x, 3))(kept)
cmap = ListedColormap(okabe_ito + ["#999999"])

fig, ax = plt.subplots(figsize=(6.4,6.0), dpi=150)
im = ax.pcolormesh(PHI4, PHI5, kept_idx, cmap=cmap, vmin=-0.5, vmax=3.5, shading="nearest")
xs = np.linspace(0,360,200)
ax.plot(xs, xs % 360, color="black", lw=2.2, label="Fix(σ) : φ4=φ5 (tie exact, survit)")
ax.plot(xs, (-xs) % 360, color="0.15", lw=1.2, ls=(0,(2,2)), label="φ4=−φ5 (n'est plus un tie)")
ax.set_xlabel("φ4 = ∠(τ4)−∠(τ0)  (deg)")
ax.set_ylabel("φ5 = ∠(τ5)−∠(τ0)  (deg)")
ax.set_title("P₂ chambre « gardé=3 », forçage 2D générique u0=(Ux,Uy), Uy≠0")
ax.set_xlim(0,360); ax.set_ylim(0,360)
ax.set_xticks([0,90,180,270,360]); ax.set_yticks([0,90,180,270,360])
handles = [Patch(facecolor=okabe_ito[0], label="gardé = nœud 3 (dominant)"),
           Patch(facecolor=okabe_ito[1], label="gardé = nœud 4"),
           Patch(facecolor=okabe_ito[2], label="gardé = nœud 5"),
           plt.Line2D([0],[0], color="black", lw=2.2, label="Fix(σ), tie exact (survit)"),
           plt.Line2D([0],[0], color="0.15", lw=1.2, ls=(0,(2,2)), label="φ4=−φ5 (disparu)")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5,-0.14), ncol=1, fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_etape2_kept3_2Dforce.png", bbox_inches="tight")
print("Figure sauvegardée.")
