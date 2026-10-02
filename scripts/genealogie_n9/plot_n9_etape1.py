import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

d = pickle.load(open('/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/n9_etape1.pkl','rb'))
PHI2, PHI6, lab_arr, path_to_id, n_grid = d['PHI2'], d['PHI6'], d['lab_arr'], d['path_to_id'], d['n_grid']

okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#CC79A7"]
n_lab = lab_arr.max()+1
cmap = ListedColormap(okabe_ito[:n_lab])
norm = BoundaryNorm(np.arange(-0.5,n_lab+0.5,1), cmap.N)

fig, ax = plt.subplots(figsize=(7.5,7))
im = ax.pcolormesh(PHI2, PHI6, lab_arr, cmap=cmap, norm=norm, shading="nearest")
ax.set_xlabel(r"$\varphi_2$ (deg)"); ax.set_ylabel(r"$\varphi_6$ (deg)")
ax.set_title("Témoin N=9 — partition à profondeur 1 sur (φ₂,φ₆)")
ax.set_aspect("equal")

# legende avec les labels de voisinage
labels_sorted = sorted(path_to_id.items(), key=lambda kv: kv[1])
handles = [plt.Rectangle((0,0),1,1, color=okabe_ito[pid]) for _,pid in labels_sorted]
legend_labels = ["{%s}" % ",".join(map(str,sorted(path[0][1]))) for path,_ in labels_sorted]
ax.legend(handles, legend_labels, title="nouveau voisinage de 0", loc="upper right", fontsize=9)

fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/partition_Fy_N9_etape1.png", dpi=150)
print("Figure sauvegardée.")
