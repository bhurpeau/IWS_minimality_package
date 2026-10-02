import pathlib as _pathlib
_pathlib.Path(__file__).resolve().parent.joinpath('figures').mkdir(exist_ok=True)
import pickle, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open(str(_pathlib.Path(__file__).resolve().parent / 'n9_depth_growth_4branches_zoom.pkl'),'rb') as f:
    d = pickle.load(f)
results = d['results']; branch_labels = d['branch_labels']

okabe_ito = ["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#999999",
             "#000000","#8B4513","#00CED1","#FF1493"]

fig, axes = plt.subplots(2,2, figsize=(11,10))
order = [frozenset([1,4,5]), frozenset([2,4,5]), frozenset([1,4,6]), frozenset([2,4,6])]

for ax, b in zip(axes.ravel(), order):
    r = results[b]
    PHI2, PHI6 = r['PHI2'], r['PHI6']
    lab5, p2id5 = r['label_maps'][5]
    id2path = {v:k for k,v in p2id5.items()}
    uniq = sorted(np.unique(lab5))
    cmap = {pid: okabe_ito[i % len(okabe_ito)] for i,pid in enumerate(uniq)}
    n_grid = r['n_grid']
    lab_grid = lab5.reshape(n_grid, n_grid)
    rgb = np.zeros((n_grid,n_grid,3))
    for pid in uniq:
        c = matplotlib.colors.to_rgb(cmap[pid])
        rgb[lab_grid==pid] = c
    ax.imshow(np.transpose(rgb,(1,0,2)), origin='lower',
              extent=[PHI2.min(),PHI2.max(),PHI6.min(),PHI6.max()], aspect='auto')
    ax.set_title("A1 = %s  (|Aut|=... voir texte)\ncentre (%.0f,%.0f), |P_5^loc|=%d"
                  % (sorted(b), r['center'][0], r['center'][1], len(uniq)), fontsize=10)
    ax.set_xlabel(r"$\varphi_2$ (deg)"); ax.set_ylabel(r"$\varphi_6$ (deg)")
    # legende compacte : numero de chambre -> couleur (le chemin complet est dans le pickle)
    handles = []
    for rank, pid in enumerate(uniq):
        handles.append(plt.Line2D([0],[0], marker='s', color='w', markerfacecolor=cmap[pid],
                                   markersize=10, label="chambre %d" % (rank+1)))
    ax.legend(handles=handles, fontsize=7, loc='upper right', framealpha=0.85)

fig.suptitle("N=9 : 4 chambres de $k{=}1$ zoomées localement (budget égal, 3600 pts chacune), carte à $k{=}5$",
             fontsize=12)
fig.tight_layout(rect=[0,0,1,0.96])
fig.savefig(str(_pathlib.Path(__file__).resolve().parent / 'figures' / 'partition_Fy_N9_4branches_zoom_k5.png'), dpi=140)
print("Sauvegardé -> partition_Fy_N9_4branches_zoom_k5.png")
