import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import os
os.chdir('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')

d1 = np.load("depth2_kept3_grid.npy", allow_pickle=True).item()
d2 = np.load("depth2_kept3_2D_grid.npy", allow_pickle=True).item()

okabe_ito = ["#009E73", "#0072B2", "#E69F00"]
label_map = {3:0, 4:1, 5:2}
cmap = ListedColormap(okabe_ito + ["#999999"])

fig, axes = plt.subplots(1,2, figsize=(11.5,5.6), dpi=150)
xs = np.linspace(0,360,200)
titles = ["Forçage mono-axe (original)", "Forçage 2D générique, $U_y\\neq0$"]
for ax, d, title in zip(axes, [d1,d2], titles):
    PHI4, PHI5, kept = d["PHI4"], d["PHI5"], d["kept_label"]
    kept_idx = np.vectorize(lambda x: label_map.get(x, 3))(kept)
    ax.pcolormesh(PHI4, PHI5, kept_idx, cmap=cmap, vmin=-0.5, vmax=3.5, shading="nearest")
    ax.plot(xs, xs % 360, color="black", lw=2.0)
    ax.plot(xs, (-xs) % 360, color="0.15", lw=1.1, ls=(0,(2,2)))
    ax.set_xlabel(r"$\varphi_4$ (deg)"); ax.set_ylabel(r"$\varphi_5$ (deg)")
    ax.set_title(title, fontsize=11)
    ax.set_xlim(0,360); ax.set_ylim(0,360)
    ax.set_xticks([0,90,180,270,360]); ax.set_yticks([0,90,180,270,360])
    ax.set_aspect("equal")

handles = [Patch(facecolor=okabe_ito[0], label="gardé = 3"),
           Patch(facecolor=okabe_ito[1], label="gardé = 4"),
           Patch(facecolor=okabe_ito[2], label="gardé = 5"),
           plt.Line2D([0],[0], color="black", lw=2.0, label=r"$\varphi_4=\varphi_5$ (Fix($\sigma$), structurel)"),
           plt.Line2D([0],[0], color="0.15", lw=1.1, ls=(0,(2,2)), label=r"$\varphi_4=-\varphi_5$ (protocolaire)")]
fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=8.5, frameon=False, bbox_to_anchor=(0.5,-0.04))
fig.suptitle("Chambre « gardé=3 » (N=6) : séparer paroi structurelle et paroi de protocole", fontsize=12)
fig.tight_layout(rect=[0,0.05,1,0.95])
fig.savefig("/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/v57_review/fig/opacity_walls_protocol_control.pdf", bbox_inches="tight")
fig.savefig("/mnt/user-data/outputs/opacity_walls_protocol_control.png", bbox_inches="tight", dpi=150)
print("OK walls_protocol_control")
