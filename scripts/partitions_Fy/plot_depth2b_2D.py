import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import pathlib as _pathlib
_pathlib.Path(__file__).resolve().parent.joinpath('figures').mkdir(exist_ok=True)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

data_old = np.load(_lp("depth2b_grid.npy"), allow_pickle=True).item()
data_new = np.load(_lp("depth2b_2D_grid.npy"), allow_pickle=True).item()

okabe_ito = ["#0072B2", "#E69F00", "#009E73"]
label_map = {1:0, 4:1, 5:2}

fig, axes = plt.subplots(1, 2, figsize=(11.5,6.0), dpi=150)
for ax, data, title in [(axes[0], data_old, "forçage 1D (U,0)  — référence"),
                          (axes[1], data_new, "forçage 2D générique (37°) — contrôle")]:
    PHI4, PHI5, kept = data["PHI4"], data["PHI5"], data["kept_label"]
    kept_idx = np.vectorize(lambda x: label_map.get(x, 3))(kept)
    cmap = ListedColormap(okabe_ito + ["#999999"])
    ax.pcolormesh(PHI4, PHI5, kept_idx, cmap=cmap, vmin=-0.5, vmax=3.5, shading="nearest")
    ax.set_xlabel("φ4 (deg)"); ax.set_ylabel("φ5 (deg)")
    ax.set_title(title, fontsize=10)
    ax.set_xlim(0,360); ax.set_ylim(0,360)
    ax.set_xticks([0,90,180,270,360]); ax.set_yticks([0,90,180,270,360])

handles = [Patch(facecolor=okabe_ito[0], label="gardé = nœud 1 (dominant)"),
           Patch(facecolor=okabe_ito[1], label="gardé = nœud 4"),
           Patch(facecolor=okabe_ito[2], label="gardé = nœud 5")]
fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9, frameon=False, bbox_to_anchor=(0.5,-0.02))
fig.suptitle("Chambre « gardé=1 » (Aut(A₁)=1) : les bandes {4,5} survivent au forçage générique", fontsize=11)
fig.tight_layout(rect=[0,0.05,1,0.95])
fig.savefig(str(_pathlib.Path(__file__).resolve().parent / 'figures' / 'partition_Fy_N6_etape2_kept1_compare.png'), bbox_inches="tight")
print("Figure sauvegardée.")

for label,data in [("1D",data_old), ("2D",data_new)]:
    kept = data["kept_label"]
    for v in (1,4,5):
        print(f"  [{label}] aire kept={v} : {100*(kept==v).mean():.2f}%")
