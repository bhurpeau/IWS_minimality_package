import numpy as np, itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

N=6
edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0=np.zeros((N,N))
for i,j in edges0: A0[i,j]=A0[j,i]=1
A1=A0.copy()
A1[0,2]=A1[2,0]=0; A1[0,3]=A1[3,0]=0; A1[0,4]=A1[4,0]=1; A1[0,5]=A1[5,0]=1

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p,p)],A)]
auts0 = automorphisms(A0)
auts1 = automorphisms(A1)
print("|Aut(A0)| =", len(auts0), auts0)
print("|Aut(A1)| =", len(auts1), auts1)
swap45_fixing0 = [(0,1,2,4,3,5),(0,2,1,5,3,4)]  # juste pour info, non utilisé
print("(1 2)(4 5) encore dans Aut(A1) ?", (0,2,1,3,5,4) in auts1)

data = np.load("depth2b_grid.npy", allow_pickle=True).item()
PHI4, PHI5, kept = data["PHI4"], data["PHI5"], data["kept_label"]

okabe_ito = ["#0072B2", "#E69F00", "#009E73", "#999999"]
# labels presents : 1,4,5 (et -1 si jamais un point non resolu)
label_map = {1:0, 4:1, 5:2, -1:3}
kept_idx = np.vectorize(lambda x: label_map.get(x, 3))(kept)
cmap = ListedColormap(okabe_ito)

fig, ax = plt.subplots(figsize=(6.4,6.0), dpi=150)
im = ax.pcolormesh(PHI4, PHI5, kept_idx.T if False else kept_idx, cmap=cmap, vmin=-0.5, vmax=3.5, shading="nearest")
ax.set_xlabel(r"$\varphi_4=\angle(\tau_4)-\angle(\tau_0)$ (deg)")
ax.set_ylabel(r"$\varphi_5=\angle(\tau_5)-\angle(\tau_0)$ (deg)")
ax.set_title("P₂ à l'intérieur de la chambre gardé=1 : gardé parmi {1,4,5} au Kairos 2")
ax.set_xlim(0,360); ax.set_ylim(0,360)
ax.set_xticks([0,90,180,270,360]); ax.set_yticks([0,90,180,270,360])
handles = [Patch(facecolor=okabe_ito[0], label="gardé = nœud 1 (dominant)"),
           Patch(facecolor=okabe_ito[1], label="gardé = nœud 4"),
           Patch(facecolor=okabe_ito[2], label="gardé = nœud 5")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5,-0.13), ncol=1, fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/partition_Fy_N6_etape2.png", bbox_inches="tight")
print("Figure sauvegardée.")

# aires
tot = kept.size
for v in (1,4,5):
    print(f"  aire kept={v} : {100*(kept==v).sum()/tot:.2f}%")
